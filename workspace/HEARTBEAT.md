# Heartbeat Tasks

## USD/JPY 変動チェック

毎回のHeartbeatで次を実行する:

```bash
python3 /home/tomoyuki/.openclaw/workspace/scripts/check_usdjpy_heartbeat.py
```

判定ルール:
- 出力が `ALERT:` で始まる場合: その内容をそのままユーザーへ通知する（`HEARTBEAT_OK` は返さない）。
- 出力が `INIT` または `OK:` の場合: 通知不要。`HEARTBEAT_OK` を返す。
- 実行失敗時: エラー要約を1行で通知する。

補足:
- 比較対象は前回取得値（`memory/usdjpy-state.json`）。
- しきい値は前回比 1.0 円以上。
