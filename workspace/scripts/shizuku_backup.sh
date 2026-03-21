#!/usr/bin/env bash
set -euo pipefail

SRC_WORKSPACE="/home/tomoyuki/.openclaw/workspace"
BACKUP_REPO="/home/tomoyuki/openclaw-shizuku-backup"
STAMP="$(date '+%Y-%m-%d %H:%M:%S %Z')"

mkdir -p "$BACKUP_REPO"

if [ ! -d "$BACKUP_REPO/.git" ]; then
  git -C "$BACKUP_REPO" init -b main
  git -C "$BACKUP_REPO" config user.name "Shizuku Backup Bot"
  git -C "$BACKUP_REPO" config user.email "shizuku-backup@local"
fi

# sync workspace (exclude volatile/internal git)
rsync -a --delete \
  --exclude '.git/' \
  --exclude 'dist/' \
  --exclude 'node_modules/' \
  --exclude '.DS_Store' \
  "$SRC_WORKSPACE/" "$BACKUP_REPO/workspace/"

# small runtime metadata (non-secret)
mkdir -p "$BACKUP_REPO/runtime"
{
  echo "backup_at=$STAMP"
  echo "host=$(hostname)"
  echo "openclaw_version=$(openclaw --version 2>/dev/null || true)"
} > "$BACKUP_REPO/runtime/backup-meta.txt"

# optional: capture cron jobs text for recovery
crontab -l > "$BACKUP_REPO/runtime/user-crontab.txt" 2>/dev/null || true

# commit only when changed
if ! git -C "$BACKUP_REPO" diff --quiet --ignore-submodules -- . || [ -n "$(git -C "$BACKUP_REPO" ls-files --others --exclude-standard)" ]; then
  git -C "$BACKUP_REPO" add -A
  git -C "$BACKUP_REPO" commit -m "backup: $STAMP"
fi

# push if remote exists
if git -C "$BACKUP_REPO" remote get-url origin >/dev/null 2>&1; then
  git -C "$BACKUP_REPO" push -u origin main
else
  echo "INFO: origin remote is not set. Skipping push."
fi
