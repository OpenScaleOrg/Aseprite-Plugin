---
description: Export a sprite as PNG, GIF, spritesheet or spritesheet + JSON
argument-hint: "<png|gif|sheet|json> [output] [scale=N] [layout=...] [tag=...] [bg=#hex]"
---

Export with the aseprite tools. Arguments: `$ARGUMENTS`

Use the sprite already in use in this conversation, or the active tab from `live_status`.

| Format | Tool | Notes |
|---|---|---|
| `png` | `export_frame(filename, frame_index, output, scale)` | Frame 1 unless `frame=N` is given |
| `gif` | `export_animation(filename, output, tag, scale, background)` | Uses each frame's own duration; `tag=` exports one loop |
| `sheet` | `export_spritesheet(..., sheet_type, scale, tag_name)` | `layout=` is `horizontal` (default), `vertical`, `rows`, `columns` or `packed` |
| `json` | `export_spritesheet(..., data_filename="<name>.json", data_format="json-array", list_tags=True)` | A PNG plus Aseprite JSON with frame rects, durations and tags. Use `json-hash` when asked. |

**Options:**
- `scale` is an integer from 1 to 8 (nearest-neighbour only).
- `bg=#hex` puts a background behind transparent GIFs, so dark outlines read in any viewer.

**Defaults:**
- The output path is the sprite's name with the right extension, next to the sprite.
- The scale is 4 for `png` and `gif`, and 1 for sheets (game engines scale in-engine).

After exporting, reply with the path, the pixel size, the frame count and the total duration. For sheets, give the engine import tip from the `sprite-export` skill.
