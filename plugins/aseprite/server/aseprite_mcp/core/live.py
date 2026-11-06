"""Live mode: run tool scripts inside a running Aseprite window.

The bundled Aseprite extension (aseprite_mcp/extension) connects to a
WebSocket server started here. When it is connected, every Lua script is
executed on the sprite open in that window, so changes appear as they
happen; otherwise scripts fall back to a batch-mode Aseprite process.

Protocol (plain text, the extension has no JSON):
    request  "<id>\\n<filename>\\n<lua script>"
    reply    "<id>\\n<1|0>\\n<printed output or error>"
    hello    "hello\\n1\\n<path of the Aseprite executable>"   (sent on connect)
"""
import filecmp
import itertools
import logging
import os
import shutil
import sys
import threading
import time

from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect
from websockets.sync.server import serve

PORT = int(os.getenv("ASEPRITE_LIVE_PORT", "45654"))
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".aseprite-mcp")
APP_PATH_FILE = os.path.join(CONFIG_DIR, "aseprite_path")
EXTENSION_SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extension")
EXTENSION_NAME = "aseprite-mcp-live"

log = logging.getLogger(__name__)

TAKEOVER_PATH = "/takeover"

_conn = None          # the Aseprite window scripts go to: the most recently connected one
_conns = []           # every connected Aseprite window
_server = None
_claiming = threading.Event()
_send_lock = threading.Lock()
_replies = {}
_cv = threading.Condition()
_ids = itertools.count(1)


def _yield_port():
    """Another Claude session wants the live link: stop listening and drop Aseprite.

    The extension reconnects within seconds and lands on the claiming server;
    this one keeps retrying the port and can claim it back on its next tool call.
    """
    global _server
    server, _server = _server, None
    if server:
        server.shutdown()
    for c in list(_conns):
        c.close()
    log.info("Handed the live link to another Claude session")


def _handler(conn):
    global _conn
    if conn.request.path == TAKEOVER_PATH:
        threading.Thread(target=_yield_port, daemon=True).start()
        return
    _conns.append(conn)
    _conn = conn
    log.info("Aseprite connected (live mode, %d window(s))", len(_conns))
    with _cv:
        _cv.notify_all()  # wakes a pending _claim()
    try:
        for msg in conn:
            rid, ok, out = msg.split("\n", 2)
            if rid == "hello":
                _remember_app_path(out)
                continue
            with _cv:
                _replies[rid] = (ok == "1", out)
                _cv.notify_all()
    except (ConnectionClosed, ValueError):
        pass
    finally:
        _conns.remove(conn)
        if _conn is conn:
            _conn = _conns[-1] if _conns else None
            log.info("Aseprite window disconnected; %d left", len(_conns))
        with _cv:
            _cv.notify_all()


def _remember_app_path(path):
    """Keep the connected Aseprite's executable for batch-mode tools."""
    if not path or os.getenv("ASEPRITE_PATH"):
        return
    os.environ["ASEPRITE_PATH"] = path
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(APP_PATH_FILE, "w", encoding="utf-8") as f:
            f.write(path)
    except OSError:
        pass


_port_busy = False


def start():
    """Start the WebSocket server in the background.

    If another process holds the port (another Claude session, or an old server
    that never exited), keep retrying so live mode starts as soon as it frees up.
    """
    def loop():
        global _port_busy, _server
        while True:
            try:
                _server = serve(_handler, "127.0.0.1", PORT)
            except OSError as e:
                if not _port_busy:
                    log.warning("Live mode waiting, port %s is in use: %s", PORT, e)
                _port_busy = True
                # Poll fast while claiming the port from another session.
                _claiming.wait(5)
                time.sleep(0.2)
                continue
            _port_busy = False
            log.info("Live mode listening on 127.0.0.1:%s", PORT)
            _server.serve_forever()   # returns when another session takes the link over
            _port_busy = True
            time.sleep(5)             # let the claiming session bind first

    threading.Thread(target=loop, daemon=True).start()


def _claim(timeout=10.0):
    """Ask the session holding the port to hand over, then wait for Aseprite to reconnect here.

    ponytail: the session making a tool call wins; two chats drawing at once
    would trade the link back and forth on every call.
    """
    _claiming.set()
    try:
        try:
            connect(f"ws://127.0.0.1:{PORT}{TAKEOVER_PATH}", open_timeout=3).close()
        except Exception:
            pass  # the holder closes on us, or the port just freed up
        with _cv:
            return _cv.wait_for(lambda: _conn is not None, timeout)
    finally:
        _claiming.clear()


def port_busy():
    return _port_busy


_last_failed_claim = 0.0


def connected():
    """True when an Aseprite window is connected here, claiming the link from
    another Claude session first if that one holds it."""
    global _last_failed_claim
    if _conn is None and _port_busy and time.monotonic() - _last_failed_claim > 30:
        if not _claim():
            _last_failed_claim = time.monotonic()  # holder too old to hand over; don't stall every call
    return _conn is not None


def run(script, filename, timeout):
    """Run a script in the live window: (success, output), or None to fall back to batch."""
    connected()
    conn = _conn
    if conn is None:
        return None
    filename = os.path.abspath(filename) if filename else ""
    rid = str(next(_ids))
    # ponytail: one script at a time; Aseprite runs them on its UI thread anyway.
    with _send_lock:
        try:
            conn.send(f"{rid}\n{filename or ''}\n{script}")
        except ConnectionClosed:
            return None
        with _cv:
            if not _cv.wait_for(lambda: rid in _replies or _conn is not conn, timeout):
                return False, (f"Aseprite did not answer within {timeout:g}s. "
                               "A dialog may be open in the Aseprite window.")
            if rid not in _replies:
                return None  # disconnected mid-request
            return _replies.pop(rid)


def extensions_dir():
    if sys.platform == "win32":
        return os.path.join(os.environ.get("APPDATA", ""), "Aseprite", "extensions")
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/Aseprite/extensions")
    return os.path.expanduser("~/.config/aseprite/extensions")


def install_extension():
    """Copy the bundled extension into Aseprite when missing or outdated.

    Returns True when files were written (Aseprite must be restarted to load them).
    """
    dest = os.path.join(extensions_dir(), EXTENSION_NAME)
    files = os.listdir(EXTENSION_SRC)
    if os.path.isdir(dest) and all(
        os.path.exists(os.path.join(dest, f)) and filecmp.cmp(os.path.join(EXTENSION_SRC, f),
                                                              os.path.join(dest, f), shallow=False)
        for f in files
    ):
        return False
    try:
        os.makedirs(dest, exist_ok=True)
        for f in files:
            shutil.copyfile(os.path.join(EXTENSION_SRC, f), os.path.join(dest, f))
    except OSError as e:
        log.warning("Could not install the Aseprite extension to %s: %s", dest, e)
        return False
    log.info("Installed the Aseprite live extension to %s; restart Aseprite to load it", dest)
    return True
