---
description: Show what the aseprite plugin can do and how to start
argument-hint: "[command or topic]"
---

Show help for the aseprite plugin. Topic: `$ARGUMENTS`

With no topic, show the overview below as it is. With a command name or a topic (`live`, `palettes`, `animation`, `export`, `dithering`), give only that part in more detail. For skills, summarise the relevant `SKILL.md`.

---

**Aseprite plugin.** Claude draws and animates pixel art in Aseprite, live in your open window.

**Start**
1. Open Aseprite. After the first install, restart it once and allow network access when asked.
2. `/pixel-setup` checks that everything is connected.
3. Ask for what you want, for example "draw a 32×32 potion bottle" or "animate a campfire loop in my open file".

**Commands**

| Command | What it does |
|---|---|
| `/pixel-new [size] [palette]` | New sprite, e.g. `/pixel-new icon pico8` or `/pixel-new 96x64 sweetie16` |
| `/pixel-palette <show\|set\|optimize\|ramp>` | View or change the palette |
| `/pixel-export <png\|gif\|sheet\|json>` | Export, e.g. `/pixel-export gif scale=6` |
| `/pixel-setup [aseprite-path]` | Check the connection and set the Aseprite path |
| `/pixel-help [topic]` | This help |

**Skills.** These are used automatically when relevant:
- **pixel-art:** planning, palette, passes, shading, outlines, checks
- **pixel-animation:** loops, pose-to-pose, seamless cycles
- **pixel-dithering:** dithering, anti-aliasing, colour theory, materials
- **sprite-export:** PNG, GIF, sheets, and Unity, Godot, Phaser or GameMaker import
- **aseprite-live:** working in your open window, undo, troubleshooting

**Live mode.** Each Claude step appears in your window as it happens, and Ctrl+Z undoes one step. If Aseprite is closed, tools still work on saved files in batch mode.

**Palettes:** `gameboy` (4), `cga` (4), `grayscale_4`, `monochrome`, `pico8` (16), `c64` (16), `sweetie16` (16), `dawnbringer16`, `dawnbringer32`, `nes` (55).
