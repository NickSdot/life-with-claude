#!/usr/bin/env python3
"""Add a new entry to the wishlist README.md."""

import json
import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import (
    README_PATH,
    CATEGORY_EMOJI,
    normalize_category,
    normalize_priority,
)

TABLE_HEADER = "| Type | ID | ⭐ | Title | Issue |"
TABLE_SEPARATOR = "|------|----|----|-------|-------|"


def add_entry(entry_id, category, priority, title, description):
    """Add a new entry to the Open section of README.md."""
    content = README_PATH.read_text()

    emoji = CATEGORY_EMOJI[category]
    priority_num = len(priority)

    # Create the new table row
    anchor = entry_id.lower()
    new_row = f"| {emoji} | {entry_id} | {priority} | [{title}](#{anchor}) | |"

    # Find the Open section table
    section_pattern = rf"(## Open\n\n{re.escape(TABLE_HEADER)}\n{re.escape(TABLE_SEPARATOR)})\n((?:\|[^\n]*\n)*)"
    match = re.search(section_pattern, content)

    if not match:
        print("Error: Could not find Open section")
        sys.exit(1)

    table_header = match.group(1)
    existing_rows = match.group(2)

    # Parse existing rows and their priorities
    rows_with_priority = []
    for row in existing_rows.strip().split('\n'):
        if row.strip():
            star_match = re.search(r'\| (⭐+) \|', row)
            if star_match:
                row_priority = len(star_match.group(1))
                rows_with_priority.append((row, row_priority))

    # Add new row and sort by priority descending
    rows_with_priority.append((new_row, priority_num))
    rows_with_priority.sort(key=lambda x: x[1], reverse=True)

    # Rebuild the table
    sorted_rows = '\n'.join(row for row, _ in rows_with_priority) + '\n'

    # Replace the section
    new_section = f"{table_header}\n{sorted_rows}"
    content = content[:match.start()] + new_section + content[match.end():]

    # Add entry details before the Done section
    details_entry = f"\n### {entry_id}\n**{title}**\n{description}\n"

    # Insert before ## Done
    done_match = re.search(r"\n## Done\n", content)
    if done_match:
        content = content[:done_match.start()] + details_entry + content[done_match.start():]
    else:
        content = content.rstrip() + details_entry

    README_PATH.write_text(content)
    print(f"Added {entry_id}: {title}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add-entry.py <json-data>")
        print('Accepts raw questionnaire answers: {"category": "🐛 Bug", "priority": "⭐⭐⭐ High", ...}')
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])

        # Normalize raw input
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
