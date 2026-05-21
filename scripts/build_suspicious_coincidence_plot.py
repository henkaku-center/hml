#!/usr/bin/env python3
"""The "suspicious coincidence" — strong vs. weak sampling posteriors.

Number game on 1-100. Two hypotheses:
  - "multiples of 10"  h10  : |h10| = 10
  - "even numbers"     hE   : |hE|  = 50
Flat prior: p(h10) = p(hE) = 0.5.

Under STRONG sampling each example is drawn uniformly from within h, so
  p(X | h) = (1/|h|)^n.
Under WEAK sampling the likelihood is 1 if every example is in h, else 0 —
independent of |h|.

For data X = {60} and X = {60, 80, 10, 30} (all of which are multiples of 10,
hence also even), this script renders dark-theme bar charts of the posterior
p(h | X) for each hypothesis, contrasting the two sampling assumptions.

Output (course/week04_generalization_hier_bayes/images/):
  suspicious_strong_1.png   strong sampling, X = {60}
  suspicious_strong_4.png   strong sampling, X = {60,80,10,30}
  suspicious_weak.png       weak sampling (same for both X — flat)

Styling matches scripts/build_zenith_plots.py.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"   # blue — multiples of 10
YELLOW = "#FFEB3B"   # yellow — even numbers
DIM = "#999999"

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "course" / "week04_generalization_hier_bayes" / "images"
)

SIZE_H10 = 10        # |multiples of 10| in 1..100
SIZE_HE = 50         # |even numbers|   in 1..100
PRIOR = 0.5          # flat prior over the two hypotheses


def strong_posterior(n: int) -> tuple[float, float]:
    """Posterior (p_h10, p_hE) under strong sampling for n examples."""
    lik10 = (1.0 / SIZE_H10) ** n
    likE = (1.0 / SIZE_HE) ** n
    z = PRIOR * lik10 + PRIOR * likE
    return PRIOR * lik10 / z, PRIOR * likE / z


def weak_posterior() -> tuple[float, float]:
    """Posterior under weak sampling: the likelihood is 1 for every hypothesis
    that contains the data, so the posterior is just the renormalised prior
    over the surviving hypotheses — independent of n AND of |h|.

    With this 2-hypothesis space and a flat prior that renormalised prior is
    0.5 / 0.5. The value 0.5 is therefore an artefact of (a) two hypotheses
    and (b) a flat prior — NOT a property of weak sampling itself. The robust
    statement is: under weak sampling the posterior never moves off the prior.
    """
    return PRIOR, PRIOR


def plot_posterior(p10: float, pE: float, title: str, subtitle: str,
                   slug: str) -> None:
    fig, ax = plt.subplots(figsize=(5.4, 4.0), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    labels = ["multiples\nof 10", "even\nnumbers"]
    vals = [p10, pE]
    cols = [ACCENT, YELLOW]
    x = np.arange(2)
    bars = ax.bar(x, vals, width=0.58, color=cols, edgecolor=cols, zorder=3)

    # value label on top of each bar
    for xi, v in zip(x, vals):
        ax.text(xi, v + 0.035, f"{v:.3f}", color=TEXT, fontsize=12,
                ha="center", va="bottom", fontweight="bold")

    # 50/50 reference line — the prior / the weak-sampling answer
    ax.axhline(0.5, color=DIM, linewidth=1.0, linestyle=(0, (5, 4)), zorder=2)
    ax.text(1.46, 0.5, "prior\n(50/50)", color=DIM, fontsize=8.0,
            ha="left", va="center")

    ax.set_title(title, color=TEXT, fontsize=14, pad=6)
    ax.text(0.5, 1.16, subtitle, color=DIM, fontsize=10, ha="center",
            va="bottom", transform=ax.transAxes)
    ax.set_ylabel("Posterior  $p(h \\mid X)$", color=TEXT, fontsize=11)
    ax.set_ylim(0, 1.18)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, color=TEXT, fontsize=10)
    ax.set_yticks([0, 0.5, 1.0])
    ax.tick_params(colors=DIM, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out_path = OUT_DIR / f"{slug}.png"
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote course/week04_generalization_hier_bayes/images/{slug}.png")


def main() -> None:
    print("Building suspicious-coincidence posterior figures...")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # strong sampling, one example
    p10, pE = strong_posterior(1)
    plot_posterior(p10, pE, "Strong sampling",
                   "X = {60}   ·   one example", "suspicious_strong_1")

    # strong sampling, four examples
    p10, pE = strong_posterior(4)
    plot_posterior(p10, pE, "Strong sampling",
                   "X = {60, 80, 10, 30}   ·   four examples",
                   "suspicious_strong_4")

    # weak sampling — posterior reverts to the flat prior, regardless of data
    p10, pE = weak_posterior()
    plot_posterior(p10, pE, "Weak sampling",
                   "posterior = prior (flat, 2 hypotheses) — data adds nothing",
                   "suspicious_weak")
    print("Done.")


if __name__ == "__main__":
    main()
