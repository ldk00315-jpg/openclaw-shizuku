# ERRORS

## [ERR-20260327-001] agentmail_mark_read_route_missing

**Logged**: 2026-03-27T08:32:20.077592+00:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
AgentMail SDKの`messages.update(... remove_labels=['unread'])`で既読化を試みたが、APIが404 Route not foundを返して失敗した。

### Error
```
agentmail.errors.not_found_error.NotFoundError: status_code: 404, body: name='NotFoundError' message='Route not found'
```

### Context
- Operation: 受信メールの既読化
- Command: `client.inboxes.messages.update(inbox_id=..., message_id=..., remove_labels=['unread'])`
- Environment: AgentMail Python SDK（installed）

### Suggested Fix
- SDKバージョンとAPI互換性を確認する
- 既読化APIが未提供なら、UI/別エンドポイントでの既読処理可否を確認する

### Metadata
- Reproducible: yes
- Related Files: skills/agentmail/scripts/check_inbox.py

---

