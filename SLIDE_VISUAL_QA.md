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

- **EMPTY-FRAME** — a slide with **no title and essentially no content** that
  still renders its background (e.g. a bare `# {.section-break ...}` that paints
  an empty yellow frame). The single most embarrassing defect, and the one a
  naive audit hides: the old audit blanket-skipped every `.section-break` slide
  (`SKIP-FRAMED`), so an *empty* section-break sailed through. The fixed audit
  counts each slide's visible content elements and flags zero-content,
  zero-title slides regardless of framing. **Cause:** authoring a section break
  as TWO slides — a bare `# {.section-break}` immediately followed by a
  `## [Title] {.section-break}`. Use only the titled `##` form; delete the bare
  `#`. (One bare `#` per break = one empty yellow box.)
- **JAMMED-TITLE** — a section-break (or other framed) slide whose title is
  pinned to the very TOP edge of the frame instead of vertically centered
  inside it (title top < 6% of stage). Reads as broken even though the slide
  "has content." **Cause here:** the `.section-break` centering rule in
  `sds-reveal/sds.scss` was scoped to `section.title-slide.section-break`, but
  Quarto only adds `.title-slide` to LEVEL-1 (`#`) headings — the common
  LEVEL-2 (`## Title {.section-break}`) form gets `section.slide.level2.section-break`
  with NO `.title-slide`, so the rule silently missed and the title fell to the
  top-left. Fix: scope the rule to plain `div.reveal div.slides section.section-break`
  (matches both heading levels). A correctly-centered section-break measures
  `top≈bot≈46%`; a jammed one measures `top=0% bot=91%`.
- **OVERFLOW** — content past slide bounds, clipped, or triggering Reveal's
  auto-shrink-to-fit. Visible in both engines. Easy to spot in PNGs.
- **FLOATING** — short content block symmetrically padded by `center: true`.
  Top gap >15% AND bottom gap >15%, fill <55% of stage height.
  **Invisible in PPTX previews.** Only visible in HTML. NOTE: these decks render
  **`center: false`**, so dead space pools at the BOTTOM (top-gap ≈ 0) and
  FLOATING almost never fires — the same physical defect lands as **BOTTOM-GAP**
  instead. "Few FLOATING flags" ≠ "few sparse slides."
- **BOTTOM-GAP** — content top-aligned with a void below it (fill < 75%,
  bottom gap > 20%). Because of `center: false`, **this is the primary
  sparse-slide flag**, not FLOATING — treat it with equal seriousness. It is
  **not auto-benign**: a poll/definition/recap at 38% fill is as broken as one
  that overflows, only in the opposite direction. The systemic fix is the
  **fill-the-slide flex layout** (content `<section>` = full-height flex column,
  `justify-content: space-between`) — apply that first; it clears most
  BOTTOM-GAP wholesale. After it, remaining cases: fill < 55% → must fix (tier
  up: `.midbig`→`.bigger`→`.biggerplus`→`.biggest`, or a poll-box / `.v-center`
  layout); fill 55–75% → fix by a tier bump if it fits, else record a one-line
  per-slide justification in the PLAN. A blanket "remaining flags are benign
  BOTTOM-GAP / just the polls" dismissal is **forbidden** — it is the exact
  sentence that propagated half-empty slides across Weeks 6–7.
- **PUSHED-DOWN** — content sits below the middle. Rare; usually a misplaced
  div or stray empty paragraph.
- **COLUMN-THIN** — a two-column slide where one column (almost always the
  text column beside a tall figure) is sparse. **The whole-slide fill looks
  fine** because the figure column sets the bounding box — so this is
  invisible to both a PPTX preview *and* a naive HTML audit that measures one
  box across the whole slide. The fixed audit measures each column on its
  own; see "Two-column slides" below.
- **CAPTION-MISALIGN** — a multi-column figure row (e.g. three portraits each
  with a label beneath) where the per-column captions are on **different
  baselines** (vertical spread > ~2.5% of stage) or **not centred under their
  figure** (horizontal offset > ~12% of column width). Happens when columns
  hold images of mismatched heights with bottom-anchored captions — each
  caption hangs at its own image's bottom, so they stair-step, and a
  `fig-align` quirk can leave one left-aligned. The audit measures, per
  `.columns` row, the spread of caption baselines (`capV`) and the worst
  caption-vs-figure horizontal offset (`capH`). **Fix:** compose the panels
  into ONE figure (a single matplotlib image with the labels + any arrows
  baked in) — alignment is then guaranteed by construction; or pad every image
  to a common height and centre the caption text. The Week 6 "Markov / Really
  past → Past → Less past" slide is the canonical example: three portraits of
  different aspect ratios, fixed by composing them into `markov_timeline.png`.
- **RUNON-CAPTION** — a caption/description paragraph packs **2+ parallel
  bold-led clauses** onto one line (`**State** = … . **Transition** = … .
  **Next ordering** …`) when the slide has vertical room (bottom gap > 10%).
  Hard to scan — the eye can't find where one clause ends. The audit looks for
  a `<p>` with ≥2 `<strong>` runs each followed by `=`/`:`. **Fix:** split each
  bold-led clause onto its own line — a bullet list (`- [**State** = …]{.dim}`).
  Same "each labeled item on its own line" principle as the poll-options rule.
  Checked *before* the fill flags, since a run-on caption usually also trips a
  borderline BOTTOM-GAP (the unused room is exactly why the split fits) and the
  caption is the actionable defect. Only fires when splitting would fit, so the
  fix is always free. Canonical example: the Week 6 card-shuffle "State /
  Transition / Next ordering" caption.

A PPTX-only check catches OVERFLOW reliably and misses
EMPTY-FRAME/JAMMED-TITLE/FLOATING/PUSHED-DOWN/COLUMN-THIN entirely. Don't trust
an "all clean" report based only on LibreOffice rasterizations. EMPTY-FRAME and
JAMMED-TITLE both ride on `.section-break` slides — the exact class the audit
used to skip — so always re-run the audit after editing section breaks or the
theme's section-break rules.

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

`--all-sizes` tests nominal plus ±50px wobble and several 16:9 ratios (720p,
1080p, laptop). Catches "works at exactly the design size, breaks at a slightly
different aspect ratio" bugs.

**Two fixes (2026-06-08) make the audit's numbers trustworthy again** — apply
the same to any forked copy:
1. **Fragments are revealed before measuring.** Un-revealed `.fragment` content
   is `visibility:hidden` (laid out but excluded from the content bbox), so
   poll options / answers / build-up steps used to be invisible to the
   measurement and every poll false-flagged as sparse. The audit now adds
   `.visible` to each `.fragment` (skipping `.fade-out`-style) before measuring,
   so a flagged poll is now a REAL sparse/clip defect — don't dismiss it.
2. **The measurement viewport matches the deck's real aspect ratio.** It was
   hardcoded 1050×700 (3:2); the decks are 960×540 (16:9), so content that fit
   the real slide overflowed the taller test viewport — phantom OVERFLOW. The
   audit now auto-reads `Reveal.getConfig()` width/height and measures at that
   aspect. A small ~1.5%-of-height tolerance also means a slide that *fills to
   the bottom edge* (good, `fill≈100%`, no clip) is no longer mis-flagged as
   OVERFLOW — only genuine spill is.
**The one true-overflow test:** read the present section's `scrollHeight` vs
`clientHeight` after revealing fragments — `scrollHeight > clientHeight` is a
real clip (defect); equal is just a full slide (good).

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
4. **Vertically center the short column** — add `.v-center` to the `.columns`
   div. Wrapping the text column's content so it centers against the figure
   removes the "text jammed at the top, void below" look when the text is
   genuinely brief.
5. **Vertically *spread* the text column** — add `.v-spread` to the `.columns`
   div. Where `.v-center` clusters the text and centers the cluster, `.v-spread`
   distributes the text column's block children (paragraphs, lists, equations)
   with even gaps top-to-bottom, so a moderately-full text column fills the
   figure's full vertical extent rather than floating. Use this for the
   figure-plus-several-paragraphs pattern (e.g. the Week 4 vote / rectangle-game
   slides). Caveat: `.v-spread` exposes real overflow that `.v-center` would
   mask by centering — if a slide overflows after switching, the text is
   genuinely too long and must be trimmed, not re-centered.

Do NOT "fix" COLUMN-THIN by shrinking the figure until the boxes match — that
usually makes the figure too small to read. Balance by *adding* to the thin
side or *re-proportioning*, not by degrading the strong side.

**`.v-spread` and the language toggle.** `.v-spread` sets `display: flex` on
the visible language block. That rule MUST be scoped to the currently-visible
language (`.lang-en` outside `body.show-ja`; `.lang-ja` under `body.show-ja`) —
a bare `.lang-ja { display: flex }` out-specifies `lang-toggle.css`'s
`.lang-ja { display: none }` and renders BOTH languages stacked. The shared
`sds.scss` already does this correctly; if you copy the pattern elsewhere,
keep the toggle scoping.

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
7. **JA-mode check (bilingual decks).** The fill audit and a default decktape
   capture both see only the EN state — they cannot catch a deck that is
   broken *in Japanese*. Two JA-only failure modes the audit will never flag:
   - **Fragment miscount** — a `.fragment` nested inside *each* lang div is
     two fragments; in JA mode the first keypress reveals the invisible EN
     one (a dead press). Polls are the usual victim. Fix: one fragment
     *wrapping* the paired lang divs (see CLAUDE.md → Fragments rule).
   - **Bare prose** — a `[…]{.yellow}` / `[…]{.dim}` line with no language
     class stays English under the JA toggle.

   To check, load the rendered HTML in a headless browser, add
   `document.body.classList.add('show-ja')`, and step through any slide with
   fragments — the content must reveal on the *first* press and be Japanese.
   A quick structural pre-check: every `.fragment` should *contain* the lang
   divs, not sit inside one.

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

## The OTHER visual-QA loop: matplotlib figure PNGs

The fill audit checks the *slide HTML*. It does NOT look inside the figure PNGs,
and the most common figure defect — **text spilling outside a box, or an
arrow/connector label colliding with a box** — is invisible to it. Figures get
their own quick loop:

1. **Composite onto the slide background before reading.** The PNGs are
   transparent with light-colored text. On a white image viewer, white-on-white
   overflow and box collisions vanish. Always composite onto `#111111` first:
   ```python
   from PIL import Image
   im = Image.open("images/foo.png").convert("RGBA")
   bg = Image.new("RGBA", im.size, (17,17,17,255)); bg.alpha_composite(im)
   bg.convert("RGB").save("/tmp/foo.png")   # now Read /tmp/foo.png
   ```
   For an audit pass, stack every box-heavy figure into one contact sheet and
   Read that — collisions jump out.
2. **Box-text fit is a hard rule.** Size each `box()` to its *longest* line (or
   drop the font); a box whose text runs past the rounded border is a defect,
   same as a clipped slide. Check the `width`/`fs` of every `box()` call against
   its string.
3. **Connector/arrow labels go in their own band.** Never place a label at the
   same `y` as a box — it overlaps the box edge. Put it clearly above the row or
   in the gap between rows (Week 9 `tom-as-irl` was the canonical fix).
4. **A wide/short figure under a text block renders microscopic.** That's not a
   figure bug, it's a *layout* bug — the fill-flex starved it of height. Move
   the figure to its own slide or a real two-column; don't shrink-fix it.

Aspect matters: a 3:1 figure at `width="90%"` is a fine big banner; the same
figure stacked under four bullets is a 5%-tall sliver. Decide the slide layout
*around* the figure's aspect ratio.

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
