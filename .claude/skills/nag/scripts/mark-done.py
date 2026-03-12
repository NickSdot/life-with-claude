#!/usr/bin/env python3
"""Mark an entry as done in entries.json and regenerate README."""

import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from entries import load, save, find, regenerate_readme


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mark-done.py <entry-id>")
        sys.exit(1)

    entry_id = sys.argv[1].upper()
    entries = load()
    idx, entry = find(entries, entry_id)

    if idx is None:
        print(f"Entry {entry_id} not found")
        sys.exit(1)

    if entry["done"]:
        print(f"{entry_id} is already marked as done")
        sys.exit(1)

    entries[idx]["done"] = True
    save(entries)
    regenerate_readme()
    print(f"Marked {entry_id} as done")
    print(f"TITLE:{entry['title']}")
