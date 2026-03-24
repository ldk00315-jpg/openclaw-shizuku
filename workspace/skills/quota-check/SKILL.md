---
name: quota-check
description: Check remaining API quota and rate limit status for all configured LLM providers (Groq, Mistral, Google Gemini, OpenRouter, OpenAI Codex, Qwen Portal)
user-invocable: true
---

# API Quota Check

Run the quota check script and relay the results to the user.

## Instructions

1. Run the following command:
   ```bash
   python3 ~/.openclaw/workspace/skills/quota-check/check_quota.py
   ```

2. Present the output to the user as-is. The script formats the results clearly.

3. If any provider shows "RATE LIMITED", note when it will reset if the reset time is available.

4. If any provider shows "AUTH ERROR", suggest the user check their API key configuration.
