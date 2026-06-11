---
name: waj-modder
description: Create and modify Witch's Apocalyptic Journey Lua-template mods from natural-language ideas. Use when Codex needs to build content mods, cards, buffs, keyword mechanics, CSV Data/Text files, Lua ScriptExecutor logic, mod assets, local game-directory setup, or workshop publishing support for Witch's Apocalyptic Journey.
---

# WAJ Modder

## Purpose

Help users turn Witch's Apocalyptic Journey mod ideas into Lua-template based, testable mod projects. Prioritize stable Data/Text CSV generation, Lua `ScriptExecutor` patterns, clear ID management, local setup help, asset generation support, and publishing assistance.

Treat outputs as testable mod drafts, not guaranteed final builds. Prefer readable, conservative scripts and explicit user-facing test steps.

## First Response Workflow

1. Identify the user's intent: new mod, card, buff, keyword mechanic, card pack, relic, blessing, enemy/event/dialogue, asset generation, install-path setup, validation, or workshop publishing.
2. Inspect local context before generating files. Prefer the user's current mod folder if one exists. Otherwise find `mod-tutorial/ModTemplate`; if it is missing, use `scripts/ensure_tutorial.py` to fetch the official tutorial repo from GitHub after any required network approval.
3. Load only the references needed for the task:
   - `references/boundaries.md` for v0 scope and exclusions.
   - `references/mod-structure.md` for directories, IDs, and setup.
   - `references/csv-schemas.md` for Data/Text table targets.
   - `references/lua-patterns.md` for common `ScriptExecutor` code.
   - `references/mechanic-patterns.md` for keyword/tag systems.
   - `references/assets-and-publishing.md` for generated art, game directory lookup, and workshop publishing.
   - `references/asset-style-guide.md` for card art, Buff icon, relic icon, and card-pack cover visual style.
   - `references/cardpack-cover-layout.md` for layered card-pack cover composition and title placement.
   - `references/cardpack-cover-prompt-examples.md` for known-good card-pack cover prompt patterns such as Ashen Ledger.
4. Use bundled scripts when they fit:
   - `scripts/ensure_tutorial.py` to find or clone the official `meowalive/apocalyptic-journey-mod-tutorial` repo.
   - `scripts/create_mod.py` to copy `ModTemplate` and update `ModConfig.json`.
   - `scripts/validate_mod.py` to check config, CSV structure, Data/Text IDs, card `BaseScript`, `PackBelong`, image paths, and script hazards.
   - `scripts/finalize_cardpack_cover.py` after generated full card-pack covers to fit to 300x440, apply the silhouette mask, and strip guide/debug edge colors.
   - `scripts/compose_cardpack_cover.py` only as a fallback when the model cannot generate a complete cover with usable title placement.
   - `scripts/locate_game.py` to find the local game install and workshop uploader.
5. Ask a concise question only when a missing choice would make file generation risky. Otherwise make a conservative assumption and continue.
6. When editing files, preserve CSV headers exactly, keep comments/second rows, and append or update only the relevant rows.
7. After generating or changing a mod, run static checks where practical and report what still requires in-game testing.

## Core Build Rules

- Use Lua-template mods by default. Do not choose C# DLL hooks unless the user explicitly asks for advanced experimental work.
- Generate content through `ModConfig.json`, `Data/**/*.csv`, `Text/**/*.csv`, `Scripts/Entry.lua`, and `ModResource/**`.
- For ordinary card packs, prefer a pure data/text/image release. Treat DLL hooks as narrow exceptions, such as UI-only presentation fixes, and document their scope.
- For cards, always set `BaseScript` in `InitScript`:
  - `AttackCardItem` when the card selects a target.
  - `CommonCardItem` when the card affects self, all enemies, the deck, or global state.
- Keep Data/Text IDs aligned. Remember runtime references use the CSV filename/stem and raw row ID. Original-game references are `<CsvFileName>_<RawId>`; mod references are `<ModFolder>_<CsvFileName>_<RawId>`. Never write a bare `{id}` rich-text reference when `{buff_id}`, `{keyword_id}`, or `{ModFolder_buff_id}` is required.
- For card-pack mods, set `PackBelong` to the runtime card pack ID on cards and relics. Missing relic `PackBelong` can place relics in an official/basic pack.
- For card numeric effects, do not hard-code final numbers only in `Text/Card` descriptions. Use `{0}`, `{1}` placeholders in text and register their values in `InitScript` with `AddDescription`; keep those values aligned with `UseScript`.
- Use literal original game IDs only after checking `mod-tutorial/ModTemplate/Scripts/Lib/DataConfigs`.
- Prefer explicit per-card `UseScript` calls for custom keyword mechanics in v0. Treat global hooks/listeners as experimental unless proven by local examples.
- Put persistent or repeated effects into Buffs rather than hiding long-lived state in one card script.
- For CSV Lua fields, quote and escape strings carefully. Avoid multi-line scripts unless the surrounding table already uses them safely.

## Deliverables

For a mod-generation task, produce or update:

- A mod directory with `ModConfig.json`.
- The necessary `Data` and `Text` CSV rows.
- `Scripts/Entry.lua` only when setup, helper functions, resource redirects, or hooks are needed.
- `ModResource` paths for referenced assets, using generated or placeholder assets as appropriate.
- A short test checklist covering load, acquisition, card play, Buff behavior, and publishing readiness.

## Asset Policy

Asset generation is part of v0. Use broad style guardrails rather than overfitting to one example: avoid photorealism, prefer readable pixel-art or pixel-adjacent game icons/covers, use clear silhouettes, and ask the developer for signature motifs such as celestial shapes, thorns, mirrors, letters, masks, bells, insects, ritual tools, weapons, flowers, clocks, or ruins. For visual style, load `references/asset-style-guide.md` before prompting image generation.

Card-pack covers are a special case: never generate them as square icons. Prefer template-guided full-cover generation: use `assets/cardpack-cover-base-300x440.png` as a visual/reference image for the image model, ask it to generate the complete cover including integrated title treatment, then run `scripts/finalize_cardpack_cover.py <generated-cover> <output>` to enforce `300x440`, apply the silhouette mask, and strip green/debug edges. Do not use script-rendered titles by default because they tend to look detached from the cover art. Use `scripts/compose_cardpack_cover.py` only as a fallback when the model cannot produce a complete cover. Do not send annotated safe-area guides, guide text, colored rectangles, green/chroma-key masks, or semi-transparent layout blocks to the image model as visible art.

Relic icons are also a fixed-format asset in v0. Use a `128x128` final PNG with an official-style square border/frame and centered object silhouette. Do not wire 256x256 generated relic art directly into CSV; treat larger AI output as intermediate concept art and downscale/composite to 128x128 before use.

Buff icons are also a special case: do not use 512x512 generated art directly. Use a 31x31 final canvas based on the provided `assets/buff-border-atlas.png` frame reference. Generate high-resolution concept art only as an intermediate, then simplify/downscale into the 31x31 frame. Use the red Buff frame for negative/debuff icons. Until official color semantics are confirmed, any non-red frame can be used for positive or neutral Buffs.

Do not claim official card art, relic icon, blessing icon, or card pack size rules unless the user provides reference images or updated documentation. Published mod examples provide practical defaults, not official guarantees.

## Publishing Policy

Support end-to-end publishing assistance:

- Locate or ask for the game install directory.
- Verify the upload tool exists.
- Validate `ModConfig.json` publishing fields.
- Prepare preview icon, visibility, title/description, and update notes.
- Launch or guide use of the Workshop uploader when permissions allow.

Do not claim a workshop upload succeeded unless the tool or files confirm success, such as `PublishedFileId` being written back.

## Script Usage

Create a mod draft:

```bash
python scripts/create_mod.py --out <mods-root> --name <ModName> --author <Author> --description "<description>"
```

Fetch or locate the official tutorial:

```bash
python scripts/ensure_tutorial.py --root <workspace-root>
```

Validate a mod:

```bash
python scripts/validate_mod.py <path-to-mod>
```

Locate the game:

```bash
python scripts/locate_game.py
```
