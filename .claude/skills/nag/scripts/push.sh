#!/bin/bash
# Push changes to the wishlist repo.
# Usage: push.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/constants.sh"

cd "$LWC_REPO"

git push
echo "Pushed to remote"
