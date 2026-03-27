# Nemotron Stuck Fallback Issue and Recovery

## Date: 2026-03-26 (updated)

## 概要
openrouter/nvidia/nemotron-3-super-120b-a12b:free が一度使われると、
以降すべてのリクエストが nemotron に固定され、上位フォールバックに戻らなくなるバグ。

## 症状
- Web UI のモデル表示が nemotron-3-super のまま変わらない
- gateway restart しても解消しない
- /reset やセッションクリアでも解消しない
- google/gemini-2.5-flash が fallback #1 に設定されていてもスキップされる

## 推定原因
OpenClaw が最初に成功したフォールバックモデルを lastGood としてキャッシュし、
以降のリクエストでそのモデルを優先的に使い続ける。
根本原因は未特定（2026-03-26 時点）。

## 発見の経緯
trinity-mini をフォールバックから除外した際に nemotron が使われ始め、
以降 Gemini に戻らなくなった。nemotron を一時除外したところ
即座に Gemini が使われるようになり、スタックが原因と判明。
（ユーザーの障害切り分け提案により特定）

## 復旧手順

### Step 1: nemotron を一時的にフォールバックから除外
以下の内容を /tmp/remove_nemotron.py として保存して実行:

    import json
    path = '/home/tomoyuki/.openclaw/openclaw.json'
    with open(path) as f:
        cfg = json.load(f)
    fb = cfg['agents']['defaults']['model']['fallbacks']
    fb_new = [m for m in fb if 'nemotron' not in m]
    cfg['agents']['defaults']['model']['fallbacks'] = fb_new
    with open(path, 'w') as f:
        json.dump(cfg, f, indent=2)
    print('Removed nemotron. New fallbacks:')
    for m in fb_new:
        print('  ' + m)

### Step 2: gateway 再起動
    openclaw gateway restart

### Step 3: 動作確認
Telegram でテストメッセージを送信。
Web UI で gemini-2.5-flash / google と表示されることを確認。

### Step 4: nemotron を復元
以下の内容を /tmp/restore_nemotron.py として保存して実行:

    import json
    path = '/home/tomoyuki/.openclaw/openclaw.json'
    with open(path) as f:
        cfg = json.load(f)
    cfg['agents']['defaults']['model']['fallbacks'] = [
        'google/gemini-2.5-flash',
        'openrouter/nvidia/nemotron-3-super-120b-a12b:free',
        'openrouter/stepfun/step-3.5-flash:free',
        'openrouter/google/gemini-2.5-flash'
    ]
    with open(path, 'w') as f:
        json.dump(cfg, f, indent=2)
    print('Restored nemotron in fallbacks')

その後 openclaw gateway restart を実行。

## 注意
- nemotron 自体の品質は高い（120B パラメータ）
- 問題はモデルではなく OpenClaw のフォールバック固定バグ
- 再発時は同じ手順で復旧可能
- 詳細な構成情報: openclaw-model-config-reference.md 参照