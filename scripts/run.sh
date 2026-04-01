#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$ROOT_DIR/.env" ]]; then
  set -a
  source "$ROOT_DIR/.env"
  set +a
fi

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run.sh --account "Account Name" [--mode all|topic]

Required env:
  WX_AUTH_KEY
  VAULT_PATH

Optional env:
  WX_EXPORTER_BASE (default: http://localhost:3101)
  OUTPUT_SUBDIR (default: 00_Inbox/competitor_analysis)
  TOPIC_REGEX
  DOWNLOAD_RETRIES (default: 1)
  MAX_DOWNLOAD (default: 0, all)
EOF
}

ACCOUNT=""
MODE="${FILTER_MODE:-all}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --account)
      ACCOUNT="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$ACCOUNT" ]]; then
  echo "--account is required" >&2
  usage
  exit 1
fi

if [[ -z "${WX_AUTH_KEY:-}" ]]; then
  echo "Missing WX_AUTH_KEY" >&2
  exit 1
fi

if [[ -z "${VAULT_PATH:-}" ]]; then
  echo "Missing VAULT_PATH" >&2
  exit 1
fi

OUTPUT_SUBDIR="${OUTPUT_SUBDIR:-00_Inbox/competitor_analysis}"
TARGET_ROOT="$VAULT_PATH/$OUTPUT_SUBDIR"
mkdir -p "$TARGET_ROOT"

fetch_args=(
  --account "$ACCOUNT"
  --output-root "$TARGET_ROOT"
  --mode "$MODE"
  --base "${WX_EXPORTER_BASE:-http://localhost:3101}"
  --auth-key "$WX_AUTH_KEY"
)

if [[ -n "${TOPIC_REGEX:-}" ]]; then
  fetch_args+=(--topic-regex "$TOPIC_REGEX")
fi

python3 "$SCRIPT_DIR/fetch_account_articles.py" "${fetch_args[@]}"

ACCOUNT_DIR="$(python3 - <<PY
import json,re
from pathlib import Path
root=Path("$TARGET_ROOT")
dirs=[p for p in root.iterdir() if p.is_dir()]
dirs.sort(key=lambda p:p.stat().st_mtime, reverse=True)
print(dirs[0] if dirs else "")
PY
)"

if [[ -z "$ACCOUNT_DIR" ]]; then
  echo "Could not resolve account output directory" >&2
  exit 1
fi

if [[ "$MODE" == "topic" ]]; then
  URL_FILE="$ACCOUNT_DIR/urls_topic.txt"
  OUT_DIR="$ACCOUNT_DIR/raw_exports_topic"
else
  URL_FILE="$ACCOUNT_DIR/urls_all.txt"
  OUT_DIR="$ACCOUNT_DIR/raw_exports_all"
fi

python3 "$SCRIPT_DIR/download_articles.py" \
  --urls "$URL_FILE" \
  --output "$OUT_DIR" \
  --retries "${DOWNLOAD_RETRIES:-1}" \
  --max-items "${MAX_DOWNLOAD:-0}"

python3 "$SCRIPT_DIR/classify_titles.py" \
  --metadata "$ACCOUNT_DIR/articles-all-metadata.json" \
  --output "$ACCOUNT_DIR/title-classification.md"

echo "done=$ACCOUNT_DIR"
