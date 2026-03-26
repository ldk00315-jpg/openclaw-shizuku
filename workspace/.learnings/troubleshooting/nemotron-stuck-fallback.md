# Nemotron Stuck Fallback Issue and Recovery

## Date: 2026-03-26

## Symptoms
- Fallback model openrouter/nvidia/nemotron-3-super-120b-a12b:free gets stuck once used
- All subsequent requests stay on nemotron, never returning to higher-priority fallbacks
- gateway restart, /reset, session clear do not fix it

## Root Cause
- Unknown (logs unavailable)
- Possibly OpenClaw caches lastGood model and keeps prioritizing it

## Recovery Steps

### 1. Remove nemotron from fallbacks temporarily
Edit openclaw.json fallbacks to:
- google/gemini-2.5-flash
- openrouter/arcee-ai/trinity-mini:free
- openrouter/stepfun/step-3.5-flash:free
- openrouter/google/gemini-2.5-flash

Then: openclaw gateway restart

### 2. Verify
- Send test message via Telegram
- Web UI should show gemini-2.5-flash google

### 3. Restore nemotron after recovery
Edit openclaw.json fallbacks to:
- google/gemini-2.5-flash
- openrouter/arcee-ai/trinity-mini:free
- openrouter/nvidia/nemotron-3-super-120b-a12b:free
- openrouter/stepfun/step-3.5-flash:free
- openrouter/google/gemini-2.5-flash

Then: openclaw gateway restart

## Normal Model Config
- Primary: openai-codex/gpt-5.3-codex
- Fallback order:
  1. google/gemini-2.5-flash - Google API direct, 500 req/day free
  2. openrouter/arcee-ai/trinity-mini:free - 1.4s, fastest free
  3. openrouter/nvidia/nemotron-3-super-120b-a12b:free - 120B, high quality
  4. openrouter/stepfun/step-3.5-flash:free - 6s, long context
  5. openrouter/google/gemini-2.5-flash - paid, last resort

## Notes
- Both openclaw.json models section and auth-profiles.json must have model entries
- Mai env needed manual addition of google:default to auth-profiles.json
- openrouter:manual profile caused issues on Mai (removed)
