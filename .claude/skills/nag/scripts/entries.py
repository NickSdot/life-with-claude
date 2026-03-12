#!/usr/bin/env python3
"""Shared helpers for reading, writing, and querying entries.json."""

import json
import subprocess
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import ENTRIES_PATH, SCRIPTS_DIR


def load():
    """Load entries from entries.json."""
    if not ENTRIES_PATH.exists():
        return []
    data = json.loads(ENTRIES_PATH.read_text())
    return data.get("entries", [])


def find(entries, entry_id):
    """Find an entry by ID (case-insensitive). Returns (index, entry) or (None, None)."""
    entry_id = entry_id.upper()
    for i, e in enumerate(entries):
        if e["id"].upper() == entry_id:
            return i, e
    return None, None


def load_and_find(entry_id):
    """Load entries and find one by ID. Exits with error if not found."""
    entries = load()
    idx, entry = find(entries, entry_id.upper())
    if idx is None:
        print(f"Entry {entry_id} not found")
        sys.exit(1)
    return entries, idx, entry


def save_and_regenerate(entries):
    """Save entries to JSON and regenerate README."""
    ENTRIES_PATH.write_text(json.dumps({"entries": entries}, indent=2) + "\n")
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "generate-readme.py")],
        check=True
    )
