# プロジェクト: eBay価格比較ワークフロー

## 概要
eBayにおける商品の価格比較ワークフローの精度改善と運用効率化。

## 課題と解決策 (2026-03-23)
- **課題**: 既存のUS比較結果でミスマッチが多く（例: パネライ/セイコー）、精度に問題があった。
- **解決策**: 方針を「件数優先」から「精度優先」に変更し、超厳密ルールを適用した再生成を実施。
  - **超厳密ルール**: ブランド一致必須（空ブランドは不採用）、型番トークン（英字+数字、6文字以上）を1つ以上厳密一致、価格比ガード（0.55〜1.8）。

## 生成ファイル
- `data/price_compare_us_ultra_strict.csv`
- `data/price_compare_us_ultra_strict_high_precision_only.csv`
- `data/price_compare_us_ultra_strict_review.csv`

## 運用
- `price_compare_us_ultra_strict_high_precision_only.csv` をGoogle Sheetsにインポート。
- スプレッドシートのタブ名は `価格比較_超厳密` へ改名し、差額順で運用。
- 日常運用は `価格比較_超厳密` を優先し、誤マッチを防ぐ。
- 要確認データは別シート/別ファイルで後追いレビューする。
