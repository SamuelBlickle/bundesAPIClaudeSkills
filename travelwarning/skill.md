---
name: searching-travelwarning
description: Queries the German Federal Foreign Office (Auswärtiges Amt) API for travel warnings and security information. Retrieves current warnings by country, diplomatic representations abroad, and foreign embassies in Germany. No dependencies required. Use when the user asks about Reisewarnungen, Sicherheitshinweise, travel advisories, embassies, or consulates for a specific country.
---

# Reisewarnungen API (Auswärtiges Amt)

Run `search.py` from this skill directory. No external dependencies (Python stdlib only). Always outputs JSON.

## Usage

```bash
python3 /mnt/skills/user/searching-travelwarning/search.py COMMAND [OPTIONS]
```

### Commands

| Command | Description | Example |
|---|---|---|
| `list` | All countries with warning status | `search.py list` |
| `detail CONTENT_ID` | Full warning text for a country | `search.py detail 201068` |
| `embassies-abroad` | German representations abroad | `search.py embassies-abroad` |
| `embassies-in-germany` | Foreign representations in Germany | `search.py embassies-in-germany` |

### Options

| Flag | Description | Example |
|---|---|---|
| `--country CODE` | Filter by 2-letter ISO country code | `--country UA` |
| `--limit N` | Max items to return (default: 10) | `--limit 20` |

### Examples

```bash
S=/mnt/skills/user/searching-travelwarning/search.py

# List all countries with warning status
python3 $S list

# Filter for a specific country
python3 $S list --country UA

# Full warning text (use contentId from list)
python3 $S detail 201068

# German embassies abroad, filtered
python3 $S embassies-abroad --country FR
```

## Response format

**List response:**
```json
{
  "_total": 195,
  "_showing": 10,
  "warnings": [
    {
      "contentId": "201068",
      "lastModified": 1707912345000,
      "title": "Ukraine: Reisewarnung",
      "countryCode": "UA",
      "countryName": "Ukraine",
      "warning": true,
      "partialWarning": false,
      "situationWarning": false,
      "situationPartWarning": false
    }
  ]
}
```

**Warning flags:**
- `warning` — full travel warning (Reisewarnung)
- `partialWarning` — partial/regional warning
- `situationWarning` — situation-based warning
- `situationPartWarning` — partial situation-based warning

**Detail response** adds `content` field with HTML text.

**Timestamps** are Unix milliseconds.

On error: `{"error": "message"}`

## Known limitations

- **HTML content**: Detail responses contain raw HTML in `content` field.
- **Content IDs**: Not predictable, must be obtained from `list` first.
- **No text search**: Cannot search warnings by keyword. Use `--country` to filter.
- **Rate limiting**: Max 60 requests per hour advised.

## Dependencies

None. Uses only Python standard library (`urllib`).
