#!/usr/bin/env python3
import json
import os
import urllib.request
from datetime import datetime

OUT_PATH = "/home/tomoyuki/.openclaw/workspace/memory/today-indicators.json"


def load_previous():
    if not os.path.exists(OUT_PATH):
        return {}
    try:
        with open(OUT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def fetch_json(url, ua="openclaw-indicator-bot"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_text(url, ua="openclaw-indicator-bot"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def fetch_usdjpy():
    data = fetch_json("https://open.er-api.com/v6/latest/USD")
    return float(data["rates"]["JPY"])


def fetch_stooq_close(symbol):
    # Example: ^dji -> %5Edji
    url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlcv&h&e=json"
    try:
        data = fetch_json(url)
        quotes = data.get("symbols", [])
        if not quotes:
            return None
        q = quotes[0]
        close = q.get("close")
        if close in (None, "N/D"):
            return None
        return float(close)
    except Exception:
        # stooq occasionally returns invalid JSON (e.g., volume empty). Fallback to text parse.
        raw = fetch_text(url)
        marker = '"close":'
        idx = raw.find(marker)
        if idx == -1:
            return None
        tail = raw[idx + len(marker):]
        num = []
        for ch in tail:
            if ch.isdigit() or ch in '.-':
                num.append(ch)
            else:
                break
        if not num:
            return None
        try:
            return float(''.join(num))
        except Exception:
            return None


def fetch_weather_komagane():
    data = fetch_json("https://wttr.in/Komagane?format=j1")
    weather = (data.get("weather") or [{}])[0]
    return {
        "maxTempC": weather.get("maxtempC"),
        "minTempC": weather.get("mintempC"),
        "summary": ((weather.get("hourly") or [{}])[4].get("weatherDesc") or [{"value": ""}])[0].get("value", ""),
    }


def pct_change(cur, prev):
    if cur is None or prev in (None, 0):
        return None
    try:
        return (float(cur) - float(prev)) / float(prev) * 100.0
    except Exception:
        return None


def diff(cur, prev):
    if cur is None or prev is None:
        return None
    try:
        return float(cur) - float(prev)
    except Exception:
        return None


def main():
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    prev = load_previous()

    snapshot = {
        "updatedAt": now,
        "fx": {},
        "indices": {},
        "commodities": {},
        "weather": {},
        "changes": {
            "indicesPct": {},
            "weatherDiff": {}
        },
        "errors": [],
    }

    # USD/JPY
    try:
        snapshot["fx"]["USDJPY"] = fetch_usdjpy()
    except Exception as e:
        snapshot["errors"].append(f"USDJPY: {e}")

    # Global/JP indices (Stooq symbols)
    symbol_map = {
        "Dow": "^dji",
        "NASDAQ": "^ndq",
        "SP500": "^spx",
        "Nikkei225": "^nkx",
        "TOPIX": "^tpx",
    }
    for name, sym in symbol_map.items():
        try:
            snapshot["indices"][name] = fetch_stooq_close(sym)
        except Exception as e:
            snapshot["indices"][name] = None
            snapshot["errors"].append(f"{name}: {e}")

    # WTI crude (front month proxy)
    try:
        snapshot["commodities"]["WTI"] = fetch_stooq_close("cl.f")
    except Exception as e:
        snapshot["commodities"]["WTI"] = None
        snapshot["errors"].append(f"WTI: {e}")

    # Weather
    try:
        snapshot["weather"]["Komagane"] = fetch_weather_komagane()
    except Exception as e:
        snapshot["weather"]["Komagane"] = {}
        snapshot["errors"].append(f"Weather: {e}")

    # changes: indices in %, weather in absolute temp difference (C)
    prev_indices = (prev.get("indices") or {}) if isinstance(prev, dict) else {}
    for k, v in snapshot["indices"].items():
        snapshot["changes"]["indicesPct"][k] = pct_change(v, prev_indices.get(k))

    prev_w = ((prev.get("weather") or {}).get("Komagane") or {}) if isinstance(prev, dict) else {}
    cur_w = snapshot["weather"].get("Komagane", {})
    snapshot["changes"]["weatherDiff"]["KomaganeMaxTempC"] = diff(cur_w.get("maxTempC"), prev_w.get("maxTempC"))
    snapshot["changes"]["weatherDiff"]["KomaganeMinTempC"] = diff(cur_w.get("minTempC"), prev_w.get("minTempC"))

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    print(f"OK updated {OUT_PATH} at {now}")
    if snapshot["errors"]:
        print("WARN", " | ".join(snapshot["errors"]))


if __name__ == "__main__":
    main()
