#!/usr/bin/env bash
set -euo pipefail

OUT="$(python3 /home/tomoyuki/.openclaw/workspace/scripts/check_usdjpy_heartbeat.py 2>&1 || true)"

if [[ "$OUT" == ALERT:* ]]; then
  openclaw message send --channel telegram --target 8719386273 --message "$OUT"
elif [[ "$OUT" == INIT* ]]; then
  # 初回は通知しない
  :
else
  # OK系や軽微なエラーは通知しない（必要ならここを変更）
  :
fi
