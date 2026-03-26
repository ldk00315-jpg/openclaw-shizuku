# プロジェクト: USD/JPY変動アラート

## 概要
USD/JPYが前回と比較して1円以上変動した場合にアラートを発信する。

## 実装
- `check_usdjpy_heartbeat.py` を使用してHeartbeatで監視。
- `check_usdjpy_notify.sh` を使用して通知。
- 毎時実行。

## 関連ファイル
- `check_usdjpy_heartbeat.py`
- `check_usdjpy_notify.sh`
