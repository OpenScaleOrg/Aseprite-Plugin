---
name: sprite-export
description: Use when exporting pixel art from Aseprite with the aseprite MCP tools - PNG, animated GIF, spritesheets, texture atlases, JSON frame data, per-layer or per-tag export, upscaling, or preparing sprites for Unity, Godot, Phaser, GameMaker, the web or social media.
---

# Exporting pixel art

## Pick the output

| Goal | Tool | Settings |
|---|---|---|
| Still image to share | `export_frame` | scale 4–8 |
| Animation to share (Discord, X, itch.io) | `export_animation` | `.gif`, scale 4–8, `background="#..."` if transparent |
| One animation loop | `export_tag` or `export_animation(tag=...)` | Tag the loop first with `set_tag` |
| Game engine sprite | `export_spritesheet` | scale 1, `data_filename` + `data_format`, `list_tags=True` |
| Many sprites in one texture | `export_spritesheet(sheet_type="packed")` | Needs JSON so the engine knows the rects |
| Separate parts or layers | `export_layers` | One PNG per layer |
| PNG frame sequence | `export_animation(output="name.png")` | Numbered files |

## Rules that keep pixels crisp

- **Scale by whole numbers only** (×2, ×3, ×4…). Every tool scales nearest-neighbour; fractional scaling smears pixels.
- **Export game assets at ×1** and scale them in the engine, unless the user asks otherwise.
- **Keep transparency for game assets.** Add a background only for previews, which `export_animation(background=...)` does on a copy.
- **GIFs keep each frame's own duration.** Check timing with `get_sprite_info` before exporting.
- **GIFs use at most 256 colours.** Pixel art is almost always well under that.
- **Use 1–2 px of padding** on spritesheets that will be filtered or mipmapped, so edge pixels don't bleed into each other.

## Spritesheet layouts

- **`horizontal`:** one strip. Best for a single animation; most engines slice it by frame count.
- **`vertical`:** one column.
- **`rows` / `columns`:** a grid. Good for several animations, with one tag per row.
- **`packed`:** the smallest texture. Requires the JSON data.

`data_format`:
- **`json-array`:** an ordered list of frames. Easiest for Phaser and generic loaders.
- **`json-hash`:** frames keyed by name. TexturePacker-style; also read by Phaser and PixiJS.

With `list_tags=True`, the JSON includes `meta.frameTags` (name, from, to, direction). Engines and importers use that to split animations.

## After exporting

- **Report** the path, the image size, the frame count and the total duration.
- **For engine assets,** add the one import tip that matters, using the [engine import reference](engines.md).
