#!/usr/bin/env python3
"""Mark an entry as done by moving it from Open to Done."""

import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH

TABLE_HEADER = "| Type | ID | ⭐ | Title | Issue |"
TABLE_SEPARATOR = "|------|----|----|-------|-------|"
ROW_PATTERN = r"\| [🐛🤔💫] \| {entry_id} \| ⭐+ \| \[[^\]]+\]\(#[^\)]+\) \| [^\n]* \|\n"


def get_entry_title(content, entry_id):
    """Get the title of an entry."""
    pattern = rf"\| [🐛🤔💫] \| {re.escape(entry_id)} \| ⭐+ \| \[([^\]]+)\]"
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1) if match else None


def mark_done(entry_id):
    """Move an entry from Open to Done."""
    content = README_PATH.read_text()

    # Find the row in the Open section
    open_pattern = rf"## Open\n\n{re.escape(TABLE_HEADER)}\n{re.escape(TABLE_SEPARATOR)}\n((?:\|[^\n]+\n)*)"
    open_match = re.search(open_pattern, content)
    if not open_match:
        print("Error: Could not find Open section")
        return False

    open_rows = open_match.group(1)
    row_pattern = rf"(\| [🐛🤔💫] \| {re.escape(entry_id)} \| [^\n]+ \|)\n"
    row_match = re.search(row_pattern, open_rows, re.IGNORECASE)

    if not row_match:
        # Check if already in Done
        done_pattern = rf"## Done\n\n{re.escape(TABLE_HEADER)}\n{re.escape(TABLE_SEPARATOR)}\n((?:\|[^\n]+\n)*)"
        done_match = re.search(done_pattern, content)
        if done_match and re.search(rf"\| {re.escape(entry_id)} \|", done_match.group(1), re.IGNORECASE):
            print(f"{entry_id} is already marked as done")
            return False
        print(f"Entry {entry_id} not found in Open section")
        return False

    row = row_match.group(1)

    # Remove row from Open table
    content = content[:open_match.start(1) + row_match.start()] + content[open_match.start(1) + row_match.end():]

    # Find the detail section for this entry and extract it
    detail_pattern = rf"\n### {re.escape(entry_id)}\n\*\*[^\*]+\*\*\n(?:Issue: [^\n]+\n)?.+?(?=\n### |\n## |\Z)"
    detail_match = re.search(detail_pattern, content, re.DOTALL)
    detail_text = detail_match.group(0) if detail_match else ""

    # Remove detail from its current location
    if detail_match:
        content = content[:detail_match.start()] + content[detail_match.end():]

    # Add row to Done table
    done_table_pattern = rf"(## Done\n\n{re.escape(TABLE_HEADER)}\n{re.escape(TABLE_SEPARATOR)})\n((?:\|[^\n]*\n)*)"
    done_match = re.search(done_table_pattern, content)

    if done_match:
        done_header = done_match.group(1)
        done_rows = done_match.group(2)
        new_done = f"{done_header}\n{row}\n{done_rows}"
        content = content[:done_match.start()] + new_done + content[done_match.end():]
    else:
        print("Error: Could not find Done section")
        return False

    # Append detail at end of file
    content = content.rstrip() + detail_text + "\n"

    README_PATH.write_text(content)
    print(f"Marked {entry_id} as done")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mark-done.py <entry-id>")
        sys.exit(1)

    entry_id = sys.argv[1].upper()

    content = README_PATH.read_text()
    title = get_entry_title(content, entry_id)

    if mark_done(entry_id):
        if title:
            print(f"TITLE:{title}")
        sys.exit(0)
    else:
        sys.exit(1)
