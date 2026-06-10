#!/usr/bin/env bash
# 推 GitHub 前必跑：把技能 prompt 文件（真源在 commands/research/ 根）同步进 _repo/skill/
# 方向永远是 根 → repo，单向；改技能永远改根目录的文件。
set -euo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"      # _repo
ROOT="$(cd "$D/.." && pwd)"                # commands/research
mkdir -p "$D/skill/references"
cp -f "$ROOT/SKILL.md" "$D/skill/SKILL.md"
cp -f "$ROOT/references/"*.md "$D/skill/references/"
echo "✓ skill prompt 已同步 → $D/skill/（真源: $ROOT，单向 根→repo）"
