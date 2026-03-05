#!/usr/bin/env python3
"""Link a GitHub issue to a wishlist entry."""

import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH


def link_issue(entry_id, issue_url):
    """Add issue link to entry in table and details section."""
    content = README_PATH.read_text()
    entry_id = entry_id.upper()

    # Extract issue number from URL (e.g., https://github.com/anthropics/claude-code/issues/123 -> #123)
    issue_match = re.search(r'/issues/(\d+)', issue_url)
    if not issue_match:
        print(f"Invalid issue URL: {issue_url}")
        sys.exit(1)

    issue_num = issue_match.group(1)
    issue_link = f"[#{issue_num}]({issue_url})"

    # Update table row: | | B001 | ⭐⭐⭐ | [Title](#b001) | | -> | | B001 | ⭐⭐⭐ | [Title](#b001) | [#123](url) |
    row_pattern = rf"(\|\s*✅?\s*\| {entry_id} \| ⭐+ \| \[[^\]]+\]\(#[^\)]+\) \|) \|"
    row_replacement = rf"\1 {issue_link} |"
    new_content, count = re.subn(row_pattern, row_replacement, content, flags=re.IGNORECASE)

    if count == 0:
        # Maybe already has an issue link, try to update it
        row_pattern = rf"(\|\s*✅?\s*\| {entry_id} \| ⭐+ \| \[[^\]]+\]\(#[^\)]+\) \|) \[#\d+\]\([^\)]+\) \|"
        row_replacement = rf"\1 {issue_link} |"
        new_content, count = re.subn(row_pattern, row_replacement, content, flags=re.IGNORECASE)

        if count == 0:
            print(f"Entry {entry_id} not found in table")
            sys.exit(1)

    # Update details section: add Issue line after title
    details_pattern = rf"(### {entry_id}\n\*\*[^\*]+\*\*\n)"

    # Check if Issue line already exists
    if re.search(rf"### {entry_id}\n\*\*[^\*]+\*\*\nIssue:", new_content, re.IGNORECASE):
        # Update existing Issue line
        details_pattern = rf"(### {entry_id}\n\*\*[^\*]+\*\*\n)Issue: \[#\d+\]\([^\)]+\)\n"
        details_replacement = rf"\1Issue: {issue_link}\n"
    else:
        # Add new Issue line
        details_replacement = rf"\1Issue: {issue_link}\n"

    new_content = re.sub(details_pattern, details_replacement, new_content, flags=re.IGNORECASE)

    README_PATH.write_text(new_content)
    print(f"Linked {entry_id} to {issue_link}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: link-issue.py <entry-id> <issue-url>")
        sys.exit(1)

    entry_id = sys.argv[1]
    issue_url = sys.argv[2]

    link_issue(entry_id, issue_url)
