---
name: searching-autobahn
description: Queries the German Autobahn API for highway traffic information. Retrieves roadworks, traffic warnings, closures, webcams, parking areas, and electric charging stations for any German highway (Autobahn/Bundesstrasse). No dependencies required. Use when the user asks about Autobahn traffic, Baustellen, Stau, Sperrungen, Raststätten, or highway conditions in Germany.
---

# Autobahn API

Run `search.py` from this skill directory. No external dependencies (Python stdlib only). Always outputs JSON.

## Usage

```bash
python3 bundesAPIClaudeSkills/autobahn/search.py COMMAND [OPTIONS]
```

### Commands

| Command | Description | Example |
|---|---|---|
| `roads` | List all 108 available highways | `search.py roads` |
| `services ROAD SERVICE` | List items for a road | `search.py services A1 roadworks` |
| `details SERVICE ITEM_ID` | Get details for an item | `search.py details roadworks "BASE64_ID"` |

### Service types

`roadworks`, `webcam`, `parking_lorry`, `warning`, `closure`, `electric_charging_station`

### Examples

```bash
S=bundesAPIClaudeSkills/autobahn/search.py

# List all highways
python3 $S roads
# -> {"roads": ["A1", "A2", "A3", ...]}  (108 entries)

# Roadworks on A1
python3 $S services A1 roadworks
# -> {"roadworks": [{...}, ...]}

# Traffic warnings on A3
python3 $S services A3 warning
# -> {"warning": [{...}, ...]}

# Charging stations on A9
python3 $S services A9 electric_charging_station

# Details for specific item
python3 $S details roadworks "Uk9BRFdPUktTX19tZG0uc2hfXzYzMTU="
```

## Response format

Road ID format: `A1`, `A23`, `B1`, etc. Item IDs are base64-encoded strings.

**Service list response** (key matches service name):
```json
{
  "roadworks": [
    {
      "identifier": "2026-002514...",
      "title": "A1 | Illingen - Schellenbach",
      "subtitle": "Saarbruecken -> Trier",
      "description": ["Zeitraum...", "Beginn: 22.01.26..."],
      "coordinate": {"lat": 49.413, "long": 7.000},
      "extent": "49.41,7.00,49.42,6.97",
      "display_type": "ROADWORKS",
      "icon": "123",
      "isBlocked": "false",
      "startTimestamp": "2026-01-22T09:00:00+01:00",
      "routeRecommendation": [],
      "footer": []
    }
  ]
}
```

**display_type values:** `ROADWORKS`, `WEBCAM`, `PARKING`, `WARNING`, `CLOSURE`, `CLOSURE_ENTRY_EXIT`, `WEIGHT_LIMIT_35`, `SHORT_TERM_ROADWORKS`, `ELECTRIC_CHARGING_STATION`, `STRONG_ELECTRIC_CHARGING_STATION`

**Webcam extras:** `imageurl` (still image URL), `linkurl` (live stream), `operator`

On error: `{"error": "message"}`

## Known limitations

- **No search/filter**: API only supports listing by road. Filtering must be done client-side.
- **Large responses**: Popular highways (A1, A7) can return 100+ roadworks.
- **Base64 IDs**: Item IDs are opaque base64 strings, not human-readable.
- **HTTP 204**: Returns empty body (no data) for some roads/services instead of an empty array.

## Dependencies

None. Uses only Python standard library (`urllib`).
