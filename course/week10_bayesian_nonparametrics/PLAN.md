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
**SP26 rebuild in progress.** Quarto/RevealJS port underway (last week still on legacy PPTX). Plan approved;
see `week10-shared-outline.md` (SOURCE OF TRUTH — Block 1 fully authored incl. speaker notes). Bias-variance
critical review done (keep/fix/cut recorded in the outline). Widget 4 (bias-variance / double-descent
explorer) BUILT and QA-verified. Remaining: Widgets 1–3, GenJAX backbones, the qmd (Blocks 1–8), LDA toy,
verification gate.

## SP26 Artifacts
- `week10-shared-outline.md` — timing-free outline; Block 1 authored with verbatim speaker notes.
- `widgets/bias-variance-explorer.html` — Widget 4 (Task 6). Two panels; right panel has a model selector:
  *closed-form min-norm* (ridge-λ slider + ‖weights‖₂ panel) and *neural net + GD* (hidden-units H ×
  GD-iterations T). QA screenshots in `widgets/preview/` (ridgeless/ridge, NN early-stop/trained).
- `slides/sp25_reference/` — legacy `Week10_BNP.pptx` (+ extra slides, PDF, transcript), reference only.

## TODOs
- [ ] Author `week10-slides.qmd` + `week10-styles.html` (Block 1 notes from the outline → `::: {.notes}`).
- [ ] Build Widgets 1 (DPMM/KDE/GMM), 2 (stick-breaking/Pólya), 3 (CRP seating).
- [ ] GenJAX backbones + figures; LDA toy + topic-emergence viz.
- [ ] Verification gate (fill audit, structure, term-definition grep, drive all widgets, JA spot-check).
- [ ] (Deferred) Create the GenJAX DPMM assignment/exercise.
