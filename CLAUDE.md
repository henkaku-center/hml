# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Course materials (not code) for **Human and Machine Learning**, Spring 2026, at Chiba Institute of Technology / School of Design & Science (SDS). The course was previously PSYC841 at UW-Madison; SP26 is a rename + port. 13 Friday sessions, Apr 17 – Jul 17, 2026 (no class May 1).

There is no build, no test suite, and no package manager at this level. Work is mostly editing Markdown PLAN files, moving/porting SP25 Canvas content, and drafting new materials.

## Directory model

```
course/week01_… … week13_…/   One dir per week. Each has PLAN.md + slides/ + wiki_pages/
course/assignments/            Assignment LaTeX sources + solutions/
course/quizzes/                README.md maps quiz → week; actual quiz XML lives in archive/
course/syllabus/               SP25 syllabus + project guidelines (reference only; docx/pdf)
textbook/                      Hugo site for the "Narrative Introduction to Probability" textbook
                               — has its own CLAUDE.md; follow that when inside textbook/
resources/                     Readings, notebooks, images copied out of the Canvas export
archive/canvas_export_sp25/    READ-ONLY. Complete SP25 Canvas export. Do NOT modify.
docs/                          GitHub Pages landing site (static HTML + assets/)
old_class_backup.tar.gz        2.2 GB archive — leave it alone unless explicitly asked
```

Each `course/weekNN_…/PLAN.md` follows a fixed template: Topics, SP25 Content (slides + wiki pages + quiz), Textbook Chapters, GenJAX Integration, Contemporary ML Notes, Status, TODOs. Preserve that structure when editing — other tooling and the top-level `TODO.md` read it.

`TODO.md` at the repo root is the consolidated backlog (SP25 carryovers + SP26 new work). Keep it in sync when a week's PLAN changes materially.

## Hard rules

- **Never modify `archive/canvas_export_sp25/`**. It's the source-of-truth SP25 Canvas export for re-import and reference. Copy *out* of it, never *into* it. The `.claude/settings.local.json` pre-approves specific `cp -r archive/canvas_export_sp25/web_resources/... resources/...` commands — use those patterns.
- **Textbook is a separate project.** `textbook/` is a Hugo site with its own `CLAUDE.md`, code-block validator (`validate_code_blocks.py`), and date-frontmatter rule. When working inside `textbook/`, switch to those conventions. The textbook is published separately at https://josephausterweil.github.io/probintro/ — this repo contains a working copy/drafts.
- **Syllabus:** The SP26 syllabus is `course/syllabus/SP26_syllabus.md` — edit this when making syllabus changes. `course/syllabus/PSYC841_Spring2025_reference.*` are SP25 UW-Madison reference material only; do not treat them as current.
- **Define technical terms/acronyms at first use on slides.** Whenever a new technical term, notation, or acronym first appears in a deck (PMF, PDF, MLE, Σ, $\binom{n}{k}$, indicator, posterior, likelihood, etc.), its first on-slide appearance must include a definition — either inline or on the immediately preceding slide. This includes symbols: if Σ, ∫, or $\binom{n}{k}$ shows up in a formula before it has been defined, either define it in a dim caption beneath the formula or add a one-line notation-lock-in slide before it. If the term reappears after a long gap (e.g. a block break, or > ~15 min of lecture time), briefly redefine it in situ rather than assuming retention. When porting SP25 content, audit for the "suddenly appears without definition" pattern — it is the most common source of student confusion and red-team hits. Applies to slides and speaker notes; the textbook has its own introduction order. **This rule covers named concepts, phenomena, and empirical paradigms — not just notation.** "Theory of mind", "false belief", "faux pas", "GAN", "discriminator", "Bradley-Terry", "max-entropy" are all terms-at-first-use that need a one-line definition (or a plain-language reframe that *avoids* the untaught term — e.g. describe adversarial imitation as "a critic tells expert from imitator; the imitator improves until it can't" instead of leaning on "GAN"). The Week-9 first delivery defined every *symbol* (τ, β, b) yet left "theory of mind" undefined and introduced GANs that were never taught — the exact gap that drew professor red-team hits. **Prerequisite check:** every concept a deck *uses* must be either taught in a prior week or defined in-deck; before lecture-ready, grep the student-facing lines (outside `::: {.notes}`) for load-bearing terms with no nearby definition.
- **Introduce the symbol when you name the variable.** A specialization of the rule above for the concrete-example case. When a slide names a domain variable in prose ("Weather", "Bento", "the patient's age"), introduce the math symbol *simultaneously* — usually as `**Weather** ($W$)` — so the formula that lands two slides later has nothing for the student to decode. If a formula uses $W, D, R, B$ and the prose-introduction slide spelled out the words without symbols, the formula slide will lose 30 seconds to "wait, which one was W again?". Add the symbols on the introduction slide, not retroactively. Apply bilingually — both `.lang-en` and `.lang-ja` need the parenthetical symbol. When a slide introduces a *set* of variables, close it with a dim one-liner noting the shorthand will be used going forward (e.g. `[We'll use $W$, $D$, $R$, $B$ as shorthand for these from here on.]{.dim}`).
- **American spellings only.** All English slide text — `.lang-en` prose, captions, speaker notes, titles, poll options — must use American English spelling. Use *behavior* (not behaviour), *color* (not colour), *favor* (not favour), *neighbor* (not neighbour), *gray* (not grey), *labeled/labeling* (not labelled/labelling), *modeled/modeling*, *generalize/generalization* and the rest of the `-ize`/`-ization` family (normalize, marginalize, summarize, optimize, regularize, etc.), *analyze* (not analyse), *artifact* (not artefact), *center*, *defense*. **Do not** "correct" words that are identical in both dialects — the `-ise` verbs *exercise, comprise, surprise, advertise, supervise, revise, advise, devise, compromise, franchise* stay `-ise`, the noun *analysis/analyses* is unchanged, and the CSS/Mermaid `color:` property is already American. This is an authoring rule for new decks **and** a porting rule: SP25 material and any imported text must be swept for British spellings before a week is marked lecture-ready. `.lang-ja` content is exempt (it's Japanese).

## Cross-cutting SP26 themes (affect almost every edit)

These show up repeatedly in PLAN TODOs and drive most new work:

1. **GenJAX integration.** All four programming assignments (clusters, generalization, mc, rl) need GenJAX ports or a GenJAX option. Week 2 homework introduces GenJAX via textbook T2 Ch 0-1. Weeks 6, 8, 11 are flagged for GenJAX exercises.
2. **Textbook chapter mapping.** Each week's PLAN.md lists the textbook chapters to assign. When adding/moving content, update both the PLAN and the textbook cross-reference.
3. **Contemporary ML content** (Weeks 11-13): LLMs, foundation models, RLHF, alignment, scaling laws, interpretability, transformers. Week 13 (ethics) should pick up recent AI-safety developments.

## Common operations

- **Find SP25 source for a week**: each PLAN.md names the original slide files (e.g. `Week00_BasicBayes.pptx`) and wiki pages. They're already copied into `course/weekNN_…/slides/` and `wiki_pages/`; the originals live in `archive/canvas_export_sp25/web_resources/`.
- **Find a quiz**: `course/quizzes/README.md` maps week → quiz name. The actual Canvas QTI XML lives under `archive/canvas_export_sp25/g<hash>/assessment_qti.xml`, with its title in `assessment_meta.xml` — identify by reading the title, not by filename. Every directory `g<hash>/` that has both files is a quiz; the bare-XML `g<hash>.xml` files are Canvas topic/announcement pages, not quizzes.

## Standing rule for lecture authoring

When building or revising any weekly lecture, **mine the SP25 quiz bank for audience-poll / check-in prompts** before declaring the week ready. Concretely:
1. Look up the week's quiz in `course/quizzes/README.md`. Adjacent weeks' quizzes are also fair game if topically overlapping (e.g. Week 2 lecture pulls from the Week 2–4 quizzes: Intro Probability 1, Intro to Prob Theory 2, Gaussian and Binomial Bayes).
2. Read the assessment_qti.xml and identify questions that (a) fit as a fast live poll (≤ 4 options, commit-before-reveal), (b) test concepts already covered by that point in the lecture, (c) don't require written prose.
3. Integrate 2–4 polls per week as paired slides: `prompt` (question + options) → `reveal` (answer + 1-line justification), landed at natural block boundaries. Each pair should cost ≤ 1.5 min.
4. Record which SP25 quiz item sourced each poll in the speaker notes, so reusing or retiring it is traceable.
5. **Bilingual poll structure (Week 2+ decks).** A poll touches every bilingual-slide trap at once, so build it deliberately:
   - **Prompt slide:** the question in paired `.lang-en`/`.lang-ja` divs, then the options in **one** `.fragment` that *wraps* the paired option divs — never a `.fragment` nested inside each lang div (that double-counts and breaks the reveal in JA — see the Fragments rule above).
   - **Reveal slide:** the bolded answer line must be paired lang spans (`[EN]{.lang-en .yellow}[JA]{.lang-ja .yellow}`), not a bare `[…]{.yellow}` — a bare answer line stays English in JA mode. The justification goes in paired `.lang-en`/`.lang-ja` divs.
   - Translate the options when porting: an SP25 quiz item is English-only; the JA option text must be authored, not left blank.
   - Verify by toggling the rendered deck to JA (press `L`) and stepping through the poll — the options must appear on the *first* keypress and the answer line must be Japanese.

Rationale: the SP25 quizzes are already-authored, already-pedagogy-tested concept checks on the exact same material. Recreating poll prompts from scratch is wasted effort, and the archived quizzes surface student misconceptions the SP25 cohort actually hit.
- **Landing page**: `docs/index.html` is a single-file static site served by GitHub Pages. Assets in `docs/assets/` (Chiba Tech SDS logos) were fetched via pre-approved `curl` commands in `.claude/settings.local.json`.
- **Readings:** `course/readings_map.yml` is the source of truth for weekly readings and paper-presentation assignments. Weeks 1 and 2 are populated; Weeks 3–12 are stubs to fill in during the readings-modernization planning session.

## Bilingual slides (EN ↔ JA toggle)

Week 2 onwards, slides support an in-lecture EN↔JA toggle for bilingual students. Press `L` (or `l`) while viewing a deck to switch language; the choice persists across reloads via localStorage. A small muted badge in the bottom-right shows the current language.

**Infrastructure** lives in `sds-reveal/`:
- `lang-toggle.css` — hides `.lang-ja` by default; `body.show-ja` swaps visibility.
- `lang-toggle.js` — `L` keypress handler, localStorage persistence, badge mount.

**Wiring is automatic.** The project-level `_quarto.yml` injects `lang-toggle.css` and `lang-toggle.js` into every `course/week*/week*-slides.qmd` render by default. New week decks pick up the toggle without any per-file frontmatter — just start using the authoring pattern below.

**Authoring pattern** — wrap parallel content in paired Quarto fenced divs:

```markdown
## Slide title

::: {.lang-en}
English content — prose, KaTeX ($P(H \mid D)$), lists, everything.
:::

::: {.lang-ja}
日本語の内容 — 散文、KaTeX（$P(H \mid D)$）、リストなど全て。
:::
```

**Rules:**

- **CSS-toggle, never re-render.** Both languages stay in the DOM at all times; KaTeX/Mermaid render once on page load and work in both. Re-rendering on toggle (which is what Ira's APS p5.js source does) would break math.
- **Mermaid diagrams**: mermaid edge labels and node text don't inherit the language wrapper the way markdown prose does. If you need a bilingual mermaid diagram, either duplicate the entire `mermaid` block inside each lang div, or author it language-agnostic (English only — fine for formula-style diagrams).
- **Fragments on bilingual slides — wrap the lang divs, do NOT nest a fragment inside each.** A `.fragment` placed inside *both* `.lang-en` and `.lang-ja` produces **two** fragments. Reveal counts hidden fragments, so in JA mode the first keypress reveals the (invisible) EN fragment — a dead press — and the JA content only appears on the second. For a poll, the options then fail to appear when expected. The correct pattern is **one** fragment that *wraps* the paired lang divs:
  ```markdown
  ::: {.lang-en} prompt text :::
  ::: {.lang-ja} prompt text :::

  ::: {.fragment}
  ::: {.lang-en} ...EN options... :::
  ::: {.lang-ja} ...JA options... :::
  :::
  ```
  For a single reveal of inline content, a fragment can also wrap two inline spans: `::: {.fragment}` `[EN]{.lang-en}[JA]{.lang-ja}` `:::`. Language-agnostic math (`$$...$$` with no prose) needs no lang wrapper inside the fragment — a bare `::: {.fragment}` around the equation is fine and correct.
- **No bare prose on a bilingual slide.** Every piece of student-facing text on a slide that has *any* `.lang-ja` content must itself be wrapped — either in a `.lang-en`/`.lang-ja` div or as paired inline spans. Bare text (a `[**answer**]{.yellow}` line, a `[…]{.dim}` notation caption) has no language class, so it stays in English when the deck is toggled to JA — a mixed-language slide. This is easy to miss because the bare line *looks* fine in the default EN render. A styled span still needs the language class: write `[EN]{.lang-en .yellow}[JA]{.lang-ja .yellow}`, not a bare `[…]{.yellow}`. (Language-agnostic math and figures are exempt — they read the same in both.)
- **Agenda / "Where we are" recap slides are bilingual too — including the bullets.** An `{.agenda}` slide and every `{.agenda}` recap reprise is student-facing text, so every bullet label must be paired `.lang-en`/`.lang-ja` spans, and the slide title must be a paired `[Agenda]{.lang-en}[本日の予定]{.lang-ja}` (never a bare `## Agenda`). The trap: the `.done` / `.highlight` state class on a recap bullet (`[label]{.done}`) *looks* complete but has no language class, so in JA mode the title flips but every bullet stays English — a half-translated slide. The state class goes on **both** spans: `- [EN label]{.lang-en .done}[JA label]{.lang-ja .done}  [0:10]{.time}`. The `[…]{.time}` stamp is language-agnostic (digits) and needs no wrapper. When a recap reprises the same agenda with a different `.done`/`.highlight` position, keep the bilingual bullet text identical across all reprises — only the state class moves.
- **Speaker notes**: one language per slide unless you wrap content inside `::: {.notes}` in paired lang divs too. Generally not worth it — instructor-only content can stay EN.
- **Title slide**: Quarto's title/subtitle frontmatter fields don't accept nested divs. If a JA title is needed, use the title in both languages with an `&nbsp;&nbsp;·&nbsp;&nbsp;` separator.
- **Keyboard**: `L` is free in Reveal. Avoid `f` (fullscreen), `s` (speaker notes), `b` (blackout), `?` (help), `esc`.

**Verifying:** decktape preview captures only the default (EN) state. To verify JA content is present, `grep -c "lang-ja" weekN-slides.html` — should be >0. To actually see JA rendered, open the HTML in a browser and press L.

**Trim symmetrically.** When the fill audit (see `SLIDE_VISUAL_QA.md`) flags a bilingual slide and the fix is content-trim rather than tier-change, trim BOTH languages — an EN-only trim leaves the JA side bloated, which `L` reveals instantly.

**Scope today:** Week 2 has ~24 concept-introducing slides translated to JA (Block 1 Meet Chibany, Block 2 Marr L1/L2/L3/cab, Block 3 Notation 1-3 + Bayes flow + polls, Block 4 Setup/joint/marginal/conditional/independence/summary, Block 5 EV/Bernoulli/Binomial intros, Block 7 Shift in what's hidden). Build-up repetitions (slides that only change a number) stay EN-only on purpose — students who want JA can press L on the concept intros, where it matters. Full retrofit of remaining slides is an open TODO in `TODO.md`.

## How to build a week (SP26 lecture artifacts)

**SCSS theme split (Week 2 pinned, Week 3+ uses synced).** `sds-reveal/sds.scss` is the shared theme synced from lecture-plans with the five-tier sizing system (`.smaller` / default / `.midbig` / `.bigger` / `.biggerplus` / `.biggest`) used by the Quarto fill-audit workflow. The 2026-07 design refresh added named tokens (ink/dim/hairline/panel + semantic colors), the content-title accent tick, `.eyebrow`, `.note-card` flavors, quiet tables/code, prose measure caps, and promoted the fill-flex/poll/widget/big-figure CSS into the theme — authoring discipline lives in `SLIDE_VISUAL_QA.md` "Design system". Week 2 was authored against an earlier, tighter-rhythm version and is pinned: its qmd points at `course/week02_basic_bayes_cont/sds-reveal-week2.scss` (a frozen snapshot, not symlinked).

**Each week's qmd MUST set its own `theme:` in frontmatter.** The repo-root `_quarto.yml` intentionally does *not* set a project-level theme, because Quarto merges (rather than replaces) parent and child theme arrays — which made it impossible to keep the shared `!important` rules out of Week 2's cascade. So:

- Week 2 (pinned): `theme: [dark, sds-reveal-week2.scss]`
- Week 3+ (shared, five-tier): `theme: [dark, ../../sds-reveal/sds.scss]`

If you create a new week's qmd and forget the theme line, the deck renders with Quarto's default `dark` theme only and looks wrong. Do not edit `sds-reveal-week2.scss`; if a fix is needed in the shared theme, mirror it to lecture-plans per the cross-repo sync rule.

Starting Week 2, lecture artifacts follow the per-week triplet pattern from the APS-I repo:

```
course/weekNN_<slug>/
├── PLAN.md                          (fixed template: Topics / SP25 Content / Textbook Chapters /
│                                     GenJAX Integration / Contemporary ML Notes / Status / SP26 artifacts / TODOs)
├── weekN-shared-outline.md          (SOURCE OF TRUTH — timing table + per-block key points + contingencies)
├── build_slides_weekN.py            (standalone Python script, uses sds_slides.SDSDeck)
├── sds_slides.py                    (shared slide-building module — first copied into Week 2;
│                                     promote to a shared location once a second week adopts it)
├── sds_branding.svg                 (source of the yellow frame + SDS wordmark PNGs — needed by sds_slides)
├── week2-speaker-notes.md           (GENERATED — do not hand-edit)
├── slides/
│   ├── sp25_reference/              (SP25 source slides, kept for reference; never present as-is)
│   └── sp26/
│       ├── weekN-slides.pptx        (GENERATED — do not hand-edit)
│       └── preview/slideNN.png      (GENERATED via `--preview` — visual-QA rasterizations)
└── wiki_pages/                      (SP25 Canvas wiki page snapshots, reference only)
```

Rule: edit the shared-outline first → edit the build script (speaker notes as `notes=` kwargs on each slide call) → re-run the build script. The `.pptx` and the `speaker-notes.md` are both regenerated; the `.md` is derived and should never be hand-edited.

**Canonical example:** `course/week02_basic_bayes_cont/`. Look there before building a new week.

`sds_slides.SDSDeck` helpers: `title_slide`, `agenda_slide`, `section_break`, `content_slide`, `break_slide`. Each accepts a `notes=` kwarg. Theme colors are module constants (`deck.ACCENT`, `deck.DIM`, `deck.YELLOW`, etc.) — reuse them rather than introducing new hex values.

Week 1's `LECTURE_NOTES.md` predates this pattern and will NOT be retrofitted — it's a historical artifact of the first session.

## Visual density baseline for new lecture decks

First-draft decks default to text+KaTeX walls and underweight figures, build-up sequences, and two-column structure. Week 4 was iterated heavily to fix this (initial scaffold: 60 slides, 0 figures, 0 column layouts → final: 78 slides, 14 figures, 16 column layouts, plus two 3–4-slide build-up sequences). For new weeks, **plan visuals in the shared-outline before writing the qmd**, and apply these baselines.

**Per-block visual budget.** Each non-section-break block should contain:
- **At least one figure** if the block introduces a model, a result, or a phenomenon. If no SP25 figure is reusable, list the figure-to-make in the outline as `figure-todo: <name>.png — <what it shows>` so it's an explicit TODO, not a hope.
- **At least one two-column slide** if the block contains structural parallelism — strong vs. weak sampling, prior vs. posterior, human vs. model, two competing hypotheses, before vs. after intervention. Default to `::: {.columns}`, not a bulleted list.
- **Build-up as N sibling slides, not N fragments**, whenever a derivation/result has 3+ steps that each deserve attention. The Tenenbaum & Griffiths vote sequence is canonical: a 1-slide equation with reveals (initial Week 4) is wrong; a 4-slide sequence (`Vote → y=x → y=x+1 → y=x+2`), each with its own figure, is right. Fragments are for *minor* reveals within a single conceptual beat; sibling slides are for *separate* beats.

**Outline-level requirement.** The `weekN-shared-outline.md` must list, per block: (a) the figures that block needs (existing or to-be-made), (b) which slides will be two-column, (c) which insight gets a sibling-slide build-up. If a block's plan reads "explain X, then Y, then state Z" without naming a figure or a column layout, that's a sign the block is being scoped as text — push back before authoring the qmd.

**One keyword-clause per line.** When a caption or description packs **two or more parallel keyword-led clauses** into one run-on line — `**State** = …. **Transition** = …. **Next ordering** …` or `**Random (ER):** …. **Scale-free:** …` — split each clause onto **its own line** (a bullet list `- [**State** = …]{.dim}`), *whenever the slide has the vertical room* (a figure-plus-caption slide almost always does). A run-on line of bolded labels is hard to scan: the eye can't find where one clause ends and the next begins. The trigger is **parallel structure** (two-plus clauses each introduced by a bold term, separated by a period), not mere length. This generalizes the poll-option rule (poll options MUST be a bullet list, never bare `A./B./C.` lines that collapse to one paragraph): the same "each labeled item gets its own line" applies to any caption with parallel bold-led clauses. Don't over-apply it to flowing prose that happens to contain a couple of bold words — only to genuinely parallel, scannable items. The card-shuffle "State / Transition / Next ordering" caption (Week 6) is the canonical example. The fill audit flags the symptom as **RUNON-CAPTION** when a `.dim`/caption block on a slide with spare vertical room contains 2+ bold-led clauses on one line.

**Figure-to-make convention.** When a figure doesn't exist in `slides/sp25_reference/` or `images/`, the outline lists it as `figure-todo: <filename>.png — <one-line description>`. On the first authoring pass, scaffold the slide with a `<!-- TODO figure: filename.png -->` placeholder, then generate the figure (a small matplotlib script under the week directory) before declaring the draft done. The audit catches stubs, but the rule is "scaffold then generate," not "ship the stub."

**Reuse SP25 figures aggressively.** The SP25 .pptx files in `slides/sp25_reference/` contain figures (Shepard decay, T&G results, rectangle-game panels, etc.) that can be extracted via LibreOffice and dropped into `images/`. Do this on first pass — recreating a figure that already exists is wasted effort.

**When in doubt, copy Week 4's final rhythm.** Look at the final `week4-slides.qmd` for the recurring shape: section-break → setup slide → motivating-figure slide → build-up sequence → poll → recap. Reproduce that rhythm.

## Recurring authoring lessons (Weeks 4–9 — front-load these)

These are the defects and friction points that recurred across the iterated decks. Applying them on the *first* draft is what makes the build smoother — each one below was caught only after the professor flagged it.

- **Matplotlib figures: the text must clear the box, and connector labels need their own band.** Every `box()`/labeled-arrow figure in `make_figures.py` is a text-overflow risk: size each box to its *longest line* (or drop the font), and never place an arrow/connector label at the same `y` as a box — it collides with the box edge (put it in a clear band above/between the rows). This was the single most common figure defect (Week 9 alone: the amortized-vs-Bayesian boxes, the ToM-as-IRL arrow labels, the LLM-ToM summary box, the α-vector clipping).
- **QA every figure by compositing it onto the slide background, not on white.** The PNGs are transparent with light text; on a white image viewer, white-on-white overflow and box collisions are invisible. Before declaring figures done, composite each onto `#111111` with PIL and Read it (a contact sheet of the box-heavy figures catches collisions fast). This is also how you verify a "tiny figure" is actually tiny vs. just cropped.
- **A substantial figure stacked under a text block gets crushed to nothing.** The fill-the-slide flex makes a tall bullet list and a wide/short figure compete for height; the figure loses and renders microscopic (Week 9 "Build the inversion"). Give any information-bearing figure its *own* slide (or a genuine two-column), never stacked beneath a full bulleted list.
- **`.smaller` is for OVERFLOW, not for sparse slides.** Adding `.smaller` to an under-filled slide makes it *worse*. If the audit flags a text slide as FLOATING / low-fill, the fix is usually to **remove** `.smaller`, not add a tier (Week 9 RLHF slides went 39%→80% just by dropping it).
- **A block reorder is a multi-slide structural edit, not a local one.** The agenda segment list is duplicated across the opening agenda + *every* "Where we are" recap + the closing "One inversion, N times" recap, and `.agenda.dense`'s font is calibrated to the item count (8 rows → 0.82em, 9 rows → 0.70em). Reordering/splitting a block means: rewrite all recaps' bullets *and* their done/highlight states, redistribute the timing, retitle the closing recap, and re-check the `.dense` sizing. Plan for all of it before starting.
- **Speaker notes that name an adjacent slide go stale under a reorder.** Phrases like "the very next slide," "we just saw," "now let's run it" break when slides move or get inserted. After any reorder/insert, grep the notes for positional references and fix them.
- **Author concept slides as bullets from the first draft, not prose.** First-draft bodies default to run-on KaTeX paragraphs and the professor consistently asks to break them up. Any slide with 3+ parallel clauses (a definition stack, a comparison, a recipe, a pass/fail/confound debate) should be a bullet list with the punchline on its own line — this generalizes the existing "one keyword-clause per line" caption rule to body text.
- **Build widgets configurable from the start, and put the control where it logically lives.** The professor repeatedly turns a watch-only widget into a manipulable one — drive-the-agent mode, adjustable Tiger noise/reward/penalty, a click-to-paint reward grid. Default every widget to "let the user set the key parameter," and place the editable control on the panel it belongs to (set the *true reward* on the *true-reward* grid, not a side panel).
- **Fact-check cross-week claims and attributions before asserting them.** "Last week we taught X" must match what the prior deck *actually* covered (Week 9 wrongly claimed Week 8 taught softmax — it taught value iteration / ε-greedy); attributions must be right (inverse-planning ToM is **Baker & Tenenbaum**, *reviewed* by Jara-Ettinger 2019, not originated by him); limit-case language must be precise (β→∞ is *greedy / pure exploit*, not "optimal"). These are exactly the things the professor catches — verify first.
- **A topic that admits a unifying probabilistic framework must be STRUCTURED as "frame → work each unknown piece," not a topic-tour.** The Week-9 first delivery was a tour (goal inference → ToM → POMDP → IRL → teaching → alignment) that re-derived Bayes in every block and only named the unifying POMDP frame at the very end — the professor's central complaint. The rebuild draws the agent model (a POMDP) as ONE master diagram in Block 1, lists its unknowns ("map of unknowns"), and lights up the active piece each block. When a week's PLAN reads as a sequence of topics, ask "what single generative model are these all inverting?" and lead with it.
- **Establish the frame ONCE, then REFERENCE it — never re-derive it.** "Reuse the same equation each block" (a good design) is NOT "restate/re-derive the equation each block" (what makes a lecture feel repetitive — the professor's "I kept repeating myself"). The mechanism that prevents it: a single persistent diagram you *point at* (highlight the changed latent), so a later block costs one slide, not a re-derivation.
- **When an instructor's own work anchors a block, cite their most recent / most formal treatment.** Week-9 first delivery mined Ho et al. **2016** (the behavioral showing-vs-doing paper) and missed Ho et al. **2021** (*Communication in Action*, JEP:General — the recursive-POMDP formalization the professor actually wanted). Before building a block around a named author, check `final_papers/` (and ask) for their latest/canonical paper on it.
- **Foreground interactive widgets — do not bury them as `background-iframe`.** Week-9 widgets were wired as `data-background-iframe` (title hidden, fell back to a static PNG in practice, never driven). Make each a titled `.widget-slide` with a sized, visible `<iframe class="widget-frame">` the instructor drives live. If the textbook already has the widget (`textbook/static/widgets/`), reuse it and pull relevant earlier-week widgets in as callbacks.
- **Clip-check the LEAF slide, not the parent stack.** Quarto nests `##` content slides as VERTICAL children under each `#` section. `document.querySelector('section.present')` returns the parent STACK (the section-break), so it silently measures the wrong element and reports section-break overflows while missing real content-slide clips. Use `Reveal.getCurrentSlide()` and walk both axes (`Reveal.slide(h,v)` over each stack's child count) — see the clip-check pattern used for the Week-9 rebuild.

## Slide visual-QA loops (two pipelines)

Two slide pipelines, two QA loops — pick by how the deck was built:

- **python-pptx weeks** (Week 1 only currently; any week built via `build_slides_weekN.py` + `sds_slides.SDSDeck`) — use the LibreOffice → `pdftoppm` → Read PNG loop documented below. PPTX previews catch overflow reliably.
- **Quarto/RevealJS weeks** (Week 2 onwards) — use the Puppeteer-based fill audit in `SLIDE_VISUAL_QA.md`. PPTX-style PNG previews **miss "floating" slides entirely** (short content blocks symmetrically padded by `center: true`); the HTML-level audit is required. Spot-check the riskiest 3–5 slides with `decktape` + `Read` PNG only *after* the fill audit reports zero flags. Remediation uses the five-tier sizing classes in `sds-reveal/sds.scss` (`.smaller` / default / `.midbig` / `.bigger` / `.biggerplus` / `.biggest`) — **except** the `COLUMN-THIN` flag, which is a two-column-balance problem (a sparse text column beside a tall figure) and is fixed by rebalancing the columns, not a tier change. See the "Two-column slides" section of `SLIDE_VISUAL_QA.md`.

Shared rule across both loops: never iteratively nudge coordinates/font-sizes blind past one cycle — fix the template (sds_slides helper for PPTX, the tier classes for Quarto), not the call site.

**Vertical fill is not optional (the `center: false` trap).** The Quarto decks render `center: false`, so a content slide's default is to top-align and leave the bottom half empty — a half-empty poll/definition/recap is the *silent default*, not an opt-in mistake. Counter it at the source: every content `<section>` should be a full-height flex column that distributes content (`height:100%; display:flex; flex-direction:column; justify-content:space-between`), with section-break/title/`.center` slides excluded (they self-center via the theme). This single rule lifts a deck from ~65% avg fill to ~85% and eliminates the top-jammed dead-rectangle look. **As of 2026-07 it lives in the shared `sds-reveal/sds.scss`** (promoted from the per-week copies, now WITH a 4.5% horizontal gutter and prose measure caps — see the "Design system" section of `SLIDE_VISUAL_QA.md` for the full token/discipline rules; cross-repo sync rule applies). New decks need little or no per-deck `<style>`; per-deck files carry only deliberate overrides + the r-stretch-fix JS. Poll slides get the boxed big-option layout (`.poll-slide`/`.poll-reveal`) from the theme; two-column slides vertically center their `.columns` so a short text column doesn't strand a void (that's the real `COLUMN-THIN` fix, alongside rebalancing). The audit was also fixed in two ways that matter: it now **reveals fragments before measuring** (polls no longer false-positive) and **measures at the deck's true 16:9 aspect** (was a 3:2 viewport that flagged phantom overflow); trust its numbers again.

### python-pptx loop (render → inspect → fix)

`python-pptx` places text boxes by absolute coordinates; without rasterized previews, overflow and misalignment are invisible to Claude. Every slide change must close the visual loop:

1. **Rebuild with `--preview`**: `python3 build_slides_weekN.py --preview` (optionally `--dpi 100` for faster iteration; default 150 is review quality). This runs LibreOffice headless to produce a PDF, then `pdf2image` + `poppler`'s `pdftoppm` to write `slides/sp26/preview/slideNN.png` (one per slide).
2. **Read the PNGs**: use the `Read` tool on `slides/sp26/preview/slideNN.png` for any slide touched. Check for text overflow past the yellow frame, overlap between text boxes, font-size inconsistency, low contrast against the dark bg, and agenda-column misalignment.
3. **One fix-and-verify cycle per issue**. Edit the shared-outline or the build script, rebuild with `--preview`, re-Read the affected slide. Do NOT iteratively nudge `Inches(...)` coordinates by guesswork past one cycle — if a slide still overflows after one deliberate fix, the template/helper in `sds_slides.py` is the problem, not the call site.
4. **For bulk/important audits, delegate to a fresh subagent.** Spawn an `Explore`-type Agent with instructions to Read every PNG in the preview dir and return a punch list of defects. A fresh context catches what the builder's pattern-matching misses (overflow, low contrast, broken alignment). Do this at minimum before a week is marked lecture-ready in its PLAN.md.

Required deps (already installed on this machine): `libreoffice`, `poppler-utils` (provides `pdftoppm`), Python `pdf2image` and `python-pptx`. The `render_previews()` method on `SDSDeck` implements the rendering step — reuse it in new weeks' build scripts rather than re-implementing.

## Before reporting a task complete

Since there's no test suite, verification means: (a) the PLAN.md structure is intact, (b) `TODO.md` reflects any status change, (c) nothing under `archive/canvas_export_sp25/` was touched, (d) if you edited inside `textbook/`, you followed *that* directory's CLAUDE.md (date frontmatter + code-block validation), and (e) if you rebuilt a week's slides, the build script ran cleanly, the generated `weekN-slides.pptx` + `weekN-speaker-notes.md` are both in sync with the shared-outline, AND every slide you touched has been re-rendered with `--preview` and visually inspected via the Read tool on the corresponding PNG.

(f) **For any Quarto/RevealJS week, the fill audit was re-run against the FINAL render and no slide actually CLIPS or is sparsely top-jammed.** Run `DECK=… OUT_DIR=… node scripts/audit_slide_fill.js --threshold 75`. The audit now (i) reveals every `.fragment` before measuring (so poll/answer/build-up slides are judged in their TRUE filled state — a flagged poll is a real defect, not the old hidden-fragment false positive) and (ii) measures at the deck's real aspect ratio (auto-read from Reveal's config; was hardcoded 3:2, wrong for the 16:9 decks). **The hard gate: no slide may genuinely CLIP** — verify the riskiest flagged slides by reading the rendered section's `scrollHeight` vs `clientHeight` (a true clip is `scrollHeight > clientHeight`); a slide that merely *fills to the bottom edge* (`fill≈100%`, no clip) is GOOD, not OVERFLOW. **No content slide may be top-jammed below ~70% fill** (the old failure: content pinned to the top with a dead rectangle below). The root cause was `center: false` + no fill mechanism; the fix is the deck-scoped "fill-the-slide" flex layout (`section{height:100%; display:flex; justify-content:space-between}` for content slides; poll-option boxes; `.columns` vertically centered) — see the qmd `<style>` block. **A residual BOTTOM-GAP in the 70–75% band is allowed only with a per-slide note; a blanket "remaining flags are benign BOTTOM-GAP / just the polls" dismissal is forbidden** — that exact sentence is what let half-empty slides ship across Weeks 6–7.

(g) **Pedagogical-structure audit (the Week-9 post-mortem gate — visual QA alone misses structural defects).** The fill audit checks density; it does NOT check whether the lecture coheres. Before a Quarto week is lecture-ready, run a separate structural pass (a checklist, and for a major build a fresh-subagent review of the qmd) confirming:
- a **single organizing framework is named early and *referenced* (not re-derived)** throughout — not a topic-tour;
- **every named concept / phenomenon / acronym is defined at first use** (the extended rule above — concepts, not just symbols), and **every concept used is taught earlier or defined in-deck** (no GAN-style smuggling) — grep student-facing lines (outside `::: {.notes}`) for undefined load-bearing terms;
- **no idea or equation is re-derived more than once** (establish-then-reference);
- where the topic admits it, the deck delivers a **"framework → work each unknown piece"** structure;
- the **shared-outline's framing directives actually made it into the built deck** (the Week-9 outline said "name the POMDP frame in Block 2"; the delivered deck didn't, and nothing caught it). Diff intended-spine vs built-spine.
This gate exists because Week 9 passed visual QA yet failed on framework coherence, an undefined "theory of mind", untaught GANs, and repetition — all invisible to a density audit.
