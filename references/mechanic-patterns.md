# Mechanic Patterns

## Simple Keyword Trigger

Use when a card always performs a shared extra behavior.

Example: "Association": after playing an Association card, add a random rarity 2-3 card to the draw pile or hand.

Implementation:

1. Add the shared Lua snippet at the end of each relevant card's `UseScript`.
2. Reference mod-created Buff or keyword names with composed runtime IDs in Text/Card, for example `{MyMod_mycsv_ink}`.
3. Optionally add a keyword row in `Text/KeyWordsDic` for glossary/tooltips.
4. Use the composed runtime keyword ID in card `Tag`, for example `MyMod_mycsv_Association`. Raw row IDs are for built-in/original content and can display incorrectly for mod content.
5. Optionally put the snippet in an `Entry.lua` helper if many cards use it.

Prefer explicit per-card scripts plus localized visible text for v0.

## Buff-Gated Keyword Trigger

Use when a keyword behaves differently depending on whether the player has a Buff.

Example shape:

1. Card has tag `Invocation`.
2. If player has `buff_revelation`, execute bonus effect.
3. Add or change `buff_revelation`.

Pattern:

```lua
local buff = self.Self:GetBuff("buff_revelation");
if buff ~= nil then
  -- bonus effect
end
self:SetStatus("Self");
self:AddBuff("buff_revelation", "1");
```

Use a mod-created Buff for new mechanics rather than overloading original Buffs unless the user explicitly wants compatibility.

## Persistent Engine

Use a Buff when a mechanic watches events over time:

- "At start of round..."
- "Whenever damaged..."
- "Whenever a card is created..."
- "For the rest of combat..."

Put the listener in `ApplyScript`, make stack behavior explicit, and set `UpperBound`.

## Themed Card Pack

For a 5-10 card mechanic package:

1. Define the keyword.
2. Define any required Buffs.
3. Create 3-4 common/simple cards.
4. Create 2-3 uncommon synergy cards.
5. Create 1-2 rare payoff cards.
6. Add card pack text if needed.
7. Ensure every card has matching Data/Text rows and clear descriptions.

## Balance Heuristics

- Avoid zero-cost cards that generate energy, draw, or random cards without limits.
- Cap stacking Buffs unless endless scaling is the core fantasy.
- Make random generation costs visible in card cost, exhaust behavior, or rarity.
- Use `*id` for special cards not intended for random pools.
- For mechanics that add random cards, consider excluding curses or locked cards after checking available helpers.
