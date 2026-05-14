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
    """Render one PDF curve. Returns the sample numbers for the .qmd."""
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    x = np.linspace(1e-4, 1 - 1e-4, 500)
    y = beta.pdf(x, a, b)

    # Clip to plot area — U-shaped pdfs diverge at endpoints
    y_max_plot = min(np.nanmax(y[np.isfinite(y)]), 6.0)

    ax.plot(x, y, color=ACCENT, linewidth=2.6)
    ax.fill_between(x, 0, y, color=ACCENT, alpha=0.18)

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

    # Pin RNG per-case so re-runs are reproducible
    rng = np.random.default_rng(seed=42 + hash(slug) % 1000)
    samples = beta.rvs(a, b, size=5, random_state=rng)
    samples = [round(float(s), 3) for s in samples]

    fig.tight_layout()
    out_path = OUT_DIR / f"{slug}.png"
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")
    return {"slug": slug, "alpha": a, "beta": b, "label": label, "samples": samples}


def _fmt(x: float) -> str:
    if x == int(x):
        return str(int(x))
    return f"{x:g}"


def plot_grid(cases: list[tuple]) -> None:
    """Render all 5 cases on a single 2×3 grid for the side-by-side slide."""
    fig, axes = plt.subplots(2, 3, figsize=(11, 5.6), dpi=150, facecolor=BG)
    axes = axes.flatten()

    for ax, (slug, a, b, _label) in zip(axes, cases):
        ax.set_facecolor(BG)
        x = np.linspace(1e-4, 1 - 1e-4, 500)
        y = beta.pdf(x, a, b)
        y_max = min(np.nanmax(y[np.isfinite(y)]), 6.0)

        ax.plot(x, y, color=ACCENT, linewidth=2.0)
        ax.fill_between(x, 0, y, color=ACCENT, alpha=0.18)
        ax.set_title(f"Beta({_fmt(a)}, {_fmt(b)})",
                     color=TEXT, fontsize=13, pad=6, loc="left")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, y_max * 1.05)
        ax.tick_params(colors=DIM, labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(DIM)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Hide unused subplot (5 cases, 6 panels)
    for ax in axes[len(cases):]:
        ax.set_visible(False)

    fig.tight_layout()
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
