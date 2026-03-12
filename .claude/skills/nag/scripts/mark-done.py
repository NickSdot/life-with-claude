#!/usr/bin/env python3
"""Mark an entry as done in entries.json and regenerate README."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from entries import load_and_find, save_and_regenerate

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mark-done.py <entry-id>")
        sys.exit(1)

    entries, idx, entry = load_and_find(sys.argv[1])

    if entry["done"]:
        print(f"{entry['id']} is already marked as done")
        sys.exit(1)

    entries[idx]["done"] = True
    save_and_regenerate(entries)
    print(f"Marked {entry['id']} as done")
    print(f"TITLE:{entry['title']}")
