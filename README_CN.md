<div align="center">

# astra-research

> *「一条命令进去，一份带品牌、可溯源的尽调报告出来。」*

![License](https://img.shields.io/badge/License-Source%20Available-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)
![Quality Gates](https://img.shields.io/badge/%E8%B4%A8%E9%87%8F%E9%97%B8%E9%97%A8-7%20%E9%A1%B9%20lint-brightgreen)

**[English](README.md) · [中文](README_CN.md)**

<br>

**还在花一周时间把零散的检索结果拼成一份市场报告？**

**还在客户交付前夜两点手调边距、字体和信纸？**

**还说不清报告里每个数字到底出自哪个来源？**

<br>

### 行业/市场尽调流水线：并行研究 agent → 质量闸门把关 → 信纸品牌化 PDF。

[**为什么有它**](#为什么有它) · [**你得到什么**](#你得到什么) · [**快速开始**](#快速开始) · [**流水线**](#流水线怎么跑) · [**仓库结构**](#仓库结构)

</div>

<br>

---

## 为什么有它

之前，做一份站得住的尽调报告意味着：开十几个检索标签页、把发现一段段贴进文档、追补丢失的引用、跟渲染不出来的图表搏斗、最后再跟排版软件耗到深夜——而且质量取决于那天是谁在做。

有了 astra-research，你只需要给出标的和角度。流水线按源纪律并行派出研究 agent，按固定结构组装中立站位的报告，跑 **7 项机械化质量闸门**（不过闸的报告永远变不成 PDF），最后渲出套公司信纸的交付件——每一次都是同一个标准。首个生产跑批就交付了一份真实的 **37 页客户级 PDF**，**131 个官方来源 URL、关键论断零无源引用**。

## 你得到什么

| 能力 | 说明 |
|---|---|
| 🧭 顾问综述前置 | 目录之前先给委托方一页：项目究竟是怎么回事、机遇与风险、实施三视角——把全貌讲透，不逼客户选 |
| 🏗️ 固定报告骨架 | 市场环境与结论 → 细分 2×2 → 产业链具名 → 业务逻辑 → 自述 vs 实际 → 两面摆开 + 附录 |
| 🔬 源纪律 | Tier-1/2/3 源分级、三角验证、置信标注；查不到就标缺口，绝不糊弄 |
| 🚦 7 项 lint 闸门 | 篇幅达标、只引官方 URL、禁用句式扫描、图资产齐全、主章配图、scope 与源分级工件 |
| 🎨 品牌包 | 信纸、配色、安全边距统一从中央品牌库 [astra-brand](https://github.com/Astralune-ai/astra-brand) 解析——换客户只改 front-matter 一行 |
| 📄 确定性 PDF | Mermaid 图走 headless Chrome 栅格化、信纸全幅定位、中文排版、目录真页码 |

## 快速开始

```bash
bash scripts/setup.sh                 # 一次性：钉版本 venv + 工具链体检
bash scripts/build.sh <工作区>         # 渲图 → 7 项 lint → 品牌化 PDF
```

工作区 = `00_scope.md + 01_sources/ + REPORT.md + assets/`。报告元信息写在 `REPORT.md` 顶部 YAML front-matter：

```yaml
---
title: Acme 2026<br>市场尽职调查
date: 2026-06-10
out: Acme_尽调报告_2026-06-10.pdf
brand: astralune          # ~/.astra/brands 里的任意包
classification: 机密 CONFIDENTIAL
---
```

## 流水线怎么跑

`Scope gate → 研究计划 gate → 并行 Collect（子 agent）→ 覆盖度检查 → Assemble →（对抗式 Verify）→ Package`

`skill/` 里的 prompt 负责编排研究与判断；`scripts/` 工具链接管全部确定性步骤——渲染、校验、构建——脚本能干的活不花一个 token。

## 仓库结构

```
skill/                  # Claude Code 技能 prompt（流水线 / 质量标准 / 报告模板 / 源注册表）
scripts/
  build.sh              # 一条命令入口：渲图 → lint → PDF
  render_charts.sh      # .mmd → SVG → headless Chrome 2× PNG（幂等）
  verify_report.py      # 7 项 lint 闸门——不过闸的报告不出门
  build_report.py       # weasyprint 构建器；meta 读 front-matter，品牌走品牌包
  setup.sh / sync_skill.sh
brand/                  # 内置兜底品牌包（中央品牌库 astra-brand 优先）
requirements.txt        # 钉版本：weasyprint / markdown / Pillow / pypdf
```

## 环境要求

macOS + Chrome、[beautiful-mermaid](https://github.com/Astralune-ai) CLI、中文字体（PingFang/Songti，系统自带）。Python 依赖由 `setup.sh` 钉版本隔离在 `~/.venvs/research`。

---

<div align="center">

**给出标的。拿到报告。每个数字可溯源。**

![astra-research](https://img.shields.io/badge/astra--research-%E5%B0%BD%E8%B0%83%EF%BC%8C%E5%B7%A5%E4%B8%9A%E5%8C%96-black?style=for-the-badge)

Powered by [**Astralune**](https://github.com/Astralune-ai) · Astra Source Available License v1.0

</div>
