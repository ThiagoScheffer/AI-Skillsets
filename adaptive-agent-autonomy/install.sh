#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${AGENT_SKILLS_DIR:-$HOME/.agents/skills}/adaptive-agent-autonomy"
ENSURE_SUPERPOWERS=0
for arg in "$@"; do
  case "$arg" in
    --ensure-superpowers) ENSURE_SUPERPOWERS=1 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
echo "Installed adaptive-agent-autonomy to $DEST"
if [[ "$ENSURE_SUPERPOWERS" == "1" ]]; then
  python "$DEST/scripts/ensure_superpowers.py" --install
else
  python "$DEST/scripts/ensure_superpowers.py" || true
  echo "Use '$DEST/install.sh --ensure-superpowers' or run ensure_superpowers.py --install to add it if missing."
fi
