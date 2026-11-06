---
name: aseprite-live
description: Use when the user wants Claude to draw or edit in the Aseprite window they have open, asks why Aseprite shows no change, or mentions live mode, the open file, an unsaved tab, or undoing Claude's steps in Aseprite.
---

# Working live in the user's Aseprite window

The aseprite MCP server has two modes, chosen per call:

- **Live**: Aseprite is running with the *Aseprite MCP Live* extension, which connects to the server. Every tool runs its script inside that window, on the open sprite, and the canvas redraws right away.
- **Batch**: no window connected. Each tool starts a hidden Aseprite, edits the file on disk and exits. An open window will not show the change until the file is reopened.

## Start every session with `live_status`

| Result | What to do |
|---|---|
| `connected; active tab: <path>` + `saved` | Use that path as `filename` for every tool. |
| `... UNSAVED` | Ask where to keep it, then `save_active_sprite("<dir>/<name>.aseprite")` and use that path. |
| `connected; no sprite is open` | `create_canvas` opens a new tab in the window. |
| `Aseprite is not connected ...` | Tell the user. Work in batch mode only if they agree. |

## Always draw in the file the user has open (strict)

Every drawing goes into the user's open tab: the active sprite reported by `live_status`. Never put the work in a separate file.

- **Never create a second sprite.** Do not call `create_canvas`, and never call `Sprite(w, h)` in `run_lua_script`, while the user has a tab open. Use `create_canvas` only when `live_status` says no sprite is open. In Lua, edit `app.activeSprite`.
- **If the canvas is too small, resize that same file.** For example, if the open tab is 64×64 and the scene needs 160×112, call `resize_canvas(<open file>, 160, 112)` on it and then draw. Do the same for frame count: add frames to that file with `add_frames`.
- **A canvas that already has artwork gets asked about first.** `resize_canvas` scales the existing pixels, so on a blank tab just resize it; when the tab already has art, ask the user before resizing.
- **If the tab is unsaved,** save it with `save_active_sprite` (ask where), then keep working in that file. Saving it is not a reason to start another one.
- **If live mode is not connected,** stop and tell the user. Do not fall back to a new file on disk unless the user explicitly says so.

The extension installs itself into Aseprite the first time the server starts. Aseprite must then be restarted once, and on first use it asks whether the script may connect to the network or write files. The user has to allow this in Aseprite. Never click these prompts on their behalf.

## While drawing live

- **One tool call is one undo step.** The user can press Ctrl+Z to take back exactly one of your steps, so tell them that when it helps.
- **Work in visible passes** (silhouette, then flats, shading, details, animation) so the user sees the piece come together, and say what each pass does.
- **One small thing per call.** The window only redraws when a call returns, so a script that paints the whole scene shows up all at once. Each call should add one object, one layer, one shading pass or one frame. Write a script, run it, then write the next one. Never write all the scripts first and run them at the end.
  - Prefer the dedicated tools (`draw_rows`, `draw_rectangle_at`, `draw_ellipse_at`, `fill_area_at`, ...). Every one of them is a single visible step.
  - In live mode `run_lua_script` refuses scripts over 40 code lines. Keep helper functions short, since every script has to redefine its own.
  - A 64×64 scene typically takes 10–25 calls. That's expected: the user is watching it build.
- **Every step is saved** to the file, which keeps `view_sprite` and the export tools in sync. Those still read the saved file through a hidden Aseprite.
- **The user may edit too.** Check with `view_sprite` or `read_rows` before redrawing an area, and do not overwrite their changes without asking.
- **Don't change their view.** Avoid switching tabs, frames or layers in the window unless the task needs it.

## Troubleshooting

- **A tool times out with "A dialog may be open".** Aseprite is waiting on a prompt, such as a permission request. Ask the user to answer it.
- **Changes don't appear in the window.** Run `live_status`. Each call first claims the live link from any other Claude session that holds it, so if it still says not connected, Aseprite was opened before the extension was installed and needs a restart. Stop and tell the user; do not keep drawing into the file on disk.
- **Never launch Aseprite yourself.** Don't open the file in a new window with a shell command. Two windows on the same file get out of sync, and scripts only go to the window that connected last. If the open tab is stale, ask the user to use File → Revert.
- **Tabs titled like the sprite appear and close.** That is expected: some analysis tools work on a temporary copy, which is closed afterwards.
