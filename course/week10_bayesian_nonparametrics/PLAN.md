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
**All three backbones BUILT & validated (jax 0.5.3 / genjax 0.10.3, run clean):**
- `genjax_dpmm.py` ✅ — `@gen` stick-breaking DPMM + slice-Gibbs inference on bento weights; discovers
  3 clusters incl. the lone 275 g outlier. Figure `images/genjax_dpmm.png`. Drives the new
  **"The DPMM, as a GenJAX program"** code slide (Block 5, after "How is a DPMM actually fit?").
- `genjax_biasvariance.py` ✅ — `@gen` Bayesian polynomial regression (ridge prior) → bias-variance
  U-curve (sweet spot deg 3) + high-dim (D=180) double descent (spike exactly at p=n=20, second
  descent). Figures `images/genjax_biasvariance.png`, `images/genjax_double_descent.png`. Dual-homed
  for the Phase-2 Bias-Variance chapter (Block 1 already ships matplotlib twins).
- `genjax_gp.py` ✅ — `@gen` GP prior (Cholesky trick over iid normals) + closed-form posterior; RBF
  kernel; interpolates data up to noise. Figure `images/genjax_gp.png`. Dual-homed for the Phase-2
  Continuous-BNP chapter (Block 7 already ships a matplotlib twin).
- (Deferred, non-blocking: the standalone GenJAX DPMM *assignment/exercise* — see TODOs.)

## Contemporary ML Notes
- **Block 1 modern coda:** double descent (Belkin 2019; Nakkiran 2019), implicit bias / min-ℓ₂-norm,
  norm↔prior dictionary, ridge as explicit twin (Nakkiran 2020), early stopping as implicit twin,
  benign overfitting (Bartlett 2020). All interactive via Widget 4.
- **Block 7:** GP→NN (NNGP/NTK), neural processes, nonparametric memory (RAG / kNN-LM).

## Status
**SP26 rebuild — deck BUILT & verified; GenJAX backbones DONE.** Full Quarto/RevealJS port: `week10-slides.qmd`
(56 slides, 8 blocks, bilingual EN↔JA), all **4 widgets** embedded live, **13 figures**, Block-1 speaker
notes in place. Verified: builds clean; fill audit 0 clips / 0 overflow; JA toggle works; widgets run in-deck.
**All 3 GenJAX backbones built & validated** (`genjax_dpmm/biasvariance/gp.py`) + a **DPMM-as-GenJAX-program**
code slide (Block 5). Closing **GP↔bias-variance synthesis** added (Block 8: "It all comes home" figure +
"One question, three answers"), with the GP→NN block (Neal/NNGP/NTK) detailed in notes. Source of truth:
`week10-shared-outline.md`. **Remaining:** Phase-2 textbook (3 chapters; backbones now built & dual-homed).

## SP26 Artifacts
- `week10-shared-outline.md` — timing-free outline; Block 1 authored with verbatim speaker notes.
- **All 4 widgets built & QA-verified** (self-contained HTML/Canvas, SDS theme; previews in `widgets/preview/`):
  - `widgets/dpmm-kde-gmm.html` — Widget 1 (centerpiece). DPMM (collapsed CRP Gibbs) vs KDE vs fixed-K GMM on
    click-to-add bento weights; α drives DPMM cluster count; K=2 GMM misses the 275 g outlier.
  - `widgets/stick-breaking-polya.html` — Widget 2. Stick-breaking + Pólya-urn, two views of DP(α).
  - `widgets/crp-seating.html` — Widget 3. CRP seating animation; rich-get-richer; α slider.
  - `widgets/bias-variance-explorer.html` — Widget 4. Two panels; right has a model selector: *closed-form
    min-norm* (ridge-λ slider + ‖weights‖₂ panel) and *neural net + GD* (hidden-units H × GD-iterations T).
- `make_figures.py` — teaching figures (`images/bv_three_fits.png`, `bv_ucurve.png`, `double_descent.png`,
  `dp_g0_to_g.png`, `bring_it_home.png`), dark SDS theme, verified.
- **`genjax_dpmm.py` / `genjax_biasvariance.py` / `genjax_gp.py`** — validated GenJAX backbones (run clean
  under jax 0.5.3 / genjax 0.10.3), each writing its figure(s) to `images/genjax_*.png`. Dual-homed for the
  Phase-2 textbook chapters; `genjax_dpmm.py` also drives the in-deck "DPMM, as a GenJAX program" code slide.
- `slides/sp25_reference/` — legacy `Week10_BNP.pptx` (+ extra slides, PDF, transcript), reference only.

## TODOs
- [ ] Author `week10-slides.qmd` + `week10-styles.html` (Block 1 notes from the outline → `::: {.notes}`).
- [ ] Build Widgets 1 (DPMM/KDE/GMM), 2 (stick-breaking/Pólya), 3 (CRP seating).
- [ ] GenJAX backbones + figures; LDA toy + topic-emergence viz.
- [ ] Verification gate (fill audit, structure, term-definition grep, drive all widgets, JA spot-check).
- [ ] (Deferred) Create the GenJAX DPMM assignment/exercise.
