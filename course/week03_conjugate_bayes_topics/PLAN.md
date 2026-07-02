# Week 3 (May 15): Conjugate Bayes + Topics

Note: No class May 1 or May 8. This is the first class after the two-week skip.

## Prerequisites from Week 2
Week 2 (April 24) now lays down the full continuous-probability backbone:
- Expected value, Bernoulli, Binomial (Block 5)
- PMF → PDF, the Gaussian formula, Bayes with a continuous likelihood (Block 6)
- **A complete worked Gaussian-Gaussian conjugate update** (Block 7)
  — prior μ ~ N(500, 20²), one observation 510g, posterior ≈ N(503.3, 16.6²).
  Week 3 opens by picking up from here.

This means Week 3 does NOT need to re-teach continuous probability or Gaussians. It opens at the level of "conjugacy as a pattern."

## Topics
- Conjugacy as a pattern: prior × likelihood → posterior in the same family
- Beta-Binomial (for inferring p from counts; back to the bento 70/30 split)
- Gaussian-Gaussian with N observations and unknown σ (Week 2 did known σ only)
- Dirichlet-Multinomial if time (multinomial bentos: tonkatsu / hamburger / curry)
- Mixture modeling teaser (full treatment pushed later)

## SP25 Content
- **Slides:** NONE — need to create. Week 2's build-up style (sequential slides for math reveals) is the canonical approach; use the same pattern.
- **Wiki pages:** `wiki_pages/` (to be populated from SP25 export): discrete-distribution.html, binomial-distribution.html, beta-distribution.html, beta-binomial-posterior-update.html, discrete-multinomial-and-dirichlet-distributions.html, mixture-modeling.html
- **Quiz:** Intro to Prob Theory Quiz 2

## Textbook Chapters
- Bk: bayesian learning (`learning/bayesian-learning.md`) — REQUIRED before class. Picks up directly from Week 2's Block 7.
- Bk: glossary (`foundations/glossary.md`) — review

## GenJAX Integration
- Bk: first model, traces (`genjax/`) (students' own time)
- Consider a short live demo: `beta_binomial_update()` generative model. Optional.

## Contemporary ML Notes
None this week.

## Status
**Lecture-ready in EN+JA.** Quarto qmd (`week3-slides.qmd`) replaces the python-pptx pattern used by Week 1 — Week 3 is the first SP26 deck built directly in Quarto/RevealJS. Pinned to the synced shared `sds-reveal/sds.scss` (five-tier sizing). Fill-audit run via `scripts/audit_slide_fill.js`; 3 remaining flags are sparse-content slides in the acceptable 60–75% fill band per `SLIDE_VISUAL_QA.md`. JA retrofit covers 17 concept-introducing slides; build-up math reveals and worked-example walkthroughs stay EN-only.

## SP26 artifacts
- `week3-slides.qmd` — single-source deck (no shared-outline split; deck is small enough that the outline is implicit in section headers + speaker notes)
- `week3-slides.html` — generated; do not hand-edit
- `week3-audit/slide-fill.json` — audit history
- `wiki_pages/` — SP25 Canvas snapshots (reference only)

## TODOs
- [x] Build SP26 Week 3 artifacts (qmd → RevealJS, audit-passed)
- [x] Copy relevant wiki pages from `archive/canvas_export_sp25/web_resources/wiki_content/` into `wiki_pages/`
- [x] Add 3 polls (1 self-authored conjugacy fail-mode + 2 adapted from SP25 "Gaussian and Binomial Bayes" quiz)
- [x] EN↔JA toggle on 17 concept slides
- [x] Pedagogical density review — split conjugacy def (1→2 slides), Beta-Binomial update (1→3 slides with explicit derivation), Gaussian-N formula (1→3 slides: notation lock-in / precision / posterior mean); fixed `p`/`θ` double-use; defined Σ before first use; filled in Sequential-update ellipsis; added $\vec{\alpha}$ shorthand definition
- [x] Added 6-slide instructor-led presentation block on **Griffiths & Tenenbaum (2001) "Randomness and coincidences"** (15 min, replaces dropped Dirichlet-Multinomial block; Dirichlet pattern still visible in the summary table). Restructured from SP25 student PPTX (`archive/.../old_paper_presents/GriffithsTenenbaum2001.pptx`) around the likelihood-ratio→conjugacy connection.
- [ ] Optional: GenJAX `beta_binomial_update()` live demo (per PLAN — currently no slide for it; consider for next iteration)
