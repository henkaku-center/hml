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
- **Define technical terms/acronyms at first use on slides.** Whenever a new technical term, notation, or acronym first appears in a deck (PMF, PDF, MLE, Σ, $\binom{n}{k}$, indicator, posterior, likelihood, etc.), its first on-slide appearance must include a definition — either inline or on the immediately preceding slide. This includes symbols: if Σ, ∫, or $\binom{n}{k}$ shows up in a formula before it has been defined, either define it in a dim caption beneath the formula or add a one-line notation-lock-in slide before it. If the term reappears after a long gap (e.g. a block break, or > ~15 min of lecture time), briefly redefine it in situ rather than assuming retention. When porting SP25 content, audit for the "suddenly appears without definition" pattern — it is the most common source of student confusion and red-team hits. Applies to slides and speaker notes; the textbook has its own introduction order.

## Cross-cutting SP26 themes (affect almost every edit)

These show up repeatedly in PLAN TODOs and drive most new work:

1. **GenJAX integration.** All four programming assignments (clusters, generalization, mc, rl) need GenJAX ports or a GenJAX option. Week 2 homework introduces GenJAX via textbook T2 Ch 0-1. Weeks 6, 8, 11 are flagged for GenJAX exercises.
2. **Textbook chapter mapping.** Each week's PLAN.md lists the textbook chapters to assign. When adding/moving content, update both the PLAN and the textbook cross-reference.
3. **Contemporary ML content** (Weeks 11-13): LLMs, foundation models, RLHF, alignment, scaling laws, interpretability, transformers. Week 13 (ethics) should pick up recent AI-safety developments.

## Common operations

- **Find SP25 source for a week**: each PLAN.md names the original slide files (e.g. `Week00_BasicBayes.pptx`) and wiki pages. They're already copied into `course/weekNN_…/slides/` and `wiki_pages/`; the originals live in `archive/canvas_export_sp25/web_resources/`.
- **Find a quiz**: `course/quizzes/README.md` maps week → quiz name. The actual Canvas QTI XML is under `archive/canvas_export_sp25/` as `g<hash>.xml` files — identify by opening and reading the title, not by filename.
- **Landing page**: `docs/index.html` is a single-file static site served by GitHub Pages. Assets in `docs/assets/` (Chiba Tech SDS logos) were fetched via pre-approved `curl` commands in `.claude/settings.local.json`.
- **Readings:** `course/readings_map.yml` is the source of truth for weekly readings and paper-presentation assignments. Weeks 1 and 2 are populated; Weeks 3–12 are stubs to fill in during the readings-modernization planning session.

## How to build a week (SP26 lecture artifacts)

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

## Slide visual-QA loop (render → inspect → fix)

`python-pptx` places text boxes by absolute coordinates; without rasterized previews, overflow and misalignment are invisible to Claude. Every slide change must close the visual loop:

1. **Rebuild with `--preview`**: `python3 build_slides_weekN.py --preview` (optionally `--dpi 100` for faster iteration; default 150 is review quality). This runs LibreOffice headless to produce a PDF, then `pdf2image` + `poppler`'s `pdftoppm` to write `slides/sp26/preview/slideNN.png` (one per slide).
2. **Read the PNGs**: use the `Read` tool on `slides/sp26/preview/slideNN.png` for any slide touched. Check for text overflow past the yellow frame, overlap between text boxes, font-size inconsistency, low contrast against the dark bg, and agenda-column misalignment.
3. **One fix-and-verify cycle per issue**. Edit the shared-outline or the build script, rebuild with `--preview`, re-Read the affected slide. Do NOT iteratively nudge `Inches(...)` coordinates by guesswork past one cycle — if a slide still overflows after one deliberate fix, the template/helper in `sds_slides.py` is the problem, not the call site.
4. **For bulk/important audits, delegate to a fresh subagent.** Spawn an `Explore`-type Agent with instructions to Read every PNG in the preview dir and return a punch list of defects. A fresh context catches what the builder's pattern-matching misses (overflow, low contrast, broken alignment). Do this at minimum before a week is marked lecture-ready in its PLAN.md.

Required deps (already installed on this machine): `libreoffice`, `poppler-utils` (provides `pdftoppm`), Python `pdf2image` and `python-pptx`. The `render_previews()` method on `SDSDeck` implements the rendering step — reuse it in new weeks' build scripts rather than re-implementing.

## Before reporting a task complete

Since there's no test suite, verification means: (a) the PLAN.md structure is intact, (b) `TODO.md` reflects any status change, (c) nothing under `archive/canvas_export_sp25/` was touched, (d) if you edited inside `textbook/`, you followed *that* directory's CLAUDE.md (date frontmatter + code-block validation), and (e) if you rebuilt a week's slides, the build script ran cleanly, the generated `weekN-slides.pptx` + `weekN-speaker-notes.md` are both in sync with the shared-outline, AND every slide you touched has been re-rendered with `--preview` and visually inspected via the Read tool on the corresponding PNG.
