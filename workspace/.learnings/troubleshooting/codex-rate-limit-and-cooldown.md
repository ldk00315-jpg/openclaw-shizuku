# Codex OAuth Rate-Limit & Cooldown Cache Bug

## Date: 2026-03-26
## Related: GitHub #23996, #43879, #23516

## 概要
OpenClaw が openai-codex の rate_limit エラーを auth-profiles.json にキャッシュし、
実際の OpenAI 側クォータが回復しても cooldown が残り続けるバグ。

## 症状
- Codex が「残り4日」表示のまま変わらない
- OpenAI ダッシュボードで 100% 残量なのに使えない場合がある
- gateway restart や /reset では解消しない
- フォールバックモデルに落ちたまま戻らない

## 根本原因
1. cooldown 理由が rate_limit にハードコード (#23996)
2. cooldown がプロファイル単位でモデル単位ではない (#43879)
3. gateway 再起動で usageStats がクリアされない (#23516)

## キャッシュされる場所
~/.openclaw/agents/main/agent/auth-profiles.json 内の usageStats:

    openai-codex:default:
      errorCount: 1
      lastFailureReason: rate_limit
      cooldownUntil: 1774517423173

## 復旧手順

### Step 1: usageStats をリセット
/tmp/reset_codex.py として保存して実行:

    import json
    path = '/home/tomoyuki/.openclaw/agents/main/agent/auth-profiles.json'
    with open(path) as f:
        d = json.load(f)
    stats = d.get('usageStats', {})
    for k in list(stats.keys()):
        if 'codex' in k.lower():
            stats[k] = {
                'errorCount': 0,
                'lastFailureReason': None,
                'cooldownUntil': 0
            }
            print('Reset: ' + k)
    with open(path, 'w') as f:
        json.dump(d, f, indent=2)
    print('Done')

### Step 2: gateway 再起動
    openclaw gateway restart

### Step 3: テストメッセージ送信
Telegram でテストメッセージを送り、Web UI でモデル表示が
gpt-5.3-codex / openai-codex になるか確認。

### 判定
- Codex 表示 → OpenAI 側の枠が回復済み、正常運用へ
- フォールバック表示 → OpenAI 側がまだリセットされていない、待機

## OpenAI Codex リミット仕様（非公式、Reddit 情報）
- 5時間リミット（RPM/TPM相当）：短期間の集中利用で発動
- 週間リミット（トークン消費ベース）：大量利用で発動、リセットまで数日
- 公式にリミット値は非公開
- Plus は標準枠、Pro は実質無制限との報告あり
- OpenClaw エージェントはツール呼び出し等で裏で複数 API コールが発生するため、
  見た目以上に枠を消費する

## 注意事項
- 「残りX日」表示は OpenClaw の簡易表示であり正確ではない可能性が高い
- openrouter:manual プロファイルが残っているとルーティングに影響する（Mai で確認済み）
- qwen-portal にも同様の usageStats キャッシュが発生し得る