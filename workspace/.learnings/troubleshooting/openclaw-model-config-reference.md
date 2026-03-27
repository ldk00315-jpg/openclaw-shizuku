# OpenClaw Model Configuration Reference

## Date: 2026-03-26

## 正常時のモデル構成

### Primary
openai-codex/gpt-5.3-codex (OAuth)
- 最高品質、Codex 専用モデル
- 週間リミットあり（非公開、推定トークンベース）
- リミット到達時は fallback に自動切替

### Fallback 順序
1. google/gemini-2.5-flash (Google API 直接、500 req/day 無料)
   - 高品質、安定、レスポンス速い
   - RPM 制限で連続リクエスト時に一時スキップあり
2. openrouter/arcee-ai/trinity-mini:free
   - 軽量モデル、1.4s レイテンシ
   - 品質は低い（エージェントが明らかにアホになる）
   - 2026-03-26 時点でフォールバックから除外済み
3. openrouter/nvidia/nemotron-3-super-120b-a12b:free
   - 120B パラメータ、高品質
   - スタックバグあり（詳細: nemotron-stuck-fallback.md）
4. openrouter/stepfun/step-3.5-flash:free
   - 6s レイテンシ、長コンテキスト対応
5. openrouter/google/gemini-2.5-flash (有料、最終フォールバック)

### 2026-03-26 時点の実運用構成（trinity-mini 除外後）
1. openai-codex/gpt-5.3-codex (primary)
2. google/gemini-2.5-flash (fallback #1)
3. openrouter/nvidia/nemotron-3-super-120b-a12b:free (fallback #2)
4. openrouter/stepfun/step-3.5-flash:free (fallback #3)
5. openrouter/google/gemini-2.5-flash (fallback #4, paid)

## 設定ファイル一覧

### ~/.openclaw/openclaw.json
- agents.defaults.model.primary: プライマリモデル
- agents.defaults.model.fallbacks: フォールバック配列
- agents.defaults.models: 許可モデル一覧（ここに無いとスキップされる）
- auth.profiles: プロバイダ認証設定

### ~/.openclaw/agents/main/agent/auth-profiles.json
- profiles: 各プロバイダの認証情報（api_key, oauth）
- usageStats: 使用状況とクールダウン状態（バグの温床）

### ~/.openclaw/agents/main/agent/models.json
- providers: モデル定義（openrouter, openai-codex, qwen-portal, groq）
- Google プロバイダはここには無く、openclaw.json 側で管理

## モデル品質ランキング（体感）
1. openai-codex/gpt-5.3-codex --- 最高
2. google/gemini-2.5-flash --- 高品質
3. openrouter/nvidia/nemotron-3-super-120b-a12b:free --- 良好（120B）
4. openrouter/stepfun/step-3.5-flash:free --- 普通
5. openrouter/arcee-ai/trinity-mini:free --- 使い物にならない

## 既知の問題
- Codex cooldown cache bug: codex-rate-limit-and-cooldown.md 参照
- Nemotron stuck bug: nemotron-stuck-fallback.md 参照
- Gemini setup issues: google-gemini-fallback-setup.md 参照