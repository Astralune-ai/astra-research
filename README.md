# astra-research

Astralune 的行业/市场尽调报告流水线（Claude Code skill）——「采集 → 综合 → 验证 → 成稿 → 客户交付 PDF」一条线。skill prompt 编排研究（并行子 agent fan-out + 质量 gate），脚本接管全部确定性步骤（图表渲染 / 七项 lint / weasyprint 套信纸出 PDF）。

## 仓库结构
```
skill/                  # 技能 prompt（SKILL.md + references/，由 scripts/sync_skill.sh 从部署机真源同步）
  SKILL.md              #   流水线编排：Scope gate → 研究计划 gate → Collect → 覆盖度 → Assemble → Verify → Package
  references/
    quality-standard.md #   研究计划 gate + 子 agent 源纪律 + 审核 rubric（Tier 分级/三角验证/对抗式 Verify）
    report-template.md  #   报告站位 + 结构（顾问综述前置 + 0–8 节）+ PDF 管线（唯一真源）
    source-registry.md  #   插槽式信息源注册表（加爬虫/API/付费库的地方）
scripts/
  build.sh              # 一条命令出 PDF：渲图 → lint → 构建
  render_charts.sh      # assets/*.mmd → SVG → 去 @import → headless Chrome 截 2× PNG
  verify_report.py      # 七项 lint（篇幅/来源写法/禁句式/图资产/主章配图/gate 工件），不过不出 PDF
  build_report.py       # weasyprint 构建器：meta 读 REPORT.md front-matter，信纸走 brand pack
  setup.sh              # venv + 钉版本依赖 + 外部工具体检
  sync_skill.sh         # 推仓前同步 skill prompt（单向 根→repo）
brand/                  # 品牌包（cover.png + inner-soft.png 整页背景），front-matter `brand:` 选用
requirements.txt
```

## 安装（部署机）
```bash
# 1) 放置：本仓库 → ~/.claude/commands/research/_repo/（skill/ 内容提一份到 ~/.claude/commands/research/ 根）
# 2) 依赖：
bash scripts/setup.sh        # 建 ~/.venvs/research + weasyprint/markdown/Pillow/pypdf（钉版本）
# 另需：beautiful-mermaid CLI（~/.local/bin/mermaid 或 MERMAID_BIN）、Chrome、中文字体（macOS 自带）
```

## 出报告
```bash
bash scripts/build.sh <工作区>          # 工作区 = 00_scope.md + 01_sources/ + REPORT.md + assets/
```
REPORT.md 顶部写 YAML front-matter（`title/date/out` 必填，`kicker/subtitle/classification/report_type/brand/footnote` 可选）。lint 不过不出 PDF；quick primer 档可 `--min-chars` 调低篇幅线。

## 设计原则
- **标准强制质量，不靠临场自觉**：研究计划 gate + 子 agent 源纪律模板 + lint 闸门，三层都可被脚本检查。
- **单一真源**：报告结构/配色/管线只写在 report-template.md；构建器只有一份，meta 参数化，禁止 cp 改副本。
- **确定性步骤交给脚本**：模型只做研究与判断，渲染/校验/构建零 token。
- **黑白灰单色排版（禁蓝禁金）**；真信纸整页背景，正文流在留白区，不加角标/页眉占位。

## 已吸收的坑（排障备查）
Mermaid SVG 含 CSS 变量 → librsvg/weasyprint 渲成黑块，必须 Chrome 截 PNG；weasyprint `@page` 背景默认画在边距内 → `background-size:210mm 297mm` + 负偏移全幅定位；CommonMark 列表前要空行、连续 `> **字段**` 并段 → `_fix_lists`/`_fix_bq` 构建时自动修。

---
© Astralune (X.H. Noctuer Holdings Pty Ltd) · 内部/客户部署用，未授权请勿分发。
