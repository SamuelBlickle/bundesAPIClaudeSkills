---
name: searching-nina-warnings
description: Queries the German NINA warning API (Bundesamt für Bevölkerungsschutz) for civil protection alerts. Retrieves current warnings for any German district including severe weather (DWD), floods, hazardous substances, police alerts, KATWARN, and MoWAS messages. No dependencies required. Use when the user asks about Warnungen, Unwetter, Hochwasser, Katastrophenschutz, or emergency alerts in Germany.
---

# NINA Warn-API

Run `search.py` from this skill directory. No external dependencies (Python stdlib only). Always outputs JSON.

## Usage

```bash
python3 bundesAPIClaudeSkills/nina/search.py COMMAND [OPTIONS]
```

### Commands

| Command | Description | Example |
|---|---|---|
| `dashboard ARS` | Current warnings for a district | `search.py dashboard 091620000000` |
| `details ID` | Full details of a warning | `search.py details "mow.DE-BY-A-SE030-..."` |
| `mapdata SOURCE` | All current warnings from a source | `search.py mapdata dwd` |

### Sources for `mapdata`

`dwd` (weather), `mowas` (civil protection), `katwarn`, `biwapp`, `lhp` (floods), `police`

### ARS (Amtlicher Regionalschlüssel)

12-digit regional code identifying a German district. Last 7 digits must be `0000000` (district level only).

Examples:
- `091620000000` — München (Stadt)
- `110000000000` — Berlin
- `059130000000` — Köln
- `064120000000` — Frankfurt am Main
- `020000000000` — Hamburg
- `091710000000` — Augsburg (Stadt)

### Examples

```bash
S=bundesAPIClaudeSkills/nina/search.py

# Warnings for Munich
python3 $S dashboard 091620000000

# Warnings for Berlin
python3 $S dashboard 110000000000

# All current DWD weather warnings
python3 $S mapdata dwd

# All current flood warnings
python3 $S mapdata lhp

# All police alerts
python3 $S mapdata police

# Details for a specific warning
python3 $S details "mow.DE-BY-A-SE030-20201014-30-000"
```

## Response format

**Dashboard response** (array of warnings):
```json
[
  {
    "id": "mow.DE-NW-BN-SE030-20201014-30-000",
    "payload": {
      "version": 2,
      "type": "ALERT",
      "id": "mow.DE-NW-BN-SE030-20201014-30-000",
      "data": {
        "headline": "Gefahrstoffausbreitung",
        "provider": "MOWAS",
        "severity": "Minor",
        "msgType": "Update",
        "area": {"type": "ZGEM", "data": "..."}
      }
    },
    "i18nTitle": {"de": "Gefahrstoffausbreitung in Bonn"},
    "sent": "2020-10-14T16:35:21+02:00"
  }
]
```

**Details response:**
```json
{
  "identifier": "mow.DE-BY-A-SE030-...",
  "sender": "CAP@bbk.bund.de",
  "sent": "2020-10-14T16:35:21+02:00",
  "status": "Actual",
  "msgType": "Alert",
  "info": [
    {
      "language": "de-DE",
      "category": ["Safety"],
      "event": "Gefahrstoffausbreitung",
      "urgency": "Immediate",
      "severity": "Minor",
      "headline": "Warning headline",
      "description": "Detailed description...",
      "instruction": "Action instructions...",
      "area": [{"areaDesc": "Area name", "geocode": [...]}]
    }
  ]
}
```

**Mapdata response** (array):
```json
[
  {
    "id": "lhp.LAND_BY_W3080...",
    "payload": {
      "id": "lhp.LAND_BY_W3080...",
      "data": {
        "headline": "HOCHWASSERWARNUNG...",
        "provider": "LHP",
        "severity": "Minor",
        "msgType": "Alert"
      }
    },
    "i18nTitle": {"de": "Title"},
    "sent": "2024-01-15T10:00:00+01:00"
  }
]
```

**Severity levels:** `Minor`, `Moderate`, `Severe`, `Extreme`

**Message types:** `Alert`, `Update`, `Cancel`

**Providers:** `MOWAS`, `KATWARN`, `BIWAPP`, `DWD`, `LHP`, `POLICE`

On error: `{"error": "message"}`

## Known limitations

- **District-level only**: Dashboard queries require ARS codes at district level (last 7 digits = 0000000).
- **No text search**: Cannot search warnings by keyword. Must query by region or source.
- **German only**: All warning texts are in German.
- **No historical data**: Only current active warnings are returned.

## Dependencies

None. Uses only Python standard library (`urllib`).
