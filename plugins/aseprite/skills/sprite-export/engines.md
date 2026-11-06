# Engine import reference

Every engine needs the same three things for crisp pixel art:
- **Nearest/point filtering.**
- **No texture compression.**
- **A consistent pixels-per-unit scale.**

## Unity

- **Texture Import Settings:**
  - Texture Type: Sprite (2D and UI)
  - Sprite Mode: Multiple (for a sheet)
  - Filter Mode: **Point (no filter)**
  - Compression: **None**
  - Pixels Per Unit: the sprite's tile size, e.g. 16 or 32
- **Slicing:** in the Sprite Editor, use Slice → Grid By Cell Size with the frame width and height.
- **With Aseprite JSON:** the free "Aseprite Importer" package (2D Aseprite Importer in Unity 2021.2+) imports `.aseprite` files directly, including tags, so you can skip the sheet entirely.
- **Camera:** use the Pixel Perfect Camera component (URP 2D), with Assets PPU equal to the sprites' PPU.

## Godot 4

- **Project-wide filtering:** Project Settings → Rendering → Textures → Default Texture Filter: **Nearest**.
- **A strip or grid:** in `Sprite2D`, set `hframes`/`vframes`. For animation, use `AnimatedSprite2D` with SpriteFrames → "Add frames from sprite sheet", then pick the grid.
- **With JSON:** the "Aseprite Wizard" plugin imports `.aseprite` files or sheet JSON into `AnimatedSprite2D` or `AnimationPlayer`, splitting by tags.
- **Viewport:** stretch mode `viewport` and scale mode `integer` to stay pixel-perfect.

## Phaser 3

```js
// json-hash or json-array from export_spritesheet
this.load.atlas('hero', 'hero.png', 'hero.json');
// pixel-perfect rendering
new Phaser.Game({ pixelArt: true, roundPixels: true, /* ... */ });
// animations from Aseprite tags (needs list_tags=True)
this.load.aseprite('hero', 'hero.png', 'hero.json');
this.anims.createFromAseprite('hero');
```

## GameMaker

- **Import a strip:** Sprite Editor → Import Strip Image, then enter the frame count and frame size.
- **Texture group:** turn off "Interpolate colours between pixels" (Game Options → Graphics), or per texture group.
- **Animation speed:** set the sprite's speed from the Aseprite frame duration. 100 ms per frame is 10 frames per second.

## Web (HTML/CSS)

```css
img.pixel { image-rendering: pixelated; width: calc(32px * 4); }
```

Export at ×1 and scale with CSS. If it must look right in old viewers, export at the exact display scale instead.
