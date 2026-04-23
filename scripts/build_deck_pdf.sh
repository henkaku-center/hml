#!/usr/bin/env bash
# Render a Quarto RevealJS deck to a per-slide-numbered PDF and stage it at
# course/weekNN_*/slides/sp26/weekNN.pdf so the landing page schedule picks
# it up automatically.
#
# Usage: scripts/build_deck_pdf.sh course/weekNN_slug/weekN-slides.qmd
# Requires decktape (npm install -g decktape).

set -euo pipefail

QMD="${1:?usage: build_deck_pdf.sh <path/to/weekN-slides.qmd>}"
QMD_ABS="$(realpath "$QMD")"
QMD_DIR="$(dirname "$QMD_ABS")"
QMD_STEM="$(basename "$QMD_ABS" .qmd)"
HTML_PATH="$QMD_DIR/$QMD_STEM.html"
REPO_ROOT="$(cd "$QMD_DIR/../.." && pwd)"

# Extract the week number from the parent dir: weekNN_slug -> NN
WEEK_DIR="$(basename "$(dirname "$QMD_ABS")")"
WEEK_NUM="${WEEK_DIR#week}"
WEEK_NUM="${WEEK_NUM%%_*}"
OUT="$QMD_DIR/slides/sp26/week${WEEK_NUM}.pdf"

STAGE="$HOME/qa-previews/${QMD_STEM}-deckpdf"
rm -rf "$STAGE" && mkdir -p "$STAGE"

# 1. Render HTML if missing or stale.
if [[ ! -f "$HTML_PATH" || "$QMD_ABS" -nt "$HTML_PATH" ]]; then
    echo "[build] rendering HTML via quarto..."
    (cd "$REPO_ROOT" && quarto render "$QMD_ABS" --to revealjs >/dev/null 2>&1)
fi

# 2. Stage dependencies so decktape can resolve relative paths.
cp "$HTML_PATH" "$STAGE/"
[[ -d "$QMD_DIR/${QMD_STEM}_files" ]] && cp -r "$QMD_DIR/${QMD_STEM}_files" "$STAGE/"
if [[ -d "$REPO_ROOT/sds-reveal" ]]; then
    THEME_DIR="$STAGE/${QMD_STEM}_files/libs/revealjs/dist/theme"
    if [[ -d "$THEME_DIR" ]]; then
        cp "$REPO_ROOT/sds-reveal/sds_frame.png" "$THEME_DIR/" 2>/dev/null || true
        cp "$REPO_ROOT/sds-reveal/sds_wordmark.png" "$THEME_DIR/" 2>/dev/null || true
    fi
    sed -i 's|\.\./\.\./sds-reveal/|./sds-reveal/|g' "$STAGE/$QMD_STEM.html"
    cp -r "$REPO_ROOT/sds-reveal" "$STAGE/"
fi
[[ -d "$QMD_DIR/images" ]] && cp -r "$QMD_DIR/images" "$STAGE/"

# 3. Render to PDF via decktape (native 960x540, KaTeX / MathJax honored).
echo "[build] rendering PDF via decktape..."
decktape reveal "file://$STAGE/$QMD_STEM.html" "$STAGE/deck.pdf" >/dev/null 2>&1

# 4. Move the PDF into the expected output path.
mkdir -p "$(dirname "$OUT")"
cp "$STAGE/deck.pdf" "$OUT"
echo "[build] wrote $OUT ($(du -h "$OUT" | cut -f1))"
