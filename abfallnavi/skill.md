---
name: searching-abfallnavi
description: Queries waste collection schedules for German municipalities via the Abfallnavi REST API. Looks up locations, streets, house numbers, waste types (Fraktionen), and collection dates (Termine). Supports 19 regions. No dependencies required. Use when the user asks about garbage collection dates, waste disposal schedules, Muellabfuhr, or Abfallkalender for German cities.
---

# Abfallnavi API

Run `search.py` from this skill directory. No external dependencies (uses only Python stdlib). Always outputs JSON.

## Usage

```bash
python3 bundesAPIClaudeSkills/abfallnavi/search.py [-r REGION] COMMAND [OPTIONS]
```

Default region: `nuernberg`. Available: `aachen`, `zew2`, `aw-bgl2`, `bav`, `din`, `dorsten`, `gt2`, `hlv`, `coe`, `krhs`, `pi`, `krwaf`, `lindlar`, `stl`, `nds`, `nuernberg`, `roe`, `solingen`, `wml2`.

### Commands

| Command | Description | Example |
|---|---|---|
| `orte` | List locations in region | `search.py orte` |
| `strassen ORT_ID` | List streets (with optional `--filter`) | `search.py strassen 6756817 --filter "Aachener"` |
| `hausnummern STRASSEN_ID` | Get house numbers for a street | `search.py hausnummern 7049828` |
| `fraktionen` | List waste types | `search.py fraktionen --hausnummern-id 7049829` |
| `termine` | Get collection dates | `search.py termine --hausnummern-id 7049829 --fraktion 0 --fraktion 1` |

### Full workflow example

```bash
S=bundesAPIClaudeSkills/abfallnavi/search.py

# 1. Find location
python3 $S orte
# -> [{"id": 6756817, "name": "Nuernberg"}]

# 2. Find street
python3 $S strassen 6756817 --filter "Aachener"
# -> [{"id": 7049828, "name": "Aachener Strasse", "hausNrList": [{"id": 7049829, "nr": "1", ...}]}]

# 3. Get waste types at address
python3 $S fraktionen --hausnummern-id 7049829
# -> [{"id": 0, "name": "Restabfall"}, {"id": 1, "name": "Bioabfall"}, ...]

# 4. Get collection dates
python3 $S termine --hausnummern-id 7049829 --fraktion 0 --fraktion 1
# -> [{"datum": "2026-01-08", "bezirk": {"fraktionId": 0, ...}}, ...]
```

### Other region example

```bash
python3 $S -r aachen orte
# -> [{"id": 11155895, "name": "Aachen"}]
```

## Response formats

**Fraktionen:**
```json
[
  {"id": 0, "name": "Restabfall", "iconNr": 7, "farbeRgb": "555555", "material": []},
  {"id": 1, "name": "Bioabfall", "iconNr": 107, "farbeRgb": "4b9b3e", "material": []}
]
```

**Termine:**
```json
{"id": 7123060, "bezirk": {"id": 7049830, "name": "B1", "gueltigAb": "2026-01-01", "fraktionId": 0}, "datum": "2026-01-08", "jahr": 2026, "info": null}
```

On error: `{"error": "message"}`

## Known limitations

- **Large responses**: `strassen` can return thousands of entries (2975 for Nuernberg). Use `--filter` to narrow down.
- **Incomplete hausNrList**: Only the first street in `strassen` response includes house numbers. Use `hausnummern STRASSEN_ID` for a specific street.
- **IDs are not stable**: IDs can change over time, do not cache permanently.
- **Region-specific fraction IDs**: Waste type IDs differ between regions (Nuernberg: 0=Restabfall, Aachen: 14=Restabfall). Always query `fraktionen` first.
- **Some regions skip house numbers**: Use `--strassen-id` instead of `--hausnummern-id` for `fraktionen` and `termine`.

## Dependencies

None. Uses only Python standard library (`urllib`).
