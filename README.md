# bundesAPI Claude Skills

Claude Skills for German government APIs, based on the open-source API wrappers from [bundesAPI](https://github.com/bundesAPI).

This is an independent project and is not affiliated with, endorsed by, or officially connected to any German government agency or the bundesAPI organization.

## Skills

| Skill | API | Description |
|---|---|---|
| [abfallnavi](abfallnavi/) | Abfallnavi REST API | Waste collection schedules for 19 municipalities |
| [autobahn](autobahn/) | Autobahn API | Highway traffic: roadworks, warnings, closures, webcams, charging stations |
| [dwd](dwd/) | DWD Warnwetter | Weather forecasts, warnings, and crowd reports from Deutscher Wetterdienst |
| [handelsregister](handelsregister/) | handelsregister.de | Company lookup (name, register number, legal form, status) |
| [hilfsmittel](hilfsmittel/) | GKV Hilfsmittelverzeichnis | Assistive devices covered by statutory health insurance |
| [nina](nina/) | NINA Warn-API (BBK) | Civil protection warnings: weather, floods, hazardous substances, police alerts |
| [pegel-online](pegel-online/) | Pegel-Online (WSV) | Water levels, discharge, and temperature at federal waterway gauges |

## Required network access

These domains must be reachable from the Claude execution environment:

| Skill | Domains |
|---|---|
| abfallnavi | `{region}-abfallapp.regioit.de` (e.g. `nuernberg-abfallapp.regioit.de`) |
| autobahn | `verkehr.autobahn.de` |
| dwd | `app-prod-ws.warnwetter.de`, `s3.eu-central-1.amazonaws.com` |
| handelsregister | `www.handelsregister.de` |
| hilfsmittel | `hilfsmittel-api.gkv-spitzenverband.de` |
| nina | `warnung.bund.de` |
| pegel-online | `www.pegelonline.wsv.de` |

Additionally, `handelsregister` requires access to `pypi.org` for auto-installing dependencies on first run.

## Installation

1. Download the `searching-*.zip` from the skill folder you want to use
2. Go to [claude.ai](https://claude.ai) → Settings → Skills
3. Click "Add Skill" and upload the zip file
4. Claude will automatically discover and use the skill when relevant

## Structure

Each skill contains:
- `skill.md` — Skill description with YAML frontmatter (name + description) and usage docs
- `search.py` — Self-contained CLI wrapper, always outputs JSON
- `searching-*.zip` — Ready-to-upload zip for the Claude UI

## Disclaimer

This software is provided "as is", without warranty of any kind. The underlying APIs are operated by third parties and may change or become unavailable at any time. No guarantee is made regarding correctness, completeness, or availability of the returned data. Use at your own risk.

Where code or components from [bundesAPI](https://github.com/bundesAPI) or other third-party projects are included, all rights remain with their respective authors and license terms.
