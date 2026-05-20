#!/usr/bin/env python3
"""Shepard's universal law of generalization — exponential decay curve.

Renders a single dark-theme PNG for the Week 4 "Shepard's universal law" slide:
the generalization gradient g(d) = exp(-d) plotted against deviation d in
psychological space, with the referent stimulus at d = 0.

The stimulus dimension is illustrated concretely as the length of a vertical
line: short lines to the left of the referent, long lines to the right, the
referent itself marked at d = 0. This makes "deviation in psychological space"
tangible — it is how different a line's length looks from the referent's.

Output: course/week04_generalization_hier_bayes/images/shepard_decay.png
Dark-theme styling matches scripts/build_zenith_plots.py.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"   # blue — the generalization curve
YELLOW = "#FFEB3B"   # yellow — the referent marker
DIM = "#999999"

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "course" / "week04_generalization_hier_bayes" / "images"
)


def build_shepard_decay() -> None:
    # Two stacked panels: the decay curve (tall) + a short strip for the
    # vertical-line stimulus glyphs. Sharing the x-axis keeps each line glyph
    # aligned under its deviation value on the curve.
    fig, (ax, axs) = plt.subplots(
        2, 1, figsize=(6.4, 4.3), dpi=150, facecolor=BG,
        sharex=True, gridspec_kw=dict(height_ratios=[4.0, 1.0], hspace=0.32),
    )
    ax.set_facecolor(BG)
    axs.set_facecolor(BG)

    # --- the exponential generalization gradient g(d) = exp(-d) ---
    d = np.linspace(0.0, 4.0, 400)
    g = np.exp(-d)
    ax.plot(d, g, color=ACCENT, linewidth=2.6, zorder=3)
    ax.fill_between(d, 0, g, color=ACCENT, alpha=0.12, zorder=1)

    # --- referent stimulus at d = 0 ---
    ax.plot([0], [1.0], "o", color=YELLOW, markersize=9,
            markeredgecolor=BG, markeredgewidth=1.2, zorder=5)
    ax.annotate(
        "referent\nstimulus",
        xy=(0, 1.0), xytext=(0.55, 0.86),
        color=YELLOW, fontsize=10, ha="left", va="center",
        arrowprops=dict(arrowstyle="-", color=YELLOW, lw=1.0),
    )

    # --- top panel: the exponential generalization gradient ---
    ax.set_xlim(-0.15, 4.2)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Probability of\ngeneralization", color=TEXT, fontsize=11)
    ax.set_yticks([0, 0.5, 1.0])
    ax.tick_params(colors=DIM, labelsize=9)
    ax.tick_params(axis="x", length=0)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # --- bottom panel: vertical-line stimuli, length encodes the dimension ---
    # The referent is a mid-length line at d = 0; comparison lines grow longer
    # as deviation increases. Each glyph is aligned under its d on the curve.
    line_xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    base_len = 0.34          # referent half-height (panel data units)
    grow = 0.13              # extra half-height per unit deviation
    for lx in line_xs:
        half = base_len + grow * lx
        col = YELLOW if lx == 0.0 else DIM
        lw = 3.6 if lx == 0.0 else 2.6
        axs.plot([lx, lx], [-half, half], color=col, linewidth=lw,
                 solid_capstyle="round", zorder=3)
    axs.text(0.0, 1.20, "referent", color=YELLOW, fontsize=8.5,
             ha="center", va="bottom")
    axs.text(4.0, 1.20, "stimulus = length of a vertical line  ·  longer → larger $d$",
             color=DIM, fontsize=8.5, ha="right", va="bottom")

    axs.set_ylim(-1.45, 1.55)
    axs.set_xlabel("Deviation in psychological space from the referent  ($d$)",
                   color=TEXT, fontsize=11, labelpad=6)
    axs.set_xticks([0, 1, 2, 3, 4])
    axs.set_xticklabels(["0", "", "", "", ""], color=DIM)
    axs.set_yticks([])
    axs.tick_params(axis="x", colors=DIM, labelsize=9)
    for spine in axs.spines.values():
        spine.set_visible(False)
    axs.spines["bottom"].set_visible(True)
    axs.spines["bottom"].set_color(DIM)

    out_path = OUT_DIR / "shepard_decay.png"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")


def main() -> None:
    print("Building Shepard universal-law decay plot...")
    build_shepard_decay()
    print("Done.")


if __name__ == "__main__":
    main()
