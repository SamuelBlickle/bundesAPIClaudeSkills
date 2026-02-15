---
name: searching-pegel-online
description: Queries the German Pegel-Online API for water level data from federal waterways. Retrieves stations, current measurements, historical values, and water body information. No dependencies required. Use when the user asks about Pegelstände, Wasserstand, Hochwasser, river levels, or water gauges in Germany.
---

# Pegel-Online API

Run `search.py` from this skill directory. No external dependencies (Python stdlib only). Always outputs JSON.

## Usage

```bash
python3 bundesAPIClaudeSkills/pegel-online/search.py COMMAND [OPTIONS]
```

### Commands

| Command | Description | Example |
|---|---|---|
| `stations` | List all stations (optional filters) | `search.py stations` |
| `station ID` | Details for a specific station | `search.py station KÖLN` |
| `measurements ID TIMESERIES` | Historical values (max 31 days) | `search.py measurements KÖLN W` |
| `waters` | List all water bodies | `search.py waters` |

### Station filters

| Flag | Description | Example |
|---|---|---|
| `--water NAME` | Filter by water body | `--water RHEIN` |
| `--fuzzy TEXT` | Fuzzy station name search | `--fuzzy Berlin` |
| `--timeseries TS` | Filter by timeseries type | `--timeseries W` |
| `--current` | Include current measurement | `--current` |

### Measurement options

| Flag | Description | Example |
|---|---|---|
| `--start PERIOD` | Start time (ISO 8601 or period) | `--start P7D` (last 7 days) |
| `--end DATETIME` | End time (ISO 8601) | `--end 2026-02-15T00:00:00+01:00` |

### Station ID

Can be UUID, station name, or gauge number. Names are uppercase (e.g. `KÖLN`, `HAMBURG ST. PAULI`, `EITZE`).

### Timeseries types

| Code | Description |
|---|---|
| `W` | Water level (cm) |
| `Q` | Discharge (m³/s) |
| `WT` | Water temperature (°C) |
| `LT` | Air temperature (°C) |
| `DFH` | Navigation height (cm) |
| `VA` | Flow velocity (m/s) |

### Examples

```bash
S=bundesAPIClaudeSkills/pegel-online/search.py

# All stations on the Rhine
python3 $S stations --water RHEIN

# Fuzzy search for stations near Berlin
python3 $S stations --fuzzy Berlin --current

# Current water level at Köln
python3 $S station KÖLN --current

# Water level measurements for last 7 days
python3 $S measurements KÖLN W --start P7D

# Discharge measurements for last 3 days
python3 $S measurements EITZE Q --start P3D

# All water bodies
python3 $S waters
```

## Response format

**Station list:**
```json
[
  {
    "uuid": "47174d8f-...",
    "number": "48900237",
    "shortname": "EITZE",
    "longname": "EITZE",
    "km": 9.56,
    "agency": "VERDEN",
    "longitude": 9.276,
    "latitude": 52.904,
    "water": {"shortname": "ALLER", "longname": "ALLER"}
  }
]
```

**Station with `--current`** adds `timeseries` array:
```json
{
  "shortname": "W",
  "longname": "WASSERSTAND ROHDATEN",
  "unit": "cm",
  "equidistance": 15,
  "currentMeasurement": {
    "timestamp": "2026-02-15T10:30:00+01:00",
    "value": 323,
    "trend": -1,
    "stateMnwMhw": "normal",
    "stateNswHsw": "unknown"
  }
}
```

**Measurements** (array of timestamp/value pairs):
```json
[
  {"timestamp": "2026-02-15T10:15:00+01:00", "value": 333},
  {"timestamp": "2026-02-15T10:30:00+01:00", "value": 331}
]
```

**trend values:** `-1` (falling), `0` (stable), `1` (rising)

**stateMnwMhw:** `low`, `normal`, `high`, `unknown`

On error: `{"error": "message"}`

## Known limitations

- **Max 31 days**: Measurement queries cannot span more than 31 days.
- **Station names uppercase**: API expects uppercase names (e.g. `KÖLN` not `Köln`).
- **Not all timeseries available everywhere**: Not every station has all timeseries types. Use `--current` to see available timeseries.

## Dependencies

None. Uses only Python standard library (`urllib`).
