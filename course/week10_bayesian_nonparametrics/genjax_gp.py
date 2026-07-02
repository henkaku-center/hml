#!/usr/bin/env python3
"""Week 10 — GenJAX/JAX backbone for Gaussian Process (GP) regression in 1-D.

Dual-homed script:
  * generates the Week-10 lecture figure ``images/genjax_gp.png``;
  * is the verified code spine for the Phase-2 textbook chapter
    "Continuous Bayesian Nonparametrics".

A Gaussian process is a *prior over functions*: any finite set of function
values f(x_1), ..., f(x_n) is jointly Gaussian with mean m(x) and covariance
given by a kernel k(x, x'). Here we use a zero mean and the RBF (squared
exponential) kernel.

We do two things, the two halves of every GP picture:
  1. PRIOR  — draw whole functions from the GP *before seeing data*. We do this
     with a GenJAX ``@gen`` model using the **Cholesky trick**: draw iid
     standard-normal latents z ~ N(0, I) with ``genjax.normal`` and push them
     through f = mu + L z, where L is the Cholesky factor of the kernel matrix.
     The transformed vector f then has covariance L Lᵀ = K, i.e. it is a draw
     from the GP. (GenJAX *does* ship ``mv_normal``, but the Cholesky trick keeps
     us on the elementary scalar-``normal`` API and makes the math explicit —
     which is the point pedagogically.)
  2. POSTERIOR — condition on a few noisy observations. For a GP with Gaussian
     observation noise the posterior is available in *closed form* (no MCMC):
         K     = k(X, X) + sigma_n^2 I
         mean* = k(X*, X) K^{-1} y
         cov*  = k(X*, X*) - k(X*, X) K^{-1} k(X, X*)
     We solve the linear systems with a Cholesky factorization (``cho_factor`` /
     ``cho_solve``) for numerical stability, then sample posterior functions with
     the same Cholesky trick applied to cov*.

Run from ``course/week10_bayesian_nonparametrics/``::

    python3 genjax_gp.py

It runs on CPU (ignore the CUDA warning), prints a sanity check (the posterior
mean at the training inputs vs. the observed y), and writes ``images/genjax_gp.png``.
"""
from __future__ import annotations

import os

import jax
import jax.numpy as jnp
from jax.scipy.linalg import cho_factor, cho_solve

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from genjax import gen, normal

# --------------------------------------------------------------------------- #
# Dark SDS theme (mirrors make_figures.py so figures composite on the #111111  #
# deck background — light text, no white-on-white overflow).                   #
# --------------------------------------------------------------------------- #
BG = "#111111"; WHITE = "#ffffff"; DIM = "#999999"; ACC = "#64B5F6"; RED = "#EF5350"
ORA = "#FFA726"; GRN = "#66BB6A"; YEL = "#FFEB3B"; TEAL = "#4DD0E1"; PUR = "#BA68C8"
PRIOR_COLORS = [ACC, RED, GRN, ORA, PUR, TEAL]
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": WHITE, "axes.labelcolor": "#cfcfcf",
    "xtick.color": DIM, "ytick.color": DIM, "axes.edgecolor": "#3a3a48",
    "font.size": 12, "font.family": "DejaVu Sans",
})

# Model / data defaults (RBF kernel hyperparameters + observation noise).
SIG_F = 1.0      # signal std: prior marginal std of f(x) is sig_f
ELL = 0.15       # length-scale: how far a point's influence reaches
SIGMA_N = 0.1    # observation-noise std
JITTER = 1e-6    # tiny diagonal added before Cholesky for numerical stability


# --------------------------------------------------------------------------- #
# 1. RBF kernel                                                                #
# --------------------------------------------------------------------------- #
def rbf_kernel(xa: jnp.ndarray, xb: jnp.ndarray,
               sig_f: float = SIG_F, ell: float = ELL) -> jnp.ndarray:
    """RBF (squared-exponential) Gram matrix.

    k(x, x') = sig_f**2 * exp(-(x - x')**2 / (2 * ell**2))

    Args:
        xa: shape (na,) input locations.
        xb: shape (nb,) input locations.
        sig_f: signal standard deviation.
        ell: length-scale.

    Returns:
        Gram matrix of shape (na, nb).
    """
    d = xa[:, None] - xb[None, :]
    return (sig_f ** 2) * jnp.exp(-(d ** 2) / (2.0 * ell ** 2))


# --------------------------------------------------------------------------- #
# 2. True function + noisy training observations                              #
# --------------------------------------------------------------------------- #
def true_function(x: jnp.ndarray) -> jnp.ndarray:
    """A smooth 1-D test function on [0, 1]: f(x) = sin(2.5 pi x) * exp(-x)."""
    return jnp.sin(2.5 * jnp.pi * x) * jnp.exp(-x)


def make_training_data(key, n: int = 6, noise: float = SIGMA_N):
    """Draw n training inputs on [0, 1] with iid Gaussian observation noise.

    Returns:
        (X, y): inputs of shape (n,) and noisy targets of shape (n,).
    """
    k_x, k_eps = jax.random.split(key)
    # Spread inputs over [0.05, 0.95] with a little jitter so they are not on a
    # perfect grid (more realistic, and avoids a degenerate kernel matrix).
    base = jnp.linspace(0.05, 0.95, n)
    X = base + 0.02 * jax.random.normal(k_x, (n,))
    X = jnp.clip(X, 0.0, 1.0)
    y = true_function(X) + noise * jax.random.normal(k_eps, (n,))
    return X, y


# --------------------------------------------------------------------------- #
# 3. GenJAX GP PRIOR model (the Cholesky trick over iid normal latents)        #
# --------------------------------------------------------------------------- #
def make_gp_prior_model(n_grid: int):
    """Factory for a GenJAX GP-prior model over a grid of ``n_grid`` points.

    ``n_grid`` is captured as a Python constant (a closure), NOT passed as a
    model argument — a ``for i in range(n)`` over a *traced* argument raises
    ``TracerIntegerConversionError`` in GenJAX. The model draws ``n_grid`` iid
    standard normals z and returns f = mu + L @ z (the Cholesky trick), so the
    returned function values have covariance L Lᵀ = K.

    Args (to the returned ``@gen`` model):
        mu: shape (n_grid,) prior mean (zeros for a zero-mean GP).
        L:  shape (n_grid, n_grid) lower-Cholesky factor of the kernel matrix.

    Returns:
        A GenJAX generative function; ``.simulate(key, (mu, L)).get_retval()``
        is one GP prior sample of shape (n_grid,).
    """
    @gen
    def gp_prior(mu, L):
        # iid standard-normal latents, one addressed choice per grid point.
        zs = [normal(0.0, 1.0) @ f"z_{i}" for i in range(n_grid)]
        z = jnp.stack(zs)
        f = mu + L @ z          # correlate the latents -> a GP draw
        return f
    return gp_prior


def sample_prior_functions(key, grid, sig_f=SIG_F, ell=ELL,
                           n_samples: int = 5, jitter: float = JITTER):
    """Draw ``n_samples`` GP prior functions on ``grid`` via the GenJAX model.

    Returns:
        Array of shape (n_samples, len(grid)); each row is one prior function.
    """
    n = grid.shape[0]
    K = rbf_kernel(grid, grid, sig_f, ell) + jitter * jnp.eye(n)
    L = jnp.linalg.cholesky(K)
    mu = jnp.zeros(n)
    model = make_gp_prior_model(n)
    keys = jax.random.split(key, n_samples)
    # One .simulate per key -> one whole function each; vmap over the keys.
    fs = jax.vmap(lambda k: model.simulate(k, (mu, L)).get_retval())(keys)
    return fs


# --------------------------------------------------------------------------- #
# 4. GP POSTERIOR in closed form (JAX linear algebra)                          #
# --------------------------------------------------------------------------- #
def gp_posterior(X, y, Xstar, sig_f=SIG_F, ell=ELL, noise=SIGMA_N):
    """Closed-form GP posterior at test inputs ``Xstar`` given train ``(X, y)``.

        K     = k(X, X) + noise**2 I
        mean* = k(X*, X) K^{-1} y
        cov*  = k(X*, X*) - k(X*, X) K^{-1} k(X, X*)

    Solved via a Cholesky factorization of K for stability.

    Returns:
        (mean, cov, std): posterior mean (m,), covariance (m, m), and marginal
        std band sqrt(diag(cov)) (m,), where m = len(Xstar).
    """
    n = X.shape[0]
    Kxx = rbf_kernel(X, X, sig_f, ell) + (noise ** 2) * jnp.eye(n)
    Ksx = rbf_kernel(Xstar, X, sig_f, ell)          # (m, n)
    Kss = rbf_kernel(Xstar, Xstar, sig_f, ell)      # (m, m)

    c_and_lower = cho_factor(Kxx)                   # Cholesky of the train Gram
    alpha = cho_solve(c_and_lower, y)               # K^{-1} y          -> (n,)
    mean = Ksx @ alpha                              # k(X*,X) K^{-1} y  -> (m,)
    v = cho_solve(c_and_lower, Ksx.T)               # K^{-1} k(X,X*)    -> (n, m)
    cov = Kss - Ksx @ v                             # (m, m)
    std = jnp.sqrt(jnp.clip(jnp.diag(cov), 0.0, None))
    return mean, cov, std


def sample_posterior_functions(key, mean, cov, n_samples: int = 4,
                               jitter: float = 1e-8):
    """Draw posterior functions: f = mean + L_cov @ z, z ~ N(0, I).

    Same Cholesky trick as the prior, now using the *posterior* covariance.

    Returns:
        Array of shape (n_samples, len(mean)).
    """
    m = mean.shape[0]
    Lc = jnp.linalg.cholesky(cov + jitter * jnp.eye(m))
    z = jax.random.normal(key, (n_samples, m))
    return mean[None, :] + z @ Lc.T


# --------------------------------------------------------------------------- #
# 5. Figure                                                                    #
# --------------------------------------------------------------------------- #
def make_figure(grid, prior_samples, post_mean, post_std, post_samples,
                X, y, path="images/genjax_gp.png"):
    """Two-panel dark figure: (a) GP prior samples, (b) GP posterior."""
    fig, (axp, axo) = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True)

    # ---- Panel (a): PRIOR samples ----
    axp.fill_between(grid, -2 * SIG_F, 2 * SIG_F, color=ACC, alpha=0.08,
                     label="prior 2σ band")
    axp.axhline(0.0, color=DIM, lw=1.0, ls=":")
    for i, f in enumerate(prior_samples):
        axp.plot(grid, f, lw=1.7, alpha=0.9, color=PRIOR_COLORS[i % len(PRIOR_COLORS)])
    axp.set_title("Prior — functions before any data", color=WHITE, fontsize=12.5)
    axp.set_xlabel("input  x"); axp.set_ylabel("f(x)")
    axp.set_xlim(0, 1); axp.set_ylim(-3, 3)
    axp.legend(facecolor="#181820", edgecolor="#3a3a48", labelcolor="#dddddd",
               fontsize=9, loc="upper right")

    # ---- Panel (b): POSTERIOR mean + 2σ band + samples + data ----
    axo.fill_between(grid, post_mean - 2 * post_std, post_mean + 2 * post_std,
                     color=GRN, alpha=0.16, label="posterior 2σ band")
    for i, f in enumerate(post_samples):
        axo.plot(grid, f, lw=1.2, alpha=0.75, color=PRIOR_COLORS[i % len(PRIOR_COLORS)])
    axo.plot(grid, true_function(grid), color=DIM, lw=1.6, ls="--", label="true f(x)")
    axo.plot(grid, post_mean, color=WHITE, lw=2.6, label="posterior mean")
    axo.scatter(X, y, color=YEL, zorder=6, s=55, edgecolor="#222", linewidth=0.7,
                label="training data")
    axo.set_title("Posterior — functions must pass near the data",
                  color=WHITE, fontsize=12.5)
    axo.set_xlabel("input  x")
    axo.set_xlim(0, 1); axo.set_ylim(-3, 3)
    axo.legend(facecolor="#181820", edgecolor="#3a3a48", labelcolor="#dddddd",
               fontsize=9, loc="upper right")

    fig.suptitle("A Gaussian process is a prior over FUNCTIONS  "
                 "(RBF kernel, GenJAX prior + closed-form posterior)",
                 color=WHITE, fontsize=13.5, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# --------------------------------------------------------------------------- #
# 6. Main                                                                      #
# --------------------------------------------------------------------------- #
def main():
    key = jax.random.key(0)
    k_data, k_prior, k_post = jax.random.split(key, 3)

    # Dense grid of test inputs (used for both prior and posterior).
    grid = jnp.linspace(0.0, 1.0, 120)

    # Training data: ~6 noisy observations of the true function.
    X, y = make_training_data(k_data, n=6, noise=SIGMA_N)

    # ---- PRIOR: several GP samples from the GenJAX @gen model ----
    prior_samples = sample_prior_functions(k_prior, grid, n_samples=5)

    # ---- POSTERIOR: closed form on the dense grid + a few samples ----
    post_mean, post_cov, post_std = gp_posterior(X, y, grid)
    post_samples = sample_posterior_functions(k_post, post_mean, post_cov,
                                              n_samples=4)

    # ---- SANITY CHECK: posterior mean at the TRAINING inputs vs observed y ----
    # With Gaussian noise the GP smooths rather than exactly interpolating, so
    # the mean at the data should match y up to ~the noise level.
    mean_at_train, _, _ = gp_posterior(X, y, X)
    resid = jnp.abs(mean_at_train - y)

    print("=" * 64)
    print("GP regression — GenJAX prior + closed-form posterior")
    print("=" * 64)
    print(f"kernel: RBF   sig_f={SIG_F}  ell={ELL}   noise sigma_n={SIGMA_N}")
    print(f"prior samples drawn from GenJAX @gen model: "
          f"{prior_samples.shape[0]} functions x {prior_samples.shape[1]} grid pts")
    print()
    print("Posterior mean at training inputs vs. observed y:")
    print(f"  {'x':>8} {'y (obs)':>10} {'post mean':>10} {'|diff|':>9}")
    for xi, yi, mi, ri in zip(X, y, mean_at_train, resid):
        print(f"  {float(xi):8.3f} {float(yi):10.3f} {float(mi):10.3f} {float(ri):9.4f}")
    max_resid = float(jnp.max(resid))
    print()
    print(f"max |post_mean - y| at train points = {max_resid:.4f}")
    print(f"observation-noise std sigma_n        = {SIGMA_N:.4f}")
    ok = max_resid < 3.0 * SIGMA_N
    print(f"GP interpolates data up to noise (max resid < 3*sigma_n)? "
          f"{'PASS' if ok else 'FAIL'}")

    # ---- FIGURE ----
    path = make_figure(grid, prior_samples, post_mean, post_std, post_samples,
                       X, y)
    print()
    print(f"wrote figure: {path}")
    print("done.")
    return ok


if __name__ == "__main__":
    main()
