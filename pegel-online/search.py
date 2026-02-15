#!/usr/bin/env python3
"""Query the Pegel-Online API for German water level data."""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

BASE_URL = "https://www.pegelonline.wsv.de/webservices/rest-api/v2"


def api_get(path, params=None):
    url = f"{BASE_URL}{path}"
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url += "&" if "?" in url else "?"
            url += urllib.parse.urlencode(filtered)
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            msg = json.loads(body).get("msg", f"HTTP {e.code}")
        except Exception:
            msg = f"HTTP {e.code}: {body[:200]}"
        print(json.dumps({"error": msg}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def cmd_stations(args):
    params = {"prettyprint": "false"}
    if args.water:
        params["waters"] = args.water
    if args.fuzzy:
        params["fuzzyId"] = args.fuzzy
    if args.timeseries:
        params["timeseries"] = args.timeseries
    if args.current:
        params["includeTimeseries"] = "true"
        params["includeCurrentMeasurement"] = "true"
    data = api_get("/stations.json", params)
    print(json.dumps(data))


def cmd_station(args):
    params = {"prettyprint": "false"}
    if args.current:
        params["includeTimeseries"] = "true"
        params["includeCurrentMeasurement"] = "true"
    station_id = urllib.parse.quote(args.id, safe="")
    data = api_get(f"/stations/{station_id}.json", params)
    print(json.dumps(data))


def cmd_measurements(args):
    station_id = urllib.parse.quote(args.id, safe="")
    ts = urllib.parse.quote(args.timeseries, safe="")
    params = {"prettyprint": "false"}
    if args.start:
        params["start"] = args.start
    if args.end:
        params["end"] = args.end
    data = api_get(f"/stations/{station_id}/{ts}/measurements.json", params)
    print(json.dumps(data))


def cmd_waters(args):
    data = api_get("/waters.json", {"prettyprint": "false"})
    print(json.dumps(data))


def main():
    parser = argparse.ArgumentParser(description="Query German Pegel-Online water level API")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("stations", help="List all stations")
    p_list.add_argument("--water", help="Filter by water body (e.g. RHEIN)")
    p_list.add_argument("--fuzzy", help="Fuzzy station name search")
    p_list.add_argument("--timeseries", help="Filter by timeseries (e.g. W, Q, WT)")
    p_list.add_argument("--current", action="store_true", help="Include current measurement")

    p_station = sub.add_parser("station", help="Details for a specific station")
    p_station.add_argument("id", help="Station UUID, name, or gauge number")
    p_station.add_argument("--current", action="store_true", help="Include current measurement")

    p_meas = sub.add_parser("measurements", help="Historical measurement values")
    p_meas.add_argument("id", help="Station UUID, name, or gauge number")
    p_meas.add_argument("timeseries", help="Timeseries type (e.g. W, Q, WT)")
    p_meas.add_argument("--start", help="Start time (ISO 8601 or period like P7D)")
    p_meas.add_argument("--end", help="End time (ISO 8601)")

    sub.add_parser("waters", help="List all water bodies")

    args = parser.parse_args()

    commands = {
        "stations": cmd_stations,
        "station": cmd_station,
        "measurements": cmd_measurements,
        "waters": cmd_waters,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
