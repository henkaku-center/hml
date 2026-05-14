#!/usr/bin/env python3
"""Build per-case Beta-distribution PDF plots for Week 3 slides.

Generates one PNG per case in course/week03_conjugate_bayes_topics/figures/.
Each PNG: dark background, single PDF curve, parameter label.
The slide author handles the "5 representative samples" via printed numbers
in the .qmd (samples are also written to a JSON for traceability).

Reproducibility: numpy seed pinned. Re-running yields byte-identical PNGs.
"""
from __future__ import annotations

import json
import zlib
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

# SDS theme colors — mirror sds-reveal/sds.scss
BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"  # blue
YELLOW = "#FFEB3B"
DIM = "#999999"

OUT_DIR = Path(__file__).resolve().parent.parent / "course" / "week03_conjugate_bayes_topics" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (slug, alpha, beta, table-row label)
CASES = [
    ("beta_uniform",    1.0, 1.0, "alpha = beta = 1: uniform on [0,1]"),
    ("beta_concentrated_high", 8.0, 3.0, "alpha > beta: concentrated above 0.5"),
    ("beta_narrow",     50.0, 50.0, "large alpha + beta: narrow (confident)"),
    ("beta_wide",       2.0, 2.0, "small alpha + beta: wide (uncertain)"),
    ("beta_ushaped",    0.5, 0.5, "alpha = beta < 1: U-shaped at the edges"),
]


def plot_case(slug: str, a: float, b: float, label: str) -> dict:
    """Render one PDF curve + rug of 5 samples. Returns the sample numbers."""
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    x = np.linspace(1e-4, 1 - 1e-4, 500)
    y = beta.pdf(x, a, b)

    # Clip to plot area — U-shaped pdfs diverge at endpoints
    y_max_plot = min(np.nanmax(y[np.isfinite(y)]), 6.0)

    ax.plot(x, y, color=ACCENT, linewidth=2.6)
    ax.fill_between(x, 0, y, color=ACCENT, alpha=0.18)

    # Pin RNG per-case so re-runs are reproducible
    rng = np.random.default_rng(seed=42 + (zlib.crc32(slug.encode()) % 1000))
    samples = beta.rvs(a, b, size=5, random_state=rng)
    samples_rounded = [round(float(s), 3) for s in samples]

    # Rug of 5 samples at the bottom
    tick_h = y_max_plot * 0.08
    for s in samples:
        ax.plot([s, s], [0, tick_h], color=YELLOW, linewidth=2.8, solid_capstyle="butt")

    # Title with the actual parameter values
    ax.set_title(f"Beta(α={_fmt(a)}, β={_fmt(b)})",
                 color=TEXT, fontsize=18, pad=12, loc="left")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, y_max_plot * 1.05)
    ax.set_xlabel("θ", color=TEXT, fontsize=14)
    ax.set_ylabel("p(θ)", color=TEXT, fontsize=14)

    ax.tick_params(colors=DIM, labelsize=11)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out_path = OUT_DIR / f"{slug}.png"
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")
    return {"slug": slug, "alpha": a, "beta": b, "label": label, "samples": samples_rounded}


def _fmt(x: float) -> str:
    if x == int(x):
        return str(int(x))
    return f"{x:g}"


def _draw_panel(ax, a: float, b: float, *, x_label: bool, y_label: bool, samples_seed: int) -> list[float]:
    """Render one PDF panel + 5 representative-sample rug ticks. Returns the samples."""
    ax.set_facecolor(BG)
    x = np.linspace(1e-4, 1 - 1e-4, 500)
    y = beta.pdf(x, a, b)
    y_max = min(np.nanmax(y[np.isfinite(y)]), 6.0)

    ax.plot(x, y, color=ACCENT, linewidth=2.0)
    ax.fill_between(x, 0, y, color=ACCENT, alpha=0.18)

    # Draw 5 representative samples as a rug at the bottom (yellow ticks).
    rng = np.random.default_rng(seed=samples_seed)
    samples = beta.rvs(a, b, size=5, random_state=rng)
    samples_rounded = [round(float(s), 3) for s in samples]
    tick_h = y_max * 0.08  # small ticks
    for s in samples:
        ax.plot([s, s], [0, tick_h], color=YELLOW, linewidth=2.2, solid_capstyle="butt")

    ax.set_title(f"Beta({_fmt(a)}, {_fmt(b)})",
                 color=TEXT, fontsize=13, pad=6, loc="left")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, y_max * 1.05)

    # Axis labels: only when the caller requests (first column / bottom row)
    if x_label:
        ax.set_xlabel("θ", color=TEXT, fontsize=11)
    if y_label:
        ax.set_ylabel("p(θ)", color=TEXT, fontsize=11)

    ax.tick_params(colors=DIM, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return samples_rounded


def plot_grid(cases: list[tuple]) -> None:
    """Render Beta cases on a 2-row grid:
       Row 1: skew case alone (Beta(8,3)) — non-symmetric, mean ≠ 0.5
       Row 2: four α=β cases — Beta(0.5,0.5), Beta(1,1), Beta(2,2), Beta(50,50)
              all with mean 0.5 but very different shapes.
    """
    case_map = {slug: (a, b) for slug, a, b, _ in cases}

    fig = plt.figure(figsize=(11.5, 7), dpi=150, facecolor=BG)
    gs = fig.add_gridspec(nrows=2, ncols=4, hspace=0.55, wspace=0.30,
                          height_ratios=[1, 1])

    # Row 1: skew case (Beta(8,3)) — span columns 1-2 (the middle two of 4) so
    # it sits centered with breathing room either side
    ax_top = fig.add_subplot(gs[0, 1:3])
    a, b = case_map["beta_concentrated_high"]
    _draw_panel(ax_top, a, b, x_label=True, y_label=True,
                samples_seed=42 + hash("beta_concentrated_high") % 1000)

    # Row 2: four same-mean (μ=0.5) cases in ascending α+β order to show
    # how concentration changes while the mean stays put.
    row2_order = ["beta_ushaped", "beta_uniform", "beta_wide", "beta_narrow"]
    for col, slug in enumerate(row2_order):
        a, b = case_map[slug]
        ax = fig.add_subplot(gs[1, col])
        _draw_panel(ax, a, b,
                    x_label=True,           # bottom row → all get x label
                    y_label=(col == 0),     # only leftmost → y label
                    samples_seed=42 + (zlib.crc32(slug.encode()) % 1000))

    # Annotation labels for the rows (left margin)
    fig.text(0.02, 0.76, "Skewed",
             color=DIM, fontsize=13, fontstyle="italic", rotation=90, va="center")
    fig.text(0.02, 0.27, "Mean = 0.5",
             color=DIM, fontsize=13, fontstyle="italic", rotation=90, va="center")

    out_path = OUT_DIR / "beta_grid.png"
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")


def main() -> None:
    print("Building Beta-case plots...")
    results = [plot_case(slug, a, b, lbl) for slug, a, b, lbl in CASES]
    plot_grid(CASES)
    # Write samples to JSON so the .qmd author can copy them in (and so we
    # have a record of which numbers landed on which slide).
    samples_path = OUT_DIR / "samples.json"
    samples_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  wrote {samples_path.relative_to(OUT_DIR.parent.parent.parent)}")
    print("Done.")


if __name__ == "__main__":
    main()
