#!/usr/bin/env python3
"""Query the NINA warning API for German civil protection alerts."""

import argparse
import json
import sys
import urllib.request
import urllib.error

BASE_URL = "https://warnung.bund.de/api31"

SOURCES = ["dwd", "mowas", "katwarn", "biwapp", "lhp", "police"]


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


def cmd_dashboard(args):
    data = api_get(f"/dashboard/{args.ars}.json")
    print(json.dumps(data))


def cmd_details(args):
    data = api_get(f"/warnings/{args.id}.json")
    print(json.dumps(data))


def cmd_mapdata(args):
    data = api_get(f"/{args.source}/mapData.json")
    print(json.dumps(data))


def main():
    parser = argparse.ArgumentParser(description="Query German NINA warning API")
    sub = parser.add_subparsers(dest="command", required=True)

    p_dash = sub.add_parser("dashboard", help="Current warnings for a district")
    p_dash.add_argument("ars", help="12-digit ARS code (e.g. 091620000000)")

    p_det = sub.add_parser("details", help="Full details of a warning")
    p_det.add_argument("id", help="Warning identifier")

    p_map = sub.add_parser("mapdata", help="All current warnings from a source")
    p_map.add_argument("source", choices=SOURCES, help="Warning source")

    args = parser.parse_args()

    commands = {
        "dashboard": cmd_dashboard,
        "details": cmd_details,
        "mapdata": cmd_mapdata,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
