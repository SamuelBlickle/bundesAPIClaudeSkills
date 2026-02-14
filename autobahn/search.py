#!/usr/bin/env python3
"""Query the Autobahn API for German highway traffic information."""

import argparse
import json
import sys
import urllib.request
import urllib.error

BASE_URL = "https://verkehr.autobahn.de/o/autobahn"

SERVICES = ["roadworks", "webcam", "parking_lorry", "warning", "closure", "electric_charging_station"]


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


def cmd_roads(args):
    print(json.dumps(api_get("/")))


def cmd_services(args):
    data = api_get(f"/{args.road_id}/services/{args.service}")
    print(json.dumps(data))


def cmd_details(args):
    data = api_get(f"/details/{args.service}/{args.item_id}")
    print(json.dumps(data))


def main():
    parser = argparse.ArgumentParser(description="Query German Autobahn traffic API")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("roads", help="List all available highways")

    p_svc = sub.add_parser("services", help="List items for a road and service type")
    p_svc.add_argument("road_id", help="Road ID (e.g. A1, A23, B1)")
    p_svc.add_argument("service", choices=SERVICES, help="Service type")

    p_det = sub.add_parser("details", help="Get details for a specific item")
    p_det.add_argument("service", choices=SERVICES, help="Service type")
    p_det.add_argument("item_id", help="Item ID (base64-encoded)")

    args = parser.parse_args()

    commands = {
        "roads": cmd_roads,
        "services": cmd_services,
        "details": cmd_details,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
