---
name: openclaw-browser-stability
description: Recover unstable OpenClaw browser/CDP sessions on low-spec PCs and continue automation safely. Use when browser tool times out, NotebookLM/heavy web apps disconnect, or repeated reconnect/restart is needed before continuing browser tasks.
---

# OpenClaw Browser Stability

Use this skill when browser automation becomes flaky (timeouts, CDP drops, long-running page generation).

## Quick Recovery

Run:

```bash
/home/tomoyuki/.openclaw/workspace/scripts/recover_browser_session.sh
```

Then verify:

```bash
openclaw gateway status
```

## Operating Rules (Low-Spec PCs)

1. Keep tabs minimal before heavy automation.
2. Split long browser jobs into short steps.
3. Start generation automatically, but hand off long waiting to manual confirmation.
4. After one timeout, run recovery before retrying.

## Suggested Flow for Heavy Apps (NotebookLM etc.)

1. Open page and trigger generation.
2. Avoid long `wait` loops in automation.
3. Ask user to confirm completion if generation takes long.
4. Resume extraction/download after completion signal.

## What this skill does not do

- It does not bypass login/captcha/2FA.
- It does not guarantee stability under sustained high load; it provides best-effort recovery and safer operation pattern.
