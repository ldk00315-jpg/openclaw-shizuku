# プロジェクト: Claude Code インストールと検証

## 概要
Claude CodeのLinux版をインストールし、基本的な動作検証を行う。

## 目的
AIエージェントのコーディングタスクにClaude Codeを導入するため。

## 経緯
- とんすけからの指示により、Claude CodeのLinux版インストールを開始。

## 実施内容
- 推奨インストールスクリプト `curl -fsSL https://claude.ai/install.sh | bash` を実行。
- Claude Code のバージョン `2.1.83` が `~/.local/bin/claude` に配置されたことを確認。
- `claude --version` コマンドでバージョン情報 `2.1.83 (Claude Code)` の取得に成功。
- `claude doctor` コマンドを実行したが、`ERROR Raw mode is not supported on the current process.stdin` エラーにより環境チェックを断念。ヘッドレス環境でのインタラクティブな入出力に起因する問題と判断。
- `claude --print \"...\"` を試したが、`Not logged in · Please run /login` エラーによりAnthropicアカウントでのログインが必要であることを確認。
