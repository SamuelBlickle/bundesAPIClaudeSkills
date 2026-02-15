#!/usr/bin/env python3
"""Query the DWD (Deutscher Wetterdienst) API for weather data and warnings."""

import argparse
import gzip
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

BASE_FORECAST = "https://app-prod-ws.warnwetter.de/v30"
BASE_STATIC = "https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16"

WARNING_PATHS = {
    "nowcast": "/warnings_nowcast.json",
    "nowcast_en": "/warnings_nowcast_en.json",
    "gemeinde": "/gemeinde_warnings_v2.json",
    "gemeinde_en": "/gemeinde_warnings_v2_en.json",
    "coast": "/warnings_coast.json",
    "coast_en": "/warnings_coast_en.json",
    "sea": "/sea_warning_text.json",
    "alpen": "/alpen_forecast_text_dwms.json",
    "lawine": "/warnings_lawine.json",
}

MAX_ITEMS = 10


def api_get(url):
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            data = raw.decode("utf-8")
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"text": data}
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code} for {url}"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def strip_bulk(items):
    """Remove large geometry and HTML data to keep output manageable."""
    for w in items:
        if "regions" in w:
            for r in w["regions"]:
                r.pop("polygonGeometry", None)
                r.pop("polygon", None)
                r.pop("triangles", None)
        w.pop("instructionHtml", None)
        w.pop("descriptionHtml", None)
    return items


def cmd_forecast(args):
    ids = args.station_ids
    url = f"{BASE_FORECAST}/stationOverviewExtended?stationIds={ids}"
    data = api_get(url)
    # Strip verbose fields, keep only forecast1 trimmed to 24h
    drop_fields = {"icon1h", "cloudCoverTotal", "temperatureStd", "surfacePressure",
                   "dewPoint2m", "isDay"}
    for station_id, station in data.items():
        if not isinstance(station, dict):
            continue
        station.pop("forecast2", None)
        fc = station.get("forecast1")
        if isinstance(fc, dict):
            for d in drop_fields:
                fc.pop(d, None)
            for k in list(fc.keys()):
                v = fc[k]
                if isinstance(v, list) and len(v) > 24:
                    fc[k] = v[:24]
        if "days" in station and isinstance(station["days"], list):
            station["days"] = station["days"][:5]
    print(json.dumps(data))


def cmd_warnings(args):
    path = WARNING_PATHS[args.type]
    url = f"{BASE_STATIC}{path}"
    data = api_get(url)
    limit = args.limit
    if isinstance(data, dict):
        # Standard warnings structure
        if "warnings" in data and isinstance(data["warnings"], list):
            total = len(data["warnings"])
            data["warnings"] = strip_bulk(data["warnings"][:limit])
            if total > limit:
                data["_total"] = total
                data["_showing"] = limit
                data["_hint"] = f"Showing {limit} of {total}. Use --limit N for more."
        # binnenSee / gemeinde keyed by region code
        for key in list(data.keys()):
            val = data[key]
            if isinstance(val, dict) and key not in ("warnings", "_total", "_showing", "_hint", "time", "binnenSee"):
                # gemeinde format: {"091620000000": [{...}], ...}
                total_keys = len(val)
                if total_keys > limit:
                    trimmed = dict(list(val.items())[:limit])
                    data[key] = trimmed
                    data["_total_regions"] = total_keys
                    data["_showing_regions"] = limit
    print(json.dumps(data))


STRIP_KEYS = {"imageUrl", "imageThumbUrl", "imageMediumUrl", "blurHash",
               "imageThumbWidth", "imageThumbHeight", "zusatzAttribute",
               "instructionHtml", "descriptionHtml"}


def slim(obj):
    """Remove bulky fields from a dict."""
    if isinstance(obj, dict):
        return {k: v for k, v in obj.items() if k not in STRIP_KEYS}
    return obj


def cmd_crowd(args):
    url = f"{BASE_STATIC}/crowd_meldungen_overview_v2.json"
    data = api_get(url)
    if isinstance(data, dict) and "meldungen" in data:
        total = len(data["meldungen"])
        data["meldungen"] = [slim(m) for m in data["meldungen"][:args.limit]]
        if total > args.limit:
            data["_total"] = total
            data["_showing"] = args.limit
    print(json.dumps(data))


def main():
    parser = argparse.ArgumentParser(description="Query German DWD weather API")
    parser.add_argument("--limit", type=int, default=MAX_ITEMS, help=f"Max items to return (default: {MAX_ITEMS})")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fc = sub.add_parser("forecast", help="Weather forecast for stations")
    p_fc.add_argument("station_ids", help="Station ID(s), comma-separated (e.g. 10865,10382)")

    p_warn = sub.add_parser("warnings", help="Current weather warnings")
    p_warn.add_argument("type", choices=list(WARNING_PATHS.keys()), help="Warning type")

    sub.add_parser("crowd", help="Crowd-sourced weather reports")

    args = parser.parse_args()

    commands = {
        "forecast": cmd_forecast,
        "warnings": cmd_warnings,
        "crowd": cmd_crowd,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
