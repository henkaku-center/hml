#!/usr/bin/env python3
"""Continuous concept learning — visualizations for Week 4 Block 5.

Dark-theme matplotlib figures for the rectangle-game (continuous concept
learning) section:

  cc_1d.png        — 1-D: a few observed points on a line, with candidate
                     interval hypotheses drawn at varying opacity = posterior
                     weight. Smaller intervals (tighter to the data) are
                     darker/heavier.

  cc_2d.png        — 2-D rectangle game: dots in a plane, candidate
                     axis-aligned rectangles at varying linewidth + grey level
                     (heavier/darker = larger posterior). r (data range), the
                     extension d, and n (number of dots) labelled on the plot.

  cc_exp_prior.png — the exponential prior over rectangle size: the density
                     p(s) = lambda * exp(-lambda * s) plotted, since this is
                     the first time the class meets the exponential
                     distribution.

  tg_results.png   — Tenenbaum & Griffiths (2001) experiment result:
                     d (extent of generalization) vs r (range spanned by the
                     n examples), one curve per n. Data eyeballed from the
                     published figure, same as build_zenith_plots.py does for
                     the G&T 2001 randomness figure.

Styling matches scripts/build_zenith_plots.py / build_shepard_plot.py.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch

BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"   # blue
YELLOW = "#FFEB3B"   # yellow — observed data
DIM = "#999999"
GREYS = ["#3A3A3A", "#5A5A5A", "#7E7E7E", "#A8A8A8", "#D6D6D6"]

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "course" / "week04_generalization_hier_bayes" / "images"
)


# --------------------------------------------------------------------------
# 1-D interval hypotheses
# --------------------------------------------------------------------------
def build_1d() -> None:
    fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    # observed points on the dimension
    data = np.array([3.4, 4.1, 4.8, 5.6])
    dlo, dhi = data.min(), data.max()

    # candidate intervals [l, u], each containing all the data. Smaller =
    # higher strong-sampling likelihood = higher posterior (flat prior).
    intervals = [
        (3.2, 5.8),    # snug
        (2.6, 6.3),
        (1.9, 7.0),
        (1.0, 8.1),
        (0.2, 9.2),    # loose
    ]
    liks = np.array([1.0 / (u - l) for l, u in intervals])
    weights = liks / liks.max()           # 0..1

    row_gap = 1.0
    n = len(intervals)
    for i, ((l, u), w) in enumerate(zip(intervals, weights)):
        y0 = (n - 1 - i) * row_gap        # snug interval near the top
        # opacity + linewidth encode posterior weight
        ax.plot([l, u], [y0, y0], color=ACCENT, alpha=0.25 + 0.75 * w,
                linewidth=2 + 7 * w, solid_capstyle="butt", zorder=2)
        # endpoint ticks
        for x in (l, u):
            ax.plot([x, x], [y0 - 0.22, y0 + 0.22], color=ACCENT,
                    alpha=0.25 + 0.75 * w, linewidth=1.6, zorder=2)

    # observed data points: yellow dots on a baseline below the intervals
    base_y = -1.0
    ax.scatter(data, [base_y] * len(data), s=70, color=YELLOW,
               edgecolor=BG, linewidth=1.0, zorder=5)
    ax.text(data.mean(), base_y - 0.6, "observed examples $X$",
            color=YELLOW, fontsize=10, ha="center", va="top")

    # vertical guides from the data range up through the intervals
    for x in (dlo, dhi):
        ax.plot([x, x], [base_y, (n - 1) * row_gap + 0.6],
                color=YELLOW, linewidth=0.9, linestyle=(0, (2, 3)), zorder=1)

    ax.text(9.6, (n - 1) * row_gap, "snug interval\n→ bigger\nlikelihood",
            color=DIM, fontsize=8.5, ha="left", va="center")
    ax.text(9.6, 0, "loose interval\n→ smaller\nlikelihood",
            color=DIM, fontsize=8.5, ha="left", va="center")

    ax.set_xlim(-0.4, 12.2)
    ax.set_ylim(base_y - 1.4, (n - 1) * row_gap + 1.0)
    ax.set_xlabel("One stimulus dimension", color=TEXT, fontsize=11)
    ax.set_ylabel("Candidate intervals $h$", color=TEXT, fontsize=10.5)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(DIM)

    fig.tight_layout()
    _save(fig, "cc_1d")


# --------------------------------------------------------------------------
# 2-D rectangle game
# --------------------------------------------------------------------------
def build_2d() -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.4), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    # observed dots inside the (unknown) true rectangle
    rng = np.random.default_rng(7)
    n_dots = 5
    dots_x = np.array([3.1, 3.8, 4.6, 5.3, 4.2])
    dots_y = np.array([3.0, 4.4, 3.6, 4.0, 5.0])
    xlo, xhi = dots_x.min(), dots_x.max()
    ylo, yhi = dots_y.min(), dots_y.max()

    # candidate rectangles, each enclosing all dots. Smaller area = bigger
    # posterior — the SMALLEST (snuggest) rectangle is drawn brightest and
    # thickest; the loosest is dim and thin.
    margins = [0.25, 0.7, 1.3, 2.2]       # how far each rect extends past data
    styles = [                            # (grey, linewidth) snug → loose
        ("#EDEDED", 3.6),
        ("#A8A8A8", 2.6),
        ("#6E6E6E", 1.9),
        ("#484848", 1.3),
    ]
    for m, (grey, lw) in zip(margins, styles):
        ax.add_patch(Rectangle(
            (xlo - m, ylo - m), (xhi - xlo) + 2 * m, (yhi - ylo) + 2 * m,
            fill=False, edgecolor=grey, linewidth=lw, zorder=2))

    # the data dots
    ax.scatter(dots_x, dots_y, s=95, color=YELLOW, edgecolor=BG,
               linewidth=1.2, zorder=6)
    # n: label above the whole nest of rectangles, clear of every edge
    ax.text((xlo + xhi) / 2, yhi + margins[-1] + 0.55,
            f"$n = {n_dots}$ observed dots", color=YELLOW, fontsize=9.5,
            ha="center", va="bottom")

    # --- annotate r (data range) and d (extension) ---
    # r: the horizontal span of the data. Draw the double-arrow spanning the
    # data above the dots, with the label above it, clear of the dots.
    r_y = yhi + 0.32
    ax.annotate("", xy=(xlo, r_y), xytext=(xhi, r_y),
                arrowprops=dict(arrowstyle="<->", color=YELLOW, lw=1.8))
    ax.text((xlo + xhi) / 2, r_y + 0.14, "$r$ — range of the data",
            color=YELLOW, fontsize=9.0, ha="center", va="bottom")

    # d: how far a looser rectangle extends beyond the data range, on the
    # right edge — measured from the data edge to the 2nd rectangle
    d_x = xhi + margins[1]
    d_y = ylo + (yhi - ylo) / 2
    ax.annotate("", xy=(xhi, d_y), xytext=(d_x, d_y),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.8))
    ax.text(d_x + 0.2, d_y, "$d$ — how far a\nrectangle extends\npast the data",
            color=ACCENT, fontsize=8.8, ha="left", va="center")

    ax.text(xlo - margins[-1] - 0.55, ylo + (yhi - ylo) / 2,
            "brighter / thicker\n= larger posterior\n(smaller rectangle)",
            color=DIM, fontsize=8.5, ha="right", va="center")

    ax.set_xlim(-3.4, 11.6)
    ax.set_ylim(0.0, 9.0)
    ax.set_xlabel("Feature 1   (e.g. insulin level)", color=TEXT, fontsize=10.5)
    ax.set_ylabel("Feature 2   (e.g. cholesterol level)", color=TEXT, fontsize=10.5)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "cc_2d")


# --------------------------------------------------------------------------
# Exponential prior over rectangle size
# --------------------------------------------------------------------------
def build_exp_prior() -> None:
    fig, ax = plt.subplots(figsize=(6.0, 4.4), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    s = np.linspace(0, 6, 400)
    lam = 0.9
    pdf = lam * np.exp(-lam * s)
    ax.plot(s, pdf, color=ACCENT, linewidth=2.6, zorder=3)
    ax.fill_between(s, 0, pdf, color=ACCENT, alpha=0.13, zorder=1)

    # mark the mean 1/lambda
    mean = 1.0 / lam
    ax.plot([mean, mean], [0, lam * np.exp(-1)], color=YELLOW,
            linewidth=1.4, linestyle=(0, (4, 3)), zorder=4)
    ax.text(mean + 0.12, lam * np.exp(-1) + 0.04,
            "mean $= 1/\\lambda$", color=YELLOW, fontsize=9, ha="left",
            va="bottom")

    ax.text(3.6, lam * 0.55,
            "big rectangles:\nlow prior probability",
            color=DIM, fontsize=9, ha="left", va="center")

    ax.set_xlim(0, 6)
    ax.set_ylim(0, lam * 1.12)
    ax.set_xlabel("Rectangle size $s$", color=TEXT, fontsize=11)
    ax.set_ylabel("Prior density  $p(s)$", color=TEXT, fontsize=11)
    ax.set_xticks([0]); ax.set_xticklabels(["0"], color=DIM)
    ax.set_yticks([])
    ax.tick_params(colors=DIM, labelsize=9)
    for sp in ax.spines.values():
        sp.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "cc_exp_prior")


# --------------------------------------------------------------------------
# Tenenbaum & Griffiths (2001) experiment results — d vs r, by n
# --------------------------------------------------------------------------
def build_tg_results() -> None:
    fig, ax = plt.subplots(figsize=(6.8, 4.4), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    # r values (range spanned by the examples) on the x-axis
    r = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0])

    # d (extent of generalization) for each n — eyeballed from Fig. (a) of
    # Tenenbaum & Griffiths (2001). Smaller n → broader generalization.
    curves = {
        2:  np.array([0.62, 0.78, 1.03, 1.22, 1.69, 2.07]),
        3:  np.array([0.30, 0.47, 0.68, 0.92, 1.01, 1.47]),
        4:  np.array([0.24, 0.33, 0.57, 0.69, 1.00, 1.25]),
        6:  np.array([0.20, 0.30, 0.42, 0.53, 0.69, 0.88]),
        10: np.array([0.15, 0.22, 0.28, 0.38, 0.51, 0.74]),
        50: np.array([0.05, 0.10, 0.18, 0.19, 0.19, 0.30]),
    }
    # warm-to-cool palette so the n-ordering reads off the colour
    colors = ["#5C6BC0", "#2E7D32", "#E53935", "#26C6DA", "#D81B60", "#FBC02D"]

    for (n, d), c in zip(curves.items(), colors):
        ax.plot(r, d, color=c, linewidth=2.2, marker="o", markersize=4,
                markeredgecolor=BG, markeredgewidth=0.6, zorder=3)
        ax.text(8.25, d[-1], f"$n = {n}$", color=c, fontsize=9.5,
                ha="left", va="center")

    ax.set_xlim(0, 9.4)
    ax.set_ylim(0, 2.4)
    ax.set_xlabel("$r$ — range spanned by the $n$ examples",
                  color=TEXT, fontsize=11)
    ax.set_ylabel("$d$ — extent of generalization", color=TEXT, fontsize=11)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.tick_params(colors=DIM, labelsize=9)
    for sp in ax.spines.values():
        sp.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Average data, 6 subjects  (Tenenbaum & Griffiths 2001)",
                 color=TEXT, fontsize=11, pad=8)

    fig.tight_layout()
    _save(fig, "tg_results")


def _save(fig, slug: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{slug}.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote course/week04_generalization_hier_bayes/images/{slug}.png")


def main() -> None:
    print("Building continuous-concept-learning figures...")
    build_1d()
    build_2d()
    build_exp_prior()
    build_tg_results()
    print("Done.")


if __name__ == "__main__":
    main()
