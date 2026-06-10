# V0 Boundaries

## Stable v0

- Create Lua-template mod projects from `ModTemplate`.
- Generate and update Data/Text CSV rows for cards, Buffs, keywords, relics, blessings, items, card packs, simple enemy cards, enemies, events, and dialogue.
- Generate common Lua `ScriptExecutor` logic for battle effects.
- Design small keyword/tag mechanics that can be expressed through card `Tag`, `UseScript`, Buffs, and keyword text.
- Generate candidate assets and wire their paths into CSV files, while clearly marking unknown size/style assumptions.
- Locate the game directory when possible, or ask the user for it.
- Prepare and assist workshop publishing through the bundled uploader.
- Run static checks and provide in-game test checklists.

## Experimental v0

- Global Hook or listener implementations for keyword mechanics.
- GUI automation of the workshop uploader.
- Automatic asset cropping/resizing when official dimensions are not known.
- New career implementations beyond a simple skeleton.
- Complex event chains or enemy behavior beyond examples in the tutorial.

## Out of Scope by Default

- C# DLL Hook development.
- Deep engine patches or core battle-flow rewrites.
- Custom UI systems.
- Save format changes.
- Steam workshop backend changes.
- Multiplayer/network behavior.
- Guaranteed official-art style matching.
- Guaranteed in-game correctness without testing.

## Wording

Call generated mods "testable drafts" or "first playable versions". Do not call them final unless the user has tested them in game.

