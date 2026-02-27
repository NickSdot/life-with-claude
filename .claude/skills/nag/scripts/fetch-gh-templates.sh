#!/bin/bash
# Fetch GitHub issue templates from claude-code repo.
# Run periodically to keep templates current.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/constants.sh"

GH_TEMPLATES_DIR="$LWC_GH_TEMPLATES_DIR"
LAST_FETCH_FILE="$GH_TEMPLATES_DIR/.last_fetch"

# Check if we fetched today already
if [ -f "$LAST_FETCH_FILE" ]; then
    LAST_FETCH=$(cat "$LAST_FETCH_FILE")
    TODAY=$(date +%Y-%m-%d)
    if [ "$LAST_FETCH" = "$TODAY" ]; then
        echo "Templates already fetched today"
        exit 0
    fi
fi

mkdir -p "$GH_TEMPLATES_DIR"

# Compute hash of current templates
hash_before=""
if [ -d "$GH_TEMPLATES_DIR" ]; then
    hash_before=$(cat "$GH_TEMPLATES_DIR"/*.yml 2>/dev/null | shasum -a 256 | cut -d' ' -f1)
fi

# Fetch templates from claude-code repo
echo "Fetching GitHub issue templates..."

for template in bug_report.yml feature_request.yml model_behavior.yml; do
    curl -sL "https://raw.githubusercontent.com/$LWC_CLAUDE_CODE_REPO/main/.github/ISSUE_TEMPLATE/$template" \
        -o "$GH_TEMPLATES_DIR/$template" 2>/dev/null || true
done

# Record fetch date
date +%Y-%m-%d > "$LAST_FETCH_FILE"

# Check if templates changed
hash_after=$(cat "$GH_TEMPLATES_DIR"/*.yml 2>/dev/null | shasum -a 256 | cut -d' ' -f1)

if [ "$hash_before" != "$hash_after" ]; then
    echo "TEMPLATES_CHANGED"
else
    echo "Templates unchanged"
fi
