#!/usr/bin/env python3
import argparse
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

QUERY_MAP = {
    "ai": "AI OR artificial intelligence",
    "cross-border-ec": "cross-border e-commerce OR de minimis OR US tariffs",
    "us-tariffs": "US tariffs OR customs OR de minimis",
}

def parse_args():
    p = argparse.ArgumentParser(description="Fetch a compact market-news digest from Google News RSS")
    p.add_argument("--topic", default="ai", help="ai | cross-border-ec | us-tariffs or custom query")
    p.add_argument("--days", type=int, default=1, help="Lookback window in days")
    p.add_argument("--count", type=int, default=5, help="Max number of items")
    p.add_argument("--hl", default="ja", help="Language code for Google News")
    p.add_argument("--gl", default="JP", help="Country code for Google News")
    p.add_argument("--ceid", default="JP:ja", help="Edition, e.g. JP:ja or US:en")
    return p.parse_args()

def fetch_items(query, hl, gl, ceid):
    url = (
        "https://news.google.com/rss/search?q="
        + urllib.parse.quote(query)
        + f"&hl={hl}&gl={gl}&ceid={ceid}"
    )
    xml = urllib.request.urlopen(url, timeout=20).read()
    root = ET.fromstring(xml)
    return root.findall("./channel/item")

def main():
    args = parse_args()
    query = QUERY_MAP.get(args.topic, args.topic)
    cutoff = datetime.now(timezone.utc) - timedelta(days=max(1, args.days))

    rows = []
    seen = set()
    for item in fetch_items(query, args.hl, args.gl, args.ceid):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        if not title or title in seen:
            continue
        try:
            dt = parsedate_to_datetime(pub)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if dt < cutoff:
            continue
        rows.append((dt, title, link))
        seen.add(title)

    rows.sort(key=lambda x: x[0], reverse=True)
    rows = rows[: max(1, args.count)]

    print(f"# News Digest: {args.topic}")
    print(f"- Query: {query}")
    print(f"- Window: last {max(1, args.days)} day(s)")
    print(f"- Generated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}")
    print()

    if not rows:
        print("No matching items found in this window.")
        return

    for i, (dt, title, link) in enumerate(rows, 1):
        print(f"{i}. **{title}**")
        print(f"   - Date: {dt.strftime('%Y-%m-%d')}")
        print(f"   - Link: {link}")

if __name__ == "__main__":
    main()
