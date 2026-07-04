# Week 11 shared outline — Deep Neural Networks & LLMs (Fri Jul 10, 2026, in person)

SOURCE OF TRUTH for `week11-slides.qmd`. Edit here first, then the qmd.

## The one organizing frame (named in Block 1, REFERENCED thereafter, never re-derived)

**"Where does the hypothesis space come from?"** Week 10 closed on one question
(how complex should a model be?) with three answers (ridge / BNP / GP) — and
ended at infinite-width nets = GPs with FIXED kernels. Week 11 is the fourth
answer: **learn the features**. One master picture (`images/four_answers_map.png`)
shows data → features → function → prediction with three lit-up questions:
**REPRESENT** (what can this hypothesis space express? — Blocks 2, 5),
**LEARN** (how do we find the hypothesis? — Blocks 3–4),
**UNDERSTAND** (why does it generalize, and is it Bayesian? — Block 6, 7).
Each block opens by pointing at the lit region of THIS diagram — one slide,
no re-derivation. Lake et al. 2017 (required reading) is the standing critical
voice: carried as a "Lake scorecard" sidebar revisited in Blocks 2, 6, 7.

## Fact-check ledger (verified against the actual prior decks)

- α learning rate, TD update, ε-greedy, value iteration, Q-learning → **Week 8**. NO softmax there.
- softmax + β rationality, Bradley–Terry σ, RLHF/DPO, POMDPs, ToM → **Week 9**.
- bias–variance, double descent, ridge=Gaussian prior, min-norm, early stopping,
  gradient descent (as idea), CRP/DP/DPMM, GP, **NNGP (at init) / NTK (during
  training) / infinite width**, neural processes, RAG → **Week 10**.
- NOTHING prior taught: backprop, transformers, attention, word embeddings,
  finite-width training mechanics. All net-new here — define at first use.
- SP25 corrections baked in: backprop **is** today's workhorse (SP25 transcript
  mis-said otherwise); activations updated (tanh → ReLU → GELU/SiLU as current
  standard, no "last 5 years" dating); vanishing gradients get the real modern
  fixes (residual connections + normalization).

## Timing (in-person, 105 min + flex)

| t | Block | Content |
|---|---|---|
| — | P | **Student paper presentation (~15 min + discussion)** — student-driven; a holder section-break slide sits after the agenda. Confirmed present (Joe, 2026-07-05). Lecture-clock times below start AFTER it. Drop-if-long: RNN slide, emergence-mirage caveat. |
| 0:00 | 0 | Housekeeping (paper presentation first; RL + MC assignments due TONIGHT 8 PM; final-project timeline) + agenda |
| 0:05 | 1 | Where we left off: recap poll ×2 → infinite-width bridge → **name the frame** + Lake scorecard intro |
| 0:17 | 2 | REPRESENT I: connectionism — emergence, PDP, the neuron, activations, distributed reps (cat/dog), localist-vs-distributed → **VECTORS INTERLUDE (zero-LA on-ramp): data→vector (bento card → [500, 8] → a point), dot product = similarity (fully worked arithmetic + cosine), vector-space widget, retro-link "the neuron's Σ IS a dot product"** → word embeddings payoff (now grounded) |
| 0:43 | 3 | LEARN I: perceptron (w·x as the similarity score just taught) → decision line → error-driven learning → gradient descent (η ↔ Week 8's α) → delta rule |
| 0:56 | — | Short rest (5 min) |
| 1:01 | 4 | LEARN II: XOR poll → Minsky/Papert separability → **MATRICES, concretely: a matrix = a machine that moves every point (worked 2×2, columns = where basis arrows land) + matrix-transform widget (presets, then the ReLU fold teaser)** → linear stacking collapses (build-up; "two machines compose into one") → depth+nonlinearity worked XOR → backprop = blame apportionment → `jax.grad` → Rumelhart |
| 1:23 | 5 | REPRESENT II: architecture = inductive bias (= prior): CNN fast → RNN faster → **attention as soft lookup (match = dot product) → the transformer** |
| 1:36 | 6 | UNDERSTAND: scaling laws → emergence (+ mirage caveat) → **ICL: the Bayesian lens as a LIVE DEBATE** (Xie/Ye vs Falck) → RLHF callback (→ Week 12) |
| 1:50 | 7 | Lake scorecard settled + "one question, four answers" closing picture + next week |
| 1:55 | — | Student presentation(s) if assigned (presenter: null in readings_map as of Jul 4 — see contingencies) |

**Linear-algebra ground rule (Joe, 2026-07-04):** students do NOT have a linear
algebra background. Every vector/matrix concept gets (a) a concrete worked
number example on the slide, (b) an interactive visualization, (c) an explicit
definition at first use — data→vectors, vectors→similarity, vectors→spaces/
embeddings, matrices→transformations of space, nonlinearity→folding. The
textbook prerequisite chapter is `deep/vectors-and-spaces.md`. No slide may use
$\mathbf{w}^\top\mathbf{x}$, $W\mathbf{x}$, or matrix products before the
interlude slides define them concretely.

**Contingencies:** (a) if a presenter is assigned, presentation lands after
Block 4's break, and Block 5 CNN/RNN compresses to 2 slides ("two prior
architectures, one lesson: bake the invariance in") — the attention/transformer
segment is protected; (b) if running long at 1:13, drop the RNN/Mozer slide
pair entirely (its only job is the cliffhanger attention resolves); (c) Block 6
mirage-caveat slide is skippable-live but stays in the deck for the recording.

## Per-block visual budget

**Block 1** — figures: `double_descent.png` (reuse from week10/images, the
"bring-it-home" callback), figure-todo: `four_answers_map.png` — the master
frame diagram (data→features→function→prediction, three question-regions;
matplotlib boxes, dark bg, generous text clearance per CLAUDE.md). Two-column:
"fixed kernel (W10)" vs "learned features (today)". Polls P1+P2 (below).

**Block 2** — figures from SP25 pptx (extract): neuron/activation diagram,
cat/dog distributed maps ×2, localist-vs-distributed; figure-todo:
`activations.png` (tanh/ReLU/GELU on one axes, dim caption "1986 → 2012 →
today"). figure-todo: `embedding_arith.png` (king−man+woman≈queen as 2-D
arrows — the word2vec payoff; presentation candidate tie-in). Two-column:
distributed vs localist. Lake scorecard sidebar #1 (compositionality?).

**Block 3** — SP25 figures: decision-line, E-vs-w gradient curve; figure-todo:
`delta_rule_anatomy.png` (update = error × input, labeled bands, no collisions).
Two-column: "Q-learning update (W8)" vs "gradient step (today)" — same shape,
`new ← old + α · error-signal`. Build-up: NONE here (delta rule is one beat).

**Block 4** — SP25 figures: AND/OR/XOR separability panel, space-warp, worked
ReLU-XOR matrices, 3-layer backprop diagram. **Build-up as sibling slides
(3):** "stack two linear layers" → "multiply out: still linear" → "so depth
alone buys nothing — the fix is nonlinearity." Widget: **`xor-playground.html`
(NEW)** — tiny 2-hidden-ReLU net on XOR; sliders for the hidden weights +
"train" button; decision boundary repaints live (manipulable-by-default rule).
Code beat: 5-line `jax.grad` cell (course identity; validated).

**Block 5** — SP25 figures: convolution GIF, 2×2-kernel arithmetic, Elman SRN,
unfolding diagram. figure-todo: `attention_lookup.png` (Q·K softmax → weighted
V mix, drawn as a soft dictionary), `transformer_block.png` (attention + MLP +
residual + norm, one clean column). Widget: **`attention-lookup.html` (NEW)**
— 5-token toy: pick the query token, watch soft weights + mixed value update;
temperature slider (softmax! — "the β you met in Week 9"). Two-column:
"RNN: sequential bottleneck" vs "attention: every token sees every token".

**Block 6** — figure-todo: `scaling_laws.png` (log-log loss vs params/data/
compute, three straight lines; Kaplan 2020 / Hoffmann 2022 one-line caption),
`icl_setup.png` (frozen weights + prompt-with-examples → continuation),
`icl_debate.png` (two-panel: "ICL = implicit Bayes" [Xie 2022; Ye 2024:
pretraining ≈ empirical Bayes, ICL ≈ posterior predictive] vs "not so fast"
[Falck 2024: martingale property violated]). Widget: reuse
`bias-variance-explorer.html` (double-descent panel) for the
scale-changes-the-rules beat. Poll P3. Callbacks referenced, not re-derived:
hierarchical Bayes (W4), softmax/RLHF (W9), NNGP/NTK (W10).

**Block 7** — figure-todo: `four_answers_close.png` (the master map, all
regions lit, four answers annotated: ridge / BNP / GP / learned features).
Lake scorecard final: what nets now do well vs what the critique still holds
on (causality, compositional generalization — cite Lake & Baroni 2023 nuance).

## Polls (commit-before-reveal; bilingual per CLAUDE.md poll structure)

- **P1 (Block 1):** "Do Bayesian nonparametric models have parameters?" —
  A. Yes, infinitely many ✓ · B. Yes, a few · C. No — it's called nonparametric
  for a reason. *Provenance: SP25 quiz "Intro to Bayes Nonparametrics" Q1
  (gf28c347…). Bridge: infinitely-many-parameters → today's overparameterized
  nets.*
- **P2 (Block 1, fast):** "Which of these is NOT a parametric model?" —
  A. kernel/exemplar methods ✓ · B. 3-cluster GMM · C. one Gaussian.
  *Provenance: same SP25 quiz, Q3. Bridge: kernel methods → NNGP/NTK recap.*
- **P3 (Block 4 opener):** "A single linear classifier can learn AND and OR.
  Which can it NOT learn?" — A. NAND · B. XOR ✓ · C. it can learn all of
  these. *New for SP26 (no NN quiz exists in the SP25 bank — verified).*
- **P4 (Block 6):** "A frozen LLM continues a made-up pattern from 3 examples
  in the prompt. Where does what-it-just-learned live?" — A. in updated
  weights · B. in the context window, weights unchanged ✓ · C. in a retrieval
  database. *New for SP26. Reveal seeds the ICL-as-inference-not-learning
  framing that the debate slides then complicate.*

## Widgets

1. `widgets/xor-playground.html` — NEW (Block 4). 2-2-1 ReLU net; weight
   sliders + train button + boundary canvas; presets: "linear only" (fails) /
   "trained" (solves). User-settable per the manipulable-widgets rule.
2. `widgets/attention-lookup.html` — NEW (Block 5). Soft dictionary lookup on
   a 5-token sentence; query selector, temperature slider, weight bars +
   mixed-value readout; "hard lookup" toggle for the limit case.
3. `widgets/bias-variance-explorer.html` — REUSE (copy from week10 widgets/,
   Block 6 double-descent callback).
4. `widgets/vector-space.html` — NEW (Block 2 vectors interlude; dual-use,
   lives in textbook static/widgets/ too). Bento data → vectors → points;
   click two items, worked dot-product arithmetic + cosine + angle readout;
   normalize toggle.
5. `widgets/matrix-transform.html` — NEW (Block 4 matrices; dual-use). 2×2
   sliders warp a gridded plane + the bento points; presets; "e1 lands at the
   first column" readout; ReLU-fold toggle (the nonlinearity teaser the XOR
   space-warp pays off).

Figures added for the interlude: `data_to_vector.png` (bento card → column
vector → point) and `dot_product_worked.png` (u·v worked arithmetic + angle).

## Speaker-note requirements

Poll provenance lines; the two SP25 corrections called out (backprop IS the
workhorse; activation history); "presentations TBD" flexibility note; Block 6
notes carry the honest epistemic status of ICL-as-Bayes (workshop-level
formalization, active counter-evidence — teach the debate, don't settle it);
Mozer music anecdote optional-color in Block 5 notes only.

## Textbook tie-ins (for PLAN.md "Textbook Chapters" + closing slide)

Bk: from rules to weights · Bk: neural net fundamentals · Bk: transformers
attention · Bk: llms in context learning · Bk: world models imagination
(all `deep/` — stubs today, authored as Phase D right after this deck;
deck and chapters share this outline's spine).
