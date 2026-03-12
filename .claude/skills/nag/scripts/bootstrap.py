"""
Bootstrap module for /nag skill.

Loads constants, provides normalization maps, runs daily maintenance.
"""

import subprocess
from datetime import date
from pathlib import Path

# === Data Maps ===

CATEGORIES = {
    "bug":  {"emoji": "🐛", "prefix": "B", "gh_template": "bug_report.yml"},
    "flaw": {"emoji": "🤔", "prefix": "F", "gh_template": "model_behavior.yml"},
    "wish": {"emoji": "💫", "prefix": "W", "gh_template": "feature_request.yml"},
}

PRIORITIES = {
    "high":   {"emoji": "🔴", "sort": 3},
    "medium": {"emoji": "🟡", "sort": 2},
    "low":    {"emoji": "🟢", "sort": 1},
}

# Normalization: accept raw questionnaire answers or clean values
_CATEGORY_MAP = {f"{v['emoji']} {k.title()}": k for k, v in CATEGORIES.items()}
_CATEGORY_MAP.update({k: k for k in CATEGORIES})

_PRIORITY_MAP = {f"{v['emoji']} {k.title()}": k for k, v in PRIORITIES.items()}
_PRIORITY_MAP.update({k: k for k in PRIORITIES})


def normalize_category(raw):
    """Normalize category from raw input."""
    return _CATEGORY_MAP.get(raw, raw.lower() if isinstance(raw, str) else raw)


def normalize_priority(raw):
    """Normalize priority from raw input."""
    return _PRIORITY_MAP.get(raw, raw)


# === Path Constants (loaded from constants.sh, shared with shell scripts) ===

def _load_constants():
    script_dir = Path(__file__).parent
    constants = {}
    for line in (script_dir / "constants.sh").read_text().splitlines():
        if line.startswith("export "):
            line = line[7:]
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            value = value.strip('"').strip("'")
            for var, val in constants.items():
                value = value.replace(f"${var}", val)
            constants[key] = value
    return constants

_C = _load_constants()

README_PATH = Path(_C["LWC_README_PATH"])
ENTRIES_PATH = Path(_C["LWC_ENTRIES_PATH"])
HEADER_PATH = Path(_C["LWC_HEADER_PATH"])
SCRIPTS_DIR = Path(_C["LWC_SCRIPTS_DIR"])
TEMPLATES_DIR = Path(_C["LWC_TEMPLATES_DIR"])
GH_TEMPLATES_DIR = Path(_C["LWC_GH_TEMPLATES_DIR"])


# === Daily Maintenance ===

def _daily_check():
    """Fetch GH templates if not done today, regenerate markdown only if changed."""
    last_fetch_file = GH_TEMPLATES_DIR / ".last_fetch"
    today = date.today().isoformat()

    if last_fetch_file.exists() and last_fetch_file.read_text().strip() == today:
        return

    fetch_script = SCRIPTS_DIR / "fetch-gh-templates.sh"
    if fetch_script.exists():
        result = subprocess.run(["bash", str(fetch_script)], capture_output=True, text=True)
        if "TEMPLATES_CHANGED" in result.stdout:
            try:
                from generate_issue_templates import generate_all
                generate_all()
            except Exception:
                pass

_daily_check()
