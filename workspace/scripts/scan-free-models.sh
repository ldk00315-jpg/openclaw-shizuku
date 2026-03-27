#!/bin/bash
# OpenRouter free model availability checker (read-only, no config changes)
# Usage: bash scan-free-models.sh

# BLACKLIST (do not use as fallback)
# - arcee-ai/trinity-mini:free : quality too low, agents become unusable (2026-03-27)

KEY=$(cat ~/.openclaw/agents/main/agent/auth-profiles.json | python3 -c "
import sys,json
d=json.loads(sys.stdin.read())
for k,v in d.get('profiles',{}).items():
    if 'openrouter' in k.lower() and 'key' in v:
        print(v['key']); break
")

if [ -z "$KEY" ]; then
  echo "ERROR: OpenRouter API key not found"
  exit 1
fi

MODELS=(
  "nvidia/nemotron-3-super-120b-a12b:free"
  "nvidia/nemotron-3-nano-30b-a3b:free"
  "nvidia/nemotron-nano-12b-v2-vl:free"
  "nvidia/nemotron-nano-9b-v2:free"
  "qwen/qwen3-coder:free"
  "qwen/qwen3-next-80b-a3b-instruct:free"
  "qwen/qwen3-4b:free"
  "stepfun/step-3.5-flash:free"
  "minimax/minimax-m2.5:free"
  "arcee-ai/trinity-large-preview:free"
  "openai/gpt-oss-120b:free"
  "openai/gpt-oss-20b:free"
  "z-ai/glm-4.5-air:free"
  "google/gemma-3-27b-it:free"
  "google/gemma-3-12b-it:free"
  "google/gemma-3-4b-it:free"
  "google/gemma-3n-e4b-it:free"
  "google/gemma-3n-e2b-it:free"
  "meta-llama/llama-3.3-70b-instruct:free"
  "meta-llama/llama-3.2-3b-instruct:free"
  "nousresearch/hermes-3-llama-3.1-405b:free"
  "mistralai/mistral-small-3.1-24b-instruct:free"
  "liquid/lfm-2.5-1.2b-thinking:free"
  "liquid/lfm-2.5-1.2b-instruct:free"
  "cognitivecomputations/dolphin-mistral-24b-venice-edition:free"
  "openrouter/free"
)

DATE=$(date +%Y-%m-%d)
echo "=== OpenRouter Free Model Scan: $DATE ==="
echo ""
printf "%-55s %s\n" "MODEL" "STATUS"
echo "----------------------------------------------------------------------"

OK=0
FAIL=0

for model in "${MODELS[@]}"; do
  resp=$(curl -s -m 20 https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"say ok\"}],\"max_tokens\":3}")

  if echo "$resp" | grep -q '"choices"'; then
    printf "%-55s \e[32mOK\e[0m\n" "$model"
    OK=$((OK+1))
  else
    ERR=$(echo "$resp" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('error',{}).get('message','unknown')[:40])" 2>/dev/null || echo "timeout/parse error")
    printf "%-55s \e[31mFAIL\e[0m (%s)\n" "$model" "$ERR"
    FAIL=$((FAIL+1))
  fi
  sleep 1
done

echo ""
echo "=== Summary: $OK OK / $FAIL FAIL / $((OK+FAIL)) total ==="
echo "BLACKLISTED (excluded): arcee-ai/trinity-mini:free"
