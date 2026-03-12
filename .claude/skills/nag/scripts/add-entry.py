#!/usr/bin/env python3
"""Add a new entry to entries.json and regenerate README."""

import json
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import normalize_category, normalize_priority
from entries import load, save, regenerate_readme


def add_entry(entry_id, category, priority, title, description):
    """Add a new entry."""
    entries = load()
    entries.append({
        "id": entry_id,
        "category": category,
        "priority": priority,
        "title": title,
        "description": description,
        "done": False,
        "issue_url": None,
    })
    save(entries)
    regenerate_readme()
    print(f"Added {entry_id}: {title}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add-entry.py <json-data>")
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        data["category"] = normalize_category(data["category"])
        data["priority"] = normalize_priority(data["priority"])

        add_entry(
            data["id"],
            data["category"],
            data["priority"],
            data["title"],
            data["description"]
        )
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Missing field: {e}")
        sys.exit(1)
