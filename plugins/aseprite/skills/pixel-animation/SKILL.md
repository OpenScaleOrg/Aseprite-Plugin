---
name: pixel-animation
description: Use when animating a sprite or scene in Aseprite with the aseprite MCP tools: idle loops, walk cycles, attacks, ambient scene loops (clouds, steam, blinking lights), frame timing, tags and GIF export.
---

# Animating pixel art with the aseprite tools

Call `animation_workflow_guide` first: use `use_case="character"`, `"idle"` or `"environment"`.

## 1. Decide the loop

- **Animate in the file the user has open.** If it is too small or has too few frames, use `resize_canvas` and `add_frames` on that same file. Never create a new sprite, either with `create_canvas` or with `Sprite()` in Lua (see the aseprite-live skill).

- **Length and timing.** Duration = frames × frame time. Common choices are 8 frames × 120 ms (about 1 s) for ambient loops, 4–6 frames × 100–150 ms for idles, and 6–8 frames for walks.
- **Durations.** Use `add_frames(count, duration_ms)`, then `set_frame_duration_all`.
- **Tags.** Name each loop with `set_tag` (for example `idle` or `walk`), so `export_tag` can export it alone.

## 2. Static layers first

Finish the still frame first; follow the pixel-art skill. Then call `propagate_cels` to copy every layer that doesn't move (background, furniture) to all frames. Only the moving layers are redrawn after that.

## 3. Move things the right way

| What moves | How |
|---|---|
| Characters, creatures | Pose to pose. Redraw each key pose on its own frame: anticipation, action, follow-through. Use `copy_frame`, then `erase_region` the moving part and redraw it with `draw_rows`. Involve the whole body. Feet stay on one ground line unless airborne. |
| Soft bodies (slime, jelly) | Squash and stretch 30–50%, with a changed shape on every airborne frame. |
| Rigid objects, secondary motion | Use `tween_cel_positions_eased`, `offset_cel_positions` or `oscillate_cel_positions` (clouds, a floating icon, a bobbing boat). |
| Rotating parts (fan, windmill) | Draw 2–4 poses and alternate them with `copy_cel`. |
| Ambient effects (steam, sparkles, screen content, blinking LEDs) | Redraw small pixel sets per frame. Let alpha fall off as particles rise. |

Never use a tween as the main motion of a living thing.

## 4. Make loops seamless

- **The last frame must flow into the first.** For particles, use positions that are `(frame + offset) % N`. For scrolling, move by exactly one period over the loop.
- **Avoid pop-backs.** Something drifting 8 px and then jumping back reads as a glitch. Use a back-and-forth sway, or move it the full canvas width so it leaves and re-enters.
- **Check continuity** with `render_onion_skin`. Use `compare_frames` and `get_bounds` to confirm what moved and by how much.

## 5. Review and export

- **Review.** Call `view_sprite(frames="1-8")` to see every frame side by side, and `audit_animation` or `validate_scene` to find missing cels.
- **Export.** `export_animation(output.gif, scale=4-8, background="#...")` makes a shareable GIF; use `export_tag` for a single loop.
- **In live mode**, the user can also press Enter in Aseprite to play the animation.
