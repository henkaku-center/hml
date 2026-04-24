# Week 2: Shared Outline
## Friday, April 24, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Required reading (pre-class):** Textbook T1 Ch 4–5 (Conditional, Bayes); T2 Ch 0–1 (GenJAX Colab setup — self-directed)
**Students:** ~6 (finalize name list before class)

---

## Key Design Decision

**This redesign repairs a scope miscalibration in the first draft of Week 2.** The initial plan spent 25 min on Marr and 25 min on a GenJAX live demo, leaving no room for the math backbone (expected value, discrete distributions, continuous probability, Gaussians) that SP25's second lecture covered. Without that math, Week 3 (conjugate Bayes) has nowhere to stand.

The fix: **Marr becomes a 10-min frame**, not a 30-min centerpiece. GenJAX's live demo is cut — students have T2 Ch 0–1 as self-directed reading and the model-building is re-introduced in Week 4. The recovered ~40 min goes to the math backbone, threaded through the **Chibany bento narrative** so notation, examples, and intuition all reinforce each other.

**Every equation is built up across sequential slides** (SP25 style). Each "piece" — a term, an index, a name, a numeric substitution — appears on its own slide. This is implemented as a sequence of `content_slide` calls sharing a title (via `sds_slides.SDSDeck.build_slides`), so advancing one slide = revealing one line. Students see formulas emerge, not land fully-formed.

Chibany is the running example through every math block:
- Discrete: meal is Bernoulli(0.7), tonkatsu vs. hamburger.
- Continuous: weight is Gaussian (tonkatsu ~ N(500, σ²); hamburger ~ N(350, σ²)).
- Gaussian-Gaussian update: given an observation of weight = 450g, what's the posterior over the *mean weight* given a prior over the mean? This is the opening move of Week 3.

Paper presentations are introduced during Block 8. Signup is during class; Weeks 4–12 are candidate slots for the ~6 students.

---

## Session Plan

| Time | Block | Duration | What Happens |
|------|-------|----------|--------------|
| 0:00 | **1. Welcome back + meet Chibany** | 8 min | 3 min syllabus pulse + 5 min Chibany/bento intro (opaque boxes, weights, 70/30 prior). |
| 0:08 | **2. Marr's three levels (compressed)** | 7 min | L1/L2/L3 (one slide each) + cab-problem check-in. Trimmed from 10 → 7 to free time for Gaussian visuals. |
| 0:15 | **3. Notation lock-in** | 3 min | H = hypothesis, D = data. Three sequential-reveal slides. |
| 0:18 | **4. Joint + marginalization, Chibany-style** | 12 min | **Bridge: sick-friend in H/D notation (3 slides).** Then the 2×2 bento joint, marginal, conditional. |
| 0:30 | **5. Expected value + discrete distributions** | 15 min | E[X], Var[X], Bernoulli, Binomial. **Ends with a real matplotlib PMF plot.** |
| 0:45 | **6. Continuous probability + the Gaussian** | 20 min | PMF → PDF (with shrinking-bins figure). Gaussian formula (built up + shape figure). Two Gaussian likelihoods overlaid (figure). Continuous-Bayes worked for weight = 450g. |
| 1:05 | **Break** | 5 min | |
| 1:10 | **7. Gaussian-Gaussian update** | 25 min | Motivation for inferring μ (3 slides). Prior, likelihood. **Derivation sketch (complete the square).** Precision visualized. Posterior built numerically. **GG posterior curve figure (prior × likelihood → posterior).** N-observation generalization (own build-up). Close. |
| 1:35 | **8. Paper presentations — rubric + signup** | 10 min | Rubric highlights + signup for Weeks 4–12. |
| 1:45 | **9. Admin + Week 3 homework** | 15 min | Three syllabus changes. Week 3 readings (T3 Ch 1 + Ch 4). Preview. |
| 2:00 | End | (buffer absorbed) | |

**Deck size:** 105 slides total. Sequential-reveal math + six pre-generated matplotlib figures (see `images/`). Regenerate with `python3 generate_images.py && python3 build_slides_week2.py`.

---

### Block 1: Welcome back + syllabus changes (5 min)

- Two or three student voices on Week 1; NOT a round-robin.
- **Targeted check:** "Anyone blocked on GenJAX Colab setup?" If yes, office hours — don't debug live.
- Flag two changes since Week 1:
  - Paper presentations are in (more at Block 8).
  - Reflections are 6 of 12, not 8 of 13 (more at Block 9).
- Do NOT open with admin detail. Move into content.

### Block 2: Marr's three levels, compressed (10 min)

**This is the framing unit, not the centerpiece.** Three slides (one per level), one check-in, done.

Open: *"Last week your visual system inferred brightness from pixels. Now let's name the framework that makes such 'inference from observations' a scientific question."*

**L1 slide (2 min).** What problem is Chibany solving? — "compute P(meal | weight)." The normative answer is Bayes. L1 specifies **what** the correct computation is. Choosing L1 is not neutral — if the goal were "minimize time to answer," you'd have a different L1 and a different normative answer.

**L2 slide (2 min).** Algorithms. Same L1, different implementations: enumerate (what we'll do today for 2 hypotheses); sample (what GenJAX does; we use it later); "always guess tonkatsu" (a BAD L2 — it's an algorithm, just a poor one).

**L3 slide (2 min).** Brain vs. JAX arrays. Fast. Full treatment in Week 11 (Deep NNs).

**Check-in slide (4 min).** Revisit the cab problem from Week 1. *"Students mostly said 80%. At which level was the mistake?"* Target: L1 says P(blue | report); 80% is a wrong-L2 claim. Humans use a non-Bayesian L2 on this problem, systematically. This is the heuristics-and-biases thread that runs through Weeks 5+.

Close the block and move on. **Do not let this block expand.**

### Block 3: Notation lock-in (3 min)

One build-up (3 slides):
1. Bare statement: "Last week I mixed h/d. From today, H = hypothesis (hidden), D = data (observed). Always."
2. Add the formula: `P(H=h | D=d) = P(D=d | H=h) · P(H=h) / P(D=d)`
3. Add piece labels: posterior, likelihood, prior, evidence.

**Move on before this turns into apology theater.** The goal is alignment, not penance.

### Block 4: Joint + marginalization, Chibany-style (12 min)

Reintroduce joint / marginal / conditional in the bento frame — students saw these in Week 1 under sick-friend/cab notation; here they land under H/D with Chibany.

Setup slide (1 min). Two discrete hypotheses (tonkatsu/hamburger), two discrete observations (heavy/light — we'll continuize them in Block 6). The joint is a 2×2 table.

**Build-up 1: the joint (4 slides, ~5 min).**
1. Blank 2×2 table: rows = meal ∈ {tonkatsu, hamburger}, columns = weight ∈ {heavy, light}.
2. Add prior 0.7 / 0.3 to a marginal column.
3. Fill in the conditionals: P(heavy | tonkatsu) = 0.9, P(heavy | hamburger) = 0.2. Then fill in the four joint cells by multiplying.
4. Highlight the joint: P(tonkatsu, heavy) = 0.63; P(tonkatsu, light) = 0.07; P(hamburger, heavy) = 0.06; P(hamburger, light) = 0.24. Sanity check: sum = 1.

**Build-up 2: marginalization (3 slides, ~3 min).**
1. P(heavy) = P(tonkatsu, heavy) + P(hamburger, heavy) = 0.63 + 0.06 = 0.69. *"Sum the joint over the hidden variable."*
2. P(light) = 0.07 + 0.24 = 0.31. Check: 0.69 + 0.31 = 1.
3. Named move: **marginalization.** "Given the joint, summing over H gives the marginal on D, and vice versa. Week 1 called this the sum rule."

**Build-up 3: conditional as restrict-and-renormalize (3 slides, ~3 min).**
1. "Observe heavy. What's P(meal | heavy)?"
2. Keep only the `heavy` column of the joint: 0.63 (tonkatsu, heavy), 0.06 (hamburger, heavy).
3. Renormalize by 0.69: P(tonkatsu | heavy) = 0.63/0.69 ≈ 0.913; P(hamburger | heavy) = 0.06/0.69 ≈ 0.087. *"Conditioning = zoom in on a slice of the joint and renormalize."*

**Close slide (~1 min).** Three reminders: (a) joint = full picture, (b) marginal = sum over the thing you don't care about, (c) conditional = slice and renormalize. This is the same Bayes from Week 1; now you can see it as a table operation.

### Block 5: Expected value + discrete distributions (15 min)

**Expected value (5 min, 4 slides build-up).**
1. Definition: for a discrete RV X with values {x_i} and probabilities {p_i}, E[X] = Σ x_i · p_i.
2. Chibany example: encode meal numerically (tonkatsu = 1, hamburger = 0). Then E[meal] = 1·0.7 + 0·0.3 = 0.7. *"The expected value of the indicator **is** the probability."*
3. Variance: Var[X] = E[(X - E[X])²] = E[X²] - E[X]². For Bernoulli(0.7): Var = 0.7 · 0.3 = 0.21.
4. Interpretation: E[X] = center of mass; Var[X] = spread. Used everywhere downstream.

**Bernoulli distribution (4 min, 3 slides build-up).**
1. Definition: X ~ Bernoulli(p). P(X=1) = p; P(X=0) = 1−p. One slide.
2. Bento as Bernoulli: meal ~ Bernoulli(0.7). *"One bento. One flip of a weighted coin."*
3. PMF plotted: two bars, heights 0.7 and 0.3. Note on parameter estimation: "In Week 3 we'll ask where 0.7 came from. For today it's given."

**Binomial distribution (6 min, 4 slides build-up).**
1. Setup: Chibany counts how many tonkatsu bentos in a week of 5. Each day: Bernoulli(0.7), independent. Let Y = total tonkatsu across the 5 days.
2. Formula: P(Y = k) = C(n, k) · p^k · (1-p)^(n-k). Name each piece: n trials (5), k successes (count), p probability per trial (0.7).
3. Worked: P(Y = 5) = 1 · 0.7^5 · 0.3^0 ≈ 0.168. P(Y = 3) = 10 · 0.7^3 · 0.3^2 ≈ 0.309. Note which is largest.
4. Plot the full PMF bar chart for n=5, p=0.7. Visual mode at k=4. *"This is what Chibany expects to see across a week. In Week 3, this becomes the likelihood."*

### Block 6: Continuous probability + the Gaussian (20 min)

**From PMF to PDF (5 min, 4 slides build-up).**
1. "Weight isn't heavy-or-light — it's a real number. We need continuous probability."
2. Binning argument: discretize weight to 10-gram bins → PMF over bins. Shrink bins → PDF as the limit. Plot a PMF with narrowing bin widths over the same histogram shape.
3. The density f(x) is NOT a probability — it's probability per unit. P(X in [a,b]) = ∫_a^b f(x) dx.
4. Why P(X = 450g) = 0: integrating over a single point is 0. But P(X in [449, 451]) ≈ f(450) · 2. *"For continuous RVs, the PDF value is what you multiply by an interval width to get a probability."*

**The Gaussian formula (8 min, 5 slides build-up).**
1. Bare formula: N(x | μ, σ²) = (1 / √(2πσ²)) · exp(−(x−μ)² / (2σ²)).
2. Name each piece: μ (mean / center), σ² (variance / spread), the exponential with squared deviation (what makes it "peak at μ, fall off fast").
3. The normalizer √(2πσ²): why it's there (so the density integrates to 1). One line, don't derive.
4. Symmetry and shape: the bell curve. At x = μ, the density is 1/√(2πσ²). At x = μ ± σ, the density is ~60% of that peak.
5. **Standard examples for bento weights:** tonkatsu weight ~ N(500, 30²); hamburger weight ~ N(350, 30²). Plot both densities on the same axes (overlapping tails between 380g and 470g).

**Back to Bayes with continuous likelihoods (7 min, 6 slides build-up).**
1. Chibany weighs today's bento: D = 450g. What's P(meal | weight = 450g)?
2. Prior stays discrete: P(tonkatsu) = 0.7, P(hamburger) = 0.3.
3. Likelihood is now a Gaussian DENSITY: P(weight=450g | tonkatsu) = N(450 | 500, 30²) ≈ 0.00270. Name it f_T. P(weight=450g | hamburger) = N(450 | 350, 30²) ≈ 0.00044. Name it f_H.
4. Numerator 1: f_T · 0.7 ≈ 0.00189. Numerator 2: f_H · 0.3 ≈ 0.000132. Evidence = 0.002022.
5. Posterior: P(tonkatsu | 450g) ≈ 0.935; P(hamburger | 450g) ≈ 0.065.
6. Interpretation: *"With a Gaussian likelihood, 450g looks much more tonkatsu-like than with coarse heavy/light bins. The prior (0.7) updated to 0.935 — the likelihood dominated. Contrast with Block 4's coarse-bin version."*

### Break (10 min)

### Block 7: Gaussian-Gaussian update (25 min)

**This block launches Week 3.** Up to now, we've been using Bayes to infer a hypothesis (meal). Now: use Bayes to infer a *continuous parameter* from continuous observations. This is the conjugate-Bayes opening move.

**Setup (3 min, 2 slides).**
1. New question: "Forget which meal. Focus on one meal type, say tonkatsu. The textbook said tonkatsu weight ~ N(500, 30²). But what if Chibany doesn't know the mean μ? They want to estimate it from observed weights."
2. Reframe: now H = μ (the hidden mean), D = observed weights. Bayes: P(μ | weights) ∝ P(weights | μ) · P(μ). Prior, likelihood, posterior — same structure, different parameterization.

**The prior is a Gaussian (4 min, 3 slides).**
1. Prior: μ ~ N(μ₀, σ₀²). Chibany's prior from last semester's memory: μ₀ = 500, σ₀ = 20. "I think tonkatsu is around 500g, give or take."
2. Plot the prior as a bell curve centered on 500.
3. Note: we're putting a Gaussian density *over a parameter*, not over data. This is the conceptual leap — priors can be distributions over anything hidden, including parameters of other distributions.

**The likelihood (4 min, 3 slides).**
1. Chibany observes ONE weight: D₁ = 510g. Assume σ (data noise) is known = 30. Likelihood: P(D₁ = 510 | μ) = N(510 | μ, 30²). As a function of μ, this is another Gaussian — peaked at μ = 510, width 30.
2. Plot the likelihood as a function of μ on the same axes as the prior.
3. Name what we're doing: "we're about to multiply two Gaussians."

**Posterior via conjugacy (10 min, 7 slides build-up).**
1. Claim: if prior is Gaussian and likelihood (as a function of μ) is Gaussian, the posterior is **also** Gaussian. This is "Gaussian-Gaussian conjugacy."
2. The magic formulas (state, don't derive — that's Week 3 homework from T3 Ch 4):
   - 1/σ_post² = 1/σ₀² + 1/σ²   (precisions add)
   - μ_post = σ_post² · (μ₀/σ₀² + D₁/σ²)
3. Name the intuition: *"Precision = 1/variance. Adding precisions = combining information. The posterior mean is a precision-weighted average of prior mean and observed data."*
4. Plug in numbers: σ₀² = 400, σ² = 900. Posterior precision = 1/400 + 1/900 = 13/3600. Posterior variance ≈ 277; posterior std ≈ 16.6. Prior std was 20; data std is 30; posterior is tighter than both.
5. Posterior mean: (500/400 + 510/900) · 277 ≈ (1.25 + 0.567) · 277 · 1/3600·3600... let me redo: μ_post = 277 · (500/400 + 510/900) = 277 · (1.25 + 0.5667) = 277 · 1.8167 ≈ 503.2. "The posterior mean moved from 500 toward 510, weighted by how precise each source is."
6. Plot the posterior bell curve on the same axes: narrower than either input, centered between them (closer to the prior since the prior was more precise).
7. Generalize: **with N observations instead of 1, you just sum N likelihood precisions.** One slide. This is the hinge for Week 3 and Week 4.

**Close the block (4 min, 2 slides).**
1. Recap: same Bayes rule. Prior × likelihood → posterior. The math is the same. The objects changed: hypotheses became parameters; likelihoods became densities; the result is a density instead of a table.
2. Named move: **conjugacy.** Next week: *why* Gaussian-Gaussian conjugates, and other conjugate pairs (Beta-Binomial, Dirichlet-Multinomial) for discrete data.

### Block 8: Paper presentations — rubric + signup (10 min)

**Tighter than the original plan.** Don't re-lecture the rubric; email the PDF.

1. *Why now (1 min).* "Enrollment is 6. Each of you presents once. 7.5% of grade. Replaces some reflection weight."
2. *Rubric in one slide (3 min).* Out of 5: understanding 1.5, coverage 1.5, clarity 1.0, discussion 0.5, time 0.5. Meet with me in office hours the week before. Full guidelines: `resources/classPresentationGuidelines.pdf`, email after class.
3. *Signup (6 min).* Nine slots (Weeks 4–12). Six students. Three slots stay open for contemporary-ML / buffer content.

### Block 9: Admin + Week 3 homework (10 min)

1. *Three syllabus changes (3 min, one slide).* 12 sessions (not 13). 6-of-12 reflections (not 8-of-13). Presentations exist (Block 8).
2. *Week 3 readings (4 min).* Friday May 15 — Conjugate Bayes. Required: T3 Ch 4 (Bayesian learning with Gaussians — picks up directly from Block 7). Recommend also skimming T1 Ch 6 (glossary review).
3. *Preview Week 3 and beyond (3 min).* The Gaussian-Gaussian update we just did is the opening example of Week 3. Week 4 brings hierarchical Bayes (Chibany's *distribution of tonkatsu rates* across students). Close warmly.

---

## Visual Aids (approximate slide list — total ~55–65 slides)

Broken out by block. Each "step" is a slide; titles repeat across a build-up.

- Title slide (1)
- Block 1: agenda (1), section-break (1), "two changes" (1) — 3 slides
- Block 2: agenda (1), section-break (1), L1 (1), L2 (1), L3 (1), check-in (1) — 6 slides
- Block 3: agenda (1), section-break (1), notation build-up (3), **poll: posterior definition (prompt + reveal)** — 7 slides
- Block 4: agenda (1), section-break (1), setup (1), joint build-up (4), marginal build-up (3), conditional build-up (3), close (1) — 14 slides
- Block 5: agenda (1), section-break (1), E[X] build-up (4), Bernoulli build-up (3), Binomial build-up (4) — 13 slides
- Block 6: agenda (1), section-break (1), PMF notation checkpoint (1), PMF→PDF build-up (4, **poll: Derek's density prompt folded before 4/4**), Gaussian-formula build-up (5), continuous-Bayes build-up (6) — 18 slides
- Break (1)
- Block 7: agenda (1), section-break (1), setup (2), prior (3), likelihood (3), **poll: Jamal's posterior (prompt)**, posterior build-up (7), close (2) — 20 slides
- Block 8: agenda (1), section-break (1), why (1), rubric (1), signup grid (1) — 5 slides
- Block 9: agenda (1), section-break (1), syllabus changes (1), Week 3 homework (1), preview (1) — 5 slides

Rough total: ~90 slides. At 2 hours = 120 min this is ~80 seconds per slide on average, which is the right pace for build-up style.

---

## Contingencies

- **Block 4 runs long** (students get stuck on the 2×2 joint): compress Block 5's Binomial slides from 4 → 2 (show formula and one worked number, skip the full PMF plot). Don't cut Block 6 or 7.
- **Block 5 feels too "statistics lecture"** (students glaze over Bernoulli): move faster through E[X]; use the bento examples as the vehicle rather than pausing on abstract definitions.
- **Block 6 runs short on time**: skip the "back to Bayes with continuous likelihoods" sub-block (6 slides). Jump straight from Gaussian formula to Block 7. Students will still see a continuous-Bayes calculation in Block 7 under the Gaussian-Gaussian frame.
- **Block 7 is the priority**: DO NOT cut this. If something else runs long, cut Block 8 down to 5 min (assign signups by email after class) rather than cutting Block 7.
- **A student is stuck on a definition from Week 1** (marginalization, conditional): point them at T1 Ch 4–5 for self-study; don't rewind the class. Offer 1:1 in office hours.
- **Time is short at 1:35**: skip the Block 9 "preview Week 3 and beyond" — the three syllabus changes + Week 3 readings are the priority.
- **Running over at any block boundary**: the three student polls (posterior / Derek's density / Jamal's posterior) can be shortened by skipping the dedicated reveal slide and just announcing the answer aloud. Each poll is a prompt + reveal pair; combining them saves ~45 sec per poll.
