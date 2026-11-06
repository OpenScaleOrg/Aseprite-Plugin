# Changelog

## 0.4.0

- **Docs:** a new landing README with a quick start, prompt examples, a comparison table and troubleshooting.
- **Discoverability:** richer plugin and marketplace descriptions and keywords.
- **Repo files:** added a changelog, a contributing guide and issue templates.

## 0.3.4

- **Live link handover:** the Claude session that is drawing takes over the live link from other sessions automatically.
- **Several Aseprite windows:** every connected window is tracked, and if the active one closes, work goes to another.
- **Extension 0.2.1:** reconnects reliably after a drop. The reconnect delay now uses wall-clock time instead of CPU time.

## 0.3.3

- **Small steps in live mode:** `run_lua_script` refuses scripts over 40 lines, so Claude builds the picture in visible steps.

## 0.3.2

- **No surprise new files:** `create_canvas` refuses while a sprite is open in live mode. Claude draws in your open file instead.

## 0.3.1

- **Busy port:** the live link retries when another session holds the port, and `live_status` explains why.

## 0.3.0

- **Commands:** `/pixel-new`, `/pixel-palette`, `/pixel-export`, `/pixel-setup` and `/pixel-help`.
- **Skills:** `pixel-dithering` (with a pattern reference) and `sprite-export` (with engine import notes).
- **Palettes:** NES and Sweetie 16 presets.

## 0.2.0

- **Live mode:** the bundled Aseprite extension runs each tool in the open window, with one undo step per call.
- **New tools:** `live_status` and `save_active_sprite`.
- **Automatic setup:** the extension installs itself, and the Aseprite path is detected.
- **Skills:** `pixel-art`, `pixel-animation` and `aseprite-live`.
