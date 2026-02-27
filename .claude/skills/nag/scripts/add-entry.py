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
    CATEGORY_HEADERS,
    normalize_category,
    normalize_priority,
)


def add_entry(entry_id, category, priority, title, description):
    """Add a new entry to README.md in the correct position."""
    content = README_PATH.read_text()

    section_header = CATEGORY_HEADERS[category]
    priority_num = len(priority)

    # Create the new table row (empty Issue column)
    anchor = entry_id.lower()
    new_row = f"| [ ] | {entry_id} | {priority} | [{title}](#{anchor}) | |"

    # Find the section and its table
    section_pattern = rf"({re.escape(section_header)}\n\| Done \| ID \| ⭐ \| Title \| Issue \|\n\|------\|----\|----\|-------\|-------\|)\n((?:\|[^\n]*\n)*)"
    match = re.search(section_pattern, content)

    if not match:
        print(f"Error: Could not find section {section_header}")
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

    # Add entry details at the end
    details_section = f"\n### {entry_id}\n**{title}**\n{description}\n"

    if "## Entry Details" in content:
        content = content.rstrip() + details_section
    else:
        content = content.rstrip() + "\n\n---\n## Entry Details" + details_section

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
