#!/usr/bin/env python3
"""Pre-generate matplotlib PNGs used by the Week 2 deck.

Run this once (or any time you tweak figure parameters). The build script
embeds the PNGs into pptx slides via SDSDeck.content_image_slide().

Output directory: ./images/
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"
IMG_DIR.mkdir(exist_ok=True)

# ---- Theme (matches SDSDeck dark palette) ----
BG = "#111111"
TEXT = "#ffffff"
DIM = "#999999"
ACCENT = "#64B5F6"     # blue
TONK = "#FFA726"       # orange for tonkatsu
HAMB = "#66BB6A"       # green for hamburger
POST = "#FFEB3B"       # yellow for posteriors
PRIOR = "#EF5350"      # red for prior
LIKE = "#64B5F6"       # blue for likelihood

plt.rcParams.update({
    "axes.facecolor": BG,
    "figure.facecolor": BG,
    "axes.edgecolor": DIM,
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "axes.titlecolor": TEXT,
    "font.size": 13,
    "axes.grid": True,
    "grid.color": "#333333",
    "grid.linewidth": 0.5,
})


def gaussian(x, mu, sigma):
    return (1.0 / np.sqrt(2 * np.pi) / sigma) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def save(fig, name):
    out = IMG_DIR / name
    fig.tight_layout()
    fig.savefig(out, dpi=180, facecolor=BG)
    plt.close(fig)
    print(f"  wrote {out.relative_to(HERE)}")


# ============================================================
# 1. PMF → PDF: shrinking bins on a weight histogram
# ============================================================

def fig_pmf_to_pdf():
    rng = np.random.default_rng(0)
    # Pretend: tonkatsu weights, ~N(500, 30)
    data = rng.normal(500, 30, 5000)
    x = np.linspace(380, 620, 400)
    pdf = gaussian(x, 500, 30)

    # Triptych — used on the "all three panels" slide (4/4).
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=False)
    for ax, bw, title in zip(axes, [30, 10, 2],
                             ["Bin width = 30g", "Bin width = 10g", "Bin width = 2g"]):
        ax.hist(data, bins=np.arange(380, 621, bw),
                density=True, color=TONK, alpha=0.75, edgecolor=BG)
        ax.plot(x, pdf, color=ACCENT, linewidth=2.2, label="limit: PDF")
        ax.set_title(title, color=TEXT)
        ax.set_xlabel("weight (g)")
        ax.set_xlim(380, 620)
    axes[0].set_ylabel("probability per gram")
    axes[-1].legend(loc="upper right", facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    save(fig, "pmf_to_pdf.png")

    # Single-panel variants — used on the step-by-step build slides.
    # Panel for 30g bins shows histogram ONLY (no PDF limit curve yet);
    # 10g adds the faint limit curve; 2g is the full "approaching the PDF" view.
    for bw, title, fname, show_pdf in [
        (30, "Bin width = 30g  (coarse — looks like a PMF)", "pmf_to_pdf_30g.png", False),
        (10, "Bin width = 10g  (finer — still a PMF)",       "pmf_to_pdf_10g.png", False),
        (2,  "Bin width = 2g  (fine — approaching the density)", "pmf_to_pdf_2g.png",  True),
    ]:
        fig, ax = plt.subplots(figsize=(9, 3.2))
        ax.hist(data, bins=np.arange(380, 621, bw),
                density=True, color=TONK, alpha=0.8, edgecolor=BG)
        if show_pdf:
            ax.plot(x, pdf, color=ACCENT, linewidth=2.4, label="limit: PDF")
            ax.legend(loc="upper right", facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
        ax.set_title(title, color=TEXT)
        ax.set_xlabel("weight (g)")
        ax.set_ylabel("probability per gram")
        ax.set_xlim(380, 620)
        save(fig, fname)


# ============================================================
# 2. Gaussian shape: peak, ±σ, ±2σ annotations
# ============================================================

def fig_gaussian_shape():
    mu, sigma = 500, 30
    x = np.linspace(380, 620, 400)
    y = gaussian(x, mu, sigma)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(x, y, color=ACCENT, linewidth=2.5)
    ax.fill_between(x, 0, y, where=(x >= mu - sigma) & (x <= mu + sigma),
                    color=ACCENT, alpha=0.25, label="±1σ  (~68%)")
    ax.fill_between(x, 0, y, where=((x >= mu - 2 * sigma) & (x <= mu - sigma))
                                   | ((x <= mu + 2 * sigma) & (x >= mu + sigma)),
                    color=ACCENT, alpha=0.12, label="±2σ  (~95%)")
    peak = gaussian(mu, mu, sigma)
    ax.axvline(mu, color=POST, linestyle="--", linewidth=1.5)
    ax.annotate(f"peak at μ = {mu}\n  height = 1/√(2π σ²) ≈ {peak:.4f}",
                xy=(mu, peak), xytext=(mu + 15, peak * 0.9),
                color=POST, fontsize=12)
    ax.set_xlabel("weight (g)")
    ax.set_ylabel("density  f(x)")
    ax.set_title("The Gaussian  N(x | μ=500, σ=30)", color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    save(fig, "gaussian_shape.png")


# ============================================================
# 3. Tonkatsu vs. hamburger weight likelihoods
# ============================================================

def fig_tonk_hamb_likelihoods():
    x = np.linspace(240, 620, 500)
    y_t = gaussian(x, 500, 30)
    y_h = gaussian(x, 350, 30)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.fill_between(x, 0, y_t, color=TONK, alpha=0.4)
    ax.fill_between(x, 0, y_h, color=HAMB, alpha=0.4)
    ax.plot(x, y_t, color=TONK, linewidth=2.5, label="tonkatsu ~ N(500, 30²)")
    ax.plot(x, y_h, color=HAMB, linewidth=2.5, label="hamburger ~ N(350, 30²)")
    ax.axvline(450, color=POST, linestyle="--", linewidth=1.5, label="observed 450g")
    ax.set_xlabel("weight (g)")
    ax.set_ylabel("density")
    ax.set_title("Two Gaussian likelihoods — they overlap in the middle", color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT, loc="upper left")
    save(fig, "tonk_hamb.png")


# ============================================================
# 4. Precision = 1/variance: sharp vs. broad Gaussians
# ============================================================

def fig_precision():
    x = np.linspace(400, 600, 500)
    sharp = gaussian(x, 500, 10)
    broad = gaussian(x, 500, 30)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(x, sharp, color=ACCENT, linewidth=2.5,
            label="σ = 10   →   precision 1/100 = 0.0100  (CONFIDENT)")
    ax.plot(x, broad, color=TONK, linewidth=2.5,
            label="σ = 30   →   precision 1/900 ≈ 0.0011  (UNCERTAIN)")
    ax.set_xlabel("μ")
    ax.set_ylabel("density")
    ax.set_title("Precision  =  1 / variance  =  \"how sharp I am\"", color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    save(fig, "precision.png")


# ============================================================
# 5. Gaussian-Gaussian update: prior × likelihood → posterior
# ============================================================

def fig_gg_update():
    mu0, s0 = 500, 20    # prior
    sigma = 30            # data noise
    D1 = 510              # observation
    # Posterior: precisions add
    post_prec = 1 / s0 ** 2 + 1 / sigma ** 2
    post_var = 1 / post_prec
    post_mu = post_var * (mu0 / s0 ** 2 + D1 / sigma ** 2)
    post_sigma = np.sqrt(post_var)

    x = np.linspace(420, 580, 500)
    prior = gaussian(x, mu0, s0)
    # Likelihood as a function of μ, evaluated at data D1 with std sigma
    likelihood = gaussian(x, D1, sigma)
    posterior = gaussian(x, post_mu, post_sigma)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(x, prior, color=PRIOR, linewidth=2.5,
            label=f"prior   N({mu0}, {s0}²)")
    ax.plot(x, likelihood, color=LIKE, linewidth=2.5,
            label=f"likelihood  (data D={D1}, σ={sigma})")
    ax.plot(x, posterior, color=POST, linewidth=3.0,
            label=f"posterior  N({post_mu:.1f}, {post_sigma:.1f}²)")
    ax.fill_between(x, 0, posterior, color=POST, alpha=0.22)
    ax.axvline(mu0, color=PRIOR, alpha=0.5, linestyle=":")
    ax.axvline(D1, color=LIKE, alpha=0.5, linestyle=":")
    ax.axvline(post_mu, color=POST, alpha=0.8, linestyle="--")
    ax.set_xlabel("μ  (the hidden mean of tonkatsu weight)")
    ax.set_ylabel("density")
    ax.set_title("Gaussian × Gaussian = Gaussian  (conjugacy)", color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT, loc="upper right")
    save(fig, "gg_update.png")
    return post_mu, post_sigma


# ============================================================
# 6. Binomial PMF (real bar chart, not ASCII)
# ============================================================

def fig_binomial_pmf():
    from math import comb
    n, p = 5, 0.7
    ks = np.arange(n + 1)
    pmf = np.array([comb(n, k) * p ** k * (1 - p) ** (n - k) for k in ks])
    fig, ax = plt.subplots(figsize=(10, 4.3))
    colors = [ACCENT if k == pmf.argmax() else TONK for k in ks]
    bars = ax.bar(ks, pmf, color=colors, edgecolor=BG)
    for k, bar, val in zip(ks, bars, pmf):
        ax.text(k, val + 0.008, f"{val:.3f}", ha="center", color=TEXT, fontsize=11)
    ax.set_xlabel("k  (number of tonkatsu in 5 days)")
    ax.set_ylabel("P(Y = k)")
    ax.set_title("Binomial(n=5, p=0.7)  —  Chibany's week of bentos", color=TEXT)
    ax.set_ylim(0, pmf.max() * 1.18)
    save(fig, "binomial_pmf.png")


if __name__ == "__main__":
    print("Generating Week 2 figure assets...")
    fig_pmf_to_pdf()
    fig_gaussian_shape()
    fig_tonk_hamb_likelihoods()
    fig_precision()
    post_mu, post_sigma = fig_gg_update()
    fig_binomial_pmf()
    print(f"\nGG-update posterior: N({post_mu:.3f}, {post_sigma:.3f}²)")
