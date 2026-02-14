#!/usr/bin/env python3
"""Query the GKV Hilfsmittelverzeichnis API for assistive devices."""

import argparse
import json
import sys
import urllib.request
import urllib.error

BASE_URL = "https://hilfsmittel-api.gkv-spitzenverband.de/api/verzeichnis"


def api_get(path):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code} for {url}"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def cmd_tree(args):
    data = api_get(f"/VerzeichnisTree/{args.level}")
    if args.filter:
        needle = args.filter.lower()
        data = [n for n in data if needle in n.get("displayValue", "").lower()
                or needle in n.get("xSteller", "").lower()]
    print(json.dumps(data))


def cmd_produktgruppe(args):
    print(json.dumps(api_get(f"/Produktgruppe/{args.id}")))


def cmd_untergruppe(args):
    print(json.dumps(api_get(f"/Untergruppe/{args.id}")))


def cmd_produktart(args):
    print(json.dumps(api_get(f"/Produktart/{args.id}")))


def cmd_produkt(args):
    if args.id:
        print(json.dumps(api_get(f"/Produkt/{args.id}")))
    else:
        print(json.dumps({"error": "Listing all products returns 30MB+. Provide --id or use 'tree' to browse."}))
        sys.exit(1)


def cmd_nachweis(args):
    print(json.dumps(api_get(f"/Nachweisschema/{args.id}")))


def main():
    parser = argparse.ArgumentParser(description="Query GKV Hilfsmittelverzeichnis API")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tree = sub.add_parser("tree", help="Browse product tree (levels 1-4)")
    p_tree.add_argument("level", type=int, choices=[1, 2, 3, 4], help="Tree depth level")
    p_tree.add_argument("--filter", help="Filter nodes by name or xSteller (case-insensitive)")

    p_pg = sub.add_parser("produktgruppe", help="Get product group details")
    p_pg.add_argument("id", help="Product group UUID")

    p_ug = sub.add_parser("untergruppe", help="Get subgroup details")
    p_ug.add_argument("id", help="Subgroup UUID")

    p_pa = sub.add_parser("produktart", help="Get product type details")
    p_pa.add_argument("id", help="Product type UUID")

    p_pr = sub.add_parser("produkt", help="Get product details")
    p_pr.add_argument("--id", help="Product UUID (required, full list is 30MB+)")

    p_nw = sub.add_parser("nachweis", help="Get proof/evidence schema")
    p_nw.add_argument("id", help="Nachweisschema UUID")

    args = parser.parse_args()

    commands = {
        "tree": cmd_tree,
        "produktgruppe": cmd_produktgruppe,
        "untergruppe": cmd_untergruppe,
        "produktart": cmd_produktart,
        "produkt": cmd_produkt,
        "nachweis": cmd_nachweis,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
