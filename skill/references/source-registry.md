# research 信息源注册表（插槽式可扩展模块）

> **设计原则**：信息源是**插槽式模块**，新源（爬虫 / 新 API / 付费库）随时往里加，主流程不改。
> 现阶段（Asher 2026-06-10）只用**开放可得**的源，尽量榨干；其余留好插槽。
> 调度方式：研究计划 gate 把「研究线 → 源」映射好，Collect 按映射派子 agent 调对应源。

## 一、现在可用（开放 / 已接）

| 源 | Tier | 覆盖 / 强在 | 调用方式 | 状态 |
|---|---|---|---|---|
| WebSearch / WebFetch | T1–T3 混 | 开放 web、新闻、官网、政府/监管、学术、公司 IR、市场报告**摘要层** | 内置 | ✅ |
| 政府/监管/官方规格/公司 IR/学术 | **T1** | 权威一手（filings、官方 spec、监管站、论文） | WebFetch 直取官方页 | ✅ |
| astra-probe（TikHub 15 平台） | T2 | 社媒/内容赛道、达人、舆情、**需求侧信号**、跨境选品 | `~/.claude/commands/astra-probe/astra_probe.sh --platform X <action>` | ✅ |
| bg-check（maigret 3158 站 + LinkedIn + Google） | T1–T2 | 人物/公司**身份**、履历、跨平台找人 | `/bg-check` | ✅ |
| OFAC SDN / BIS Entity List / EU 制裁名单 | **T1** | **制裁/出口管制名单筛查** | WebFetch 官方名单页 / 公开搜索 API | ✅ |
| 本地附件 / Drive / Lark | — | 委托方给的私有数据、附件 | Read / google-workspace / lark-* | ✅ |

## 二、待接入（认证/给凭证后即用）

| 源 | Tier | 覆盖 | 接入方式 | 状态 |
|---|---|---|---|---|
| 金融专业库 CapIQ/FactSet/PitchBook/S&P/Moody's/Morningstar | **T1** | 交易、财务、可比公司硬数据 | `mcp__plugin_financial-analysis_*__authenticate`（Asher 有账号则认证） | ⏳ 待认证 |
| 付费工商/贸易库（企查查·天眼查·海关数据·行业库） | T1–T2 | 中国工商、进出口、行业 | 凭证进 vault，运行时读 | ⏳ 待加 |
| 一手调研（专家访谈/渠道核查） | T1 | 真 DD 护城河 | 我列问题清单 → Asher 转给对的人 | ⏳ 按需 |

## 三、可扩展槽位 —— 怎么加新源（后面加爬虫/API 的地方）

加一个新源 = 两步，**主流程不动**：

1. **登记**：在「一、现在可用」加一行（源 / Tier / 覆盖 / 调用 / 状态）。
2. **若需代码**（爬虫 / 新 API）：仿 **astra-probe wrapper 模式**——
   - 脚本放 `~/.claude/commands/research/sources/<name>.{sh,py}`，做一个统一入口包装底层 API/爬虫；
   - 对外暴露**统一动作**：`search` / `fetch` / `list`（与 astra-probe 的 7 动作同思路），让研究计划的「研究线→源」映射能直接调；
   - 凭证一律进 `~/Asher/_私钥_vault`，运行时读，不硬编码；
   - 在本表登记 + 标 Tier + 标"它强在哪/拿不到啥"。

**约束**：每个源适配器自报可信层级（Tier）与覆盖边界；judgment rubric（见 quality-standard.md §C）按 Tier 决定它产出的数据进不进报告。新源不豁免源纪律。
