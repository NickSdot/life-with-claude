#!/usr/bin/env python3
"""Link a GitHub issue URL to an entry in entries.json and regenerate README."""

import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from entries import load, save, find, regenerate_readme


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: link-issue.py <entry-id> <issue-url>")
        sys.exit(1)

    entry_id = sys.argv[1].upper()
    issue_url = sys.argv[2]

    entries = load()
    idx, entry = find(entries, entry_id)

    if idx is None:
        print(f"Entry {entry_id} not found")
        sys.exit(1)

    entries[idx]["issue_url"] = issue_url
    save(entries)
    regenerate_readme()
    print(f"Linked {entry_id} to {issue_url}")
