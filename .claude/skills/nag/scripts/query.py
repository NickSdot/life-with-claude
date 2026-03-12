#!/usr/bin/env python3
"""Query entries.json for wishlist data."""

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import CATEGORIES, normalize_category
from entries import load, find


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
    """Get the next available ID for a category."""
    category = normalize_category(category)
    prefix = CATEGORIES[category]["prefix"]
    entries = load()

    existing_ids = [
        int(e["id"][1:]) for e in entries
        if e["id"].startswith(prefix)
    ]

    next_num = max(existing_ids, default=0) + 1
    return f"{prefix}{next_num:03d}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: query.py <command> [args]")
        print("Commands: stats, list, search <query>, next-id <category>, get <id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "stats":
        entries = load()
        open_entries = [e for e in entries if not e["done"]]
        stats = {
            cat: sum(1 for e in open_entries if e["category"] == cat)
            for cat in CATEGORIES
        }
        print(json.dumps(stats))

    elif command == "list":
        print(json.dumps(load(), indent=2))

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: query.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        matches = fuzzy_search(query, load())
        print(json.dumps(matches, indent=2))

    elif command == "next-id":
        if len(sys.argv) < 3:
            print("Usage: query.py next-id <category>")
            sys.exit(1)
        try:
            print(get_next_id(sys.argv[2]))
        except KeyError:
            print(f"Invalid category: {sys.argv[2]}")
            sys.exit(1)

    elif command == "get":
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
        print(f"Unknown command: {command}")
        sys.exit(1)
