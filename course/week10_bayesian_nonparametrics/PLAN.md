# Week 10 (Jul 3): Bayesian Nonparametrics

## Topics
- Bias-variance tradeoff
- Bayesian nonparametric models
- Dirichlet process mixture models

## SP25 Content
- **Slides:** Week10_BNP.pptx, Week10_BNPWExtraSlides.pptx (+ PDF)
- **Transcript:** Week10_BiasVarianceBNPTranscript.docx
- **Wiki pages:** bias-variance-and-bnp.html
- **Quiz:** ~~Social Cognition and Inverse Reinforcement Learning~~ (likely a Week-9 carryover — audit the
  clustering / Gaussian-Bayes quizzes for pause-and-predict items during Task 8; see `course/quizzes/README.md`)

## Textbook Chapters
- **Prerequisite (assign):** intro2 Ch5 (mixture models / GMM+EM on bento weights), Ch6 (DPMM).
- **Phase 2 (separate session) — revise toward the lecture into 3 GenJAX-modernized chapters:**
  *Bias-Variance Dilemma* (new), *Discrete Bayesian Nonparametrics* (revise+expand Ch6),
  *Continuous Bayesian Nonparametrics* (new — GPs/NNGP/NTK/neural processes/RAG). Phase-1 artifacts
  (widgets, GenJAX backbones, figures) are built dual-homed so the revision is a port, not a re-derivation.

## GenJAX Integration
- `genjax_dpmm.py` (reuse Ch6 backbone) — DPMM code slide + figure (Block 5).
- `genjax_biasvariance.py` — polynomial hypothesis-space demo + double-descent (Block 1 / Phase-2 ch).
- `genjax_gp.py` — GP regression (Block 7 / Phase-2 ch).
- (Deferred, non-blocking: the standalone GenJAX DPMM *assignment/exercise* — see TODOs.)

## Contemporary ML Notes
- **Block 1 modern coda:** double descent (Belkin 2019; Nakkiran 2019), implicit bias / min-ℓ₂-norm,
  norm↔prior dictionary, ridge as explicit twin (Nakkiran 2020), early stopping as implicit twin,
  benign overfitting (Bartlett 2020). All interactive via Widget 4.
- **Block 7:** GP→NN (NNGP/NTK), neural processes, nonparametric memory (RAG / kNN-LM).

## Status
**SP26 rebuild — deck BUILT & verified.** Full Quarto/RevealJS port done: `week10-slides.qmd` (51 slides,
8 blocks, bilingual EN↔JA), all **4 widgets** embedded live, **8 figures**, Block-1 speaker notes in place.
Verified: builds clean; fill audit 0 clips / 0 overflow (12 slides at 70–74%, centered/acceptable); JA toggle
works; widgets run in-deck. Source of truth: `week10-shared-outline.md`. **Remaining:** GenJAX backbones
(optional code slide / Phase-2 dual-home), nudge the 70–74% slides, sync root `TODO.md`, Phase-2 textbook.

## SP26 Artifacts
- `week10-shared-outline.md` — timing-free outline; Block 1 authored with verbatim speaker notes.
- **All 4 widgets built & QA-verified** (self-contained HTML/Canvas, SDS theme; previews in `widgets/preview/`):
  - `widgets/dpmm-kde-gmm.html` — Widget 1 (centerpiece). DPMM (collapsed CRP Gibbs) vs KDE vs fixed-K GMM on
    click-to-add bento weights; α drives DPMM cluster count; K=2 GMM misses the 275 g outlier.
  - `widgets/stick-breaking-polya.html` — Widget 2. Stick-breaking + Pólya-urn, two views of DP(α).
  - `widgets/crp-seating.html` — Widget 3. CRP seating animation; rich-get-richer; α slider.
  - `widgets/bias-variance-explorer.html` — Widget 4. Two panels; right has a model selector: *closed-form
    min-norm* (ridge-λ slider + ‖weights‖₂ panel) and *neural net + GD* (hidden-units H × GD-iterations T).
- `make_figures.py` — Block-1 teaching figures (`images/bv_three_fits.png`, `bv_ucurve.png`,
  `double_descent.png`), dark SDS theme, verified.
- `slides/sp25_reference/` — legacy `Week10_BNP.pptx` (+ extra slides, PDF, transcript), reference only.

## TODOs
- [ ] Author `week10-slides.qmd` + `week10-styles.html` (Block 1 notes from the outline → `::: {.notes}`).
- [ ] Build Widgets 1 (DPMM/KDE/GMM), 2 (stick-breaking/Pólya), 3 (CRP seating).
- [ ] GenJAX backbones + figures; LDA toy + topic-emergence viz.
- [ ] Verification gate (fill audit, structure, term-definition grep, drive all widgets, JA spot-check).
- [ ] (Deferred) Create the GenJAX DPMM assignment/exercise.
