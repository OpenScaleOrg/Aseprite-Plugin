---
description: Show, set or optimize a sprite's palette
argument-hint: "<show|set|optimize|ramp> [preset|colors|count|base-color] [filename]"
---

Manage a sprite's palette with the aseprite tools. Arguments: `$ARGUMENTS`

When no filename is given, use the sprite already in use in this conversation. Otherwise call `live_status` and use the active tab, saving it first with `save_active_sprite` if it is unsaved.

| Action | What to do |
|---|---|
| `show` | Call `get_palette`, then list the colours as hex. Also call `get_color_stats` to show which colours the art actually uses. |
| `set <preset>` | Call `apply_palette_preset`. Presets: `gameboy`, `nes`, `pico8`, `c64`, `cga`, `sweetie16`, `dawnbringer16`, `dawnbringer32`, `grayscale_4`, `monochrome`. Then ask whether to snap the existing pixels to it with `quantize_to_palette`. |
| `set #hex,#hex,...` | Call `set_palette` with those colours. |
| `optimize <N>` | Call `extract_palette` to build an N-colour palette from the art, then `quantize_to_palette` to snap the pixels to it. |
| `ramp <#base> [steps]` | Call `generate_color_ramp(base, steps)` to make a hue-shifted shading ramp. Offer to add it with `set_palette`. |

`set` and `optimize` change the art. In live mode, mention that a single Ctrl+Z undoes each step.
