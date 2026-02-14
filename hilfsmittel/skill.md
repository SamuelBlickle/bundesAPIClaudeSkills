---
name: searching-hilfsmittel
description: Queries the GKV Hilfsmittelverzeichnis API for assistive devices covered by German statutory health insurance. Browses the hierarchical product tree (Produktgruppen, Anwendungsorte, Untergruppen, Produktarten) and retrieves product details. No dependencies required. Use when the user asks about Hilfsmittel, medical aids, assistive devices, GKV, Krankenkasse, or health insurance product catalogs.
---

# Hilfsmittelverzeichnis API

Run `search.py` from this skill directory. No external dependencies (Python stdlib only). Always outputs JSON.

## Usage

```bash
python3 bundesAPIClaudeSkills/hilfsmittel/search.py COMMAND [OPTIONS]
```

### Commands

| Command | Description | Example |
|---|---|---|
| `tree LEVEL` | Browse product tree (1-4) | `search.py tree 1` |
| `produktgruppe ID` | Product group details | `search.py produktgruppe UUID` |
| `untergruppe ID` | Subgroup details | `search.py untergruppe UUID` |
| `produktart ID` | Product type details | `search.py produktart UUID` |
| `produkt --id ID` | Product details | `search.py produkt --id UUID` |
| `nachweis ID` | Proof/evidence schema | `search.py nachweis UUID` |

All IDs are UUIDs. Use `tree` to discover them.

### Hierarchy (x-Steller system)

1. **Produktgruppe** (2-digit, e.g. `18`) - Top category
2. **Anwendungsort** (4-digit, e.g. `18.50`) - Application site
3. **Untergruppe** (6-digit, e.g. `18.50.01`) - Subgroup
4. **Produktart** (7-digit, e.g. `18.50.01.0`) - Product type
5. **Produkt** (10-digit, e.g. `18.50.01.0002`) - Individual product

### Workflow example

```bash
S=bundesAPIClaudeSkills/hilfsmittel/search.py

# 1. Browse top-level groups (43 groups)
python3 $S tree 1
# -> [{"id": "97ae20d2-...", "xSteller": "18", "displayValue": "18 - Kranken-/ Behindertenfahrzeuge"}, ...]

# 2. Filter by keyword or xSteller
python3 $S tree 2 --filter "18"
# -> [{"xSteller": "18.50", "displayValue": "50 - Innenraum und Aussenbereich"}, ...]

# 3. Get details for a product group
python3 $S produktgruppe "97ae20d2-e9dc-490b-996f-8a804dfeaca9"
# -> {"bezeichnung": "Kranken-/ Behindertenfahrzeuge", "definition": "...", "indikation": "..."}

# 4. Get specific product
python3 $S produkt --id "PRODUCT_UUID"
```

## Response formats

**Tree node:**
```json
{"id": "97ae20d2-...", "parentId": null, "displayValue": "18 - Kranken-/ Behindertenfahrzeuge", "xSteller": "18", "level": 1}
```

**Produktgruppe:**
```json
{"id": "...", "bezeichnung": "...", "nummer": 18, "definition": "...", "indikation": "...", "querverweis": "..."}
```

**Produkt:**
```json
{"id": "...", "name": "...", "zehnSteller": "18.50.01.0002", "herstellerName": "...", "artikelnummern": [...]}
```

On error: `{"error": "message"}`

## Known limitations

- **No full product list**: `GET /Produkt` returns 30MB+. The script blocks this and requires `--id`.
- **UUIDs required**: All detail endpoints need UUIDs from the tree. No search by name at API level.
- **Tree level 2+ is large**: Level 2 returns hundreds of nodes. Use `--filter` to narrow down.
- **Tree filter**: Filters `displayValue` and `xSteller` only, not descriptions.

## Dependencies

None. Uses only Python standard library (`urllib`).
