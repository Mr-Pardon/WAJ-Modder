# Card-Pack Cover Prompt Examples

Use this file as a practical reference for card-pack cover generation prompts. These are not fixed lore requirements; replace the theme, palette, motifs, and titles for each pack.

## Successful Pattern: Ashen Ledger

Reference result:

- `docs/images/ashen-ledger-cardpack-success.png`

Why this worked:

- It asked for a complete card-pack cover, not separate center art.
- It used the official-style cover layout vocabulary: top brush wrapper, dark side body, lower title area, and central illustration.
- It allowed generated title art instead of script-rendered text.
- It gave exact title strings while allowing natural two-line title layout.
- It kept a narrow palette: deep navy/purple, ember orange, parchment beige, dark red, pale lavender-white text.
- It used concrete motifs that visually reinforce one another: ledger, feather quill, wax seals, burned paper, ritual/debt marks.

Prompt:

```text
Use case: stylized-concept
Asset type: Witch's Apocalyptic Journey card-pack cover
Primary request: Generate a complete 300x440 pixel-art card-pack cover for a mod pack named "<English title>" / "<Chinese title>".
Style/medium: refined pixel-art / pixel-adjacent fantasy game cover, low-to-mid color count, crisp silhouettes, posterized shading, not photorealistic.
Composition/framing: exact 15:22 portrait card-pack cover layout. Preserve an official-style pack wrapper structure: jagged brush-textured top strip, dark side body, subtle side cover silhouette, large central illustration area, lower title area. The center area must be fully covered by finished art, no blank placeholder.
Scene/backdrop: <dark setting that fits the pack>, with small accent lights and atmospheric texture.
Subject: <one strong central motif or object cluster>.
Text (verbatim): English title "<English title>" in the upper-right / upper-center safe title area; Chinese title "<Chinese title>" large in the lower-left safe title area. The titles may split naturally into two lines if it improves the layout. The titles should be integrated as pixel title art with pale lavender-white letters, dark outline, and subtle purple shadow, matching the cover style.
Color palette: <dark background family>, <main accent>, <secondary material color>, <small highlight color>, pale lavender-white title text.
Constraints: all title pixels must stay inside the cover safe area with visible padding from the transparent/jagged outer edges; do not let text touch the raw image border. Use a complete card-pack cover design, not a square card illustration. The top and bottom wrapper bands should feel like part of the package design. No guide lines, no debug rectangles, no placeholder question mark, no watermark, no UI mockup, no photorealism.
```

Filled Ashen Ledger example:

```text
Use case: stylized-concept
Asset type: Witch's Apocalyptic Journey card-pack cover
Primary request: Generate a complete 300x440 pixel-art card-pack cover for a mod pack named "Ashen Ledger" / "灾厄账本".
Style/medium: refined pixel-art / pixel-adjacent fantasy game cover, low-to-mid color count, crisp silhouettes, posterized shading, not photorealistic.
Composition/framing: exact 15:22 portrait card-pack cover layout. Preserve an official-style pack wrapper structure: jagged brush-textured top strip, dark side body, subtle side cover silhouette, large central illustration area, lower title area. The center area must be fully covered by finished art, no blank placeholder.
Scene/backdrop: deep navy and dark purple magical archive, ember-lit contract ledger on a stone surface, ash sparks, red-orange ritual lines, charred paper texture.
Subject: a black feather quill writing glowing debt marks into an ancient ledger, wax seals, burned paper edges, faint account-book runes.
Text (verbatim): English title "Ashen Ledger" in the upper-right / upper-center safe title area; Chinese title "灾厄账本" large in the lower-left safe title area. The titles may split naturally into two lines if it improves the layout. The titles should be integrated as pixel title art with pale lavender-white letters, dark outline, and subtle purple shadow, matching the cover style.
Color palette: deep navy, black purple, ember orange, parchment beige, dark red, pale lavender-white title text.
Constraints: all title pixels must stay inside the cover safe area with visible padding from the transparent/jagged outer edges; do not let text touch the raw image border. Use a complete card-pack cover design, not a square card illustration. The top and bottom wrapper bands should feel like part of the package design. No guide lines, no debug rectangles, no placeholder question mark, no watermark, no UI mockup, no photorealism.
```

Post-process every generated cover:

```bash
python scripts/finalize_cardpack_cover.py <generated-cover> <final-300x440-png>
```

Review:

- Final image is `300x440`.
- Title text is correct enough for release, or regenerate.
- English and Chinese titles feel integrated with the image.
- Title pixels do not touch the outer transparent silhouette.
- Center area is complete, not a pasted square card image.
- No green/debug edge pixels remain after finalization.
