---
name: searching-handelsregister
description: Searches the German Handelsregister (handelsregister.de) for company data. Auto-installs dependencies on first run. Queries by company name, register number, legal form, location, and federal state. Use when the user wants to look up German companies, check registration status, or find entries in the Handelsregister.
---

# Handelsregister - Erweiterte Suche

Run `search.py` from this skill directory. It auto-installs dependencies (`mechanize`, `beautifulsoup4`) on first run and wraps `handelsregister/handelsregister.py`. Always outputs JSON.

**Rate limit**: Max 60 requests/hour (legal requirement per Paragraph 9 Abs. 1 HGB).

## Usage

```bash
python3 bundesAPIClaudeSkills/handelsregister/search.py -s "SUCHBEGRIFF" [OPTIONS]
```

### Options

| Flag | Description |
|---|---|
| `-s`, `--schlagwoerter` | Search keywords (required) |
| `-so`, `--schlagwortOptionen` | `all` = all keywords match, `min` = at least one, `exact` = exact company name. Default: `all` |
| `-f`, `--force` | Skip cache, force fresh query |
| `-d`, `--debug` | Enable debug logging (to stderr) |

### Examples

```bash
# Exact company name
python3 bundesAPIClaudeSkills/handelsregister/search.py -s "GASAG AG" -so exact

# All keywords must match
python3 bundesAPIClaudeSkills/handelsregister/search.py -s "deutsche bahn" -so all

# At least one keyword, skip cache
python3 bundesAPIClaudeSkills/handelsregister/search.py -s "Test" -so min -f
```

## Response format

```json
[
  {
    "court": "Amtsgericht Stuttgart HRB 12345",
    "register_num": "HRB 12345",
    "name": "Example GmbH",
    "state": "Baden-Wuerttemberg",
    "status": "aktuell eingetragen",
    "statusCurrent": "AKTUELL_EINGETRAGEN",
    "documents": "ADCDHDDKUTVÖSI",
    "history": [["Alter Name GmbH", "Stuttgart"]]
  }
]
```

On error: `{"error": "message"}`

## Caching

Results are cached in `{tempdir}/handelsregister_cache/` keyed by search term. Use `-f` to bypass.

## Known limitations

- **Rate limiting / 404 errors**: Rapid successive requests can trigger HTTP 404 on `handelsregister.de`. Wait a few seconds between requests.
- **`-so exact` is strict**: The portal requires the exact registered name. "Siemens AG" returns 0 results because the registered name is "Siemens Aktiengesellschaft". Prefer `-so all` for discovery.
- **Empty results `[]`**: Can mean no match or a silent server rejection. Retry with `-f` and different `-so` option.
- **Max 10 results**: The default response is capped. Pagination is not supported.

## Dependencies

Automatically installed on first run via `pip install --user`:
- `mechanize` (browser automation with session/cookie/form handling)
- `beautifulsoup4` (HTML parsing)
