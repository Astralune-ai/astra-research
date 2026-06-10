# brand packs — 报告信纸/品牌包（内置兜底）

> **2026-06-10 起，品牌包的正式家是中央品牌库 `astra-brand`**（仓 `Astralune-ai/astra-brand`，运行时 `~/.astra/brands`，规范 `BRAND_SPEC.md`，跨技能统一接口 + brand.json 清单 + 无信纸客户的模板生成器）。本目录仅作**未装中央库时的兜底**，构建器解析顺序：中央库 → 本目录。

每个子目录 = 一个品牌包，REPORT.md front-matter 用 `brand: <目录名>` 选用（默认 `astralune`）。

## 包规范（两个文件，名字固定）
| 文件 | 要求 |
|---|---|
| `cover.png` | 封面整页背景，A4 比例（约 1055×1491 或同比例更高清）。标题区留白在中部（脚本把标题排在 ~98mm 起、左右 32mm 缩进）。 |
| `inner-soft.png` | 内页整页背景，A4 比例。头部装饰（logo/横线）止于 ~40mm，底部装饰始于 ~277mm——正文边距 `40mm 24mm 20mm 24mm` 卡在两线之间。水印要淡（文字直接压上去）。 |

## 给客户机加新品牌
1. 建 `brand/<客户名>/`，放两张按上述规范做的 PNG（水印重就用 PIL 把淡像素推白，参考 astralune 的 soft 版做法）。
2. 客户工作区 REPORT.md front-matter 写 `brand: <客户名>`。
3. 配色原则不变：黑白灰单色排版，信纸自带的品牌色由背景图本身呈现。

> Astralune 包的正式来源在公司品牌柜
> `~/Company/X.H._Noctuer_Holdings_Pty_Ltd/07_品牌资产_branding/Astralune/素材_assets/信纸_letterhead/`
> （cover = astralune_letterhead_cover_v1.png；inner-soft = astralune_letterhead_inner_soft_v1.png）。
