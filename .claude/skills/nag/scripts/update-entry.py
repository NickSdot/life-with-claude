#!/usr/bin/env python3
"""Update an existing entry in the wishlist README.md."""

import json
import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH, CATEGORY_HEADERS, ID_PREFIX


def update_entry(entry_id, field, new_value):
    """Update a specific field of an entry."""
    content = README_PATH.read_text()
    entry_id = entry_id.upper()

    if field == "title":
        # Update title in table row
        pattern = rf"(\| \[[x ]\] \| {entry_id} \| ⭐+ \| \[)[^\]]+(\]\(#)"
        replacement = rf"\g<1>{new_value}\g<2>"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Update title in details section
        pattern = rf"(### {entry_id}\n)\*\*[^\*]+\*\*"
        replacement = rf"\g<1>**{new_value}**"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    elif field == "priority":
        # Update priority in table row
        pattern = rf"(\| \[[x ]\] \| {entry_id} \| )⭐+( \|)"
        replacement = rf"\g<1>{new_value}\g<2>"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Re-sort the table this entry is in
        content = resort_tables(content)

    elif field == "description":
        # Update description in details section (preserve Issue line if present)
        pattern = rf"(### {entry_id}\n\*\*[^\*]+\*\*\n(?:Issue: [^\n]+\n)?).+?(?=\n###|\n---|\Z)"
        replacement = rf"\g<1>{new_value}"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)

    elif field == "category":
        # This is more complex - need to move between tables
        content = change_category(content, entry_id, new_value)

    else:
        print(f"Unknown field: {field}")
        sys.exit(1)

    README_PATH.write_text(content)
    print(f"Updated {entry_id} {field} to: {new_value}")


def resort_tables(content):
    """Re-sort all tables by priority."""
    for header in CATEGORY_HEADERS.values():
        pattern = rf"({re.escape(header)}\n\| Done \| ID \| ⭐ \| Title \| Issue \|\n\|------\|----\|----\|-------\|-------\|)\n((?:\|[^\n]*\n)*)"
        match = re.search(pattern, content)

        if match:
            table_header = match.group(1)
            existing_rows = match.group(2)

            rows_with_priority = []
            for row in existing_rows.strip().split('\n'):
                if row.strip():
                    star_match = re.search(r'\| (⭐+) \|', row)
                    if star_match:
                        row_priority = len(star_match.group(1))
                        rows_with_priority.append((row, row_priority))

            rows_with_priority.sort(key=lambda x: x[1], reverse=True)
            sorted_rows = '\n'.join(row for row, _ in rows_with_priority) + '\n' if rows_with_priority else ''

            new_section = f"{table_header}\n{sorted_rows}"
            content = content[:match.start()] + new_section + content[match.end():]

    return content


def change_category(content, entry_id, new_category):
    """Move an entry from one category table to another."""
    # Find the row in current table (includes Issue column)
    row_pattern = rf"\| \[[x ]\] \| {entry_id} \| ⭐+ \| \[[^\]]+\]\(#[^\)]+\) \| [^\|]* \|\n"
    match = re.search(row_pattern, content, re.IGNORECASE)

    if not match:
        print(f"Entry {entry_id} not found")
        sys.exit(1)

    row = match.group(0).rstrip('\n')

    # Remove from current table
    content = re.sub(row_pattern, '', content, flags=re.IGNORECASE)

    # Change the ID prefix
    old_prefix = entry_id[0]
    new_prefix = ID_PREFIX[new_category]
    new_id = new_prefix + entry_id[1:]

    row = row.replace(entry_id, new_id)
    row = re.sub(r'\(#[^\)]+\)', f'(#{new_id.lower()})', row)

    # Find new section and add row
    section_header = CATEGORY_HEADERS[new_category]

    pattern = rf"({re.escape(section_header)}\n\| Done \| ID \| ⭐ \| Title \| Issue \|\n\|------\|----\|----\|-------\|-------\|)\n"
    content = re.sub(pattern, rf"\g<1>\n{row}\n", content)

    # Update details section ID
    content = re.sub(rf"### {entry_id}", f"### {new_id}", content, flags=re.IGNORECASE)

    # Resort
    content = resort_tables(content)

    print(f"Changed {entry_id} to {new_id} ({new_category})")
    return content


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: update-entry.py <entry-id> <field> <new-value>")
        print("Fields: title, priority, description, category")
        sys.exit(1)

    entry_id = sys.argv[1]
    field = sys.argv[2]
    new_value = sys.argv[3]

    update_entry(entry_id, field, new_value)
