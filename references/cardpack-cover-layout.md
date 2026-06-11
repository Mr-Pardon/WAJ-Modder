# Card-Pack Cover Layout

Use this reference when generating card-pack covers. The preferred v0 route is template-guided full-cover generation, not script-composited title text.

For a known-good prompt and result, see `cardpack-cover-prompt-examples.md` and `docs/images/ashen-ledger-cardpack-success.png`.

## Goal

Create a `300x440` official-style card-pack cover where:

- The image model sees `assets/cardpack-cover-base-300x440.png` as the structural reference.
- The model generates a complete, visually unified cover: wrapper bands, central illustration, English title, and Chinese title.
- The titles are part of the generated art direction, not pasted afterward by script.
- The script only finalizes the image: crop/downscale, silhouette alpha, transparent cleanup, and green/debug edge removal.

## Base Template Role

Use `assets/cardpack-cover-base-300x440.png` as a reference/control image when the image tool supports image input. Ask for exact `300x440` output when possible; if the image tool cannot set exact pixels, ask for the same `15:22` portrait aspect ratio.

Preserve the template's layout logic:

- Top brush strip and upper title region.
- Dark side body and cover silhouette.
- Large central illustration area.
- Bottom/lower-left Chinese title region.
- Jagged wrapper texture at top and bottom.

The generated cover should not keep the placeholder question mark. It should replace the blank center with the pack's main motif.

Keep titles inside the safe areas:

- English title: upper-right/upper-center, below the top jagged edge, not touching the transparent silhouette.
- Chinese title: lower-left/lower area, above the bottom jagged edge, not touching the transparent silhouette.
- Leave visible padding between title pixels and the outer cover edge. If the title touches the raw image border, it will be clipped when `finalize_cardpack_cover.py` applies the silhouette mask.

## Preferred Workflow

1. Ask for:
   - Chinese pack name.
   - English pack name.
   - Theme color or palette.
   - Two to four signature motifs.
2. Use the base template as a reference image, then prompt for a complete cover:

```text
Use the provided 300x440 card-pack base as the structural guide.
Generate a complete 300x440 pixel-art card-pack cover in the same layout:
top brush wrapper, dark side body, central illustration, upper English title,
large lower-left Chinese title. Replace the placeholder mark completely.
Integrated title art, blocky pixel lettering, dark outlined light text.
Keep all title pixels inside the cover safe area with padding from transparent edges.
Theme: <theme>. Palette: <palette>. Motifs: <motifs>.
Chinese title: <Chinese name>. English title: <English name>.
No guide lines, no debug rectangles, no visible template placeholder,
no photorealism, no square icon.
```

3. Finalize the generated full cover:

```bash
python scripts/finalize_cardpack_cover.py <generated-cover> <final-300x440-png>
```

`finalize_cardpack_cover.py` defaults to `--resize-mode stretch` to preserve generated titles and avoid cropping. If the source is intentionally larger with safe padding, `--resize-mode crop` is available.

4. Review the final output:
   - `300x440`
   - cover silhouette and transparent corners are correct
   - center area fully covers the template's blank area
   - no placeholder question mark remains
   - Chinese title and English title feel integrated with the cover
   - no green/debug edges
   - no copied third-party imagery

## When To Use compose_cardpack_cover.py

Use `compose_cardpack_cover.py` only as a fallback when the model cannot generate a complete cover with acceptable title placement.

Tradeoff:

- It is deterministic and keeps dimensions safe.
- It can look less natural because text is script-rendered over art.

For publication-quality covers, prefer template-guided image generation plus `finalize_cardpack_cover.py`.

## Distribution Note

If publishing this skill publicly, verify whether the base template asset may be redistributed. If redistribution is not permitted, keep the template local and document how the developer should provide `assets/cardpack-cover-base-300x440.png`.
