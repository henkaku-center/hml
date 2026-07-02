"""
GenJAX backbone — Dirichlet Process Mixture Model (DPMM) on Chibany bento weights.

Week-10 (Human & Machine Learning) lecture backbone, dual-homed for the Phase-2
textbook "Discrete Bayesian Nonparametrics" chapter. Two halves:

  (A) the GENERATIVE model in GenJAX (@gen, stick-breaking) — a prior over
      partitions + Gaussian clusters; `.simulate` draws a synthetic dataset.
  (B) posterior INFERENCE — a slice-sampled Gibbs sampler (JAX) that infers, from
      the observed bento weights, HOW MANY clusters there are and where they sit.

The point of the week: "how complex should the model be? — let the data decide."
The DPMM never fixes K; the sampler grows clusters as the data demand them (here a
275 g outlier gets its own table on top of the Hamburger ~350 g / Tonkatsu ~500 g
modes).

Run:  python3 genjax_dpmm.py
Needs jax 0.5.3 / genjax 0.10.3 (CPU is fine — ignore the CUDA warning).
The Gibbs machinery is the validated backbone from textbook intro2/06_dpmm.md.
"""
import os
from functools import partial
from collections import Counter

import numpy as np
import jax
import jax.numpy as jnp
import jax.random as random
from genjax import gen, beta, normal, categorical

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- dark theme, matching make_figures.py ----
BG = "#111111"; WHITE = "#ffffff"; DIM = "#999999"
ACC = "#64B5F6"; PUR = "#BA68C8"; YEL = "#FFEB3B"; ORA = "#FFA726"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": WHITE, "axes.labelcolor": "#cfcfcf",
    "xtick.color": DIM, "ytick.color": DIM, "axes.edgecolor": "#3a3a48",
    "font.size": 12, "font.family": "DejaVu Sans",
})
os.makedirs("images", exist_ok=True)

# ===== Hyperparameters (bento weights, in grams) =====
ALPHA = 1.0     # concentration: how eagerly to open new tables
MU0   = 425.0   # prior mean for a cluster's mean weight
SIG0  = 80.0    # prior spread of cluster means
SIGX  = 22.0    # within-cluster observation noise
KMAX  = 12      # truncation / storage bound (the slice decides how many are live)


# ============== (A) GENERATIVE MODEL — GenJAX ==============
def make_dpmm_model(K, N):
    """Factory: K (truncation) and N (n obs) are closures, not traced args
    (avoids TracerIntegerConversionError on `range(K)` / `range(N)`)."""
    @gen
    def dpmm_model(alpha, mu0, sig0, sigx):
        # stick-breaking: beta_k ~ Beta(1, alpha) -> mixing weights pi_k
        betas = [beta(1.0, alpha) @ f"beta_{k}" for k in range(K)]
        pis, remaining = [], 1.0
        for k in range(K):
            pis.append(betas[k] * remaining)
            remaining = remaining * (1.0 - betas[k])
        pis = jnp.maximum(jnp.array(pis), 1e-6)
        pis = pis / jnp.sum(pis)
        # each table gets a Gaussian center theta_k ~ N(mu0, sig0)
        mus = jnp.array([normal(mu0, sig0) @ f"mu_{k}" for k in range(K)])
        # each diner picks a table, then a weight from that table's Gaussian
        xs = []
        for i in range(N):
            z_i = categorical(pis) @ f"z_{i}"
            xs.append(normal(mus[z_i], sigx) @ f"x_{i}")
        return {"pis": pis, "mus": mus, "xs": jnp.array(xs)}
    return dpmm_model


# ============== (B) INFERENCE — slice-sampled Gibbs (JAX) ==============
def stick_break(betas):
    """betas (K,) -> mixing weights pis (K,): pi_k = beta_k * prod_{j<k}(1-beta_j)."""
    log1m = jnp.log1p(-betas)
    cum = jnp.concatenate([jnp.zeros(1), jnp.cumsum(log1m)[:-1]])
    return betas * jnp.exp(cum)


def normal_logpdf(x, mu, sig):
    return -0.5 * jnp.log(2 * jnp.pi * sig**2) - 0.5 * ((x - mu) / sig)**2


def sample_betas(key, z, alpha, K):
    """Stick-breaking posterior: beta_k ~ Beta(1 + n_k, alpha + sum_{j>k} n_j)."""
    counts = jnp.bincount(z, length=K)
    after = jnp.cumsum(counts[::-1])[::-1]
    after = jnp.concatenate([after[1:], jnp.zeros(1)])
    keys = random.split(key, K)
    betas = jax.vmap(lambda k, a, b: jax.random.beta(k, a, b))(keys, 1.0 + counts, alpha + after)
    return jnp.clip(betas, 1e-6, 1 - 1e-6)


def sample_mus(key, x, z, K, mu0, sig0, sigx):
    """Conjugate Normal-Normal posterior for each cluster mean (empty -> prior)."""
    counts = jnp.bincount(z, length=K)
    sums = jnp.zeros(K).at[z].add(x)
    prec0, precx = 1.0 / sig0**2, 1.0 / sigx**2
    post_prec = prec0 + counts * precx
    post_mean = (prec0 * mu0 + precx * sums) / post_prec
    post_std = jnp.sqrt(1.0 / post_prec)
    eps = jax.vmap(lambda k: jax.random.normal(k))(random.split(key, K))
    return post_mean + post_std * eps


@partial(jax.jit, static_argnums=(2,))
def gibbs_sweep(key, state, K, x, alpha, mu0, sig0, sigx):
    z, betas, mus = state
    k1, k2, k3, k4 = random.split(key, 4)
    pis = stick_break(betas)
    # 1. slice variables u_i ~ Uniform(0, pi_{z_i}) — caps how many tables are live
    u = jax.random.uniform(k1, (x.shape[0],)) * pis[z]
    # 2. assignments: P(z_i=k) propto 1[pi_k > u_i] * N(x_i | mu_k, sigx)
    loglik = normal_logpdf(x[:, None], mus[None, :], sigx)
    logp = jnp.where(pis[None, :] > u[:, None], loglik, -jnp.inf)
    keys = random.split(k2, x.shape[0])
    z = jax.vmap(lambda k, lp: jax.random.categorical(k, lp))(keys, logp)
    # 3. stick weights, 4. cluster means
    betas = sample_betas(k3, z, alpha, K)
    mus = sample_mus(k4, x, z, K, mu0, sig0, sigx)
    return (z, betas, mus)


def run_sampler(x, n_sweeps=400, burn=150, seed=0):
    """Slice-sampled Gibbs. Returns (post-burn z samples, post-burn (betas,mus), final state)."""
    key = random.PRNGKey(seed)
    N = x.shape[0]
    z = jnp.zeros(N, dtype=jnp.int32)               # init: everyone at table 0
    key, kb, km = random.split(key, 3)
    betas = jnp.clip(jax.random.beta(kb, 1.0, ALPHA, (KMAX,)), 1e-6, 1 - 1e-6)
    mus = MU0 + SIG0 * jax.random.normal(km, (KMAX,))
    state = (z, betas, mus)
    z_hist, mb_hist = [], []
    for t in range(n_sweeps):
        key, sk = random.split(key)
        state = gibbs_sweep(sk, state, KMAX, x, ALPHA, MU0, SIG0, SIGX)
        if t >= burn:
            z_hist.append(state[0])
            mb_hist.append((state[1], state[2]))
    return jnp.stack(z_hist), mb_hist, state


# ============== data + run + figure ==============
def bento_data(seed=3):
    """8 Hamburger ~350 g, 6 Tonkatsu ~500 g, and one 275 g outlier."""
    rng = np.random.default_rng(seed)
    ham = rng.normal(350, 10, 8)
    ton = rng.normal(500, 11, 6)
    out = np.array([275.0])
    return jnp.array(np.concatenate([ham, ton, out]).astype(np.float32))


def predictive_density(grid, z_hist, mb_hist):
    """Sweep-averaged DPMM posterior predictive density on `grid`."""
    dens = np.zeros_like(grid)
    S = len(mb_hist)
    N = z_hist.shape[1]
    s0 = np.sqrt(SIG0**2 + SIGX**2)
    for s in range(S):
        _, mus = mb_hist[s]
        counts = np.bincount(np.array(z_hist[s]), minlength=KMAX)
        for k in range(KMAX):
            if counts[k] > 0:
                dens += counts[k] * np.exp(-0.5 * ((grid - float(mus[k])) / SIGX)**2) / (SIGX * np.sqrt(2 * np.pi))
        dens += ALPHA * np.exp(-0.5 * ((grid - MU0) / s0)**2) / (s0 * np.sqrt(2 * np.pi))  # new-table term
    return dens / (S * (N + ALPHA))


def main():
    # (A) forward GenJAX model — draw a synthetic dataset from the prior
    model = make_dpmm_model(K=KMAX, N=15)
    tr = model.simulate(random.PRNGKey(42), (ALPHA, MU0, SIG0, SIGX))
    syn = tr.get_retval()
    print("(A) GenJAX forward draw — synthetic weights (g):",
          np.round(np.array(syn["xs"]), 0).tolist())

    # (B) inference on the observed bento weights
    x = bento_data()
    print("(B) observed bento weights (g):", np.round(np.array(x), 0).tolist())
    z_hist, mb_hist, final = run_sampler(x)
    ks = [int(np.unique(np.array(z)).size) for z in z_hist]
    mode_k = Counter(ks).most_common(1)[0][0]
    print(f"    posterior #clusters: mode={mode_k}, mean={np.mean(ks):.2f}")
    # a representative post-burn sweep with the modal number of clusters
    rep = next((i for i, z in enumerate(z_hist)
                if int(np.unique(np.array(z)).size) == mode_k), len(z_hist) - 1)
    rep_mus = mb_hist[rep][1]
    rep_centers = sorted(float(rep_mus[k]) for k in np.unique(np.array(z_hist[rep])))
    print("    representative cluster means (g):", [round(c, 1) for c in rep_centers])

    # figure: data rug + sweep-averaged predictive density + discovered centers
    grid = np.linspace(220, 580, 400)
    dens = predictive_density(grid, z_hist, mb_hist)
    fig, ax = plt.subplots(figsize=(7.6, 4.9))
    ax.plot(grid, dens, color=ACC, lw=2.8, label="DPMM posterior predictive")
    for c in rep_centers:
        ax.axvline(c, color=PUR, ls="--", lw=1.4, alpha=0.75)
    ax.scatter(np.array(x), np.full(x.shape[0], -0.00035), marker="|", s=440,
               color=YEL, label="bento weights", clip_on=False, zorder=5)
    ax.tick_params(labelsize=12)
    ax.set_xlabel("bento weight (g)", fontsize=14)
    ax.set_ylabel("density", fontsize=14)
    ax.set_title(f"DPMM on bento weights — {mode_k} clusters",
                 color=WHITE, fontsize=15, pad=8)
    ax.legend(facecolor="#181820", edgecolor="#3a3a48", labelcolor="#dddddd",
              fontsize=11, loc="upper right")
    ax.set_ylim(bottom=-0.0010)
    fig.tight_layout()
    fig.savefig("images/genjax_dpmm.png", dpi=150)
    plt.close(fig)
    print("    wrote images/genjax_dpmm.png")


if __name__ == "__main__":
    main()
