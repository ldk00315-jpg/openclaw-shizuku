# プロジェクト: 今日の指標提供

## 概要
ユーザーからの「今日の指標 / 指標教えて」というリクエストに対し、USDJPY、主要指数(ダウ/NASDAQ/SP500/日経225/TOPIX)、WTI、駒ヶ根天気(最高/最低)の最新データを提供。

## 実装
- `scripts/collect_today_indicators.py` を使用してデータを収集。
- データは `memory/today-indicators.json` にキャッシュされる。
- 1時間ごと (`cron` 毎時10分) に更新。

## 関連ファイル
- `scripts/collect_today_indicators.py`
- `memory/today-indicators.json`
