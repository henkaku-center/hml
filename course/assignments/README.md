# Human and Machine Learning SP26 — Assignments

All four programming assignments can be completed in **GenJAX** (the canonical stencil, run on Google Colab), or in **vanilla Python**, **R**, or **Matlab**. The GenJAX, Python, and R stencils are provided for each assignment; for the Matlab stencil, email the instructor.

You have **3 free late days** that can be used across the programming assignments. See the [syllabus](syllabus.html) for the full late policy.

## Schedule

| Assignment | Assigned | Due | Weight | Topic |
|---|---|---|---|---|
| [Clusters](#clusters) | Week 3 (May 15) | **Fri Jun 5, 8:00 PM** | 7.5% | Mixture models & categorization |
| [Generalization](#generalization) | Week 4 (May 22) | **Fri Jun 19, 8:00 PM** | 7.5% | Bayesian generalization |
| [Monte Carlo](#monte-carlo) | Week 7 (Jun 12) | **Fri Jul 10, 8:00 PM** | 10.5% | Monte Carlo, importance sampling, MCMC |
| [Reinforcement Learning](#reinforcement-learning) | Week 8 (Jun 19) | **Fri Jul 10, 8:00 PM** | 4.5% | Q-learning, reward hacking, reward shaping |

Total assignments: **30%** of the course grade. The final-project proposal (pass/fail, tracked in the syllabus) is due **Sun Jun 28, 8:00 PM** — one week after the Generalization assignment. See the [project guidelines](project.html) for full details.

## Assignment details

### Clusters (7.5%) {#clusters}

**Due: Fri Jun 5, 2026 at 8:00 PM.**

Investigate categorization and prediction in a 2-component Gaussian mixture model. Problem 1 is the Gaussian-Gaussian conjugate update; Problem 2 derives the posterior and marginal distributions for a mixture using Bayes' rule and the Law of Total Probability.

**Start here — the assignment:**

- **[Assignment PDF — clusters.pdf](assignments/clusters/clusters.pdf)** — the problem statements and all the math. Read this first.

**Then pick one stencil to work in.** All three cover the same problems with the same scaffolding — choose whichever language you prefer:

| Stencil | Open in Colab | Download | Notes |
|---|---|---|---|
| **GenJAX (canonical)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/clusters/clusters.ipynb) | [clusters.ipynb](assignments/clusters/clusters.ipynb) | Recommended if you've done the Tutorial 2 GenJAX readings. Includes a bonus Part 2(e). |
| **Python (no GenJAX)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/clusters/clusters_python.ipynb) | [clusters_python.ipynb](assignments/clusters/clusters_python.ipynb) | numpy + scipy + matplotlib. Each cell has an optional paired "Now in GenJAX" tutorial cell. |
| **R** | — (knit locally in RStudio) | [clusters_nosoln.Rmd](assignments/clusters/clusters_nosoln.Rmd) | base R + ggplot2. Colab does not run `.Rmd` files. |
| **Matlab** | — | available on request | Email Prof. Austerweil. |

**Other details:**

- **Prep reading:** [Textbook — Mixture Models (T3 Ch 5)](https://josephausterweil.github.io/probintro/intro2/05_mixture_models/)
- **GenJAX background:** [Tutorial 2, Chapters 0–4](https://josephausterweil.github.io/probintro/genjax/)
- **Submit** (by DM or email to the instructor) **one** of the following:
    - your completed notebook (or knitted `.Rmd`) — it must run end-to-end and contain your figures, inline text answers, derivations, and descriptions; **or**
    - a single PDF report containing your code, figures, text answers, derivations, and descriptions.

### Generalization (7.5%) {#generalization}

**Due: Fri Jun 19, 2026 at 8:00 PM.**

Build your own Bayesian generalization model for six animals (Cow, Dolphin, Chicken, Seal, Penguin, Bat). You design the hypothesis space, define a prior, then compute posteriors and predictive distributions under both weak and strong sampling. The final problem expands to all $2^6 - 1 = 63$ hypotheses to illustrate the No Free Lunch theorem. **There is no single correct hypothesis space** — the assignment is about how the framework behaves under your choice of $\mathcal{H}$.

**Start here — the assignment:**

- **[Assignment PDF — generalization.pdf](assignments/generalization/generalization.pdf)** — the problem statements and all the math. Read this first.

**Then pick one stencil to work in.** All three cover the same five problems with the same scaffolding:

| Stencil | Open in Colab | Download | Notes |
|---|---|---|---|
| **GenJAX (canonical)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/generalization/generalization.ipynb) | [generalization.ipynb](assignments/generalization/generalization.ipynb) | Hypothesis space as `jnp.array`, posterior by enumeration, `@gen` model with `categorical` over the hypothesis index. |
| **Python (no GenJAX)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/generalization/generalization_python.ipynb) | [generalization_python.ipynb](assignments/generalization/generalization_python.ipynb) | numpy + matplotlib. Each cell has an optional paired "Now in GenJAX" tutorial cell. |
| **R** | — (knit locally in RStudio) | [generalization_nosoln.Rmd](assignments/generalization/generalization_nosoln.Rmd) | base R + ggplot2. Colab does not run `.Rmd` files. |
| **Matlab** | — | available on request | Email Prof. Austerweil. |

**Other details:**

- **Prep reading:** A textbook chapter on Bayesian generalization is forthcoming in Tutorial 3 of the [Probability Tutorial](https://josephausterweil.github.io/probintro/); until then, the Week 4 lecture slides are the canonical reference.
- **Lecture:** Week 4 covers the Bayesian generalization framework, size principle, and No Free Lunch.
- **Submit** (by DM or email to the instructor) **one** of the following:
    - your completed notebook (or knitted `.Rmd`) — it must run end-to-end and contain your figures, inline text answers, and descriptions; **or**
    - a single PDF report containing your code, figures, text answers, and descriptions.

### Monte Carlo (10.5%) {#monte-carlo}

**Due: Fri Jul 10, 2026 at 8:00 PM.**

Explore three Monte Carlo methods. **Problem 1:** compare naive Monte Carlo with importance sampling for a tail probability $P(Y>2)$, $Y\sim N(0,1)$. **Problem 2:** build a Markov chain Monte Carlo sampler — interleaving **Gibbs** (for the per-bag proportions) and **Metropolis–Hastings** (for the hyperparameters) — for the hierarchical Beta-Binomial model of Kemp, Perfors & Tenenbaum (2007), parameterized by mean $\varphi$ and concentration $\kappa$. **Problem 3:** quantify sampler efficiency with the effective sample size, and work through why a weight-based ESS measures proposal quality rather than estimator accuracy.

**Start here — the assignment:**

- **[Assignment PDF — mc_approx.pdf](assignments/mc/mc_approx.pdf)** — the problem statements and all the math. Read this first.

**Then pick one stencil to work in.** All three cover the same three problems with the same scaffolding:

| Stencil | Open in Colab | Download | Notes |
|---|---|---|---|
| **GenJAX (canonical)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/mc/mc_approx.ipynb) | [mc_approx.ipynb](assignments/mc/mc_approx.ipynb) | GenJAX distribution primitives (`beta.sample`, `beta.logpdf`, `normal.logpdf`) inside a hand-assembled Gibbs+MH loop, with `jax.vmap`/`jax.lax.scan` for speed. |
| **Python (no GenJAX)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/mc/mc_approx_python.ipynb) | [mc_approx_python.ipynb](assignments/mc/mc_approx_python.ipynb) | numpy + scipy + matplotlib. Each problem has a short "Now in GenJAX" translation note. |
| **R** | — (knit locally in RStudio) | [mcmc_approx.Rmd](assignments/mc/mcmc_approx.Rmd) | base R + ggplot2. Colab does not run `.Rmd` files. |
| **Matlab** | — | available on request | Email Prof. Austerweil. |

**Other details:**

- **Prep reading:** [Textbook — Tutorial 3 Ch 12 (Hierarchical Bayes / approximate inference)](https://josephausterweil.github.io/probintro/intro2/12_hierarchical_bayes/) (carried from the Week 4 hand-off).
- **Lecture:** Week 7 covers Monte Carlo, importance sampling, particle filtering, and MCMC (Metropolis–Hastings + Gibbs), and walks through the Kemp-model sampler this assignment asks you to implement.
- **Submit** (by DM or email to the instructor) **one** of the following:
    - your completed notebook (or knitted `.Rmd`) — it must run end-to-end and contain your figures, inline text answers, and descriptions; **or**
    - a single PDF report containing your code, figures, text answers, and descriptions.

### Reinforcement Learning (4.5%) {#reinforcement-learning}

**Due: Fri Jul 10, 2026 at 8:00 PM.**

Implement **Q-learning** on the *GardenPath* gridworld, then use it to see how the *reward you write* can diverge from the *goal you intend*. **Problem 1:** fill in the one-line temporal-difference update and confirm it solves the task under reward-maximizing (outcome) feedback. **Problem 2:** diagnose a *reward-hacking* failure — under human-style action feedback the learned policy loops forever in a **+14/lap** positive cycle and never reaches the goal. **Problem 3:** design your own potential function $\Phi(s)$ and add **potential-based shaping** to give dense feedback the principled way; verify it reaches the goal **and** provably does not change the optimal policy (invariance). **Bonus:** confirm your model-free learner found the same route a model-based value-iteration planner computes exactly.

**Start here — the assignment:**

- **[Assignment PDF — rl.pdf](assignments/rl/rl.pdf)** — the problem statements. Read this first.

**Then pick one stencil to work in.** All three cover the same problems with the same scaffolding (a shared `rl_gridworld.py` provides the world, the reward schemes, the figure renderer, and an in-notebook interactive explorer — keep it next to your notebook; the Colab stencils fetch it automatically).

| Stencil | Open in Colab | Download | Notes |
|---|---|---|---|
| **GenJAX (canonical)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/rl/rl_genjax.ipynb) | [rl_genjax.ipynb](assignments/rl/rl_genjax.ipynb) | The environment is a GenJAX `@gen` generative model; Q-learning learns by *sampling* it. Bonus value iteration reads the same model. |
| **Python (no GenJAX)** | [Open in Colab](https://colab.research.google.com/github/henkaku-center/hml/blob/main/course/assignments/rl/rl_python.ipynb) | [rl_python.ipynb](assignments/rl/rl_python.ipynb) | numpy + matplotlib. Same problems, no JAX. |
| **R** | — (knit locally in RStudio) | [rl_nosoln.Rmd](assignments/rl/rl_nosoln.Rmd) | base R + ggplot2, self-contained. Colab does not run `.Rmd` files. |
| **Matlab** | — | available on request | Email Prof. Austerweil. |

**Other details:**

- **Prep reading:** Textbook Tutorial 3 — [Ch 21 (Markov Decision Processes)](https://josephausterweil.github.io/probintro/intro2/21_markov_decision_processes/) and [Ch 22 (Q-Learning)](https://josephausterweil.github.io/probintro/intro2/22_q_learning/), including the live Q-learning widget (the same GardenPath world).
- **Lecture:** Week 8 covers decision theory, MDPs + value iteration, Q-learning, reward shaping, and simulation-based RL.
- **Submit** (by DM or email to the instructor) **one** of the following:
    - your completed notebook (or knitted `.Rmd`) — it must run end-to-end and contain your figures, inline text answers, and descriptions; **or**
    - a single PDF report containing your code, figures, text answers, and descriptions.
