"""
Bootstrap module for /nag skill.

Loads constants, provides normalization maps, runs daily maintenance.
Import this module to access paths, maps, and trigger daily checks.
"""

import subprocess
from datetime import date
from pathlib import Path


# === Normalization Maps ===
# Accept raw questionnaire answers and normalize to clean values

CATEGORY_MAP = {
    "🐛 Bug": "bug",
    "🤔 Flaw": "flaw",
    "💫 Wish": "wish",
    "bug": "bug",
    "flaw": "flaw",
    "wish": "wish",
}

PRIORITY_MAP = {
    "🔴 High": "high",
    "🟡 Medium": "medium",
    "🟢 Low": "low",
    "high": "high",
    "medium": "medium",
    "low": "low",
}

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

EMOJI_CATEGORY = {v["emoji"]: k for k, v in CATEGORIES.items()}


def normalize_category(raw):
    """Normalize category from raw input."""
    return CATEGORY_MAP.get(raw, raw.lower() if isinstance(raw, str) else raw)


def normalize_priority(raw):
    """Normalize priority from raw input."""
    return PRIORITY_MAP.get(raw, raw)


# === Path Constants ===

def _load_constants():
    """Load constants from constants.sh."""
    constants = {}
    script_dir = Path(__file__).parent
    constants_file = script_dir / "constants.sh"

    for line in constants_file.read_text().splitlines():
        if line.startswith("export "):
            line = line[7:]
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            value = value.strip('"').strip("'")
            value = value.replace("$LWC_REPO", constants.get("LWC_REPO", ""))
            value = value.replace("$LWC_SKILL_DIR", constants.get("LWC_SKILL_DIR", ""))
            value = value.replace("$LWC_TEMPLATES_DIR", constants.get("LWC_TEMPLATES_DIR", ""))
            value = value.replace("$LWC_DETAILS_DIR", constants.get("LWC_DETAILS_DIR", ""))
            constants[key] = value
    return constants


_CONSTANTS = _load_constants()

WISHLIST_REPO = _CONSTANTS["LWC_REPO"]
SKILL_DIR = _CONSTANTS["LWC_SKILL_DIR"]
README_PATH = Path(_CONSTANTS["LWC_README_PATH"])
DETAILS_DIR = Path(_CONSTANTS["LWC_DETAILS_DIR"])
ENTRIES_PATH = Path(_CONSTANTS["LWC_ENTRIES_PATH"])
HEADER_PATH = Path(_CONSTANTS["LWC_HEADER_PATH"])
SCRIPTS_DIR = Path(_CONSTANTS["LWC_SCRIPTS_DIR"])
TEMPLATES_DIR = Path(_CONSTANTS["LWC_TEMPLATES_DIR"])
GH_TEMPLATES_DIR = Path(_CONSTANTS["LWC_GH_TEMPLATES_DIR"])




# === Daily Maintenance ===

def _generate_markdown_templates():
    """Generate markdown fill-in templates from YAML sources."""
    try:
        # Import here to avoid circular dependency
        from generate_issue_templates import generate_all
        generate_all()
    except Exception:
        # Silently fail - not critical
        pass


def _daily_check():
    """Fetch GH templates if not done today, regenerate markdown only if changed. Runs silently."""
    last_fetch_file = GH_TEMPLATES_DIR / ".last_fetch"
    today = date.today().isoformat()

    if last_fetch_file.exists() and last_fetch_file.read_text().strip() == today:
        return

    fetch_script = SCRIPTS_DIR / "fetch-gh-templates.sh"
    if fetch_script.exists():
        result = subprocess.run(["bash", str(fetch_script)], capture_output=True, text=True)
        # Only regenerate if templates actually changed
        if "TEMPLATES_CHANGED" in result.stdout:
            _generate_markdown_templates()


_daily_check()
