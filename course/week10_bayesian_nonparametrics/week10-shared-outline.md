# Week 10 — Bias-Variance & Bayesian Nonparametrics — shared outline (SOURCE OF TRUTH)

**Lecture date:** 2026-07-03 (Fri). **Format this week: ASYNC / RECORDED** — no fixed slot, no
timing contingencies. Optimize for a clean recorded walkthrough; "polls" become *pause-and-predict*
beats (ask → pause → reveal), not live audience polling.

**How to use this file:** edit the outline FIRST, then build `week10-slides.qmd` from it (speaker notes
go into `::: {.notes}` blocks, copied from the **Speaker notes** subsections below). The qmd and any
generated notes file are DERIVED from this outline. Theme line for the qmd:
`theme: [dark, ../../sds-reveal/sds.scss]`; `center: false`; `include-in-header: week10-styles.html`.

**Organizing framework (name once in Block 1, then REFERENCE — never re-derive):**
> *How complex should the model be? Don't guess the complexity — let the data decide.*
Block 1 (bias-variance + double descent) poses the question and shows the two modern answers
(deep-learning: go huge + regularize; **Bayesian nonparametrics: grow the model with the data under an
explicit prior**). Blocks 2-8 build the BNP answer: one machine — a prior over partitions/measures —
reused to define many models.

---

## Widget inventory (all self-contained HTML/Canvas, SDS dark theme, dual-homed course + textbook)

1. **`widgets/dpmm-kde-gmm.html`** — centerpiece. **BUILT & QA-verified.** Click the bento-weight axis
   (250–600 g) to add points; three live density curves: **DPMM** (collapsed CRP Gibbs, modal-K readout),
   **KDE** (Gaussian kernel, Silverman default), **fixed-K GMM** (EM, k-means++, adjustable K). Auto-seed
   8×350 + 6×500 + a 275 g outlier → DPMM finds 3 clusters, K=2 GMM misses the outlier (mean dragged to
   340). α drives DPMM cluster count (0.1→2, 5→7). Preview: `widgets/preview/w1-dpmm-default.png`.
2. **`widgets/stick-breaking-polya.html`** — **BUILT & QA-verified.** Drag α; the unit stick breaks
   (βₖ~Beta(1,α)) into weights (top), paired with a Pólya-urn ball fill (bottom). Weights sum to 1; α=0.2→2
   pieces, α=5→42. Preview: `widgets/preview/w2-stickbreaking-polya.png`.
3. **`widgets/crp-seating.html`** — **BUILT & QA-verified.** Customers seat one-by-one (existing ∝ nₖ,
   new ∝ α), with a live next-customer probability bar; K grows; rich-get-richer visible. Valid partitions
   (Σnₖ=total); α=0.2→1 table, α=1→2, α=5→10. Seat-one / Auto-seat / Reset. Preview:
   `widgets/preview/w3-crp-seating.png`.
4. **`widgets/bias-variance-explorer.html`** — **BUILT (Task 6).** Two linked panels. LEFT: classical
   1-D polynomial bias-variance (degree slider, truth + per-dataset spaghetti + avg fit, live bias²/var
   readout). RIGHT: double descent past the interpolation threshold, with a **model selector**:
   - **"closed-form min-norm"** — isotropic Gaussian model; **ridge-λ slider** flattens the spike live
     (peak test 337 → 1.35 at λ≈0.3); a **‖weights‖₂ panel** spikes at p=n.
   - **"neural net + GD"** — a real 1-hidden-layer net (random features, output trained by GD); sweep
     **hidden units H**, set **GD iterations T**. Small T = flat (early stopping); large T = spike at H=n.
   QA-verified in-browser (see `widgets/preview/`). Reused for Block 1 slides B1.7–B1.13 and Phase-2
   textbook Ch "Bias-Variance Dilemma".

---

## Spine (8 blocks)

1. **Bias-variance → double descent** — pose the framing question; classical U-curve (the half they teach)
   + the modern coda (double descent, implicit/explicit regularization). Bridge to "let the data decide."
2. **Finite mixtures → "how many clusters?"** — recap GMM on bento weights; the K problem; Widget 1 fixed-K.
3. **CRP** — a law over partitions; rich-get-richer; α. Widget 3.
4. **CRP → Dirichlet Process (three lenses)** — Pólya urn (predictive marginal) / stick-breaking / the random
   measure G~DP(α,G₀) (a.s. discrete → why it clusters). Widget 2. Fix the SP25 Pólya=DP conflation.
5. **DPMM** — DP prior + Gaussian likelihood; Widget 1 full 3-way; the parametric/nonparametric/BNP slide;
   inference conceptually (collapsed Gibbs / variational); honest "niche now" + K-posterior caveat.
6. **Building-block move** — "replace a finite parameter with a random measure." LDA worked toy +
   topic-emergence viz (LDA = finite-Dirichlet; HDP-LDA = nonparametric). IBP = feature sibling (compressed).
7. **Gaussian processes + contemporary frame (promoted)** — prior over functions; kernels; GP→NN
   (NNGP/NTK); neural processes; nonparametric memory (RAG/kNN-LM).
8. **Recap — the one picture** — parametric→nonparametric→BNP; one machine → many models; callback to B1.

---

## BLOCK 1 — Bias-Variance Dilemma → Double Descent  *(fully authored)*

**Goal:** pose the organizing question and answer the "is the textbook U-curve still the whole story?"
honestly. Keep what the professor likes (the SP25 bias-variance build), correct/extend it with the modern
picture, and make it interactive via Widget 4.

### Critical-review outcome (Task 2 — what we keep / fix / cut, decided with the professor)
- **KEEP:** the SP25 build — mapping to learn → hypothesis spaces (linear/quad/high-degree) → train-vs-test
  error → overfitting → the decomposition `E[(ŷ−y)²]=Bias²+Var+σ²` → high-bias vs high-variance two-column →
  sample-size effect → "the moral" U-curve. This is clean, correct, and well-paced; port it tightened
  (bullets, not prose paragraphs).
- **FIX:** attribute the decomposition (Geman, Bienenstock & Doursat 1992). Define every symbol at first use
  (ŷ, σ², Bias², Variance, the expectation E over datasets). The SP25 deck stated the U-curve as the *whole*
  story — that is the one substantive correctness gap (see below).
- **ADD (the modern coda):** double descent (Belkin et al. 2019 PNAS; Nakkiran et al. 2019); implicit bias /
  min-ℓ₂-norm; the norm↔prior dictionary; ridge as the explicit twin; early stopping as the implicit twin;
  benign overfitting (Bartlett et al. 2020). The classical U-curve is **correct but incomplete** — it is the
  *left half* of the picture. Retire only the claim "more capacity always eventually hurts."

### Slide sequence
- **B1.0** Section break: *"How complex should the model be?"* — name the framing question for the whole week.
- **B1.1** The setup: a mapping to learn (x → y regression). Three hypothesis spaces: **linear / quadratic /
  high-degree polynomial**. [figure: three fits to the same points]
- **B1.2** Train error vs **prediction (test) error**; the overfitting gap. [figure]
- **B1.3** The decomposition: `E[(ŷ−y)²] = Bias² + Variance + σ²` (Geman, Bienenstock & Doursat 1992).
  Define each term in a dim caption. Bias = how far the *average* fit is from truth; Variance = how much the
  fit *wobbles* across datasets; σ² = irreducible noise.
- **B1.4** High-bias vs high-variance — **two-column** (underfit straight line | overfit wiggle with fanned
  spaghetti). [figure]
- **B1.5** Sample-size effect: n=10 vs n=100 (more data shrinks variance, lets you afford more complexity).
  [figure]
- **B1.6** The classical moral: **the U-curve** (test error = bias² + variance, minimized at intermediate
  complexity). [figure: classic U]
- **B1.7** **WIDGET 4 (left panel), live** — drag the polynomial-degree slider; watch bias fall and variance
  rise; the live bias²/var readout. *(This is the SP25 story, now playable.)*
- **PAUSE-AND-PREDICT:** *"Keep adding parameters past the point where the model can fit every training point
  exactly — does test error keep rising, plateau, or fall again?"* (pause) → reveal on B1.8.
- **B1.8** *"That U-curve is only half the story."* **Double descent**: extend the x-axis past the
  **interpolation threshold** (where #parameters = #training points, p = n). Test error rises to a spike at
  p = n, then **descends a second time** (Belkin et al. 2019 PNAS; Nakkiran et al. 2019). [figure:
  extended-axis double-descent curve]
- **B1.9** Why the spike at p = n? **WIDGET 4 (right panel, "closed-form min-norm"), live.** With exactly as
  many knobs as data points, the model is forced to thread *all* n noisy points with no slack → a wild,
  huge-norm solution → variance explodes. (Drive capacity p to n; watch the test spike AND the ‖weights‖₂
  panel spike together.)
- **B1.10** Past the threshold there are **infinitely many** parameter settings that fit the training data
  perfectly. Which one does the learner pick? **Two-column:** "any interpolating solution" vs "the *minimum-
  ℓ₂-norm* one." The solver (pseudoinverse / GD-from-zero) picks the smallest-norm interpolant → smooth →
  generalizes. **This choice is an implicit prior.**
- **B1.11** The **norm ↔ prior dictionary**: minimizing **‖β‖₂²** (Euclidean/ℓ₂) ⇔ a **Gaussian prior** on the
  weights (ridge); minimizing **‖β‖₁** (ℓ₁) ⇔ a **Laplace prior** (lasso → sparsity). Min-norm GD picks the
  **ℓ₂ / Gaussian** one — *not* L1.
- **B1.12** **Ridge regression = the explicit twin.** `β_λ = (ΦᵀΦ + λI)⁻¹ Φᵀy`. λ→0⁺ recovers the min-norm
  interpolant (the spike); a well-chosen λ>0 **removes the spike** (Nakkiran et al. 2020, "Optimal
  Regularization Can Mitigate Double Descent"). **WIDGET 4 (ridge-λ slider), live** — drag λ up; the peak
  collapses 337 → 1.35; push λ too far and the optimum slides back to low capacity (classical tradeoff
  returns).
- **B1.13** **Early stopping = the implicit twin.** A real network trained by GD: stop early and you never
  reach the wild interpolant — early stopping ≈ ridge with λ ∝ 1/(η·T) (Yao, Rosasco & Caponnetto 2007; Ali
  et al. 2019). **WIDGET 4 ("neural net + GD" selection), live** — sweep hidden units H; set GD iterations T.
  Small T → flat curve, small weights (no double descent); large T → spike at H = n. *(There is also an
  epoch-wise double descent — Nakkiran et al. 2019 — same idea on the iteration axis.)*
- **B1.14** **Benign overfitting** (Bartlett et al. 2020): in high dimensions, a model can interpolate the
  *noise* and still generalize, because the geometry spreads noise-fitting across many low-variance
  directions. **Honest caveats:** double descent needs the right regime (high-dimensional, roughly isotropic
  features); 1-D correlated features (Widget 4's *left* panel) cannot show it — itself a teaching point. The
  classical U-curve is correct but incomplete.
- **B1.15** **Bridge:** so "how complex should the model be?" has two principled modern answers — (a) deep
  learning: make it huge and let implicit/explicit regularization pick a simple interpolant; (b) **Bayesian
  nonparametrics: let the model grow with the data under an explicit prior.** The rest of today builds (b).
  → Block 2.

### Figures for Block 1  *(all DONE — `make_figures.py`, verified onto the dark bg)*
- `images/bv_three_fits.png` — DONE: linear/quad/degree-12 fits to the same noisy points (underfit/good/overfit).
- `images/bv_ucurve.png` — DONE: classic bias²+variance U-curve with the sweet spot marked.
- `images/double_descent.png` — DONE: extended-axis (p/n) test-error curve, classical U dashed on the left,
  p=n spike + second descent labelled ("min-norm = implicit prior").
- Widget 4 screenshots (`widgets/preview/`): ridgeless vs ridge; NN early-stop vs trained — static fallbacks
  for the widget slides.

### >>> SPEAKER NOTES — Block 1 modern coda (paste verbatim into the qmd `::: {.notes}` on B1.8–B1.15) <<<
*(Written for the recorded delivery. These are the "ultimate speaker notes" capturing the double-descent /
implicit-prior / ridge / early-stopping explanation. One language — instructor-only, EN.)*

**B1.8 — double descent.** "Everything up to here is the bias-variance story you already know, and it's
correct — as far as it goes. But it stops at the point where the model has just enough parameters to fit the
training data. For decades we never looked to the *right* of that point, because why would you use more
parameters than data? Modern machine learning lives entirely to the right of it. When you keep adding
parameters, the test error does something the U-curve says is impossible: after spiking, it comes *back
down*, often to a new minimum lower than the classical sweet spot. Belkin and colleagues named this **double
descent** in 2019; Nakkiran and colleagues showed the same year that it shows up in real neural networks and
even in the number of training epochs. The classical U-curve isn't wrong — it's the *left half* of this
picture. The only thing we retire is the slogan 'more capacity always eventually hurts.'"

**B1.9 — why the spike.** "The peak is at the **interpolation threshold**: the width where the model has
*exactly* as many free parameters as it has training points — I'll call that p = n. Think about what that
means. With exactly n knobs and n noisy points, there's a unique setting that threads every single point with
no slack at all. To pass through noise exactly, that unique solution has to be wild — enormous coefficients
swinging up and down between the points. That's what the right panel of the widget shows: at p = n the test
error spikes, and the new purple panel — the *size* of the weight vector — spikes with it. The model is
contorting itself to interpolate, and the contortion is what kills generalization."

**B1.10–B1.11 — the resolution: an implicit prior.** "Now go *past* p = n. Once you have more parameters than
data, there's no longer a unique solution — there are infinitely many parameter settings that fit the
training data perfectly. So the question stops being 'can it fit?' and becomes '*which* perfect fit does the
learner choose?' And here's the key idea for the whole rest of the course. The standard solver — the
pseudoinverse, or gradient descent started from zero — doesn't pick a random interpolant. It picks the one
with the **smallest weights**: the minimum-norm interpolant. Smallest weights means smoothest, least
contorted, so it generalizes. And 'prefer the smallest-norm solution' is not a neutral act — it's a **prior**.
"
"Here's the dictionary, because it's worth pinning down and it answers the question some of you are asking.
Penalizing the **squared Euclidean length of the weights, ‖β‖₂²** — the ℓ₂ norm — is *exactly* equivalent to
putting a **Gaussian prior** on the weights and taking the MAP estimate. That's ridge regression. Penalizing
the **ℓ₁ norm, ‖β‖₁** — the sum of absolute values — corresponds to a **Laplace prior**, and that's lasso,
which produces *sparse* solutions. They're different priors with different fingerprints. Gradient descent
from zero on a least-squares problem provably converges to the minimum-**ℓ₂** solution — the **Gaussian**-prior
one, the Euclidean-shortest one. So when I said 'a prior sneaks in' — it does, and it's specifically the
Gaussian / ℓ₂ prior, not the L1/sparsity one. (If we'd trained a different way we could get the L1 solution,
but plain GD-from-zero gives you ℓ₂.)"

**B1.12 — ridge, the explicit twin.** "If a hidden Gaussian prior is doing the work, we can also add it *on
purpose* and dial it. That's ridge: instead of just minimizing training error, minimize training error plus
λ·‖β‖₂². The solution is β = (ΦᵀΦ + λI)⁻¹Φᵀy — that little +λI is the entire change. As λ → 0 you get the
min-norm interpolant back, spike and all. Turn λ up and watch the widget: the spike at p = n **flattens** —
in our setup the peak test error drops from about 337 to about 1.3 with a modest λ. Nakkiran and colleagues
proved this in 2020: the *right* amount of ridge removes double descent entirely — the curve becomes a single
gentle bowl. Push λ *too* far, though, and you over-shrink: the best capacity slides back down to small
models and the old bias-variance tradeoff reappears. So ridge λ is a knob that interpolates between 'trust
the data, let it interpolate' and 'trust the prior, keep the weights small.'"

**B1.13 — early stopping, the implicit twin (this is the intuition some of you had).** "There's a second way
the same prior sneaks in, and it's the one a lot of people guess first: **just don't train as long.** Switch
the widget to 'neural net + GD' — now it's a real one-hidden-layer network, and the two knobs are the number
of hidden units and the number of gradient-descent steps T. Watch what T does. Train for only a handful of
steps and the double-descent spike *isn't there* — the curve is flat and the weights stay small. Train for
ten thousand steps and the spike snaps back at the interpolation threshold. Why? Gradient descent from zero
grows the weights gradually; stopping early is mathematically almost the same as ridge, with an effective λ
of about 1/(η·T) — more steps, weaker prior. Yao, Rosasco and Caponnetto worked this equivalence out in 2007;
Ali and colleagues made it precise for least squares in 2019. So three different-looking knobs — pick the
min-norm interpolant, add ridge λ, or stop GD early — are all **the same move**: put a Gaussian prior on the
weights and control how strong it is. That's the unifying idea, and it's a Bayesian idea, which is exactly
where we're headed."

**B1.14 — benign overfitting + honesty.** "One more piece of intuition, then the honest caveats. It feels
illegal to fit the noise exactly and still generalize — 'benign overfitting,' Bartlett and colleagues 2020.
The resolution is dimensionality: in a very high-dimensional model, the noise gets absorbed across an
enormous number of directions, each one barely perturbed, so interpolating it costs almost nothing on test.
Caveats, because this is a place to be careful: double descent needs the right setting — high-dimensional,
roughly isotropic features. In low dimensions with correlated features — like the *left*, polynomial panel of
our widget — you do **not** get a clean second descent, and that contrast is itself worth pointing out. The
classical U-curve was never wrong; it was incomplete."

**B1.15 — bridge to BNP.** "So, back to the question we opened with: how complex should the model be? Modern
ML gives two principled answers. One: make the model enormous and let an implicit or explicit prior pick a
simple solution among all the ones that fit — that's the deep-learning answer we just dissected. Two: don't
fix the size at all — let the model *grow with the data*, under an explicit prior that says how eager it is to
add complexity. That second answer is **Bayesian nonparametrics**, and it's the rest of today. Same question,
Bayesian answer: don't guess the number of parameters — put a prior over *all* of them and let the data
decide."

**Term-definition checklist (must be defined at first on-slide use, per the deck rule):** interpolation
threshold, overparameterized / underparameterized, min-norm / minimum-ℓ₂-norm, implicit vs explicit
regularization, ℓ₂ norm ‖·‖₂ and ℓ₁ norm ‖·‖₁, Gaussian prior, Laplace prior, MAP, ridge regression, λ,
pseudoinverse, condition number (if used), benign overfitting, early stopping. Put the symbol next to the
word the first time (e.g. "the **weight vector** ($\beta$)", "**ridge strength** ($\lambda$)").

---

## BLOCK 2 — Finite mixtures → "how many clusters?"  *(stub — expand in Task 8)*
Recap GMM on bento weights (textbook Ch5: Tonkatsu μ≈500g, Hamburger μ≈350g; "425g is ambiguous"). The K
problem: you must pick K in advance, and the number of partitions blows up. **Widget 1, fixed-K pass** — set
K=2, watch it miss the 275g outlier. Figure-todo: `partition_blowup.png`. Define: mixture model, component,
responsibility, EM (recap).

## BLOCK 3 — CRP  *(stub)*
Chinese Restaurant Process: a law over *partitions*, no parameters. Customer n+1 joins table k ∝ nₖ, or a new
table ∝ α; rich-get-richer; concentration α. **Widget 3 (CRP seating)**. Define: partition, CRP,
concentration parameter α, exchangeability.

## BLOCK 4 — CRP → Dirichlet Process (the three lenses)  *(stub)*
Pólya urn / Blackwell-MacQueen 1973 = CRP + dishes = the DP's *predictive marginal* (integrate G out) — **fix
the SP25 slide-35 conflation (Pólya urn ≠ "the DP")**. Stick-breaking (Sethuraman 1994): βₖ~Beta(1,α),
πₖ=βₖ∏(1−βⱼ) — **Widget 2**. The DP itself: G ~ DP(α,G₀), draws are **almost surely discrete → that's *why*
it clusters**. Synthesis slide tying the three lenses to one object. Define: Dirichlet Process, base measure
G₀, random measure, stick-breaking, almost-surely discrete.

## BLOCK 5 — DPMM  *(stub)*
DP prior + Gaussian likelihood (generative diagram). **Widget 1, full 3-way** (DPMM vs KDE vs fixed-K GMM).
**Port the SP25 parametric/nonparametric/BNP comparison slide** (to bento weights) — professor likes it, keep
it. Inference conceptually: collapsed CRP Gibbs (Neal 2000) = what the widget runs; variational / truncated
stick-breaking (Blei & Jordan 2006) = scalable default (sklearn `BayesianGaussianMixture`). Honest "DPMM
clustering is niche now." Backup: K-posterior inconsistency (Miller & Harrison 2014; Ascolani et al. 2022).
Port the misconceptions Q&A (SP25 slide 37). Reuse `genjax_dpmm.py` for a code slide. Define: DPMM, collapsed
Gibbs, conjugacy (recap), variational inference.

## BLOCK 6 — Building-block move  *(stub)*
"Replace a finite parameter with a random measure." **LDA worked toy example** + **topic-emergence viz**
(sibling-slide build-up: tiny Chibany corpus → document→topic→word → topics emerge). **Precise: LDA
(Blei, Ng & Jordan 2003) is finite-Dirichlet over fixed K; the nonparametric version is HDP-LDA (Teh et al.
2006)** — a shared top-level DP = a reusable topic menu. **IBP = the feature sibling** (Beta process; features
vs one-cluster-per-item) — compress to 1–2 slides reusing one Austerweil-Griffiths figure; name HDP-HMM,
Pitman-Yor in passing. Define: topic model, LDA, plate notation, HDP, IBP, Beta process, feature.

## BLOCK 7 — Gaussian processes + contemporary frame (promoted)  *(stub)*
GP = a prior over *functions*, the BNP that endured (Rasmussen & Williams 2006; Distill/Görtler figure).
Kernels (callback to the KDE kernel in Widget 1). **GP→NN, updated:** Neal 1996 → deep NNGP (Lee et al. 2018)
→ NTK (Jacot et al. 2018), distinguishing **NNGP (net at init / Bayesian inference *is* a GP)** from **NTK
(governs GD *training*)**, with the honest "omits feature learning" caveat. Neural processes (Garnelo et al.
2018). **Nonparametric memory** = RAG / kNN-LM (Lewis et al. 2020; Khandelwal et al. 2020). Through-line:
nonparametrics = the principled "let capacity grow with the data," which scaling laws gesture at. Reuse
`genjax_gp.py`. Define: Gaussian process, kernel / covariance function, NNGP, NTK, neural process,
retrieval-augmented generation.

## BLOCK 8 — Recap, the one picture  *(stub)*
parametric → nonparametric → BNP in one slide; one machine → many models (CRP/DP reused for clustering,
topics, features, functions); **callback to Block 1** — the bias-variance question, now answered the Bayesian
way. Define nothing new; consolidate.

---

## Pause-and-predict beats (recorded; mined from SP25 quizzes — verify the right quiz via
`course/quizzes/README.md`; the PLAN's "Social Cognition/IRL" mapping looks like a Week-9 carryover, audit
the clustering / Gaussian-Bayes quizzes instead)
- B1.7→B1.8: "past p = n — rise, plateau, or fall?" (double descent reveal). *Authored above.*
- B2: "set K=2 — does the 275g bento get its own cluster?" (reveal with Widget 1).
- B4: "draw twice from a DP — can you get the exact same value twice?" (yes — a.s. discrete; that's the point).
- (2–4 more to mine during Task 8.)

## TODO ledger for the rest of the build
- [x] Task 2 — bias-variance critical review (outcome recorded above).
- [x] Task 6 — Widget 4 (now incl. ridge-λ + ‖β‖₂ panel + neural-net-GD selection).
- [x] Task 3/4/5 — Widgets 1/2/3 (DPMM·KDE·GMM, stick-breaking·Pólya, CRP seating) — all BUILT & QA-verified.
- [x] Task 1 — skeleton DONE: `week10-slides.qmd` + `week10-styles.html` built; legacy PPTX in sp25_reference.
- [x] Task 8 — qmd authored: all 8 blocks, bilingual, 4 widgets embedded, Block-1 notes in `::: {.notes}`.
- [x] Task 9 — LDA toy + topic-emergence viz DONE (`lda_topic_emergence.png` + the LDA/HDP-LDA slides).
- [x] Task 10 — verification: deck builds; fill audit 0 clips / 0 overflow (12 slides 70–74%, centered);
  EN↔JA toggle verified; all 4 live widgets embed in-deck; 8 figures render. Previews in `deck-preview/`.
- [~] Task 7 — figures DONE (8: bv_three_fits, bv_ucurve, double_descent, partition_blowup, gp_prior_posterior,
  lda_topic_emergence, bento_bimodal, kernel_shapes). **Pending:** GenJAX backbones (`genjax_dpmm.py`,
  `genjax_biasvariance.py`, `genjax_gp.py`) — dual-home for Phase-2 textbook; a code slide can follow.
- [ ] Residual polish: nudge the 12 slides in the 70–74% band higher; optional fresh-subagent structural
  deep-review; sync root `TODO.md`; (Phase 2) the 3-chapter textbook revision.
