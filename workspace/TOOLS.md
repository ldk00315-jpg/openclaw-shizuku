# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## OpenClaw 安定運用プリセット（低スペックPC向け）

### 症状
- Browser操作中に `timed out` が出る
- NotebookLM など重いWebアプリで接続が切れやすい

### 基本方針
- 生成開始まで自動、長い待機は手動確認
- 同時操作を減らす（並列操作しすぎない）
- 作業前に Browser/Gateway を再起動してクリーン状態にする

### クイック復旧コマンド
```bash
/home/tomoyuki/.openclaw/workspace/scripts/recover_browser_session.sh
```

### 作業前チェック（毎回）
1. 不要タブを閉じる
2. Browser/Gatewayを再起動
3. 重い画面（NotebookLM生成など）は完了待ちを人手に切り替える

### 実運用ルール
- 1ターンでのブラウザ操作は短く区切る
- `wait` を多用しすぎない（短い操作→状態確認→次の操作）
- 失敗時は2回目のリトライ前に復旧スクリプトを実行
