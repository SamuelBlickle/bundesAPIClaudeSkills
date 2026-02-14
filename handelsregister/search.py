#!/usr/bin/env python3
"""Wrapper for handelsregister.py with automatic dependency installation."""

import subprocess
import sys
import importlib
import os
import argparse
import json

REQUIRED_PACKAGES = {
    "mechanize": "mechanize",
    "bs4": "beautifulsoup4",
}


def ensure_dependencies():
    missing = []
    for module, package in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--user", "--quiet"] + missing
        )
        importlib.invalidate_caches()


def main():
    ensure_dependencies()

    # Add handelsregister source to path (local scripts/ dir first, then repo fallback)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(script_dir, "scripts")
    hr_dir = os.path.normpath(os.path.join(script_dir, "..", "..", "handelsregister"))
    if os.path.isdir(scripts_dir):
        sys.path.insert(0, scripts_dir)
    elif os.path.isdir(hr_dir):
        sys.path.insert(0, hr_dir)
    else:
        print(json.dumps({"error": "handelsregister.py not found in scripts/ or repo"}))
        sys.exit(1)

    from handelsregister import HandelsRegister

    parser = argparse.ArgumentParser(description="Search the German Handelsregister")
    parser.add_argument("-s", "--schlagwoerter", required=True, help="Search keywords")
    parser.add_argument(
        "-so",
        "--schlagwortOptionen",
        choices=["all", "min", "exact"],
        default="all",
        help="all=all keywords, min=at least one, exact=exact name",
    )
    parser.add_argument("-f", "--force", action="store_true", help="Skip cache")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug logging")
    args = parser.parse_args()

    # Always output JSON
    args.json = True

    if args.debug:
        import logging
        logger = logging.getLogger("mechanize")
        logger.addHandler(logging.StreamHandler(sys.stderr))
        logger.setLevel(logging.DEBUG)

    try:
        h = HandelsRegister(args)
        h.open_startpage()
        companies = h.search_company()
        print(json.dumps(companies if companies else []))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
