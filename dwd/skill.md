---
name: searching-dwd-weather
description: Queries the German Weather Service (DWD) API for weather forecasts and warnings. Retrieves station forecasts, nowcast warnings, municipality warnings, coastal warnings, avalanche warnings, and crowd weather reports. No dependencies required. Use when the user asks about Wetter, Wettervorhersage, Unwetterwarnung, Temperatur, or weather forecasts in Germany.
---

# DWD Weather API

Run `search.py` from this skill directory. No external dependencies (Python stdlib only). Always outputs JSON.

## Usage

```bash
python3 /mnt/skills/user/searching-dwd-weather/search.py [--limit N] COMMAND [OPTIONS]
```

### Global options

| Flag | Description | Default |
|---|---|---|
| `--limit N` | Max warnings/items to return | 10 |

Output is automatically truncated: forecast limited to 24 hours and 5 days, polygon geometry and image URLs stripped. Use `--limit` to adjust warning/item count.

### Commands

| Command | Description | Example |
|---|---|---|
| `forecast STATION_IDS` | Weather forecast for stations | `search.py forecast 10865` |
| `warnings TYPE` | Current weather warnings | `search.py warnings nowcast` |
| `crowd` | Crowd-sourced weather reports | `search.py crowd` |

### Warning types

| Type | Description |
|---|---|
| `nowcast` | Nowcast warnings (short-term) |
| `nowcast_en` | Nowcast warnings (English) |
| `gemeinde` | Municipality warnings |
| `gemeinde_en` | Municipality warnings (English) |
| `coast` | Coastal warnings |
| `coast_en` | Coastal warnings (English) |
| `sea` | High-sea warnings (text) |
| `alpen` | Alpine weather forecast (text) |
| `lawine` | Avalanche warnings |

### Station IDs

DWD station identifiers. Common examples:
- `10865` — München-Stadt
- `10382` — Berlin-Tempelhof
- `10513` — Frankfurt/Main
- `10501` — Aachen
- `G005` — Garmisch-Partenkirchen
- `10224` — Hamburg-Fuhlsbüttel
- `10554` — Leipzig-Holzhausen
- `K2621` — Köln-Wahn

Multiple stations: `search.py forecast 10865,10382`

Full list: https://www.dwd.de/DE/leistungen/klimadatendeutschland/stationsliste.html

### Examples

```bash
S=/mnt/skills/user/searching-dwd-weather/search.py

# Forecast for Munich
python3 $S forecast 10865

# Forecast for multiple stations
python3 $S forecast 10865,10382

# Current nowcast warnings
python3 $S warnings nowcast

# Municipality warnings (German)
python3 $S warnings gemeinde

# Coastal warnings
python3 $S warnings coast

# Avalanche warnings
python3 $S warnings lawine

# Crowd weather reports
python3 $S crowd
```

## Response format

**Forecast response** (keyed by station ID):
```json
{
  "10865": {
    "forecast1": {
      "stationId": "10865",
      "start": 1630077980735,
      "timeStep": 3600000,
      "temperature": [123, 125, 130],
      "windSpeed": [50, 45, 60],
      "windDirection": [180, 190, 200],
      "windGust": [85, 80, 90],
      "precipitationTotal": [0, 10, 5],
      "sunshine": [600, 550, 0],
      "icon": [1, 2, 3]
    },
    "days": [
      {
        "dayDate": "2026-02-15",
        "temperatureMin": 20,
        "temperatureMax": 85,
        "icon": 2,
        "precipitation": 10,
        "windSpeed": 50,
        "sunshine": 600
      }
    ],
    "warnings": []
  }
}
```

**Data units** (values are integers in tenths):
| Field | Unit | Conversion |
|---|---|---|
| `temperature` | 0.1 °C | divide by 10 → °C |
| `precipitationTotal` | 0.1 mm/h | divide by 10 → mm/h |
| `precipitation` (daily) | 0.1 mm/d | divide by 10 → mm/d |
| `sunshine` | 0.1 min/d | divide by 10 → min/d |
| `windSpeed` | 0.1 km/h | divide by 10 → km/h |
| `windGust` | 0.1 km/h | divide by 10 → km/h |
| `windDirection` | degrees | — |
| `start`, `end` | ms | Unix timestamp in milliseconds |
| `timeStep` | ms | interval between values |

**Warnings response:**
```json
{
  "time": 1630077980735,
  "warnings": [
    {
      "type": 31,
      "level": 2,
      "start": 1630077980735,
      "end": 1630164380735,
      "event": "Thunderstorm",
      "headLine": "Severe Weather Warning",
      "description": "Detailed description...",
      "instruction": "Action instructions...",
      "isVorabinfo": false,
      "bn": true
    }
  ]
}
```

On error: `{"error": "message"}`

## Known limitations

- **Two base URLs**: Forecast uses `app-prod-ws.warnwetter.de`, warnings use S3 static files.
- **Station IDs**: Must be valid DWD identifiers, no search/autocomplete available.
- **Integer units**: All values are in tenths (divide by 10 for human-readable values).
- **No historical data**: Only current forecasts and active warnings.
- **Large responses**: Output is truncated to 10 items by default. Polygon geometry and HTML fields are stripped. Use `--limit N` for more.

## Dependencies

None. Uses only Python standard library (`urllib`).
