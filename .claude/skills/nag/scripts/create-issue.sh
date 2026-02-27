#!/bin/bash
# Create a GitHub issue for a wishlist entry.
# Usage: create-issue.sh <entry-id> <title> <body-file>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/constants.sh"

ENTRY_ID="$1"
TITLE="$2"
BODY_FILE="$3"

if [ -z "$ENTRY_ID" ] || [ -z "$TITLE" ] || [ -z "$BODY_FILE" ]; then
    echo "Usage: create-issue.sh <entry-id> <title> <body-file>"
    exit 1
fi

# Create the issue
ISSUE_URL=$(gh issue create \
    --repo "$LWC_CLAUDE_CODE_REPO" \
    --title "$ENTRY_ID: $TITLE" \
    --body-file "$BODY_FILE")

echo "Created issue: $ISSUE_URL"
echo "ISSUE_URL:$ISSUE_URL"
