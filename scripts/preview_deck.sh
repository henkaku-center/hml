#!/usr/bin/env bash
# Render a Quarto RevealJS deck to per-slide PNGs for visual QA.
#
# Usage: scripts/preview_deck.sh course/weekNN_foo/weekN-slides.qmd
#
# Output: ~/qa-previews/weekN/slide*.png
#
# Snap-confined chromium on WSL can't read files outside $HOME, so we stage
# the rendered HTML + sds-reveal assets into ~/qa-previews/weekN/ before
# rasterizing. pdftoppm (from poppler-utils) converts the Chromium-printed
# PDF into per-slide PNGs at 150 DPI.

set -euo pipefail

QMD="${1:?usage: preview_deck.sh <path/to/weekN-slides.qmd>}"
QMD_ABS="$(realpath "$QMD")"
QMD_DIR="$(dirname "$QMD_ABS")"
QMD_STEM="$(basename "$QMD_ABS" .qmd)"
HTML_PATH="$QMD_DIR/$QMD_STEM.html"
REPO_ROOT="$(cd "$QMD_DIR/../.." && pwd)"
STAGE="$HOME/qa-previews/$QMD_STEM"
PDF_PATH="$STAGE/deck.pdf"

# 1. Render HTML if missing or older than the .qmd.
if [[ ! -f "$HTML_PATH" || "$QMD_ABS" -nt "$HTML_PATH" ]]; then
    echo "[preview] rendering HTML via quarto..."
    (cd "$REPO_ROOT" && quarto render "$QMD_ABS" --to revealjs >/dev/null 2>&1)
fi

# 2. Stage deck + theme assets into a snap-accessible HOME location.
echo "[preview] staging into $STAGE"
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp "$HTML_PATH" "$STAGE/"
if [[ -d "$QMD_DIR/${QMD_STEM}_files" ]]; then
    cp -r "$QMD_DIR/${QMD_STEM}_files" "$STAGE/"
fi
if [[ -d "$REPO_ROOT/sds-reveal" ]]; then
    # The compiled theme CSS references url("sds_frame.png") relative to the
    # CSS file's location (inside _files/libs/revealjs/dist/theme/). Copy the
    # PNGs in there too so they resolve.
    THEME_DIR="$STAGE/${QMD_STEM}_files/libs/revealjs/dist/theme"
    if [[ -d "$THEME_DIR" ]]; then
        cp "$REPO_ROOT/sds-reveal/sds_frame.png" "$THEME_DIR/" 2>/dev/null || true
        cp "$REPO_ROOT/sds-reveal/sds_wordmark.png" "$THEME_DIR/" 2>/dev/null || true
    fi
    # Also stage the sds-reveal dir at the expected relative depth so
    # background-image attrs in the .qmd (../../sds-reveal/sds_frame.png)
    # resolve. From $STAGE/foo.html, ../../sds-reveal would be $HOME/sds-reveal.
    # Instead, place a copy at $STAGE/../../sds-reveal relative to … no,
    # simpler: replace the relative path in the HTML with something local.
    sed -i 's|\.\./\.\./sds-reveal/|./sds-reveal/|g' "$STAGE/$QMD_STEM.html"
    cp -r "$REPO_ROOT/sds-reveal" "$STAGE/"
fi

# Also copy any images/ referenced from the .qmd's own dir (e.g. binomial_pmf.png).
if [[ -d "$QMD_DIR/images" ]]; then
    cp -r "$QMD_DIR/images" "$STAGE/"
fi

# 3. Render PDF. Prefer decktape — it drives a bundled Chromium via CDP,
# honors RevealJS slide dimensions natively (960×540 for a 16:9 deck), and
# handles KaTeX / MathJax without the --headless flag / --virtual-time-budget
# fights that google-chrome's --print-to-pdf requires. Fall back to
# google-chrome --headless=old if decktape isn't installed.
if command -v decktape >/dev/null 2>&1; then
    echo "[preview] rendering PDF via decktape..."
    decktape reveal "file://$STAGE/$QMD_STEM.html" "$PDF_PATH" >/dev/null 2>&1 || true
else
    if command -v google-chrome >/dev/null 2>&1; then
        BROWSER=google-chrome
    elif command -v chromium >/dev/null 2>&1; then
        BROWSER=chromium
    else
        echo "[preview] ERROR: need decktape, google-chrome, or chromium" >&2
        exit 1
    fi
    echo "[preview] rendering PDF via $BROWSER (decktape not installed)..."
    # --headless=old is required for chrome ≥ 124 (new mode ignores RevealJS's
    # @page rule). --hide-scrollbars prevents a 1-page truncation bug.
    # --virtual-time-budget=90000 gives math libs time to load. KaTeX may
    # still break print-pdf mode — install decktape instead if so.
    "$BROWSER" --headless=old --disable-gpu --no-sandbox --hide-scrollbars \
        --print-to-pdf="$PDF_PATH" --print-to-pdf-no-header \
        --virtual-time-budget=90000 \
        "file://$STAGE/$QMD_STEM.html?print-pdf" >/dev/null 2>&1 || true
fi

if [[ ! -s "$PDF_PATH" ]]; then
    echo "[preview] ERROR: renderer produced no PDF" >&2
    exit 1
fi

# 4. Rasterize to per-slide PNGs.
echo "[preview] rasterizing PDF to PNGs..."
rm -f "$STAGE"/slide*.png
pdftoppm -png -r 150 "$PDF_PATH" "$STAGE/slide" >/dev/null

COUNT=$(ls "$STAGE"/slide*.png 2>/dev/null | wc -l)
echo "[preview] $COUNT slide PNGs written to $STAGE"
