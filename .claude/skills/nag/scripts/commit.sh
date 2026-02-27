#!/bin/bash
# Commit changes to the wishlist repo (no push).
# Usage: commit.sh "commit message" [files...]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/constants.sh"

MESSAGE="$1"
shift

if [ -z "$MESSAGE" ]; then
    echo "Usage: commit.sh \"commit message\" [files...]"
    exit 1
fi

cd "$LWC_REPO"

# Add specified files or README.md by default
if [ $# -eq 0 ]; then
    git add README.md
else
    git add "$@"
fi

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

git commit -m "$MESSAGE"
echo "Committed: $MESSAGE"
