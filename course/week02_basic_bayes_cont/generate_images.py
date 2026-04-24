#!/usr/bin/env python3
"""Pre-generate matplotlib PNGs used by the Week 2 deck.

Run this once (or any time you tweak figure parameters). The build script
embeds the PNGs into pptx slides via SDSDeck.content_image_slide().

Output directory: ./images/

For each figure, TWO PNGs are produced:
  <name>.png     — English titles/labels/legend
  <name>-ja.png  — Japanese titles/labels/legend (uses Noto Sans CJK JP)

The slide deck references both via paired .lang-en / .lang-ja divs so the
bilingual toggle swaps the image, not just the prose.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
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

BASE_RCPARAMS = {
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
}
plt.rcParams.update(BASE_RCPARAMS)

# Pick a Japanese-capable font family if available on the system.
def _detect_ja_font():
    for candidate in (
        "Noto Sans CJK JP", "Noto Serif CJK JP",
        "Hiragino Sans", "Yu Gothic", "Meiryo",
    ):
        if any(f.name == candidate for f in font_manager.fontManager.ttflist):
            return candidate
    # Fallback: matplotlib's default; JA characters may render as tofu.
    return None

JA_FONT = _detect_ja_font()


def gaussian(x, mu, sigma):
    return (1.0 / np.sqrt(2 * np.pi) / sigma) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def save(fig, name):
    out = IMG_DIR / name
    fig.tight_layout()
    fig.savefig(out, dpi=180, facecolor=BG)
    plt.close(fig)
    print(f"  wrote {out.relative_to(HERE)}")


def _with_ja_font(rc=None):
    """Context to render a figure using the Japanese font family."""
    class _Ctx:
        def __enter__(self):
            self._prev = dict(plt.rcParams)
            plt.rcParams.update(BASE_RCPARAMS)
            if JA_FONT:
                plt.rcParams["font.family"] = JA_FONT
            if rc:
                plt.rcParams.update(rc)
        def __exit__(self, *a):
            plt.rcParams.update(self._prev)
    return _Ctx()


# ============================================================
# 1. PMF → PDF: shrinking bins on a weight histogram
# ============================================================

def _draw_pmf_to_pdf(panels, titles, xlabel, ylabel, legend_label, fname):
    rng = np.random.default_rng(0)
    data = rng.normal(500, 30, 5000)
    x = np.linspace(380, 620, 400)
    pdf = gaussian(x, 500, 30)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=False)
    for ax, bw, title in zip(axes, panels, titles):
        ax.hist(data, bins=np.arange(380, 621, bw),
                density=True, color=TONK, alpha=0.75, edgecolor=BG)
        ax.plot(x, pdf, color=ACCENT, linewidth=2.2, label=legend_label)
        ax.set_title(title, color=TEXT)
        ax.set_xlabel(xlabel)
        ax.set_xlim(380, 620)
    axes[0].set_ylabel(ylabel)
    axes[-1].legend(loc="upper right", facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    save(fig, fname)


def _draw_pmf_to_pdf_single(bw, title, show_pdf, legend_label, xlabel, ylabel, fname):
    rng = np.random.default_rng(0)
    data = rng.normal(500, 30, 5000)
    x = np.linspace(380, 620, 400)
    pdf = gaussian(x, 500, 30)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.hist(data, bins=np.arange(380, 621, bw),
            density=True, color=TONK, alpha=0.8, edgecolor=BG)
    if show_pdf:
        ax.plot(x, pdf, color=ACCENT, linewidth=2.4, label=legend_label)
        ax.legend(loc="upper right", facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    ax.set_title(title, color=TEXT)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(380, 620)
    save(fig, fname)


def fig_pmf_to_pdf():
    # EN triptych
    _draw_pmf_to_pdf(
        panels=[30, 10, 2],
        titles=["Bin width = 30g", "Bin width = 10g", "Bin width = 2g"],
        xlabel="weight (g)",
        ylabel="probability per gram",
        legend_label="limit: PDF",
        fname="pmf_to_pdf.png",
    )
    # JA triptych
    with _with_ja_font():
        _draw_pmf_to_pdf(
            panels=[30, 10, 2],
            titles=["区間幅 = 30g", "区間幅 = 10g", "区間幅 = 2g"],
            xlabel="重さ (g)",
            ylabel="1gあたりの確率",
            legend_label="極限：PDF",
            fname="pmf_to_pdf-ja.png",
        )
    # EN single-panel builds
    for bw, title, fname, show_pdf in [
        (30, "Bin width = 30g  (coarse — looks like a PMF)", "pmf_to_pdf_30g.png", False),
        (10, "Bin width = 10g  (finer — still a PMF)",       "pmf_to_pdf_10g.png", False),
        (2,  "Bin width = 2g  (fine — approaching the density)", "pmf_to_pdf_2g.png",  True),
    ]:
        _draw_pmf_to_pdf_single(
            bw, title, show_pdf,
            legend_label="limit: PDF",
            xlabel="weight (g)", ylabel="probability per gram",
            fname=fname,
        )
    # JA single-panel builds
    with _with_ja_font():
        for bw, title, fname, show_pdf in [
            (30, "区間幅 = 30g  （粗い — PMFのように見える）", "pmf_to_pdf_30g-ja.png", False),
            (10, "区間幅 = 10g  （より細かい — まだPMF）",     "pmf_to_pdf_10g-ja.png", False),
            (2,  "区間幅 = 2g  （細かい — 密度に近づく）",      "pmf_to_pdf_2g-ja.png",  True),
        ]:
            _draw_pmf_to_pdf_single(
                bw, title, show_pdf,
                legend_label="極限：PDF",
                xlabel="重さ (g)", ylabel="1gあたりの確率",
                fname=fname,
            )


# ============================================================
# 2. Gaussian shape: peak, ±σ, ±2σ annotations
# ============================================================

def _draw_gaussian_shape(title, xlabel, ylabel,
                         band1, band2, peak_label_fn, fname):
    mu, sigma = 500, 30
    x = np.linspace(380, 620, 400)
    y = gaussian(x, mu, sigma)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(x, y, color=ACCENT, linewidth=2.5)
    ax.fill_between(x, 0, y, where=(x >= mu - sigma) & (x <= mu + sigma),
                    color=ACCENT, alpha=0.25, label=band1)
    ax.fill_between(x, 0, y, where=((x >= mu - 2 * sigma) & (x <= mu - sigma))
                                   | ((x <= mu + 2 * sigma) & (x >= mu + sigma)),
                    color=ACCENT, alpha=0.12, label=band2)
    peak = gaussian(mu, mu, sigma)
    ax.axvline(mu, color=POST, linestyle="--", linewidth=1.5)
    ax.annotate(peak_label_fn(mu, peak),
                xy=(mu, peak), xytext=(mu + 15, peak * 0.9),
                color=POST, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    save(fig, fname)


def fig_gaussian_shape():
    _draw_gaussian_shape(
        title="The Gaussian  N(x | μ=500, σ=30)",
        xlabel="weight (g)", ylabel="density  f(x)",
        band1="±1σ  (~68%)", band2="±2σ  (~95%)",
        peak_label_fn=lambda mu, peak: f"peak at μ = {mu}\n  height = 1/√(2π σ²) ≈ {peak:.4f}",
        fname="gaussian_shape.png",
    )
    with _with_ja_font():
        _draw_gaussian_shape(
            title="ガウス分布  N(x | μ=500, σ=30)",
            xlabel="重さ (g)", ylabel="密度  f(x)",
            band1="±1σ  （~68%）", band2="±2σ  （~95%）",
            peak_label_fn=lambda mu, peak: f"μ = {mu} でピーク\n  高さ = 1/√(2π σ²) ≈ {peak:.4f}",
            fname="gaussian_shape-ja.png",
        )


# ============================================================
# 3. Tonkatsu vs. hamburger weight likelihoods
# ============================================================

def _draw_tonk_hamb(title, xlabel, ylabel, tonk_label, hamb_label, obs_label, fname):
    x = np.linspace(240, 620, 500)
    y_t = gaussian(x, 500, 30)
    y_h = gaussian(x, 350, 30)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.fill_between(x, 0, y_t, color=TONK, alpha=0.4)
    ax.fill_between(x, 0, y_h, color=HAMB, alpha=0.4)
    ax.plot(x, y_t, color=TONK, linewidth=2.5, label=tonk_label)
    ax.plot(x, y_h, color=HAMB, linewidth=2.5, label=hamb_label)
    ax.axvline(450, color=POST, linestyle="--", linewidth=1.5, label=obs_label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT, loc="upper left")
    save(fig, fname)


def fig_tonk_hamb_likelihoods():
    _draw_tonk_hamb(
        title="Two Gaussian likelihoods — they overlap in the middle",
        xlabel="weight (g)", ylabel="density",
        tonk_label="tonkatsu ~ N(500, 30²)",
        hamb_label="hamburger ~ N(350, 30²)",
        obs_label="observed 450g",
        fname="tonk_hamb.png",
    )
    with _with_ja_font():
        _draw_tonk_hamb(
            title="2つのガウス尤度 — 真ん中で重なる",
            xlabel="重さ (g)", ylabel="密度",
            tonk_label="とんかつ ~ N(500, 30²)",
            hamb_label="ハンバーグ ~ N(350, 30²)",
            obs_label="観測値 450g",
            fname="tonk_hamb-ja.png",
        )


# ============================================================
# 4. Precision = 1/variance: sharp vs. broad Gaussians
# ============================================================

def _draw_precision(title, xlabel, ylabel, sharp_label, broad_label, fname):
    x = np.linspace(400, 600, 500)
    sharp = gaussian(x, 500, 10)
    broad = gaussian(x, 500, 30)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(x, sharp, color=ACCENT, linewidth=2.5, label=sharp_label)
    ax.plot(x, broad, color=TONK, linewidth=2.5, label=broad_label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT)
    save(fig, fname)


def fig_precision():
    _draw_precision(
        title="Precision  =  1 / variance  =  \"how sharp I am\"",
        xlabel="μ", ylabel="density",
        sharp_label="σ = 10   →   precision 1/100 = 0.0100  (CONFIDENT)",
        broad_label="σ = 30   →   precision 1/900 ≈ 0.0011  (UNCERTAIN)",
        fname="precision.png",
    )
    with _with_ja_font():
        _draw_precision(
            title="精度  =  1 / 分散  =  「どれくらい鋭いか」",
            xlabel="μ", ylabel="密度",
            sharp_label="σ = 10   →   精度 1/100 = 0.0100  （自信あり）",
            broad_label="σ = 30   →   精度 1/900 ≈ 0.0011  （不確実）",
            fname="precision-ja.png",
        )


# ============================================================
# 5. Gaussian-Gaussian update: prior × likelihood → posterior
# ============================================================

def _draw_gg_update(title, xlabel, ylabel,
                    prior_label_fn, like_label_fn, post_label_fn, fname,
                    mu0=500, s0=20, sigma=30, D1=510):
    # Posterior: precisions add
    post_prec = 1 / s0 ** 2 + 1 / sigma ** 2
    post_var = 1 / post_prec
    post_mu = post_var * (mu0 / s0 ** 2 + D1 / sigma ** 2)
    post_sigma = np.sqrt(post_var)

    x = np.linspace(420, 580, 500)
    prior = gaussian(x, mu0, s0)
    likelihood = gaussian(x, D1, sigma)
    posterior = gaussian(x, post_mu, post_sigma)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(x, prior, color=PRIOR, linewidth=2.5, label=prior_label_fn(mu0, s0))
    ax.plot(x, likelihood, color=LIKE, linewidth=2.5, label=like_label_fn(D1, sigma))
    ax.plot(x, posterior, color=POST, linewidth=3.0, label=post_label_fn(post_mu, post_sigma))
    ax.fill_between(x, 0, posterior, color=POST, alpha=0.22)
    ax.axvline(mu0, color=PRIOR, alpha=0.5, linestyle=":")
    ax.axvline(D1, color=LIKE, alpha=0.5, linestyle=":")
    ax.axvline(post_mu, color=POST, alpha=0.8, linestyle="--")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, color=TEXT)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=TEXT, loc="upper right")
    save(fig, fname)
    return post_mu, post_sigma


def fig_gg_update():
    post_mu, post_sigma = _draw_gg_update(
        title="Gaussian × Gaussian = Gaussian  (conjugacy)",
        xlabel="μ  (the hidden mean of tonkatsu weight)", ylabel="density",
        prior_label_fn=lambda mu0, s0: f"prior   N({mu0}, {s0}²)",
        like_label_fn=lambda D1, sig: f"likelihood  (data D={D1}, σ={sig})",
        post_label_fn=lambda pm, ps: f"posterior  N({pm:.1f}, {ps:.1f}²)",
        fname="gg_update.png",
    )
    with _with_ja_font():
        _draw_gg_update(
            title="ガウス × ガウス = ガウス  （共役性）",
            xlabel="μ  （とんかつの重さの隠れた平均）", ylabel="密度",
            prior_label_fn=lambda mu0, s0: f"事前分布   N({mu0}, {s0}²)",
            like_label_fn=lambda D1, sig: f"尤度  （データ D={D1}, σ={sig}）",
            post_label_fn=lambda pm, ps: f"事後分布  N({pm:.1f}, {ps:.1f}²)",
            fname="gg_update-ja.png",
        )
    return post_mu, post_sigma


# ============================================================
# 6. Binomial PMF (real bar chart, not ASCII)
# ============================================================

def _draw_binomial_pmf(title, xlabel, ylabel, fname):
    from math import comb
    n, p = 5, 0.7
    ks = np.arange(n + 1)
    pmf = np.array([comb(n, k) * p ** k * (1 - p) ** (n - k) for k in ks])
    fig, ax = plt.subplots(figsize=(10, 4.3))
    colors = [ACCENT if k == pmf.argmax() else TONK for k in ks]
    bars = ax.bar(ks, pmf, color=colors, edgecolor=BG)
    for k, bar, val in zip(ks, bars, pmf):
        ax.text(k, val + 0.008, f"{val:.3f}", ha="center", color=TEXT, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, color=TEXT)
    ax.set_ylim(0, pmf.max() * 1.18)
    save(fig, fname)


def fig_binomial_pmf():
    _draw_binomial_pmf(
        title="Binomial(n=5, p=0.7)  —  Chibany's week of bentos",
        xlabel="k  (number of tonkatsu in 5 days)", ylabel="P(Y = k)",
        fname="binomial_pmf.png",
    )
    with _with_ja_font():
        _draw_binomial_pmf(
            title="二項分布 Binomial(n=5, p=0.7)  —  チバニーの一週間",
            xlabel="k  （5日間でとんかつが出た回数）", ylabel="P(Y = k)",
            fname="binomial_pmf-ja.png",
        )


if __name__ == "__main__":
    print(f"Generating Week 2 figure assets... (JA font: {JA_FONT or 'NONE — tofu likely'})")
    fig_pmf_to_pdf()
    fig_gaussian_shape()
    fig_tonk_hamb_likelihoods()
    fig_precision()
    post_mu, post_sigma = fig_gg_update()
    fig_binomial_pmf()
    print(f"\nGG-update posterior: N({post_mu:.3f}, {post_sigma:.3f}²)")
