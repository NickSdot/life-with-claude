#!/usr/bin/env python3
"""Add a new entry to entries.json and regenerate README."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import normalize_category, normalize_priority
from entries import load, save_and_regenerate

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add-entry.py <json-data>")
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        data["category"] = normalize_category(data["category"])
        data["priority"] = normalize_priority(data["priority"])

        entries = load()
        entries.append({
            "id": data["id"],
            "category": data["category"],
            "priority": data["priority"],
            "title": data["title"],
            "description": data["description"],
            "done": False,
            "issue_url": data.get("issue_url"),
        })
        save_and_regenerate(entries)
        print(f"Added {data['id']}: {data['title']}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Missing field: {e}")
        sys.exit(1)
