#!/usr/bin/env python3
"""Query the Auswärtiges Amt travel warning API."""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error

BASE_URL = "https://www.auswaertiges-amt.de/opendata"

MAX_ITEMS = 10


def api_get(path):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code} for {url}"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def strip_html(text):
    """Remove HTML tags for compact output."""
    return re.sub(r"<[^>]+>", "", text).strip() if text else ""


def cmd_list(args):
    data = api_get("/travelwarning")
    resp = data.get("response", data)
    content_list = resp.get("contentList", [])
    warnings = []
    for cid in content_list:
        entry = resp.get(str(cid))
        if not entry or not isinstance(entry, dict):
            continue
        item = {
            "contentId": str(cid),
            "lastModified": entry.get("lastModified"),
            "title": entry.get("title"),
            "countryCode": entry.get("CountryCode", entry.get("countryCode")),
            "countryName": entry.get("CountryName", entry.get("countryName")),
            "warning": entry.get("warning", False),
            "partialWarning": entry.get("partialWarning", False),
            "situationWarning": entry.get("situationWarning", False),
            "situationPartWarning": entry.get("situationPartWarning", False),
        }
        if args.country and item.get("countryCode", "").upper() != args.country.upper():
            continue
        warnings.append(item)
    total = len(warnings)
    result = {"warnings": warnings[:args.limit]}
    if total > args.limit:
        result["_total"] = total
        result["_showing"] = args.limit
    print(json.dumps(result))


def cmd_detail(args):
    data = api_get(f"/travelwarning/{args.content_id}")
    resp = data.get("response", data)
    entry = resp.get(str(args.content_id))
    if not entry:
        print(json.dumps({"error": f"No data for contentId {args.content_id}"}))
        sys.exit(1)
    content = entry.get("content", "")
    # Truncate HTML content to avoid context overflow
    plain = strip_html(content)
    if len(plain) > 4000:
        plain = plain[:4000] + "... [truncated]"
    result = {
        "contentId": str(args.content_id),
        "title": entry.get("title"),
        "countryCode": entry.get("CountryCode", entry.get("countryCode")),
        "countryName": entry.get("CountryName", entry.get("countryName")),
        "lastModified": entry.get("lastModified"),
        "warning": entry.get("warning", False),
        "partialWarning": entry.get("partialWarning", False),
        "content": plain,
    }
    print(json.dumps(result))


def resolve_country_name(code):
    """Resolve a 2-letter ISO code to the German country name via travelwarning API."""
    data = api_get("/travelwarning")
    resp = data.get("response", data)
    for cid in resp.get("contentList", []):
        entry = resp.get(str(cid))
        if not entry or not isinstance(entry, dict):
            continue
        cc = (entry.get("CountryCode") or entry.get("countryCode") or "").upper()
        if cc == code.upper():
            return entry.get("CountryName") or entry.get("countryName") or ""
    return None


def cmd_embassies(args, endpoint):
    data = api_get(endpoint)
    resp = data.get("response", data)
    content_list = resp.get("contentList", [])
    results = []
    for cid in content_list:
        country_block = resp.get(str(cid))
        if not isinstance(country_block, dict):
            continue
        country_name = country_block.get("country", "")
        for key, entry in country_block.items():
            if not isinstance(entry, dict) or key in ("contentList", "lastModified", "country"):
                continue
            item = {
                "description": entry.get("description"),
                "leader": entry.get("leader"),
                "country": entry.get("country", country_name),
                "city": entry.get("city"),
                "address": entry.get("address"),
                "phone": entry.get("phone"),
                "fax": entry.get("fax"),
                "website": entry.get("website"),
            }
            results.append(item)
    if args.country:
        query = args.country.strip()
        # If it looks like a 2-letter ISO code, resolve to German country name
        if len(query) == 2 and query.isalpha():
            resolved = resolve_country_name(query)
            if resolved:
                query = resolved
        # Case-insensitive exact match on country name
        query_upper = query.upper()
        results = [r for r in results if (r.get("country") or "").upper() == query_upper]
    total = len(results)
    out = {"representations": results[:args.limit]}
    if total > args.limit:
        out["_total"] = total
        out["_showing"] = args.limit
    print(json.dumps(out))


def add_common(p):
    p.add_argument("--limit", type=int, default=MAX_ITEMS, help=f"Max items (default: {MAX_ITEMS})")
    p.add_argument("--country", help="Filter by country code or name")


def main():
    parser = argparse.ArgumentParser(description="Query German travel warning API")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="All countries with warning status")
    add_common(p_list)

    p_det = sub.add_parser("detail", help="Full warning text for a country")
    p_det.add_argument("content_id", help="Content ID from list command")

    p_ea = sub.add_parser("embassies-abroad", help="German representations abroad")
    add_common(p_ea)

    p_eg = sub.add_parser("embassies-in-germany", help="Foreign representations in Germany")
    add_common(p_eg)

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "detail":
        cmd_detail(args)
    elif args.command == "embassies-abroad":
        cmd_embassies(args, "/representativesInCountry")
    elif args.command == "embassies-in-germany":
        cmd_embassies(args, "/representativesInGermany")


if __name__ == "__main__":
    main()
