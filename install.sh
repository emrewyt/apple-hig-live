#!/usr/bin/env bash
# Install apple-hig-live for Claude Code, Codex, Antigravity 2.0, Gemini CLI, Cursor.
# Usage: ./install.sh [claude|codex|antigravity|gemini|cursor|all] [user|project]
set -euo pipefail

TARGET="${1:-all}"
SCOPE="${2:-user}"
SRC="$(cd "$(dirname "$0")" && pwd)/skills/apple-hig-live"
[ -d "$SRC" ] || { echo "skill folder not found: $SRC" >&2; exit 1; }

dest_for() {
  if [ "$SCOPE" = "project" ]; then
    case "$1" in
      claude) echo ".claude/skills" ;;
      codex) echo ".codex/skills" ;;
      antigravity) echo ".agents/skills" ;;
      gemini) echo ".gemini/skills" ;;
      cursor) echo ".cursor/skills" ;;
    esac
  else
    case "$1" in
      claude) echo "$HOME/.claude/skills" ;;
      codex) echo "$HOME/.codex/skills" ;;
      antigravity) echo "$HOME/.gemini/config/skills" ;;
      gemini) echo "$HOME/.gemini/skills" ;;
      cursor) echo "$HOME/.cursor/skills" ;;
    esac
  fi
}

install_one() {
  local dest; dest="$(dest_for "$1")"
  mkdir -p "$dest"
  rm -rf "$dest/apple-hig-live"
  cp -r "$SRC" "$dest/apple-hig-live"
  echo "[OK] Installed apple-hig-live for $1 -> $dest/apple-hig-live"
}

case "$TARGET" in
  claude|codex|antigravity|gemini|cursor) install_one "$TARGET" ;;
  all) for t in claude codex antigravity gemini; do install_one "$t"; done ;;
  *) echo "usage: $0 [claude|codex|antigravity|gemini|cursor|all] [user|project]" >&2; exit 1 ;;
esac
