# CSV Schemas

Preserve first-row headers exactly. Preserve the second comment row when present. Append new rows rather than rewriting whole files unless the user requests cleanup. Locate columns by header name, not by fixed position; published mods may reorder columns or add fields such as `PackBelong`.

## High-Priority Tables

### Card

Data: `Data/Card/*.csv`

```csv
Id,Rarity,Expend,Tag,PackBelong,InitScript,DrawScript,UseScript,DropScript,Icon,Effects,Action
```

Text: `Text/Card/*.csv`

```csv
Id,是否完成,Type,Note,Name,Name_en,Name_zh-Hant,Name_ja,Description,Description_zh-Hant,Description_en,Description_ja
```

Rules:

- Put `AttackCardItem` or `CommonCardItem` in `InitScript`.
- Put main play behavior in `UseScript`.
- For player-facing effect numbers, write placeholders in Text descriptions, such as `{0}` and `{1}`, and register the values in `InitScript` with `AddDescription`. Avoid fixed numeric prose like `造成5点伤害` for generated cards unless the number is intentionally not dynamic UI data.
- Use `Tag` for proven built-in keywords or card pools. For mod-created keyword rows, use the composed runtime ID, for example `MyMod_mycsv_Contract`, not the raw row ID `Contract`; otherwise cards may display raw English like `Contract;DebtMark`.
- Separate multiple tags with the same delimiter used by original data, usually comma plus space, for example `Combo, Burnout`. Avoid semicolon-separated tags unless a local example proves it.
- In Text/Card descriptions, `{0}`, `{1}`, etc. are numeric description placeholders. For Buff or keyword name references inside `{...}`, use the composed runtime ID for mod-created rows, such as `{MyMod_mycsv_ink}`. Do not write custom mechanic names as `{Ink}` or `{DebtMark}` unless you have verified that exact token resolves in game. If a token still does not resolve in-game, fall back to the localized visible name directly in card descriptions and keep the Buff tooltip in Text/Buff.
- Fill `PackBelong` with the runtime card pack ID when making a themed card pack.

### Buff

Data: `Data/Buff/*.csv`

```csv
Id,InitScript,ApplyScript,ClearScript,ReducePerTurn,ReducePerAttacked,ReducePerUse,UpperBound,Icon,Type,Rarity,Effects,SoundEffects,Action,CanZero
```

Text: `Text/Buff/*.csv`

```csv
Id,Note,Name,Name_zh-Hant,Name_en,Name_ja,Description,Description_zh-Hant,Description_ja,Description_en
```

Rules:

- Put event registration in `ApplyScript`.
- Use `UpperBound` for stacking Buffs.
- Use reduction fields for simple duration decay before writing custom decay logic.
- Buff `Icon` resources should resolve to a 31x31 final PNG when using custom ModResource art. Do not use 512x512 generated art directly.
- Negative/debuff Buff icons should use the red 31x31 frame from `assets/buff-border-atlas.png`. Until official color rules are confirmed, non-red frames are acceptable for positive or neutral Buffs.

### Keyword

Text: `Text/KeyWordsDic/*.csv`

```csv
Id,Note,Description,Keywords,Keywords_zh-Hant,Keywords_en,Description_zh-Hant,Description_en,Keywords_ja,Description_ja,ShouldShow
```

Rules:

- Use an internal ASCII ID, for example `Association`.
- Use localized visible names in `Keywords*`.
- Set `ShouldShow` to `TRUE` for player-facing mechanics.

## Other Common Tables

- Relic: `Data/Relic`, `Text/Relic`. Add/fill `PackBelong` for pack-owned relics. Custom relic `Icon` resources should resolve to a 128x128 final PNG with a square framed icon style; do not use raw 256x256 generated art directly.
- Blessing: `Data/Blessing`, `Text/Blessing`.
- Item: `Data/Item`, `Text/Item`.
- Card pack: `Data/CardPack`, `Text/CardPack`; use the runtime card pack ID in card and relic `PackBelong`. Card-pack `Icon` resources must be portrait cover art, not square card/icon art.
- Enemy card: `Data/EnemyCard`, `Text/EnemyCard`.
- Enemy: `Data/Enemy`, `Text/Enemy`.
- Event and dialogue: `Data/EventList`, `Text/EventList`, `Data/Dialogue`, `Text/Dialogue`.

Load the corresponding sample file from `mod-tutorial/ModTemplate` before editing a table not listed in detail here.
