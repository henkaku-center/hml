#!/usr/bin/env python3
"""
genjax_biasvariance.py -- Week 10 GenJAX backbone: the Bias-Variance Dilemma
and (benign) Double Descent.

This is a *dual-homed* script: it produces the Week-10 lecture figures AND is the
verified code spine for the Phase-2 textbook "Bias-Variance Dilemma" chapter. Keep
it clean, documented, and runnable end-to-end:

    cd course/week10_bayesian_nonparametrics
    python3 genjax_biasvariance.py        # CPU is fine; ignore the CUDA warning

Three parts:

  (1) A GenJAX generative model for *Bayesian polynomial regression*. Putting an
      i.i.d. Gaussian prior on the coefficients IS ridge regression -- the ridge
      penalty is exactly the negative log of that prior. The closed-form
      posterior mean is the usual ridge estimator, which we use for speed.

  (2) A bias-variance sweep over polynomial degree d = 1..12. Resampling many
      datasets and fitting each exposes the classic U-curve:
      test error = bias^2 + variance.

  (3) Double descent. CRITICAL: a 1-D polynomial / random-feature model does NOT
      show *benign* double descent -- the min-norm interpolant diverges for
      width > n. Benign double descent is a HIGH-DIMENSIONAL phenomenon, so part
      (3) switches to an isotropic high-dim random-feature model and sweeps model
      capacity p through the interpolation threshold p = n.

Tested against jax 0.5.3 / genjax 0.10.3, Python 3.12 (CPU).

Funding note (textbook): this material is developed for the "Narrative
Introduction to Probability" textbook; reuse the model + sweeps as the chapter
spine rather than re-deriving them.
"""

import os

import numpy as np
import jax
import jax.numpy as jnp
from genjax import gen, normal

import matplotlib
matplotlib.use("Agg")  # headless: write PNGs, never open a window
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Dark SDS theme (mirrors course/week10_bayesian_nonparametrics/make_figures.py
# so these figures composite cleanly onto the #111111 slide background).
# ----------------------------------------------------------------------------
BG = "#111111"; WHITE = "#ffffff"; DIM = "#999999"
ACC = "#64B5F6"; RED = "#EF5350"; ORA = "#FFA726"
GRN = "#66BB6A"; YEL = "#FFEB3B"; PUR = "#BA68C8"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": WHITE, "axes.labelcolor": "#cfcfcf",
    "xtick.color": DIM, "ytick.color": DIM, "axes.edgecolor": "#3a3a48",
    "font.size": 12, "font.family": "DejaVu Sans",
})

# ----------------------------------------------------------------------------
# Problem constants.
# ----------------------------------------------------------------------------
TAU = 3.0      # Gaussian (ridge) prior std on each coefficient beta_j
SIGMA = 0.25   # observation-noise std for the regression problem


def true_f(x):
    """Fixed cubic ground truth on [0, 1] (range ~[-1, 1]).

    The model never gets to see this functional form; it only sees noisy
    samples. Bias is what remains because the fitted family is *not* this cubic.
    """
    return 1.7 * (x - 0.18) * (x - 0.55) * (x - 0.88) * 5.0


def design_matrix(x, degree):
    """Polynomial design rows [1, t, t^2, ..., t^degree] with t = 2x - 1.

    Centering/scaling x in [0, 1] to t in [-1, 1] keeps the columns
    well-conditioned (a poor man's Chebyshev basis), which matters once the
    degree climbs into the teens.

    Args:
        x:      array of inputs in [0, 1], shape (n,).
        degree: Python int (captured as a constant; see make_regression_model).

    Returns:
        design array of shape (n, degree + 1).
    """
    t = 2.0 * x - 1.0
    return jnp.stack([t ** j for j in range(degree + 1)], axis=-1)


# ============================================================================
# PART 1 -- GenJAX generative model: Bayesian polynomial regression
#           ("ridge regression IS a Gaussian prior over the coefficients")
# ============================================================================
def make_regression_model(x, degree):
    """Factory returning a @genjax.gen Bayesian polynomial-regression model.

    The factory pattern captures `degree` (hence the design matrix and the
    coefficient count p = degree + 1) as Python constants in the closure. That
    is required: a `for j in range(degree)` where `degree` is a *traced* model
    argument raises TracerIntegerConversionError in GenJAX.

    Generative story (this is the whole model):
        beta_j ~ Normal(0, tau)          # i.i.d. Gaussian prior == ridge penalty
        y_i    ~ Normal(Phi[i] . beta, sigma)

    Args:
        x:      design inputs in [0, 1], shape (n,).
        degree: polynomial degree (Python int).

    Returns:
        a GenJAX generative function `model(tau, sigma)` whose return value is
        the vector y of shape (n,). Run it with `model.simulate(key, (tau, sigma))`.
    """
    Phi = design_matrix(x, degree)
    p = degree + 1

    @gen
    def model(tau, sigma):
        # Vectorized prior: one Normal(0, tau) per coefficient. Sampling the
        # whole vector at a single address ("beta") is the clean GenJAX idiom and
        # broadcasts the scalar tau across the p coordinates.
        beta = normal(jnp.zeros(p), tau) @ "beta"
        mu = Phi @ beta                  # noise-free function values at x
        y = normal(mu, sigma) @ "y"      # vectorized Gaussian likelihood
        return y

    return model


def ridge_posterior_mean(Phi, y, tau, sigma):
    """Closed-form posterior mean of the Part-1 model == the ridge estimator.

        beta_hat = (Phi^T Phi + (sigma^2 / tau^2) I)^{-1} Phi^T y

    The ridge strength lambda = sigma^2 / tau^2 is not a free knob here -- it is
    *dictated* by the prior (tau) and the noise (sigma). A tighter prior (small
    tau) => stronger shrinkage. We use the closed form purely for speed; it is
    the exact posterior mean of the GenJAX model above.
    """
    p = Phi.shape[-1]
    lam = (sigma ** 2) / (tau ** 2)
    A = Phi.T @ Phi + lam * jnp.eye(p)
    return jnp.linalg.solve(A, Phi.T @ y)


@gen
def observe(mu, sigma):
    """Shared Gaussian likelihood, factored out so the bias-variance sweep draws
    its noisy datasets *through GenJAX* rather than calling jax.random directly.

    Given a vector of true means mu (here mu = true_f(x)), returns one noisy
    dataset y ~ Normal(mu, sigma).
    """
    return normal(mu, sigma) @ "y"


def demo_generative_model(key, n=20, degree=6):
    """Exercise the GenJAX model: draw prior-predictive functions and one fit.

    Returns a dict of arrays used by the left panel of the bias-variance figure
    and prints a short confirmation that the generative model runs.
    """
    grid = jnp.linspace(0.0, 1.0, 200)

    # --- prior predictive: simulate coefficients from the prior, read them back
    #     out of the trace, and turn them into smooth functions on a grid. ---
    prior_model = make_regression_model(grid, degree)
    keys = jax.random.split(key, 6)
    Phi_grid = design_matrix(grid, degree)

    def one_prior_function(k):
        tr = prior_model.simulate(k, (TAU, SIGMA))
        beta = tr.get_choices()["beta"]      # genuinely read the latent draw
        return Phi_grid @ beta               # the noise-free function it implies
    prior_funcs = jax.vmap(one_prior_function)(keys)  # (6, 200)

    # --- one dataset from the TRUE cubic (noise via the GenJAX observe model),
    #     then the ridge posterior-mean fits at three degrees. ---
    kx, ko = jax.random.split(jax.random.fold_in(key, 99))
    x = jax.random.uniform(kx, (n,))
    y = observe.simulate(ko, (true_f(x), SIGMA)).get_retval()

    fits = {}
    for d in (1, 3, 12):
        beta_hat = ridge_posterior_mean(design_matrix(x, d), y, TAU, SIGMA)
        fits[d] = design_matrix(grid, d) @ beta_hat

    print("[part 1] GenJAX generative model exercised:")
    print(f"         prior-predictive functions: {prior_funcs.shape[0]} draws, "
          f"value range [{float(prior_funcs.min()):+.2f}, {float(prior_funcs.max()):+.2f}]")
    print(f"         one dataset (n={n}) drawn via observe(); ridge fits at d=1,3,12 computed")

    return dict(grid=np.asarray(grid), prior_funcs=np.asarray(prior_funcs),
                x=np.asarray(x), y=np.asarray(y),
                fits={d: np.asarray(v) for d, v in fits.items()})


# ============================================================================
# PART 2 -- Bias-variance sweep over polynomial degree
# ============================================================================
def sample_datasets(key, M, n):
    """Draw M independent regression datasets.

    Each dataset is x ~ Uniform[0, 1]^n and y = true_f(x) + Normal(0, SIGMA),
    with the noise sampled through the GenJAX `observe` model (vmapped over the
    M datasets). The datasets are shared across all degrees so the bias/variance
    curves are comparable.

    Returns:
        X: (M, n) inputs,  Y: (M, n) noisy targets.
    """
    kx, ky = jax.random.split(key)
    X = jax.random.uniform(kx, (M, n))
    mu = true_f(X)                                    # (M, n) true means
    keys = jax.random.split(ky, M)
    Y = jax.vmap(lambda k, m: observe.simulate(k, (m, SIGMA)).get_retval())(keys, mu)
    return X, Y


def bias_variance_sweep(key, degrees, M=60, n=20, n_grid=200):
    """Decompose test error into bias^2 + variance at each polynomial degree.

    For each degree d:
      * fit every one of the M datasets with the ridge posterior mean,
      * evaluate all fits on a dense grid,
      * bias^2   = mean over grid of (mean-fit - true_f)^2,
      * variance = mean over grid of (per-grid-point variance of the fits),
      * total    = bias^2 + variance.

    Returns (bias2, variance, total) as numpy arrays aligned with `degrees`.
    """
    grid = jnp.linspace(0.0, 1.0, n_grid)
    f_grid = true_f(grid)
    X, Y = sample_datasets(key, M, n)

    bias2, variance, total = [], [], []
    for d in degrees:
        Phi_grid = design_matrix(grid, d)

        def fit_eval(x_i, y_i):
            beta_hat = ridge_posterior_mean(design_matrix(x_i, d), y_i, TAU, SIGMA)
            return Phi_grid @ beta_hat               # prediction on the grid
        fits = jax.vmap(fit_eval)(X, Y)              # (M, n_grid)

        mean_fit = jnp.mean(fits, axis=0)
        b2 = float(jnp.mean((mean_fit - f_grid) ** 2))
        v = float(jnp.mean(jnp.var(fits, axis=0)))
        bias2.append(b2); variance.append(v); total.append(b2 + v)

    return np.array(bias2), np.array(variance), np.array(total)


def plot_bias_variance(demo, degrees, bias2, variance, total, outpath):
    """Two-panel figure: example fits (left) + the bias-variance U-curve (right)."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 4.6))

    # --- left: the GenJAX model in action -- three ridge fits to one dataset ---
    g = demo["grid"]
    axL.plot(g, true_f(g), color=WHITE, lw=2.4, label="truth  f(x)")
    fit_styles = {1: (RED, "degree 1  (underfit)"),
                  3: (GRN, "degree 3  (good)"),
                  12: (ORA, "degree 12  (overfit)")}
    for d, (c, lab) in fit_styles.items():
        axL.plot(g, np.clip(demo["fits"][d], -2.6, 2.6), color=c, lw=2.2, label=lab)
    axL.scatter(demo["x"], demo["y"], color=YEL, s=46, zorder=6,
                edgecolor="white", linewidth=1.0, label="one dataset")
    axL.set_ylim(-2.6, 2.6); axL.set_xlim(0, 1)
    axL.set_xlabel("input  x"); axL.set_ylabel("y")
    axL.set_title("Ridge fits from the GenJAX model", color=WHITE, fontsize=12.5, pad=8)
    axL.legend(facecolor="#181820", edgecolor="#3a3a48", labelcolor="#dddddd",
               fontsize=9, loc="upper center", ncol=2)

    # --- right: bias^2, variance, and their sum vs degree -- the classic U ---
    axR.plot(degrees, bias2, color=RED, lw=2.2, marker="o", ms=4,
             label="bias$^2$  (falls with degree)")
    axR.plot(degrees, variance, color=ORA, lw=2.2, marker="s", ms=4,
             label="variance  (rises with degree)")
    axR.plot(degrees, total, color=ACC, lw=3.0, marker="D", ms=5,
             label="test error = bias$^2$ + variance")
    imin = int(np.argmin(total))
    axR.axvline(degrees[imin], color=DIM, ls=":", lw=1.3)
    axR.scatter([degrees[imin]], [total[imin]], color=YEL, zorder=6, s=55,
                edgecolor="#222", linewidth=0.6)
    axR.annotate(f"sweet spot\n(degree {degrees[imin]})", (degrees[imin], total[imin]),
                 textcoords="offset points", xytext=(14, 18), color=YEL, fontsize=10.5)
    axR.set_xlabel("polynomial degree  (model complexity)  ->")
    axR.set_ylabel("error")
    axR.set_xticks(list(degrees))
    axR.set_ylim(0, min(1.0, float(np.max(total)) * 1.15))
    axR.set_title("The classical bias-variance tradeoff", color=WHITE, fontsize=12.5, pad=8)
    axR.legend(facecolor="#181820", edgecolor="#3a3a48", labelcolor="#dddddd",
               fontsize=9.5, loc="upper center")

    fig.suptitle("Bias-variance dilemma (Bayesian polynomial regression)",
                 color=WHITE, fontsize=14, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"[part 2] wrote {outpath}")


# ============================================================================
# PART 3 -- Double descent (HIGH-DIMENSIONAL isotropic random features)
# ============================================================================
# Why high-dim: a 1-D polynomial / random-feature model does NOT show *benign*
# double descent -- past the interpolation threshold its min-norm interpolant
# diverges. Benign double descent (the second descent) needs many isotropic
# directions so the min-norm solution's implicit l2 bias becomes a useful prior.
#
# Model:
#   features z ~ N(0, I_D) in R^D
#   signal   theta_j ~ DD_DECAY^j, normalized to ||theta|| = 1   (decaying coords)
#   target   y = z . theta + DD_SIGMA * noise
# Capacity sweep: use the first p of the D features, p = 1 .. 8n. Fit the
# min-norm least-squares solution and measure test error (bias^2 + variance
# against the *noise-free* signal z.theta) on fresh draws.
#
# Note on DD_DECAY: the task suggested theta_j ~ 0.98^j. Over D=180 dims that
# spreads the signal across ~1/(1-0.98^2) ~= 25 effective directions, which is
# *larger* than n -- so the underparameterized sweet spot is washed out and there
# is no visible classical U on the left. A moderately faster geometric decay
# (0.9) concentrates the signal into ~5 effective directions, which restores the
# textbook left-hand U while staying a "decaying coordinates" signal. The three
# qualitative features the curve must show -- left U, spike at p=n, second
# descent -- are robust to the exact decay; 0.9 simply makes them all legible.
DD_N = 20          # training points (interpolation threshold sits here)
DD_D = 180         # ambient feature dimension (>= 8 * DD_N)
DD_SIGMA = 0.3     # label noise std (this is what the spike interpolates)
DD_DECAY = 0.9     # geometric decay of the true coefficients
DD_REPS = 50       # training-set replications averaged at each capacity
DD_NTEST = 2500    # fresh test points for the risk estimate


def _signal(D, decay):
    """True coefficient vector with geometrically decaying coords, unit norm."""
    theta = decay ** np.arange(D)
    return theta / np.linalg.norm(theta)


def _fit_min_norm(Xtr, ytr, n):
    """Min-norm least-squares fit on a (n, p) design.

    p <= n  (under/critically parameterized): normal equations with a tiny ridge
            (1e-8) only for numerical stability near p = n.
    p >  n  (overparameterized): the minimum-norm interpolant
            beta = X^T (X X^T)^{-1} y, computed via the (n x n) Gram matrix.
    """
    p = Xtr.shape[1]
    if p <= n:
        A = Xtr.T @ Xtr + 1e-8 * np.eye(p)
        return np.linalg.solve(A, Xtr.T @ ytr)
    G = Xtr @ Xtr.T + 1e-8 * np.eye(n)
    return Xtr.T @ np.linalg.solve(G, ytr)


def double_descent(seed=0, n=DD_N, D=DD_D, sigma=DD_SIGMA, decay=DD_DECAY,
                   reps=DD_REPS, n_test=DD_NTEST):
    """Sweep capacity p = 1..8n and return (ps, risk, n).

    risk[i] is the expected test error E||pred - signal||^2 at capacity ps[i],
    averaged over `reps` independent training sets and `n_test` fresh test
    points. Because the test target is the noise-free signal z.theta, this risk
    is exactly bias^2 + variance (no irreducible-noise floor).
    """
    rng = np.random.default_rng(seed)
    theta = _signal(D, decay)
    Ztest = rng.standard_normal((n_test, D))
    test_signal = Ztest @ theta                 # noise-free test targets
    ps = np.arange(1, 8 * n + 1)
    risk = np.zeros(len(ps))

    for _ in range(reps):
        Ztr = rng.standard_normal((n, D))
        ytr = Ztr @ theta + sigma * rng.standard_normal(n)   # noisy training labels
        for i, p in enumerate(ps):
            beta = _fit_min_norm(Ztr[:, :p], ytr, n)
            pred = Ztest[:, :p] @ beta
            risk[i] += np.mean((pred - test_signal) ** 2)
    risk /= reps
    return ps, risk, n


def plot_double_descent(ps, risk, n, outpath):
    """Plot test error vs capacity on a log-y axis, marking the p = n threshold."""
    fig, ax = plt.subplots(figsize=(8.6, 4.8))

    under = ps <= n
    over = ps >= n
    ax.plot(ps[under], risk[under], color=ACC, lw=2.6,
            label="test error  (underparameterized)")
    ax.plot(ps[over], risk[over], color=GRN, lw=2.6,
            label="test error  (overparameterized)")

    # interpolation threshold
    ax.axvline(n, color=RED, ls=":", lw=1.6)
    ax.text(n * 1.04, risk.max() * 0.62, "p = n\n(interpolation\nthreshold)",
            color=RED, fontsize=10.5, va="center")

    # left-hand sweet spot (classical U minimum)
    imin_left = int(np.argmin(risk[:n - 1]))
    ax.scatter([ps[imin_left]], [risk[imin_left]], color=YEL, s=55, zorder=6,
               edgecolor="#222", linewidth=0.6)
    ax.annotate("classical\nsweet spot", (ps[imin_left], risk[imin_left]),
                textcoords="offset points", xytext=(2, -42), color=YEL, fontsize=10,
                ha="center")

    # second descent
    ax.annotate("second descent\n(min-norm = implicit prior)",
                (ps[-1] * 0.62, risk[ps >= 2 * n].min()),
                textcoords="offset points", xytext=(-30, 70), color=GRN, fontsize=10.5,
                arrowprops=dict(arrowstyle="->", color=GRN, lw=1.2))

    ax.text(n * 0.5, risk.min() * 1.3, "underparameterized", color=DIM,
            fontsize=9.5, ha="center")
    ax.text(n * 4.0, risk.min() * 1.3, "overparameterized", color=DIM,
            fontsize=9.5, ha="center")

    ax.set_yscale("log")
    ax.set_xlabel("capacity  p   (number of random features used)  ->")
    ax.set_ylabel("test error  =  bias$^2$ + variance   (log scale)")
    ax.set_xticks([1, n, 2 * n, 4 * n, 6 * n, 8 * n])
    ax.set_xticklabels(["1", "n", "2n", "4n", "6n", "8n"])
    ax.set_xlim(0, 8 * n)
    ax.set_title(f"Double descent in a high-dim random-feature model "
                 f"(n={n}, D={DD_D})", color=WHITE, fontsize=12.5, pad=8)
    ax.legend(facecolor="#181820", edgecolor="#3a3a48", labelcolor="#dddddd",
              fontsize=9.5, loc="upper right")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"[part 3] wrote {outpath}")


# ============================================================================
# Main
# ============================================================================
def main():
    os.makedirs("images", exist_ok=True)
    key = jax.random.key(0)

    # --- Part 1: exercise the GenJAX generative model -----------------------
    demo = demo_generative_model(jax.random.fold_in(key, 1))

    # --- Part 2: bias-variance sweep ----------------------------------------
    degrees = np.arange(1, 13)
    bias2, variance, total = bias_variance_sweep(jax.random.fold_in(key, 2), degrees)
    print("[part 2] bias-variance decomposition (polynomial regression):")
    print("         deg   bias^2    variance   total")
    for d, b, v, t in zip(degrees, bias2, variance, total):
        print(f"         {d:>3}  {b:8.4f}  {v:9.4f}  {t:8.4f}")
    imin = int(np.argmin(total))
    print(f"         => lowest total error at degree {degrees[imin]} "
          f"(true f is a cubic; bias drops by degree 3, variance grows after)")
    plot_bias_variance(demo, degrees, bias2, variance, total,
                       "images/genjax_biasvariance.png")

    # --- Part 3: double descent ---------------------------------------------
    ps, risk, n = double_descent()
    peak_i = int(np.argmax(risk))
    print("[part 3] double descent (high-dim random features):")
    print(f"         test error @ p=1   : {risk[0]:.4f}   (underfit: high bias)")
    print(f"         test error @ p=n={n} : {risk[n - 1]:.2f}   (interpolation spike)")
    print(f"         peak is at p = {ps[peak_i]}  "
          f"(== n: confirms the spike sits at the interpolation threshold)")
    print(f"         test error @ p=8n={8 * n}: {risk[-1]:.4f}   "
          f"(second descent: error back below the p=1 underfit)")
    assert ps[peak_i] == n, "double-descent spike must sit exactly at p = n"
    assert risk[-1] < risk[n - 1], "expected a second descent below the spike"
    plot_double_descent(ps, risk, n, "images/genjax_double_descent.png")

    print("\nDone. Wrote images/genjax_biasvariance.png and "
          "images/genjax_double_descent.png")


if __name__ == "__main__":
    main()
