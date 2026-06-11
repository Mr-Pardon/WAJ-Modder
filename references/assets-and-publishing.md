# Assets, Game Directory, and Publishing

## Asset Generation

Asset support is part of v0. Keep constraints broad enough for new creative directions while preventing obvious style mismatch.

For visual language and prompting, use `asset-style-guide.md` together with this file. This file defines sizes, post-processing, and publishing checks; `asset-style-guide.md` defines the preferred game-like look.

Known local facts:

- `ModTemplate/Icon.png` is 100x100.
- `Example/Defect/Icon.png` is 402x402.
- `Example/Defect` animation frames are 384x384.
- A published card-pack example used 512x512 card art, portrait card-pack cover art, 128x128 full-frame relic icons, and a square workshop/mod icon larger than 512px.
- A developer-provided Buff border atlas in `assets/buff-border-atlas.png` contains six 31x31 Buff frames inside a 768x256 image. Use 31x31 as the default final Buff icon size. Use the red frame for negative/debuff icons; until official semantics are known, non-red frames may be used for positive or neutral Buffs.
- Official card-pack samples are 300x440. Use `assets/cardpack-cover-base-300x440.png` as the preferred image-generation reference, `assets/cardpack-cover-silhouette-300x440.png` as the final alpha mask, and `assets/cardpack-cover-frame-300x440.png` as a clean outline reference or optional final overlay.
- Treat published example dimensions as practical defaults, not official guarantees.
- Official-looking card-pack covers are portrait images with a framed cover layout and inner safe area. Do not generate card-pack covers as 512x512 square images.

Broad style guardrails:

- Avoid photorealism and modern stock-art looks.
- Prefer pixel-art, pixel-adjacent, or low-color game illustration.
- Keep shapes readable at small UI sizes.
- Use strong silhouettes and restrained details.
- Do not include text inside card art, Buff icons, or relic icons unless the user explicitly wants it.
- Ask for one or more signature motifs before generating a themed pack: celestial bodies, flowers, masks, bells, mirrors, thorns, insects, letters, ritual tools, weapons, clocks, ruins, ribbons, keys, or candles.
- Maintain a shared palette and motif list within one pack so generated assets feel related.

## Constraint Levels

Not every asset type has the same confidence level. Before generating or wiring images, classify the asset:

Hard-constrained assets:

- Card-pack cover: final `300x440`; for new covers, use `assets/cardpack-cover-base-300x440.png` as an image reference and generate a complete cover, then run `scripts/finalize_cardpack_cover.py`; use `scripts/compose_cardpack_cover.py` only as a fallback; do not use square card art.
- Buff icon: final `31x31`; use the Buff border atlas; red frame for negative/debuff, non-red frames for positive/neutral until official semantics are confirmed.
- Relic icon: final `128x128`; square framed icon with centered object; do not wire raw 256x256 generated art directly.

Practical defaults:

- Card art: `512x512` square.
- Mod/workshop icon: square image, often derived from the pack cover or a dedicated icon.

Unconstrained or reference-needed:

- Blessing icons.
- Keyword icons.
- Character portraits and animation frames.
- Enemy intent icons.
- Dialogue/event illustrations.
- Any asset type without official references or tested published examples.

For hard-constrained assets, validate size and post-processing before writing CSV paths. For unconstrained assets, ask for references when possible and clearly report that in-game verification is required.

Workflow:

1. Generate an asset inventory from the mod design: card art, card pack cover, Buff icons, relic icons, preview icon, character/animation assets.
2. Ask for signature motifs and any reference images. Do not block if the user has only a theme.
3. Use practical default sizes unless the user supplies better references:
   - Card art: 512x512 square.
   - Card-pack cover: final asset 300x440 portrait. For new assets, generate a complete cover with `assets/cardpack-cover-base-300x440.png` as the structural image reference, including integrated Chinese and English title art. Ask for exact `300x440` output, or at least the same `15:22` portrait aspect ratio. Then run `scripts/finalize_cardpack_cover.py <generated-cover> <output>` so the final size, silhouette mask, transparent pixels, and green-edge cleanup are deterministic. Use `scripts/compose_cardpack_cover.py <center-art> <output>` only as a fallback when full-cover generation fails.
   - Relic icon: final asset 128x128 square with an official-style border/frame and centered object/icon. Do not wire 256x256 generated relic art directly into CSV.
   - Buff icon: 31x31 final PNG using the Buff frame reference. Do not wire 512x512 generated Buff art into CSV.
   - Keyword icon: square, readable at small sizes; confirm size when possible.
4. Save candidate images under role-specific paths, not a generic dump:
   - `ModResource/Images/Card/<PackName>/<card_id>.png`
   - `ModResource/Images/CardPack/<pack_id>.png`
   - `ModResource/Images/Relic/<PackName>/<relic_id>.png`
   - `ModResource/Images/Buff/<PackName>/<buff_id>.png`
5. Omit extensions in CSV paths when practical; the game can try `.png`, `.jpg`, and `.jpeg`.
6. Wire paths into CSV fields, but report that exact dimensions/style still require in-game verification.

Do not claim official compliance without references or in-game verification.

## Buff Icon Template

Use `assets/buff-border-atlas.png` as the Buff frame reference. The atlas is 768x256 and contains six colored 31x31 frames:

| Frame | Bounds `(x1,y1)-(x2,y2)` | Size | Current use |
| --- | --- | --- | --- |
| 1 | `(81,28)-(111,58)` | `31x31` | Negative/debuff |
| 2 | `(115,28)-(145,58)` | `31x31` | Positive/neutral |
| 3 | `(149,28)-(179,58)` | `31x31` | Positive/neutral |
| 4 | `(183,28)-(213,58)` | `31x31` | Positive/neutral |
| 5 | `(217,28)-(247,58)` | `31x31` | Positive/neutral |
| 6 | `(251,28)-(281,58)` | `31x31` | Positive/neutral |

Prompt and processing requirements for Buff icons:

- Final asset must be 31x31 PNG.
- Negative/debuff icons should use frame 1, the red frame.
- Positive or neutral Buff icons can use any non-red frame until official frame semantics are confirmed.
- Design must be readable as a tiny status icon.
- Use simple shapes, high contrast, and very few details.
- Avoid text, tiny symbols, photorealism, complex scenes, and large transparent padding.
- If AI generation produces a larger image, treat it as concept art only; crop/simplify/downscale and composite into a 31x31 frame before writing the CSV path.

## Card-Pack Cover Template

Use `assets/cardpack-cover-base-300x440.png` as the preferred structural reference for new cover generation. Use `assets/cardpack-cover-silhouette-300x440.png` as the precise outer transparency mask. Use `assets/cardpack-cover-frame-300x440.png` only as a clean outer-outline reference or optional final overlay. These files are not finished standalone card-pack art by themselves; use them for generation constraints, compositing, cropping, and manual review.

For new card-pack covers, use `assets/cardpack-cover-base-300x440.png` as an image reference and generate a complete cover first. Then run:

```bash
python scripts/finalize_cardpack_cover.py <generated-cover> <final-300x440-png>
```

This is the preferred v0 path because the image model can integrate the titles, palette, center art, and wrapper style into one coherent cover, while the script still keeps final size, silhouette, transparent cleanup, and green-edge removal deterministic. The finalize script defaults to `--resize-mode stretch` so generated titles are not cropped; use `--resize-mode crop` only when the source has safe outer padding.

If the model repeatedly fails to generate usable title placement or structure, use the deterministic fallback:

```bash
python scripts/compose_cardpack_cover.py <center-art> <final-300x440-png> --title-zh "<Chinese name>" --title-en "<English name>" --theme-color "#6db6d6"
```

The `finalize_cardpack_cover.py` default output applies the silhouette but does not overlay `cardpack-cover-frame-300x440.png`, because the outer frame can look like an unwanted extra border in game. Use `--overlay-frame` only when that explicit frame is desired.

Important: never use an annotated safe-area guide as a visible generation base. If a reference image contains labels, cyan/yellow guide rectangles, dark translucent safe-area blocks, or any instruction text, it is for human review only. Do not feed it to img2img and do not composite it into the final PNG. Those guide marks can be learned or preserved by the image model and will appear as unwanted line boxes or UI-like overlays.

Important: never use a green, chroma-key, or debug-colored mask as a visible layer. The silhouette file is only an alpha source; ignore its RGB channels. When saving the final PNG, set fully transparent pixels to `(0,0,0,0)` and check the outer edge for green halos or one-pixel green outlines. If green remains, remove it before wiring the card-pack icon path.

Prompt requirements for card-pack covers:

- Portrait image, not square.
- Final output: 300x440 PNG.
- Preferred generated aspect ratio: exact `300x440`, or `15:22` if the image model only accepts aspect ratios.
- Preferred model input for new covers: the 300x440 base template as a reference image, plus prompt instructions to replace the placeholder mark and integrate the English and Chinese titles into the art.
- Optional working draft: larger portrait complete cover, then crop/finalize back to 300x440.
- The final PNG should contain finished cover art with integrated title treatment. It must not contain safety guide lines, labels, debug rectangles, prompt text outside the intended titles, green mask outlines, chroma-key edges, or large semi-transparent layout panels.
- Pixel-art or pixel-adjacent game cover.
- Full framed cover with a visible border, inner inset, and enough padding for UI cropping.
- Keep title pixels inside the inner safe area with padding from the transparent silhouette; titles touching the raw image border will be clipped by the final mask.
- Avoid photorealism, screenshots, plain square icons, and full card UI mockups.
- Include the pack's signature motifs and a small coherent palette.

Recommended processing order:

1. Generate a complete cover from theme, motifs, Chinese title, English title, and the base template reference.
2. Run `scripts/finalize_cardpack_cover.py` on the generated complete cover.
3. Confirm the result is exactly 300x440 and has no visible green/chroma-key fringe.
4. Do not overlay `cardpack-cover-frame-300x440.png` by default. Use `--overlay-frame` only for an intentional extra outline.
5. Review the final PNG for accidental guide lines, wrong title text, square UI panels, green outer outlines, placeholder question marks, or large dark translucent boxes before wiring it into `Text/CardPack` or `Data/CardPack`.

If an image generator returns a square cover, reject or regenerate before wiring it. Do not use 512x512 card art as a card-pack cover.

## Relic Icon Caveat

Use `128x128` as the v0 final relic icon size. This is based on the verified published card-pack example and should be treated as a practical default until official relic-icon source assets are provided.

Prompt and processing requirements for relic icons:

- Final asset must be a 128x128 PNG.
- Use a square framed icon, not a full relic card and not a bare unframed object.
- Keep the central object readable at small UI sizes.
- Use pixel-art or pixel-adjacent rendering with a restrained palette.
- Generate larger concept art only as an intermediate, then downscale/composite into a 128x128 framed icon before writing the CSV path.
- If an official relic border/frame template is later provided, use it as the composition base and update this section.

The same relic `Icon` may be used in both shop display and card-pack preview/detail. A published card-pack example confirmed that shop UI may call `SetNativeSize()` while pack detail uses a fixed relic-card frame.

Data-only workaround: transparent padding can make shop display smaller, but may make pack preview too small.

Robust but advanced workaround: a narrow UI-only DLL hook can clamp only the affected shop icon size, while leaving gameplay, save data, pack selection, reward pools, and inventory untouched. Do not use this by default.

## Game Directory Location

Try these sources:

1. User-provided path.
2. Common Steam install path:
   `C:\Program Files (x86)\Steam\steamapps\common\Witch's Apocalyptic Journey`
3. Steam library folders from `steamapps/libraryfolders.vdf` when accessible.
4. Ask the user for the Steam library or game install folder.

Validate with likely markers:

- `Witch's Apocalyptic Journey.exe`
- `Witch's Apocalyptic Journey_Data`
- `Witch's Apocalyptic Journey_Data\StreamingAssets\Mod Upload Tool\WorkshopUploader.exe`

Reading outside the workspace may require approval.

## Publishing Assistant

Before publishing:

- Confirm `ModConfig.json` exists.
- Confirm `ModName`, `ModVersion`, `ModAuthor`, `ModDescription`, `IconPath`, and `Enabled`.
- Set or confirm `WorkshopVisibility`.
- For first upload, keep `PublishedFileId` empty.
- For updates, preserve `PublishedFileId`.
- Generate concise title, description, and update notes.
- Warn if generated assets are placeholders.
- Check that upload content selects the actual mod folder, not an outer staging folder.
- Keep temporary generated source images, atlases, C# source, and unneeded DLLs out of release packages.

Uploader:

```text
<GameDir>\Witch's Apocalyptic Journey_Data\StreamingAssets\Mod Upload Tool\WorkshopUploader.exe
```

Automation may launch the uploader when permissions allow, but GUI completion can depend on Steam login state and workshop agreement state. If automatic GUI control is unreliable, give the user a short handoff checklist.

Success evidence:

- Uploader reports success, or
- `PublishedFileId` is written back to `ModConfig.json`.
