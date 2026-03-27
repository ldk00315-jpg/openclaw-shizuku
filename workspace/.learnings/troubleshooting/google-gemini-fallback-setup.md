# Google Gemini Fallback Setup Issues

## Date: 2026-03-26

## 概要
Mai 環境で google/gemini-2.5-flash がフォールバックとしてスキップされ、
低品質の trinity-mini や nemotron にフォールバックし続けた問題と解決手順。

## 症状
- openclaw.json の fallbacks に google/gemini-2.5-flash を設定済みなのにスキップされる
- Web UI でモデルが nemotron-3-super や trinity-mini と表示される
- Shizuku では正常に Gemini が使えるのに Mai では使えない

## 原因（3つの複合）

### 1. auth-profiles.json に google:default が未登録
Shizuku には google:default (type: api_key) が存在したが、
Mai には存在しなかった。手動で追加して解決。

確認コマンド:
    cat ~/.openclaw/agents/main/agent/auth-profiles.json | python3 -c "
    import sys,json
    d=json.loads(sys.stdin.read())
    for k,v in d.get('profiles',{}).items():
        if 'google' in k.lower():
            print(k,':',{kk:str(vv)[:30] for kk,vv in v.items()})
    "

### 2. models の allowed リストに未登録
openclaw.json の agents.defaults.models に google/gemini-2.5-flash が
含まれていなかったため、fallbacks に書いてもスキップされた。

確認コマンド:
    cat ~/.openclaw/openclaw.json | python3 -c "
    import sys,json
    cfg=json.loads(sys.stdin.read())
    models=cfg.get('agents',{}).get('defaults',{}).get('models',{})
    print('google/gemini-2.5-flash in allowed:', 'google/gemini-2.5-flash' in models)
    "

### 3. openrouter:manual プロファイルの干渉
Mai に openrouter:manual (mode: token) と order 設定が残っており、
ルーティングに影響していた可能性。削除して解決。

## 正常時の構成チェックリスト
- [ ] openclaw.json の auth.profiles に google:default が存在する
- [ ] auth-profiles.json に google:default (type: api_key) が存在する
- [ ] GEMINI_API_KEY が openclaw.json 内に記載されている
- [ ] openclaw.json の models に google/gemini-2.5-flash が含まれている
- [ ] fallbacks の先頭が google/gemini-2.5-flash になっている
- [ ] openrouter:manual や不要な order 設定が残っていない

## Google Gemini 2.5 Flash 無料枠
- 500 requests/day (RPD)
- RPM 制限あり（連続リクエストで一時的にスキップされる場合がある）
- 有料版は openrouter/google/gemini-2.5-flash として fallback 末尾に配置

## 教訓
- 設定ファイルが複数箇所（openclaw.json, auth-profiles.json, models.json）に
  分散しているため、1箇所だけ修正しても動かないケースがある
- Shizuku と Mai で設定を揃える際は全ファイルを比較する必要がある