#!/usr/bin/env python3
"""Link a GitHub issue URL to an entry in entries.json and regenerate README."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from entries import load_and_find, save_and_regenerate

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: link-issue.py <entry-id> <issue-url>")
        sys.exit(1)

    entries, idx, _ = load_and_find(sys.argv[1])
    entries[idx]["issue_url"] = sys.argv[2]
    save_and_regenerate(entries)
    print(f"Linked {entries[idx]['id']} to {sys.argv[2]}")
