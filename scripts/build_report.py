#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""research 客户交付 PDF 构建器（参数化模板 · 唯一副本，禁止再 cp 出分身）。

用法:  python3 build_report.py <工作区目录>
输入:  <工作区>/REPORT.md，顶部必须有 YAML front-matter:
       title / date / out 必填; kicker / subtitle / classification / report_type /
       brand(默认 astralune) / footnote 可选。title、subtitle 内可用 <br> 断行。
信纸:  brand pack = <repo>/brand/<brand>/{cover.png, inner-soft.png} 整页背景。
原则:  真信纸当整页背景、正文流在留白区、不加角标/页眉/logo 占位；
       黑白灰单色（禁蓝禁金）；文字压淡水印正常。
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def die(msg):
    print(f"✗ build_report: {msg}")
    sys.exit(1)


def parse_front_matter(text):
    m = re.match(r'^---[ \t]*\n(.*?)\n---[ \t]*\n', text, re.S)
    if not m:
        die("REPORT.md 缺 YAML front-matter（title/date/out 必填）——见 report-template.md「客户交付」节")
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line and not line.lstrip().startswith('#'):
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    missing = [k for k in ('title', 'date', 'out') if not meta.get(k)]
    if missing:
        die(f"front-matter 缺必填字段: {', '.join(missing)}")
    return meta, text[m.end():]


def esc(s):
    """转义裸 & （保留 <br> 与已有实体）。"""
    return re.sub(r'&(?!\w+;)', '&amp;', s or '')


def fix_lists(t):
    """列表块前自动补空行（CommonMark：列表前无空行会被压成一段）。"""
    lines = t.split("\n")
    is_li = lambda x: bool(re.match(r'^\s*(\d+[.)]|[-*+])\s', x))
    is_tr = lambda x: x.lstrip().startswith("|")
    out = []
    for x in lines:
        if is_li(x) and out and out[-1].strip() and not is_li(out[-1]) and not is_tr(out[-1]):
            out.append("")
        out.append(x)
    return "\n".join(out)


def fix_blockquotes(t):
    """多行引用块：下一行是新加粗字段(> **)时，本行补 <br>（否则连续 > 行被并段）。
    边界：只覆盖「> **字段**」式标签行；普通连续 > 行仍按 CommonMark 并段。"""
    lines = t.split("\n")
    out = []
    for i, x in enumerate(lines):
        nx = lines[i + 1] if i + 1 < len(lines) else ""
        if (x.startswith(">") and nx.startswith(">") and re.match(r'^>\s*\*\*', nx)
                and x.rstrip() and not x.rstrip().endswith("<br>")):
            x = x.rstrip() + " <br>"
        out.append(x)
    return "\n".join(out)


def main():
    ws = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    md_path = os.path.join(ws, "REPORT.md")
    if not os.path.isfile(md_path):
        die(f"找不到 {md_path}")

    text = open(md_path, encoding="utf-8").read()
    meta, text = parse_front_matter(text)

    # —— 护栏 1：brand pack 存在
    brand = meta.get("brand", "astralune")
    brand_dir = os.path.join(REPO, "brand", brand)
    cover_png = os.path.join(brand_dir, "cover.png")
    inner_png = os.path.join(brand_dir, "inner-soft.png")
    for p in (cover_png, inner_png):
        if not os.path.isfile(p):
            die(f"brand pack 缺文件: {p}（brand pack 规范见 {os.path.join(REPO,'brand','README.md')}）")

    # SVG 引用换成 Chrome 渲好的 PNG（weasyprint 渲不动含 CSS 变量的 SVG）
    text = re.sub(r'\(assets/([^)\s]+)\.svg\)', r'(assets/\1.png)', text)
    text = fix_lists(text)
    text = fix_blockquotes(text)

    # —— 护栏 2：所有引用图存在
    missing = []
    for p in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
        if not p.startswith(("http://", "https://")) and not os.path.isfile(os.path.join(ws, p)):
            missing.append(p)
    if missing:
        die("引用的图不存在（先跑 render_charts.sh？）:\n  " + "\n  ".join(missing))

    # 顾问综述前置块：提取放封面与目录之间、不进 TOC
    import markdown
    from markdown.extensions.toc import slugify_unicode
    from weasyprint import HTML

    front_html = ""
    mf = re.search(r'<!-- FRONT-OVERVIEW -->(.*?)<!-- /FRONT-OVERVIEW -->', text, re.S)
    if mf:
        text = text.replace(mf.group(0), "")
        front_html = ('<div class="front">'
                      + markdown.markdown(mf.group(1), extensions=['tables', 'attr_list', 'md_in_html', 'sane_lists'])
                      + '</div>')

    md = markdown.Markdown(
        extensions=['tables', 'fenced_code', 'toc', 'attr_list', 'sane_lists', 'md_in_html'],
        extension_configs={'toc': {'slugify': slugify_unicode, 'toc_depth': '2-3'}})
    body = md.convert(text)
    toc_html = md.toc

    css = CSS_TEMPLATE.replace("@@INNER@@", inner_png).replace("@@COVER@@", cover_png)

    rows = [f'<div class="row"><b>编制日期</b><span>{esc(meta["date"])}</span></div>']
    if meta.get("report_type"):
        rows.append(f'<div class="row"><b>报告类型</b><span>{esc(meta["report_type"])}</span></div>')
    if meta.get("classification"):
        rows.append(f'<div class="row"><b>密&nbsp;&nbsp;&nbsp;&nbsp;级</b><span>{esc(meta["classification"])}</span></div>')
    cover = f"""
<section class="cover">
  <div class="kicker">{esc(meta.get('kicker', ''))}</div>
  <h1>{esc(meta['title'])}</h1>
  <div class="sub">{esc(meta.get('subtitle', ''))}</div>
  <div class="meta">{''.join(rows)}</div>
  <div class="conf">{esc(meta.get('footnote', ''))}</div>
</section>
"""
    toc = f'<div class="toc-wrap"><div class="toc-h">目录　CONTENTS</div><div class="toc">{toc_html}</div></div>'
    full = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            f'<style>{css}</style></head><body>{cover}{front_html}{toc}{body}</body></html>')

    out = os.path.join(ws, meta["out"])
    HTML(string=full, base_url=ws).write_pdf(out)

    pages = ""
    try:
        import pypdf
        pages = f" | {len(pypdf.PdfReader(out).pages)} 页"
    except Exception:
        pass
    print(f"✓ PDF => {out} | {os.path.getsize(out)} bytes{pages} | brand={brand}")


# ============ 样式（黑白灰单色：炭黑 #26282c / 银灰 #9fa1a6 / 近黑 #1a1b1e / 浅灰 #f5f5f6）============
CSS_TEMPLATE = r"""
/* 内页：真信纸整页背景，正文流在留白区；背景全幅 A4 定位抵消页边距 */
@page {
  size: A4;
  margin: 40mm 24mm 20mm 24mm;
  background-image: url('@@INNER@@');
  background-repeat: no-repeat;
  background-size: 210mm 297mm; background-position: -24mm -40mm;
  @bottom-center{ content: counter(page) " / " counter(pages);
                  font: 8pt 'PingFang SC',sans-serif; color: #8d9095; vertical-align: bottom; padding-bottom: 3mm; }
}
@page coverpage {
  margin: 0;
  background: url('@@COVER@@') no-repeat; background-size: 100% 100%;
  @bottom-center{content:none}
}
* { box-sizing: border-box; }
html { font-family: 'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif; color:#202124; }
body { margin:0; font-size:9.8pt; line-height:1.62; }

/* 顾问综述（目录前置） */
.front { page-break-after: always; }
.front h2 { page-break-before: avoid; font-size:16pt; color:#26282c; font-weight:700;
  border-bottom:2px solid #26282c; padding-bottom:3mm; margin:0 0 5mm; }
.front h2::before { content:none; }
.front h3 { font-size:11.5pt; color:#34363b; font-weight:700; margin:6mm 0 2.5mm; page-break-after:avoid; }
.front p { margin:0 0 3mm; text-align:justify; }
.front blockquote { margin:4mm 0; padding:3.5mm 5mm; background:rgba(244,244,245,.9);
  border-left:3px solid #9fa1a6; color:#3c3e44; font-size:9.9pt; border-radius:0 3px 3px 0; }
.front blockquote p { margin:0; }

/* 封面：标题排进中部白区，不占 logo/边框位置 */
.cover { page: coverpage; position: relative; height: 297mm; page-break-after: always; }
.cover .kicker { position:absolute; top:88mm; left:32mm; right:32mm;
  font-size:10pt; letter-spacing:3px; color:#9fa1a6; font-weight:600; }
.cover h1 { position:absolute; top:98mm; left:32mm; right:30mm; margin:0;
  font-family:'Songti SC','STSong',serif; font-size:25pt; line-height:1.4; font-weight:700; color:#1a1b1e; }
.cover .sub { position:absolute; top:135mm; left:32mm; right:32mm;
  font-size:11.5pt; color:#4a4c52; line-height:1.75; }
.cover .meta { position:absolute; bottom:54mm; left:32mm; right:32mm; }
.cover .meta .row { display:flex; gap:6mm; font-size:9.8pt; color:#3b3d42;
  padding:2.5mm 0; border-top:1px solid #e1e1e3; }
.cover .meta .row b { color:#26282c; min-width:24mm; display:inline-block; }
.cover .conf { position:absolute; bottom:40mm; left:32mm; font-size:8.4pt; color:#8d9095; letter-spacing:.5px; }

/* 目录 */
.toc-wrap { page-break-after: always; }
.toc-h { font-family:'PingFang SC',sans-serif; font-size:16pt; color:#26282c;
  font-weight:700; border-bottom:2px solid #26282c; padding-bottom:3mm; margin:0 0 6mm; }
.toc ul { list-style:none; margin:0; padding:0; }
.toc > ul > li { margin:2.6mm 0; }
.toc > ul > li > a { font-size:11pt; font-weight:600; color:#202124; }
.toc ul ul { margin:1mm 0 1mm 7mm; }
.toc ul ul li a { font-size:9.4pt; color:#4d4f55; font-weight:400; }
.toc a { text-decoration:none; }
.toc li a::after { content: leader('·') " " target-counter(attr(href url), page); color:#a5a6aa; font-size:8.6pt; }

/* 正文 */
h2 { font-size:14pt; color:#26282c; font-weight:700; margin:0 0 5mm;
  padding-bottom:3mm; border-bottom:2px solid #e4e4e6; page-break-before: always; page-break-after: avoid; }
h2::before { content:""; display:inline-block; width:5px; height:14.5pt; background:#9fa1a6;
  margin-right:8px; vertical-align:-2px; }
h3 { font-size:11.5pt; color:#34363b; font-weight:700; margin:7mm 0 3mm; page-break-after: avoid; }
h4 { font-size:11pt; color:#2c2e33; font-weight:700; margin:5mm 0 2mm; }
p  { margin:0 0 3.2mm; text-align:justify; }
strong { color:#1a1b1e; font-weight:700; }
a { color:#26282c; text-decoration:none; word-break:break-all; }
ul,ol { margin:0 0 3.5mm; padding-left:6mm; }
li { margin:1.3mm 0; }
blockquote { margin:4mm 0; padding:3mm 5mm; background:rgba(244,244,245,.9); border-left:3px solid #9fa1a6;
  color:#3c3e44; font-size:9.9pt; border-radius:0 3px 3px 0; page-break-inside:avoid; }
blockquote p { margin:0; }
table { width:100%; border-collapse:collapse; margin:4mm 0; font-size:8.3pt; }
thead { display:table-header-group; }
th { background:#26282c; color:#fff; font-weight:600; text-align:left; padding:2.6mm 3mm; font-size:8.8pt; }
td { padding:2.4mm 3mm; border-bottom:1px solid #e4e4e6; vertical-align:top; background:rgba(255,255,255,.78); }
tbody tr:nth-child(even) td { background:rgba(245,245,246,.85); }
tr { page-break-inside:avoid; }
img { display:block; margin:5mm auto; max-width:80%; border:1px solid #e4e4e6;
  border-radius:5px; box-shadow:0 1px 4px rgba(0,0,0,.06); page-break-inside:avoid; background:#fff; }
hr { border:none; border-top:1px solid #e4e4e6; margin:6mm 0; }
code { font-family:'SF Mono',Menlo,monospace; font-size:8.6pt; background:#f0f0f1; padding:.5mm 1.5mm; border-radius:3px; }
"""

if __name__ == "__main__":
    main()
