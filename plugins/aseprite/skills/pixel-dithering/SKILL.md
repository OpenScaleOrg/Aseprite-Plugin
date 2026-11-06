---
name: pixel-dithering
description: Use when refining or polishing existing pixel art in Aseprite with the aseprite MCP tools - dithering (ordered/Bayer, patterns, gradients), anti-aliasing curves, hue-shifted shading, colour ramps, limited or retro palettes, contrast and readability, or material textures like metal, stone, wood, fabric and glass.
---

# Dithering, anti-aliasing and colour

## Dithering

Dithering mixes two colours with a pixel pattern to fake a third colour or a gradient.

**When to use it:**
- **Big, flat areas** at 48 px and up, such as skies, large shadows and backgrounds.
- **Tight palettes** of 4–16 colours that need more tones.
- **Textures:** stone, sand, fabric.

**When not to:**
- **Sprites under 32 px.** It reads as noise.
- **Characters' faces, or anything that moves.** It shimmers between frames.
- **Places a third palette colour would do better.** Prefer a ramp step over dithering.

**Tools:**

| Need | Tool |
|---|---|
| Gradient between two colours | `apply_dither_gradient(..., color_start, color_end, horizontal)`. This is ordered Bayer 4×4. |
| Even texture or mix | `apply_dither_pattern(..., color_a, color_b, density)`. Density 0.5 is a checkerboard; 0.25 and 0.75 are sparse dots. |
| Hand-placed pattern | `draw_rows` with the pattern spelled out. See the [pattern reference](patterns.md). |

**Rules:**
- **Dither only between neighbouring ramp colours.** Two distant colours look like a grid, not a blend.
- **Keep the transition band narrow,** 2–6 px. The solid areas carry the form.
- **Never dither across an outline or a silhouette edge.**

## Anti-aliasing (AA)

AA puts intermediate colours where a curve or diagonal steps, to soften the jaggies.

- **Use it only on internal lines and large curves, at 32 px and up.** Leave the outer silhouette against a transparent background hard. AA'd edges show halos on other backgrounds.
- **Place one AA pixel** in the inside corner of each step, coloured between the line and the fill. For long steps use 2 px: a lighter one and a darker one.
- **Check the result** with `view_sprite` (region zoom). AA that makes a line look thicker is wrong, so remove it.

## Shading with colour

- **Build every material's ramp** with `generate_color_ramp(base, steps=3-5, hue_shift_degrees=15-30)`. The shadows lean toward blue or purple, and the highlights toward yellow or orange.
- **Push contrast between materials** with lightness, not only hue. A quick check: `adjust_hsl(saturation_shift=-1)` on a copy shows whether the art reads in greyscale.
- **For mood shifts** (night, poison, a hit flash), use `adjust_hsl` on a layer, or `replace_color` / `remap_colors_in_cel_range` across frames.
- **Fitting a retro palette:** apply it with `apply_palette_preset`, then `quantize_to_palette`. Fix the spots that went muddy by hand, using colours from the same ramp.

## Materials

| Material | How it reads |
|---|---|
| Metal | High contrast. A hard, sharp highlight next to a deep shadow. Reflected light on the shadow edge. |
| Stone | Low contrast. Clustered texture, sparse dither or 2–3 px clumps, chipped edges. |
| Wood | Grain lines along the plank, in a darker step. Knots are small ellipses. |
| Fabric | Soft gradients, folds as curved darker bands, vertical-line texture for weave. |
| Glass / water | Mostly the background showing through. Bright specular dots, edge highlights, a little tint. |
| Skin | A 3–4 step warm ramp with reddish shadows. No dithering. |

After any polish pass, call `get_color_stats` to keep the palette tight, and `lint_sprite` to catch stray pixels.
