# Mod Structure

## Source of Truth

Use the official tutorial repo for templates and original game references:

```text
https://github.com/meowalive/apocalyptic-journey-mod-tutorial.git
```

Find a local checkout first. Accepted local folder names include `mod-tutorial` and `apocalyptic-journey-mod-tutorial`. If missing, run `scripts/ensure_tutorial.py --root <workspace-root>` and request network approval if needed.

Use `ModTemplate` for a Lua mod and `Example/Defect` for a worked example. Use `ModTemplate/Scripts/Lib/DataConfigs` for original game CSV references.

## Standard Directory

For a card-pack style mod, prefer:

```text
<ModName>/
  ModConfig.json
  Icon.png
  README.md
  Data/
    Card/
    Buff/
    CardPack/
    Relic/
  Text/
    Card/
    Buff/
    CardPack/
    Relic/
    KeyWordsDic/
  ModResource/
    Images/
      Card/
        <PackName>/
      CardPack/
      Relic/
        <PackName>/
      Buff/
        <PackName>/
  Scripts/
    Entry.lua
  Docs/
```

For a pure data card pack, omit `Scripts/` if no setup, helper, redirect, or hook is needed. For a minimal single-card test mod, include only the relevant Data/Text folders.

Local testing usually uses:

```text
<GameDir>\Witch's Apocalyptic Journey_Data\Mods\<ModName>
```

Workshop upload should select the actual `<ModName>` folder, not an outer staging folder.

## ModConfig

Required fields:

- `ModName`: should match the folder name. The folder name participates in runtime IDs; renaming after authoring requires updating all runtime references.
- `ModVersion`: default `0.1.0` for new drafts.
- `ModAuthor`: ask if unknown; otherwise use a neutral placeholder only with user consent.
- `ModDescription`: summarize the mod idea.
- `IconPath`: usually `Icon.png`.
- `Enabled`: use `true` for local testing.
- `Dependencies`: usually `null`.

Publishing fields:

- `WorkshopVisibility`: `Private`, `FriendsOnly`, `Unlisted`, or `Public`.
- `PublishedFileId`: empty for first upload, preserved for updates.

## ID Rules

- Data/Text row IDs should be short ASCII identifiers, for example `memory_echo`.
- Use a leading `*` for content that should not enter random pools.
- Runtime IDs are composed from CSV filename without extension and raw row ID. Mod content also receives the mod folder name as a prefix.

Original game content:

```text
<CsvFileName>_<RawId>
```

Mod content:

```text
<ModFolder>_<CsvFileName>_<RawId>
```

Examples:

- Original `Data/Buff/buff.csv` row `revelation` is referenced as `buff_revelation`.
- `Mods/ExamplePack/Data/Card/examplepack.csv` row `memory_echo` becomes `ExamplePack_examplepack_memory_echo`.
- `Mods/ExamplePack/Data/Buff/buff.csv` row `memory_mark` becomes `ExamplePack_buff_memory_mark`.

- `PackBelong` is compared directly and must use the runtime card pack ID. Example: `ExamplePack_cardpack_cardpack_example` if the row lives in `Data/CardPack/cardpack.csv`.
- Add `PackBelong` to `Data/Relic/*.csv` for pack-owned relics; otherwise they may default to an official/basic pack.
- Original game IDs may be referenced directly only after checking `Scripts/Lib/DataConfigs`.
- Rich text references in descriptions must use runtime IDs inside braces:
  - Original Buff: `{buff_revelation}`
  - Original keyword/tag: `{KeyWordsDic_Association}` only after confirming the original CSV filename and row ID.
  - Mod Buff: `{ExamplePack_buff_memory_mark}`
  - Mod keyword/tag: `{ExamplePack_<CsvFileName>_<RawId>}`
- Do not write bare `{memory_mark}` or `{Association}` in card descriptions; those usually fail lookup because the CSV filename and, for mod content, mod folder prefix are missing.

## Entry.lua

Use `function ModConfig:Setup() ... end` for setup work:

- Resource redirects.
- Mod helper functions.
- Method hooks only when explicitly needed.
- Logging for debug-only setup.

Avoid stuffing normal card effects into `Entry.lua`; put card effects in card script columns unless shared helpers materially reduce duplication.

## Release Hygiene

- Keep source drafts, temp image atlases, sync metadata, and unneeded DLLs out of the release folder.
- Include `README.md`, workshop description files, or `Docs/` only when useful for players/developers.
- If a DLL hook is shipped, document what it changes and what it must not touch.
