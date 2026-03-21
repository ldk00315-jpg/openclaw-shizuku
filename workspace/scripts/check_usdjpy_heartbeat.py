#!/usr/bin/env python3
import json
import os
import urllib.request
from datetime import datetime

STATE_PATH = "/home/tomoyuki/.openclaw/workspace/memory/usdjpy-state.json"
URL = "https://open.er-api.com/v6/latest/USD"
THRESHOLD = 1.0


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def fetch_rate():
    req = urllib.request.Request(URL, headers={"User-Agent": "openclaw-heartbeat"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    if data.get("result") not in ("success", None):
        raise RuntimeError(f"rate api error: {data.get('result')}")
    return float(data["rates"]["JPY"])


def main():
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    state = load_state()
    prev = state.get("lastRate")

    current = fetch_rate()
    out = {
        "lastRate": current,
        "lastCheckedAt": now,
    }
    save_state(out)

    if prev is None:
        print(f"INIT USD/JPY {current:.3f} ({now})")
        return

    diff = current - float(prev)
    abs_diff = abs(diff)

    if abs_diff >= THRESHOLD:
        direction = "上昇" if diff > 0 else "下落"
        print(
            f"ALERT: USD/JPYが前回比{abs_diff:.3f}円{direction}しました。"
            f" 前回 {float(prev):.3f} → 現在 {current:.3f}（{now}）"
        )
    else:
        print(
            f"OK: USD/JPY {current:.3f}（前回 {float(prev):.3f}, 差分 {diff:+.3f}円）"
        )


if __name__ == "__main__":
    main()
