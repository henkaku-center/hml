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

The three failure modes you must hunt for:

- **OVERFLOW** — content past slide bounds, clipped, or triggering Reveal's
  auto-shrink-to-fit. Visible in both engines. Easy to spot in PNGs.
- **FLOATING** — short content block symmetrically padded by `center: true`.
  Top gap >15% AND bottom gap >15%, fill <55% of stage height.
  **Invisible in PPTX previews.** Only visible in HTML.
- **PUSHED-DOWN** — content sits below the middle. Rare; usually a misplaced
  div or stray empty paragraph.

A PPTX-only check catches OVERFLOW reliably and misses FLOATING/PUSHED-DOWN
entirely. Don't trust an "all clean" report based only on LibreOffice
rasterizations.

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
   per-slide fill%, top-gap%, bottom-gap%, and a flag (OK / OVERFLOW /
   FLOATING / PUSHED-DOWN / SHORT / SKIP-FRAMED). Writes JSON for later diffs.
3. **Classify each flagged slide** by its current sizing class (`grep` the
   `## Title {.xxx}` in the qmd):
   - OVERFLOW + already `.smaller` → trim content (no smaller tier exists).
   - OVERFLOW + `.bigger`/`.midbig` → downgrade one tier.
   - OVERFLOW + no class → try `.smaller` first; if still overflows, trim.
   - FLOATING + `.smaller` → remove `.smaller` (verify it fits at default).
   - FLOATING + no class → try `.midbig`; then `.bigger`; then `.biggerplus`.
   - FLOATING + `.bigger` → `.biggerplus` or `.biggest`; if those now overflow,
     trim content.
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
