# Dither pattern reference

The patterns are written for `draw_rows`. `A` is the base colour, `B` is the mix colour, and the legend maps them to hex. Tile them across the area to fill it.

## Two-colour mixes

**Checkerboard, 50%.** The smoothest mix.
```
AB
BA
```

**Sparse dots, 25% B.**
```
BAAA
AAAA
AABA
AAAA
```

**Dense dots, 75% B.** The inverse of sparse dots.
```
ABBB
BBBB
BBAB
BBBB
```

**Diagonal lines, 50%.** Reads as movement or rain.
```
ABAB
BABA
```
Shift the start by one pixel each row for a 45° slant:
```
ABAA
AABA
AAAB
BAAA
```

## Bayer 4×4 ordered dither

Each threshold is out of 16. A pixel takes colour B when the blend amount (0–1) × 16 is greater than its threshold. `apply_dither_gradient` uses this matrix.
```
 0  8  2 10
12  4 14  6
 3 11  1  9
15  7 13  5
```

Pattern at each level:

| Level | Rows (B = mix colour) |
|---|---|
| 1/8 | `B...` `....` `..B.` `....` |
| 1/4 | `B.B.` `....` `B.B.` `....` |
| 3/8 | `B.B.` `.B..` `B.B.` `...B` |
| 1/2 | `B.B.` `.B.B` `B.B.` `.B.B` |
| 3/4 | `BBBB` `.B.B` `BBBB` `.B.B` |

## Gradient bands

For a stepped gradient from A to B to C, change the pattern band by band, each 2–4 px tall:
```
AAAAAAAA   solid A
ABAAABAA   25% B
ABABABAB   50%
BABBBABB   75% B
BBBBBBBB   solid B
BCBBBCBB   25% C
...
```

## Texture patterns

**Hatching.** Shadows on cloth or paper.
```
A.A.A.
.A.A.A
```
**Cross-hatching.** A deeper shadow.
```
AAAA
A.A.
AAAA
.A.A
```
**Vertical lines.** Fabric weave, wood.
```
AB
AB
```
**Horizontal lines.** Brushed metal, scanlines.
```
AA
BB
```
**Stipple.** Sand, stone, rust. Scatter irregular single pixels; avoid any repeating grid.
