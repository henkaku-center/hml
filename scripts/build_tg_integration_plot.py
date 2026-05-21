#!/usr/bin/env python3
"""Tenenbaum & Griffiths (2001) — how the posterior-weighted vote builds an
(approximately) exponential generalization gradient.

Renders a stacked two-panel dark-theme figure for the Week 4
"posterior-weighted vote" slide series:

  TOP panel    — one observed datum x, with a stack of candidate
                 consequential-interval hypotheses h that contain x. Each
                 interval is drawn at a THICKNESS proportional to the
                 likelihood it assigns under strong sampling, 1/|h|
                 (smaller interval = thicker = bigger likelihood — the
                 size principle).

  BOTTOM panel — the posterior-weighted vote: for each candidate point y,
                 sum the posterior weight of every hypothesis that contains
                 y. Plotted as discrete bars, tracing an approximately
                 exponential decay away from x — Shepard's law derived.

The two panels share an x-axis so a given y lines up across both.

Four variants are produced:
  tg_vote.png        — base figure, no y highlighted.
  tg_vote_y0.png     — y = x   highlighted.
  tg_vote_y1.png     — y = x+1 highlighted.
  tg_vote_y2.png     — y = x+2 highlighted.

When a y is highlighted: a labeled marker is drawn at the top, the
hypotheses that do NOT contain y are greyed out, and in the gradient panel
every bar except the one at y is greyed — so the highlighted bar reads as
"the sum of exactly the still-coloured hypotheses".

Styling matches scripts/build_zenith_plots.py / build_shepard_plot.py.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"   # blue — active hypotheses / gradient bars
YELLOW = "#FFEB3B"   # yellow — the observed datum x and highlighted y
GREY = "#4A4A4A"     # greyed-out (inactive) hypotheses / bars
DIM = "#999999"

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "course" / "week04_generalization_hier_bayes" / "images"
)

# One observed data point on a 1-D stimulus dimension.
X_OBS = 0.0

# Candidate interval hypotheses, each (left, right). All contain X_OBS = 0.
# Mix of widths and offsets — the overlapping consequential subsets of the
# Tenenbaum & Griffiths construction.
HYPS = [
    (-0.6, 0.6),
    (-1.4, 0.5),
    (-0.4, 1.6),
    (-2.4, 1.1),
    (-1.0, 3.0),
    (-3.6, 1.6),
    (-1.8, 4.6),
]

# Discretised candidate points y on the dimension.
YS = np.arange(-4.0, 6.01, 1.0)

# Shared x-range so the two panels line up exactly.
XLIM = (-4.6, 7.2)


def hyp_likelihood(h: tuple[float, float]) -> float:
    """Strong-sampling likelihood for a single datum: 1 / |h| (interval length)."""
    return 1.0 / (h[1] - h[0])


def build_vote_figure(highlight_y: float | None, slug: str) -> None:
    """Stacked hypotheses + gradient panels. If highlight_y is set, mark that
    y, grey the hypotheses that exclude it, and grey every gradient bar but y."""
    # Aspect tuned so that, at a 54%-width column, the figure fills most of
    # the slide's vertical space without dwarfing the text column beside it
    # (the text column is `.v-center`ed against it). Tall enough to avoid the
    # BOTTOM-GAP void, not so tall it triggers COLUMN-THIN on the text.
    fig, (axh, axg) = plt.subplots(
        2, 1, figsize=(7.4, 5.5), dpi=150, facecolor=BG,
        gridspec_kw=dict(height_ratios=[1.55, 1.0], hspace=0.42),
    )
    axh.set_facecolor(BG)
    axg.set_facecolor(BG)

    # hypotheses sorted by likelihood: most likely (smallest |h|) at the top.
    hyps = sorted(HYPS, key=hyp_likelihood, reverse=True)
    liks = np.array([hyp_likelihood(h) for h in hyps])
    heights = liks / liks.max()           # 0..1, proportional to likelihood
    post = liks / liks.sum()              # flat prior -> posterior ∝ likelihood

    contains_y = [
        (highlight_y is not None and h[0] <= highlight_y <= h[1])
        for h in hyps
    ]
    any_highlight = highlight_y is not None

    # ----- TOP PANEL: candidate hypotheses over the datum -----
    row_gap = 1.0
    n = len(hyps)
    for i, (h, ht) in enumerate(zip(hyps, heights)):
        y0 = (n - 1 - i) * row_gap        # row 0 (most likely) drawn at top
        bar_h = 0.16 + 0.74 * ht          # thickness ∝ likelihood
        active = (not any_highlight) or contains_y[i]
        col = ACCENT if active else GREY
        ax_alpha = 0.5 if active else 0.32
        axh.add_patch(plt.Rectangle(
            (h[0], y0 - bar_h / 2), h[1] - h[0], bar_h,
            facecolor=col, edgecolor=col, alpha=ax_alpha, linewidth=1.4,
            zorder=2))
        axh.text(h[1] + 0.28, y0, f"$1/|h|$ = {hyp_likelihood(h):.2f}",
                 color=col if active else GREY, fontsize=8.0,
                 ha="left", va="center", zorder=6)

    top_y = (n - 1) * row_gap

    # observed datum x — a yellow line through every interval
    axh.plot([X_OBS, X_OBS], [-0.7, top_y + 0.7],
             color=YELLOW, linewidth=2.2, zorder=4)
    axh.plot([X_OBS], [top_y + 0.7], "o", color=YELLOW, markersize=8,
             markeredgecolor=BG, markeredgewidth=1.0, zorder=5)
    axh.text(X_OBS, top_y + 1.02, "datum  $x$", color=YELLOW, fontsize=10,
             ha="center", va="bottom", zorder=5)

    # highlighted y — a second marker + line, offset so it's distinct from x
    if any_highlight and highlight_y != X_OBS:
        axh.plot([highlight_y, highlight_y], [-0.7, top_y + 0.7],
                 color=YELLOW, linewidth=1.6, linestyle=(0, (4, 3)), zorder=1)
        axh.plot([highlight_y], [top_y + 0.7], "v", color=YELLOW,
                 markersize=10, markeredgecolor=BG, markeredgewidth=1.0,
                 zorder=5)
        # stagger the y label below the x label when the two are close
        close = abs(highlight_y - X_OBS) < 2.0
        axh.text(highlight_y, top_y + (0.42 if close else 1.02),
                 y_label(highlight_y), color=YELLOW, fontsize=10,
                 ha="center", va="bottom", zorder=5,
                 bbox=dict(boxstyle="round,pad=0.15", facecolor=BG,
                           edgecolor="none") if close else None)

    axh.set_xlim(*XLIM)
    axh.set_ylim(-1.1, top_y + 1.7)
    axh.set_ylabel("Hypotheses $h$\n(thicker = bigger likelihood)",
                   color=TEXT, fontsize=9.5)
    axh.set_xticks([])
    axh.set_yticks([])
    for spine in axh.spines.values():
        spine.set_visible(False)
    axh.spines["bottom"].set_visible(True)
    axh.spines["bottom"].set_color(DIM)
    if any_highlight:
        n_active = sum(contains_y)
        axh.set_title(
            f"{n_active} of {n} hypotheses contain {y_label_plain(highlight_y)}",
            color=YELLOW, fontsize=10.5, pad=8)

    # ----- BOTTOM PANEL: the posterior-weighted vote -----
    gen = np.zeros_like(YS)
    for w, h in zip(post, hyps):
        inside = (YS >= h[0]) & (YS <= h[1])
        gen[inside] += w

    bar_cols = []
    for yv in YS:
        if any_highlight and not np.isclose(yv, highlight_y):
            bar_cols.append(GREY)
        else:
            bar_cols.append(ACCENT)
    axg.bar(YS, gen, width=0.7, color=bar_cols, edgecolor=bar_cols, zorder=3)

    # reference exponential decay anchored at x
    grid = np.linspace(XLIM[0], XLIM[1], 400)
    ref = gen.max() * np.exp(-np.abs(grid - X_OBS) / 2.0)
    axg.plot(grid, ref, color=DIM, linewidth=1.6, linestyle=(0, (5, 4)),
             zorder=2)
    axg.text(5.4, gen.max() * 0.66, "≈ exponential", color=DIM, fontsize=8.5,
             ha="left", va="center")

    # mark x on the gradient axis
    axg.plot([X_OBS, X_OBS], [0, gen.max() * 1.16], color=YELLOW,
             linewidth=1.2, linestyle=(0, (2, 3)), zorder=2)

    if any_highlight:
        # call out the highlighted bar's height = its posterior-weighted sum
        idx = int(np.argmin(np.abs(YS - highlight_y)))
        axg.annotate(
            y_label(highlight_y),
            xy=(highlight_y, gen[idx]),
            xytext=(highlight_y, gen.max() * 1.05),
            color=YELLOW, fontsize=10, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=YELLOW, lw=1.0))

    axg.set_xlim(*XLIM)
    axg.set_ylim(0, gen.max() * 1.22)
    axg.set_xlabel("Novel stimulus $y$", color=TEXT, fontsize=11)
    axg.set_ylabel("$p(y \\in C \\mid x)$", color=TEXT, fontsize=11)
    axg.set_xticks([])
    axg.set_yticks([])
    for spine in axg.spines.values():
        spine.set_visible(False)
    axg.spines["bottom"].set_visible(True)
    axg.spines["bottom"].set_color(DIM)

    fig.savefig(OUT_DIR / f"{slug}.png", facecolor=BG, edgecolor="none",
                bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote course/week04_generalization_hier_bayes/images/{slug}.png")


def y_label(y: float) -> str:
    """Math-mode label for a y offset from x."""
    off = int(round(y - X_OBS))
    if off == 0:
        return "$y = x$"
    return f"$y = x + {off}$" if off > 0 else f"$y = x - {abs(off)}$"


def y_label_plain(y: float) -> str:
    """Plain-text label (titles don't render mathtext cleanly inline)."""
    off = int(round(y - X_OBS))
    if off == 0:
        return "y = x"
    return f"y = x+{off}" if off > 0 else f"y = x-{abs(off)}"


def main() -> None:
    print("Building Tenenbaum & Griffiths posterior-weighted-vote figures...")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_vote_figure(None, "tg_vote")
    build_vote_figure(X_OBS + 0.0, "tg_vote_y0")
    build_vote_figure(X_OBS + 1.0, "tg_vote_y1")
    build_vote_figure(X_OBS + 2.0, "tg_vote_y2")
    print("Done.")


if __name__ == "__main__":
    main()
