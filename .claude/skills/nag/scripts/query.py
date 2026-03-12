#!/usr/bin/env python3
"""Query entries.json for wishlist data."""

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import CATEGORIES, normalize_category
from entries import load, find


def fuzzy_search(query, entries):
    """Find entries matching a query (ID or fuzzy text match)."""
    query = query.strip()

    if re.match(r'^[BFW]\d+$', query, re.IGNORECASE):
        return [e for e in entries if e["id"].upper() == query.upper()]

    results = []
    query_lower = query.lower()

    for entry in entries:
        title_score = SequenceMatcher(None, query_lower, entry["title"].lower()).ratio()
        desc_score = SequenceMatcher(None, query_lower, entry["description"].lower()).ratio()
        score = max(title_score, desc_score)

        # Boost score if query is a substring
        if query_lower in entry["title"].lower() or query_lower in entry["description"].lower():
            score += 0.5

        if score > 0.3:
            results.append((entry, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]


def get_next_id(category):
    """Get the next available ID for a category."""
    category = normalize_category(category)
    prefix = CATEGORIES[category]["prefix"]
    nums = [int(e["id"][1:]) for e in load() if e["id"].startswith(prefix)]
    return f"{prefix}{max(nums, default=0) + 1:03d}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: query.py <command> [args]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "stats":
        open_entries = [e for e in load() if not e["done"]]
        print(json.dumps({cat: sum(1 for e in open_entries if e["category"] == cat) for cat in CATEGORIES}))

    elif cmd == "list":
        print(json.dumps(load(), indent=2))

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: query.py search <query>")
            sys.exit(1)
        print(json.dumps(fuzzy_search(" ".join(sys.argv[2:]), load()), indent=2))

    elif cmd == "next-id":
        if len(sys.argv) < 3:
            print("Usage: query.py next-id <category>")
            sys.exit(1)
        try:
            print(get_next_id(sys.argv[2]))
        except KeyError:
            print(f"Invalid category: {sys.argv[2]}")
            sys.exit(1)

    elif cmd == "get":
        if len(sys.argv) < 3:
            print("Usage: query.py get <id>")
            sys.exit(1)
        _, entry = find(load(), sys.argv[2])
        if entry:
            print(json.dumps(entry, indent=2))
        else:
            print(f"Entry {sys.argv[2]} not found")
            sys.exit(1)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
