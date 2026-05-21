# Week 4: Shared Outline
## Friday, May 22, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Required reading (pre-class):** Tenenbaum (1999), *Bayesian modeling of human concept learning* (NeurIPS 11). Optional: textbook T3 Ch 5 (Mixture models) — primes the hierarchical-Bayes teaser.
**Students:** ~6
**Student presenter:** **Shohei** — Tenenbaum & Xu (2000), *Word learning as Bayesian inference* (CogSci).

---

## Key Design Decision

**This week has a hard structural constraint: the student presentation eats ~25 min** (15 min talk + 5 min discussion + 5 min swap/setup buffer). The instructor's job is to deliver the *entire* Bayesian-generalization core — framework, size principle, and **both** worked games (continuous rectangle game + discrete number game) — **before** the break, so nothing the lecture owes the students depends on time that the presentation might overrun.

Sequencing decision (confirmed with Prof. Austerweil):

1. **Clusters-assignment walkthrough opens the session** (~8 min). Assignment 1 (Clusters) is due **Fri Jun 5, 8:00 PM**; Week 4 is the natural point to walk the stencil since students have now seen the Gaussian-Gaussian and mixture math it depends on. Short, concrete, not a re-lecture.
2. **All core generalization content lands before the break** (~0:18–1:05). Framework → size principle → rectangle game → number game, in that order. The size principle is introduced abstractly, then *shown* twice — once continuous, once discrete — so students see it is one principle, not two tricks.
3. **Break, then Shohei presents** (~1:10–1:35). A dedicated **bridge slide** right before his block primes the audience: his paper (Tenenbaum & Xu word learning) is the *discrete number-game machinery applied to children learning word meanings*. He gets a running start; the audience knows exactly which lecture concept his paper extends.
4. **No Free Lunch + hierarchical Bayes close the session** (~1:35–2:00). NFL is the "why does generalization need a prior at all" capstone. **Hierarchical Bayes is authored two ways** (instructor selects on the day, by timing):
   - **Variant A — teaser** (~5 min, 3 slides): priors-over-priors, Chibany bento-rate-across-students, T3 Ch 5 assigned. Use if the presentation or earlier blocks overran.
   - **Variant B — full block** (~15 min, ~8 slides): the teaser plus a worked two-level Beta-Binomial — infer the shared $(a,b)$ across students, show shrinkage/partial-pooling. Use if the day is on schedule.

   Both variants are built into the deck and clearly fenced (see Block 10). A full hier-Bayes block trades against nothing in the core — it only competes with slack — so the choice is purely a timing call made live.

**Authoring style** follows Week 3: Quarto RevealJS, shared SCSS theme (`../../sds-reveal/sds.scss`), EN/JA `.lang-en`/`.lang-ja` divs on every concept-introducing slide, KaTeX math, sequential-reveal build-ups for the size-principle arithmetic. Polls are mined from the SP25 **Bayesian Generalization** quiz (`g90f0d9a6c127ebc338dedf7fbd11b4f8`) per the CLAUDE.md standing rule.

**Chibany continuity.** Where it doesn't strain the canonical Tenenbaum examples, the framework is motivated through Chibany: generalization = "Chibany saw three tonkatsu lunches near 500g — is a 480g lunch also tonkatsu?" The rectangle and number games stay in their canonical Tenenbaum form (gnarbles, the number game) because those are exactly what Shohei's paper and the textbook build on — but the *opening* motivation and the hier-Bayes teaser are Chibany-framed.

**"Where we are" recap slides.** At each major block boundary the deck re-shows the agenda as a `{.agenda .dense}` slide with finished blocks dimmed (`.done`) and the upcoming block highlighted (`.highlight`). Six recaps: before the generalization problem, the framework, the rectangle game, the break, No Free Lunch, and hierarchical Bayes. Each is a ~10s orientation beat, not read aloud. (The `.done` dim style is a shared-SCSS addition — see TODO for the cross-repo mirror.)

---

## Session Plan

| Time | Block | Duration | What Happens |
|------|-------|----------|--------------|
| 0:00 | **1. Welcome + Clusters walkthrough** | 10 min | 2 min welcome/agenda + 8 min Clusters stencil walkthrough (due Jun 5, 8 PM). |
| 0:10 | **2. The generalization problem** | 8 min | What generalization is; Shepard's universal law; why it's *the* inductive problem. Poll 1 (universal law). |
| 0:18 | **3. The Bayesian generalization framework** | 12 min | Hypotheses as consequential subsets; prior, likelihood, posterior; generalization = posterior-weighted vote. |
| 0:30 | **4. The size principle** | 10 min | Strong vs. weak sampling; size principle stated; "suspicious coincidence" intuition. Poll 2 (strong sampling). |
| 0:40 | **5. Rectangle game — continuous concept learning** | 15 min | Gnarbles. 1-D interval, then 2-D rectangle. Generalization gradient; effect of n; the exponential prior. |
| 0:55 | **6. Number game — discrete concept learning** | 13 min | Tenenbaum's number game. Discrete hypothesis space (math + magnitude). Size principle arithmetic worked numerically. |
| 1:08 | **Break** | 5 min | |
| 1:13 | **7. Bridge → Shohei's paper** | 2 min | One slide: word learning = the number game for word meanings. Hand off. |
| 1:15 | **8. Student presentation — Shohei** | 25 min | 15 min talk + 5 min discussion (Shohei facilitates) + 5 min swap/buffer. |
| 1:40 | **9. No Free Lunch** | 10 min | Wolpert's NFL; averaged over all worlds no learner wins; why the prior is doing the work. Poll 3 (NFL). |
| 1:50 | **10. Hierarchical Bayes + close** | 10 min* | **Variant A (teaser, ~5 min):** priors over priors; Chibany's per-student bento rates; T3 Ch 5 assigned. **Variant B (full, ~15 min):** teaser + worked two-level Beta-Binomial + shrinkage. Then Week 5 preview. |
| 2:00 | End | (buffer absorbed) | |

\* Block 10 is **10 min if Variant A, ~20 min if Variant B.** Variant B runs the session ~10 min long; that's intended — it only spends slack, and the instructor opts into it only when the day is already on schedule. The Week 5 preview + close (~3 min) is appended after whichever variant is used.

**Deck size target:** ~75–90 slides depending on how many Variant-B slides are kept (sequential-reveal build-ups inflate the count; the size-principle arithmetic alone is ~6 slides, the Variant-B Beta-Binomial worked example ~5). Lighter than Week 2/3 because 25 min is presentation, not slides.

---

### Block 1: Welcome + Clusters walkthrough (10 min)

- 2 min: welcome, one-line agenda. No round-robin.
- 8 min: **Clusters assignment walkthrough.** This is a *tour of the stencil*, not a re-derivation.
  - Assignment 1: "Gaussians, Categories, and Clusters." **Due Fri Jun 5, 2026, 8:00 PM.** 7.5% of grade.
  - Three problems: (1) Gaussian-Gaussian conjugate model — they already have this from Week 3; (2) Gaussian mixture / categorization — Bayes' rule over two category Gaussians; (3) clustering. Maps to textbook T1 Ch 5 and T3 Ch 5.
  - The **GenJAX notebook (`clusters.ipynb`) is the canonical stencil.** `clusters_python.ipynb` and `clusters_nosoln.Rmd` are non-GenJAX paths for students who want them — same math, same credit. Matlab on request.
  - "Open in Colab" links are live on the assignments page; point at them.
  - Tell them Problem 1 is doable *today* (it's Week 3 material); Problems 2–3 lean on this week + T3 Ch 5.
- **Contingency:** if questions run long, cut to "the rest is on the assignments page, DM me" — do not let this block bleed into the generalization content.

### Block 2: The generalization problem (8 min)

- Open with the phenomenon, not the definition (show-before-tell): Chibany saw three tonkatsu lunches at ~500g; is a 480g lunch tonkatsu? A 700g one? Let students answer before naming anything.
- **Generalization = deciding when to extend a property from observed stimuli to a novel one.** No two stimuli are identical, so this is unavoidable and pervasive: word learning, categorization, stereotypes, property induction.
- **Shepard (1987), universal law of generalization:** probability of generalization decays *exponentially* with distance in *psychological* space. Define "psychological space" explicitly — it is not raw stimulus space.
- **Poll 1** (SP25 Bayesian Generalization quiz, item "Universal Law"): *"Shepard's universal law: generalization decays/grows ___ in ___ space."* Options: exp. decay / psychological (correct); exp. decay / stimulus; exp. growth / psychological; exp. growth / stimulus. Reveal: decay, psychological — and that's *why* we need a model of the psychological space.

### Block 3: The Bayesian generalization framework (12 min)

- The move: instead of measuring distance directly, posit a **hypothesis space** of candidate concepts and let Bayes do the generalizing.
- **Notation lock-in slide** (define before use, per CLAUDE.md):
  - $h$ — a hypothesis, a candidate concept (a *set* of stimuli that share the property). Define "consequential subset" (Shepard's term) here.
  - $\mathcal{H}$ — the hypothesis space, all candidate $h$.
  - $X = \{x_1,\dots,x_n\}$ — the observed examples of the concept.
  - $y$ — a novel stimulus we are asked to generalize to.
- **Prior** $p(h)$: domain knowledge — which concepts are "natural" before data. The *choice of hypothesis space is itself a strong prior* ($p(h)\approx 0$ for unnatural concepts not in $\mathcal H$).
- **Likelihood** $p(X \mid h)$: how probable the examples are if $h$ is the true concept. (The size principle, Block 4, is a claim *about this term*.)
- **Posterior** $p(h \mid X) \propto p(X \mid h)\,p(h)$.
- **Generalization** = posterior-weighted vote:
  $$p(y \in C \mid X) = \sum_{h} \mathbf{1}[\,y \in h\,]\; p(h \mid X)$$
  Define the bold-1 indicator $\mathbf{1}[\,y\in h\,]$ in a dim caption. Generalization to $y$ = total posterior mass on hypotheses that *contain* $y$.
- Emphasize: this one equation drives **both** games today. Continuous vs. discrete only changes what $\mathcal H$ is.
- **Four figure slides — the Tenenbaum & Griffiths (2001) BBS integration construction**, all on one shared stacked figure (candidate consequential-interval hypotheses on top, posterior-weighted-vote gradient below, shared x-axis):
  - *One datum → the posterior-weighted vote* — overview: one observed point $x$, the stack of overlapping intervals (thickness $\propto$ strong-sampling likelihood $1/|h|$), and the vote sum below.
  - *Vote for $y = x$* — all 7 hypotheses contain $y$; the bar at $x$ is the full sum (gradient peak).
  - *Vote for $y = x+1$* — the 2 smallest (most likely) intervals drop out and grey; 5 of 7 vote; bar is shorter.
  - *Vote for $y = x+2$* — only the 2 widest (least likely) intervals reach $y$; bar is short. Close: sweeping $y$ traces an **approximately exponential** decay — Shepard's universal law *derived* rather than assumed.
  Figures by `scripts/build_tg_integration_plot.py` → `images/tg_vote.png`, `tg_vote_y0/1/2.png`. Each highlight slide labels the chosen $y$ at the top and greys the hypotheses (and their gradient bars) that don't contain it.

### Block 4: The size principle (10 min)

- **Strong vs. weak sampling** — the distinction is *an assumption about how the examples were generated*, and it changes the likelihood:
  - **Weak sampling:** examples are generated some other way, then *labeled* by whether they're in $h$. Likelihood is $1$ if all examples $\in h$, else $0$. Independent of $|h|$.
  - **Strong sampling:** each example is drawn *uniformly at random from within $h$*. Then $p(x \mid h) = 1/|h|$ for $x \in h$, and $p(X \mid h) = (1/|h|)^n$.
- **The size principle:** under strong sampling, smaller hypotheses get higher likelihood — and *exponentially* more so as $n$ grows, because $(1/|h|)^n$.
- Intuition: the **"suspicious coincidence."** If you saw {60, 80, 10, 30} and the concept were "multiples of 10", that's unremarkable. If the concept were "even numbers", it's a suspicious coincidence that none of the four happened to be 2, 4, 6, … — strong sampling penalizes the larger hypothesis for failing to predict the tight clustering.
- **Poll 2** (SP25 quiz, item "Strong sampling"): *"What is strong sampling?"* Options: stimulus generated uniformly at random from the true hypothesis (correct); stimulus has probability one given the true hypothesis [= weak sampling]; larger hyps get smaller prior; smaller hyps get smaller prior. Reveal: uniform-at-random-from-the-hypothesis; note the distractor "probability one" is *weak* sampling.

### Block 5: Rectangle game — continuous concept learning (15 min)

- **Gnarbles** (Tenenbaum's healthy-levels framing): a gnarble is a rectangle whose width lies in some interval; equivalently, a 2-D concept = an axis-aligned rectangle in (e.g.) insulin × cholesterol space.
- Build up in order (each step has a dark-theme figure from `scripts/build_continuous_concept_plots.py`):
  1. **1-D first.** Concept = an interval $[\ell, u]$. Observe a few points. Hypothesis space = all intervals. Strong sampling → likelihood $\propto (1/\text{length})^n$. *Figure `cc_1d.png`*: observed points on a line, candidate intervals above them at opacity/thickness ∝ posterior weight.
  2. **Generalization gradient.** Plot $p(y \in C \mid X)$ as a function of $y$: high inside the data range, decaying outside. The decay rate is set by the posterior — this *recovers Shepard's exponential law* as a consequence, not an assumption.
  3. **Effect of $n$.** More examples → tighter generalization (size principle: large intervals lose likelihood fast). One example → broad, diffuse generalization.
  4. **2-D rectangle.** Same machinery, hypothesis = axis-aligned rectangle. *Figure `cc_2d.png`*: dots in a plane, nested candidate rectangles (brightest/thickest = smallest = highest posterior), with $r$ (data range), $d$ (extension past $r$), and $n$ (dot count) all labelled.
  4b. **The rectangle experiment** (own slide): Tenenbaum (1999) ran it behaviourally — subjects saw $n$ dots ($n$ from 2 to 50), drew the rectangle, measure = $d$.
  4c. **The result** (own slide): *Figure `tg_results.png`* — $d$ vs $r$, one curve per $n$, recreated dark-theme from Tenenbaum & Griffiths (2001) Fig. a. Fewer examples → generalize further; the Bayesian model reproduces the family.
  5. **The exponential prior.** Pure size principle slightly over-extends; an **exponential prior over rectangle size** fixes the fit. *Figure `cc_exp_prior.png`* + the density $p(s)=\lambda e^{-\lambda s}$ — this is the **first time the class meets the exponential distribution**, so define it properly (rate $\lambda>0$, mean $1/\lambda$, monotonically decreasing).
- Payoff line: the *continuous* concept learner is just the framework equation with $\mathcal H$ = intervals/rectangles.

### Block 6: Number game — discrete concept learning (13 min)

- **Tenenbaum's number game.** Task: observe one or more "yes" numbers (1–100); judge whether other numbers are "yes". Show the phenomenon first (the N=20 generalization-judgment data): {60} → diffuse similarity; {60, 80, 10, 30} → "multiples of 10"; {60, 52, 57, 55} → "numbers near 60". One example vs. four flips graded → rule-like.
- **The two phenomena to explain:** (a) generalization can look similarity-based (graded) *or* rule-based (all-or-none); (b) learning happens from very few examples.
- **Discrete hypothesis space.** $\mathcal H$ = mathematical-property hypotheses (even, odd, primes, squares, multiples of $k$, powers of $k$ — ~24) ∪ magnitude-interval hypotheses (numbers in $[a,b]$). Prior: math properties vs. interval families.
- **Size principle worked numerically** (sequential-reveal build-up — this is the arithmetic centerpiece of the day):
  - Concept "multiples of 2": 50 numbers in 1–100, so $p(x \mid h) = 1/50 = 2\%$ each.
  - Concept "multiples of 10": 10 numbers, so $p(x \mid h) = 1/10 = 10\%$ each.
  - One example $x=60$: $p(60\mid \text{mult-2}) = 1/50$ vs. $p(60\mid\text{mult-10}) = 1/10$ — mult-10 already 5× better.
  - Four examples {10,30,60,80}: $p \mid \text{mult-2} = (1/50)^4 \approx 1.6\times10^{-7}$; $p \mid \text{mult-10} = (1/10)^4 = 10^{-4}$ — now ~625× better. *This* is why four examples produce a rule and one example produces graded similarity.
- **Likelihood → posterior — strong vs. weak sampling (4-slide sub-sequence).** Turns the likelihood arithmetic into an explicit posterior over a two-hypothesis space $\mathcal H = \{$multiples of 10, even numbers$\}$ with a flat prior, then contrasts the sampling assumptions:
  - *From likelihood to posterior* — bridge: state the 2-hypothesis model, flat prior, Bayes' rule.
  - *Strong sampling, $X=\{60\}$* — posterior $\approx 0.83 / 0.17$ (5:1 likelihood ratio). Graded.
  - *Strong sampling, $X=\{60,80,10,30\}$* — posterior $\approx 0.998 / 0.002$ ($5^4 = 625{:}1$). Rule-like; the suspicious coincidence made quantitative.
  - *Weak sampling — eliminate, but don't rank* — likelihood is $1$/$0$ (size-blind). Be precise: weak sampling **can** move the posterior, by **ruling out** any hypothesis a datum falls outside of (likelihood $0$). What it **can't** do is *rank* the hypotheses that all still contain the data — every survivor keeps likelihood $1$, so the posterior over the survivors is the renormalised prior. In this example both hypotheses contain every example, nothing is eliminated, so the posterior sits at $0.5/0.5$ (and the $0.5$ is an artefact of *two surviving hypotheses + flat prior*). The teaching point: weak sampling can eliminate but cannot *prefer the smaller* hypothesis, so it cannot produce the suspicious-coincidence effect — that needs strong sampling. Figures: `scripts/build_suspicious_coincidence_plot.py` → `images/suspicious_strong_1.png`, `suspicious_strong_4.png`, `suspicious_weak.png`.
- Tie back: same equation as the rectangle game, $\mathcal H$ now discrete. Both phenomena (graded vs. rule-like) fall out of the posterior — no extra mechanism.

### Block 7: Bridge → Shohei's paper (2 min)

- **One slide.** Tenenbaum & Xu (2000), *Word learning as Bayesian inference*: a child hears "this is a dax" pointing at three Dalmatians. Is a poodle a dax? A cat? — this is **exactly the number game**, with the hypothesis space = candidate word meanings (subordinate / basic-level / superordinate categories) and the size principle explaining why three subordinate examples → a subordinate meaning ("suspicious coincidence" if the word meant "dog").
- Say explicitly: "Everything Shohei is about to present runs on the discrete framework you just saw — watch for the size principle doing the work." Hand off; start the 5-min swap buffer.

### Block 8: Student presentation — Shohei (25 min)

- 15 min talk, 5 min discussion (Shohei facilitates, ≥3 questions), 5 min swap/setup buffer folded in.
- Instructor stays hands-off during discussion unless it stalls. If it stalls, the lecture's own hook: "How does the size principle show up in their word-learning data?"

### Block 9: No Free Lunch (10 min)

- **Wolpert's No Free Lunch theorem.** Averaged over *all possible worlds*, no learning algorithm beats any other. Sequence-prediction illustration: given $x_1, x_2$, predict $x_3$ — with all hypotheses equally weighted, every prediction is 50/50.
- The point for this course: a learner only works because the **distribution over worlds is constrained** — i.e., because it has a non-flat **prior**. Generalization is impossible without inductive bias.
- This closes the loop on the whole day: the prior $p(h)$ and the hypothesis space $\mathcal H$ in the framework equation are not bookkeeping — they are *the entire reason generalization is possible at all*.
- **Poll 3** (SP25 quiz, item "No free lunch"): *"What is the No Free Lunch theorem (for prediction)?"* Options: when all hypotheses are possible, there's nothing you can learn to predict (correct); learning one hyp hurts another; free-lunch social-debt joke; generalizing can hurt a learner. Reveal: option 1 — and connect to "this is why your prior matters."

### Block 10: Hierarchical Bayes — two variants + close

**Authored both ways. The instructor decides live which to run, by where the clock is at 1:50.** In the deck, the two variants are fenced with HTML comment markers (`<!-- HIER-BAYES VARIANT A: TEASER -->` … and `<!-- HIER-BAYES VARIANT B: FULL BLOCK -->` …) so whichever is unused can be deleted, or simply skipped with Reveal's slide-menu, without disturbing the other. The shared teaser slides (the first three) are physically part of Variant A; Variant B *opens by reusing those same three* then continues — so running B means "keep going past the teaser," running A means "stop after the teaser."

#### Variant A — teaser (~5 min, 3 slides) — use if behind schedule

- **Slide A1 — the setup.** Each student in Chibany's class has their *own* tonkatsu/hamburger ratio $\theta_i$. The ratios aren't identical, but they aren't unrelated either — they're drawn from a *shared* distribution. Show before tell: "Should learning Aoi's ratio tell us anything about Ben's?"
- **Slide A2 — priors over priors.** Put a prior on the parameters of the prior: $\theta_i \sim \text{Beta}(a,b)$, and $(a,b)$ themselves are unknown and inferred. One picture of the two-level graphical model: $(a,b) \to \theta_i \to$ observed bentos.
- **Slide A3 — why it matters.** This lets a learner *learn the prior from data* — exactly the inductive bias NFL just said you need. It's also how "overhypotheses" (Kemp, Perfors & Tenenbaum 2007) get learned. Name-drop, don't derive.

#### Variant B — full block (~15 min, ~8 slides) — use if on schedule

- **Opens with A1–A3** (the same three teaser slides — they are the conceptual setup either way).
- **Slide B4 — the pooling spectrum.** Three ways to handle six students' bento data, as a slide with three columns:
  - *Complete pooling:* one $\theta$ for everyone — ignores that students differ.
  - *No pooling:* a separate $\theta_i$ per student, unrelated — ignores that they're all Chibany's customers.
  - *Hierarchical (partial pooling):* $\theta_i \sim \text{Beta}(a,b)$ — the middle path; each student informs the shared $(a,b)$, which in turn informs every student.
- **Slide B5–B6 — the two-level model, written out.** Sequential-reveal build-up:
  $$(a,b) \sim \text{prior}; \quad \theta_i \mid a,b \sim \text{Beta}(a,b); \quad k_i \mid \theta_i \sim \text{Binomial}(n_i,\theta_i)$$
  Define each symbol on first use ($k_i$ = tonkatsu count for student $i$, $n_i$ = that student's bento count). The posterior $p(a,b,\{\theta_i\} \mid \text{data})$ — note it does *not* have a clean closed form; this is where sampling/GenJAX comes in (callback to Week 2's GenJAX setup; the hierarchical `bento_day()` exercise).
- **Slide B7 — shrinkage, shown.** A figure-style slide: each student's raw tonkatsu fraction $k_i/n_i$ vs. their posterior mean $\hat\theta_i$. The posterior means are *pulled toward the group mean* — students with little data shrink more, students with lots of data barely move. This is the payoff: hierarchical Bayes automatically borrows strength.
- **Slide B8 — overhypotheses, properly.** With the model in hand, restate Kemp/Perfors/Tenenbaum 2007: the shape bias, the object/substance distinction — these are *learned* second-level hypotheses ($\,(a,b)$ generalised to a distribution over kinds). One sentence connecting it to NFL: the hierarchy is where a learner *acquires* its inductive bias instead of being born with it.

#### Close (~3 min — appended after whichever variant ran)

- Assign **T3 Ch 5 (Mixture models)** as the pre-read for Week 5. (If Variant B ran, note T3 Ch 5 also formalises the same partial-pooling idea.)
- **Week 5 preview:** Bayes nets + causal Bayes nets. (Confirm Week 5's student presenter against `readings_map.yml` before class — Week 3 deck's "next week" slide and the readings map disagreed on a name once; verify.)
- Thank Shohei, thank the room.

---

## Contingencies

- **Presentation overruns.** Block 8's 5-min swap buffer absorbs minor overrun. If Shohei runs to ~30 min total, run **Variant A** (teaser) for Block 10, cut Block 9's poll, and tighten NFL to the one core slide (3 min). Never cut the hier-Bayes teaser (Variant A) entirely — even A3 alone is the assigned-reading hook for Week 5.
- **Hier-Bayes variant decision (live, at ~1:50).** On schedule or ahead → **Variant B** (full block, runs ~10 min over, intended). Behind → **Variant A** (teaser, ends on time). The deck holds both; nothing else changes between them.
- **Clusters walkthrough overruns.** Hard-cap at 10 min; remainder goes to a DM/office-hours offer. The generalization core cannot start late.
- **Polls run long.** All three polls are commit-before-reveal, ≤1.5 min each. If behind, Poll 1 is the most cuttable (universal law is also stated on the slide).
- **Both games must survive.** If the session is somehow compressed, trim the rectangle game's 2-D experiment detail (Block 5 step 4) and the exponential-prior slide before cutting any number-game arithmetic — the discrete worked example is what Shohei's paper builds on and is the highest-value 5 minutes of the day.

---

## Poll provenance (per CLAUDE.md standing rule)

All three polls sourced from the SP25 **Bayesian Generalization** quiz, `archive/canvas_export_sp25/g90f0d9a6c127ebc338dedf7fbd11b4f8/`:

| Poll | Block | SP25 quiz item | Lands at |
|------|-------|----------------|----------|
| 1 | 2 | "Universal Law" (Shepard 1987) | after stating the universal law |
| 2 | 4 | "Strong sampling" | after stating the size principle |
| 3 | 9 | "No free lunch" | after stating Wolpert's NFL |

The quiz's fourth item ("Building generalization models") is held in reserve — it fits as a Block 5/6 check if a poll slot opens, but three is the target.
