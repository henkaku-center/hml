# Slide visual-QA method (handoff from the APS-I `lecture-plans` agent)

This is a method-transfer doc, not a replacement for `CLAUDE.md`. The existing
"Slide visual-QA loop" section in `CLAUDE.md` covers PPTX-preview reading via
LibreOffice → `pdftoppm`. That works for the python-pptx pipeline. Once a week
moves to Quarto/RevealJS (as Week 2 has), **a PPTX-preview pass alone is not
enough** — it misses an entire class of layout defects that only appear in the
HTML deck students actually see.

The method below was developed iteratively while building the APS-I Week 3
deck. It converged to "0 flagged slides" after the previous ad-hoc PNG-only
approach had silently shipped ~40 floating slides.

## Why a PPTX-only audit is insufficient for RevealJS decks

RevealJS and LibreOffice render `.qmd` content differently. The
`center: true` setting (default in `_quarto.yml`), `.smaller` classes, KaTeX
math, and `r-stretch` all behave inconsistently between the two engines.

The failure modes you must hunt for:

- **OVERFLOW** — content past slide bounds, clipped, or triggering Reveal's
  auto-shrink-to-fit. Visible in both engines. Easy to spot in PNGs.
- **FLOATING** — short content block symmetrically padded by `center: true`.
  Top gap >15% AND bottom gap >15%, fill <55% of stage height.
  **Invisible in PPTX previews.** Only visible in HTML.
- **PUSHED-DOWN** — content sits below the middle. Rare; usually a misplaced
  div or stray empty paragraph.
- **COLUMN-THIN** — a two-column slide where one column (almost always the
  text column beside a tall figure) is sparse. **The whole-slide fill looks
  fine** because the figure column sets the bounding box — so this is
  invisible to both a PPTX preview *and* a naive HTML audit that measures one
  box across the whole slide. The fixed audit measures each column on its
  own; see "Two-column slides" below.

A PPTX-only check catches OVERFLOW reliably and misses
FLOATING/PUSHED-DOWN/COLUMN-THIN entirely. Don't trust an "all clean" report
based only on LibreOffice rasterizations.

## The audit script

In `lecture-plans` there's a script at `scripts/audit_slide_fill.js` that
headless-loads the rendered HTML with Puppeteer, measures the content
bounding-box per slide, and flags each one. You can copy it across:

```bash
cp ~/work/aps1_versions/lecture-plans/scripts/audit_slide_fill.js \
   ~/work/hummachlearn/spring2026/scripts/
```

Then edit the top of the file to point at your deck — change `DECK` and
`OUT_DIR` paths (they're hardcoded to the lecture-plans week3 deck).

Usage:

```bash
node scripts/audit_slide_fill.js --threshold 75              # nominal viewport only
node scripts/audit_slide_fill.js --threshold 75 --all-sizes  # 8 viewports
```

`--all-sizes` tests nominal (1050×700) plus ±50px wobble and several 16:9
ratios (720p, 1080p, laptop). Catches "works at exactly the design size, breaks
at a slightly different aspect ratio" bugs.

### What the script measures (the trap to avoid)

RevealJS layout: `.reveal .slides` is the stage; `section.present` is
positioned absolutely within the stage. With `center: true`, the section is
sized to its content and vertically centered.

- `section.height / stage.height` catches "center:true floating" (section is
  short, stage is full-height, ratio is small).
- But with `center: false`, the section fills the stage and inner content sits
  at the top — `section.height ≈ stage.height` always. You must *also* measure
  the inner-content bbox.

The script takes the MIN of section-fill and inner-content-fill so both modes
are caught. An earlier version measured (content / section), which is circular
and always reports ~100% fill — it shipped a clean report on visibly broken
slides. **If you ever modify the script, verify it against a slide you've
personally eyeballed as broken before trusting it.**

## Two-column slides

Slides built with Quarto's `:::: {.columns}` / `::: {.column}` divs (a figure
beside a text column is the common case) need their own check. The whole-slide
inner-content box spans **both** columns, so it is dominated by whichever
column is taller — almost always the figure. A sparse text column beside a
full-height figure is therefore **invisible to a whole-slide measurement**:
the slide reports ~90% fill while the text column is at 30%.

This was a real gap. The four T&G "posterior-weighted vote" slides audited at
89–93% whole-slide fill while their text columns were genuinely at 20–46%.

**The audit now measures each `.columns > .column` separately** — its content
fill *and* its vertical placement within the row — and reports them as
`(col=NN% skew=NN)` in the report line. A column counts only if it is wider
than 12% of the stage (sliver columns are layout, not content) and has real
content. Two per-column quantities, two flags:

- `columnFill` — the thinnest column's content height as a % of the stage.
- `columnSkew` — how far the worst column's content *center* sits from the
  row's center, as a % of the row span. 0 = every column vertically centered
  in the row; a top-jammed column scores high.

- **COLUMN-THIN** — whole-slide fill is fine, but the thinnest column is below
  42%. The column is genuinely sparse (a few words floating beside a
  full-height figure) and should be laid out better. Whole-slide fill is *not*
  dragged down by a thin column — otherwise a legitimately figure-heavy slide
  would be mislabeled `SHORT`.
- **COLUMN-SKEW** — a column's content is not vertically centered in its row
  (`columnSkew` > 34): it hugs the top with a void below, even though it has
  enough content. Fix by adding `.v-center` to the `.columns` div (see below).

The 42% column threshold is well below the 75% whole-slide threshold: a text
column legitimately runs shorter than a figure beside it, so the flag fires
only for a *genuinely* sparse column. It was calibrated against real slides —
genuinely-bad text columns (a few floating words) measured 20–38%; substantive
3–5 element text panels beside a chart measured 44–60%; 42% cleanly separates
them. A real multi-element text panel that simply isn't as tall as the figure
beside it is fine and won't flag.

**Remediation for COLUMN-THIN** (in rough order of preference):

1. **Move content into the thin column.** A figure caption, the governing
   equation, the symbol definitions, or a "what to notice" line often live
   better beside the figure than under it or in speaker notes.
2. **Rebalance the split.** A 60/40 figure/text split with a sparse text side
   often reads better at 52/48 or 50/50 — give the text room to breathe
   instead of forcing a narrow ragged column.
3. **Let the figure carry more.** Widen the figure to ~70% and make the text a
   short single caption-style line beneath it (one column, not two) — for
   slides where the text genuinely is just a caption.
4. **Vertically center the short column.** Wrapping the text column's content
   so it centers against the figure removes the "text jammed at the top,
   void below" look even when the text is genuinely brief.

Do NOT "fix" COLUMN-THIN by shrinking the figure until the boxes match — that
usually makes the figure too small to read. Balance by *adding* to the thin
side or *re-proportioning*, not by degrading the strong side.

## The five-tier sizing system

A single global body font-size can't satisfy a deck with mixed content
density: tighten it and you create floating slides; loosen it and dense slides
overflow. The `lecture-plans/sds-reveal/sds.scss` file defines five opt-in
tiers; each slide gets exactly one (or none = default).

| Class          | body / h2     | When to use                                        |
|----------------|---------------|----------------------------------------------------|
| `.smaller`     | 0.78em / 1.05em | Dense slides — long tables, equation-heavy, many bullets |
| (default)      | 0.82em / 1.20em | Workhorse for typical mid-density content          |
| `.midbig`      | 0.92em / 1.25em | Overflows at `.bigger`, floats at default; 3-row tables + takeaway |
| `.bigger`      | 1.00em / 1.35em | Sparse content (1 paragraph + 3 short bullets)     |
| `.biggerplus`  | 1.12em / 1.45em | Very sparse (2-3 short bullets + takeaway)         |
| `.biggest`     | 1.25em / 1.65em | Extremely sparse (3-4 short lines, instruction slides) |

The H&ML `sds-reveal/sds.scss` is byte-identical to lecture-plans' copy as of
the last cross-repo sync, so these classes already exist on your side. If they
don't (i.e. the H&ML SCSS predates the five-tier system), grab the current
`sds.scss` from `lecture-plans/sds-reveal/`.

Apply a class in the qmd by appending it to the slide title:

```markdown
## English title · 日本語タイトル {.bigger}
```

For bilingual titles wrapped in spans, the class goes at the very end:

```markdown
## [English]{.lang-en}[日本語]{.lang-ja} {.smaller}
```

Agenda slides need their own rule — see `.agenda li` in the SCSS. Don't try
to handle dense agendas with `.smaller`; use the dedicated `.agenda.dense`
modifier instead.

## The iterative loop

This converged to zero flagged slides on the APS-I Week 3 deck. Each cycle is
~2-3 minutes.

1. **Render:** `quarto render weekN-slides.qmd`. Watch for non-zero exit;
   `\textcolor` math warnings are pre-existing and ignorable.
2. **Audit:** `node scripts/audit_slide_fill.js --threshold 75`. Records
   per-slide fill%, top-gap%, bottom-gap%, per-column fill + skew, and a flag
   (OK / OVERFLOW / FLOATING / PUSHED-DOWN / COLUMN-THIN / COLUMN-SKEW / SHORT
   / SKIP-FRAMED). Writes JSON for later diffs.
3. **Classify each flagged slide** by its current sizing class (`grep` the
   `## Title {.xxx}` in the qmd):
   - OVERFLOW + already `.smaller` → trim content (no smaller tier exists).
   - OVERFLOW + `.bigger`/`.midbig` → downgrade one tier.
   - OVERFLOW + no class → try `.smaller` first; if still overflows, trim.
   - FLOATING + `.smaller` → remove `.smaller` (verify it fits at default).
   - FLOATING + no class → try `.midbig`; then `.bigger`; then `.biggerplus`.
   - FLOATING + `.bigger` → `.biggerplus` or `.biggest`; if those now overflow,
     trim content.
   - COLUMN-THIN / COLUMN-SKEW → **not a sizing-tier fix.** COLUMN-THIN: the
     thin column needs more content, a re-proportioned split, or a merge to
     one column. COLUMN-SKEW: the column has enough content but is top-jammed
     — add `.v-center` to the `.columns` div. See the "Two-column slides"
     section for the full remediation order. A tier bump won't help — the
     slide as a whole is already fine.
4. **Re-render, re-audit.** Loop until flagged = 0.
5. **All-sizes sanity check:** `node scripts/audit_slide_fill.js --all-sizes`.
   Most failures are size-invariant, but the wobble has caught real cases
   once.
6. **Visual spot-check** for the riskiest 3-5 slides — the audit measures
   bboxes, but the human eye catches line-wrap awkwardness and table-border
   clipping that bbox math doesn't:

   ```bash
   decktape --size 1050x700 --slides N reveal weekN-slides.html /tmp/slideN.pdf
   pdftoppm -r 150 /tmp/slideN.pdf /tmp/slideN -png
   ```

   Then `Read` the PNG.

## When the loop oscillates

Some slides cycle between "this tier overflows, the next-smaller tier floats."
That means trim content (preferred) or accept ~70% fill (acceptable
mid-range). Don't keep nudging.

Content-trim patterns that reliably work:

- Merge two bullets into one inline statement when they make the same point.
- Move long parenthetical context to speaker notes (`::: {.notes}`).
- Collapse "header line + colon + bullets" into one inline sentence.
- Drop "we already saw this" callback lines — students remember, and the
  speaker notes can prompt the instructor instead.
- For tables, combine adjacent rows with overlapping categories (e.g. one
  "opt-out countries" row beats four single-country rows).
- **For bilingual slides, trim BOTH languages symmetrically.** The `L`-toggle
  reveals asymmetries instantly; an EN-trim without the matching JA-trim
  leaves the JA side bloated.

## Hard truths to internalize

- **Some slides genuinely have only 5-6 lines of real content.** No font-size
  adjustment will make those fill the stage without looking like a
  kindergarten poster. Accepting 60-75% fill on sparse slides is fine; only
  treat <50% fill as a real defect.
- **Be skeptical of "all clean" reports.** If the user is asking for a
  thorough pass, they've probably already spotted something. If your audit
  comes back empty, ask them to point at a specific slide before declaring
  victory.
- **Verify the script when you change it.** Run it against a slide you've
  personally eyeballed as broken before trusting any modification.

## What this doc does NOT replace

- The python-pptx visual-QA loop in `CLAUDE.md` (LibreOffice → `pdftoppm` →
  Read PNG). That's still correct for weeks built with `build_slides_weekN.py`
  via `sds_slides.SDSDeck`. Use this doc for the Quarto/RevealJS pipeline.
- The bilingual authoring rules in `CLAUDE.md` (paired `::: {.lang-en}` /
  `::: {.lang-ja}` divs, `L` keypress, mermaid duplication, etc.). Those are
  unchanged.
- The cross-repo sync rules. `sds-reveal/` is shared verbatim with
  `lecture-plans`; if you fix a CSS bug here, mirror it there.
