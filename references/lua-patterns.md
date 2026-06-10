# Lua ScriptExecutor Patterns

Use Lua syntax in mod files even when original game references under `Scripts/Lib/DataConfigs` use C#-style scripts.

## Card BaseScript

Targeted attack card:

```lua
self.Vars:set_Item("BaseScript", "AttackCardItem");
```

Self/global skill card:

```lua
self.Vars:set_Item("BaseScript", "CommonCardItem");
```

## Common Effects

Damage target:

```lua
self:SetStatus("Target");
self:Damage("7");
```

Damage all enemies:

```lua
self:SetStatus("AllTarget");
self:Damage("5");
```

Gain shield:

```lua
self:SetStatus("Self");
self:ChangeDefence("8");
```

Heal:

```lua
self:SetStatus("Self");
self:ChangeHp("3");
```

Gain power/energy:

```lua
self:SetStatus("Self");
self:ChangePower("1");
```

Draw cards:

```lua
self:DrawCount("2");
```

Apply Buff:

```lua
self:SetStatus("Target");
self:AddBuff("buff_vulnerability", "1");
```

Get own Buff level:

```lua
local buff = self.Self:GetBuff("buff_id_here");
local level = 0;
if buff ~= nil then
  level = buff.buffConfig.Level;
end
```

Repeat by count:

```lua
for i = 1, count do
  self:SetStatus("Target");
  self:Damage("4");
end
```

## Events in Buff ApplyScript

End of round:

```lua
self:AddEvent("EndRound", function()
  self:SetStatus("Self");
  self:ChangeDefence("3");
end);
```

Start of round:

```lua
self:AddEvent("StartRound", function()
  self:SetStatus("Self");
  self:ChangePower("1");
end);
```

On damage:

```lua
self:AddEvent("Damage", function(_data)
  self:SetStatus("Self");
  self:ChangeHp("1");
end);
```

## Random Rarity Card

When adding a random card by rarity, prefer a known helper after checking examples:

```lua
local cards = self:GetcardsByRarity("2", "3");
if cards ~= nil and cards.Count > 0 then
  local index = math.random(0, cards.Count - 1);
  local card = cards:get_Item(index);
  if card ~= nil then
    local id = card:get_Item("Id");
    self:RandomAddCard(id);
  end
end
```

Verify collection access in-game; xLua dictionary/list bindings may require `get_Item`.

## Dynamic Card Descriptions

Original card data uses a dynamic description channel instead of writing final effect numbers directly into text. `ScriptExecutor` exposes `AddDescription(index, type, value)` and `GetDesValue(index)`; official Text/Card rows consume these values with placeholders such as `{0}` and `{1}`.

Observed mapping:

- `AddDescription("1", ..., value)` feeds `{0}`.
- `AddDescription("2", ..., value)` feeds `{1}`.
- Continue the same one-based-to-zero-based pattern for later values.

Basic Lua-template pattern:

```lua
-- InitScript
self.Vars:set_Item("BaseScript", "AttackCardItem");
self:AddDescription("1", "Damage", "7");
self:AddDescription("2", "Buff", "2");
```

```csv
Description
造成{0}点伤害，并施加{1}层{buff_vulnerability}。
```

Keep `UseScript` numerically aligned with `InitScript`:

```lua
-- UseScript
self:SetStatus("Target");
self:Damage("7");
self:AddBuff("buff_vulnerability", "2");
```

Use the closest description type so the game can format or recalculate display values like original cards:

- `Damage`: ordinary damage affected by damage modifiers.
- `TrueDamage`: true damage.
- `Defence`: shield/block values.
- `Hp`: healing or HP change values.
- `Buff`: buff stack counts.
- `Power`: mana/energy values.
- `Draw`: draw counts.
- `Money`: gold values.
- `Percent`: percent values.
- `Value` or `Special`: untyped custom values when no better type exists.

When a value depends on Buff stacks, counters, or other runtime state, compute the display value in `InitScript` using the same formula as `UseScript`, then pass that result to `AddDescription`. If another displayed value depends on an already registered one, use `self:GetDesValue("1")` after `AddDescription("1", ...)`, mirroring original card examples.

Rules for generated cards:

- Text/Card descriptions should contain placeholders for all effect numbers that might be modified, recalculated, or reused.
- `InitScript` is the display calculation layer; `UseScript` is still the actual execution layer.
- If a card has a custom keyword sub-effect, register separate placeholders for base and keyword-triggered values rather than embedding literal numbers in prose.
- Keep formulas short in CSV. Move repeated formula helpers to `Scripts/Entry.lua` only when multiple cards share them.

## Defensive Style

- Guard nils before reading Buffs, managers, lists, or dictionaries.
- Convert numbers with `tostring(...)` when passing to ScriptExecutor methods.
- Use `dict:get_Item` and `dict:set_Item` for C# dictionaries, not `dict[key]`.
- Keep scripts short in CSV fields. Move repeated helpers to `Entry.lua` only when useful.
