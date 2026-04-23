# Week 2: Speaker Notes

## Slide 1: Week 2 — Levels of Analysis + Bayes Continued

Crisp start. Today's backbone is the second half: continuous probability, Gaussian, and the Gaussian-Gaussian update. Marr is a 7-min frame; Chibany meets us at the top.

## Slide 2: Agenda

_(no speaker notes)_

## Slide 3: Welcome back + meet Chibany

~8 min. First 3 min: syllabus updates + Week 1 pulse. Next 5 min: introduce Chibany and the bento scenario properly, so the rest of the session has a narrative it can actually lean on.

## Slide 4: Two changes since Week 1

State the two facts, move on. If a student asks for detail, say 'I'll get to that at 1:40 / 1:50.' ~1 min.

## Slide 5: Meet Chibany

Slide 1: 'Before we do math, meet Chibany. They're the character we'll use as our worked example all semester. They\'re also the protagonist of the textbook, so reading T3 Ch 1 tonight will top this up.'

## Slide 6: Meet Chibany

Slide 2: 'The hook: opaque bentos. Chibany can\'t directly see the meal. Classic hidden-variable setup. Just like last week\'s checkershadow and Heider-Simmel — an inference problem under incomplete information.'

## Slide 7: Meet Chibany

Slide 3: 'Prior knowledge. Two canonical weights and a 70/30 prior on the meal. Note the prior comes from the world (overheard conversation), not from nowhere — priors are usually knowledge from somewhere else.'

## Slide 8: Meet Chibany

Slide 4: 'Chibany\'s strategy: weigh the bento and update. This is the Week 1 sick-friend move, just with a bento instead of a patient. Prior belief, observation, posterior. Same rule. New anchor.'

## Slide 9: Agenda

_(no speaker notes)_

## Slide 10: Marr's three levels — frame for the whole course

7 min hard cap. Trimmed from the earlier draft to free time for Gaussian visualization. 3 slides (one per level) + check-in. Do NOT let this expand.

## Slide 11: Marr L1 — what problem is being solved?

~2 min. Bayes is the normative answer for 'combine prior + evidence.' Counterfactual: if the goal were 'minimize reaction time,' L1 differs. Choosing L1 IS a modeling move.

## Slide 12: Marr L2 — what algorithm?

~2 min. The bad-algorithm point is important: "always guess tonkatsu" is 70% accurate because of the prior — it's still a well-defined L2, just one that ignores the observation.

## Slide 13: Marr L3 — what implementation?

~2 min. FAST. Land the independence point — this is the thread for the rest of the course.

## Slide 14: Check-in — the cab problem

~1 min. Fast — elicit the answer. Bridge: "humans systematically use a non-Bayesian L2 on this problem; that gap between L1 and L2 is behavioral economics."

## Slide 15: Agenda

_(no speaker notes)_

## Slide 16: Notation lock-in

3 min. Quick. No theatrical apology.

## Slide 17: Notation — one rule, starting today

Slide 1: 'H = hypothesis, D = data. For Chibany, H is the meal, D is the weight. Simple, consistent.'

## Slide 18: Notation — one rule, starting today

Slide 2: 'The formula you saw last week. Same one.'

## Slide 19: Notation — one rule, starting today

Slide 3: 'Name the four pieces. You\'ll see these names the rest of the semester.'

## Slide 20: Agenda

_(no speaker notes)_

## Slide 21: Joint + marginalization — Chibany-style

12 min. Three build-ups + a Week-1 bridge slide. Now in H/D notation with Chibany — students saw these moves last week in the 2-coin-flip grid and in the sick-friend/cab problems.

## Slide 22: Last week's sick-friend problem, in H/D notation

Slide 1: 'Quick re-cast. H = disease hypothesis (note: lowercase h from last week is now uppercase H; content unchanged). D = cough. Same problem, new notation.'

## Slide 23: Last week's sick-friend problem, in H/D notation

Slide 2: 'Same numbers as last week. Prior, likelihood, multiply, sum 'for the evidence.'

## Slide 24: Last week's sick-friend problem, in H/D notation

Slide 3: 'Posterior 0.75 / 0.083 / 0.167. Cold wins despite smoking — priors matter, likelihoods matter, neither alone is enough. Now today: same structure, but with Chibany.'

## Slide 25: Setup — two-by-two Chibany world

~1 min. The 2×2 is the scaffolding. Structurally the same as last week\'s 2-coin-flip grid {HH, HT, TH, TT} — same moves apply. The difference: different numbers, and meal ≠ weight (two variables, not the same coin twice).

## Slide 26: The joint  P(H, D)  — build the 2×2 table

Slide 1: 'Four combinations of (meal, weight). We want the joint probability of each.'

## Slide 27: The joint  P(H, D)  — build the 2×2 table

Slide 2: 'Joint = prior times conditional. Multiply across.'

## Slide 28: The joint  P(H, D)  — build the 2×2 table

Slide 3: 'Sanity check. Sum to 1. Analogy to last week\'s {HH, HT, TH, TT} — the structure is the same; we\'re just working with asymmetric probabilities.'

## Slide 29: Marginalization — sum over what you don't care about

Slide 1: 'What\'s P(heavy) unconditionally? The bento is heavy either because it\'s a heavy tonkatsu OR a heavy hamburger. Sum across H.'

## Slide 30: Marginalization — sum over what you don't care about

Slide 2: 'And P(light). Check it sums to 1.'

## Slide 31: Marginalization — sum over what you don't care about

Slide 3: 'Named: marginalization. Sum rule. Same move as last week.'

## Slide 32: Conditional — restrict and renormalize

Slide 1: 'Observation arrives. Now ask the conditional question. This is the SAME move as last week\'s P(first=H | at least one H) = 2/3 on the coin-flip grid. Restrict and renormalize.'

## Slide 33: Conditional — restrict and renormalize

Slide 2: 'Two steps. Slice the joint to keep only rows consistent with the observation; renormalize.'

## Slide 34: Conditional — restrict and renormalize

Slide 3: 'Posterior. Observing heavy moved prior 0.70 to posterior 0.91 — strongly diagnostic. Much stronger than the cab problem (0.15 prior → 0.41 posterior). Why? The likelihoods here are more informative, and the prior was less extreme.'

## Slide 35: Summary — three operations on the joint

~1 min. Mental model to carry forward. Everything today (and Week 3) is operations on this table — just with infinitely many cells.

## Slide 36: Agenda

_(no speaker notes)_

## Slide 37: Expected value + discrete distributions

15 min. E[X] (4 slides), Bernoulli (3 slides), Binomial (4 slides + 1 real PMF image). Bernoulli IS the meal draw; Binomial IS a week.

## Slide 38: Expected value  E[X]

Slide 1: 'Expected value. Weighted average. The formula is what you\'d naïvely call an average — but weighted by probability instead of counted equally.'

## Slide 39: Expected value  E[X]

Slide 2: 'Encode meal as 1/0. Then E[meal] equals the probability. Key trick — we use it constantly in RL and in hypothesis testing.'

## Slide 40: Expected value  E[X]

Slide 3: 'Variance. Spread. For Bernoulli(p), it simplifies to p(1-p). Maxed at p=0.5; smaller at the extremes.'

## Slide 41: Expected value  E[X]

Slide 4: 'Mental model: mean = balance point, variance = width.'

## Slide 42: Bernoulli distribution

Slide 1: 'Bernoulli. One parameter.'

## Slide 43: Bernoulli distribution

Slide 2: 'The bento meal is Bernoulli(0.7). Every day, a weighted flip.'

## Slide 44: Bernoulli distribution

Slide 3: 'Flag: in Week 3 we shift gears and INFER p from observed counts. That\'s what conjugacy enables — we\'ll put a prior on p '(Beta distribution) and use Bayes to update.'

## Slide 45: Binomial distribution

Slide 1: 'Zoom out. A single bento is Bernoulli. A WEEK is Binomial. Y counts successes.'

## Slide 46: Binomial distribution

Slide 2: 'Binomial formula. Name each piece. Binomial coefficient C(n,k) = "n choose k" = count of orderings.'

## Slide 47: Binomial distribution

Slide 3: 'Plug in for k=3, 4, 5. The mode is k=4 — this surprises students who expect k=5 because p=0.7 > 0.5. The answer: 5 orderings for k=4 vs 1 ordering for k=5. The combinatorics wins over the extra factor of 0.7.'

## Slide 48: Binomial(5, 0.7) — full PMF

~1 min. Real bar chart. Let it sit — students can see the shape. Flag the Week-3 connection: when we don\'t KNOW p, this PMF with an unknown p becomes a function of p, and Beta conjugates nicely with it.

## Slide 49: Agenda

_(no speaker notes)_

## Slide 50: Continuous probability + the Gaussian

20 min. Build: PMF→PDF (4 text + 1 image), Gaussian formula (5 text + 1 image), continuous-Bayes worked (6 text + 1 image). The images are the payoff — do NOT speak over them; pause.

## Slide 51: From PMF to PDF — going continuous

Slide 1: 'Weight is continuous. No finite outcome space. We need a new object — the PDF.'

## Slide 52: From PMF to PDF — going continuous

Slide 2: 'Binning thought experiment. Bin the weights. Shrink bins. In the limit: a smooth curve. That curve is the density.'

## Slide 53: From PMF to PDF — going continuous

Slide 3: 'Density ≠ probability. This trips students up. Density is 'probability PER UNIT. You integrate to get a probability. Density values can be > 1 (density of N(0, 0.01) at 0 is ~40).'

## Slide 54: From PMF to PDF — going continuous

Slide 4: 'Corollary: probability of ANY exact value is 0 for a continuous RV. But probability of being near any value is f(x) × (small interval). Intuitive and mathematically honest.'

## Slide 55: Shrinking bins → PDF as the limit

Pause 10 seconds. Let them see the histograms smoothing into the PDF. The blue curve is the same Gaussian in all three panels — the histograms are approaching it from above and below.

## Slide 56: The Gaussian (normal) distribution

Slide 1: 'Real bentos vary. Not every tonkatsu is exactly 500g. The natural distribution for that variation is the Gaussian.'

## Slide 57: The Gaussian (normal) distribution

Slide 2: 'The formula. Don\'t try to hold the whole thing at once — we\'ll name each piece now.'

## Slide 58: The Gaussian (normal) distribution

Slide 3: 'Four pieces. Mean, variance, the exponential (which does the peaking), and the normalizer (which makes the area equal 1 — 'required of any PDF).'

## Slide 59: The Gaussian (normal) distribution

Slide 4: 'Shape. Symmetric around μ. SHARPER (smaller σ) → TALLER peak. The 68-95-99.7 rule — most mass within 1, 2, 3 sigma.'

## Slide 60: The Gaussian (normal) distribution

Slide 5: 'Two Gaussians for Chibany. They overlap in the 380-470 range. Next slide: picture.'

## Slide 61: The Gaussian — shape and the 68-95 rule

Pause. Let them trace the curve and see the shaded bands. The peak height formula 1/√(2πσ²) ≈ 0.013 for σ=30 — visible at the top.

## Slide 62: Chibany's two bento-weight likelihoods

Key setup image for the continuous-Bayes worked example that follows. 450g sits squarely in the tonkatsu Gaussian, far in the right tail of hamburger. The next slide computes the densities.

## Slide 63: Bayes with a continuous likelihood — worked

Slide 1: 'New observation: actual weight, 450g. Same Bayesian question.'

## Slide 64: Bayes with a continuous likelihood — worked

Slide 2: 'Prior unchanged — still 0.7/0.3 on meal.'

## Slide 65: Bayes with a continuous likelihood — worked

Slide 3: 'The work: compute each Gaussian density value. I\'m showing the arithmetic for f_T: the normalizer coefficient ≈ 0.0133, the exponent is −(−50)²/1800 = −1.389, exp of that is 0.249, product ≈ 0.00332. f_H comes out to 0.00044 — much smaller because 450 is far from 350.'

## Slide 66: Bayes with a continuous likelihood — worked

Slide 4: 'Multiply prior by likelihood. Sum for the evidence.'

## Slide 67: Bayes with a continuous likelihood — worked

Slide 5: 'Divide. Posterior is 0.95/0.05.'

## Slide 68: Bayes with a continuous likelihood — worked

Slide 6: 'Compare to Block 4 (heavy/light bucketing): 0.91. The continuous exact value moves belief further because it uses the precise weight, not just a bucket.'

## Slide 69: Break — 10 minutes

Hard 10. Block 7 is the highest-stakes block of the session. Come back sharp. Double-check the tonk_hamb.png loaded correctly on the projector.

## Slide 70: Agenda

_(no speaker notes)_

## Slide 71: Gaussian-Gaussian update — launching Week 3

25 min. THE block of the session. Now with: (a) explicit motivation for inferring μ, (b) a derivation SKETCH (complete the square), (c) a real posterior-curve picture, (d) precision visualized, (e) N-observation generalization given its own build-up.

## Slide 72: Why would Chibany want to infer μ ?

Slide 1: 'Up to now, the question has been about today\'s meal. A discrete hypothesis.'

## Slide 73: Why would Chibany want to infer μ ?

Slide 2: 'But we wrote 500g as if we KNEW it. We don\'t really. This term is an unknown PARAMETER. Call it μ.'

## Slide 74: Why would Chibany want to infer μ ?

Slide 3: 'So now Bayesian inference is shifting: H = μ, a continuous parameter, not a discrete category. Why not just average the weights? Because Chibany has prior knowledge from past experience, and early in the semester they have very few data points. Averaging is what a frequentist would do and it discards the prior. 'Bayes keeps both.'

## Slide 75: Step 1 — the prior  μ ~ N(μ₀, σ₀²)

Slide 1: 'Prior is a Gaussian over μ. Two hyperparameters: μ₀ and σ₀.'

## Slide 76: Step 1 — the prior  μ ~ N(μ₀, σ₀²)

Slide 2: 'Chibany\'s best guess 500, uncertainty 20. Prior = N(500, 400).'

## Slide 77: Step 1 — the prior  μ ~ N(μ₀, σ₀²)

Slide 3: 'THIS IS THE BIG MOVE. The density isn\'t over weights now. 'It\'s over the unknown parameter μ. Priors can live on parameters. In Week 4 we\'ll even put a prior on the PRIOR — hierarchical Bayes.'

## Slide 78: Step 2 — the likelihood

Slide 1: 'One observation. 510g. We pretend σ is known — only μ is unknown. Week 3 will relax this.'

## Slide 79: Step 2 — the likelihood

Slide 2: 'Likelihood is the Gaussian density evaluated at the 'observed weight, as a function of μ.'

## Slide 80: Step 2 — the likelihood

Slide 3: 'Here\'s the trick: when you treat the likelihood N(D|μ,σ²) as a function of μ for fixed D, it\'s STILL a Gaussian shape — peaked where μ=D. So we have two Gaussians in μ. Multiplying them is the Bayes step.'

## Slide 81: Why Gaussian × Gaussian = Gaussian  (derivation sketch)

Slide 1: 'Multiply the two Gaussian densities. Normalizers are constants in μ — we absorb them into the final normalization later.'

## Slide 82: Why Gaussian × Gaussian = Gaussian  (derivation sketch)

Slide 2: 'Expand the squared terms and combine. You get a quadratic in μ. Form: Aμ² − 2Bμ + constants.'

## Slide 83: Why Gaussian × Gaussian = Gaussian  (derivation sketch)

Slide 3: 'Complete the square — just like in high school algebra. A quadratic in μ inside an exp is the kernel of a Gaussian. So the posterior IS Gaussian. Not magic — algebra.'

## Slide 84: Why Gaussian × Gaussian = Gaussian  (derivation sketch)

Slide 4: 'The new μ and σ come from matching coefficients. A (coefficient of μ²) gives you 1/σ²_post. B/A (the minimum of the quadratic) gives you μ_post. Full derivation in T3 Ch 4 — read it.'

## Slide 85: Precision  =  1 / variance  =  "how sharp I am"

Pause. Two Gaussians, same mean, different widths. The sharp one is more precise — if you\'re that sharp, you\'re very sure, and in a Bayesian update your view gets more weight. Intuition for the precision-sum formula on the next slide.

## Slide 86: Plug in the numbers  —  posterior  =  prior × likelihood, rescaled

Slide 1: 'The formulas. Precisions add. Posterior mean is precision-weighted average.'

## Slide 87: Plug in the numbers  —  posterior  =  prior × likelihood, rescaled

Slide 2: 'The inputs.'

## Slide 88: Plug in the numbers  —  posterior  =  prior × likelihood, rescaled

Slide 3: 'Posterior variance. 1/400 + 1/900 combines on 3600. Gets you 13/3600, so σ²_post ≈ 277, σ_post ≈ 16.6. TIGHTER than either input. Combining information reduces uncertainty — that\'s the whole point of Bayesian updating.'

## Slide 89: Plug in the numbers  —  posterior  =  prior × likelihood, rescaled

Slide 4: 'Posterior mean ≈ 503.1. Moved from 500 toward 510 but mostly stayed near the prior. Because the prior was more precise (σ₀=20 vs data σ=30). The more precise source wins.'

## Slide 90: Prior × Likelihood = Posterior

THE payoff visual. Pause. Red prior, blue likelihood, yellow posterior. The posterior IS tighter than both inputs and lives between them — closer to the prior because the prior is tighter. This one picture replaces 20 minutes of algebra in students\' memory.

## Slide 91: N observations  —  precisions keep adding

Slide 1: 'Each independent observation adds precision 1/σ². Two observations = 2/σ² added. N observations = N/σ². This is the key property of conjugate updates.'

## Slide 92: N observations  —  precisions keep adding

Slide 2: 'The general formulas. Σ_i D_i is the sum of observed weights.'

## Slide 93: N observations  —  precisions keep adding

Slide 3: 'Asymptotic behavior: as N grows, the prior term becomes negligible and the posterior mean approaches the sample mean. You recover the frequentist answer in the limit of much data — but with a Bayesian path there, and a well-calibrated posterior variance 'along the way. This formula IS the skeleton of Week 3\'s conjugate updates and Week 4\'s hierarchical models.'

## Slide 94: Closing the arc — same Bayes, new objects

Slide 1: 'Zoom out. Three flavors of Bayes today. Same rule, progressively more general objects.'

## Slide 95: Closing the arc — same Bayes, new objects

Slide 2: 'Named: conjugacy. Today was Gaussian-Gaussian. Week 3 we do it on the discrete side (Beta-Binomial, Dirichlet-Multinomial). Beta × Binomial gives Beta — try to see what\'s on your tongue re Bayesian inference on a coin\'s p.'

## Slide 96: Agenda

_(no speaker notes)_

## Slide 97: Paper presentations — rubric + signup

10 min tight.

## Slide 98: Presentations — why and what

~2 min.

## Slide 99: Rubric — 5 points

~2 min. Email the PDF.

## Slide 100: Signup — Weeks 4 through 12

~6 min. Signups on the board. Photograph; transcribe into readings_map.yml.

## Slide 101: Agenda

_(no speaker notes)_

## Slide 102: Admin + Week 3 homework

10 min.

## Slide 103: Syllabus — three things changed

~3 min.

## Slide 104: Week 3 — readings + homework

~4 min. T3 Ch 1 is added so Chibany\'s backstory is reinforced; T3 Ch 4 derives what we sketched in Block 7.

## Slide 105: Preview — the arc from here

~3 min. Close warm.
