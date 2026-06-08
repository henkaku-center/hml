"""Build the GenJAX and Python (no-GenJAX) Jupyter stencils for the
Monte Carlo / MCMC assignment (Assignment 3).

Run from this directory:
    python3 _build_stencils.py

Writes:
    mc_approx.ipynb            (GenJAX canonical — primitives in a hand-assembled loop)
    mc_approx_python.ipynb     (Python + numpy/scipy, with paired "Now in GenJAX" notes)

The R stencil (mcmc_approx.Rmd) is authored separately in this directory.

Design note: the MCMC sampler is a hand-written Gibbs + Metropolis-Hastings loop,
so the canonical GenJAX stencil uses genjax's distribution PRIMITIVES
(beta.sample, beta.logpdf, normal.logpdf) inside the student-assembled loop,
with jax.vmap / jax.lax.scan for speed. This matches the Week 7 lecture's message
that MH is "assembled from the scoring primitives, not a black box." The reference
solutions these cells are blanked from live in .solution_reference/ and are verified
to run end-to-end.
"""

import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell


def md(text):
    return new_markdown_cell(text)


def code(src):
    return new_code_cell(src)


# ===========================================================================
# Shared prose
# ===========================================================================

INTRO_MD = r"""# Assignment 3: Approximation via Monte Carlo

__STENCIL_LABEL__

In this assignment you will explore three Monte Carlo methods:

1. **Problem 1** — compare **naive Monte Carlo** and **importance sampling** for estimating a tail probability $P(Y>2)$, $Y\sim N(0,1)$.
2. **Problem 2** — build a **Markov chain Monte Carlo** sampler (interleaving **Gibbs** and **Metropolis–Hastings**) for the hierarchical Beta-Binomial model of Kemp, Perfors & Tenenbaum (2007).
3. **Problem 3** — quantify how "efficient" a set of samples is with the **effective sample size** ($N_{\mathrm{eff}}$).

**Read `mc_approx.pdf` first** — it has the full problem statements and all the math. This notebook is the scaffold: cells marked `# fill me` are for you to complete. Submit the completed notebook (it must run end-to-end) *or* a single PDF report with your code, figures, and written answers.

**Textbook background:** Tutorial 3 Ch 12 (hierarchical Bayes / approximate inference). The Week 7 lecture covers Monte Carlo, importance sampling, and MCMC (Metropolis–Hastings + Gibbs)."""

# --- Problem 1 ---

P1_MD = r"""---

## Problem 1: Monte Carlo vs. importance sampling

Estimate $P(Y>2)$ for $Y\sim N(0,1)$ two ways, with $T=1000$ samples.

- **(a) Naive MC.** Draw $x^{(1)},\dots,x^{(T)}\sim N(0,1)$ and form the cumulative estimate $f_{MC}(t) = \frac{1}{t}\sum_{s\le t} \mathbb{1}[x^{(s)}>2]$. Plot $f_{MC}$ vs. $t$. Report $f_{MC}(T)$ and explain the shape of the curve.
- **(b) Importance sampling.** Draw $x^{(1)},\dots,x^{(T)}\sim q=N(2,1)$ and form the cumulative IS estimate using the explicit weight $e^{-2x+2}\,\mathbb{1}[x>2]$. Plot $f_{IS}$ vs. $t$. Report $f_{IS}(T)$.
- **(c)** Compare the two curves: how and why do they differ? State a broad lesson about Monte Carlo approximation."""

# --- Problem 2 ---

P2_MD = r"""---

## Problem 2: MCMC for the Kemp hierarchical Beta-Binomial model

You observe $M$ bags of marbles; bag $i$ shows $y_i$ white out of $n_i$ drawn. The model:
$$\theta_i \mid \kappa,\varphi \sim \mathrm{Beta}(\kappa\varphi,\ \kappa(1-\varphi)), \qquad y_i \mid n_i,\theta_i \sim \mathrm{Binomial}(\theta_i; n_i),$$
parameterized by the **mean** $\varphi=a/(a+b)$ and **concentration** $\kappa=a+b$ (so $a=\kappa\varphi$, $b=\kappa(1-\varphi)$). Priors: $\varphi\sim\mathrm{Uniform}(0,1)$ and a weak proper **log-normal** on $\kappa$, i.e. $\log\kappa\sim N(\mu_0,\sigma_0^2)$ with $\mu_0=\log 10$, $\sigma_0=1.5$.

The sampler does two moves per sweep:
- **Gibbs** resamples each $\theta_i$ from its conjugate posterior $\mathrm{Beta}(\kappa\varphi+y_i,\ \kappa(1-\varphi)+n_i-y_i)$.
- **Metropolis–Hastings** updates $(\varphi,\ell)$ with $\ell=\log\kappa$, via a symmetric Gaussian random walk. The acceptance ratio is the Beta likelihood of the current $\theta_i$'s times the log-normal prior ratio on $\ell$ (the proposal is symmetric, so there is no asymmetry-correction term, and there is no Jacobian — see the PDF).

See `mc_approx.pdf` Problem 2 for the full derivation and the acceptance formula."""

# --- Problem 3 ---

P3_MD = r"""---

## Problem 3: Effective sample size

The effective sample size summarizes how useful a set of weighted samples is:
$$N_{\mathrm{eff}} = \frac{1}{\sum_t (w^{(t)})^2}, \qquad w^{(t)}\ge 0,\ \textstyle\sum_t w^{(t)}=1.$$

- **(a) Good vs. bad proposal.** With target $p=N(0,1)$ and IS weights $w\propto p/q$, compute $N_{\mathrm{eff}}$ for a **good** proposal that overlaps $p$ well (e.g. $q=N(0,1.5^2)$) and a **bad** one that does not (e.g. $q=N(4,1)$). You should see good $q$ in the high hundreds, bad $q$ in the single digits. (Do **not** use $q=N(2,1)$ here — that is part (b).)
- **(b) The puzzle.** Compute $N_{\mathrm{eff}}$ for two estimators of $P(Y>2)$: the IS sampler with $q=N(2,1)$ ($w\propto p/q$), and plain MC from $p$ ($w=1/T$). MC reports $N_{\mathrm{eff}}=T=1000$ while IS reports ~50 — yet IS is the *more accurate* estimator (Problem 1). Resolve the puzzle in writing (see the PDF for the three points to address)."""


# ===========================================================================
# GenJAX canonical stencil
# ===========================================================================

def build_genjax_notebook():
    cells = []
    cells.append(md(INTRO_MD.replace(
        "__STENCIL_LABEL__",
        "This is the **GenJAX (canonical)** stencil. Two paired stencils are available — "
        "`mc_approx_python.ipynb` (Python + numpy/scipy) and `mcmc_approx.Rmd` (R). "
        "Matlab available on request.\n\n"
        "**How GenJAX is used here.** The sampler is a loop *you* assemble. GenJAX gives "
        "you the scoring primitives — `beta.sample`, `beta.logpdf`, `normal.logpdf` — and "
        "JAX gives you speed (`jax.vmap`, `jax.lax.scan`, `jax.jit`). This mirrors the "
        "lecture: MH is *assembled from the scoring primitives*, not a black box.")))

    cells.append(code(
        "# !pip install genjax\n"
        "import jax\n"
        "import jax.numpy as jnp\n"
        "import jax.random as random\n"
        "from genjax import beta, normal\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "# genjax 0.10.3 primitive cheatsheet (all match scipy):\n"
        "#   beta.sample(key, a, b)        -> one Beta(a,b) draw\n"
        "#   beta.logpdf(x, a, b)          -> log density (vectorizes over x)\n"
        "#   normal.logpdf(x, mu, sigma)   -> log density of N(mu, sigma^2)\n"
        "#   random.normal(key, shape)     -> standard normal draws\n"
        "# NOTE: genjax's `binomial` takes LOGITS, not a probability -- we do not\n"
        "# need it here (bag data are given directly as (y, n))."))

    # ----- Problem 1 -----
    cells.append(md(P1_MD))
    cells.append(code(
        '# fill me -- Problem 1(a) and 1(b)\n'
        '#\n'
        '# (a) Naive MC for P(Y>2), Y~N(0,1):\n'
        '#   - draw x ~ N(0,1), T of them, with random.normal\n'
        '#   - indicator = (x > 2)\n'
        '#   - cumulative estimate f_mc[t] = mean of indicator over first t samples\n'
        '#     (hint: jnp.cumsum(indicator) / jnp.arange(1, T+1))\n'
        '#\n'
        '# (b) Importance sampling with q = N(2,1):\n'
        '#   - draw xis = 2 + random.normal(...)\n'
        '#   - weight w = exp(-2*xis + 2) * (xis > 2)   # the explicit p/q * indicator\n'
        '#   - cumulative estimate f_is[t] = mean of w over first t samples\n'
        '\n'
        'T = 1000\n'
        'key = random.PRNGKey(0)\n'
        '\n'
        '# f_mc = ...\n'
        '# f_is = ...\n'
        '\n'
        '# Plot both cumulative estimates vs t on the same axes, with a line at the\n'
        '# true value (you may use jax.scipy.stats.norm or scipy.stats.norm for the truth).\n'))

    # ----- Problem 2 -----
    cells.append(md(P2_MD))
    cells.append(code(
        '# Provided: the two bag sets and the prior hyperparameters.\n'
        'MU0, S0 = jnp.log(10.0), 1.5   # log-normal prior on kappa: log(kappa) ~ N(MU0, S0^2)\n'
        '\n'
        'def ab(kappa, phi):\n'
        '    """Convert (concentration, mean) -> Beta shape params (a, b)."""\n'
        '    return kappa * phi, kappa * (1 - phi)\n'
        '\n'
        '# Bag set I: 10 bags, each 9 white of 20.   Bag set II: 5 bags 1/20, 5 bags 19/20.\n'
        'bagset_I  = (jnp.array([9.0]*10),               jnp.array([20.0]*10))\n'
        'bagset_II = (jnp.array([1.0]*5 + [19.0]*5),     jnp.array([20.0]*10))'))

    cells.append(code(
        '# fill me -- Problem 2(a): the conjugate posterior over theta for FIXED (kappa, phi).\n'
        '#\n'
        '# For each (kappa, phi) pair in the PDF, plot on one figure: the prior Beta(a, b),\n'
        '# and the posteriors after (1 white, 0 black), (5,5), and (9,1). Use the conjugate\n'
        '# update: posterior = Beta(a + y, b + (n - y)). beta.logpdf(grid, a, b) gives the\n'
        '# log-density on a grid in (0,1); exponentiate to plot.\n'
        '\n'
        'grid = jnp.linspace(1e-3, 1 - 1e-3, 400)\n'
        '\n'
        '# def plot_posterior_updates(kappa, phi): ...\n'
        '# plot_posterior_updates(1.0, 0.5)   # etc. for the six pairs\n'))

    cells.append(code(
        '# fill me -- Problem 2(b)+(c): implement the Gibbs + MH sampler.\n'
        '#\n'
        '# Write ONE sweep as a function step(carry, key) for use with jax.lax.scan, where\n'
        '# carry = (phi, ell) with ell = log(kappa). Each sweep:\n'
        '#\n'
        '#   1. GIBBS: resample every theta_i from its conjugate posterior\n'
        '#        theta_i ~ Beta(a + y_i,  b + (n_i - y_i))     where a, b = ab(exp(ell), phi)\n'
        '#      Vectorize over bags: split a key per bag and jax.vmap beta.sample.\n'
        '#\n'
        '#   2. MH PROPOSE: eps ~ N(0,1) of shape (2,);\n'
        '#        phi_p = phi + s_phi * eps[0];   ell_p = ell + s_ell * eps[1]\n'
        '#      (s_phi, s_ell are the step sizes you will tune in part (e).)\n'
        '#\n'
        '#   3. ACCEPT/REJECT: with ap, bp = ab(exp(ell_p), phi_p),\n'
        '#        log_c =   sum(beta.logpdf(theta, ap, bp)) - sum(beta.logpdf(theta, a, b))\n'
        '#                + normal.logpdf(ell_p, MU0, S0)    - normal.logpdf(ell, MU0, S0)\n'
        '#      accept iff (0 < phi_p < 1) and (log(uniform) < log_c). On reject, keep (phi, ell).\n'
        '#      (Symmetric proposal => no asymmetry correction; prior is on ell directly => no Jacobian.)\n'
        '#\n'
        '#   Record (kappa, phi, accepted) each sweep via the scan output.\n'
        '#\n'
        '# Then wrap with jax.lax.scan over random.split(key, T). Remember to jit with\n'
        '# T as a STATIC argument (functools.partial(jax.jit, static_argnums=...)) -- otherwise\n'
        '# random.split(key, T) fails to trace.\n'
        '\n'
        'def make_sampler(y, n, s_phi, s_ell):\n'
        '    M = len(y)\n'
        '    def step(carry, key):\n'
        '        phi, ell = carry\n'
        '        # fill me\n'
        '        pass\n'
        '    def run(key, T):\n'
        '        # fill me -- lax.scan(step, (0.5, jnp.log(10.0)), random.split(key, T))\n'
        '        pass\n'
        '    return run\n'))

    cells.append(code(
        '# fill me -- Problem 2(d): run the sampler on bag sets I and II.\n'
        '#\n'
        '# For each set: run T = 3000 sweeps (after a few hundred burn-in), then\n'
        '#   - histogram the kappa samples and the phi samples (separately),\n'
        '#   - report posterior means kbar = mean(kappa), pbar = mean(phi),\n'
        '#   - report the predictive prob a new bag is white = pbar (since E[theta]=phi).\n'
        '# Suggested starting step sizes: set I  ~ (s_phi=0.04, s_ell=0.30);\n'
        '#                                set II ~ (s_phi=0.05, s_ell=0.40).\n'
        '\n'
        '# run_I = make_sampler(*bagset_I, s_phi=0.04, s_ell=0.30)\n'
        '# ks, ps, accs = run_I(random.PRNGKey(1), 3000)\n'
        '# ... burn-in, histograms, means ...\n'))

    cells.append(code(
        '# fill me -- Problem 2(e): tune the step sizes.\n'
        '#\n'
        '# Report the acceptance rate (mean of the `accepted` flags) for each bag set, and\n'
        '# adjust (s_phi, s_ell) so each lands in ~0.2-0.5. You will find the two sets prefer\n'
        '# different step sizes. Then write the short explanation asked for in the PDF\n'
        '# (too-small vs too-large step; why the two sets differ; connect to mixing).\n'))

    # ----- Problem 3 -----
    cells.append(md(P3_MD))
    cells.append(code(
        '# fill me -- Problem 3.\n'
        '#\n'
        'def ess(w):\n'
        '    """Effective sample size from unnormalized nonnegative weights w."""\n'
        '    # fill me:  normalize w to sum to 1, then return 1 / sum(w**2)\n'
        '    pass\n'
        '\n'
        '# (a) good vs bad proposal for target p = N(0,1), weights w = p(x)/q(x):\n'
        '#     good q = N(0, 1.5^2);  bad q = N(4, 1).  Use T = 1000. Report both ESS.\n'
        '#     (weight in log space then exponentiate:\n'
        '#         logw = normal.logpdf(xq, 0., 1.) - normal.logpdf(xq, q_mean, q_sd))\n'
        '#\n'
        '# (b) the puzzle: ESS for IS (q=N(2,1), w = p/q) vs plain MC (w = ones).\n'
        '#     Report both, then write the resolution (see PDF).\n'))

    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    return nb


# ===========================================================================
# Python (no-GenJAX) stencil
# ===========================================================================

def build_python_notebook():
    cells = []
    cells.append(md(INTRO_MD.replace(
        "__STENCIL_LABEL__",
        "This is the **Python (no-GenJAX)** stencil — numpy + scipy + matplotlib. "
        "If you'd prefer the GenJAX-first stencil, see `mc_approx.ipynb`. The math is "
        "identical; only the library calls differ. Each problem has a short *Now in GenJAX* "
        "note showing the one-line translation, in case you want to compare.")))

    cells.append(code(
        "import numpy as np\n"
        "from scipy.stats import norm, beta as Beta\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "rng = np.random.default_rng(0)\n"
        "\n"
        "# scipy cheatsheet:\n"
        "#   rng.standard_normal(T)          -> standard normal draws\n"
        "#   rng.beta(a, b)                  -> one Beta(a,b) draw\n"
        "#   Beta.logpdf(x, a, b)            -> log density (vectorizes over x)\n"
        "#   norm.logpdf(x, mu, sigma)       -> log density of N(mu, sigma^2)\n"
        "# Now in GenJAX: rng.beta(a,b)->beta.sample(key,a,b); Beta.logpdf->beta.logpdf;\n"
        "#                norm.logpdf->normal.logpdf."))

    # Problem 1
    cells.append(md(P1_MD))
    cells.append(code(
        '# fill me -- Problem 1(a) naive MC and 1(b) importance sampling.\n'
        '#\n'
        '# (a) x = rng.standard_normal(T); ind = (x > 2); f_mc = np.cumsum(ind)/np.arange(1,T+1)\n'
        '# (b) xis = 2 + rng.standard_normal(T); w = np.exp(-2*xis+2)*(xis>2); f_is = cumsum/arange\n'
        '# Plot both vs t with the true value (1 - norm.cdf(2)) as a reference line.\n'
        '\n'
        'T = 1000\n'))

    # Problem 2
    cells.append(md(P2_MD + "\n\n*Now in GenJAX:* replace `rng.beta(a,b)` with `beta.sample(key,a,b)`, `Beta.logpdf` with `beta.logpdf`, and `norm.logpdf` with `normal.logpdf`; the loop is identical."))
    cells.append(code(
        'MU0, S0 = np.log(10.0), 1.5\n'
        '\n'
        'def ab(kappa, phi):\n'
        '    return kappa * phi, kappa * (1 - phi)\n'
        '\n'
        'bagset_I  = (np.array([9]*10),            np.array([20]*10))\n'
        'bagset_II = (np.array([1]*5 + [19]*5),    np.array([20]*10))'))

    cells.append(code(
        '# fill me -- Problem 2(a): conjugate posterior over theta for fixed (kappa, phi).\n'
        '# For each (kappa, phi) in the PDF, plot prior Beta(a,b) and the posteriors after\n'
        '# (1,0), (5,5), (9,1) on one figure. Posterior = Beta(a + y, b + (n - y)).\n'
        'grid = np.linspace(1e-3, 1-1e-3, 400)\n'))

    cells.append(code(
        '# fill me -- Problem 2(b)+(c): the Gibbs + MH sampler.\n'
        '#\n'
        'def sampler(y, n, T=3000, burn=500, s_phi=0.04, s_ell=0.30, seed=0):\n'
        '    rng = np.random.default_rng(seed)\n'
        '    M = len(y)\n'
        '    phi, ell = 0.5, np.log(10.0)\n'
        '    theta = np.full(M, 0.5)\n'
        '    ks, ps = [], []\n'
        '    n_acc = 0\n'
        '    for t in range(T):\n'
        '        kappa = np.exp(ell); a, b = ab(kappa, phi)\n'
        '        # 1. GIBBS sweep: for each bag i (random order),\n'
        '        #    theta[i] = rng.beta(a + y[i], b + (n[i] - y[i]))\n'
        '        # 2. MH propose: phi_p = phi + s_phi*N(0,1); ell_p = ell + s_ell*N(0,1)\n'
        '        # 3. accept iff 0<phi_p<1 and log(rng.uniform()) < log_c, where\n'
        '        #    log_c =  sum(Beta.logpdf(theta, ap, bp)) - sum(Beta.logpdf(theta, a, b))\n'
        '        #           + norm.logpdf(ell_p, MU0, S0)     - norm.logpdf(ell, MU0, S0)\n'
        '        #    On reject, keep (phi, ell). Record kappa, phi after burn-in.\n'
        '        # fill me\n'
        '        pass\n'
        '    return np.array(ks), np.array(ps), n_acc / T\n'))

    cells.append(code(
        '# fill me -- Problem 2(d): run on bag sets I and II; histograms of kappa and phi;\n'
        '# report mean kappa, mean phi, and the predictive value (= mean phi).\n'))

    cells.append(code(
        '# fill me -- Problem 2(e): report acceptance rate per set; tune s_phi, s_ell to ~0.2-0.5;\n'
        '# explain too-small vs too-large steps and why the two sets differ (connect to mixing).\n'))

    # Problem 3
    cells.append(md(P3_MD + "\n\n*Now in GenJAX:* the ESS formula is library-agnostic; only the weight computation changes (`norm.logpdf` -> `normal.logpdf`)."))
    cells.append(code(
        '# fill me -- Problem 3.\n'
        'def ess(w):\n'
        '    """Effective sample size from unnormalized nonnegative weights."""\n'
        '    # fill me: normalize, then 1 / sum(w**2)\n'
        '    pass\n'
        '\n'
        '# (a) good q=N(0,1.5^2) vs bad q=N(4,1), target p=N(0,1), w = p/q. Report both ESS.\n'
        '# (b) IS (q=N(2,1), w=p/q) vs plain MC (w=ones). Report both; write the resolution.\n'))

    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    return nb


def main():
    with open("mc_approx.ipynb", "w") as f:
        nbf.write(build_genjax_notebook(), f)
    with open("mc_approx_python.ipynb", "w") as f:
        nbf.write(build_python_notebook(), f)
    print("Wrote mc_approx.ipynb (GenJAX) and mc_approx_python.ipynb (Python).")


if __name__ == "__main__":
    main()
