#!/usr/bin/env bash
# research 客户交付 PDF 一条命令入口：渲图 → 七项 lint（不过不出）→ weasyprint 出 PDF
# 用法: build.sh <工作区> [--min-chars N]
set -euo pipefail
WS="${1:?用法: build.sh <工作区> [--min-chars N]}"; shift || true
D="$(cd "$(dirname "$0")" && pwd)"
VENV="${RESEARCH_VENV:-$HOME/.venvs/research}"
if [ -x "$VENV/bin/python3" ]; then PY="$VENV/bin/python3"; else
  echo "⚠ venv 未装（先跑: bash $D/setup.sh），临时回退系统 python3"; PY="python3"
fi
bash "$D/render_charts.sh" "$WS"
"$PY" "$D/verify_report.py" "$WS" "$@"
"$PY" "$D/build_report.py" "$WS"
