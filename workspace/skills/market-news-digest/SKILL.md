---
name: market-news-digest
description: Build concise market-news digests (typically top 5) from Google News RSS for topics like AI, cross-border e-commerce, and US tariffs/de minimis. Use when a user asks for recent headlines, time-bounded picks (e.g., last 7/10/30 days), or a quick briefing with title/date/link output in Japanese or English.
---

# Market News Digest

Create short, reliable headline digests with clear time windows and low noise.

## Workflow

1. Clarify scope: topic, window (days), count, language/region.
2. Run `scripts/fetch_digest.py` with matching parameters.
3. Return top items with:
   - title
   - date
   - link
   - one-line relevance note (optional)
4. If results are fewer than requested, say so explicitly and suggest widening window/scope.

## Quick Commands

```bash
# AI, last 1 day, top 5 (JP)
python3 scripts/fetch_digest.py --topic ai --days 1 --count 5

# Cross-border EC + de minimis/tariffs, last 10 days (US)
python3 scripts/fetch_digest.py --topic cross-border-ec --days 10 --count 5 --hl en --gl US --ceid US:en

# Custom query
python3 scripts/fetch_digest.py --topic "US customs de minimis Shein Temu" --days 14 --count 5 --hl en --gl US --ceid US:en
```

## Output Rules

- Prefer recent and directly relevant items over generic macro news.
- Avoid pretending there are 5 items if the window is narrow.
- If links are Google redirect links, still return them (fastest stable source).
- Keep response compact; bullets are preferred over tables for chat apps.
