#!/usr/bin/env python3
"""
Update Google Sheets tab from CSV (price compare workflow).

Purpose:
- Replace manual Google Sheets UI operations with API calls.
- Clear/create target sheet, upload CSV, sort by diff_abs desc,
  and apply number formats.

Required env:
- GOOGLE_SERVICE_ACCOUNT_JSON: path to service-account json
  (shared to target spreadsheet)
Optional env:
- TARGET_SPREADSHEET_ID (default: saved_sellers)
- TARGET_SHEET_NAME (default: 価格比較_超厳密)
- SORT_COLUMN_NAME (default: diff_abs)
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import List

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DEFAULT_SPREADSHEET_ID = "12zYJ5EoCioy6qGe5G9pJ5VrAAzK9uCwEk707EoJM-Fk"
DEFAULT_SHEET_NAME = "価格比較_超厳密"


def col_to_a1(col_idx_0: int) -> str:
    n = col_idx_0 + 1
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def read_csv(path: str) -> List[List[str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return [row for row in csv.reader(f)]


def ensure_sheet(service, spreadsheet_id: str, sheet_name: str) -> int:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for s in meta.get("sheets", []):
        props = s.get("properties", {})
        if props.get("title") == sheet_name:
            return props["sheetId"]

    req = {"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]}
    res = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=req)
        .execute()
    )
    return res["replies"][0]["addSheet"]["properties"]["sheetId"]


def _add_link_columns(values: List[List[str]]) -> List[List[str]]:
    if not values:
        return values

    header = values[0]
    idx = {h: i for i, h in enumerate(header)}

    if not {"item_id_my", "my_title", "item_id_rival", "rival_title"}.issubset(idx):
        return values

    # avoid duplicate insertion on re-run
    if "my_ebay_url" in idx or "rival_ebay_url" in idx:
        return values

    my_title_i = idx["my_title"]
    rival_title_i = idx["rival_title"]
    item_my_i = idx["item_id_my"]
    item_rival_i = idx["item_id_rival"]

    def item_url(item_id: str) -> str:
        s = str(item_id or "").strip()
        if not s:
            return ""
        return f"https://www.ebay.com/itm/{s}"

    new_header = []
    for i, h in enumerate(header):
        new_header.append(h)
        if i == my_title_i:
            new_header.append("my_ebay_url")
        if i == rival_title_i:
            new_header.append("rival_ebay_url")

    out = [new_header]
    for row in values[1:]:
        # pad for safety
        row = list(row) + [""] * max(0, len(header) - len(row))
        new_row = []
        for i, v in enumerate(row[: len(header)]):
            new_row.append(v)
            if i == my_title_i:
                new_row.append(item_url(row[item_my_i]))
            if i == rival_title_i:
                new_row.append(item_url(row[item_rival_i]))
        out.append(new_row)

    return out


def _coerce_values(values: List[List[str]]) -> List[List[object]]:
    if not values:
        return values
    header = values[0]
    numeric_cols = {"match_conf", "my_price", "rival_price", "diff_abs", "diff_pct"}
    idxs = {i for i, h in enumerate(header) if h in numeric_cols}

    out: List[List[object]] = [header]
    for row in values[1:]:
        r: List[object] = []
        for i, v in enumerate(row):
            if i in idxs and str(v).strip() != "":
                try:
                    r.append(float(str(v).replace(",", "")))
                except Exception:
                    r.append(v)
            else:
                r.append(v)
        out.append(r)
    return out


def clear_and_put_values(service, spreadsheet_id: str, sheet_name: str, values: List[List[str]]):
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A:ZZ", body={}
    ).execute()

    coerced = _coerce_values(values)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        body={"values": coerced},
    ).execute()


def apply_format_and_sort(service, spreadsheet_id: str, sheet_id: int, header: List[str], rows: int):
    if not header:
        return

    hmap = {h: i for i, h in enumerate(header)}

    def col_index(name: str, fallback: int | None = None):
        if name in hmap:
            return hmap[name]
        return fallback

    requests = []

    # Freeze header row
    requests.append(
        {
            "updateSheetProperties": {
                "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount",
            }
        }
    )

    # Currency columns
    for col_name in ["my_price", "rival_price", "diff_abs"]:
        idx = col_index(col_name)
        if idx is None:
            continue
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": rows,
                        "startColumnIndex": idx,
                        "endColumnIndex": idx + 1,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {"type": "NUMBER", "pattern": '#,##0.00" USD"'}
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat",
                }
            }
        )

    # Percent column
    pct_idx = col_index("diff_pct")
    if pct_idx is not None:
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": rows,
                        "startColumnIndex": pct_idx,
                        "endColumnIndex": pct_idx + 1,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {"type": "NUMBER", "pattern": '0.00" %"'}
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat",
                }
            }
        )

    # Sort by diff_abs desc if present
    sort_idx = col_index(os.getenv("SORT_COLUMN_NAME", "diff_abs"))
    if sort_idx is not None and rows > 1:
        requests.append(
            {
                "sortRange": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": rows,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(header),
                    },
                    "sortSpecs": [{"dimensionIndex": sort_idx, "sortOrder": "DESCENDING"}],
                }
            }
        )

    # Basic filter on header row
    requests.append(
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": rows,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(header),
                    }
                }
            }
        }
    )

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests}
    ).execute()


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--csv",
        default="/home/tomoyuki/.openclaw/workspace/data/price_compare_us_ultra_strict_high_precision_only.csv",
        help="input CSV path",
    )
    p.add_argument(
        "--spreadsheet-id",
        default=os.getenv("TARGET_SPREADSHEET_ID", DEFAULT_SPREADSHEET_ID),
    )
    p.add_argument(
        "--sheet-name",
        default=os.getenv("TARGET_SHEET_NAME", DEFAULT_SHEET_NAME),
    )
    args = p.parse_args()

    cred_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not cred_path:
        print("Set GOOGLE_SERVICE_ACCOUNT_JSON to service account JSON path", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(cred_path):
        print(f"Credential file not found: {cred_path}", file=sys.stderr)
        sys.exit(2)

    values = read_csv(args.csv)
    if not values:
        print("CSV is empty", file=sys.stderr)
        sys.exit(2)
    values = _add_link_columns(values)

    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except Exception:
        print(
            "Missing dependency. Install: pip install google-api-python-client google-auth",
            file=sys.stderr,
        )
        sys.exit(2)

    creds = Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    sheet_id = ensure_sheet(service, args.spreadsheet_id, args.sheet_name)
    clear_and_put_values(service, args.spreadsheet_id, args.sheet_name, values)
    header = values[0] if values else []
    apply_format_and_sort(service, args.spreadsheet_id, sheet_id, header, len(values))

    print("OK")
    print(f"spreadsheet_id={args.spreadsheet_id}")
    print(f"sheet={args.sheet_name}")
    print(f"rows={len(values)-1}")


if __name__ == "__main__":
    main()
