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

## The layout scheme (v2, 2026-07 — read BEFORE authoring, not just QA'ing)

v2 exists because three defects kept reaching the professor's eyes on first
render across Weeks 9–12 despite clean audits: **figures rendered tiny**
(crushed by the text stacked around them), **prose walls that should have been
bullets**, and **one default layout for everything**. Root cause: the fill
metric REWARDS text-stuffing — text is the cheapest filler, so a slide whose
figure had been flex-crushed to an illegible sliver still audited ~100% full.
v1 was a strong detection system but a weak authoring system. v2 changes both:
the theme now makes figures win *by construction*, and the audit measures
figures and prose directly (TINY-FIGURE / SQUISHED-FIGURE / PROSE-WALL + a
layout-mix report). The goal is unchanged: **clean like a designed deck, while
using the whole slide** — on the SDS identity (dark stage, yellow frame,
Inter, blue accent).

### Rule 0 — pick the layout archetype BEFORE writing the slide

The recurring failure is authoring every slide as "title + text," then
noticing too late that the content wanted another shape. At outline time (and
again when writing each slide), match the content's shape to an archetype:

| Content shape | Archetype | How |
|---|---|---|
| A figure IS the argument, ≤ 2 caption lines | **Big figure** | `{.big-figure}` — figure auto-grows, ≥300px floor (`.bih`: 340px) |
| A figure needs ≥ 3 lines of commentary | **Split** | `:::: {.columns .v-center}` — figure column 45–60%, text column with punchline + bullets. NEVER stack ≥3 text lines under a full-width figure |
| Two things compared/contrasted | **Split or cards** | columns (add `.cmp-cols` for top-aligned parallel panels), or paired `.note-card`s (`.ink`/`.warn`/`.good`/`.bad`) |
| Definition stack / recipe / claims | **Bullets** | one clause per line; the punchline on its own line |
| One takeaway that must land | **Statement** | `{.statement}` — hero layout, ≤ ~5 short lines |
| Concept check | **Poll** | `{.poll-slide}` / `{.poll-reveal}` (boxed options from the theme) |
| A derivation/result with 3+ beats | **Build-up** | N sibling slides, not N fragments |
| Live demo | **Widget** | `{.widget-slide}` + visible sized iframe |

The audit prints a **layout-mix histogram** per deck; if >55% of content
slides classify as bullets/prose it prints a MONO-LAYOUT advisory. That's the
"not using different layouts when it would be effective" complaint, measured.

### Figure-first mechanics (what the theme now guarantees)

The old scheme let the fill-flex column shrink figures when text ran long —
silently, and with distortion (a flexed height fighting an inline width).
Week 12 slide 8 shipped a 1500×975 diagram painted at 520×124. The theme
(`sds-reveal/sds.scss` + shared `sds-reveal/fig-size.js`, injected
project-wide via `_quarto.yml`) now enforces:

- **Figures grow, text doesn't.** A standalone figure on a content slide is
  the slide's flex-grow element: it absorbs whatever height the text doesn't
  use. Default floor **150px**; `.big-figure` **300px**; `.big-figure.bih`
  **340px**. Small deliberate images opt out with `.fig-inline`.
- **Figures can never shrink below the floor or distort.** `object-fit:
  contain` everywhere; if floor + text exceed the stage, the slide overflows
  LOUDLY (audit: OVERFLOW / TINY-FIGURE) instead of the figure dying quietly.
- **The remediation direction is fixed:** when a figure slide overflows, trim
  the text to caption length, switch to the split archetype, or give the
  figure its own slide. **Never shrink the figure, never lower the floor.**
- **`.columns` rows never crush their content either** (`flex: 1 0 auto` —
  grow-only): an over-tall column spills visibly instead of clipping under
  the card (the Week 12 slide-7 lesson).
- The r-stretch/lazy-load strip is now shared (`fig-size.js`); new decks need
  NO per-deck figure CSS or JS at all.

**Authoring contract for figure slides:** a `.big-figure` slide carries at
most ~2 caption lines per language; a split slide's text column carries a
punchline plus 2–3 bullets. Plan the slide around the figure's aspect ratio:
a 2.4:1 banner wants full width with a bullet caption; a 1.5:1 diagram wants
the split.

### Bullet discipline (prose belongs in the textbook)

- **A paragraph that wraps to 3+ rendered lines gets rewritten** — as bullets
  (one clause per line), a two-column split, or moved to `::: {.notes}`. The
  audit flags 4+ lines as PROSE-WALL; don't author up to the limit.
- **2+ parallel bold-led clauses never share a line** (the RUNON-CAPTION rule,
  which also covers poll options: always a bullet list).
- **The punchline gets its own line** — usually the single `.yellow` span.
- Exception: `{.statement}` slides are deliberate hero prose, ≤ ~5 short
  lines, and are exempt from PROSE-WALL.

### Tokens & emphasis (unchanged from the 2026-07 refresh)

**Tokens (in `sds.scss` — never invent new hex values in a deck):**
`$sds-bg-dark #111111` (stage) · `$sds-bg-panel #191920` (raised panels:
code/cards/poll options) · ink `#F4F4F2` · dim `#A6A6A2` (captions,
provenance, asides) · hairline `rgba(255,255,255,.12)` (ALL borders/dividers)
· accent `#64B5F6` (links, structure, the title tick) · yellow `#FFEB3B`
(punchline) · green/red/orange (semantic only: correct/wrong/caution).

1. **Emphasis discipline.** At most ONE yellow punchline per slide. Bold for
   in-sentence stress; `.dim` for support text. Green/red/orange appear only
   with their semantic meaning. If a slide has three colors of emphasis, it
   has none.
2. **The gutter is sacred.** Content slides get a 4.5% horizontal gutter from
   the theme's fill-flex — nothing may run edge-to-edge except a full-bleed
   figure that explicitly earns it. Never restore `padding-left/right: 0`.
3. **Measure.** Top-level prose is capped (~72ch). If a paragraph still reads
   as a wall, the fix is AUTHORING (see bullet discipline) — not a smaller
   font.
4. **Structure over decoration.** Every content title carries the accent tick
   (automatic). Use `.eyebrow` for a block label above a title on key slides.
5. **Quiet chrome.** Tables: hairline row separators + accent-underlined
   header, no full cage. Code: raised panel, hairline border, 8px radius.
   Numbers in columns get `tabular-nums` (`.num` cells, `.time` stamps).
6. **Proximity is grouping.** Related lines sit tight; unrelated blocks are
   separated by the flex gap. If two blocks need more separation, they're
   probably two slides.
7. **Fill without cram.** No CLIP, no top-jam under ~70% — fewer,
   better-shaped elements at comfortable sizes.

**What lives where:** fill-flex (with gutter), figure-first sizing + floors,
`.columns` row behavior + `.cmp-cols`, poll boxes, widget-slide base,
big-figure, `.statement`, cards, eyebrow, measure caps → the SHARED theme;
the eager-load/r-stretch strip → shared `sds-reveal/fig-size.js` (wired in
`_quarto.yml`). Per-deck style files carry ONLY deck-specific overrides
(`codeslide`, `.cite`, `.agenda-roomy`, widget sizing). New decks should need
little or no per-deck CSS — if you find yourself writing per-deck figure
rules, fix the theme instead (cross-repo sync rule applies). Weeks 3–11 keep
their old per-deck copies — their published HTML is frozen, and on a
re-render their `!important` copies still win over the theme (acceptable
drift, documented here); Week 12 was re-authored onto the v2 theme as the
validation deck.

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
  auto-shrink-to-fit. Visible in both engines. Easy to spot in PNGs. The audit
  now ALSO runs the one true clip test directly (`scrollHeight >
  clientHeight` on the present section after revealing fragments) — this
  catches spill that the content-bbox test misses, e.g. a card overflowing a
  `.columns` row whose own box stayed small (Week 12 slide 7).
- **TINY-FIGURE** — the slide's LARGEST figure paints below the legibility
  floor (< 24% of stage height, main figures only: naturalWidth ≥ 400). THE
  marquee recurring defect (Weeks 9, 10, 12): a figure starved of height by
  the text stacked around it. The fill metric cannot see it — text fills the
  stage while the figure dies. With the v2 theme this should only fire when
  an author hard-caps a figure or opts out of the flex rules; remediation is
  NEVER "shrink something else a bit": trim the text to caption length,
  switch to the split archetype, or give the figure its own slide. The report
  line shows `(fig=NN%)` — the largest figure's visible height — on every
  slide with a figure, so you can watch this without waiting for the flag.
- **SQUISHED-FIGURE** — a figure painted at the wrong aspect ratio (rendered
  vs natural aspect off by > 12%). Happens when a flexed height fights an
  inline width without `object-fit: contain`. The v2 theme makes this
  structurally impossible; the flag is a regression guard for decks that
  override the theme.
- **PROSE-WALL** — a visible paragraph (≥ 200 chars) wrapping to 4+ rendered
  lines. Slides carry bullets and punchlines; prose belongs in the textbook
  or the speaker notes. Fix: one clause per line, a split, or `::: {.notes}`.
  `{.statement}` slides are exempt (deliberate hero prose).
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

**Fixes that make the audit's numbers trustworthy** — apply the same to any
forked copy:
1. **Fragments are revealed before measuring** (2026-06-08). Un-revealed
   `.fragment` content is `visibility:hidden` (laid out but excluded from the
   content bbox), so poll options / answers / build-up steps used to be
   invisible to the measurement and every poll false-flagged as sparse. The
   audit adds `.visible` to each `.fragment` (skipping `.fade-out`-style)
   before measuring, so a flagged poll is a REAL sparse/clip defect — don't
   dismiss it.
2. **The measurement viewport is the deck's EXACT logical size** (2026-07,
   superseding the 2026-06 aspect-ratio fix). Two historical mistakes: a
   hardcoded 1050×700 (3:2) viewport flagged phantom overflow on 16:9 decks;
   then measuring at the right aspect but scaled up (×1.3 to 1244×700) let
   Reveal's zoom change text-wrap rounding, so content that CLIPS at the true
   960×540 fit the enlarged viewport (the Week 12 slide-7 clip sailed
   through). The audit now reads `Reveal.getConfig()` and measures at the
   logical size, exactly. A ~1.5%-of-height tolerance still means a slide
   that *fills to the bottom edge* (good, `fill≈100%`, no clip) is not
   mis-flagged — only genuine spill is.
3. **The one true-overflow test is implemented, not just documented**
   (2026-07): the audit reads the present section's `scrollHeight` vs
   `clientHeight` after revealing fragments and flags `clipPx > 3` as
   OVERFLOW. This catches "unreachable" spill the bbox test misses (content
   escaping a `.columns` row). Content overflowing the TOP of a centered flex
   column is NOT counted by scrollHeight — the bbox test still covers that
   side, which is why both run.
4. **Figures and prose are measured directly** (2026-07): per-slide, the
   largest figure's *visible content* height (contain-aware — letterboxing
   inside a grown flex box doesn't count as figure), the worst rendered-vs-
   natural aspect skew, and any 4+-line paragraph. These drive TINY-FIGURE /
   SQUISHED-FIGURE / PROSE-WALL and the `(fig=NN%)` report note, plus the
   deck-level layout-mix histogram printed after the per-slide report.

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
   - TINY-FIGURE / SQUISHED-FIGURE → **not a sizing-tier fix, and never a
     shrink-the-figure fix.** The slide has more text than its archetype
     allows: trim to caption length, switch to the split archetype
     (`.columns .v-center`), or give the figure its own slide. If the figure
     is deliberately small (an icon), mark it `.fig-inline`.
   - PROSE-WALL → **an authoring fix, not a font fix.** Rewrite the paragraph
     as bullets (one clause per line), split to columns, or move detail to
     `::: {.notes}`. If the slide is a deliberate hero takeaway, make it a
     real `{.statement}` slide instead.
   - OVERFLOW on a figure slide → the figure floor is doing its job: the TEXT
     is too long. Trim text or change archetype — do not touch the figure.
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
   - Any flag on an agenda slide → use the agenda-specific classes
     (`.agenda.dense` for 11+ rows, a `.agenda-roomy`-style spread for 4–6
     rows), never body tiers.
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
4. **A wide/short figure under a text block used to render microscopic.**
   The v2 theme now prevents the silent version (figures grow and hold a
   floor), so this failure surfaces as OVERFLOW or TINY-FIGURE instead. The
   *fix* is unchanged and directional: move the figure to its own slide or a
   real two-column, or trim the text — never shrink the figure.

Aspect matters: a 3:1 figure at `width="90%"` is a fine big banner; the same
figure stacked under four bullets wants a split or its own slide. Decide the
slide layout *around* the figure's aspect ratio (Rule 0).

## Hard truths to internalize

- **Some slides genuinely have only 5-6 lines of real content.** No font-size
  adjustment will make those fill the stage without looking like a
  kindergarten poster. Accepting 60-75% fill on sparse slides is fine; only
  treat <50% fill as a real defect. (Or make it an honest `{.statement}`
  slide.)
- **A high fill% is NOT a healthy slide.** Fill measures quantity, not
  layout quality — a 100%-full slide can be a prose wall over a crushed
  thumbnail. Read the `(fig=NN%)` notes and the layout-mix histogram, not
  just the flag count.
- **When a figure slide overflows, the text is the problem.** The floors are
  deliberate; the loud failure is the feature. Do not "fix" it by opting the
  figure out of the flex rules or by lowering a floor.
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
