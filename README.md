# bundesAPI Claude Skills

Claude Skills for German government APIs from [bundesAPI](https://github.com/bundesAPI).

## Skills

| Skill | API | Description |
|---|---|---|
| [handelsregister](handelsregister/) | handelsregister.de | Company lookup (name, register number, legal form, status) |
| [abfallnavi](abfallnavi/) | Abfallnavi REST API | Waste collection schedules for 19 municipalities |
| [autobahn](autobahn/) | Autobahn API | Highway traffic: roadworks, warnings, closures, webcams, charging stations |
| [hilfsmittel](hilfsmittel/) | GKV Hilfsmittelverzeichnis | Assistive devices covered by statutory health insurance |

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
