#!/usr/bin/env bash
# Install every skill for Claude Code, Codex, Gemini CLI and Antigravity (user level).
# Usage: bash install.sh            (all tools)
#        bash install.sh claude     (one tool: claude | codex | gemini | antigravity)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/.agents/skills"
declare -A DEST=(
  [claude]="$HOME/.claude/skills"
  [codex]="$HOME/.codex/skills"
  [gemini]="$HOME/.gemini/skills"
  [antigravity]="$HOME/.gemini/config/skills"
)
TOOLS=("${@:-claude codex gemini antigravity}")
for tool in ${TOOLS[@]}; do
  dir="${DEST[$tool]:-}"
  if [ -z "$dir" ]; then echo "Unknown tool: $tool (use claude, codex, gemini or antigravity)"; exit 1; fi
  mkdir -p "$dir"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    rm -rf "$dir/$name"
    cp -R "$skill" "$dir/$name"
  done
  echo "✓ $tool → $dir"
done
echo "Done. Restart your AI tool so it picks up the new skills."
