#!/usr/bin/env python3
"""Mark an entry as done in the wishlist README.md."""

import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH


def mark_done(entry_id):
    """Mark an entry as done by changing [ ] to [x] in its table row."""
    content = README_PATH.read_text()

    # Find the row with this entry ID and change [ ] to [x]
    # Pattern: | [ ] | B001 | ...
    pattern = rf"\| \[ \] \| ({re.escape(entry_id)}) \|"
    replacement = rf"| [x] | \1 |"

    new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)

    if count == 0:
        # Check if already done
        if re.search(rf"\| \[x\] \| {re.escape(entry_id)} \|", content, re.IGNORECASE):
            print(f"{entry_id} is already marked as done")
            return False
        print(f"Entry {entry_id} not found")
        return False

    README_PATH.write_text(new_content)
    print(f"Marked {entry_id} as done")
    return True


def get_entry_title(entry_id):
    """Get the title of an entry."""
    content = README_PATH.read_text()

    # Find in table: | [x] | B001 | ⭐⭐⭐ | [Title here](#b001) |
    pattern = rf"\| \[[x ]\] \| {re.escape(entry_id)} \| ⭐+ \| \[([^\]]+)\]"
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        return match.group(1)
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mark-done.py <entry-id>")
        sys.exit(1)

    entry_id = sys.argv[1].upper()

    # Get title first (for commit message)
    title = get_entry_title(entry_id)

    if mark_done(entry_id):
        if title:
            print(f"TITLE:{title}")
        sys.exit(0)
    else:
        sys.exit(1)
