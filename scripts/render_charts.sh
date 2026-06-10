#!/usr/bin/env bash
# 图表渲染：assets/*.mmd → beautiful-mermaid SVG → 去 Google Fonts @import → headless Chrome 截 2× PNG
# （weasyprint/librsvg 渲不动含 CSS 变量的 SVG，会塌成黑块——必须走 Chrome）
# 用法: render_charts.sh <工作区> [--force]    # 默认 PNG 比 .mmd 新则跳过
set -euo pipefail
WS="${1:?用法: render_charts.sh <工作区> [--force]}"
A="$WS/assets"
MERMAID="${MERMAID_BIN:-$HOME/.local/bin/mermaid}"

CHROME=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "/Applications/Chromium.app/Contents/MacOS/Chromium" \
         "$(command -v google-chrome 2>/dev/null || true)" \
         "$(command -v chromium 2>/dev/null || true)"; do
  [ -n "$c" ] && [ -x "$c" ] && CHROME="$c" && break
done

shopt -s nullglob
MMDS=("$A"/*.mmd)
if [ ${#MMDS[@]} -eq 0 ]; then echo "render_charts: $A 无 .mmd，跳过"; exit 0; fi
[ -x "$MERMAID" ] || { echo "✗ 找不到 mermaid CLI（$MERMAID，可用 MERMAID_BIN 覆盖）"; exit 1; }
[ -n "$CHROME" ] || { echo "✗ 找不到 Chrome/Chromium（SVG→PNG 需要）"; exit 1; }

for mmd in "${MMDS[@]}"; do
  base="${mmd%.mmd}"; svg="$base.svg"; png="$base.png"
  if [ "${2:-}" != "--force" ] && [ -f "$png" ] && [ "$png" -nt "$mmd" ]; then
    echo "· $(basename "$png") 已最新，跳过"; continue
  fi
  "$MERMAID" "$mmd" -o "$svg"
  # 去 @import（Chrome 离线截图卡远程字体）+ 读 viewBox 尺寸
  dims=$(python3 - "$svg" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
s = re.sub(r'@import[^;]+;', '', s)
open(p, "w", encoding="utf-8").write(s)
m = re.search(r'viewBox="\s*[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)', s)
w, h = (int(float(m.group(1))) + 2, int(float(m.group(2))) + 2) if m else (1200, 800)
print(w, h)
PY
)
  read -r W H <<< "$dims"
  "$CHROME" --headless --screenshot="$png" --window-size="$W,$H" \
            --force-device-scale-factor=2 --hide-scrollbars \
            --default-background-color=FFFFFFFF "file://$svg" 2>/dev/null
  [ -s "$png" ] || { echo "✗ Chrome 截图失败: $png"; exit 1; }
  echo "✓ $(basename "$png") (${W}x${H} @2x)"
done
