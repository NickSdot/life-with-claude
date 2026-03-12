#!/usr/bin/env python3
"""Generate README.md from entries.json and readme-header.md."""

import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH, HEADER_PATH, CATEGORIES, PRIORITIES
from entries import load

TABLE_HEADER = "| Type | ID | Prio | Title | Issue |"
TABLE_SEPARATOR = "|------|----|----|-------|-------|"


def issue_num_from_url(url):
    """Extract issue number from GitHub URL."""
    match = re.search(r'/issues/(\d+)', url)
    return match.group(1) if match else None


def render_row(entry):
    """Render a single table row."""
    emoji = CATEGORIES[entry["category"]]["emoji"]
    prio = PRIORITIES[entry["priority"]]["emoji"]
    anchor = entry["id"].lower()
    title_link = f"[{entry['title']}](#{anchor})"

    issue_cell = ""
    if entry.get("issue_url"):
        num = issue_num_from_url(entry["issue_url"])
        if num:
            issue_cell = f"[#{num}]({entry['issue_url']})"

    return f"| {emoji} | {entry['id']} | {prio} | {title_link} | {issue_cell} |"


def render_detail(entry):
    """Render a detail section for an entry."""
    lines = [f"### {entry['id']}", f"**{entry['title']}**"]

    if entry.get("issue_url"):
        num = issue_num_from_url(entry["issue_url"])
        if num:
            lines.append(f"Issue: [#{num}]({entry['issue_url']})")

    lines.append(entry["description"])
    return "\n".join(lines)


def render_section(title, entries):
    """Render a full section (table + details)."""
    sorted_entries = sorted(
        entries,
        key=lambda e: PRIORITIES[e["priority"]]["sort"],
        reverse=True
    )

    lines = [f"## {title}", "", TABLE_HEADER, TABLE_SEPARATOR]
    for entry in sorted_entries:
        lines.append(render_row(entry))

    lines.append("")
    for entry in sorted_entries:
        lines.append(render_detail(entry))

    return "\n".join(lines)


def generate():
    """Generate README.md from header + entries."""
    header = HEADER_PATH.read_text().rstrip()
    entries = load()

    open_entries = [e for e in entries if not e["done"]]
    done_entries = [e for e in entries if e["done"]]

    parts = [header, ""]
    parts.append(render_section("Open", open_entries))
    parts.append("")
    parts.append(render_section("Done", done_entries))
    parts.append("")

    README_PATH.write_text("\n".join(parts))


if __name__ == "__main__":
    generate()
    print("Generated README.md")
