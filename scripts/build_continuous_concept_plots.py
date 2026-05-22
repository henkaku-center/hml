#!/usr/bin/env python3
"""Continuous concept learning — visualizations for Week 4 Block 5.

Dark-theme matplotlib figures for the rectangle-game (continuous concept
learning) section:

  cc_1d.png        — 1-D: a few observed points on a line, with candidate
                     interval hypotheses drawn at varying opacity = posterior
                     weight. Smaller intervals (tighter to the data) are
                     darker/heavier.

  cc_1d_gradient.png — multi-example analog of the T&G vote figure: candidate
                     intervals consistent with several observed examples,
                     thickness = posterior, summed into the 1-D generalization
                     gradient (flat over the data, decaying outside).

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
    top_y = (n - 1) * row_gap             # y of the snug (top) interval
    for i, ((l, u), w) in enumerate(zip(intervals, weights)):
        y0 = (n - 1 - i) * row_gap        # snug interval near the top
        # opacity + linewidth encode posterior weight
        ax.plot([l, u], [y0, y0], color=ACCENT, alpha=0.25 + 0.75 * w,
                linewidth=2 + 7 * w, solid_capstyle="butt", zorder=2)
        # endpoint ticks
        for x in (l, u):
            ax.plot([x, x], [y0 - 0.22, y0 + 0.22], color=ACCENT,
                    alpha=0.25 + 0.75 * w, linewidth=1.6, zorder=2)

    # label the endpoints of the snug (top) interval as the lower / upper
    # bounds [l, u] — the notation used on the slide
    snug_l, snug_u = intervals[0]
    ax.text(snug_l, top_y + 0.42, r"$\ell$", color=ACCENT, fontsize=12,
            ha="center", va="bottom", fontweight="bold")
    ax.text(snug_u, top_y + 0.42, r"$u$", color=ACCENT, fontsize=12,
            ha="center", va="bottom", fontweight="bold")
    ax.text((snug_l + snug_u) / 2, top_y + 0.42,
            r"interval $[\ell,\, u]$", color=DIM, fontsize=8.5,
            ha="center", va="bottom")

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
# 1-D generalization gradient for multiple examples
# --------------------------------------------------------------------------
def build_1d_gradient() -> None:
    """Multi-example analog of the T&G vote figure: with several observed
    examples, every consistent interval votes (weighted by posterior), and the
    posterior-weighted sum traces the 1-D generalization gradient.
    """
    fig, (ax_h, ax_g) = plt.subplots(
        2, 1, figsize=(7.4, 6.0), dpi=150, facecolor=BG,
        gridspec_kw=dict(height_ratios=[1.55, 1.0], hspace=0.42))
    for ax in (ax_h, ax_g):
        ax.set_facecolor(BG)

    # several observed examples spanning a range on the dimension
    data = np.array([3.6, 4.3, 5.1, 5.8])
    dlo, dhi = data.min(), data.max()

    # candidate intervals [l, u] that contain ALL the examples. Smaller =
    # higher strong-sampling likelihood = higher posterior (flat prior).
    intervals = [
        (3.4, 6.0),    # snug
        (2.9, 6.6),
        (2.2, 7.4),
        (1.3, 8.4),
        (0.4, 9.4),    # loose
    ]
    liks = np.array([1.0 / (u - l) for l, u in intervals])
    post = liks / liks.sum()              # posterior weights, sum to 1
    wmax = post.max()

    # --- top panel: the consistent intervals, thickness = posterior ----------
    row_gap = 1.0
    n = len(intervals)
    for i, ((l, u), w) in enumerate(zip(intervals, post)):
        y0 = (n - 1 - i) * row_gap
        rel = w / wmax
        ax_h.plot([l, u], [y0, y0], color=ACCENT, alpha=0.30 + 0.70 * rel,
                  linewidth=2 + 7 * rel, solid_capstyle="butt", zorder=2)
        for x in (l, u):
            ax_h.plot([x, x], [y0 - 0.22, y0 + 0.22], color=ACCENT,
                      alpha=0.30 + 0.70 * rel, linewidth=1.6, zorder=2)

    # observed examples, baseline below the intervals
    base_y = -1.05
    ax_h.scatter(data, [base_y] * len(data), s=80, color=YELLOW,
                 edgecolor=BG, linewidth=1.0, zorder=5)
    ax_h.text(data.mean(), base_y - 0.55, "observed examples $X$",
              color=YELLOW, fontsize=9.5, ha="center", va="top")
    for x in (dlo, dhi):
        ax_h.plot([x, x], [base_y, (n - 1) * row_gap + 0.5],
                  color=YELLOW, linewidth=0.9, linestyle=(0, (2, 3)), zorder=1)
    ax_h.text(9.9, (n - 1) * row_gap,
              "every interval\ncontaining $X$\nvotes — thicker\n= more posterior",
              color=DIM, fontsize=8.2, ha="left", va="center")

    ax_h.set_xlim(-0.4, 12.6)
    ax_h.set_ylim(base_y - 1.5, (n - 1) * row_gap + 0.9)
    ax_h.set_ylabel("Candidate intervals $h$", color=TEXT, fontsize=10)
    ax_h.set_xticks([]); ax_h.set_yticks([])
    for sp in ax_h.spines.values():
        sp.set_visible(False)

    # --- bottom panel: the posterior-weighted vote = generalization gradient -
    grid = np.linspace(-0.4, 12.6, 600)
    gradient = np.zeros_like(grid)
    for (l, u), w in zip(intervals, post):
        gradient += w * ((grid >= l) & (grid <= u))
    ax_g.fill_between(grid, gradient, color=ACCENT, alpha=0.32, zorder=2)
    ax_g.plot(grid, gradient, color=ACCENT, linewidth=2.2, zorder=3)
    for x in (dlo, dhi):
        ax_g.plot([x, x], [0, 1.05], color=YELLOW, linewidth=0.9,
                  linestyle=(0, (2, 3)), zorder=1)
    ax_g.scatter(data, [-0.12] * len(data), s=80, color=YELLOW,
                 edgecolor=BG, linewidth=1.0, zorder=5, clip_on=False)
    ax_g.text(11.3, 0.80, "flat over $X$,\ndecays outside",
              color=DIM, fontsize=8.2, ha="center", va="center")

    ax_g.set_xlim(-0.4, 12.6)
    ax_g.set_ylim(0, 1.12)
    ax_g.set_xlabel("Novel stimulus $y$  (one stimulus dimension)",
                    color=TEXT, fontsize=10.5, labelpad=14)
    ax_g.set_ylabel(r"$p(y \in C \mid X)$", color=TEXT, fontsize=10.5)
    ax_g.set_xticks([]); ax_g.set_yticks([])
    for sp in ax_g.spines.values():
        sp.set_color(DIM)
    ax_g.spines["top"].set_visible(False)
    ax_g.spines["right"].set_visible(False)

    _save(fig, "cc_1d_gradient")


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
    ax.text((xlo + xhi) / 2, yhi + margins[-1] + 0.70,
            f"$n = {n_dots}$ observed dots", color=YELLOW, fontsize=9.5,
            ha="center", va="bottom")

    # --- annotate r (data range) and d (extension) ---
    # r: the horizontal span of the data. Place the arrow + label in the gap
    # ABOVE the snuggest rectangle's top edge (yhi + margins[0]) so neither
    # the arrow nor its label sits on a rectangle line. A short yellow tick
    # at each end ties the span back to the data extent it measures.
    r_y = yhi + margins[0] + 0.45
    for x_end in (xlo, xhi):
        ax.plot([x_end, x_end], [yhi + margins[0] + 0.06, r_y],
                color=YELLOW, lw=1.0, zorder=3)
    ax.annotate("", xy=(xlo, r_y), xytext=(xhi, r_y),
                arrowprops=dict(arrowstyle="<->", color=YELLOW, lw=1.8))
    ax.text((xlo + xhi) / 2, r_y + 0.16, "$r$ — range of the data",
            color=YELLOW, fontsize=9.0, ha="center", va="bottom")

    # d: how far a candidate rectangle extends past the data range. Measure on
    # the right side, from the data edge (xhi) out to the LOOSEST rectangle's
    # edge (xhi + margins[-1]) — a long, unambiguous span. Put it on a row
    # comfortably below the dots and below the snug rectangle's bottom edge so
    # the arrow crosses no dot; the label sits fully clear to the right.
    d_y = ylo - margins[1] - 0.55
    d_x_data = xhi
    d_x_loose = xhi + margins[-1]
    for x_end, ytop in ((d_x_data, ylo), (d_x_loose, ylo - margins[-1])):
        ax.plot([x_end, x_end], [d_y, ytop], color=ACCENT, lw=1.0,
                linestyle=":", zorder=3)
    ax.annotate("", xy=(d_x_data, d_y), xytext=(d_x_loose, d_y),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.8))
    ax.text(d_x_loose + 0.45, d_y, "$d$ — how far a rectangle\nextends past the data",
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
    build_1d_gradient()
    build_2d()
    build_exp_prior()
    build_tg_results()
    print("Done.")


if __name__ == "__main__":
    main()
