"""Build the GenJAX and Python (no-GenJAX) Jupyter stencils for the
Bayesian Generalization assignment.

Run from this directory:
    python3 _build_stencils.py

Writes:
    generalization.ipynb           (GenJAX canonical)
    generalization_python.ipynb    (Python, with paired "Now in GenJAX" cells)
"""

import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell


# ---------------------------------------------------------------------------
# Shared assignment prose
# ---------------------------------------------------------------------------

ANIMALS_TUPLE = '("cow", "dolphin", "chicken", "seal", "penguin", "bat")'

INTRO_MD = r"""# Assignment 2: Bayesian Generalization

__STENCIL_LABEL__

For this assignment, you will build a **Bayesian generalization model** for six animals: Cow, Dolphin, Chicken, Seal, Penguin, and Bat. There is no single "right" hypothesis space — *you* design it from properties shared by these animals.

**The setup.** Given that you observe one or more animals have some novel property, how likely is it that the other animals also have it? The Bayesian generalization framework solves this in three steps:

1. **Hypothesis space.** A set $\mathcal{H}$ of hypothesized properties. Each hypothesis $h$ is a binary vector of length 6 (1 if the animal has the property, 0 if not).
2. **Posterior over hypotheses.** After observing animal(s) ${\bf x}$ have the property,
   $$P(h \mid {\bf x}) = \frac{P(h)\,\prod_n P(x_n \mid h)}{\sum_{h' \in \mathcal{H}} P(h')\,\prod_n P(x_n \mid h')}.$$
3. **Predictive distribution over animals.** For each unobserved animal $y$,
   $$P(y \text{ has property} \mid {\bf x}) = \sum_{h:\, y \in h} P(h \mid {\bf x}).$$

We compare two likelihoods:
- **Weak sampling:** $P(x \mid h) = 1$ if $x \in h$, else $0$.
- **Strong sampling:** $P(x \mid h) = 1/|h|$ if $x \in h$, else $0$ (where $|h|$ is the number of animals in $h$).

**Corresponding textbook chapter:** [Tutorial 3 Ch 6 — Generalization](https://josephausterweil.github.io/probintro/intro2/06_generalization/) (and revisit T1 Ch 5 on Bayesian inference).
"""

PROBLEM_1_MD = r"""---

## Problem 1: Define your hypothesis space

Write down your hypotheses. Each hypothesis is a binary vector of length 6 (one entry per animal in the order Cow, Dolphin, Chicken, Seal, Penguin, Bat). Give each hypothesis a 1–4 word label (e.g. "has wings", "lives in water").

**Constraints:**
- Include a **catch-all** hypothesis containing all six animals.
- Use **more than 4** and **fewer than 63** hypotheses.
- Each entry is 0 or 1 — no animal is "partially" in a hypothesis.

There is no single correct hypothesis space. Pick properties you think are meaningful for these animals.
"""

PROBLEM_2_MD = r"""---

## Problem 2: Prior

Define a prior $P(h)$ over your hypotheses. A uniform prior (every hypothesis equally likely) is fine. Write 1–2 sentences justifying your choice.
"""

PROBLEM_3_INTRO_MD = r"""---

## Problem 3: Posterior

Compute the posterior $P(h \mid {\bf x})$ under both **weak** and **strong** sampling. Write the weak/strong likelihood functions, multiply by the prior, normalize.
"""

PROBLEM_3A_MD = r"""### 3(a): One observation

Pick one animal and compute the posterior under weak and strong sampling. Plot both as a bar chart over your hypothesis labels.

**Write 1–2 sentences:** how does the posterior change after observing one animal? Are there differences between weak and strong sampling? If so, what are they (and why)?
"""

PROBLEM_3B_MD = r"""### 3(b): Three observations

Add two more animals (so three animals total) and recompute the posterior under both samplings. Plot.

**Write 1–2 sentences:** how has the posterior changed compared to (a)? How does that differ between weak and strong sampling?
"""

PROBLEM_4_MD = r"""---

## Problem 4: Predictive distribution

For each of the six animals $y$, compute
$$P(y \text{ has property} \mid {\bf x}) = \sum_{h:\, y \in h} P(h \mid {\bf x}).$$

Make **four** histograms (1-obs weak, 1-obs strong, 3-obs weak, 3-obs strong) — one bar per animal, height = predictive probability. Label axes and title each plot.

**Write a paragraph** describing the results: which animals are predicted to share the property? How does this differ between weak and strong, and between 1 vs. 3 observations? Tie the patterns back to the hypotheses that survived in the posterior.
"""

PROBLEM_5_INTRO_MD = r"""---

## Problem 5: Break your model

Now expand the hypothesis space to **all** $2^6 - 1 = 63$ non-empty binary vectors of length 6 (i.e. every possible subset of the six animals except the empty set). Use a uniform prior over this expanded space. Recompute the posterior and predictive distributions from Problems 3 and 4.
"""

PROBLEM_5_PROMPT_MD = r"""**Write a few sentences:** what happened to the posterior and predictive probabilities? Why? **Relate this to a theorem we covered in class.** (Hint: think about what a uniform prior over *all possible* hypotheses encodes about your beliefs — and what it does *not* encode.)

You do not need to dump all 63 hypotheses' probabilities in your report — just enough to make your point.
"""

SUBMISSION_MD = r"""---

## Submission

Submit by DM or email to the instructor **one** of:

- your completed notebook — it must run end-to-end with no errors and contain your figures, inline text answers, and descriptions; **or**
- a single PDF report containing your code, figures, text answers, and descriptions.
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def md(text):
    return new_markdown_cell(text)

def code(src):
    return new_code_cell(src)


# ---------------------------------------------------------------------------
# GenJAX canonical stencil
# ---------------------------------------------------------------------------

def build_genjax_notebook():
    cells = []

    cells.append(md(INTRO_MD.replace(
        "__STENCIL_LABEL__",
        "This is the **GenJAX (canonical)** stencil. Two paired stencils are available — `generalization_python.ipynb` (Python + numpy) and `generalization_nosoln.Rmd` (R + ggplot2). Matlab available on request.",
    )))

    cells.append(md(r"""## Setup

Run the install cell if you are in Google Colab (uncomment the `!pip` line). Then run the imports.

**Dtype note.** GenJAX distributions produce `float32`. Any Python/numpy scalar passed into a `@gen` model or a `ChoiceMap` must be cast with `jnp.float32(...)` (or `jnp.int32(...)` for discrete latents) — mixing in numpy `float64` raises a `TypeError` inside the sampler.
"""))

    cells.append(code(r"""# Run on first launch in Colab:
# !pip install genjax
"""))

    cells.append(code(
        "import jax\n"
        "import jax.numpy as jnp\n"
        "import jax.random as random\n"
        "from genjax import gen, categorical\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "plt.style.use('seaborn-v0_8-whitegrid')\n"
        "%matplotlib inline\n"
        "\n"
        "np.random.seed(42)\n"
        "key = random.PRNGKey(42)\n"
        "\n"
        f"ANIMALS = {ANIMALS_TUPLE}\n"
        "N_ANIMALS = len(ANIMALS)\n"
        "print(f\"Animals (in fixed order): {ANIMALS}\")\n"
    ))

    # Problem 1 — hypothesis space
    cells.append(md(PROBLEM_1_MD))

    cells.append(md(r"""### Building $\mathcal{H}$ as a matrix

Represent the hypothesis space as a 2-D `jnp.array` of shape `(H, 6)` where `H` is the number of hypotheses and each row is a hypothesis vector. Keep a parallel list of 1–4 word labels in the **same order** as the rows.

**Fill me.** Define `hypothesis_labels` and `hypothesis_matrix` below. Below the cell, briefly describe the properties you chose."""))

    cells.append(code(r"""# fill me
#
# Suggested approach:
#   1. List your hypothesis labels (strings, 1-4 words each).
#   2. For each label, write a length-6 binary vector — in the SAME order as
#      ANIMALS = ("cow", "dolphin", "chicken", "seal", "penguin", "bat").
#   3. Stack them into a single matrix.
#   4. Don't forget the catch-all (all ones).
#   5. Keep `H > 4` and `H < 63`.
#
# Example shape (replace with your own):
#   hypothesis_labels = ["catch-all (any animal)", "lives in water", ...]
#   hypothesis_matrix = jnp.array([
#       [1, 1, 1, 1, 1, 1],   # catch-all
#       [0, 1, 0, 1, 1, 0],   # lives in water
#       ...
#   ], dtype=jnp.float32)

hypothesis_labels = [
    # your labels here
]

hypothesis_matrix = jnp.array(
    [
        # your binary rows here
    ],
    dtype=jnp.float32,
)

H = hypothesis_matrix.shape[0]
assert hypothesis_matrix.shape == (H, N_ANIMALS), f"expected (H, {N_ANIMALS}), got {hypothesis_matrix.shape}"
assert len(hypothesis_labels) == H, "labels and matrix rows must align"
assert 4 < H < 63, "use more than 4 and fewer than 63 hypotheses"
assert jnp.all((hypothesis_matrix.sum(axis=1) > 0)), "no empty hypotheses"
assert jnp.any(jnp.all(hypothesis_matrix == 1, axis=1)), "include a catch-all hypothesis"
print(f"H = {H} hypotheses, sizes = {hypothesis_matrix.sum(axis=1).astype(int).tolist()}")
"""))

    cells.append(md("*(Describe your hypotheses here in 1–2 sentences — what kinds of properties did you include?)*"))

    # Problem 2 — prior
    cells.append(md(PROBLEM_2_MD))

    cells.append(code(r"""# fill me
#
# Suggested approach:
#   1. A uniform prior is `jnp.full((H,), 1.0 / H)`.
#   2. If you prefer a non-uniform prior, build any positive vector of length H and normalize.
#   3. Make sure `prior` sums to 1.

prior = None   # replace with a length-H jnp array that sums to 1
assert prior is not None and prior.shape == (H,), "prior must have shape (H,)"
assert jnp.isclose(prior.sum(), 1.0), "prior must sum to 1"
"""))

    cells.append(md("*(1–2 sentences justifying your prior.)*"))

    # Problem 3 — posterior
    cells.append(md(PROBLEM_3_INTRO_MD))

    cells.append(md(r"""### The generative model as a `@gen` function

The Bayesian-generalization model is **discrete in `h`**: there are finitely many hypotheses, so we can enumerate them. We will:

1. Write the generative process as a `@gen` function — `h_idx` sampled from `categorical(log_prior)`, then each observed animal $x$ generated according to the chosen sampling rule given `h`.
2. Compute the posterior over `h_idx` by **enumeration** — evaluate the unnormalized posterior at every hypothesis and normalize. This is exact (no sampling needed) because the latent is discrete with a small support.

**`categorical(logits)` in GenJAX takes log-probabilities** (logits), so use `jnp.log(prior)`. It returns an integer index in `[0, H)`.

**`@gen` cheatsheet (Tutorial 2 Ch 2–4).**
- `x = dist(args) @ "name"` — sample from a distribution, address the choice as `"name"`.
- `model.simulate(key, args)` — run the model once forward, get a trace.
- `model.assess(choices, args)` — return `(log_density, retval)` for an entire trace of choices. We use this for enumeration.

**Fill me** — write the model and the per-hypothesis log-likelihood. The model itself is short; the enumeration logic does the real work below."""))

    cells.append(code(r'''# fill me — log-likelihood of observations under hypothesis h
#
# Given:
#   h:        length-N_ANIMALS binary vector
#   x_idxs:   indices (into ANIMALS) of the observed animals
#   sampling: "weak" or "strong"
#
# Suggested approach (weak):
#   - log P(x | h) = 0  if h[x] == 1  else -inf  (i.e. likelihood 1 or 0)
#   - For multiple x's, sum the per-x log-likelihoods.
#
# Suggested approach (strong):
#   - log P(x | h) = -log |h|  if h[x] == 1  else -inf
#   - For multiple x's, sum (since data are iid given h).
#
# Use jnp.where + jnp.log and -jnp.inf (or a large negative number like -1e9) to
# represent the impossible outcomes.

def log_likelihood(h, x_idxs, sampling):
    """Return log P(x_idxs | h) under weak or strong sampling.

    Args:
        h:        jnp.array shape (N_ANIMALS,) of 0/1 (float ok)
        x_idxs:   jnp.array of integer indices into ANIMALS, shape (n_obs,)
        sampling: "weak" or "strong"
    """
    # fill me
    pass
'''))

    cells.append(code(r'''# fill me — vectorized posterior over hypotheses by enumeration
#
# Suggested approach:
#   1. For each row h_i in hypothesis_matrix, compute
#         log_post_unnorm[i] = log(prior[i]) + log_likelihood(h_i, x_idxs, sampling)
#   2. Stabilize with log-sum-exp:
#         m = log_post_unnorm.max()
#         post = jnp.exp(log_post_unnorm - m)
#         post = post / post.sum()
#   3. Vectorize the per-row computation with jax.vmap.

def posterior(x_idxs, sampling, hyp_matrix=hypothesis_matrix, prior_=prior):
    """Return posterior P(h | x_idxs) as a length-H jnp.array that sums to 1."""
    # fill me
    pass


# Now also wrap the same model as a @gen function so you can simulate from it.
# This is short — the heavy lifting was the enumeration above.

@gen
def generalization_model(log_prior, hyp_matrix, x_idxs_placeholder, sampling):
    """A generative model for a single observation x_1, given hypothesis space."""
    # fill me
    #
    # Suggested approach:
    #   1. Sample h_idx = categorical(log_prior) @ "h_idx".
    #   2. Pick h = hyp_matrix[h_idx].
    #   3. (Optional) sample the observed animal x_1 from the appropriate
    #      distribution under weak/strong. For weak: any animal in h equiprobable.
    #      For strong: same — uniform over animals in h. (Weak vs. strong differ
    #      only in the LIKELIHOOD, not in forward sampling — both sample uniformly
    #      from h. The difference shows up when you condition on x_1.)
    #   4. Return h_idx.
    pass
'''))

    cells.append(md(PROBLEM_3A_MD))

    cells.append(code(r"""# fill me
#
# 1. Pick ONE observed animal (an index into ANIMALS, say 2 for "chicken").
# 2. Call posterior(...) for both samplings.
# 3. Bar-plot both, side by side, with hypothesis_labels on the x-axis.

one_obs_idx = jnp.array([2])   # e.g. chicken; pick any animal you want

post_weak_1 = None             # replace with posterior(one_obs_idx, "weak")
post_strong_1 = None           # replace with posterior(one_obs_idx, "strong")

# Plot:
# fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
# x = np.arange(H)
# axes[0].bar(x, np.array(post_weak_1));   axes[0].set_xticks(x); axes[0].set_xticklabels(hypothesis_labels, rotation=45, ha='right'); axes[0].set_title(...)
# axes[1].bar(x, np.array(post_strong_1)); axes[1].set_xticks(x); axes[1].set_xticklabels(hypothesis_labels, rotation=45, ha='right'); axes[1].set_title(...)
# plt.tight_layout(); plt.show()

# your plotting code here
"""))

    cells.append(md("**Your answer (3a).** *(1–2 sentences. How did the posterior change? Differences between weak and strong sampling, and why?)*"))

    cells.append(md(PROBLEM_3B_MD))

    cells.append(code(r"""# fill me
#
# 1. Pick three observed animals (3 distinct indices).
# 2. posterior(three_obs_idxs, "weak") / posterior(three_obs_idxs, "strong").
# 3. Plot — same style as 3(a).

three_obs_idxs = jnp.array([2, 5, 4])   # e.g. chicken, bat, penguin

post_weak_3 = None
post_strong_3 = None

# your plotting code here
"""))

    cells.append(md("**Your answer (3b).** *(1–2 sentences. Compared to 3(a) — what changed? Weak vs. strong?)*"))

    # Problem 4 — predictive
    cells.append(md(PROBLEM_4_MD))

    cells.append(code(r'''# fill me — predictive distribution over animals
#
# Suggested approach:
#   For each animal y in 0..N_ANIMALS-1:
#     P(y has property | x) = sum over h such that h[y] == 1 of posterior[h]
#   This is the matrix product:  posterior @ hypothesis_matrix   (shape (H,) @ (H, N_ANIMALS) -> (N_ANIMALS,))

def predictive(post, hyp_matrix=hypothesis_matrix):
    """Return length-N_ANIMALS vector of P(y has property | observations)."""
    # fill me
    pass


# Then build the four histograms:
#   pred_weak_1   = predictive(post_weak_1)
#   pred_strong_1 = predictive(post_strong_1)
#   pred_weak_3   = predictive(post_weak_3)
#   pred_strong_3 = predictive(post_strong_3)
#
# A 2x2 grid of bar plots (rows = #observations, cols = sampling) reads well.

# your code + plotting here
'''))

    cells.append(md("**Your answer (Problem 4).** *(A paragraph. Which animals get high predictive probability, under each condition? Tie back to which hypotheses survived in the posterior. How does weak vs. strong differ?)*"))

    # Problem 5 — break the model
    cells.append(md(PROBLEM_5_INTRO_MD))

    cells.append(code(r"""# fill me — enumerate all 63 non-empty subsets of 6 animals
#
# Suggested approach:
#   1. There are 2^6 = 64 binary vectors of length 6. Drop the all-zeros one.
#   2. itertools.product([0, 1], repeat=6) generates all 64.
#   3. Stack into a jnp.array, drop the zero row, dtype=float32.
#   4. Uniform prior over all 63.
#   5. Reuse posterior() and predictive() — they only need a hypothesis matrix and prior.

import itertools

all_hyp_matrix = None     # shape (63, 6)
all_prior = None          # shape (63,) uniform

# your code here
"""))

    cells.append(code(r"""# fill me — repeat 3(a) / 3(b) / Problem 4 with the expanded hypothesis space.
#
# You don't need ALL 63 individual posterior values in your write-up — pick the
# slices that make your point (e.g. the predictive bars; the most-likely 5
# hypotheses; the entropy of the predictive).

# Example calls (you'll need to thread the new (hyp_matrix, prior_) through your posterior/predictive):
#   post_weak_1_big   = posterior(one_obs_idx,    "weak",   hyp_matrix=all_hyp_matrix, prior_=all_prior)
#   post_strong_1_big = posterior(one_obs_idx,    "strong", hyp_matrix=all_hyp_matrix, prior_=all_prior)
#   pred_weak_1_big   = predictive(post_weak_1_big, hyp_matrix=all_hyp_matrix)
#   ... etc for the 3-obs case.

# your code + plotting here
"""))

    cells.append(md(PROBLEM_5_PROMPT_MD))
    cells.append(md("**Your answer (Problem 5).** *(A few sentences — what happened to the posterior and predictive? Why? Which theorem from class does this illustrate?)*"))

    # Submission
    cells.append(md(SUBMISSION_MD))

    nb = new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11",
        },
    }
    return nb


# ---------------------------------------------------------------------------
# Python (no-GenJAX) stencil — with paired "Now in GenJAX" cells
# ---------------------------------------------------------------------------

def build_python_notebook():
    cells = []

    cells.append(md(INTRO_MD.replace(
        "__STENCIL_LABEL__",
        (
            "This is the **Python (no-GenJAX)** stencil. The primary path uses `numpy` + `matplotlib`. "
            "Optionally, each numpy code cell is followed by a paired *Now in GenJAX* cell that walks "
            "through the same task with GenJAX (with enough inline explanation that you can complete "
            "them without prior GenJAX experience). The paired cells are not required.\n\n"
            "If you would prefer the GenJAX-first stencil, see `generalization.ipynb` in this directory."
        ),
    )))

    cells.append(md(r"""## Setup

The GenJAX install only matters if you plan to do the optional GenJAX cells. The numpy path works without it.
"""))

    cells.append(code(r"""# Optional: only needed for the "Now in GenJAX" cells.
# In Google Colab, uncomment on first run:
# !pip install genjax
"""))

    cells.append(code(
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import itertools\n"
        "\n"
        "plt.style.use('seaborn-v0_8-whitegrid')\n"
        "%matplotlib inline\n"
        "\n"
        "np.random.seed(42)\n"
        "\n"
        f"ANIMALS = {ANIMALS_TUPLE}\n"
        "N_ANIMALS = len(ANIMALS)\n"
        "print(f\"Animals (in fixed order): {ANIMALS}\")\n" + r"""

# GenJAX imports — only used by the paired "Now in GenJAX" cells.
# If you skip those, an ImportError here is fine.
# DTYPE note: GenJAX distributions are float32; cast model args with jnp.float32(...) / jnp.int32(...).
try:
    import jax
    import jax.numpy as jnp
    import jax.random as random
    from genjax import gen, categorical
    key = random.PRNGKey(42)
    _GENJAX_AVAILABLE = True
except ImportError:
    _GENJAX_AVAILABLE = False
    print("GenJAX not available — the 'Now in GenJAX' cells will not run. The numpy path works fine.")
"""))

    # Problem 1
    cells.append(md(PROBLEM_1_MD))

    cells.append(md(r"""Represent $\mathcal{H}$ as a numpy array of shape `(H, 6)` — each row is a hypothesis. Keep a parallel list of 1–4 word labels."""))

    cells.append(code(r"""# fill me
#
# Suggested approach:
#   1. List your hypothesis labels (strings, 1-4 words each).
#   2. For each label, write a length-6 binary vector — in the SAME order as
#      ANIMALS = ("cow", "dolphin", "chicken", "seal", "penguin", "bat").
#   3. Stack into a numpy array (dtype=float for math convenience).
#   4. Don't forget the catch-all (all ones).
#   5. Keep `4 < H < 63`.

hypothesis_labels = [
    # your labels here
]

hypothesis_matrix = np.array(
    [
        # your binary rows here
    ],
    dtype=float,
)

H = hypothesis_matrix.shape[0]
assert hypothesis_matrix.shape == (H, N_ANIMALS), f"expected (H, {N_ANIMALS}), got {hypothesis_matrix.shape}"
assert len(hypothesis_labels) == H, "labels and matrix rows must align"
assert 4 < H < 63, "use more than 4 and fewer than 63 hypotheses"
assert (hypothesis_matrix.sum(axis=1) > 0).all(), "no empty hypotheses"
assert (hypothesis_matrix == 1).all(axis=1).any(), "include a catch-all hypothesis"
print(f"H = {H} hypotheses, sizes = {hypothesis_matrix.sum(axis=1).astype(int).tolist()}")
"""))

    cells.append(md("*(1–2 sentences describing the properties you chose.)*"))

    # Problem 2
    cells.append(md(PROBLEM_2_MD))

    cells.append(code(r"""# fill me
#
# Suggested approach:
#   1. Uniform prior: np.full(H, 1.0 / H).
#   2. Or any positive length-H vector, normalized.

prior = None   # replace with a length-H numpy array that sums to 1
assert prior is not None and prior.shape == (H,)
assert np.isclose(prior.sum(), 1.0)
"""))

    cells.append(md("*(1–2 sentences justifying your prior.)*"))

    # Problem 3 — posterior
    cells.append(md(PROBLEM_3_INTRO_MD))

    cells.append(md(r"""**Approach.** The hypothesis space is small and discrete, so the posterior is computed by **enumeration**: evaluate the unnormalized posterior at every hypothesis, then normalize."""))

    cells.append(code(r'''# fill me — likelihood under weak and strong sampling
#
# Suggested approach (weak):
#   P(x | h) = 1 if h[x] == 1 else 0.
#   For multiple x's, P(x_1..x_n | h) = prod over n of P(x_n | h) (iid given h).
#
# Suggested approach (strong):
#   P(x | h) = 1/|h| if h[x] == 1 else 0  (where |h| = h.sum()).
#   For multiple x's, prod over n.
#
# Vectorize over hypotheses: pass the full (H, N_ANIMALS) matrix and return a length-H likelihood vector.

def likelihood(hyp_matrix, x_idxs, sampling):
    """Return length-H array of P(x_idxs | h) for each h.

    Args:
        hyp_matrix: shape (H, N_ANIMALS) binary
        x_idxs:     iterable of indices into ANIMALS
        sampling:   "weak" or "strong"
    """
    # fill me
    pass
'''))

    cells.append(code(r"""# fill me — posterior
#
# Suggested approach:
#   1. unnorm = prior * likelihood(hyp_matrix, x_idxs, sampling)
#   2. post   = unnorm / unnorm.sum()       (assert no division by zero)
#
# Tip: work in log-space if you expect numerical issues. For a small H, linear math is fine.

def posterior(x_idxs, sampling, hyp_matrix=hypothesis_matrix, prior_=prior):
    # fill me
    pass
"""))

    cells.append(md(PROBLEM_3A_MD))

    cells.append(code(r"""# fill me
one_obs_idx = [2]   # e.g. chicken

post_weak_1   = None   # = posterior(one_obs_idx, "weak")
post_strong_1 = None   # = posterior(one_obs_idx, "strong")

# Bar-plot side by side with hypothesis_labels on the x-axis.
# fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
# x = np.arange(H)
# axes[0].bar(x, post_weak_1);   axes[0].set_xticks(x); axes[0].set_xticklabels(hypothesis_labels, rotation=45, ha='right')
# axes[1].bar(x, post_strong_1); ...
# axes[0].set_title("Weak — 1 obs"); axes[1].set_title("Strong — 1 obs")

# your plotting code here
"""))

    cells.append(md(r"""### Now in GenJAX — Problem 3(a) optional

**Concept (Tutorial 2 Ch 2–4): a `@gen` model with a discrete latent.** Here the unknown $h$ is a *discrete* index into the hypothesis matrix, so we use `categorical(logits)`. Unlike continuous latents that require importance sampling, a discrete latent with a small support can be handled by **enumeration**: evaluate the unnormalized posterior at every value of `h_idx` and normalize.

**Key syntax:**
- `h_idx = categorical(log_prior) @ "h_idx"` — sample a discrete index from a categorical with given log-probabilities.
- `model.assess(choices, args)` — return `(log_density, retval)` for a complete trace of choices. We use this to score each hypothesis index.

**Why bother?** For a finite hypothesis space, the numpy enumeration above is faster and more transparent. The GenJAX version below is here to show how the *same* model would look as a `@gen` function — the pattern generalizes to mixed discrete-continuous models where direct enumeration is no longer enough."""))

    cells.append(code(r"""# fill me — optional GenJAX path
#
# Suggested approach:
#   1. Write a @gen function `gen_model(log_prior)` that samples h_idx = categorical(log_prior) @ "h_idx"
#      and returns h_idx.
#   2. For one observation x_1 = chicken (index 2):
#        - Compute the posterior over h_idx by enumeration via `assess`:
#            for each h_idx in 0..H-1, score = log_prior[h_idx] + log_likelihood(hyp_matrix[h_idx], [2], "weak")
#            (model.assess works too but for this simple model the formula above is cleaner)
#        - Normalize to get posterior probabilities.
#      Verify they match the numpy result above.
#
# DTYPE: cast log_prior with jnp.float32(...) before passing it in.

if _GENJAX_AVAILABLE:
    log_prior_j = jnp.log(jnp.array(prior, dtype=jnp.float32))

    @gen
    def gen_model(log_prior):
        # h_idx = categorical(log_prior) @ "h_idx"
        # return h_idx
        pass

    # your enumeration + comparison-to-numpy code here
else:
    print("GenJAX not installed — skipping.")
"""))

    cells.append(md("**Your answer (3a).** *(1–2 sentences.)*"))

    cells.append(md(PROBLEM_3B_MD))

    cells.append(code(r"""# fill me
three_obs_idxs = [2, 5, 4]   # e.g. chicken, bat, penguin

post_weak_3   = None
post_strong_3 = None

# your plotting code here
"""))

    cells.append(md("**Your answer (3b).** *(1–2 sentences.)*"))

    # Problem 4
    cells.append(md(PROBLEM_4_MD))

    cells.append(code(r"""# fill me — predictive distribution
#
# Suggested approach:
#   P(y has property | x) = sum over h where h[y]==1 of posterior[h]
#   This is the matrix product: posterior @ hypothesis_matrix   (shape (H,) @ (H, N_ANIMALS))

def predictive(post, hyp_matrix=hypothesis_matrix):
    # fill me
    pass


# Build the four predictives:
#   pred_weak_1, pred_strong_1, pred_weak_3, pred_strong_3
# Then plot as a 2x2 grid (rows = #obs, cols = sampling).

# your code + plotting here
"""))

    cells.append(md("**Your answer (Problem 4).** *(A paragraph.)*"))

    # Problem 5
    cells.append(md(PROBLEM_5_INTRO_MD))

    cells.append(code(r"""# fill me — full 2^6 - 1 hypothesis space
#
# Suggested approach:
#   1. itertools.product([0, 1], repeat=6) -> 64 binary vectors.
#   2. Stack into np.array, drop the all-zeros row (you'll have 63 rows).
#   3. Uniform prior of length 63.
#   4. Reuse posterior() and predictive() — they accept hyp_matrix + prior_ kwargs.

all_hyp_matrix = None    # shape (63, 6)
all_prior      = None    # shape (63,) uniform

# your code here
"""))

    cells.append(code(r"""# fill me — recompute and plot.
#
# Recompute the 1-obs and 3-obs posteriors + predictives under the expanded space.
# You don't need to dump all 63 posterior values — show the predictive (which is length 6).

# your code + plotting here
"""))

    cells.append(md(PROBLEM_5_PROMPT_MD))
    cells.append(md("**Your answer (Problem 5).** *(A few sentences.)*"))

    # Submission
    cells.append(md(SUBMISSION_MD))

    nb = new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11",
        },
    }
    return nb


def main():
    nb_g = build_genjax_notebook()
    nb_p = build_python_notebook()

    with open("generalization.ipynb", "w") as f:
        nbf.write(nb_g, f)
    with open("generalization_python.ipynb", "w") as f:
        nbf.write(nb_p, f)

    print(f"Wrote generalization.ipynb ({len(nb_g['cells'])} cells)")
    print(f"Wrote generalization_python.ipynb ({len(nb_p['cells'])} cells)")


if __name__ == "__main__":
    main()
