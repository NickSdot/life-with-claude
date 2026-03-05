#!/usr/bin/env python3
"""Track GitHub issues for wishlist entries."""

import json
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import SKILL_DIR

ISSUES_PATH = Path(SKILL_DIR) / "issues.json"


def load_issues():
    """Load issues mapping."""
    if not ISSUES_PATH.exists():
        return {}
    return json.loads(ISSUES_PATH.read_text())


def save_issues(issues):
    """Save issues mapping."""
    ISSUES_PATH.write_text(json.dumps(issues, indent=2) + "\n")


def get_issue(entry_id):
    """Get issue data for an entry. Returns string (URL or template) or dict with template/body."""
    issues = load_issues()
    return issues.get(entry_id.upper())


def set_issue(entry_id, value):
    """Set issue data for an entry. Value can be URL string or dict with template/body."""
    issues = load_issues()
    issues[entry_id.upper()] = value
    save_issues(issues)
    if isinstance(value, dict):
        print(f"Tracked {entry_id}: {value.get('template', 'unknown')} (with body)")
    else:
        print(f"Tracked {entry_id}: {value}")


def remove_issue(entry_id):
    """Remove issue tracking for an entry."""
    issues = load_issues()
    entry_id = entry_id.upper()
    if entry_id in issues:
        del issues[entry_id]
        save_issues(issues)
        print(f"Removed tracking for {entry_id}")
    else:
        print(f"No issue tracked for {entry_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: issues.py <get|set|remove> <entry-id> [url]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "get":
        if len(sys.argv) < 3:
            print("Usage: issues.py get <entry-id>")
            sys.exit(1)
        url = get_issue(sys.argv[2])
        if url:
            print(url)
        else:
            sys.exit(1)

    elif command == "set":
        if len(sys.argv) < 4:
            print("Usage: issues.py set <entry-id> <url-or-template> [body-file]")
            sys.exit(1)
        if len(sys.argv) >= 5:
            # Body file provided - store as object
            body = Path(sys.argv[4]).read_text()
            set_issue(sys.argv[2], {"template": sys.argv[3], "body": body})
        else:
            set_issue(sys.argv[2], sys.argv[3])

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: issues.py remove <entry-id>")
            sys.exit(1)
        remove_issue(sys.argv[2])

    elif command == "list":
        issues = load_issues()
        print(json.dumps(issues, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
