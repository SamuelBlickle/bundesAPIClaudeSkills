#!/usr/bin/env python3
"""Search waste collection schedules via the Abfallnavi REST API."""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

REGIONS = [
    "aachen", "zew2", "aw-bgl2", "bav", "din", "dorsten", "gt2", "hlv",
    "coe", "krhs", "pi", "krwaf", "lindlar", "stl", "nds", "nuernberg",
    "roe", "solingen", "wml2",
]


def api_get(region, path):
    url = f"https://{region}-abfallapp.regioit.de/abfall-app-{region}/rest{path}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code} for {url}"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed for region '{region}': {e.reason}"}))
        sys.exit(1)


def cmd_orte(args):
    data = api_get(args.region, "/orte")
    print(json.dumps(data))


def cmd_strassen(args):
    data = api_get(args.region, f"/orte/{args.ort_id}/strassen")
    if args.filter:
        needle = args.filter.lower()
        data = [s for s in data if needle in s["name"].lower()]
    print(json.dumps(data))


def cmd_hausnummern(args):
    data = api_get(args.region, f"/strassen/{args.strassen_id}")
    print(json.dumps(data))


def cmd_fraktionen(args):
    if args.hausnummern_id:
        data = api_get(args.region, f"/hausnummern/{args.hausnummern_id}/fraktionen")
    elif args.strassen_id:
        data = api_get(args.region, f"/strassen/{args.strassen_id}/fraktionen")
    else:
        data = api_get(args.region, "/fraktionen")
    print(json.dumps(data))


def cmd_termine(args):
    if not args.fraktion:
        print(json.dumps({"error": "At least one --fraktion ID is required"}))
        sys.exit(1)
    params = "&".join(f"fraktion={f}" for f in args.fraktion)
    if args.hausnummern_id:
        path = f"/hausnummern/{args.hausnummern_id}/termine?{params}"
    elif args.strassen_id:
        path = f"/strassen/{args.strassen_id}/termine?{params}"
    else:
        print(json.dumps({"error": "Either --strassen-id or --hausnummern-id is required"}))
        sys.exit(1)
    data = api_get(args.region, path)
    print(json.dumps(data))


def main():
    parser = argparse.ArgumentParser(description="Query Abfallnavi waste collection API")
    parser.add_argument(
        "-r", "--region", default="nuernberg", choices=REGIONS,
        help="Region identifier (default: nuernberg)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("orte", help="List locations in region")

    p_str = sub.add_parser("strassen", help="List streets in a location")
    p_str.add_argument("ort_id", type=int, help="Location ID")
    p_str.add_argument("--filter", help="Filter street names (case-insensitive substring)")

    p_hnr = sub.add_parser("hausnummern", help="Get house numbers for a street")
    p_hnr.add_argument("strassen_id", type=int, help="Street ID")

    p_frak = sub.add_parser("fraktionen", help="List waste types")
    p_frak.add_argument("--hausnummern-id", type=int, help="House number ID")
    p_frak.add_argument("--strassen-id", type=int, help="Street ID")

    p_term = sub.add_parser("termine", help="Get collection dates")
    p_term.add_argument("--hausnummern-id", type=int, help="House number ID")
    p_term.add_argument("--strassen-id", type=int, help="Street ID")
    p_term.add_argument("--fraktion", type=int, action="append", help="Waste type ID (repeatable)")

    args = parser.parse_args()

    commands = {
        "orte": cmd_orte,
        "strassen": cmd_strassen,
        "hausnummern": cmd_hausnummern,
        "fraktionen": cmd_fraktionen,
        "termine": cmd_termine,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
