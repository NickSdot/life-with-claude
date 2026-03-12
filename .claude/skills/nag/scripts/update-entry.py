#!/usr/bin/env python3
"""Update an existing entry in the wishlist README.md."""

import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH, CATEGORY_EMOJI, ID_PREFIX

TABLE_HEADER = "| Type | ID | ⭐ | Title | Issue |"
TABLE_SEPARATOR = "|------|----|----|-------|-------|"


def update_entry(entry_id, field, new_value):
    """Update a specific field of an entry."""
    content = README_PATH.read_text()
    entry_id = entry_id.upper()

    if field == "title":
        # Update title in table row
        pattern = rf"(\| [🐛🤔💫] \| {entry_id} \| ⭐+ \| \[)[^\]]+(\]\(#)"
        replacement = rf"\g<1>{new_value}\g<2>"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Update title in details section
        pattern = rf"(### {entry_id}\n)\*\*[^\*]+\*\*"
        replacement = rf"\g<1>**{new_value}**"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    elif field == "priority":
        # Update priority in table row
        pattern = rf"(\| [🐛🤔💫] \| {entry_id} \| )⭐+( \|)"
        replacement = rf"\g<1>{new_value}\g<2>"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Re-sort the tables
        content = resort_tables(content)

    elif field == "description":
        # Update description in details section (preserve Issue line if present)
        pattern = rf"(### {entry_id}\n\*\*[^\*]+\*\*\n(?:Issue: [^\n]+\n)?).+?(?=\n### |\n## |\Z)"
        replacement = rf"\g<1>{new_value}"
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)

    elif field == "category":
        # Change the type emoji and ID prefix
        content = change_category(content, entry_id, new_value)

    else:
        print(f"Unknown field: {field}")
        sys.exit(1)

    README_PATH.write_text(content)
    print(f"Updated {entry_id} {field} to: {new_value}")


def resort_tables(content):
    """Re-sort Open and Done tables by priority."""
    for section in ("Open", "Done"):
        pattern = rf"(## {section}\n\n{re.escape(TABLE_HEADER)}\n{re.escape(TABLE_SEPARATOR)})\n((?:\|[^\n]*\n)*)"
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
    """Change an entry's category (type emoji and ID prefix)."""
    old_prefix = entry_id[0]
    new_prefix = ID_PREFIX[new_category]
    new_id = new_prefix + entry_id[1:]
    new_emoji = CATEGORY_EMOJI[new_category]

    # Update table row: change emoji and ID
    row_pattern = rf"\| [🐛🤔💫] \| {re.escape(entry_id)} \|"
    row_replacement = f"| {new_emoji} | {new_id} |"
    content = re.sub(row_pattern, row_replacement, content, flags=re.IGNORECASE)

    # Update anchor in table row
    content = re.sub(
        rf"\(#{re.escape(entry_id.lower())}\)",
        f"(#{new_id.lower()})",
        content,
        flags=re.IGNORECASE
    )

    # Update details section ID
    content = re.sub(rf"### {re.escape(entry_id)}", f"### {new_id}", content, flags=re.IGNORECASE)

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
