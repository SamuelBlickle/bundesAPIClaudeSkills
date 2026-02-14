# bundesAPI Claude Skills

Claude Skills for German government APIs, based on the open-source API wrappers from [bundesAPI](https://github.com/bundesAPI).

This is an independent project and is not affiliated with, endorsed by, or officially connected to any German government agency or the bundesAPI organization.

## Skills

| Skill | API | Description |
|---|---|---|
| [handelsregister](handelsregister/) | handelsregister.de | Company lookup (name, register number, legal form, status) |
| [abfallnavi](abfallnavi/) | Abfallnavi REST API | Waste collection schedules for 19 municipalities |
| [autobahn](autobahn/) | Autobahn API | Highway traffic: roadworks, warnings, closures, webcams, charging stations |
| [hilfsmittel](hilfsmittel/) | GKV Hilfsmittelverzeichnis | Assistive devices covered by statutory health insurance |

## Required network access

These domains must be reachable from the Claude execution environment:

| Skill | Domains |
|---|---|
| handelsregister | `www.handelsregister.de` |
| abfallnavi | `{region}-abfallapp.regioit.de` (e.g. `nuernberg-abfallapp.regioit.de`) |
| autobahn | `verkehr.autobahn.de` |
| hilfsmittel | `hilfsmittel-api.gkv-spitzenverband.de` |

Additionally, `handelsregister` requires access to `pypi.org` for auto-installing dependencies on first run.

## Structure

Each skill contains:
- `skill.md` — Skill description with YAML frontmatter (name + description) and usage docs
- `search.py` — Self-contained CLI wrapper, always outputs JSON
- `searching-*.zip` — Ready-to-upload zip for the Claude UI

## Usage

All skills (except handelsregister) require no external dependencies.

```bash
# Autobahn roadworks
python3 autobahn/search.py services A1 roadworks

# Waste collection dates in Nuernberg
python3 abfallnavi/search.py orte
python3 abfallnavi/search.py termine --hausnummern-id 7049829 --fraktion 0

# Assistive devices catalog
python3 hilfsmittel/search.py tree 1

# Company lookup (auto-installs mechanize + beautifulsoup4)
python3 handelsregister/search.py -s "Deutsche Bahn" -so all
```

## Disclaimer

This software is provided "as is", without warranty of any kind. The underlying APIs are operated by third parties and may change or become unavailable at any time. No guarantee is made regarding correctness, completeness, or availability of the returned data. Use at your own risk.
