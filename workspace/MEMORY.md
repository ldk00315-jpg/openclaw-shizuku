# MEMORY.md - インデックス

## 人物一覧

- **山吹しずく（やまぶき しずく）**: このAIアシスタント。詳細: `IDENTITY.md`

## プロジェクト一覧

- **今日の指標提供**: `memory/projects/today-indicators.md`
- **USD/JPY変動アラート**: `memory/projects/usdjpy-alert.md`
- **自動バックアップシステム**: `memory/projects/backup-system.md`
- **eBay価格比較ワークフロー**: `memory/projects/ebay-price-compare.md`
- **API連携デバッグと検証**: `memory/projects/api-integration-debugging.md`
- **eBay海外市場調査**: `memory/projects/ebay-market-research.md`
- **eBay Research Tool スキル**: `memory/projects/ebay-research-tool-skill.md`
- **Claude Code インストールと検証**: `memory/projects/claude-code-installation.md`

## 決定事項一覧

- **2026年3月**: `memory/decisions/2026-03.md`

## Active Context

## ドリルダウンルール

- **MEMORY.mdの利用**: メインセッションでのみロードし、共有環境ではロードしない。
- **記述の徹底**: 「覚えておいて」と言われたことは必ずファイルに書き出す。
- **インデックスの同時更新**: 詳細ファイルを更新したら、必ず`MEMORY.md`のインデックスも同時に更新する。
- **MEMORY.mdのサイズ**: `MEMORY.md`は3kトークン以下を維持する。
- **Active Contextの制限**: `Active Context`は最大2〜3ファイルに留める。
- **セッション開始時のドリルダウン**: 最大5ファイルまでとする。
- **定期的なメンテナンス**: 定期的にデイリーログをレビューし、`MEMORY.md`に重要な学びを抽出し、古い情報は削除する。
