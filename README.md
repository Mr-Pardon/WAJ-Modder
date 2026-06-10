# WAJ Modder

English | [中文](#中文)

WAJ Modder is an unofficial Codex skill for creating and validating Witch's Apocalyptic Journey Lua-template mods from natural-language ideas.

It is intended for mod authors who have design ideas but may not know Lua, C#, or the game's CSV conventions yet.

## Contents

- [Status](#status)
- [Model Note](#model-note)
- [What v0 Handles Well](#what-v0-handles-well)
- [Asset Constraints](#asset-constraints)
- [Current Boundaries](#current-boundaries)
- [Official Tutorial](#official-tutorial)
- [Demo](#demo)
- [License](#license)
- [中文](#中文)

## Status

This is a v0 skill. Treat generated mods as testable drafts, not guaranteed final releases.

## Model Note

The Ashen Ledger demo shown in this repository was produced with GPT-5.5. Model capability matters: different language models, image models, prompts, and context can produce different implementation quality, asset style, and reliability. The v0 boundaries below should be read as the demonstrated result for this model-assisted workflow, not as a guarantee that every model will match it.

## What v0 Handles Well

- Lua-template card-pack mods
- Card, Buff, relic, blessing, keyword, and card-pack CSV rows
- Matching `Data` / `Text` entries
- Runtime ID references
- `PackBelong` ownership for cards and relics
- Dynamic card descriptions through placeholders and `AddDescription`
- Generated image asset guidance and post-processing
- Card-pack covers, Buff icons, and relic icon size checks
- Local static validation before in-game testing
- Basic publishing preparation

## Asset Constraints

v0 includes asset generation support, but only some asset categories have concrete size and post-processing constraints. Use the constrained categories below when predictable results matter.

Constrained in v0:

- Card-pack cover: final PNG should be `300x440`. Generated portrait art must be post-processed with `scripts/finalize_cardpack_cover.py`, which applies the official-style silhouette alpha mask and removes guide/debug edge colors. Do not use square card art as a pack cover.
- Buff icon: final PNG must be `31x31`. Use `assets/buff-border-atlas.png` as the frame reference. Negative/debuff Buffs use the red frame; positive or neutral Buffs can use non-red frames until official semantics are known.
- Relic icon: final PNG should be `128x128`, square, framed, and object-centered. Larger generated art is only an intermediate concept image.
- Card art: practical default is `512x512` square art. This is a stable workflow default for card images, but not yet an official size claim.
- Mod/workshop icon: square image; use the generated pack cover or a dedicated icon as source, then resize/crop as needed.

Not yet tightly constrained:

- Blessing icons
- Keyword icons
- Character portraits and animation frames
- Enemy intent icons
- Dialogue/event illustrations
- Any asset type without a verified official reference or tested published example

For unconstrained categories, the skill should ask for references when possible and report that in-game verification is still required.

## Current Boundaries

The skill can provide guidance for these topics, but they are not yet tightly constrained in v0:

- Complex C# DLL hooks
- Broad runtime patches or global listeners
- Advanced UI changes
- Character animation pipelines
- Automatic live game-log streaming back into Codex
- Asset types where no official size or frame references have been verified

## Official Tutorial

The official tutorial is not bundled in this skill. When needed, the skill checks for a local `mod-tutorial` or `apocalyptic-journey-mod-tutorial` directory and can fetch:

```text
https://github.com/meowalive/apocalyptic-journey-mod-tutorial.git
```

## Demo

Ashen Ledger is a Workshop demonstration mod created to show the v0 skill boundary and output style.

Workshop link: TODO_WORKSHOP_URL

The screenshot below captures one full AI-assisted generation pass: content summary, generated assets, card-pack cover, asset sheets, and static validation output.

![Ashen Ledger AI generation result](docs/images/ashen-ledger-ai-generation-result.png)

## License

MIT License, copyright (c) 2026 Mr_Pardon.

See `LICENSE` and `NOTICE.md`.

---

## 中文

WAJ Modder 是一个非官方 Codex skill，用于根据自然语言想法创建和校验《魔女：终末旅途》的 Lua 模板模组。

它面向有模组创意、但不熟悉 Lua、C# 或游戏 CSV 结构的创作者。

## 目录

- [状态](#状态)
- [模型说明](#模型说明)
- [v0 较稳定的能力](#v0-较稳定的能力)
- [素材规范约束](#素材规范约束)
- [当前边界](#当前边界)
- [官方教程](#官方教程)
- [展示模组](#展示模组)
- [许可](#许可)

## 状态

这是 v0 版本 skill。生成结果应被视为可测试草稿，而不是无需验证的最终发布版本。

## 模型说明

本仓库展示的 Ashen Ledger 示例使用 GPT-5.5 生成与协助完成。模型能力会直接影响结果：不同语言模型、图像模型、提示词和上下文，可能带来不同的实现质量、素材风格和稳定性。因此，下方 v0 能力边界应理解为该模型辅助流程下的展示结果，而不是所有模型都能完全复现的保证。

## v0 较稳定的能力

- Lua 模板卡包模组
- 卡牌、Buff、遗物、祝福、关键词和卡包 CSV
- `Data` / `Text` 配对
- 运行时 ID 引用
- 通过 `PackBelong` 处理卡牌和遗物的卡包归属
- 通过占位符和 `AddDescription` 处理动态卡牌描述
- 生成图片素材的规格约束和后处理
- 卡包封面、Buff 图标、遗物图标的尺寸检查
- 进游戏测试前的本地静态校验
- 基础发布准备

## 素材规范约束

v0 支持素材生成，但并不是所有素材类型都已经有明确尺寸和后处理规范。需要稳定结果时，优先使用下面这些已经约束过的类型。

v0 已约束：

- 卡包封面：最终 PNG 应为 `300x440`。生成的竖版图必须经过 `scripts/finalize_cardpack_cover.py` 后处理，套用官方式外形 alpha，并清理引导线、调试色和绿色边缘。不要把方形卡面直接当作卡包封面。
- Buff 图标：最终 PNG 必须是 `31x31`。使用 `assets/buff-border-atlas.png` 作为边框参考。负面/debuff 使用红色边框；正面或中性 Buff 暂时可使用非红色边框，直到确认官方语义。
- 遗物图标：最终 PNG 应为 `128x128`，方形、带边框、中心物件清晰。更大的生成图只能作为中间概念图。
- 卡面：实践默认是 `512x512` 方图。这是当前稳定工作流默认值，但还不是官方尺寸声明。
- 模组/工坊图标：使用方形图片；可以从卡包封面或单独图标生成后裁切/缩放。

暂未严格约束：

- 祝福图标
- 关键词图标
- 角色头像和动画帧
- 敌人攻击意图图标
- 对话/事件插图
- 任何没有官方参考图或已验证发布样例的素材类型

对于暂未约束的素材类型，skill 应优先询问参考图，并明确说明仍需要进游戏验证。

## 当前边界

skill 可以为以下方向提供指导，但 v0 暂时还没有同样严格的约束：

- 复杂 C# DLL hook
- 大范围运行时补丁或全局监听
- 高级 UI 修改
- 角色动画流程
- 游戏日志实时回传到 Codex
- 尚未验证官方尺寸或边框参考的素材类型

## 官方教程

本 skill 不内置官方教程仓库。需要时，skill 会先查找本地 `mod-tutorial` 或 `apocalyptic-journey-mod-tutorial` 目录，也可以拉取：

```text
https://github.com/meowalive/apocalyptic-journey-mod-tutorial.git
```

## 展示模组

Ashen Ledger 是一个创意工坊展示模组，用于说明 v0 skill 的能力边界和输出风格。

创意工坊链接：TODO_WORKSHOP_URL

下图记录了一次完整 AI 协助生成流程：内容摘要、生成素材、卡包封面、素材板和静态校验结果。

![Ashen Ledger AI generation result](docs/images/ashen-ledger-ai-generation-result.png)

## 许可

MIT License，copyright (c) 2026 Mr_Pardon。

详见 `LICENSE` 和 `NOTICE.md`。
