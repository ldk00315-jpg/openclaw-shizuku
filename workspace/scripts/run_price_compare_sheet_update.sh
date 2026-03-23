#!/usr/bin/env bash
set -euo pipefail

# One-command updater for 価格比較_超厳密 sheet.
# eBay CSV acquisition remains manual; this script automates Sheets sync via API.

WORKSPACE="/home/tomoyuki/.openclaw/workspace"
VENV="$WORKSPACE/.venv_sheets"
PY="$VENV/bin/python"
UPDATER="$WORKSPACE/scripts/update_price_compare_sheet.py"

CSV_DEFAULT="$WORKSPACE/data/price_compare_us_ultra_strict_high_precision_only.csv"
CSV_PATH="${1:-$CSV_DEFAULT}"
SPREADSHEET_ID="${TARGET_SPREADSHEET_ID:-12zYJ5EoCioy6qGe5G9pJ5VrAAzK9uCwEk707EoJM-Fk}"
SHEET_NAME="${TARGET_SHEET_NAME:-価格比較_超厳密}"
CRED_PATH="${GOOGLE_SERVICE_ACCOUNT_JSON:-/home/tomoyuki/.config/gcp/sheets-sa.json}"
LOG_DIR="$WORKSPACE/memory"
LOG_FILE="$LOG_DIR/price-compare-sync.log"

mkdir -p "$LOG_DIR"

if [[ ! -f "$CSV_PATH" ]]; then
  echo "[ERROR] CSV not found: $CSV_PATH" | tee -a "$LOG_FILE"
  exit 2
fi

if [[ ! -f "$CRED_PATH" ]]; then
  echo "[ERROR] Credential not found: $CRED_PATH" | tee -a "$LOG_FILE"
  exit 2
fi

if [[ ! -x "$PY" ]]; then
  echo "[ERROR] Python venv not found: $PY" | tee -a "$LOG_FILE"
  echo "Create venv first: python3 -m venv $VENV && $VENV/bin/pip install google-api-python-client google-auth" | tee -a "$LOG_FILE"
  exit 2
fi

echo "[$(date '+%F %T')] START csv=$CSV_PATH sheet=$SHEET_NAME" | tee -a "$LOG_FILE"

GOOGLE_SERVICE_ACCOUNT_JSON="$CRED_PATH" "$PY" "$UPDATER" \
  --csv "$CSV_PATH" \
  --spreadsheet-id "$SPREADSHEET_ID" \
  --sheet-name "$SHEET_NAME" | tee -a "$LOG_FILE"

echo "[$(date '+%F %T')] DONE" | tee -a "$LOG_FILE"
