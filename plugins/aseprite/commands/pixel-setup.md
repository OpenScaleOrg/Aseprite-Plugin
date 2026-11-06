---
description: Check the Aseprite connection and set the Aseprite path if detection failed
argument-hint: "[path-to-aseprite-executable]"
---

Check that the aseprite plugin is ready, and fix what isn't. Argument: `$ARGUMENTS`

1. **Live connection.** Call `live_status`.
   - If it is connected: report the active tab. Live mode works.
   - If it is not connected:
     - The extension installs itself to `%APPDATA%\Aseprite\extensions\aseprite-mcp-live` on Windows, `~/Library/Application Support/Aseprite/extensions/` on macOS, or `~/.config/aseprite/extensions/` on Linux. Check that the folder exists.
     - Aseprite must be restarted once after the extension is installed.
     - The first time, Aseprite asks for network access, and the user must allow it.
     - Port 45654 may be held by another Claude session's server. Closing old sessions frees it.
2. **Aseprite executable** (used by batch-mode tools such as `view_sprite` and the exports).
   - If a path argument was given, check that it exists, then write it, with nothing else, to `~/.aseprite-mcp/aseprite_path`. That is the file the server reads.
   - Otherwise, read that file if it exists. The extension writes it when Aseprite connects.
   - If neither is set, look in the common locations: `C:\Program Files\Aseprite\Aseprite.exe`, `C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe`, `/Applications/Aseprite.app/Contents/MacOS/aseprite` and `~/.steam/steam/steamapps/common/Aseprite/aseprite`.
   - Run `"<path>" --version` to confirm it works.
3. **Smoke test.** Call `create_canvas(8, 8, "<temp dir>/pixel-setup-check.aseprite")`, then `view_sprite` on it. Delete the file afterwards.

Finish with a short checklist: live connection ✓/✗, executable ✓/✗ with its path and version, smoke test ✓/✗. Add one line on how to fix each ✗.
