---
description: Create a new pixel-art sprite from a size and palette preset
argument-hint: "[size] [palette] [filename]"
---

Create a new sprite with the aseprite tools. Arguments: `$ARGUMENTS`

**Size** (first argument; default `medium`). Accept a preset or `WxH` such as `96x64`:

| Preset | Size | For |
|---|---|---|
| tile | 16×16 | tilemap tiles |
| icon | 32×32 | icons, items |
| small | 48×48 | characters |
| medium | 64×64 | general sprites |
| large | 128×128 | detailed sprites, scenes |
| gameboy | 160×144 | Game Boy screen |
| nes | 256×240 | NES screen |

**Palette** (optional): any `apply_palette_preset` name, i.e. `gameboy`, `nes`, `pico8`, `c64`, `cga`, `sweetie16`, `dawnbringer16`, `dawnbringer32`, `grayscale_4` or `monochrome`. You can also pass comma-separated hex colours.

**Filename** (optional): default `sprite.aseprite` in the working directory. Do not overwrite an existing file without asking.

Steps:
1. Call `live_status`, so the new tab opens in the user's Aseprite window if it is connected.
2. Call `create_canvas(width, height, filename)`.
3. If a palette was given, apply it: `apply_palette_preset(filename, preset)`, or `set_palette` for hex colours.
4. Reply with the size, the palette and its colour count, and the file path, and suggest a next step.

If an argument is unrecognised, list the valid presets instead of guessing.
