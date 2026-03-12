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


def save(entries):
    """Save entries to entries.json."""
    ENTRIES_PATH.write_text(json.dumps({"entries": entries}, indent=2) + "\n")


def find(entries, entry_id):
    """Find an entry by ID (case-insensitive). Returns (index, entry) or (None, None)."""
    entry_id = entry_id.upper()
    for i, e in enumerate(entries):
        if e["id"].upper() == entry_id:
            return i, e
    return None, None


def regenerate_readme():
    """Call generate-readme.py to rebuild README.md from JSON."""
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "generate-readme.py")],
        check=True
    )
