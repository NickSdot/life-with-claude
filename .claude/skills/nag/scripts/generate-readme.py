#!/usr/bin/env python3
"""Generate README.md from entries.json and readme-header.md."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH, HEADER_PATH, CATEGORIES, PRIORITIES
from entries import load

TABLE_HEADER = "| Type | ID | Prio | Title | Issue |"
TABLE_SEPARATOR = "|------|----|----|-------|-------|"


def issue_link(url):
    """Format a GitHub issue URL as a markdown link, or empty string."""
    if not url:
        return ""
    match = re.search(r'/issues/(\d+)', url)
    return f"[#{match.group(1)}]({url})" if match else ""


def render_row(entry):
    """Render a single table row."""
    emoji = CATEGORIES[entry["category"]]["emoji"]
    prio = PRIORITIES[entry["priority"]]["emoji"]
    title = f"[{entry['title']}](#{entry['id'].lower()})"
    issue = issue_link(entry.get("issue_url"))
    return f"| {emoji} | {entry['id']} | {prio} | {title} | {issue} |"


def render_detail(entry):
    """Render a detail section for an entry."""
    lines = [f"### {entry['id']}", f"**{entry['title']}**"]
    link = issue_link(entry.get("issue_url"))
    if link:
        lines.append(f"Issue: {link}")
    lines.append(entry["description"])
    return "\n".join(lines)


def render_section(title, entries):
    """Render a full section (table + details)."""
    by_prio = sorted(entries, key=lambda e: PRIORITIES[e["priority"]]["sort"], reverse=True)
    rows = [render_row(e) for e in by_prio]
    details = [render_detail(e) for e in by_prio]
    return "\n".join([f"## {title}", "", TABLE_HEADER, TABLE_SEPARATOR] + rows) + "\n\n" + "\n\n".join(details)


if __name__ == "__main__":
    header = HEADER_PATH.read_text().rstrip()
    entries = load()
    open_entries = [e for e in entries if not e["done"]]
    done_entries = [e for e in entries if e["done"]]

    readme = "\n\n".join([
        header,
        render_section("Open", open_entries),
        render_section("Done", done_entries),
    ]) + "\n"

    README_PATH.write_text(readme)
    print("Generated README.md")
