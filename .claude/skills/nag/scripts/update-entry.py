#!/usr/bin/env python3
"""Update an existing entry in entries.json and regenerate README."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import CATEGORIES
from entries import load_and_find, save_and_regenerate

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: update-entry.py <entry-id> <field> <new-value>")
        sys.exit(1)

    field = sys.argv[2]
    new_value = sys.argv[3]
    entries, idx, entry = load_and_find(sys.argv[1])

    if field == "category":
        new_prefix = CATEGORIES[new_value]["prefix"]
        new_id = new_prefix + entry["id"][1:]
        if any(e["id"] == new_id for e in entries if e is not entry):
            print(f"ID collision: {new_id} already exists")
            sys.exit(1)
        entries[idx]["id"] = new_id
        entries[idx]["category"] = new_value
    elif field in ("title", "priority", "description", "issue_url"):
        entries[idx][field] = new_value
    else:
        print(f"Unknown field: {field}")
        sys.exit(1)

    save_and_regenerate(entries)
    print(f"Updated {entries[idx]['id']} {field}")
