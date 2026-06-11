# Asset Style Guide

Use this guide when generating or editing WAJ mod assets. It captures practical style observations from official-looking card-pack samples, official UI/icon extracts, and tested published examples. Treat it as a prompt and review guide, not an official art bible.

## Global Visual Language

Prefer:

- Pixel-art or pixel-adjacent illustration with crisp silhouettes.
- Low-to-mid color count, posterized shading, and deliberate color bands.
- A restrained palette: usually one dark background family plus one or two strong accent hue families.
- Deep navy, near-black blue, dark purple, or dark desaturated backgrounds that push the subject forward.
- Clear central subject, readable at small UI sizes.
- Strong outline separation between subject and background.
- Stylized shapes over painterly realism.
- Simple but precise details: runes, stamps, metal edges, cracks, ribbons, sparks, petals, clock marks, ritual geometry.

Avoid:

- Photorealism, stock-art lighting, glossy 3D rendering, and photographic textures.
- Wide cinematic gradients, soft airbrush-heavy rendering, and noisy over-detail.
- Full UI mockups inside card art.
- Text inside card art, Buff icons, relic icons, or ordinary card illustrations unless explicitly requested.
- Too many unrelated colors in one asset. The game-like look usually comes from a narrow palette and sharp subject focus.

## Card Art

Purpose: square card images, usually wired under `ModResource/Images/Card/<PackName>/`.

Default final size:

- `512x512` square.

Style target:

- Minimal, refined illustration.
- One central object, figure, symbol, or action.
- Mostly dark single-color background, often deep navy or near-black blue.
- Subject uses two or three main color families with slight RGB/value shifts for detail.
- Use hard-edged highlights and shadow blocks rather than soft rendered volume.
- Add small motif details only if they support the card idea.

Good prompt shape:

```text
pixel-art / pixel-adjacent square card illustration, deep navy simple background,
one strong centered subject, limited palette of <main colors>, crisp silhouette,
subtle pixel shading, refined but not busy, no text, no UI frame, no photorealism
```

Review checklist:

- Does the subject read when viewed small?
- Is the background quieter than the subject?
- Are there only two or three dominant hue families?
- Is there no text or accidental UI border?
- Does the asset still look like a game card illustration after downscaling?

## Buff Icons

Purpose: tiny status icons, wired from `Data/Buff/Icon`.

Default final size:

- `31x31` final PNG.

Style target:

- Extremely simple, high contrast, iconic symbol.
- Dark or transparent-ish interior with a framed border.
- One dominant symbol: flame, eye, chain, drop, feather, clock, shard, thorn, skull-like mark, etc.
- Avoid scenes. Buff icons are symbols, not illustrations.

Color/frame rule:

- Negative/debuff icons use the red frame from `assets/buff-border-atlas.png`.
- Positive or neutral Buffs can use any non-red frame until official frame semantics are confirmed.

Prompt guidance:

```text
tiny pixel-art status icon, simple centered symbol, high contrast,
dark blue background, readable at 31x31, framed icon, no text, no scene,
limited colors
```

Processing:

- Generate larger concept art only as an intermediate.
- Simplify/crop/downscale into a `31x31` final canvas.
- Composite into the chosen Buff frame before wiring the CSV path.

## Relic Icons

Purpose: square relic icons, wired from `Data/Relic/Icon`.

Default final size:

- `128x128` final PNG.

Style target:

- Square framed icon with a centered object.
- Object can use more colors than a card, but should still have a dominant palette and clear silhouette.
- Dark blue or near-black background that does not compete with the object.
- Visible border/frame detail is expected.
- The object should feel like a collectible artifact, not a whole scene.

Prompt guidance:

```text
128x128 pixel-art relic icon, square framed border, centered magical object,
deep navy background, crisp silhouette, limited but rich palette,
small highlight details, no text, no full card UI, no photorealism
```

Review checklist:

- Is it a framed square icon rather than a full card?
- Does the central object remain readable at shop/inventory scale?
- Is the background subdued?
- Is the final PNG exactly `128x128`?

## Card-Pack Covers

Purpose: card-pack cover images, wired from `Data/CardPack/Icon` or `Text/CardPack/Icon`.

Default final size:

- `300x440` final PNG.
- For new covers, prefer template-guided full-cover generation using `assets/cardpack-cover-base-300x440.png` as the image reference. Then run `scripts/finalize_cardpack_cover.py <generated-cover> <output>` before wiring the CSV path. Use `scripts/compose_cardpack_cover.py <center-art> <output>` only as a fallback when the model cannot produce a coherent complete cover.

Observed official-like layout:

- A portrait package/cover silhouette with transparent clipped outer corners.
- Top and bottom bands should follow the base template's brushy or striped shadow/edge texture, but may be adapted by the image model to fit the pack palette.
- The English pack name sits near the upper-right or upper-center area, often overlapping the top-middle art boundary.
- The Chinese pack name sits near the lower-left area, usually large and blocky.
- The central area carries the main illustration or emblem.
- Side areas may include horizontal dark bands, pixel strips, or palette blocks.
- The palette is usually one strong theme color plus deep navy/purple shadows and light text.

Important limitation:

- Text rendering can vary by model. For high-quality models with strong image-text rendering, prefer generating the Chinese and English titles as integrated title art because it usually looks more natural than script-rendered text.
- Always review generated text closely. If the generated title is wrong, regenerate or use `compose_cardpack_cover.py` as a deterministic fallback.
- The top/bottom cover wrapper and side strips should be guided by `assets/cardpack-cover-base-300x440.png`. Do not use annotated guides or debug masks as the visual reference.

Prompt guidance for template-guided full cover:

```text
use the provided 300x440 card-pack base template as the structural guide,
complete 300x440 pixel-art card-pack cover, 15:22 portrait aspect ratio,
top brush wrapper, dark side body,
central illustration replacing the placeholder mark, upper English title,
large lower-left Chinese title, integrated blocky pixel lettering,
keep all title pixels inside the cover safe area with padding from transparent edges,
dark outlined light text, limited palette around <theme colors>,
motifs: <motifs>, Chinese title: <Chinese name>, English title: <English name>,
no guide lines, no debug rectangles, no visible placeholder question mark,
no square icon, no photorealism
```

Fallback prompt guidance for center art only:

```text
portrait pixel-art central card-pack motif art, deep navy shadow base,
central emblem/character/object, limited palette around <theme colors>,
bold readable silhouette, clean edges, no text, no title block, no border template,
no top or bottom wrapper band, no side pixel strips, no placeholder question mark,
no square icon, no photorealism
```

Recommended composition steps:

1. Ask for pack theme, Chinese name, English name, and two to four signature motifs.
2. Use `assets/cardpack-cover-base-300x440.png` as the image reference and generate a complete cover with integrated titles.
3. Run `scripts/finalize_cardpack_cover.py <generated-cover> <output>`.
4. Use `scripts/compose_cardpack_cover.py` only if full-cover generation repeatedly fails or title placement is unusable.
5. Review generated title text, top/bottom banding, center motif coverage, and edge artifacts.

For a successful copy/adapt prompt, use `cardpack-cover-prompt-examples.md`.

Layered composition rules:

- The image model should generate the complete cover when given the base template reference.
- The script should normally only finalize dimensions, alpha mask, and edge cleanup.
- Script-rendered titles are a fallback, not the default publication-quality path.
- Do not use official or third-party cover art as a pasted layer.
- Do not include specific third-party draft names or motifs in prompts.

Review checklist:

- Final output is `300x440`.
- It does not look like a square card illustration.
- Top and bottom bands read like a cover wrapper, not a plain background.
- Central motif is the main visual focus.
- Text, if present, is legible and not hallucinated.
- No green mask edge, guide line, debug rectangle, or safe-area label remains.

## Prompting Pattern

When generating a pack, keep a shared style memory:

- Theme name.
- Two or three dominant hue families.
- Background dark family.
- Signature motifs.
- Forbidden motifs.
- Asset-specific constraint: card, Buff, relic, or cover.

Example:

```text
Theme: ash ledger / contracts / burned paper.
Palette: deep navy background, ember orange, parchment beige, dark red accents.
Motifs: ledger book, wax seal, ash page, debt stamp, bell.
Avoid: modern office objects, photorealism, clean vector UI, random text.
```

Use the same palette and motifs across the pack so cards, Buffs, relics, and cover feel related.
