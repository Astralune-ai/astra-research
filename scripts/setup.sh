#!/usr/bin/env bash
# research PDF 管线安装：建 venv + 钉版本依赖 + 外部工具体检（macOS）
# 用法: bash setup.sh    （venv 位置可用 RESEARCH_VENV 覆盖，默认 ~/.venvs/research）
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
V="${RESEARCH_VENV:-$HOME/.venvs/research}"

python3 -m venv "$V" 2>/dev/null || true
"$V/bin/pip" install -q --upgrade pip
"$V/bin/pip" install -q -r "$D/../requirements.txt"

if "$V/bin/python3" -c "import weasyprint,markdown,PIL,pypdf,sys;print(f'✓ venv OK: weasyprint {weasyprint.__version__} / markdown {markdown.__version__} / python {sys.version.split()[0]}')"; then :; else
  echo "✗ weasyprint 导入失败——macOS 先装系统库: brew install pango libffi glib"; exit 1
fi

[ -x "${MERMAID_BIN:-$HOME/.local/bin/mermaid}" ] && echo "✓ mermaid CLI（beautiful-mermaid）" \
  || echo "⚠ 缺 mermaid CLI → 图表渲染不可用（装 beautiful-mermaid 或设 MERMAID_BIN）"
[ -e "/Applications/Google Chrome.app" ] || command -v chromium >/dev/null 2>&1 \
  && echo "✓ Chrome/Chromium" || echo "⚠ 缺 Chrome/Chromium → SVG 转 PNG 不可用"
if [ -e "/System/Library/Fonts/PingFang.ttc" ] || fc-list 2>/dev/null | grep -qi "PingFang\|Songti"; then
  echo "✓ 中文字体（PingFang/Songti）"
else
  echo "⚠ 未检出 PingFang/Songti（macOS 自带；其他系统需装中文字体）"
fi
echo "—— 安装完成。出报告: bash $D/build.sh <工作区>"
