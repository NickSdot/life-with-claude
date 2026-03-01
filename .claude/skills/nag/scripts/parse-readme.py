#!/usr/bin/env python3
"""Parse README.md and extract wishlist entries with fuzzy search support."""

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import README_PATH, ID_PREFIX, normalize_category


def parse_readme():
    """Parse README.md and extract all entries."""
    if not README_PATH.exists():
        return {"entries": [], "stats": {"bugs": 0, "flaws": 0, "wishes": 0}}

    content = README_PATH.read_text()
    entries = []

    # Parse tables for each category
    categories = {
        "🐛 Bugs": "bug",
        "🤔 Flaws": "flaw",
        "💫 Wishes": "wish"
    }

    for section_title, category in categories.items():
        section_pattern = rf"## {re.escape(section_title)}\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)*)"
        match = re.search(section_pattern, content)
        if match:
            table_rows = match.group(1)
            # Pattern captures: done (optional checkbox or empty), id, priority, title, and optional issue link
            row_pattern = r"\|\s*(\[([x ])\]|)\s*\| ([BFW]\d+) \| (⭐+) \| \[([^\]]+)\]\(#[^\)]+\) \| (?:\[#(\d+)\]\(([^\)]+)\))? \|"
            for row_match in re.finditer(row_pattern, table_rows):
                done = row_match.group(2) == "x"  # group(2) is the x or space inside brackets, None if empty cell
                entry_id = row_match.group(3)
                priority = row_match.group(4)
                title = row_match.group(5)
                issue_num = row_match.group(6)  # May be None
                issue_url = row_match.group(7)  # May be None

                desc_pattern = rf"### {entry_id}\n\*\*[^\*]+\*\*\n(?:Issue: [^\n]+\n)?(.+?)(?=\n###|\n---|\Z)"
                desc_match = re.search(desc_pattern, content, re.DOTALL)
                description = desc_match.group(1).strip() if desc_match else ""

                entry = {
                    "id": entry_id,
                    "category": category,
                    "priority": priority,
                    "priority_num": len(priority),
                    "title": title,
                    "description": description,
                    "done": done
                }
                if issue_url:
                    entry["issue"] = {"number": int(issue_num), "url": issue_url}

                entries.append(entry)

    stats = {
        "bugs": sum(1 for e in entries if e["category"] == "bug" and not e["done"]),
        "flaws": sum(1 for e in entries if e["category"] == "flaw" and not e["done"]),
        "wishes": sum(1 for e in entries if e["category"] == "wish" and not e["done"])
    }

    return {"entries": entries, "stats": stats}


def fuzzy_search(query, entries):
    """Find entries matching a query (ID or fuzzy text match)."""
    query = query.strip()

    if re.match(r'^[BFW]\d+$', query, re.IGNORECASE):
        query_upper = query.upper()
        return [e for e in entries if e["id"].upper() == query_upper]

    results = []
    query_lower = query.lower()

    for entry in entries:
        title_lower = entry["title"].lower()
        desc_lower = entry["description"].lower()

        if query_lower in title_lower or query_lower in desc_lower:
            title_score = SequenceMatcher(None, query_lower, title_lower).ratio()
            desc_score = SequenceMatcher(None, query_lower, desc_lower).ratio()
            score = max(title_score, desc_score)
            results.append((entry, score + 0.5))
            continue

        title_score = SequenceMatcher(None, query_lower, title_lower).ratio()
        desc_score = SequenceMatcher(None, query_lower, desc_lower).ratio()
        score = max(title_score, desc_score)

        if score > 0.3:
            results.append((entry, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]


def get_next_id(category):
    """Get the next available ID for a category. Accepts raw questionnaire answers."""
    category = normalize_category(category)
    data = parse_readme()
    prefix = ID_PREFIX[category]

    existing_ids = [
        int(e["id"][1:]) for e in data["entries"]
        if e["id"].startswith(prefix)
    ]

    next_num = max(existing_ids, default=0) + 1
    return f"{prefix}{next_num:03d}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse-readme.py <command> [args]")
        print("Commands: stats, list, search <query>, next-id <category>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "stats":
        data = parse_readme()
        print(json.dumps(data["stats"]))

    elif command == "list":
        data = parse_readme()
        print(json.dumps(data["entries"], indent=2))

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: parse-readme.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        data = parse_readme()
        matches = fuzzy_search(query, data["entries"])
        print(json.dumps(matches, indent=2))

    elif command == "next-id":
        if len(sys.argv) < 3:
            print("Usage: parse-readme.py next-id <category>")
            sys.exit(1)
        category = sys.argv[2]
        try:
            print(get_next_id(category))
        except KeyError:
            print(f"Invalid category: {category}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
