#!/usr/bin/env bash
# Build the course website, then encrypt the readings page and the PDFs
# behind a single class-wide password (SP26 uses one password, no rotation).
#
# Usage:
#   docs/_build_site.sh                  # reads password from READINGS_PW env
#   READINGS_PW=foo docs/_build_site.sh
#
# Writes to docs/ — commit afterwards.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS="$REPO_ROOT/docs"

# 1. Render the static site from sources.
echo "[build] rendering HTML from source..."
python3 "$DOCS/_build.py"

# 2. Look up the password. Prefer the env var; fall back to a gitignored
#    secret file; error out if neither is set.
if [[ -z "${READINGS_PW:-}" ]]; then
    if [[ -f "$DOCS/.readings_pw" ]]; then
        READINGS_PW="$(cat "$DOCS/.readings_pw")"
    else
        echo "[build] ERROR: set READINGS_PW env var or create docs/.readings_pw" >&2
        echo "        (docs/.readings_pw should be gitignored — see .gitignore)" >&2
        exit 1
    fi
fi

# 3. Encrypt the readings page + the game-plan page in-place. staticrypt
#    writes the encrypted HTML to the same file by default when --directory
#    matches the input's directory.
echo "[build] encrypting readings.html..."
cd "$DOCS"
staticrypt readings.html \
    -p "$READINGS_PW" \
    --short \
    --remember 180 \
    --template-title "Readings — SP26" \
    --template-instructions "Enter the SP26 class password (pinned in Slack #hml-2026). Tick \"Remember me\" to stay unlocked for the semester." \
    --template-button "Unlock" \
    -d . >/dev/null

# staticrypt wrote a .staticrypt.json config — do NOT commit that either
# (it contains the password salt). It's gitignored via docs/.gitignore below
# if present, or the root .gitignore.

echo "[build] done. Commit docs/ to publish."
