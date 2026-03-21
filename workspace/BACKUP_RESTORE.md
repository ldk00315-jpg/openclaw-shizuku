# Shizuku Backup / Restore Guide

## Backup target
- Local backup repo: `/home/tomoyuki/openclaw-shizuku-backup`
- Source: `/home/tomoyuki/.openclaw/workspace`

## Automatic schedule
- Daily at 03:30 JST (user crontab)
- Command:
  - `/home/tomoyuki/.openclaw/workspace/scripts/shizuku_backup.sh`

## One-time GitHub setup
1. Create a private GitHub repo: `openclaw-shizuku`.
2. Set remote:
   ```bash
   git -C /home/tomoyuki/openclaw-shizuku-backup remote add origin <YOUR_REPO_URL>
   ```
3. First push:
   ```bash
   /home/tomoyuki/.openclaw/workspace/scripts/shizuku_backup.sh
   ```

## Manual backup now
```bash
/home/tomoyuki/.openclaw/workspace/scripts/shizuku_backup.sh
```

## Restore
```bash
rsync -a --delete /home/tomoyuki/openclaw-shizuku-backup/workspace/ /home/tomoyuki/.openclaw/workspace/
```

## Notes
- Secrets/credentials are intentionally excluded by backing up workspace only.
- `runtime/user-crontab.txt` is included as reference for recovery.
