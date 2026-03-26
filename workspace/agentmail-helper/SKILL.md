---
name: agentmail-helper
description: AgentMailのメールボックス作成、表示名更新、メール送受信、受信メール確認をサポートするスキルだよ！これを使えばAgentMailの操作がスムーズにできるはず！
---

# AgentMail Helper

このスキルは、AgentMailの基本的な操作をアシストするよ。
メールボックスの作成から、メールの送受信、受信メールの確認まで、必要なPythonスクリプトがまとまっているから、AgentMailをもっと便利に使えるはず！

## 使い方

AgentMailの機能を使うには、事前に`AGENTMAIL_API_KEY`を環境変数に設定しておく必要があるよ。「am_us_...」みたいなキーだよ。

### 1. メールボックスを作成する

メールアドレスはランダムに生成されるけど、`agent-shizuku`みたいに特定の表示名にしたい場合は、その後の「表示名を更新する」手順で見つけやすくできるよ。

```python
import os
from agentmail import AgentMail

api_key = os.getenv("AGENTMAIL_API_KEY")
if not api_key:
    raise ValueError("AGENTMAIL_API_KEY environment variable not set")

client = AgentMail(api_key=api_key)

try:
    inbox = client.inboxes.create()
    print(f"Created inbox: {inbox.inbox_id} with display_name: {inbox.display_name}")
except Exception as e:
    print(f"Error creating inbox: {e}")
```

### 2. メールボックスの表示名を更新する

メールボックスの表示名を、よりわかりやすいものに変更するよ。メールアドレス自体は変わらないことに注意してね。

#### 例：`grumpybear493@agentmail.to` の表示名を `agent-shizuku` に変更

```python
import os
from agentmail import AgentMail

api_key = os.getenv("AGENTMAIL_API_KEY")
if not api_key:
    raise ValueError("AGENTMAIL_API_KEY environment variable not set")

client = AgentMail(api_key=api_key)

inbox_id_to_update = "grumpybear493@agentmail.to" # ここを更新したいメールボックスのIDに変えてね！
new_display_name = "agent-shizuku" # ここを好きな表示名に変えてね！

try:
    updated_inbox = client.inboxes.update(
        inbox_id=inbox_id_to_update,
        display_name=new_display_name
    )
    print(f"Updated inbox display name: {updated_inbox.inbox_id} with display_name: {updated_inbox.display_name}")
except Exception as e:
    print(f"Error updating inbox: {e}")
```

### 3. メールを送信する

作成したメールボックスからメールを送る方法だよ。

```python
import os
from agentmail import AgentMail

api_key = os.getenv("AGENTMAIL_API_KEY")
if not api_key:
    raise ValueError("AGENTMAIL_API_KEY environment variable not set")

client = AgentMail(api_key=api_key)

inbox_id = "grumpybear493@agentmail.to" # 自分のメールボックスのIDに変えてね！
to_email = "recipient@example.com" # 送りたい相手のメールアドレスに変えてね！
subject = "Hi from AgentMail!" # 件名
body_text = "Hello there! This is a test email from AgentMail." # 本文

try:
    client.inboxes.messages.send(
        inbox_id=inbox_id,
        to=to_email,
        subject=subject,
        text=body_text
    )
    print(f"Email sent from {inbox_id} to {to_email} with subject \\"{subject}\\"")
except Exception as e:
    print(f"Error sending email: {e}")
```

### 4. 受信メールを確認する

メールボックスに届いた最新のメールを確認する方法だよ。

```python
import os
from agentmail import AgentMail

api_key = os.getenv("AGENTMAIL_API_KEY")
if not api_key:\
    raise ValueError("AGENTMAIL_API_KEY environment variable not set")

client = AgentMail(api_key=api_key)

inbox_id = "grumpybear493@agentmail.to" # 自分のメールボックスのIDに変えてね！

try:
    messages_response = client.inboxes.messages.list(inbox_id=inbox_id, limit=1)
    if messages_response.messages:
        latest_message = messages_response.messages[0]
        # 本文はpreview属性から取得するよ
        message_body = latest_message.preview if hasattr(latest_message, 'preview') and latest_message.preview is not None else ""

        print(f"Latest message from: {latest_message.from_}\nSubject: {latest_message.subject}\nBody: {message_body[:200]}...") # 本文が長すぎる場合は、200文字で省略するよ！
    else:
        print("No new messages in the inbox.")
except Exception as e:
    print(f"Error listing messages: {e}")
```
