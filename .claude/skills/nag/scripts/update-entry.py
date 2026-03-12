#!/usr/bin/env python3
"""Update an existing entry in entries.json and regenerate README."""

import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import CATEGORIES
from entries import load, save, find, regenerate_readme


def update_entry(entry_id, field, new_value):
    """Update a specific field of an entry."""
    entries = load()
    idx, entry = find(entries, entry_id)

    if idx is None:
        print(f"Entry {entry_id} not found")
        sys.exit(1)

    if field == "category":
        new_prefix = CATEGORIES[new_value]["prefix"]
        old_num = entry["id"][1:]
        new_id = new_prefix + old_num

        # Check for ID collision
        if any(e["id"] == new_id for e in entries):
            print(f"ID collision: {new_id} already exists")
            sys.exit(1)

        entries[idx]["id"] = new_id
        entries[idx]["category"] = new_value
        print(f"Changed {entry_id} to {new_id} ({new_value})")
    elif field in ("title", "priority", "description"):
        entries[idx][field] = new_value
    else:
        print(f"Unknown field: {field}")
        sys.exit(1)

    save(entries)
    regenerate_readme()
    print(f"Updated {entries[idx]['id']} {field} to: {new_value}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: update-entry.py <entry-id> <field> <new-value>")
        print("Fields: title, priority, description, category")
        sys.exit(1)

    update_entry(sys.argv[1].upper(), sys.argv[2], sys.argv[3])
