---
name: pixel-art
description: Use when drawing a still pixel-art sprite, scene, icon or tile in Aseprite with the aseprite MCP tools: planning size and palette, blocking shapes, shading, outlining and checking the result.
---

# Drawing pixel art with the aseprite tools

## 1. Plan before drawing

- **Pick the canvas size by subject.** Use 16–32 px for an item or icon, 32–64 px for a character, and 64–128 px or more for a scene. Keep the size the user chose. If the open file is too small for the subject, resize that file with `resize_canvas`; never start a new file instead (see the aseprite-live skill).
- **Write down a pixel box for each part** (x, y, w, h), for example "monitor 14,9 36×27". Leave a 1–2 px margin from the edges.
- **Put each object on its own layer**, named for what it holds: `sky`, `ground`, `tree`, `character`. Layers created later sit on top.

## 2. Palette first

- **Build a ramp per material.** Call `generate_color_ramp(base, steps=3-4)` for each one, or use `apply_palette_preset` for a retro look. Aim for 8–16 colours in total.
- **Separate neighbouring materials by lightness**, not only by hue.
- **Choose one light direction** (top-left by default) and keep it for the whole piece.

## 3. Draw in passes, checking after each one

1. **Silhouette in flat colour.** Use the shape tools (`draw_rectangle_at`, `draw_ellipse_at`, `draw_polygon`, `fill_area_at`, `apply_gradient_rect`) for big forms. Use `draw_rows` for anything under about 12 px, such as faces, hands, handles and small props. These are drawn pixel by pixel, never built from shapes.
2. **Flats.** Fill each part with its base colour.
3. **Shading.** Put highlights on the lit side, and shadows on the far side and under overhangs. No pillow shading (a light centre with a dark ring). No dithering or anti-aliasing under 32 px.
4. **Outline** in one dark colour, never lighter than the fill. `outline_cel` adds 1 px outside the shape; pass `region=` for a single object.
5. **Details.** Add highlights, texture and small props.

After every pass:

- `view_sprite` (with `region="x,y,w,h"` to zoom in).
- `get_color_stats` to catch stray colours.
- `lint_sprite` to find lone pixels and detached parts.

Fix problems before moving on. If something doesn't read, change the shape, not the details.

## Clean lines

- **Straight diagonals** use equal steps (1-1-1 or 2-2-2).
- **Curves** use gradual steps (1, 2, 3, not 1, 3, 1).
- **No L-shaped doubles** on 1 px lines, and no lone pixels.
- **Objects sit fully on their surfaces** and parts stay attached: a handle touches its mug, and leaves grow from their pot.

## `draw_rows` quick reference

```
draw_rows(filename, layer_name="mug", frame_index=1, x=47, y=38,
          rows=["wCCCw..", "WWWWWhh", "WRRRW.h", "WWWWWhh", "wWWWw.."],
          legend={"W": "#ECECF4", "w": "#C8C8D8", "C": "#4A2E1C", "R": "#D05050", "h": "#C8C8D8"})
```

A `.` leaves that pixel untouched. `read_rows` returns pixels in the same format, so you can read an area, edit a few characters and draw it back.

Use `run_lua_script` only for what no dedicated tool covers. It can batch many pixels into one call, but it hides the work from the dedicated checks.
