#!/usr/bin/env python3
"""Generate the new DAG figures for the Week 5 lecture deck.

Each figure is emitted to ../images/<name>.png at 1600x1000 px with a dark
background and yellow accent edges, matching the sds-reveal theme.

Run:  python3 scripts/build_dags_week5.py
Output: course/week05_bayes_nets_causal/images/*.png
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

# ---- theme ---------------------------------------------------------------

BG = "#1a1a1a"          # slide background
FG = "#f4f4f4"          # primary text / strokes
DIM = "#888"            # secondary text / strokes
YELLOW = "#f4d35e"      # accent (sds-reveal yellow)
RED = "#e63946"         # cut / forbidden
NODE_FILL = "#2a2a2a"   # latent (unobserved/unconditioned) node background
NODE_OBS = "#cfcfcf"    # observed / conditioned-on node — strong light-gray contrast
NODE_OBS_TEXT = "#1a1a1a"  # dark label on the light observed node so the symbol stays readable
NODE_HIGHLIGHT = "#3a3a18"  # subtle yellow tint for highlighted nodes
EDGE_WIDTH = 2.2
NODE_LW = 2.0
FONT = {"family": "sans-serif", "color": FG}

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def new_fig(figsize=(8, 5)):
    fig, ax = plt.subplots(figsize=figsize, dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_aspect("equal")
    return fig, ax


def draw_node(ax, pos, label, *, observed=False, highlight=False,
              radius=0.42, fontsize=22, italic=False):
    x, y = pos
    fill = NODE_HIGHLIGHT if highlight else (NODE_OBS if observed else NODE_FILL)
    edge = YELLOW if highlight else FG
    # Observed nodes get a light fill, so the white-on-dark label flips to dark.
    # Highlighted nodes keep the dark tinted fill and the white label.
    text_color = NODE_OBS_TEXT if (observed and not highlight) else FG
    circ = plt.Circle((x, y), radius, facecolor=fill, edgecolor=edge,
                      linewidth=NODE_LW + (0.8 if highlight else 0.0),
                      zorder=3)
    ax.add_patch(circ)
    style = "italic" if italic else "normal"
    ax.text(x, y, label, ha="center", va="center", color=text_color,
            fontsize=fontsize, fontstyle=style, zorder=4)


def draw_plate(ax, x0, y0, x1, y1, label, *, label_pos="br"):
    """Draw a rounded plate (rectangle) with a small label.

    label_pos:
      "br"            inside bottom-right (default; for tight figures)
      "bl"            inside bottom-left
      "outside_br"    just below bottom-right edge (use when contents are
                      tight against the plate floor and an inside label
                      would overlap a node or an arrow)
      "outside_bl"    just below bottom-left edge
    """
    w, h = x1 - x0, y1 - y0
    box = FancyBboxPatch((x0, y0), w, h,
                         boxstyle="round,pad=0.08,rounding_size=0.18",
                         facecolor="none", edgecolor=DIM,
                         linewidth=1.4, linestyle="--", zorder=2)
    ax.add_patch(box)
    if label_pos == "br":
        ax.text(x1 - 0.18, y0 + 0.18, label, ha="right", va="bottom",
                color=DIM, fontsize=14, style="italic")
    elif label_pos == "bl":
        ax.text(x0 + 0.18, y0 + 0.18, label, ha="left", va="bottom",
                color=DIM, fontsize=14, style="italic")
    elif label_pos == "outside_br":
        ax.text(x1 - 0.05, y0 - 0.28, label, ha="right", va="top",
                color=DIM, fontsize=14, style="italic")
    elif label_pos == "outside_bl":
        ax.text(x0 + 0.05, y0 - 0.28, label, ha="left", va="top",
                color=DIM, fontsize=14, style="italic")
    elif label_pos == "outside_right":
        # To the right of the plate, vertically centered along its bottom edge.
        # Use when a vertical arrow exits the plate's bottom-center and would
        # cut through a centered outside-bottom label.
        ax.text(x1 + 0.15, y0 + 0.05, label, ha="left", va="bottom",
                color=DIM, fontsize=14, style="italic")


def draw_edge(ax, src, dst, *, color=None, lw=EDGE_WIDTH, style="-",
              shrink=0.42, label=None, label_offset=(0, 0), cut=False):
    """Draw an arrow from src→dst with proper shrink so it stops at node edges."""
    color = color or FG
    arrow = FancyArrowPatch(src, dst,
                            arrowstyle="-|>", mutation_scale=18,
                            color=color, linewidth=lw, linestyle=style,
                            shrinkA=shrink * 72, shrinkB=shrink * 72,
                            zorder=2)
    ax.add_patch(arrow)
    if cut:
        # Draw a red X over the midpoint
        mx, my = (src[0] + dst[0]) / 2, (src[1] + dst[1]) / 2
        s = 0.18
        for dx, dy in [(-s, -s), (-s, s)]:
            ax.plot([mx + dx, mx - dx], [my + dy, my - dy],
                    color=RED, linewidth=3, zorder=5)
    if label:
        mx, my = (src[0] + dst[0]) / 2, (src[1] + dst[1]) / 2
        ax.text(mx + label_offset[0], my + label_offset[1], label,
                ha="center", va="center", color=DIM, fontsize=14, style="italic")


def save(fig, name: str, *, pad=0.4):
    out = IMAGES_DIR / f"{name}.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=pad)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def set_limits(ax, xs, ys, margin=0.6):
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)


# ---- figures -------------------------------------------------------------


def fig_gmm_as_bn():
    """GMM drawn as a Bayes net: π → z_i → x_i with a plate over i."""
    fig, ax = new_fig(figsize=(9, 5.5))
    # Outside the plate: pi, mu/sigma
    pos_pi = (-2.4, 1.2)
    pos_mu = (-2.4, -1.2)
    # Inside the plate: z, x
    pos_z = (0.6, 1.2)
    pos_x = (0.6, -1.2)

    # Plate around z and x
    draw_plate(ax, -0.4, -2.0, 1.6, 2.0, label="i = 1, ..., N")

    draw_node(ax, pos_pi, r"$\pi$", italic=True, fontsize=26)
    draw_node(ax, pos_mu, r"$\mu_k,\sigma_k$", fontsize=18)
    draw_node(ax, pos_z, r"$z_i$", italic=True, fontsize=22)
    draw_node(ax, pos_x, r"$x_i$", observed=True, italic=True, fontsize=22)

    draw_edge(ax, pos_pi, pos_z)
    draw_edge(ax, pos_z, pos_x)
    draw_edge(ax, pos_mu, pos_x)

    # K plate around mu/sigma
    draw_plate(ax, -3.4, -2.0, -1.4, -0.4, label="k = 1, ..., K", label_pos="bl")

    set_limits(ax, [-3.4, 1.6], [-2.0, 2.0])
    save(fig, "gmm_as_bn")


def fig_gmm_with_hyperprior():
    """GMM + hyperprior: α → π → z_i → x_i; (μ₀, σ₀) → (μ_k, σ_k)."""
    fig, ax = new_fig(figsize=(10, 5.5))
    pos_alpha = (-4.6, 1.2)
    pos_pi = (-2.6, 1.2)
    pos_mu0 = (-4.6, -1.2)
    pos_mu = (-2.6, -1.2)
    pos_z = (0.4, 1.2)
    pos_x = (0.4, -1.2)

    draw_plate(ax, -0.6, -2.0, 1.4, 2.0, label="i = 1, ..., N")
    draw_plate(ax, -3.6, -2.0, -1.6, -0.4, label="k = 1, ..., K", label_pos="bl")

    # Hyperprior nodes: highlight in yellow per outline
    draw_node(ax, pos_alpha, r"$\alpha$", italic=True, fontsize=24, highlight=True)
    draw_node(ax, pos_mu0, r"$\mu_0,\sigma_0$", fontsize=16, highlight=True)
    draw_node(ax, pos_pi, r"$\pi$", italic=True, fontsize=26)
    draw_node(ax, pos_mu, r"$\mu_k,\sigma_k$", fontsize=18)
    draw_node(ax, pos_z, r"$z_i$", italic=True, fontsize=22)
    draw_node(ax, pos_x, r"$x_i$", observed=True, italic=True, fontsize=22)

    draw_edge(ax, pos_alpha, pos_pi, color=YELLOW)
    draw_edge(ax, pos_mu0, pos_mu, color=YELLOW)
    draw_edge(ax, pos_pi, pos_z)
    draw_edge(ax, pos_z, pos_x)
    draw_edge(ax, pos_mu, pos_x)

    set_limits(ax, [-4.6, 1.4], [-2.0, 2.0])
    save(fig, "gmm_with_hyperprior")


def fig_chibany_bento_bn():
    """Multi-parent: Weather, Day, Restaurant → Bento."""
    fig, ax = new_fig(figsize=(9, 5))
    pos_w = (-2.5, 1.6)
    pos_d = (0.0, 1.6)
    pos_r = (2.5, 1.6)
    pos_b = (0.0, -1.4)

    draw_node(ax, pos_w, "Weather", fontsize=15, radius=0.6)
    draw_node(ax, pos_d, "Day", fontsize=16, radius=0.55)
    draw_node(ax, pos_r, "Restaurant", fontsize=14, radius=0.7)
    draw_node(ax, pos_b, "Bento", fontsize=18, radius=0.6, highlight=True)

    draw_edge(ax, pos_w, pos_b)
    draw_edge(ax, pos_d, pos_b)
    draw_edge(ax, pos_r, pos_b)

    set_limits(ax, [-3.2, 3.2], [-2.0, 2.2])
    save(fig, "chibany_bento_bn")


def fig_chibany_monty_hall():
    """Collider: Tonkatsu → CafeteriaReveals ← ChibanyChooses."""
    fig, ax = new_fig(figsize=(9, 5))
    pos_t = (-2.6, 1.4)
    pos_c = (0.0, -1.4)
    pos_p = (2.6, 1.4)

    draw_node(ax, pos_t, "Tonkatsu", fontsize=14, radius=0.65)
    draw_node(ax, pos_c, "Cafeteria\nReveals", fontsize=13, radius=0.7)
    draw_node(ax, pos_p, "Chibany\nChooses", fontsize=13, radius=0.65)

    draw_edge(ax, pos_t, pos_c)
    draw_edge(ax, pos_p, pos_c)

    set_limits(ax, [-3.4, 3.4], [-2.2, 2.0])
    save(fig, "chibany_monty_hall")


def _three_node_skeleton(ax, positions, labels):
    for pos, lbl in zip(positions, labels):
        draw_node(ax, pos, lbl, italic=True, fontsize=26)


def fig_dsep_chain():
    """A → B → C; condition on B (shaded)."""
    fig, ax = new_fig(figsize=(9, 3.5))
    pa, pb, pc = (-2.8, 0), (0, 0), (2.8, 0)
    draw_node(ax, pa, "A", italic=True, fontsize=26)
    draw_node(ax, pb, "B", italic=True, fontsize=26, observed=True)
    draw_node(ax, pc, "C", italic=True, fontsize=26)
    draw_edge(ax, pa, pb)
    draw_edge(ax, pb, pc)
    ax.text(0, -1.4, "conditioning on B  →  A ⊥ C", ha="center", va="center",
            color=DIM, fontsize=18, style="italic")
    set_limits(ax, [-3.5, 3.5], [-2.0, 1.0])
    save(fig, "dsep_chain")


def fig_dsep_fork():
    """A ← B → C; condition on B (shaded)."""
    fig, ax = new_fig(figsize=(9, 3.8))
    pa, pb, pc = (-2.8, -0.6), (0, 1.0), (2.8, -0.6)
    draw_node(ax, pa, "A", italic=True, fontsize=26)
    draw_node(ax, pb, "B", italic=True, fontsize=26, observed=True)
    draw_node(ax, pc, "C", italic=True, fontsize=26)
    draw_edge(ax, pb, pa)
    draw_edge(ax, pb, pc)
    ax.text(0, -2.0, "conditioning on B  →  A ⊥ C", ha="center", va="center",
            color=DIM, fontsize=18, style="italic")
    set_limits(ax, [-3.5, 3.5], [-2.6, 1.8])
    save(fig, "dsep_fork")


def fig_dsep_collider():
    """A → B ← C; condition on B INDUCES dependence."""
    fig, ax = new_fig(figsize=(9, 3.8))
    pa, pb, pc = (-2.8, 1.0), (0, -0.6), (2.8, 1.0)
    draw_node(ax, pa, "A", italic=True, fontsize=26)
    draw_node(ax, pb, "B", italic=True, fontsize=26, observed=True, highlight=True)
    draw_node(ax, pc, "C", italic=True, fontsize=26)
    draw_edge(ax, pa, pb)
    draw_edge(ax, pc, pb)
    ax.text(0, -2.0, "conditioning on B  →  A and C become DEPENDENT",
            ha="center", va="center", color=YELLOW, fontsize=18, fontstyle="italic")
    set_limits(ax, [-3.5, 3.5], [-2.6, 1.8])
    save(fig, "dsep_collider")


def fig_markov_blanket():
    """5-node DAG with X's Markov blanket highlighted."""
    fig, ax = new_fig(figsize=(9, 6))
    # Layout: X in center; two parents above, one child below, one spouse
    pos_x = (0, 0)
    pos_p1 = (-2.0, 2.0)   # parent
    pos_p2 = (2.0, 2.0)    # parent
    pos_c  = (0, -2.2)     # child
    pos_s  = (2.0, -2.2)   # spouse (other parent of child)
    pos_far = (-3.3, -2.0) # unrelated node (outside blanket)

    # Blanket: parents (P1, P2), child (C), spouse (S) — highlight these
    draw_node(ax, pos_x, "X", italic=True, fontsize=26, highlight=True)
    draw_node(ax, pos_p1, "P₁", fontsize=22, highlight=True)
    draw_node(ax, pos_p2, "P₂", fontsize=22, highlight=True)
    draw_node(ax, pos_c, "Ch", fontsize=22, highlight=True)
    draw_node(ax, pos_s, "Sp", fontsize=22, highlight=True)
    draw_node(ax, pos_far, "Y", italic=True, fontsize=22)

    draw_edge(ax, pos_p1, pos_x)
    draw_edge(ax, pos_p2, pos_x)
    draw_edge(ax, pos_x, pos_c)
    draw_edge(ax, pos_s, pos_c)
    draw_edge(ax, pos_far, pos_p1)   # Y influences a parent but is NOT in blanket

    ax.text(0, 3.4, "Markov blanket of X = parents + children + co-parents",
            ha="center", va="center", color=YELLOW, fontsize=15, style="italic")
    set_limits(ax, [-3.8, 3.0], [-3.0, 3.8])
    save(fig, "markov_blanket")


def fig_do_setup():
    """Smoking confounder network — original."""
    fig, ax = new_fig(figsize=(9, 5))
    pos_s = (0, 1.6)
    pos_t = (-2.4, -1.4)
    pos_l = (2.4, -1.4)

    draw_node(ax, pos_s, "Smoke", fontsize=18, radius=0.65)
    draw_node(ax, pos_t, "Teeth", fontsize=18, radius=0.65)
    draw_node(ax, pos_l, "Lung\ncancer", fontsize=14, radius=0.65)

    draw_edge(ax, pos_s, pos_t)
    draw_edge(ax, pos_s, pos_l)

    ax.text(0, -2.6, "S confounds T and L", ha="center", va="center",
            color=DIM, fontsize=16, style="italic")
    set_limits(ax, [-3.3, 3.3], [-3.2, 2.6])
    save(fig, "do_setup")


def fig_do_cut():
    """do(T = white): cut S → T, set T directly."""
    fig, ax = new_fig(figsize=(9, 5))
    pos_s = (0, 1.6)
    pos_t = (-2.4, -1.4)
    pos_l = (2.4, -1.4)

    draw_node(ax, pos_s, "Smoke", fontsize=18, radius=0.65)
    draw_node(ax, pos_t, "T = white", fontsize=14, radius=0.7, highlight=True)
    draw_node(ax, pos_l, "Lung\ncancer", fontsize=14, radius=0.65)

    draw_edge(ax, pos_s, pos_t, cut=True, color=DIM, style="--")
    draw_edge(ax, pos_s, pos_l)

    ax.text(0, -2.6, "do(T = white)  →  arrow into T is cut",
            ha="center", va="center", color=YELLOW, fontsize=16, style="italic")
    set_limits(ax, [-3.3, 3.3], [-3.2, 2.6])
    save(fig, "do_cut")


def fig_do_compute():
    """After surgery: P(L | do(T)) reduces to P(L)."""
    fig, ax = new_fig(figsize=(9, 5))
    pos_s = (0, 1.6)
    pos_t = (-2.4, -1.4)
    pos_l = (2.4, -1.4)

    draw_node(ax, pos_s, "Smoke", fontsize=18, radius=0.65)
    draw_node(ax, pos_t, "T = white", fontsize=14, radius=0.7, highlight=True)
    draw_node(ax, pos_l, "Lung\ncancer", fontsize=14, radius=0.65, observed=True)

    # No edge from S to T (cut). S → L remains.
    draw_edge(ax, pos_s, pos_l)

    ax.text(0, -2.7,
            r"$P(L \mid do(T = \mathrm{white})) = P(L)$  —  T no longer informs about S",
            ha="center", va="center", color=YELLOW, fontsize=14, style="italic")
    set_limits(ax, [-3.3, 3.3], [-3.4, 2.6])
    save(fig, "do_compute")


def fig_do_vs_cond():
    """Side-by-side: P(L|T) on left (observational), P(L|do(T)) on right."""
    fig = plt.figure(figsize=(12, 5), dpi=200)
    fig.patch.set_facecolor(BG)

    for idx, (title, cut) in enumerate(
        [("Observe: $P(L \\mid T)$", False),
         ("Intervene: $P(L \\mid do(T))$", True)]
    ):
        ax = fig.add_subplot(1, 2, idx + 1)
        ax.set_facecolor(BG)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_aspect("equal")

        pos_s = (0, 1.4)
        pos_t = (-2.0, -1.2)
        pos_l = (2.0, -1.2)
        draw_node(ax, pos_s, "S", italic=True, fontsize=24)
        draw_node(ax, pos_t, "T", italic=True, fontsize=24,
                  highlight=cut, observed=True)
        draw_node(ax, pos_l, "L", italic=True, fontsize=24)

        if cut:
            draw_edge(ax, pos_s, pos_t, cut=True, color=DIM, style="--")
        else:
            draw_edge(ax, pos_s, pos_t)
        draw_edge(ax, pos_s, pos_l)

        ax.set_xlim(-3.0, 3.0); ax.set_ylim(-2.8, 2.4)
        ax.set_title(title, color=FG, fontsize=16, pad=14)

    fig.suptitle("", color=FG)
    out = IMAGES_DIR / "do_vs_cond.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def _draw_bn_param_count_base(ax):
    """Shared scaffold for the param-count figure: nodes, edges, factor labels.

    Returns the four node positions so caller can place per-node counts.
    """
    pos_x4 = (-2.8, 1.6)
    pos_x3 = (2.0, 1.6)
    pos_x1 = (-1.4, -1.4)
    pos_x2 = (3.2, -1.4)

    draw_node(ax, pos_x4, r"$X_4$", italic=True, fontsize=22)
    draw_node(ax, pos_x3, r"$X_3$", italic=True, fontsize=22)
    draw_node(ax, pos_x1, r"$X_1$", italic=True, fontsize=22)
    draw_node(ax, pos_x2, r"$X_2$", italic=True, fontsize=22)

    draw_edge(ax, pos_x4, pos_x1)
    draw_edge(ax, pos_x3, pos_x1)
    draw_edge(ax, pos_x3, pos_x2)

    # Conditional factor labels under nodes (dim, present on both variants)
    ax.text(pos_x4[0] - 1.0, pos_x4[1] - 0.05, r"$P(x_4)$",
            color=DIM, fontsize=15, ha="right", va="center")
    ax.text(pos_x3[0] + 1.0, pos_x3[1] - 0.05, r"$P(x_3)$",
            color=DIM, fontsize=15, ha="left", va="center")
    ax.text(pos_x1[0] - 1.0, pos_x1[1] - 0.05, r"$P(x_1\,|\,x_3,x_4)$",
            color=DIM, fontsize=15, ha="right", va="center")
    ax.text(pos_x2[0] + 1.0, pos_x2[1] - 0.05, r"$P(x_2\,|\,x_3)$",
            color=DIM, fontsize=15, ha="left", va="center")

    set_limits(ax, [-4.0, 4.4], [-3.4, 2.6])
    return pos_x4, pos_x3, pos_x1, pos_x2


def fig_bn_param_count():
    """4-node psychic-friend network with per-node parameter counts (full reveal).

    Pearl-style example: X1 = coin-toss-heads; X2 = pencil-levitates;
    X3 = friend-has-psychic-powers; X4 = friend-has-two-headed-coin.
    Bayes net needs 1 + 1 + 4 + 2 = 8 numbers vs. 15 for the full joint.
    """
    fig, ax = new_fig(figsize=(10, 5.5))
    pos_x4, pos_x3, pos_x1, pos_x2 = _draw_bn_param_count_base(ax)

    # Per-node parameter counts (yellow numbers next to each node)
    ax.text(pos_x4[0] - 0.8, pos_x4[1] + 0.7, "1", color=YELLOW,
            fontsize=24, fontweight="bold", ha="center")
    ax.text(pos_x3[0] + 0.8, pos_x3[1] + 0.7, "1", color=YELLOW,
            fontsize=24, fontweight="bold", ha="center")
    ax.text(pos_x1[0] - 0.8, pos_x1[1] - 0.7, "4", color=YELLOW,
            fontsize=24, fontweight="bold", ha="center")
    ax.text(pos_x2[0] + 0.8, pos_x2[1] - 0.7, "2", color=YELLOW,
            fontsize=24, fontweight="bold", ha="center")

    ax.text(0.7, -2.7, r"total = 8   (vs. 15)", color=YELLOW,
            fontsize=22, fontweight="bold", ha="center", style="italic")

    save(fig, "bn_param_count")


def fig_bn_param_count_question():
    """4-node Bayes net with conditional-factor labels but NO parameter counts
    and NO total. Companion to fig_bn_param_count — used as the question-side
    slide so the count answer isn't pre-revealed."""
    fig, ax = new_fig(figsize=(10, 5.5))
    _draw_bn_param_count_base(ax)
    save(fig, "bn_param_count_question")


def _explaining_away_frame(rain_state, sprinkler_state, wet_state,
                           wet_observed, *, caption, filename):
    """One frame of the Sprinkler/Rain/Wet-Grass explaining-away build-up.

    State strings can be "?" (unknown), "yes", or "no".  wet_observed=True
    makes the Wet node shaded.
    """
    fig, ax = new_fig(figsize=(9, 5.5))
    pos_r = (-2.4, 1.4)
    pos_s = (2.4, 1.4)
    pos_w = (0.0, -1.4)

    # Node labels
    def fmt(name, val):
        if val == "?":
            return name
        return f"{name}\n= {val}"

    # Highlight a node if its value is known and not "?"
    rain_highlight = rain_state != "?"
    sprinkler_highlight = sprinkler_state != "?"

    draw_node(ax, pos_r, fmt("Rain", rain_state), fontsize=14, radius=0.65,
              highlight=rain_highlight)
    draw_node(ax, pos_s, fmt("Sprinkler", sprinkler_state), fontsize=12,
              radius=0.75, highlight=sprinkler_highlight)
    draw_node(ax, pos_w, fmt("Wet grass", wet_state), fontsize=13,
              radius=0.7, observed=wet_observed,
              highlight=wet_observed)

    draw_edge(ax, pos_r, pos_w)
    draw_edge(ax, pos_s, pos_w)

    ax.text(0, -2.9, caption, ha="center", va="center",
            color=YELLOW, fontsize=15, style="italic")
    set_limits(ax, [-3.4, 3.4], [-3.6, 2.4])
    save(fig, filename)


def fig_explaining_away():
    """3-frame Sprinkler/Rain/Wet-Grass explaining-away build-up."""
    _explaining_away_frame(
        "?", "?", "?", False,
        caption="Rain and Sprinkler are independent a priori",
        filename="explaining_away_1",
    )
    _explaining_away_frame(
        "?", "?", "yes", True,
        caption="Observe wet grass → P(Rain) AND P(Sprinkler) both go up",
        filename="explaining_away_2",
    )
    _explaining_away_frame(
        "?", "yes", "yes", True,
        caption="Also observe Sprinkler = yes → P(Rain) drops back ('explained away')",
        filename="explaining_away_3",
    )


def fig_smoking_confound():
    """Two structures with identical observations — observation alone can't tell."""
    fig = plt.figure(figsize=(11, 5), dpi=200)
    fig.patch.set_facecolor(BG)

    # Left panel: smoking causes both
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_facecolor(BG); ax1.set_xticks([]); ax1.set_yticks([])
    for s in ax1.spines.values(): s.set_visible(False)
    ax1.set_aspect("equal")
    pos_s, pos_t, pos_l = (0, 1.4), (-2.0, -1.2), (2.0, -1.2)
    draw_node(ax1, pos_s, "Smoking", fontsize=14, radius=0.65)
    draw_node(ax1, pos_t, "Yellow\nteeth", fontsize=13, radius=0.65)
    draw_node(ax1, pos_l, "Lung\ncancer", fontsize=13, radius=0.65)
    draw_edge(ax1, pos_s, pos_t)
    draw_edge(ax1, pos_s, pos_l)
    ax1.set_title("Correct: smoking confounds", color=YELLOW,
                  fontsize=15, pad=10, fontstyle="italic")
    ax1.set_xlim(-3.0, 3.0); ax1.set_ylim(-2.6, 2.6)

    # Right panel: teeth-causes-cancer (the wrong story; arrow X'd)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_facecolor(BG); ax2.set_xticks([]); ax2.set_yticks([])
    for s in ax2.spines.values(): s.set_visible(False)
    ax2.set_aspect("equal")
    draw_node(ax2, pos_s, "Smoking", fontsize=14, radius=0.65)
    draw_node(ax2, pos_t, "Yellow\nteeth", fontsize=13, radius=0.65)
    draw_node(ax2, pos_l, "Lung\ncancer", fontsize=13, radius=0.65)
    draw_edge(ax2, pos_s, pos_l)
    # Direct teeth→cancer with X (the seductive wrong story)
    draw_edge(ax2, pos_t, pos_l, cut=True, color=DIM, style="--")
    ax2.set_title("Wrong: teeth → cancer directly", color=RED,
                  fontsize=15, pad=10, fontstyle="italic")
    ax2.set_xlim(-3.0, 3.0); ax2.set_ylim(-2.6, 2.6)

    fig.suptitle("Same observations ↔ different structures",
                 color=FG, fontsize=18, y=0.05)
    out = IMAGES_DIR / "smoking_confound.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.5)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def _draw_detector(ax, center, *, lit=False, blocks=None, scale=1.0):
    """Schematic blicket detector: a flat box with a colored top panel,
    and optionally 1-2 blocks placed on top.

    blocks: list of (label, color) tuples for blocks sitting on the detector.
    lit: whether the detector's top "light" panel is glowing yellow (on).
    """
    cx, cy = center
    w, h = 1.6 * scale, 0.5 * scale
    # Detector body (slate gray)
    body = Rectangle((cx - w/2, cy - h/2), w, h,
                     facecolor="#3a3a3a", edgecolor=FG, linewidth=1.6,
                     zorder=2)
    ax.add_patch(body)
    # Top panel (lit or unlit)
    panel_color = YELLOW if lit else "#222"
    panel = Rectangle((cx - w/2 + 0.05, cy + h/2 - 0.08), w - 0.1, 0.16,
                      facecolor=panel_color, edgecolor=FG, linewidth=1.0,
                      zorder=3)
    ax.add_patch(panel)
    # Blocks on top (small colored rectangles)
    if blocks:
        n = len(blocks)
        spacing = (w - 0.2) / max(n, 1)
        start = cx - (n - 1) * spacing / 2
        for i, (label, color) in enumerate(blocks):
            bx = start + i * spacing
            by = cy + h/2 + 0.08
            block = Rectangle((bx - 0.18, by), 0.36, 0.4 * scale,
                              facecolor=color, edgecolor=FG, linewidth=1.4,
                              zorder=4)
            ax.add_patch(block)
            ax.text(bx, by + 0.2 * scale, label, ha="center", va="center",
                    color="white", fontsize=14, fontweight="bold", zorder=5)


def fig_blicket_detector():
    """Schematic 'blicket detector' explainer slide."""
    fig, ax = new_fig(figsize=(11, 4.5))
    # Three states left-to-right: empty detector / block on / block on (lit)
    _draw_detector(ax, (-3.8, 0), lit=False)
    ax.text(-3.8, -1.0, "empty detector", ha="center", va="center",
            color=FG, fontsize=14)

    _draw_detector(ax, (0, 0), lit=False,
                   blocks=[("A", "#5b89c7")])
    ax.text(0, -1.0, "place block A —\ndetector OFF", ha="center", va="center",
            color=FG, fontsize=14)

    _draw_detector(ax, (3.8, 0), lit=True,
                   blocks=[("B", "#d97a3b")])
    ax.text(3.8, -1.0, "place block B —\ndetector ON", ha="center", va="center",
            color=YELLOW, fontsize=14)

    ax.text(0, 2.2,
            'A "blicket" is whatever makes the detector light up',
            ha="center", va="center", color=FG, fontsize=16, style="italic")
    ax.set_xlim(-6.5, 6.5); ax.set_ylim(-2.0, 2.8)
    save(fig, "blicket_detector")


def fig_blicket_backwards_blocking():
    """The Sobel et al. backwards-blocking 2-trial setup."""
    fig, ax = new_fig(figsize=(11, 4.5))
    # Trial 1: A + B together → ON
    _draw_detector(ax, (-3.0, 0), lit=True,
                   blocks=[("A", "#5b89c7"), ("B", "#d97a3b")])
    ax.text(-3.0, -1.1, "Trial 1: A + B → ON", ha="center", va="center",
            color=FG, fontsize=14)

    # Trial 2: A alone → ON
    _draw_detector(ax, (3.0, 0), lit=True,
                   blocks=[("A", "#5b89c7")])
    ax.text(3.0, -1.1, "Trial 2: A alone → ON", ha="center", va="center",
            color=FG, fontsize=14)

    # Conclusion (yellow caption)
    ax.text(0, 2.2,
            "Backwards blocking: by Trial 2, kids infer A is a blicket and B probably isn't",
            ha="center", va="center", color=YELLOW, fontsize=14, style="italic")
    ax.set_xlim(-6.5, 6.5); ax.set_ylim(-2.0, 2.8)
    save(fig, "blicket_backwards_blocking")


def fig_blicket_taught_prior():
    """Adult backwards-blocking with a TAUGHT prior on the base rate of blickets.

    Design (Sobel, Tenenbaum & Gopnik 2004 / Griffiths-Sobel followups):
    before the AB→A trials, adults see ~12 demonstration blocks where roughly
    25% (rare-prior condition) OR 75% (common-prior condition) of arbitrary
    blocks turn on the detector. THEN they see the classic AB→A backwards-
    blocking sequence and rate P(B is a blicket).

    The key test is whether P(B) after the A-alone trial returns toward the
    TAUGHT base rate — that's the Bayesian prediction (posterior over B
    relaxes back toward the prior once A explains away the AB observation)
    and the associative-learning prediction is uniform low confidence in B
    regardless of the taught rate.

    Numbers are qualitative re-creations of Fig. 4-style results in the
    backwards-blocking-with-taught-prior paradigm.
    """
    import numpy as np
    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    conditions = ["Rare prior\n(~25% blickets)", "Common prior\n(~75% blickets)"]
    model_vals = [0.27, 0.72]   # Bayesian posterior on B after A-alone trial
    human_vals = [0.31, 0.68]   # Adult ratings
    prior_vals = [0.25, 0.75]   # The taught base rate

    x = np.arange(len(conditions))
    width = 0.32

    # Bayes-net model bars (yellow)
    ax.bar(x - width / 2, model_vals, width,
           color=YELLOW, edgecolor=FG, linewidth=1.2,
           label="Bayes-net model")
    # Human bars (blue)
    ax.bar(x + width / 2, human_vals, width,
           color="#5b89c7", edgecolor=FG, linewidth=1.2,
           label="Adults' judgments")

    # Taught-prior reference lines per condition
    for xi, p in zip(x, prior_vals):
        ax.plot([xi - 0.55, xi + 0.55], [p, p],
                color=DIM, linewidth=2, linestyle="--", zorder=1)
        ax.text(xi + 0.58, p, f"taught prior = {p:.2f}",
                color=DIM, fontsize=10, va="center", fontstyle="italic")

    # Numeric labels above each bar
    for xi, m, h in zip(x, model_vals, human_vals):
        ax.text(xi - width / 2, m + 0.025, f"{m:.2f}",
                color=FG, fontsize=12, ha="center", va="bottom", fontweight="bold")
        ax.text(xi + width / 2, h + 0.025, f"{h:.2f}",
                color=FG, fontsize=12, ha="center", va="bottom", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(conditions, color=FG, fontsize=12)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("P(B is a blicket)  after the A-alone trial",
                  color=FG, fontsize=12)
    ax.tick_params(colors=FG)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.grid(True, axis="y", color=DIM, alpha=0.3, linewidth=0.7)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=FG, fontsize=11,
              loc="upper left")

    ax.set_title(
        "P(B) returns toward the taught prior — for both model and humans",
        color=YELLOW, fontsize=14, pad=10, fontstyle="italic"
    )

    fig.text(0.5, 0.01,
             "Adults shown a base-rate-teaching phase before the AB→A blicket sequence.",
             color=DIM, fontsize=10, ha="center", fontstyle="italic")

    out = IMAGES_DIR / "blicket_taught_prior.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def fig_blicket_model_human():
    """Side-by-side line graphs: model predictions vs. human (children) judgments."""
    import numpy as np
    fig = plt.figure(figsize=(11, 4.5), dpi=200)
    fig.patch.set_facecolor(BG)

    conditions = ["Initial", "After AB", "After A"]
    # Stylized data — qualitative match to Sobel/Tenenbaum/Gopnik 2004 results
    model_A = [0.20, 0.55, 0.95]
    model_B = [0.20, 0.55, 0.30]
    human_A = [0.25, 0.50, 0.95]
    human_B = [0.25, 0.50, 0.34]

    for idx, (title, A_data, B_data) in enumerate(
        [("Model predictions", model_A, model_B),
         ("Children's judgments", human_A, human_B)]
    ):
        ax = fig.add_subplot(1, 2, idx + 1)
        ax.set_facecolor(BG)
        x = list(range(len(conditions)))
        ax.plot(x, A_data, "o-", color=YELLOW, linewidth=2.5,
                markersize=10, label="Object A")
        ax.plot(x, B_data, "s--", color="#5b89c7", linewidth=2.5,
                markersize=10, label="Object B")
        ax.set_xticks(x)
        ax.set_xticklabels(conditions, color=FG, fontsize=12)
        ax.set_ylim(0, 1.0)
        ax.set_ylabel("P(blicket)", color=FG, fontsize=13)
        ax.set_title(title, color=FG, fontsize=14, pad=8)
        ax.tick_params(colors=FG)
        for spine in ax.spines.values():
            spine.set_color(DIM)
        ax.grid(True, color=DIM, alpha=0.3, linewidth=0.7)
        ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=FG, fontsize=11)

    fig.suptitle("Children's causal inferences match the Bayes-net model",
                 color=YELLOW, fontsize=15, y=1.0, fontstyle="italic")
    out = IMAGES_DIR / "blicket_model_human.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


# ---- GMM generative-process build-up (Week 5 opening) -------------------
#
# Each figure pairs a small visual plot (left) with the graphical-model
# fragment built so far (right), so students see the link between the
# generative-process line they wrote in Clusters and its node in the DAG.

def _dark_axes(ax):
    """Apply the deck's dark theme to a matplotlib axes."""
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.tick_params(colors=FG)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)


def _gauss_pdf(x, mu, sigma):
    norm = 1.0 / (sigma * math.sqrt(2 * math.pi))
    return [norm * math.exp(-0.5 * ((xi - mu) / sigma) ** 2) for xi in x]


def _draw_split_panels(fig, plot_fn, dag_fn, plot_title=None, dag_title=None):
    """Two-panel layout: visual plot on the left, DAG fragment on the right.

    Shared dark theme; plot panel has matplotlib axes; DAG panel is a clean
    SVG-style axes (no spines, no ticks).
    """
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.08)
    ax_plot = fig.add_subplot(gs[0, 0])
    ax_dag = fig.add_subplot(gs[0, 1])
    ax_plot.set_facecolor(BG)
    ax_dag.set_facecolor(BG)
    if plot_title:
        ax_plot.set_title(plot_title, color=FG, fontsize=15, pad=10,
                          fontstyle="italic")
    if dag_title:
        ax_dag.set_title(dag_title, color=FG, fontsize=15, pad=10,
                         fontstyle="italic")
    # Strip DAG axes
    ax_dag.set_xticks([]); ax_dag.set_yticks([])
    for s in ax_dag.spines.values():
        s.set_visible(False)
    ax_dag.set_aspect("equal")
    return ax_plot, ax_dag


def _bernoulli_bar(ax, theta=0.6, highlight=None):
    """Two bars showing P(c=1)=theta and P(c=2)=1-theta.

    Bars themselves keep their original blue/orange colors regardless of
    highlight (so the sampling action between Step 1 and Step 2 reads as
    *highlight added*, not *colors changed*).  When highlight is 1 or 2,
    a yellow box is drawn around the chosen bar and a thick yellow arrow
    points down at its top.
    """
    _dark_axes(ax)
    cats = ["c = 1", "c = 2"]
    vals = [theta, 1.0 - theta]
    # Bars: always the same blue/orange — DO NOT recolor on highlight.
    bar_colors = ["#5b89c7", "#d97a3b"]
    bars = ax.bar(cats, vals, color=bar_colors, edgecolor=FG,
                  linewidth=1.8, width=0.55)
    for i, (b, v) in enumerate(zip(bars, vals)):
        label = (f"θ = {theta:.1f}" if i == 0 else f"1 − θ = {1-theta:.1f}")
        ax.text(b.get_x() + b.get_width() / 2, v + 0.03, label,
                ha="center", va="bottom", color=FG, fontsize=14)
    # Highlight: yellow box around the chosen bar + downward arrow above it.
    if highlight in (1, 2):
        idx = highlight - 1
        b = bars[idx]
        v = vals[idx]
        x0, x1 = b.get_x() - 0.06, b.get_x() + b.get_width() + 0.06
        y0, y1 = -0.03, v + 0.14
        # Yellow selection box
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0,
                               facecolor="none", edgecolor=YELLOW,
                               linewidth=3.0, zorder=4))
        # Downward arrow pointing at the top of the bar
        arrow_top_y = v + 0.32
        ax.annotate("", xy=(b.get_x() + b.get_width() / 2, v + 0.16),
                    xytext=(b.get_x() + b.get_width() / 2, arrow_top_y),
                    arrowprops=dict(arrowstyle="-|>", color=YELLOW,
                                    lw=3.5, mutation_scale=22),
                    zorder=5)
        # "sampled!" label next to the arrow tail
        ax.text(b.get_x() + b.get_width() / 2 + 0.18, arrow_top_y - 0.02,
                f"c_n = {highlight}", color=YELLOW, fontsize=15,
                fontweight="bold", va="center", ha="left", zorder=5)
    ax.set_ylim(0, 1.25)
    ax.set_ylabel("P(c)", color=FG, fontsize=13)


def _two_gaussians(ax, mu1=-1, mu2=1, s1=0.7, s2=0.7,
                   highlight=None, sample_x=None):
    """Two-Gaussian density plot with optional highlight and sampled point."""
    _dark_axes(ax)
    n = 400
    lo, hi = min(mu1, mu2) - 4 * max(s1, s2), max(mu1, mu2) + 4 * max(s1, s2)
    xs = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    y1 = _gauss_pdf(xs, mu1, s1)
    y2 = _gauss_pdf(xs, mu2, s2)
    c1 = YELLOW if highlight == 1 else "#5b89c7"
    c2 = YELLOW if highlight == 2 else "#d97a3b"
    lw1 = 3.2 if highlight == 1 else 2.0
    lw2 = 3.2 if highlight == 2 else 2.0
    ax.plot(xs, y1, color=c1, linewidth=lw1,
            label=f"N(μ₁={mu1}, σ₁²={s1**2:.2f})")
    ax.plot(xs, y2, color=c2, linewidth=lw2,
            label=f"N(μ₂={mu2}, σ₂²={s2**2:.2f})")
    # Sticks at the means
    peak1 = max(y1); peak2 = max(y2)
    ax.vlines(mu1, 0, peak1, color=c1, linewidth=1.5,
              linestyles="--", alpha=0.7)
    ax.vlines(mu2, 0, peak2, color=c2, linewidth=1.5,
              linestyles="--", alpha=0.7)
    ax.text(mu1, -0.04, f"μ₁={mu1}", color=c1, ha="center", va="top",
            fontsize=12)
    ax.text(mu2, -0.04, f"μ₂={mu2}", color=c2, ha="center", va="top",
            fontsize=12)
    if sample_x is not None:
        sample_y = (peak1 if highlight == 1 else peak2) * 0.15
        ax.scatter([sample_x], [sample_y], color=YELLOW, s=180,
                   edgecolor=FG, linewidth=1.8, zorder=5)
        ax.annotate(f"x = {sample_x:.1f}", xy=(sample_x, sample_y),
                    xytext=(sample_x + 0.5, sample_y + 0.1),
                    color=YELLOW, fontsize=14, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=1.5))
    ax.set_xlabel("x", color=FG, fontsize=13)
    ax.set_ylabel("density", color=FG, fontsize=13)
    ax.legend(facecolor=BG, edgecolor=DIM, labelcolor=FG, fontsize=11,
              loc="upper right")
    ax.set_ylim(-0.08, max(max(y1), max(y2)) * 1.25)


def _dag_node_at(ax, xy, label, *, observed=False, highlight=False,
                 radius=0.42, fontsize=20, italic=True):
    """Draw a DAG node directly with matplotlib (no shared deps issue)."""
    x, y = xy
    fill = NODE_HIGHLIGHT if highlight else (NODE_OBS if observed else NODE_FILL)
    edge = YELLOW if highlight else FG
    lw = NODE_LW + (0.8 if highlight else 0.0)
    circ = plt.Circle((x, y), radius, facecolor=fill, edgecolor=edge,
                      linewidth=lw, zorder=3)
    ax.add_patch(circ)
    style = "italic" if italic else "normal"
    ax.text(x, y, label, ha="center", va="center", color=FG,
            fontsize=fontsize, fontstyle=style, zorder=4)


def _dag_edge(ax, src, dst, *, color=None, lw=EDGE_WIDTH, style="-",
              shrink=0.42):
    color = color or FG
    arrow = FancyArrowPatch(src, dst, arrowstyle="-|>", mutation_scale=16,
                            color=color, linewidth=lw, linestyle=style,
                            shrinkA=shrink * 72, shrinkB=shrink * 72, zorder=2)
    ax.add_patch(arrow)


def fig_gmm_step1_theta():
    """Step 1: introduce θ. Bernoulli bars + single θ node."""
    fig = plt.figure(figsize=(12, 5), dpi=150)
    fig.patch.set_facecolor(BG)
    ax_plot, ax_dag = _draw_split_panels(
        fig,
        plot_fn=None, dag_fn=None,
        plot_title="P(c = 1) = θ  (a Bernoulli prior)",
        dag_title="The graph so far",
    )
    _bernoulli_bar(ax_plot, theta=0.6)
    _dag_node_at(ax_dag, (0, 0), "θ", italic=True, fontsize=28, highlight=True)
    ax_dag.set_xlim(-2.2, 2.2); ax_dag.set_ylim(-2.0, 2.0)
    ax_dag.text(0, -1.4, "one node: θ", ha="center", color=DIM,
                fontsize=13, style="italic")
    fig.suptitle(r"Step 1:  $\theta$  (prior on category)",
                 color=YELLOW, fontsize=18, y=1.02, fontstyle="italic")
    out = IMAGES_DIR / "gmm_step1_theta.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def fig_gmm_step2_sample_c():
    """Step 2: c_n ~ Bernoulli(θ). Highlight a chosen bar; add c_n node + arrow."""
    fig = plt.figure(figsize=(12, 5), dpi=150)
    fig.patch.set_facecolor(BG)
    ax_plot, ax_dag = _draw_split_panels(
        fig,
        plot_fn=None, dag_fn=None,
        plot_title="Sample  c_n ~ Bernoulli(θ)  →  c_n = 1",
        dag_title="θ → c_n",
    )
    _bernoulli_bar(ax_plot, theta=0.6, highlight=1)
    pos_theta = (-1.2, 0.6)
    pos_c = (1.2, 0.6)
    _dag_node_at(ax_dag, pos_theta, "θ", italic=True, fontsize=24)
    _dag_node_at(ax_dag, pos_c, r"$c_n$", italic=True, fontsize=22,
                 highlight=True)
    _dag_edge(ax_dag, pos_theta, pos_c, color=YELLOW)
    ax_dag.set_xlim(-2.4, 2.4); ax_dag.set_ylim(-2.0, 2.0)
    ax_dag.text(0, -1.4, "arrow: θ generates c_n", ha="center", color=DIM,
                fontsize=13, style="italic")
    fig.suptitle(r"Step 2:  sample $c_n \sim \mathrm{Bernoulli}(\theta)$",
                 color=YELLOW, fontsize=18, y=1.02, fontstyle="italic")
    out = IMAGES_DIR / "gmm_step2_sample_c.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def fig_gmm_step3_gaussians():
    """Step 3: introduce μ_k, σ_k. Two Gaussians + parameter nodes."""
    fig = plt.figure(figsize=(12, 5), dpi=150)
    fig.patch.set_facecolor(BG)
    ax_plot, ax_dag = _draw_split_panels(
        fig,
        plot_fn=None, dag_fn=None,
        plot_title="Two Gaussian components: μ₁=−1, μ₂=+1",
        dag_title="add (μ₁, σ₁²) and (μ₂, σ₂²)",
    )
    _two_gaussians(ax_plot, mu1=-1, mu2=1, s1=0.7, s2=0.7)
    # DAG: theta, c_n, plus two parameter nodes (no edges into c yet — still building)
    pos_theta = (-1.6, 1.2)
    pos_c = (0.4, 1.2)
    pos_mu1 = (-1.6, -1.2)
    pos_mu2 = (1.0, -1.2)
    _dag_node_at(ax_dag, pos_theta, "θ", italic=True, fontsize=22)
    _dag_node_at(ax_dag, pos_c, r"$c_n$", italic=True, fontsize=20)
    _dag_node_at(ax_dag, pos_mu1, r"$\mu_1,\sigma_1^2$", italic=False,
                 fontsize=14, radius=0.55, highlight=True)
    _dag_node_at(ax_dag, pos_mu2, r"$\mu_2,\sigma_2^2$", italic=False,
                 fontsize=14, radius=0.55, highlight=True)
    _dag_edge(ax_dag, pos_theta, pos_c)
    ax_dag.set_xlim(-2.6, 2.4); ax_dag.set_ylim(-2.0, 2.0)
    ax_dag.text(-0.3, -1.95, "two new parameter nodes", ha="center", color=DIM,
                fontsize=12, style="italic")
    fig.suptitle(r"Step 3:  introduce  $(\mu_1, \sigma_1^2),  (\mu_2, \sigma_2^2)$",
                 color=YELLOW, fontsize=18, y=1.02, fontstyle="italic")
    out = IMAGES_DIR / "gmm_step3_gaussians.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def fig_gmm_step4_sample_x():
    """Step 4: x_n ~ N(μ_{c(n)}, σ²_{c(n)}). Sample point under chosen Gaussian + arrows.

    DAG layout (uncluttered):
        θ (top-left)    c_n (top-center)
                            ↓
        μ₁,σ₁² (bot-left) → x_n ← μ₂,σ₂² (bot-right)
    """
    fig = plt.figure(figsize=(12, 5), dpi=150)
    fig.patch.set_facecolor(BG)
    ax_plot, ax_dag = _draw_split_panels(
        fig,
        plot_fn=None, dag_fn=None,
        plot_title="Sample  x_n ~ N(μ₁, σ₁²)  (because c_n = 1)",
        dag_title="c_n → x_n   and   (μ_k,σ_k²) → x_n",
    )
    _two_gaussians(ax_plot, mu1=-1, mu2=1, s1=0.7, s2=0.7,
                   highlight=1, sample_x=-0.8)
    # DAG: 3-row layout with parameter nodes on the OUTER sides of x_n.
    pos_theta = (-1.6, 1.6)
    pos_c     = ( 0.0, 1.6)
    pos_x     = ( 0.0, -1.0)
    pos_mu1   = (-2.4, -1.0)
    pos_mu2   = ( 2.4, -1.0)
    _dag_node_at(ax_dag, pos_theta, "θ", italic=True, fontsize=22)
    _dag_node_at(ax_dag, pos_c, r"$c_n$", italic=True, fontsize=20)
    _dag_node_at(ax_dag, pos_mu1, r"$\mu_1,\sigma_1^2$", italic=False,
                 fontsize=12, radius=0.6)
    _dag_node_at(ax_dag, pos_mu2, r"$\mu_2,\sigma_2^2$", italic=False,
                 fontsize=12, radius=0.6)
    _dag_node_at(ax_dag, pos_x, r"$x_n$", italic=True, fontsize=20,
                 observed=True, highlight=True)
    _dag_edge(ax_dag, pos_theta, pos_c)
    _dag_edge(ax_dag, pos_c, pos_x, color=YELLOW)
    _dag_edge(ax_dag, pos_mu1, pos_x, color=YELLOW)
    _dag_edge(ax_dag, pos_mu2, pos_x, color=YELLOW)
    ax_dag.set_xlim(-3.4, 3.4); ax_dag.set_ylim(-2.0, 2.5)
    fig.suptitle(r"Step 4:  sample $x_n \sim \mathrm{N}(\mu_{c_n}, \sigma^2_{c_n})$",
                 color=YELLOW, fontsize=18, y=1.02, fontstyle="italic")
    out = IMAGES_DIR / "gmm_step4_sample_x.png"
    fig.savefig(out, facecolor=BG, edgecolor="none", bbox_inches="tight",
                pad_inches=0.4)
    plt.close(fig)
    print(f"  wrote {out.relative_to(IMAGES_DIR.parent.parent)}")


def fig_gmm_step5_unrolled():
    """Step 5: N copies of (c_n, x_n) drawn explicitly (no plate yet).

    Layout (3 rows):
        θ at top-center           (1 node)
        c_1 c_2 c_3 ... c_N       (per-datum row)
        x_1 x_2 x_3 ... x_N       (per-datum row, shaded)
        (μ_1,σ_1²)   (μ_2,σ_2²)   (shared parameters at bottom)

    Arrows: θ→c_n (fan down from top), c_n→x_n (short vertical),
    μ_k→x_n (fan up from bottom). All edges short, no crossings between
    parameter arrows and per-datum arrows.
    """
    fig, ax = new_fig(figsize=(12, 6.5))

    # Per-datum x positions: 3 copies + ellipsis + Nth
    x_positions = [-3.0, -1.4, 0.2]
    pos_theta = (-1.4, 2.4)
    pos_mu1 = (-1.4, -2.4)
    pos_mu2 = (1.4, -2.4)
    pos_ellipsis = (1.3, -0.5)
    pos_cN = (2.4, 0.6)
    pos_xN = (2.4, -1.4)

    _dag_node_at(ax, pos_theta, "θ", italic=True, fontsize=22, radius=0.36)
    _dag_node_at(ax, pos_mu1, r"$\mu_1,\sigma_1^2$", italic=False,
                 fontsize=12, radius=0.55)
    _dag_node_at(ax, pos_mu2, r"$\mu_2,\sigma_2^2$", italic=False,
                 fontsize=12, radius=0.55)

    # 3 explicit copies of (c_n, x_n)
    for idx, x_pos in enumerate(x_positions):
        n = idx + 1
        pos_c = (x_pos, 0.6)
        pos_x = (x_pos, -1.4)
        _dag_node_at(ax, pos_c, rf"$c_{n}$", italic=True, fontsize=15,
                     radius=0.32)
        _dag_node_at(ax, pos_x, rf"$x_{n}$", italic=True, fontsize=15,
                     observed=True, radius=0.32)
        _dag_edge(ax, pos_theta, pos_c, lw=1.5)
        _dag_edge(ax, pos_c, pos_x, lw=1.5)
        _dag_edge(ax, pos_mu1, pos_x, lw=1.2, color=DIM)
        _dag_edge(ax, pos_mu2, pos_x, lw=1.2, color=DIM)

    # Ellipsis between the 3rd copy and the Nth
    ax.text(pos_ellipsis[0], pos_ellipsis[1], "...", color=FG, fontsize=28,
            ha="center", va="center", fontweight="bold")

    # The Nth copy
    _dag_node_at(ax, pos_cN, r"$c_N$", italic=True, fontsize=15, radius=0.32)
    _dag_node_at(ax, pos_xN, r"$x_N$", italic=True, fontsize=15,
                 observed=True, radius=0.32)
    _dag_edge(ax, pos_theta, pos_cN, lw=1.5)
    _dag_edge(ax, pos_cN, pos_xN, lw=1.5)
    _dag_edge(ax, pos_mu1, pos_xN, lw=1.2, color=DIM)
    _dag_edge(ax, pos_mu2, pos_xN, lw=1.2, color=DIM)

    ax.text(0, 3.3,
            "N copies of (c_n, x_n) — θ and (μ_k, σ_k²) are shared",
            ha="center", color=YELLOW, fontsize=16, style="italic")
    set_limits(ax, [-3.8, 3.5], [-3.2, 3.7])
    save(fig, "gmm_step5_unrolled")


def fig_gmm_step6_plated():
    """Step 6: plate notation — compact form of the Step 5 unrolled graph.

    Same logical structure as Step 5, but compressed into one plate:
        θ (top-center)
        plate { c_n → x_n }    (per-datum, one copy)
        (μ_1,σ_1²)  (μ_2,σ_2²)  (shared at bottom)
    """
    fig, ax = new_fig(figsize=(9, 6.5))
    pos_theta = (0.0, 2.4)
    pos_c     = (0.0, 0.6)
    pos_x     = (0.0, -1.4)
    # Move μ-nodes wider so arrows into x_n don't crowd the plate boundary
    pos_mu1   = (-2.6, -2.6)
    pos_mu2   = ( 2.6, -2.6)

    # Plate around (c_n, x_n).  Label below the plate's bottom edge — the
    # μ_1/μ_2 → x_n arrows come in from the lower corners, leaving the area
    # directly below the plate clear for the label.
    draw_plate(ax, -0.95, -2.0, 0.95, 1.3,
               label="n = 1, ..., N", label_pos="outside_br")

    _dag_node_at(ax, pos_theta, "θ", italic=True, fontsize=24, radius=0.4)
    _dag_node_at(ax, pos_mu1, r"$\mu_1,\sigma_1^2$", italic=False,
                 fontsize=12, radius=0.55)
    _dag_node_at(ax, pos_mu2, r"$\mu_2,\sigma_2^2$", italic=False,
                 fontsize=12, radius=0.55)
    _dag_node_at(ax, pos_c, r"$c_n$", italic=True, fontsize=20)
    _dag_node_at(ax, pos_x, r"$x_n$", italic=True, fontsize=20, observed=True)

    _dag_edge(ax, pos_theta, pos_c)
    _dag_edge(ax, pos_c, pos_x)
    _dag_edge(ax, pos_mu1, pos_x)
    _dag_edge(ax, pos_mu2, pos_x)

    ax.text(0, 3.4, "Plate = 'repeat for each n'",
            ha="center", color=YELLOW, fontsize=16, style="italic")
    set_limits(ax, [-3.6, 3.6], [-3.4, 3.8])
    save(fig, "gmm_step6_plated")


def fig_gmm_step7_categorical():
    """Step 7: generalize Bernoulli/2 → Categorical/K.

    Same layout as Step 6 but with K-plate around the parameters and π/z_n
    highlighted in yellow (the renamed nodes).
    """
    fig, ax = new_fig(figsize=(9, 7.0))
    pos_pi  = (0.0, 2.6)
    pos_z   = (0.0, 0.8)
    pos_x   = (0.0, -1.2)
    pos_mu  = (0.0, -3.4)   # shared parameters now in a K-plate at bottom
    # Note: the N-plate label sits in the gap between the two plates, so the
    # K-plate is pushed further down to give vertical breathing room.

    # N-plate around (z_n, x_n).  Label to the RIGHT of the plate so the
    # central μ→x_n arrow (which exits the plate through its bottom-center)
    # doesn't slice through the label text.
    draw_plate(ax, -0.95, -1.85, 0.95, 1.5,
               label="n = 1, ..., N", label_pos="outside_right")
    # K-plate around (μ_k, σ_k²).  Same trick — label to the right.
    draw_plate(ax, -0.95, -4.0, 0.95, -2.8,
               label="k = 1, ..., K", label_pos="outside_right")

    _dag_node_at(ax, pos_pi, r"$\pi$", italic=True, fontsize=24, radius=0.4,
                 highlight=True)
    _dag_node_at(ax, pos_mu, r"$\mu_k,\sigma_k^2$", italic=False,
                 fontsize=12, radius=0.55)
    _dag_node_at(ax, pos_z, r"$z_n$", italic=True, fontsize=20,
                 highlight=True)
    _dag_node_at(ax, pos_x, r"$x_n$", italic=True, fontsize=20, observed=True)

    _dag_edge(ax, pos_pi, pos_z, color=YELLOW)
    _dag_edge(ax, pos_z, pos_x)
    _dag_edge(ax, pos_mu, pos_x)

    ax.text(0, 3.8,
            "K components:  θ → π,  c_n → z_n.   Same picture.",
            ha="center", color=YELLOW, fontsize=14, style="italic")
    set_limits(ax, [-2.5, 3.4], [-4.6, 4.4])
    save(fig, "gmm_step7_categorical")


def fig_canonical_monty_hall():
    """Classic Monty Hall: Car → HostOpens ← PlayerPicks.

    Y-limits intentionally match fig_chibany_monty_hall so the two figures
    render at the same scale when shown side-by-side on "Same network,
    different costume".
    """
    fig, ax = new_fig(figsize=(9, 5))
    pos_car = (-2.6, 1.4)
    pos_open = (0.0, -1.4)
    pos_pick = (2.6, 1.4)

    draw_node(ax, pos_car, "Car", fontsize=18, radius=0.55)
    draw_node(ax, pos_open, "Host\nOpens", fontsize=14, radius=0.65)
    draw_node(ax, pos_pick, "Player\nPicks", fontsize=13, radius=0.6)

    draw_edge(ax, pos_car, pos_open)
    draw_edge(ax, pos_pick, pos_open)

    set_limits(ax, [-3.4, 3.4], [-2.2, 2.0])
    save(fig, "canonical_monty_hall")


# ---- driver --------------------------------------------------------------


def main():
    print(f"Writing figures into {IMAGES_DIR}")
    fig_gmm_as_bn()
    fig_gmm_with_hyperprior()
    fig_chibany_bento_bn()
    fig_chibany_monty_hall()
    fig_dsep_chain()
    fig_dsep_fork()
    fig_dsep_collider()
    fig_markov_blanket()
    fig_do_setup()
    fig_do_cut()
    fig_do_compute()
    fig_do_vs_cond()
    fig_canonical_monty_hall()
    # GMM generative-process build-up (Week 5 opening — 7 slides)
    fig_gmm_step1_theta()
    fig_gmm_step2_sample_c()
    fig_gmm_step3_gaussians()
    fig_gmm_step4_sample_x()
    fig_gmm_step5_unrolled()
    fig_gmm_step6_plated()
    fig_gmm_step7_categorical()
    # SP25 figure recreations (dark-theme matplotlib versions)
    fig_bn_param_count()
    fig_bn_param_count_question()
    fig_explaining_away()
    fig_smoking_confound()
    fig_blicket_detector()
    fig_blicket_backwards_blocking()
    fig_blicket_model_human()
    fig_blicket_taught_prior()
    print("Done.")


if __name__ == "__main__":
    main()
