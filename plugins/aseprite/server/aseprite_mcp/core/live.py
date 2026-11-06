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
from websockets.sync.server import serve

PORT = int(os.getenv("ASEPRITE_LIVE_PORT", "45654"))
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".aseprite-mcp")
APP_PATH_FILE = os.path.join(CONFIG_DIR, "aseprite_path")
EXTENSION_SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extension")
EXTENSION_NAME = "aseprite-mcp-live"

log = logging.getLogger(__name__)

_conn = None
_send_lock = threading.Lock()
_replies = {}
_cv = threading.Condition()
_ids = itertools.count(1)


def _handler(conn):
    global _conn
    _conn = conn
    log.info("Aseprite connected (live mode)")
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
        if _conn is conn:
            _conn = None
            log.info("Aseprite disconnected (batch mode)")


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
        global _port_busy
        while True:
            try:
                server = serve(_handler, "127.0.0.1", PORT)
            except OSError as e:
                if not _port_busy:
                    log.warning("Live mode waiting, port %s is in use: %s", PORT, e)
                _port_busy = True
                time.sleep(5)
                continue
            _port_busy = False
            log.info("Live mode listening on 127.0.0.1:%s", PORT)
            server.serve_forever()
            return

    threading.Thread(target=loop, daemon=True).start()


def port_busy():
    return _port_busy


def connected():
    return _conn is not None


def run(script, filename, timeout):
    """Run a script in the live window: (success, output), or None to fall back to batch."""
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
