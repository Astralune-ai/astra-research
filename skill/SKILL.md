---
name: research
description: |
  行业/市场尽调报告流水线 — 给一个研究对象（行业/赛道/项目/标的）+ 角度，跑一条「采集→综合→（验证）→成稿→包装」的工业级流水线，产出带引用的商业 research 报告。是一个**编排技能**：把现有零件串成一条线——
    · astra-probe   → 社媒/内容赛道数据（15 平台）
    · bg-check      → 关键玩家/主体小档 + 制裁名单筛查
    · astra-graphic / astra-imagen → 配图 / 信息图
    · astra-slide-impeccable / astralune-web → HTML/slide 展示版
    · astra-share   → 深度成稿
    · WebSearch/WebFetch 并行子 agent → 通用 web 调研 + 对抗式验证
  工作区开局指定（默认 ~/Asher/reports/<主题>_<日期>/），所有中间稿编号落盘可随时翻；同引擎双输出（内部精简档 / 客户品牌化档）。
  数据纪律：关键数字必有来源；估算标注；查不到标缺口；不替委托方臆造业务意图。
  触发词：/research、做研究报告、行业研究、市场研究、行业尽调、市场尽调、商业报告、竞品分析报告、调研报告、market research、industry report、due diligence report、研究一下 X 这个行业/赛道/项目。
  非本技能：查单个人 → bg-check；只要社媒数据 → astra-probe；写文章/内容 → astra-share。
---

# research — 行业/市场尽调报告流水线

## 这是什么
把散落的采集/验证/成稿/出图零件，串成一条可复用的 research 流水线。主轴是**行业/市场尽调报告**，可折入通用主题深调、公司/机构尽调、社媒赛道趋势作为交叉补充。

## 质量标准（每次必过 — 这条流水线好不好用的关键）
质量 = **信息获取能力 × 采集工作流 × 信息审核判断**，三者缺一不可。两份强制参考：
- [`references/quality-standard.md`](references/quality-standard.md) — 研究计划 gate（工作流）+ 信息审核 rubric（判断）+ 子 agent 源纪律模板
- [`references/source-registry.md`](references/source-registry.md) — 信息源注册表（获取能力），**插槽式可扩展**，新源（爬虫/API/付费库）随时加

## 工作区（开局指定，中间稿全落盘）
```
<输出目录>/                        ← 默认 ~/Asher/reports/<主题>_<YYYY-MM-DD>/
                                     指定了客户/人 → 进对应业务目录
  00_scope.md          ← 研究范围、问题、玩家名单、方法、档位（确认后才往下跑）
  01_sources/          ← 各研究线原始发现（带 URL，一线一份，审计轨迹）
  REPORT.md            ← 综合报告 + 结论（委托方读的那份）
  assets/              ← 配图/信息图（客户档生成；内部档可空）
  REPORT.html / .pdf   ← 客户档：展示版 / 交付版
```
> 经实跑验证：`01_sources/`（原始带引用）+ `REPORT.md`（综合）这两层已足够，不必再做 02/03/04 per-pillar 中间稿（会与 sources 重复）。

## 流水线（七个阶段：0 / 0.5 / 1 / 1.5 / 2 / 3 / 4）

### 阶段 0 · Scope（强制 gate，不可跳）
用**一次 AskUserQuestion** 收口，再写 `00_scope.md`，**停下来给委托方过**才往下跑（防跑偏）。必收口：
- **研究对象 + 角度**（行业/赛道/项目/标的；一句话定位）
- **目的/读者** → 决定怀疑者 vs 说服者视角：内部决策 DD / 给合作方支撑 / 中立 primer
- **研究重点**（多选）：市场与竞争 / 技术与竞品验证 / 投资可行性 / 需求侧·区位·合规 / 通用深调 …
- **输出目录**（默认 ~/Asher/reports/，指定客户进对应目录）
- **档位**：内部精简 / 客户品牌化
- **深度**：quick primer（快） / 深调（全流水线）
`00_scope.md` 写：标的速写、研究问题、相关方/玩家名单、方法、档位、什么暂缓。

### 阶段 0.5 · Research Plan（fan-out 前必经 gate）⭐ 质量的统一标准在这一步
详见 [`references/quality-standard.md`](references/quality-standard.md) §A。把每个研究问题拆成研究线，给每条线定：**必打源层级（Tier-1 优先）→ 用哪个源（查 [`references/source-registry.md`](references/source-registry.md)）→ 验收标准（≥2 个独立 Tier-1/2 源互证才算"查到"，查不到标缺口、不放 Tier-3 凑数）**，附已知头部源/玩家名单。写进 `00_scope.md` 的「研究计划」节。
- **强制度（Asher 定）**：大项目 / 高风险 / 对外交付 → **停下来给 Asher 过计划**再 fan-out；小调研 / 内部快查 → 自动跑，计划仍落盘可查。拿不准按大处理。

### 阶段 1 · Collect（并行 fan-out）
**主线程不直接吞海量原始数据。** 按研究计划的研究线，每线派一个 `general-purpose` 子 agent（一条消息里一次性发出，并行），各跑带引用的 research（按 source-registry 调 web / astra-probe / bg-check），原始发现各落 `01_sources/<NN>_<线名>.md`。
**每个子 agent 必带 quality-standard.md §B 的「源纪律 prompt 模板」**（背景+claim / 研究问题 / 源纪律+三角验证+自报数据压测 / 输出含「置信度与缺口」/ 时间盒），不靠它临场自觉。
> 典型四线（行业 DD）：市场与竞争格局 / 竞品规格与 claim 压测 / 需求侧与应用 / 区位与合规。按 scope 增删。

### 阶段 1.5 · 覆盖度检查（Collect 后、Assemble 前）
对照 quality-standard.md §D：scope 每个研究问题是否都有答案？有没有该跑没跑的源/模态？哪些落「缺口」→ 集中进 REPORT 待核实节，别藏。

### 阶段 2 · Assemble
把 `01_sources/` 综合成 `REPORT.md`（每条结论先过 quality-standard.md §C 判断 rubric：源分级 / 三角验证 / 自报数据压测 / 相关性 / 置信标注 / 对抗式 Verify）：
- **结构、站位、配图规则、PDF 管线，一律以 [`references/report-template.md`](references/report-template.md) 为唯一真源**（顾问综述前置 + 0–8 节 + 附录；中立站位不替委托方拍板；主章配图收尾豁免）。本文件不复述细节——复述必过期。
- 标的若附自报数据/对比表，**必须压测**，不照抄。

### 阶段 3 · Verify（对抗式，可暂缓）
对关键数字与论断逐条对抗式复核，标 `[UNSOURCED]`/存疑，写进 REPORT「待核实」或独立 `05_verify.md`。
**默认可暂缓**（委托方说「验证先放一边」时跳过，把缺口集中到 REPORT「待核实硬缺口」节，留作下一轮）。

### 阶段 4 · Package（按档位）
- **内部档**：REPORT.md 收工，可选配几张关键图（mermaid / astra-graphic）。
- **客户档（PDF）**：`bash _repo/scripts/build.sh <工作区>` 一条命令——渲图 → 七项 lint（不过不出）→ weasyprint 套信纸出 PDF；meta 写 REPORT.md front-matter，品牌走 brand pack（见 report-template.md「客户交付」节）。slide/HTML 展示版另走 astra-slide-impeccable / astralune-web；深度成稿可走 astra-share。

## 复用映射（什么时候调什么）
| 需要 | 调 |
|---|---|
| 社媒/内容赛道数据（15 平台） | `astra-probe` |
| 关键玩家小档 / 主体·制裁名单筛查 | `bg-check` |
| 配图 / 信息图 | `astra-graphic` · `astra-imagen` |
| HTML 展示版 / slide | `astralune-web` · `astra-slide-impeccable` |
| 深度成稿 | `astra-share` |
| podcast/mindmap 衍生 | `notebooklm` |
| 通用 web 调研 + 对抗验证 | 并行 general-purpose 子 agent（WebSearch/WebFetch） |

## 硬约束
- **数据纪律**：关键数字必有 URL；估算明确标「估算」；查不到标「缺口」，不编造可被 fact-check 的业务事实。
- **不臆造业务意图**：研究目的/读者/重点由委托方在 Scope gate 拍板，不脑补。
- **合规类研究只做风险识别**，不提供任何规避/绕开管制的建议。
- **写作禁令**（Asher 全局）：禁用「不是 X 而是 Y」「从 X 到 Y」「Not X but Y」等对比框架，正面直叙。
- bg-check 用于主体筛查时遵守其伦理边界（仅公开信息）。

## 首跑参考案例
`~/Asher/reports/PrintLive2026_3D打印无气轮胎_尽调_2026-06-09/` — 内部 DD 档、Verify 暂缓、九线并行采集的实例。注意：该跑批早于 0.5 研究计划 gate 与 Tier 标注规范定稿，scope 内研究计划为事后补记、sources 未逐条标 Tier（工作区已注明）——**新跑批以规范为准，勿照抄此例的缺项**。
