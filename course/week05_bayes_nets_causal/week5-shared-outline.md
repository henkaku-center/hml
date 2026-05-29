# Week 5: Shared Outline
## Friday, May 29, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Required reading (pre-class):** Austerweil, *A Narrative Introduction to Probability* — T3 Ch 5 (Mixture models), Ch 6 (DPMM). Finishes the hierarchical-Bayes thread from Week 4 before we shift to graphical models.
**Optional readings (also fair game for the Week 5 reflection):** Gerstenberg et al. 2015 (counterfactual causal judgments); Lagnado & Sloman 2002 (learning causal structure from interventions); Tenenbaum et al. 2011 (How to grow a mind).
**Students:** ~6
**Student presenter:** None this week.

---

## Key Design Decision

**The lecture opens on the Gaussian mixture model from Clusters and reveals it as a Bayes net students have already been writing.** This is a deliberate inductive (Koller / Xing / Ghahramani style) order: concrete networks first, formal definition extracted from them.

The arc:

1. **Block 1 — your assignment IS a Bayes net.** Draw the Gaussian mixture as a 3-node DAG with a plate, name the parts, point out that the responsibility weights students computed in Clusters Problem 2 are *Bayesian-network inference*. Pre-class T3 Ch 5 reading lands here. Hierarchical Bayes from Week 4 is revealed as the structure that was sitting inside the mixture all along.
2. **Block 2 — two complications, then notation lock-in.** Add one hyperprior (the mixture+hyperprior = Week 4 hier-Bayes drawn as a graph). Add multi-parent latents (weather + day-of-week → bento). End with **one slide** that names the shorthand: DAG, $\text{Pa}(X)$, $\prod_i P(X_i \mid \text{Pa}(X_i))$. Don't call it "the Markov factorization" yet — it's just notation they'll use in the next two examples.
3. **Block 3 — Chibany Monty Hall + the formal definition.** Monty Hall is the *third* example, not the first. After it lands, the factorization rule becomes a *theorem* with a name (Markov factorization), and the param-counting argument seals it (3 min, tight — students already accept the picture's compactness from Blocks 1–2). The Chibany Monty Hall (three bento boxes, one tonkatsu, cafeteria worker reveals one non-tonkatsu) opens; the canonical Monty Hall (doors / car / host) is a 1-slide callback showing "same network, different costume" later.
4. **Block 4 — d-separation, with an interactive Bayes-Ball widget.** Chain / fork / collider as a 3-slide sibling build-up. Widget runs 3 scripted scenarios (chain-conditioning, collider-open, collider-conditioning) mid-block.
5. **Block 5 — explaining away.** Sprinkler / Rain / Wet-Grass as a 3-slide unroll (was 4 in draft 1; tightened). Numerical update each slide. Callback to Monty Hall: this is *why* switching wins.
6. **Break.**
7. **Block 6 — observation → intervention.** Smoking / yellow-teeth / lung-cancer; chain / fork / collider all Markov-equivalent under observation; observation alone can't disambiguate.
8. **Block 7 — the do-operator.** Graph surgery: $do(X = x)$ cuts incoming arrows into $X$. $P(Y \mid X)$ vs. $P(Y \mid do(X))$. Worked numerically.
9. **Block 8 — blicket detector.** Cog-sci payoff. Gopnik & Sobel: children's causal inferences match Bayes-net learning with intervention.
10. **Block 9 — information theory + close.** 3 info-theory slides framed *through today's spine*: entropy as expected surprise, mutual information as "how much one variable tells you about another," the punchline $I(A; B \mid C) > 0$ when $C$ is a collider. Forward pointer to Week 6 (random walks on networks). 1-min close.

**No student presentation this week** → more time per topic. Two natural elastic blocks (the Chibany Monty Hall walk-through and the blicket-detector close) absorb overruns. Prof. Austerweil tends to run under time, not over — the schedule is feasible.

**Authoring style** follows Week 4: Quarto RevealJS, shared SCSS theme (`../../sds-reveal/sds.scss`), EN/JA `.lang-en`/`.lang-ja` divs on every concept-introducing slide, KaTeX math, sibling-slide build-ups for the d-separation rules, the explaining-away unroll, and the do-operator surgery. **3 polls** authored fresh (the SP25 Bayes-Net quiz is open-response Monty Hall — not poll-shaped — so polls are authored from the same scenario, just with ≤4 options committed-before-reveal).

**Chibany continuity.** Chibany's bento-rate hierarchical structure (Week 4) becomes the **second complication slide** in Block 2 — the hier-Bayes model drawn as a Bayes net. The Chibany-flavored Monty Hall opens Block 3. Chibany appears 3 times total across the deck.

---

## Session Plan

| Time | Block | Min | What Happens |
|---|---|---:|---|
| 0:00 | **1. Your assignment IS a Bayes net** | 10 | Welcome (1) + Clusters mixture model drawn as a DAG with plate; responsibility weights = BN inference; pre-class T3 Ch 5 reading paid off (9). |
| 0:10 | **2. Two complications + notation** | 10 | Mixture+hyperprior (Week 4 hier-Bayes as a graph) → multi-parent (Chibany bento with weather + day). One notation lock-in slide at end: DAG, Pa(X), product formula as shorthand. |
| 0:20 | **3. Monty Hall + formal definition** | 15 | **Chibany Monty Hall** (three bentos, tonkatsu-or-not, cafeteria worker reveals one). Joint, marginals, conditional. **Then:** name it — Markov factorization as theorem; param-counting (tight: 3 min); canonical Monty Hall as 1-slide costume-callback. Poll 1 (factorization). |
| 0:35 | **4. d-separation + Bayes-Ball widget** | 25 | Chain / fork / collider 3-slide build-up. **Interactive Bayes-Ball widget** runs 3 scripted scenarios. Two-column Markov-blanket slide. Poll 2 (collider conditioning). |
| 1:00 | **5. Explaining away** | 12 | Sprinkler / Rain / Wet-Grass, 3-slide unroll (tightened from 4). Numerical update each slide. Callback: *this* is why switching wins in Monty Hall. |
| 1:12 | **Break** | 10 | Cat photo. |
| 1:22 | **6. Observation → intervention** | 10 | Smoking / yellow-teeth / lung-cancer confound; chain / fork / collider all Markov-equivalent; observation can't disambiguate. |
| 1:32 | **7. The do-operator** | 15 | Graph surgery: $do(X=x)$ cuts incoming arrows. 4-slide sibling build-up. $P(Y \mid X)$ vs. $P(Y \mid do(X))$ two-column. Poll 3 (do vs. condition). |
| 1:47 | **8. Causal cognition — blicket detector** | 8 | Gopnik & Sobel blicket experiment; children's inferences match BN inference *with intervention*; cog-sci payoff. |
| 1:55 | **9. Information theory + Week 6 preview + close** | 5 | 3 info-theory slides: entropy as expected surprise; mutual info; $I(A;B\mid C) > 0$ when $C$ is a collider (ties info theory back to today's spine). 1-slide Week 6 preview (Markov chains + networks; Abbott 2012). |
| 2:00 | End | | |

**Deck size target:** ~75–85 slides. The 3-slide d-separation build-up, the 3-slide explaining-away unroll, the 4-slide do-operator surgery, and the Chibany Monty Hall walk-through all push slide count above what 9 blocks suggest. Sibling-slide build-ups inflate the count by design (per CLAUDE.md visual density baseline).

---

## Per-block visual budget

Per the CLAUDE.md "visual density baseline for new lecture decks" rule. Each block lists: **figures** (existing reusable or `figure-todo:`), **column layouts**, and **sibling-slide build-ups**. SP25 source figures pre-inventoried; see the figure-todo summary at the end.

### Block 1: Your assignment IS a Bayes net (10 min)

- **Figure (new):** `figure-todo: gmm_as_bn.png` — Gaussian mixture model drawn as a DAG: $\pi \to z_i \to x_i$, with plate over $i = 1, \ldots, N$ and $(\mu_k, \sigma_k) \to x_i$ outside the plate. Dark theme, yellow accent edges.
- **Two-column slide — your homework, named:** LHS shows the GMM density formula students wrote in Clusters Problem 2 ($p(x_i) = \sum_k \pi_k \mathcal{N}(x_i \mid \mu_k, \sigma_k)$); RHS shows the DAG. **Column layout required (formula ↔ graph).**
- **Sibling-slide pair — what the responsibility weight is:** *Slide A* shows $p(z_i = k \mid x_i)$ as the formula students computed; *Slide B* overlays it on the DAG with the conditioning arrow highlighted — "this is a node's posterior given its child. You did Bayesian-network inference."
- **DPMM one-liner:** dim-caption only on the "you've been doing this" slide: *"Choosing K is its own problem — DPMM (T3 Ch 6) avoids fixing it. Week 10 picks this up."* No separate slide.
- **No build-up sequences** beyond the responsibility-weight pair. This block is a *recognition* moment, not a derivation.

### Block 2: Two complications + notation lock-in (10 min)

- **Figure (new):** `figure-todo: gmm_with_hyperprior.png` — same GMM, now with a hyperprior added: $\alpha \to \pi$, $(\mu_0, \sigma_0) \to (\mu_k, \sigma_k)$. The hyperprior nodes are highlighted in yellow with a callout: "This is exactly Week 4's hierarchical Bayes." **One slide.**
- **Figure (new):** `figure-todo: chibany_bento_bn.png` — multi-parent latent: Weather → Bento, Day-of-week → Bento, Restaurant → Bento. 4-node DAG, Chibany sticker in the corner. **One slide.**
- **Sibling-slide pair — what's new in this graph:** *Slide A* shows the bento DAG; *Slide B* overlays the factorization $P(W, D, R, B) = P(W) P(D) P(R) P(B \mid W, D, R)$ — "the rule for graphs with multiple parents."
- **Two-column slide — notation lock-in (the C-concession):** LHS the symbols (DAG, $\text{Pa}(X)$, $\prod_i P(X_i \mid \text{Pa}(X_i))$); RHS a recap of the three networks seen so far (GMM, GMM+hyperprior, Chibany bento) with $\text{Pa}$ called out on each. **Column layout required (notation + visual recap).** Critically: **do NOT call this "the Markov factorization" yet** — frame it as "the shorthand we'll use in the next two examples." The full theorem lands in Block 3.

### Block 3: Monty Hall + formal definition (15 min)

- **Figure (new):** `figure-todo: chibany_monty_hall.png` — 3-node collider DAG: TonkatsuBento → CafeteriaReveals ← ChibanyPicks. Three bento boxes drawn small as visual aid. Chibany sticker.
- **Sibling-slide build-up (4 slides) — Chibany Monty Hall:** *Setup* (the scenario: three bentos, one tonkatsu, Chibany picks, cafeteria worker — who knows — reveals a non-tonkatsu) → *The Bayes net* (collider DAG; factorization $P(T) P(C) P(R \mid T, C)$) → *Marginals before reveal* (each bento equally likely: $P(T = k) = 1/3$) → *Conditional after reveal* ($P(T = \text{Chibany's pick} \mid R) = 1/3$; $P(T = \text{other unopened} \mid R) = 2/3$). Each slide adds one row of conditioning, with the DAG re-drawn each time with the relevant edge / node highlighted.
- **Two-column slide — "Should Chibany switch?":** LHS the numerical answer (2/3 vs 1/3 → switch); RHS *why* (the cafeteria worker's choice depends on both Chibany's pick and the tonkatsu location; that conditional dependence flows through the collider). Don't name explaining-away yet — pay off in Block 5. **Column layout required (numbers + intuition).**
- **Formal definition slide — Markov factorization as theorem:** "What we've just been doing has a name." DAG, parents, the factorization formula now labeled **Markov factorization** with the theorem statement: *for any DAG $G$ over $X_1, \ldots, X_n$, the joint factorizes as $\prod_i P(X_i \mid \text{Pa}(X_i))$ iff the graph is an I-map for $P$.* (Don't unpack I-map; one dim-caption: "I-map = the graph's independence assumptions are valid for $P$.") **One slide.**
- **Param-counting recap (tight, 3 min, one slide):** For 4 binary variables, full joint = 15 numbers; the bento BN = 8. **Figure (reuse):** SP25 Week 4 slide 36 — `figure-todo: bn_param_count.png` (extract from SP25 .pptx).
- **Canonical Monty Hall costume-callback (1 slide):** Door / Car / Host diagram with caption "same network, different decoration." Visual only, no calculation.
- **Poll 1 — Bayes-net factorization** (authored, Chibany flavor): *"In the Chibany Monty Hall network (Tonkatsu → CafeteriaReveals ← ChibanyPicks), the joint factorizes as:"*
  - (A) $P(\text{Tonkatsu})\,P(\text{Picks})\,P(\text{Reveals} \mid \text{Tonkatsu}, \text{Picks})$ ← **correct**
  - (B) $P(\text{Tonkatsu} \mid \text{Picks})\,P(\text{Picks})\,P(\text{Reveals})$
  - (C) $P(\text{Tonkatsu})\,P(\text{Picks} \mid \text{Tonkatsu})\,P(\text{Reveals} \mid \text{Picks})$
  - (D) Cannot factorize — all three are dependent.
  Reveal: (A); each node, given its parents, contributes one factor. Source note: **authored from SP25 Monty Hall quiz scenario.**

### Block 4: d-separation + Bayes-Ball widget (25 min)

- **Sibling-slide build-up (3 slides) — d-separation:**
  - *Chain* ($A \to B \to C$): conditioning on $B$ *blocks* dependence. `figure-todo: dsep_chain.png` with shaded $B$.
  - *Fork* ($A \leftarrow B \to C$): conditioning on $B$ *blocks* dependence. `figure-todo: dsep_fork.png` with shaded $B$.
  - *Collider* ($A \to B \leftarrow C$): conditioning on $B$ *induces* dependence. `figure-todo: dsep_collider.png` with shaded $B$, exclamation-mark accent.
  Each slide: DAG, shaded node, one-line statement of what flows / blocks. The collider slide is the surprise — flag it as "we'll come back to *why* this one is backwards in Block 5."
- **Two-column slide — Markov blanket:** LHS the formal definition (parents + children + children's other parents); RHS a small DAG with the blanket nodes shaded. `figure-todo: markov_blanket.png`. **Column layout required (definition + visual).**
- **Interactive Bayes-Ball widget (3 scripted scenarios):** Custom JS+SVG widget embedded in the deck (file: `course/week05_bayes_nets_causal/widgets/bayes_ball.html`, loaded via Reveal). The lecturer drives it on stage; **not** open exploration.
  - **Scenario 1:** chain $A \to B \to C$; condition on $B$; ball launched from $A$, bounces at $B$, doesn't reach $C$. (~30 sec)
  - **Scenario 2:** collider $A \to B \leftarrow C$; **don't** condition on $B$; ball launched from $A$, reaches $B$ but can't pass through (collider blocks unconditionally), doesn't reach $C$. (~30 sec)
  - **Scenario 3:** collider $A \to B \leftarrow C$; condition on $B$; ball passes through $B$, reaches $C$. The visual "click" when the conditioning flips the collider open is the punchline. (~30 sec)
  - Widget styling: dark theme, yellow ball, yellow shading for conditioning. Three "next scenario" buttons; no open-ended exploration on stage.
  - **Fallback:** static figures in case the widget doesn't load. SP25 Week 4 slide 41 (Bayes-Ball grid) — `figure-todo: bayes_ball_static.png`.
- **Poll 2 — collider conditioning** (authored, Chibany Monty Hall callback): *"Chibany hasn't picked yet, but you see the cafeteria worker open Bento 2 (no tonkatsu). Does this change your belief about which bento Chibany will pick?"*
  - (A) Yes — the cafeteria worker's choice and Chibany's pick are now dependent. ← **correct (collider conditioning)**
  - (B) No — they were independent before, so they're still independent.
  - (C) Only if you also know which bento has the tonkatsu.
  - (D) Chibany's pick was random, so observation can't change it.
  Reveal: (A); collider conditioning *induces* dependence. (B) is the natural mistake; flag it as the misconception Block 5 explains. Source note: **authored from SP25 Monty Hall scenario.**

### Block 5: Explaining away (12 min)

- **Sibling-slide build-up (3 slides) — Sprinkler / Rain / Wet-Grass** (was 4 in draft 1; tightened). **Model: deterministic OR** — $W = 1 \iff (R = 1)\ \text{or}\ (S = 1)$, with $P(R) = P(S) = 0.3$ independent. State the CPT on the setup slide so the numbers are reproducible (CLAUDE.md "introduce the model" rule):
  - *Setup — Rain ⊥ Sprinkler a priori* (each has independent prior $0.3$; show the 3-node DAG; state the deterministic-OR CPT for $W$).
  - *Observe Wet-Grass — both probabilities go up* (exact under det-OR: $P(R \mid W) = P(S \mid W) = 10/17 \approx 0.59$).
  - *Also observe Sprinkler on — Rain drops back to its prior* ($P(R \mid W, S = 1) = 0.3 = P(R)$ **exactly**, because $S = 1$ makes $W$ certain regardless of $R$, so $W$ carries zero further info about $R$). **This is explaining away.** Sprinkler fully "explains" the wetness. (A noisy-OR would leave $R$ slightly above prior — the residual is the signature of non-determinism; the deterministic version is kept for clean arithmetic.)
  - **Figure (reuse):** SP25 Week 4 slide 40 — `figure-todo: explaining_away_srw.png`. Standout SP25 figure.
- **Two-column slide — what just happened:** LHS the numerical sequence ($P(R) = 0.30 \to 0.59 \to 0.30$); RHS the take-home in one sentence: *"Conditioning on a common effect makes independent causes dependent — and conditioning on one cause then *reduces* support for the other."* **Column layout required (numbers + interpretation).**
- **Monty Hall callback (1 slide, no formal poll):** "Remember Chibany's switching dilemma? The cafeteria worker opening Bento 2 *is* a collider observation. The other unopened bento got 'explained up' — that's why switching gives you 2/3." Audience: show of hands, who switches now?

### Block 6: Observation → intervention (10 min, post-break)

- **Figure (reuse):** SP25 Week 5 slide 16 — Smoking / Yellow-teeth / Lung-cancer DAGs in two configurations (one where smoking is parent of both, one where the wrong arrow is X-marked). `figure-todo: smoking_confound.png`. Standout figure for the confounding setup.
- **Sibling-slide build-up (3 slides) — Markov equivalence:** *Chain* ($A \to B \to C$) → *Fork* ($A \leftarrow B \to C$) → *Collider* ($A \to B \leftarrow C$) → punchline: chain and fork are Markov-equivalent under observation alone; only the collider is observationally distinguishable. **Reuse** the `dsep_chain.png`, `dsep_fork.png`, `dsep_collider.png` figures from Block 4 with new annotations: ✓ on chain and fork ("same observations"), ✗ on collider ("different — but rarely the structure of confounding").
- **Two-column slide — observation vs. intervention setup:** LHS what observation tells you (statistical dependence; can't disambiguate chain from fork); RHS what intervention *would* do (cut incoming arrows; reveal the cause). **Column layout required (the conceptual contrast).** Don't reveal the do-operator yet; just preview the move.

### Block 7: The do-operator (15 min)

- **Figure (reuse):** SP25 Week 5 slide 21 — "Logic of doing": graph surgery shown explicitly with original DAG → arrows cut. `figure-todo: do_surgery.png`. Standout SP25 figure.
- **Sibling-slide build-up (4 slides) — graph surgery on smoking/teeth/lung-cancer:**
  - *Original network*: $S \to T$, $S \to L$. Confounded.
  - *do(T = white)*: cut the incoming arrow into $T$, set $T = \text{white}$, leave $S \to L$ intact. `figure-todo: do_cut.png` with the cut arrow X'd out and the new $T$ value shown.
  - *Compute $P(L \mid do(T))$*: equals $P(L)$ — the intervention severed the path from $T$ back to $L$ through $S$. Numerical, ~3 lines.
  - *Compare $P(L \mid T)$ vs. $P(L \mid do(T))$*: observational quantity ≠ interventional quantity. Numerical comparison.
- **Two-column slide — $P(Y \mid X)$ vs. $P(Y \mid do(X))$:** LHS the conditioning formula (observational, integrates over how $X$ was generated); RHS the do-formula (interventional, replaces the mechanism that generates $X$). Same notation, different meaning. **Column layout required (the formal contrast).**
- **Poll 3 — do vs. condition** (authored): *"In a network $S \to T, S \to L$ (smoking → teeth, smoking → lung-cancer), painting Chibany's teeth white sets $T = \text{white}$ as an intervention. What is $P(\text{lung-cancer} \mid do(T = \text{white}))$?"*
  - (A) Lower than $P(\text{lung-cancer})$ — whiter teeth predict less smoking, less smoking predicts less lung-cancer.
  - (B) Same as $P(\text{lung-cancer})$ — the intervention cuts the $S \to T$ edge, so $T$ no longer informs about $S$. ← **correct**
  - (C) Higher than $P(\text{lung-cancer})$ — paint chemicals cause cancer.
  - (D) Unknown without more data.
  Reveal: (B); the do-operator's whole point is that observation and intervention are *different operations* on the network. (A) is the seductive observational answer — the misconception the block exists to defeat.

### Block 8: Causal cognition — the blicket detector (8 min)

- **Figure (reuse):** SP25 Week 5 slides 10–11 — blicket detector physical experiment photos. `figure-todo: blicket_detector.png`, `figure-todo: blicket_backwards_blocking.png`.
- **Figure (reuse):** SP25 Week 5 slide 13 — line graph of human judgments vs. model predictions for "backwards blocking" experiment. **Standout SP25 figure (data + model integration).** `figure-todo: blicket_model_human.png`.
- **Two-column slide — experiment setup:** LHS the physical setup (blocks on a "detector" that lights up); RHS the corresponding Bayes net. **Column layout required (physical + formal).**
- **One-slide payoff:** human (children's) judgments match the Bayes-net inference that *requires* intervention to compute. "Children do graph surgery." Frame as the cog-sci payoff: the formal machinery isn't just for engineers.
- **Elastic block:** if running short, cut to one slide (just the model-vs-human figure + 1 sentence).

### Block 9: Information theory + close (5 min)

- **Slide 1 — entropy as expected surprise:** $H(X) = -\sum_x P(x) \log P(x) = \mathbb{E}[-\log P(X)]$. One-line motivation: "if I told you the outcome of $X$, how surprised would you be on average?" Coin-flip example (fair coin: 1 bit; biased coin: less). One slide.
- **Slide 2 — mutual information:** $I(X; Y) = H(X) - H(X \mid Y) = H(Y) - H(Y \mid X)$. "How much knowing $Y$ reduces uncertainty about $X$." Note the symmetry. One slide.
- **Slide 3 — the connection back to today:** $X \perp Y \iff I(X; Y) = 0$. Conditional mutual info: $X \perp Y \mid Z \iff I(X; Y \mid Z) = 0$. **The collider punchline:** for $A \to B \leftarrow C$, $I(A; C) = 0$ but $I(A; C \mid B) > 0$ — explaining away in info-theoretic clothing. One slide. Caption: "info theory and Bayes nets are two languages for the same structure."
- **Week 6 preview slide (1 slide):** Abbott et al. 2012 — human memory search as a random walk on a semantic network. "We've spent today on the *structure* of multi-variable distributions. Next week we *walk* on a network instead of conditioning on one." Reading callout: T3 Ch 6 (DPMM) is your pre-read.

---

## Figure-todo summary

Total figures: **~22**. Breakdown:

- **Pure reuse from SP25** (extract via PowerPoint screenshot or LibreOffice export): `bn_param_count.png`, `explaining_away_srw.png`, `bayes_ball_static.png` (fallback), `smoking_confound.png`, `do_surgery.png`, `blicket_detector.png`, `blicket_backwards_blocking.png`, `blicket_model_human.png`. **8 figures.**
- **New, generated by `scripts/build_dags_week5.py`** (one script, graphviz + matplotlib, dark theme, yellow accents, consistent node sizing):
  - `gmm_as_bn.png` — GMM with plate
  - `gmm_with_hyperprior.png` — GMM + α, (μ₀, σ₀) hyperprior
  - `chibany_bento_bn.png` — Weather + Day + Restaurant → Bento
  - `chibany_monty_hall.png` — 3-node collider with bento aesthetic
  - `dsep_chain.png` — A → B → C
  - `dsep_fork.png` — A ← B → C
  - `dsep_collider.png` — A → B ← C
  - `markov_blanket.png` — 5-node DAG with blanket highlighted
  - `do_cut.png` — smoking/teeth/cancer with the do-cut arrow X'd
  - canonical Monty Hall costume-callback figure (Door / Car / Host) — reuse a free clip-art or generate fresh; lower priority
  - **~10 figures.**
- **Interactive widget:** `widgets/bayes_ball.html` — custom SVG + vanilla JS, 3 scripted scenarios, dark theme, yellow ball. ~half-day build. Loaded via Reveal `<iframe>` or inline-included script.

---

## Open questions / call-outs

1. **GMM-as-Bayes-net visual style.** Plate notation is standard (Bishop, Murphy) but not everyone in the class has seen it. I propose introducing it inline on the GMM slide (one dim-caption: "the box = repeat for each $i$") rather than a separate plate-notation slide. Confirm OK.
2. **Markov factorization vs. "Markov condition" vs. "Bayes-net factorization."** Three names for the same thing in the literature. I'm using "Markov factorization" throughout (matches Koller & Friedman; matches Pearl's *Causality*). Flag if you prefer one of the others.
3. **The I-map / D-map / minimal-I-map machinery is skipped** — only the formal-definition slide mentions I-map in a dim caption. This is intentional (full I-map theory is a 30-min topic and not needed for this lecture's goals). Confirm OK to skip.
4. **Bayes-Ball widget build path:** custom JS+SVG selected (over Quarto OJS). Half-day budget. If short on build time, the static SP25 grid is the fallback (already in figure-todo list).

---

## Status

**Draft 2.** Awaiting Joe's review before:
- writing the qmd
- building `scripts/build_dags_week5.py`
- building `widgets/bayes_ball.html`

**Changes from Draft 1:**
- Opened on Clusters mixture model as the first Bayes net (was: Monty Hall opened)
- Added Block 2 (two complications + notation lock-in) as a new block (was: notation in Block 3)
- Moved Monty Hall to Block 3 and Chibany-flavored it (was: canonical, in Block 2)
- Tightened param-counting argument (3 min instead of 5)
- Trimmed explaining-away unroll from 4 to 3 slides
- Added interactive Bayes-Ball widget with 3 scripted scenarios (was: optional static figure)
- Added Block 9 info-theory mini-block (was: zero info-theory content)
- Compressed blicket-detector block to 8 min (was: 10)
- DPMM mentioned only as a dim-caption forward pointer (was: not mentioned at all)
