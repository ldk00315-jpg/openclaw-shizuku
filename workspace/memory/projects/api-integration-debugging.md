# プロジェクト: API連携デバッグと検証

## 概要
OpenRouter APIキーの問題調査と、Gemini 2.5 Flash Liteの機能確認。

## OpenRouter API Key Issue Debugging (2026-03-24)
- **問題**: OpenRouter APIキーは当初動作したが、Gateway経由で401 "User not found"エラーを返すようになった。直接APIコールではキーは有効である。
- **調査結果**: 
  - `~/.openclaw/agents/main/agent/auth-profiles.json` に有効な `openrouter:default` エントリを確認。
  - `openclaw.json` のフォールバック設定を更新したが、Gatewayが変更を認識していない可能性。
  - Gatewayの認証キャッシュ問題、またはプロファイル読み込みの不具合が疑われた。
  - `openclaw secrets reload` を実行したが効果なし。GatewayログにもOpenRouter API呼び出しの痕跡なし。
- **現在の状況**: OpenRouter APIは認証エラーのためGateway経由では使用不可。GatewayがOpenRouterクレデンシャルを正しく読み込めない根本原因は不明だが、キャッシングまたは内部Gateway認証処理に関連していると疑われる。

## Gemini 2.5 Flash Lite Confirmation (2026-03-24)
- **テスト結果**: `google/gemini-2.5-flash-lite` がフォールバックモデルとして機能することを確認。`sessions_spawn` タスクが正常に実行され、応答を生成した。

## 現在のフォールバックモデル
- `qwen-portal/coder-model` (OAuth経由で動作中)
- `google/gemini-2.5-flash-lite` (APIキー経由で動作中)
