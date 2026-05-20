# Human and Machine Learning SP26 — Assignments

All four programming assignments can be completed in **GenJAX** (the canonical stencil, run on Google Colab), or in **vanilla Python**, **R**, or **Matlab**. The GenJAX, Python, and R stencils are provided for each assignment; for the Matlab stencil, email the instructor.

You have **3 free late days** that can be used across the programming assignments. See the [syllabus](syllabus.html) for the full late policy.

## Schedule

| Assignment | Assigned | Due | Weight | Topic |
|---|---|---|---|---|
| [Clusters](#clusters) | Week 3 (May 15) | **Fri Jun 5, 8 PM** | 7.5% | Mixture models & categorization |
| Generalization | Week 4 (May 22) | *TBA when released* | 7.5% | Bayesian generalization |
| Monte Carlo | Week 7 (Jun 12) | *TBA when released* | 10.5% | Monte Carlo methods |
| Reinforcement Learning | Week 8 (Jun 19) | *TBA when released* | 4.5% | MDPs & reinforcement learning |

Total assignments: **30%** of the course grade. The final-project proposal (pass/fail, tracked in the syllabus) is due **Sun Jun 28, 5 PM** — one week after the Generalization assignment.

## Assignment details

### Clusters (7.5%) {#clusters}

**Due: Fri Jun 5, 2026 at 8:00 PM.**

Investigate categorization and prediction in a 2-component Gaussian mixture model. Problem 1 is the Gaussian-Gaussian conjugate update; Problem 2 derives the posterior and marginal distributions for a mixture using Bayes' rule and the Law of Total Probability.

**Start here — the assignment:**

- **[Assignment PDF — clusters.pdf](assignments/clusters/clusters.pdf)** — the problem statements and all the math. Read this first.

**Then pick one stencil to work in.** All three cover the same problems with the same scaffolding — choose whichever language you prefer:

| Stencil | File | Notes |
|---|---|---|
| **GenJAX (canonical)** | [clusters.ipynb](assignments/clusters/clusters.ipynb) | Recommended if you've done the Tutorial 2 GenJAX readings. Includes a bonus Part 2(e). |
| **Python (no GenJAX)** | [clusters_python.ipynb](assignments/clusters/clusters_python.ipynb) | numpy + scipy + matplotlib. Each cell has an optional paired "Now in GenJAX" tutorial cell. |
| **R** | [clusters_nosoln.Rmd](assignments/clusters/clusters_nosoln.Rmd) | base R + ggplot2. |
| **Matlab** | available on request | Email Prof. Austerweil. |

**Other details:**

- **Prep reading:** [Textbook — Mixture Models (T3 Ch 5)](https://josephausterweil.github.io/probintro/intro2/05_mixture_models/)
- **GenJAX background:** [Tutorial 2, Chapters 0–4](https://josephausterweil.github.io/probintro/genjax/)
- **Submit** (by DM or email to the instructor) **one** of the following:
    - your completed notebook (or knitted `.Rmd`) — it must run end-to-end and contain your figures, inline text answers, derivations, and descriptions; **or**
    - a single PDF report containing your code, figures, text answers, derivations, and descriptions.

### Generalization (7.5%) {#generalization}

*Details will be posted when the assignment is released.*

### Monte Carlo (10.5%) {#monte-carlo}

*Details will be posted when the assignment is released.*

### Reinforcement Learning (4.5%) {#reinforcement-learning}

*Details will be posted when the assignment is released.*
