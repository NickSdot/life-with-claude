#!/bin/bash
# Create a GitHub issue for a wishlist entry.
# Usage: create-issue.sh <template> <title> <body-file>
# Template: bug, model, or feature (determines title prefix)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/constants.sh"

TEMPLATE="$1"
TITLE="$2"
BODY_FILE="$3"

if [ -z "$TEMPLATE" ] || [ -z "$TITLE" ] || [ -z "$BODY_FILE" ]; then
    echo "Usage: create-issue.sh <template> <title> <body-file>"
    echo "Template: bug, model, or feature"
    exit 1
fi

# Map template to title prefix (matching GitHub YAML templates)
case "$TEMPLATE" in
    bug)     PREFIX="[BUG]" ;;
    model)   PREFIX="[MODEL]" ;;
    feature) PREFIX="[FEATURE]" ;;
    *)       PREFIX="" ;;
esac

# Create the issue with proper prefix
ISSUE_URL=$(gh issue create \
    --repo "$LWC_CLAUDE_CODE_REPO" \
    --title "$PREFIX $TITLE" \
    --body-file "$BODY_FILE")

echo "Created issue: $ISSUE_URL"
echo "ISSUE_URL:$ISSUE_URL"
