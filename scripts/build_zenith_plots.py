#!/usr/bin/env python3
"""Reconstruct Griffiths & Tenenbaum (2001) Figure 1 in the SDS dark theme.

Two panels (Zenith data + Randomness model) rendered as separate PNGs so the
slide can lay them out side-by-side. Probabilities are eyeballed from the
published figure with reasonable precision (~2 decimal places) — accurate
enough for the lecture's "model fits the data" point.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BG = "#111111"
TEXT = "#FFFFFF"
ACCENT = "#64B5F6"   # blue for data
YELLOW = "#FFEB3B"   # yellow for model
DIM = "#999999"

OUT_DIR = Path(__file__).resolve().parent.parent / "course" / "week03_conjugate_bayes_topics" / "images"

# 16 sequences in the paper's Figure 1 order (initial choice ignored so 32 → 16)
LABELS = [
    "00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111",
    "01000", "01001", "01010", "01011", "01100", "01101", "01110", "01111",
]

# Eyeballed from Figure 1 of the paper. Top panel: empirical Zenith data.
# Bottom panel: model predictions with λ ≈ 0.6.
ZENITH_DATA = [
    0.009, 0.014, 0.044, 0.050, 0.057, 0.142, 0.118, 0.038,
    0.033, 0.087, 0.045, 0.057, 0.109, 0.117, 0.064, 0.020,
]
MODEL_PRED = [
    0.001, 0.012, 0.039, 0.050, 0.041, 0.121, 0.107, 0.029,
    0.019, 0.105, 0.158, 0.082, 0.087, 0.103, 0.046, 0.005,
]


def plot_panel(values: list[float], title: str, color: str, slug: str, *, show_xlabels: bool) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.4), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)

    x = np.arange(len(LABELS))
    ax.bar(x, values, color=color, edgecolor=color, width=0.75)

    ax.set_title(title, color=TEXT, fontsize=15, pad=10)
    ax.set_ylabel("Probability", color=TEXT, fontsize=12)
    ax.set_ylim(0, 0.20)
    ax.set_xticks(x)
    if show_xlabels:
        ax.set_xticklabels(LABELS, color=DIM, rotation=90, fontsize=9, family="monospace")
    else:
        ax.set_xticklabels([])

    ax.tick_params(colors=DIM, labelsize=10)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out_path = OUT_DIR / f"{slug}.png"
    fig.savefig(out_path, facecolor=BG, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.relative_to(OUT_DIR.parent.parent.parent)}")


def main() -> None:
    print("Building Zenith data + model panels...")
    plot_panel(ZENITH_DATA, "Zenith Radio Data (1937)", ACCENT, "gt2001_zenith_data", show_xlabels=True)
    plot_panel(MODEL_PRED, "Randomness model (λ = 0.6)", YELLOW, "gt2001_zenith_model", show_xlabels=True)
    print("Done.")


if __name__ == "__main__":
    main()
