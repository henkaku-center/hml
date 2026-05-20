#!/usr/bin/env python3
"""Tenenbaum & Griffiths (2001) — how the posterior-weighted vote builds an
(approximately) exponential generalization gradient.

Renders two dark-theme PNGs for the Week 4 "posterior-weighted vote" slide:

  tg_hypotheses.png  — one observed data point x, with a stack of candidate
                       consequential-interval hypotheses h that contain x.
                       Each interval is drawn at a HEIGHT proportional to the
                       likelihood it assigns to points in its support, which
                       under strong sampling is 1/|h| (smaller interval = taller
                       = bigger likelihood, the size principle).

  tg_gradient.png    — the result of the posterior-weighted vote: for each
                       candidate point y, sum the posterior weight of every
                       hypothesis that contains y. Plotted as discrete bars,
                       which trace out an approximately exponential decay away
                       from x — Shepard's law, derived rather than assumed.

Styling matches scripts/build_zenith_plots.py / build_shepard_plot.py.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"   # blue — hypotheses / gradient bars
YELLOW = "#FFEB3B"   # yellow — the observed data point
DIM = "#999999"

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "course" / "week04_generalization_hier_bayes" / "images"
)

# One observed data point on a 1-D stimulus dimension.
X_OBS = 0.0
# Candidate interval hypotheses, each (left, right). All contain X_OBS = 0.
# Mix of widths and offsets — exactly the overlapping consequential subsets of
# Tenenbaum & Griffiths' construction.
HYPS = [
    (-0.6, 0.6),
    (-1.4, 0.5),
    (-0.4, 1.6),
    (-2.4, 1.1),
    (-1.0, 3.0),
    (-3.6, 1.6),
    (-1.8, 4.6),
]


def hyp_likelihood(h: tuple[float, float]) -> float:
    """Strong-sampling likelihood for a single datum: 1 / |h| (interval length)."""
    return 1.0 / (h[1] - h[0])


def build_hypotheses_panel() -> None:
    """One data point + stacked candidate intervals, height = likelihood."""
    fig, ax = plt.subplots(figsize=(6.2, 4.0), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    # sort by likelihood — most likely (smallest |h|) at the BOTTOM, so the
    # stack reads top-to-bottom as "bigger hypothesis → thinner bar".
    hyps = sorted(HYPS, key=hyp_likelihood)
    liks = np.array([hyp_likelihood(h) for h in hyps])
    heights = liks / liks.max()           # 0..1, proportional to likelihood

    # draw each interval as a horizontal bar; thicker = more likely (smaller |h|)
    row_gap = 1.0
    for i, (h, ht) in enumerate(zip(hyps, heights)):
        y0 = i * row_gap
        bar_h = 0.16 + 0.74 * ht          # visual thickness ∝ likelihood
        ax.add_patch(plt.Rectangle(
            (h[0], y0 - bar_h / 2), h[1] - h[0], bar_h,
            facecolor=ACCENT, edgecolor=ACCENT, alpha=0.5, linewidth=1.4,
            zorder=2))
        # likelihood label: 1/|h| printed to the right of each interval
        ax.text(h[1] + 0.28, y0, f"$1/|h|$ = {hyp_likelihood(h):.2f}",
                color=ACCENT, fontsize=8.0, ha="left", va="center", zorder=3)

    n = len(hyps)
    # the observed data point: a vertical yellow line through every interval
    ax.plot([X_OBS, X_OBS], [-0.7, (n - 1) * row_gap + 0.7],
            color=YELLOW, linewidth=2.2, zorder=4)
    ax.plot([X_OBS], [(n - 1) * row_gap + 0.7], "o", color=YELLOW,
            markersize=8, markeredgecolor=BG, markeredgewidth=1.0, zorder=5)
    ax.text(X_OBS, (n - 1) * row_gap + 1.05, "observed datum  $x$",
            color=YELLOW, fontsize=10, ha="center", va="bottom")

    ax.text(X_OBS - 4.0, (n - 1) * row_gap * 0.5,
            "thicker bar\n= smaller $|h|$\n= bigger\nlikelihood",
            color=DIM, fontsize=8.5, ha="left", va="center")

    ax.set_xlim(-4.4, 7.0)
    ax.set_ylim(-1.1, (n - 1) * row_gap + 1.7)
    ax.set_xlabel("Stimulus dimension", color=TEXT, fontsize=11)
    ax.set_ylabel("Candidate hypotheses $h$  (each contains $x$)",
                  color=TEXT, fontsize=10.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(DIM)

    fig.tight_layout()
    out_path = OUT_DIR / "tg_hypotheses.png"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")


def build_gradient_panel() -> None:
    """The posterior-weighted vote: sum posterior over hypotheses containing y."""
    fig, ax = plt.subplots(figsize=(6.2, 3.4), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    # posterior weight of each hypothesis (prior flat → posterior ∝ likelihood)
    liks = np.array([hyp_likelihood(h) for h in HYPS])
    post = liks / liks.sum()

    # candidate points y on the dimension; discretised
    ys = np.arange(-4.0, 6.01, 0.5)
    gen = np.zeros_like(ys)
    for w, h in zip(post, HYPS):
        inside = (ys >= h[0]) & (ys <= h[1])
        gen[inside] += w   # indicator * posterior weight, summed

    ax.bar(ys, gen, width=0.42, color=ACCENT, edgecolor=ACCENT, zorder=3)

    # a reference exponential decay anchored at x for the "≈ exponential" point
    grid = np.linspace(ys.min(), ys.max(), 400)
    ref = gen.max() * np.exp(-np.abs(grid - X_OBS) / 1.6)
    ax.plot(grid, ref, color=YELLOW, linewidth=2.0, linestyle="--", zorder=4)
    ax.text(4.7, gen.max() * 0.62, "≈ exponential\n(Shepard's law)",
            color=YELLOW, fontsize=9, ha="left", va="center")

    # mark the observed datum
    ax.plot([X_OBS], [gen.max() * 1.06], "v", color=YELLOW, markersize=9,
            markeredgecolor=BG, markeredgewidth=1.0, zorder=5, clip_on=False)
    ax.text(X_OBS, gen.max() * 1.14, "$x$", color=YELLOW, fontsize=10,
            ha="center", va="bottom", clip_on=False)

    ax.set_xlim(-4.4, 6.6)
    ax.set_ylim(0, gen.max() * 1.18)
    ax.set_xlabel("Novel stimulus $y$", color=TEXT, fontsize=11)
    ax.set_ylabel("$p(y \\in C \\mid x)$", color=TEXT, fontsize=11)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(DIM)

    fig.tight_layout()
    out_path = OUT_DIR / "tg_gradient.png"
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")


def main() -> None:
    print("Building Tenenbaum & Griffiths integration figures...")
    build_hypotheses_panel()
    build_gradient_panel()
    print("Done.")


if __name__ == "__main__":
    main()
