#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Restarting OpenClaw gateway..."
openclaw gateway restart >/tmp/openclaw-gateway-restart.log 2>&1 || true

sleep 2

echo "[2/3] Restarting OpenClaw browser driver..."
openclaw browser stop >/tmp/openclaw-browser-stop.log 2>&1 || true
sleep 1
openclaw browser start >/tmp/openclaw-browser-start.log 2>&1 || true

sleep 2

echo "[3/3] Browser status"
openclaw browser status || true

echo "Done. If browser tool still times out, close heavy tabs and retry once."
