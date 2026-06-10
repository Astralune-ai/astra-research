#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""research 报告七项 lint —— 出 PDF 前必过（不过不出）。纯标准库，零依赖。

用法:  python3 verify_report.py <工作区目录> [--min-chars N]
检查（任一 ✗ 即退出码 1）:
  1. REPORT.md 顶部 front-matter 含 title/date/out
  2. 正文总字符 ≥ N（默认 20000，行业/市场尽调档；quick primer 可 --min-chars 调低）
  3. 不引用内部 01_sources 当来源（那是审计轨迹，报告只写官方 URL）
  4. 禁用句式：「不是 X 而是 Y」hard fail；「从 X 到 Y」框架仅警告（数字区间豁免）
  5. 每个引用图都有渲好的 PNG（.svg 引用按构建规则折算成 .png 检查）
  6. 主章（## 一、…—— ## 六、…）每章 ≥1 图或表；收尾章/摘要/顾问综述豁免（Asher 2026-06-10 定）
  7. gate 工件：00_scope.md 含「研究计划」节；01_sources/*.md 逐条标 Tier（或带「规范注」豁免标记）
"""
import os
import re
import sys

CN_NUM = "一二三四五六"


def main():
    args = sys.argv[1:]
    min_chars = 20000
    if "--min-chars" in args:
        i = args.index("--min-chars")
        min_chars = int(args[i + 1])
        del args[i:i + 2]
    ws = os.path.abspath(args[0] if args else ".")
    md_path = os.path.join(ws, "REPORT.md")
    fails, warns = [], []

    def ok(label):
        print(f"  ✓ {label}")

    def bad(label, detail=""):
        fails.append(label)
        print(f"  ✗ {label}" + (f" — {detail}" if detail else ""))

    def warn(label, detail=""):
        warns.append(label)
        print(f"  ⚠ {label}" + (f" — {detail}" if detail else ""))

    print(f"verify_report: {ws}")
    if not os.path.isfile(md_path):
        bad("REPORT.md 存在", md_path)
        sys.exit(1)
    raw = open(md_path, encoding="utf-8").read()

    # 1. front-matter
    m = re.match(r'^---[ \t]*\n(.*?)\n---[ \t]*\n', raw, re.S)
    if m:
        keys = {l.split(':', 1)[0].strip() for l in m.group(1).splitlines() if ':' in l}
        missing = {'title', 'date', 'out'} - keys
        bad("front-matter 必填字段", f"缺 {missing}") if missing else ok("front-matter（title/date/out）")
        body = raw[m.end():]
    else:
        bad("front-matter 存在", "REPORT.md 顶部缺 YAML meta（见 report-template.md「客户交付」节）")
        body = raw

    # 2. 篇幅
    n = len(body)
    ok(f"篇幅 {n:,} ≥ {min_chars:,} 字符") if n >= min_chars else bad("篇幅", f"{n:,} < {min_chars:,} 字符（补真内容，不灌水）")

    # 3. 内部引用
    hits = len(re.findall(r'01_sources', body))
    ok("无内部 01_sources 引用") if hits == 0 else bad("来源写法", f"{hits} 处引用内部 01_sources——报告只写官方 URL")

    # 4. 禁用句式
    banned = [x for x in re.finditer(r'不是[^。\n]{1,20}而是', body)]
    if banned:
        bad("禁用句式「不是…而是」", "；".join(b.group(0) for b in banned[:3]))
    else:
        ok("无「不是…而是」")
    fxty = [x.group(0) for x in re.finditer(r'从[^。\n，\d]{1,10}到[^。\n，]{1,10}', body)]
    if fxty:
        warn("疑似「从 X 到 Y」框架（人工确认，数字区间豁免）", "；".join(fxty[:3]))

    # 5. 图资产
    text = re.sub(r'\(assets/([^)\s]+)\.svg\)', r'(assets/\1.png)', body)
    missing = [p for p in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
               if not p.startswith(("http://", "https://")) and not os.path.isfile(os.path.join(ws, p))]
    ok("引用图的 PNG 全部存在") if not missing else bad("图资产", "缺 " + "、".join(missing))

    # 6. 主章配图（一–六）
    secs = re.split(r'^## ', body, flags=re.M)[1:]
    lacking = []
    for s in secs:
        head = s.split("\n", 1)[0]
        if re.match(rf'[{CN_NUM}]、', head):
            has_fig = bool(re.search(r'!\[', s))
            has_tbl = bool(re.search(r'^\|.*\|\s*$\n^\|[-: |]+\|', s, re.M))
            if not (has_fig or has_tbl):
                lacking.append(head[:18])
    if lacking:
        bad("主章配图（一–六每章 ≥1 图/表）", "缺：" + "、".join(lacking))
    else:
        ok("主章配图（收尾章豁免）")

    # 7. gate 工件
    scope = os.path.join(ws, "00_scope.md")
    if os.path.isfile(scope):
        s = open(scope, encoding="utf-8").read()
        ok("00_scope 含「研究计划」节") if "研究计划" in s else bad("研究计划 gate", "00_scope.md 无「研究计划」节（quality-standard §A）")
    else:
        warn("无 00_scope.md（非标准工作区？）")
    src_dir = os.path.join(ws, "01_sources")
    if os.path.isdir(src_dir):
        no_tier = []
        for f in sorted(os.listdir(src_dir)):
            if f.endswith(".md"):
                c = open(os.path.join(src_dir, f), encoding="utf-8").read()
                if not (re.search(r'Tier[- ]?[123]', c) or "规范注" in c):
                    no_tier.append(f)
        if no_tier:
            bad("sources Tier 标注（quality-standard §B）", "缺：" + "、".join(no_tier))
        else:
            ok("sources Tier 标注（或带规范注豁免）")
    else:
        warn("无 01_sources/（非标准工作区？）")

    print(f"—— {'FAIL ✗ ' + str(len(fails)) + ' 项不过，不出 PDF' if fails else 'PASS ✓ 全部通过'}"
          + (f"（{len(warns)} 条警告需人工过目）" if warns else ""))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
