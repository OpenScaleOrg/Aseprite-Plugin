import os
from ..core import live
from ..core.commands import command_timeout, lua_escape, reject_traversal
from .. import mcp

_NOT_CONNECTED = (
    "Aseprite is not connected, so tools run in batch mode on saved files and "
    "changes will not show in an open window. Open Aseprite (the Aseprite MCP Live "
    "extension installs itself; restart Aseprite once after the first install) "
    "and allow network access when Aseprite asks. Tell the user before creating a "
    "new file instead of working in their open one."
)
_PORT_BUSY = (
    f"Live mode is blocked: port {live.PORT} is held by another aseprite-mcp server "
    "(another Claude session, or an old server that never exited), and Aseprite is "
    "connected to that one. Tools here run in batch mode and will NOT show in the "
    "open window. Tell the user to close the other Claude session or stop the stale "
    "python 'aseprite_mcp' process; this server takes over within 5 seconds. Do not "
    "silently create a new file instead."
)


def _not_connected():
    return _PORT_BUSY if live.port_busy() else _NOT_CONNECTED


@mcp.tool()
async def live_status() -> str:
    """Report whether a running Aseprite window is connected (live mode) and what
    its active tab is.

    In live mode every tool edits the sprite open in that window, so the user
    watches changes happen and can undo each tool call with Ctrl+Z. Call this
    first when the user wants to work in the file they have open.
    """
    if not live.connected():
        return _not_connected()
    result = live.run("""
    local spr = app.activeSprite
    if not spr then print("connected; no sprite is open") return end
    print("connected; active tab: " .. spr.filename)
    print((app.fs.isFile(spr.filename) and "saved" or "UNSAVED (call save_active_sprite first)")
          .. string.format("; %dx%d, %d frame(s), %d layer(s)", spr.width, spr.height, #spr.frames, #spr.layers))
    """, "", command_timeout())
    if result is None:
        return _not_connected()
    return result[1]


@mcp.tool()
async def save_active_sprite(filename: str) -> str:
    """Save the tab that is active in the connected Aseprite window to a file.

    Tools take a filename, so an unsaved tab (e.g. "Sprite-0001") needs a path
    first. After saving, pass the same filename to any tool and it edits that
    open tab live.

    Args:
        filename: Path to save to, ending in .aseprite
    """
    if not live.connected():
        return _not_connected()
    err = reject_traversal(filename)
    if err:
        return err
    path = os.path.abspath(filename)
    result = live.run(f"""
    local spr = app.activeSprite
    if not spr then print("ERROR:no sprite is open") return end
    spr:saveAs("{lua_escape(path)}")
    print("OK")
    """, "", command_timeout())
    if result is None:
        return _not_connected()
    ok, out = result
    if not ok or out.startswith("ERROR:"):
        return f"Failed to save: {out.removeprefix('ERROR:')}"
    return f"Saved the active tab as {path}; use this filename with the other tools"
