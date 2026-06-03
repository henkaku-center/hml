#!/usr/bin/env python3
"""Generate Week 6 (Markov Chains + Networks) figures.

All figures are rendered on a TRANSPARENT background with light strokes/text so
they sit on the dark SDS RevealJS theme (#111111). Theme colours mirror
sds-reveal/sds.scss. Run:  python3 make_figures.py
Outputs land in images/.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import networkx as nx

# ---- theme ---------------------------------------------------------------
BG       = "#111111"
WHITE    = "#FFFFFF"
DIM      = "#999999"
ACCENT   = "#64B5F6"   # blue
YELLOW   = "#FFEB3B"
RED      = "#EF5350"
GREEN    = "#66BB6A"
ORANGE   = "#FFA726"
PURPLE   = "#BA68C8"

plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor":   "none",
    "savefig.facecolor": "none",
    "text.color":       WHITE,
    "axes.edgecolor":   DIM,
    "axes.labelcolor":  WHITE,
    "xtick.color":      DIM,
    "ytick.color":      DIM,
    "font.size":        15,
    "font.family":      "DejaVu Sans",
})

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
os.makedirs(IMG, exist_ok=True)


def save(fig, name):
    p = os.path.join(IMG, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", transparent=True, pad_inches=0.15)
    plt.close(fig)
    print("wrote", os.path.relpath(p, HERE))


# ==========================================================================
# 1. Chibany bento Markov chain — 2-state {tonkatsu, hamburger}
# ==========================================================================
def fig_chibany_bento():
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    # two state circles
    cT = (2.6, 3.0); cH = (7.4, 3.0); r = 1.15
    ax.add_patch(Circle(cT, r, fc="#3a2a1a", ec=ORANGE, lw=3, zorder=2))
    ax.add_patch(Circle(cH, r, fc="#2a1a1a", ec=RED, lw=3, zorder=2))
    ax.text(*cT, "Tonkatsu\n(T)", ha="center", va="center", color=WHITE,
            fontsize=15, fontweight="bold", zorder=3)
    ax.text(*cH, "Hamburger\n(H)", ha="center", va="center", color=WHITE,
            fontsize=15, fontweight="bold", zorder=3)

    def arc(p0, p1, rad, color, label, lpos, lcol):
        a = FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                            arrowstyle="-|>", mutation_scale=22, lw=2.6,
                            color=color, zorder=1)
        ax.add_patch(a)
        ax.text(*lpos, label, ha="center", va="center", color=lcol,
                fontsize=15, fontweight="bold", zorder=4)

    # Transition probs chosen so the STATIONARY distribution is 70% T / 30% H
    # (matches Chibany's canonical "loves tonkatsu, 70/30").
    #   T->T = 0.65 (sticks with tonkatsu)   T->H = 0.35 (occasional change)
    #   H->T = 0.82 (swings back to tonkatsu) H->H = 0.18 (rarely repeats burger)
    #   pi_T = p_HT / (p_TH + p_HT) = 0.82 / (0.35 + 0.82) = 0.70
    # TWO PARALLEL LANES that never cross (gentle bow, separate top/bottom
    # bands) + explicit direction labels so the arrow directions are clear.
    # T -> H (top lane)
    arc((cT[0]+1.0, cT[1]+0.48), (cH[0]-1.0, cH[1]+0.48),  0.20, DIM,    "0.35", (5.0, 5.15), DIM)
    # H -> T (bottom lane)
    arc((cH[0]-1.0, cH[1]-0.48), (cT[0]+1.0, cT[1]-0.48),  0.20, ACCENT, "0.82", (5.0, 0.85), ACCENT)
    # self loops
    arc((cT[0]-0.6, cT[1]+0.98), (cT[0]-1.0, cT[1]-0.55), 2.6, ORANGE, "0.65", (0.4, 3.0), ORANGE)
    arc((cH[0]+1.0, cH[1]-0.55), (cH[0]+0.6, cH[1]+0.98), 2.6, DIM,    "0.18", (9.6, 3.0), DIM)
    ax.text(5.0, 4.05, "T → H", ha="center", color=DIM, fontsize=11, style="italic", zorder=4)
    ax.text(5.0, 1.95, "H → T", ha="center", color=ACCENT, fontsize=11, style="italic", zorder=4)
    save(fig, "chibany_bento_markov.png")


# ==========================================================================
# 2. Chibany T/H chain: FSA view (companion matrix shown in qmd as KaTeX).
#    Same chain as "Draw the habit": T->T .65, T->H .35, H->T .82, H->H .18.
#    Kept consistent throughout Block 2 so students track ONE chain.
# ==========================================================================
def fig_ht_fsa():
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    cT = (2.5, 3.1); cH = (7.5, 3.1); r = 1.05
    ax.add_patch(Circle(cT, r, fc="#3a2a1a", ec=ORANGE, lw=3, zorder=2))
    ax.add_patch(Circle(cH, r, fc="#2a1a1a", ec=RED, lw=3, zorder=2))
    ax.text(*cT, "T", ha="center", va="center", color=WHITE, fontsize=26, fontweight="bold", zorder=3)
    ax.text(*cH, "H", ha="center", va="center", color=WHITE, fontsize=26, fontweight="bold", zorder=3)

    def arc(p0, p1, rad, color, label, lpos):
        ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                     arrowstyle="-|>", mutation_scale=22, lw=2.8, color=color, zorder=1))
        ax.text(*lpos, label, ha="center", va="center", color=color, fontsize=16, fontweight="bold", zorder=4)
    # TWO PARALLEL LANES that never cross. T->H rides the TOP lane (both
    # endpoints high on each node); H->T rides the BOTTOM lane (both endpoints
    # low). Small upward/downward bow keeps each lane in its own band, so the
    # arrowheads are unambiguous. Labels sit on each lane near the arrow's TAIL.
    # T -> H  (top lane, bows gently up; label over T's exit)
    arc((cT[0]+0.95, cT[1]+0.50), (cH[0]-0.95, cH[1]+0.50),  0.22, DIM,    "0.35", (5.0, 5.05))
    # H -> T  (bottom lane, bows gently down; label under H's exit)
    arc((cH[0]-0.95, cH[1]-0.50), (cT[0]+0.95, cT[1]-0.50),  0.22, ACCENT, "0.82", (5.0, 1.15))
    # self-loops
    arc((cT[0]-0.5, cT[1]+0.9), (cT[0]-0.9, cT[1]-0.5), 2.6, ORANGE, "0.65", (0.45, 3.1))
    arc((cH[0]+0.9, cH[1]-0.5), (cH[0]+0.5, cH[1]+0.9), 2.6, DIM,    "0.18", (9.55, 3.1))
    # explicit direction labels so there is zero doubt which way each lane goes
    ax.text(5.0, 4.05, "T → H", ha="center", color=DIM, fontsize=11, style="italic", zorder=4)
    ax.text(5.0, 2.15, "H → T", ha="center", color=ACCENT, fontsize=11, style="italic", zorder=4)
    save(fig, "ht_fsa.png")


# 3-state SP25 quiz matrix (used for the SECOND example, fully presented).
A = np.array([[0.0, 0.1, 0.9],
              [0.5, 0.0, 0.5],
              [0.8, 0.2, 0.0]])

def _dist_after(start, k):
    v = np.zeros(3); v[start] = 1.0
    for _ in range(k):
        v = v @ A
    return v


# ==========================================================================
# 3a. Power-iteration convergence — CHIBANY 2-state chain (FIRST example).
#     P = [[.65,.35],[.82,.18]] over {T,H}; converges to pi = (0.70, 0.30).
#     Two different starts (always T / always H) -> same 70/30 distribution.
# ==========================================================================
PCH = np.array([[0.65, 0.35],   # T->T, T->H
                [0.82, 0.18]])  # H->T, H->H

def _dist_after_2(start, k):
    v = np.zeros(2); v[start] = 1.0
    for _ in range(k):
        v = v @ PCH
    return v

def fig_power_iteration():
    steps = [1, 3, 20]
    fig, axes = plt.subplots(2, 3, figsize=(10.4, 5.6), sharey=True)
    states = ["T", "H"]
    x = np.arange(2)
    colors = [ORANGE, RED]
    startnames = ["tonkatsu (T)", "hamburger (H)"]
    for row, start in enumerate([0, 1]):  # start always T / always H
        for col, k in enumerate(steps):
            ax = axes[row, col]
            d = _dist_after_2(start, k)
            ax.bar(x, d, color=colors, edgecolor=WHITE, lw=0.8, width=0.56)
            ax.set_ylim(0, 1.05)
            ax.set_xticks(x); ax.set_xticklabels(states, color=WHITE, fontsize=14)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            ax.spines["left"].set_color(DIM); ax.spines["bottom"].set_color(DIM)
            ax.tick_params(colors=DIM, labelsize=11)
            if row == 0:
                ax.set_title(f"after {k} step" + ("s" if k > 1 else ""),
                             color=YELLOW, fontsize=14, pad=8)
            for xi, di in zip(x, d):
                ax.text(xi, di + 0.03, f"{di:.2f}", ha="center", color=WHITE, fontsize=11)
        axes[row, 0].set_ylabel(f"start: {startnames[start]}", color=ACCENT,
                                fontsize=13, fontweight="bold")
    fig.text(0.5, -0.02, "By 20 steps both starts give the SAME 70/30 split — the chain forgets where it began.",
             ha="center", color=DIM, fontsize=12.5, style="italic")
    fig.tight_layout()
    save(fig, "power_iteration_convergence.png")

# Chibany stationary-distribution single-panel bar (70/30 reveal)
def fig_stationary_bar():
    pi = _dist_after_2(0, 200)
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    x = np.arange(2)
    ax.bar(x, pi, color=[ORANGE, RED], edgecolor=WHITE, lw=1, width=0.55)
    ax.set_xticks(x); ax.set_xticklabels(["Tonkatsu", "Hamburger"], color=WHITE, fontsize=14)
    ax.set_ylim(0, 0.85)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(DIM); ax.spines["bottom"].set_color(DIM)
    ax.tick_params(colors=DIM)
    for xi, di in zip(x, pi):
        ax.text(xi, di + 0.02, f"{di:.2f}", ha="center", color=YELLOW, fontsize=16, fontweight="bold")
    ax.set_title("Chibany's stationary distribution  π", color=YELLOW, fontsize=14, pad=8)
    save(fig, "stationary_bar.png")


# ==========================================================================
# 3b. Power-iteration convergence — 3-STATE quiz matrix (SECOND example).
#     A = [[0,.1,.9],[.5,0,.5],[.8,.2,0]]; pi ≈ (0.42, 0.13, 0.45).
#     Two starts (state 1 / state 2) -> same distribution by 20 steps.
# ==========================================================================
def fig_power_iteration_3state():
    steps = [1, 3, 20]
    fig, axes = plt.subplots(2, 3, figsize=(10.4, 5.6), sharey=True)
    states = ["1", "2", "3"]
    x = np.arange(3)
    colors = [ACCENT, ORANGE, GREEN]
    for row, start in enumerate([0, 1]):
        for col, k in enumerate(steps):
            ax = axes[row, col]
            d = _dist_after(start, k)
            ax.bar(x, d, color=colors, edgecolor=WHITE, lw=0.8, width=0.62)
            ax.set_ylim(0, 0.85)
            ax.set_xticks(x); ax.set_xticklabels(states, color=WHITE, fontsize=13)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            ax.spines["left"].set_color(DIM); ax.spines["bottom"].set_color(DIM)
            ax.tick_params(colors=DIM, labelsize=11)
            if row == 0:
                ax.set_title(f"after {k} step" + ("s" if k > 1 else ""),
                             color=YELLOW, fontsize=14, pad=8)
            for xi, di in zip(x, d):
                ax.text(xi, di + 0.02, f"{di:.2f}", ha="center", color=WHITE, fontsize=10)
        axes[row, 0].set_ylabel(f"start: state {start+1}", color=ACCENT,
                                fontsize=14, fontweight="bold")
    fig.text(0.5, -0.02, "Same story, bigger chain: by 20 steps both starts agree — π ≈ (0.42, 0.13, 0.45).",
             ha="center", color=DIM, fontsize=12.5, style="italic")
    fig.tight_layout()
    save(fig, "power_iteration_3state.png")

# 3-state network diagram (for the second-example setup slide)
def fig_quiz3_network():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.2, 1.35); ax.axis("off"); ax.set_aspect("equal")
    pos = {1: (0.0, 1.05), 2: (-0.95, -0.55), 3: (0.95, -0.55)}
    cols = {1: ACCENT, 2: ORANGE, 3: GREEN}
    # directed edges with probs (from the quiz matrix A, rows = from)
    edges = [(1, 2, "0.1"), (1, 3, "0.9"), (2, 1, "0.5"), (2, 3, "0.5"),
             (3, 1, "0.8"), (3, 2, "0.2")]
    for a, b, lab in edges:
        pa, pb = np.array(pos[a]), np.array(pos[b])
        d = pb - pa; d = d / np.linalg.norm(d)
        s = pa + d * 0.32; e = pb - d * 0.32
        ax.add_patch(FancyArrowPatch(s, e, connectionstyle="arc3,rad=0.16",
                     arrowstyle="-|>", mutation_scale=15, lw=1.8, color=DIM, zorder=1))
        mid = (pa + pb) / 2 + np.array([-d[1], d[0]]) * 0.17
        ax.text(*mid, lab, ha="center", va="center", color=WHITE, fontsize=11, zorder=4)
    for n, p in pos.items():
        ax.add_patch(Circle(p, 0.30, fc="#1A1A2E", ec=cols[n], lw=2.6, zorder=2))
        ax.text(*p, str(n), ha="center", va="center", color=WHITE, fontsize=16, fontweight="bold", zorder=3)
    save(fig, "quiz3_network.png")


# ==========================================================================
# 4. Animal semantic network (Meow/Lion/Cat/Dog + a couple more) — base graph
#    Reused for the random-walk trace (highlighted nodes) and the degree poll.
# ==========================================================================
# Clean two-cluster layout with NO overlapping edges: pets triangle
# (Dog-Wolf-Cat) on the left, big-animals triangle (Lion-Tiger-Zebra) on the
# right, joined by Cat. Cat is the bridge → the unique degree-4 hub (the degree
# poll answer). Every edge is a distinct straight line.
ANIMAL_EDGES = [
    ("Dog", "Cat"), ("Wolf", "Cat"), ("Dog", "Wolf"),     # pets cluster
    ("Cat", "Lion"), ("Cat", "Tiger"),                    # bridge
    ("Lion", "Tiger"), ("Lion", "Zebra"), ("Tiger", "Zebra"),  # big-animals cluster
]
ANIMAL_POS = {
    "Dog":   (-2.6,  0.9),
    "Wolf":  (-2.6, -0.9),
    "Cat":   (-1.0,  0.0),
    "Lion":  ( 0.9,  0.8),
    "Tiger": ( 0.9, -0.8),
    "Zebra": ( 2.6,  0.0),
}

def _draw_animal_net(ax, highlight=None, visited_path=None, title=None,
                     show_degree=False):
    G = nx.Graph(); G.add_edges_from(ANIMAL_EDGES)
    highlight = highlight or []
    nx.draw_networkx_edges(G, ANIMAL_POS, ax=ax, edge_color=DIM, width=1.8, alpha=0.7)
    # current-walk path edges in accent
    if visited_path and len(visited_path) > 1:
        pe = list(zip(visited_path[:-1], visited_path[1:]))
        nx.draw_networkx_edges(G, ANIMAL_POS, edgelist=pe, ax=ax,
                               edge_color=ACCENT, width=3.4, alpha=0.95)
    deg = dict(G.degree())
    for n, (xx, yy) in ANIMAL_POS.items():
        is_hi = n in highlight
        rad = 0.46 + (0.05 * deg[n] if show_degree else 0)
        ax.add_patch(Circle((xx, yy), rad, zorder=3,
                            fc=(YELLOW if is_hi else "#1A1A2E"),
                            ec=(YELLOW if is_hi else ACCENT), lw=2.6))
        lbl = f"{n}\n(deg {deg[n]})" if show_degree else n
        ax.text(xx, yy, lbl, ha="center", va="center", zorder=4,
                color=("#111111" if is_hi else WHITE),
                fontsize=11.5, fontweight="bold")
    ax.set_xlim(-3.2, 3.7); ax.set_ylim(-2.0, 2.0); ax.axis("off")
    ax.set_aspect("equal")
    if title:
        ax.set_title(title, color=YELLOW, fontsize=15, pad=4)

def fig_animal_net_base():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    _draw_animal_net(ax)
    save(fig, "animal_net_base.png")

def _hub():
    G = nx.Graph(); G.add_edges_from(ANIMAL_EDGES)
    return max(G.degree(), key=lambda kv: kv[1])[0]

def fig_animal_net_degree():
    # HIGHLIGHTED hub version — for the poll ANSWER slide (degrees shown + hub lit).
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    _draw_animal_net(ax, highlight=[_hub()], show_degree=True)
    save(fig, "animal_net_degree.png")

def fig_animal_net_degree_nohi():
    # NO-HIGHLIGHT version — for the poll PROMPT slide. Shows each node's degree
    # so students can reason, but does NOT light up the answer (no spoiler).
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    _draw_animal_net(ax, highlight=[], show_degree=True)
    save(fig, "animal_net_degree_nohi.png")

# random-walk trace: a sequence of slides (build-up "animation")
WALK = ["Wolf", "Dog", "Cat", "Lion", "Tiger", "Zebra"]  # all valid edges; crosses the bridge at Cat
def fig_walk_steps():
    for i in range(2, len(WALK) + 1):
        path = WALK[:i]
        fig, ax = plt.subplots(figsize=(6.6, 4.3))
        _draw_animal_net(ax, highlight=[path[-1]], visited_path=path)
        ax.text(0.0, -1.85, "visited:  " + " → ".join(path),
                ha="center", color=ACCENT, fontsize=13, fontweight="bold")
        save(fig, f"walk_step{i}.png")


# ==========================================================================
# 5. Fluency / categories-burst illustration (Abbott payoff): a path that
#    clusters within communities (pets) then switches (africa).
# ==========================================================================
def fig_fluency_communities():
    # two communities
    edges = [("dog","cat"),("cat","hamster"),("dog","hamster"),  # pets
             ("lion","zebra"),("zebra","giraffe"),("lion","giraffe"),("giraffe","elephant"),("lion","elephant"),
             ("hamster","lion")]  # bridge
    pos = {"dog":(-2.6,1.0),"cat":(-3.0,-0.4),"hamster":(-1.7,0.1),
           "lion":(0.6,0.9),"zebra":(2.4,0.7),"giraffe":(2.7,-0.7),"elephant":(1.0,-1.0)}
    G = nx.Graph(); G.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(8.0, 4.2))
    # community hulls (soft)
    ax.add_patch(plt.matplotlib.patches.Ellipse((-2.4,0.2),2.6,2.2,fc=GREEN,ec="none",alpha=0.12,zorder=0))
    ax.add_patch(plt.matplotlib.patches.Ellipse((1.7,0.0),3.4,2.6,fc=ORANGE,ec="none",alpha=0.12,zorder=0))
    nx.draw_networkx_edges(G,pos,ax=ax,edge_color=DIM,width=1.6,alpha=0.7)
    walk = ["cat","dog","hamster","lion","zebra","giraffe"]
    pe=list(zip(walk[:-1],walk[1:]))
    nx.draw_networkx_edges(G,pos,edgelist=pe,ax=ax,edge_color=ACCENT,width=3.2,alpha=0.95)
    for n,(xx,yy) in pos.items():
        ax.add_patch(Circle((xx,yy),0.44,fc="#1A1A2E",ec=ACCENT,lw=2.4,zorder=3))
        ax.text(xx,yy,n,ha="center",va="center",color=WHITE,fontsize=10.5,fontweight="bold",zorder=4)
    ax.text(-2.4,1.75,"pets",color=GREEN,fontsize=14,fontweight="bold",ha="center")
    ax.text(1.7,1.6,"African animals",color=ORANGE,fontsize=14,fontweight="bold",ha="center")
    ax.text(0.0,-1.95,'recall:  "cat, dog, hamster, lion, zebra, giraffe …"',
            ha="center",color=ACCENT,fontsize=13,fontweight="bold")
    ax.set_xlim(-4.0,4.2); ax.set_ylim(-2.2,2.1); ax.axis("off"); ax.set_aspect("equal")
    save(fig,"fluency_communities.png")


# ==========================================================================
# 6. Erdos-Renyi vs scale-free: degree distributions + the networks.
# ==========================================================================
def fig_er_vs_scalefree():
    rng = np.random.default_rng(7)
    n = 240
    G_er = nx.gnp_random_graph(n, 0.03, seed=7)
    G_ba = nx.barabasi_albert_graph(n, 2, seed=7)
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    for ax, G, title, col in [(axes[0], G_er, "Erdős–Rényi (random)", ACCENT),
                               (axes[1], G_ba, "Scale-free (power-law)", ORANGE)]:
        degs = [d for _, d in G.degree()]
        bins = np.arange(0, max(degs) + 2) - 0.5
        ax.hist(degs, bins=bins, color=col, edgecolor=WHITE, lw=0.5)
        ax.set_title(title, color=YELLOW, fontsize=14, pad=8)
        ax.set_xlabel("degree (# edges)", color=WHITE, fontsize=12)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(DIM); ax.spines["bottom"].set_color(DIM)
        ax.tick_params(colors=DIM, labelsize=10)
    axes[0].set_ylabel("# of nodes", color=WHITE, fontsize=12)
    axes[1].annotate("a few hubs\nwith many edges", xy=(0.78, 0.55),
                     xycoords="axes fraction", color=ORANGE, fontsize=11.5,
                     ha="center", fontweight="bold")
    fig.tight_layout()
    save(fig, "er_vs_scalefree.png")


# ==========================================================================
# 7. PageRank illustration: random surfer on a small web graph, node size ~ PR
# ==========================================================================
def fig_pagerank():
    edges = [("A","B"),("A","C"),("B","C"),("C","A"),("D","C"),("E","C"),
             ("B","D"),("F","C"),("C","G"),("G","C")]
    G = nx.DiGraph(); G.add_edges_from(edges)
    pr = nx.pagerank(G)
    pos = nx.circular_layout(G)  # predictable, evenly-spaced — no node overlaps
    prmax = max(pr.values())
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    # draw edges to node EDGES (clip to each node's radius) so arrows don't hide
    rad = {n: 0.085 + 0.16 * (pr[n] / prmax) for n in G}  # radii in [0.085, 0.245]
    for u, v in G.edges():
        pu, pv = np.array(pos[u]), np.array(pos[v])
        d = pv - pu; d = d / np.linalg.norm(d)
        s = pu + d * rad[u]; e = pv - d * rad[v]
        ax.add_patch(FancyArrowPatch(s, e, connectionstyle="arc3,rad=0.10",
                     arrowstyle="-|>", mutation_scale=12, lw=1.4, color=DIM,
                     alpha=0.7, zorder=1))
    for n, (xx, yy) in pos.items():
        hub = pr[n] == prmax
        ax.add_patch(Circle((xx, yy), rad[n], fc=(YELLOW if hub else "#1A1A2E"),
                            ec=(YELLOW if hub else ACCENT), lw=2.2, zorder=3))
        ax.text(xx, yy, n, ha="center", va="center", zorder=4,
                color=("#111111" if hub else WHITE),
                fontsize=12 if hub else 10.5, fontweight="bold")
    ax.text(0.5, -0.06, "node size ∝ PageRank = long-run visit frequency of a random surfer",
            transform=ax.transAxes, ha="center", color=DIM, fontsize=11.5, style="italic")
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.45, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "pagerank.png")


# ==========================================================================
# 8. Card shuffle as a Markov chain (themed) — "move random card to top"
#    Three deck states, an arrow, converging to "uniform over orderings".
# ==========================================================================
def fig_card_shuffle():
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")

    def draw_deck(x0, order, label, lcol):
        for i, c in enumerate(order):
            y = 3.6 - i * 0.62
            ax.add_patch(plt.matplotlib.patches.FancyBboxPatch(
                (x0, y), 1.5, 0.52, boxstyle="round,pad=0.02,rounding_size=0.08",
                fc="#1A1A2E", ec=ACCENT, lw=1.6, zorder=2))
            ax.text(x0 + 0.75, y + 0.26, c, ha="center", va="center",
                    color=WHITE, fontsize=13, fontweight="bold", zorder=3)
        ax.text(x0 + 0.75, 4.35, label, ha="center", color=lcol,
                fontsize=12.5, fontweight="bold")

    draw_deck(0.6, ["A♠", "K♥", "7♦", "3♣"], "state t", DIM)
    draw_deck(5.4, ["7♦", "A♠", "K♥", "3♣"], "state t+1", YELLOW)
    draw_deck(10.3, ["3♣", "7♦", "A♠", "K♥"], "…", DIM)

    for x in (3.2, 8.1):
        ax.add_patch(FancyArrowPatch((x, 2.4), (x + 1.6, 2.4),
                     arrowstyle="-|>", mutation_scale=22, lw=2.4, color=ACCENT))
    ax.text(4.0, 2.85, "move a random\ncard to top", ha="center", color=ACCENT, fontsize=11)
    ax.text(8.9, 2.85, "again…", ha="center", color=ACCENT, fontsize=11)
    # No stationary-distribution caption here on purpose: the first card-shuffle
    # slide shows PROCESS ONLY (asks students the goal); the "goal = uniform"
    # reveal is on the following slide's text, not baked into the figure.
    save(fig, "card_shuffle.png")


# ==========================================================================
# 9. Markov "Really past / Past / Less past" — three portraits in ONE panel
#    with centred captions directly under each, and arrows between them.
#    Composing this as a single figure guarantees caption alignment (vs. three
#    Quarto columns with bottom-anchored captions on mismatched image heights).
# ==========================================================================
def fig_markov_timeline():
    from PIL import Image
    from matplotlib.patches import FancyBboxPatch
    portraits = ["markov_young.jpg", "markov_mid.png", "markov_old.jpg"]
    captions = ["Really past", "Past", "Less past"]

    def to_square(p, side=460):
        # crop each portrait to a common SQUARE around its centre, so all three
        # render at identical size (kills the white-border / mismatched-height
        # problem) and the captions share a baseline by construction.
        im = Image.open(os.path.join(IMG, p)).convert("RGB")
        w, h = im.size
        s = min(w, h)
        im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
        return np.asarray(im.resize((side, side)))

    imgs = [to_square(p) for p in portraits]

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.6))
    for ax, im, cap in zip(axes, imgs, captions):
        # dark rounded frame behind each portrait so the varying photo
        # backgrounds read as intentional framed photos on the dark slide.
        ax.add_patch(FancyBboxPatch((0.10, 0.20), 0.80, 0.72,
                     boxstyle="round,pad=0.012,rounding_size=0.04",
                     fc="#1A1A2E", ec=DIM, lw=1.6, zorder=1,
                     transform=ax.transAxes))
        ax.imshow(im, extent=[0.13, 0.87, 0.23, 0.89], aspect="auto", zorder=2)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        # caption: centred under the panel, SAME y for all three (baseline aligned)
        ax.text(0.5, 0.10, cap, ha="center", va="top", color=DIM,
                fontsize=17, fontweight="bold", transform=ax.transAxes)

    # arrows between panels, in figure coordinates, at portrait mid-height.
    # Portrait spans axes-y 0.23..0.89 → mid ≈ 0.56 of each axes box.
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.04, wspace=0.10)
    for ax_a, ax_b in [(axes[0], axes[1]), (axes[1], axes[2])]:
        pa, pb = ax_a.get_position(), ax_b.get_position()
        x0 = pa.x0 + 0.87 * pa.width      # right edge of portrait in panel A
        x1 = pb.x0 + 0.13 * pb.width      # left edge of portrait in panel B
        ymid = pa.y0 + 0.56 * pa.height
        arr = FancyArrowPatch((x0, ymid), (x1, ymid),
                              transform=fig.transFigure, arrowstyle="-|>",
                              mutation_scale=26, lw=3, color=ACCENT, zorder=5)
        fig.patches.append(arr)
    save(fig, "markov_timeline.png")


# ==========================================================================
# 10. IRT relative to patch switch (Abbott et al. 2012, Fig 1a / Fig 3).
#     The signature optimal-foraging result: the FIRST word in a new patch
#     (position 1) takes longest (above the long-run average), then word 2 is
#     fast; within a patch IRTs rise back toward average before the next switch.
#     Two panels — HUMAN vs the RANDOM-WALK MODEL — showing they match.
#     (Values are representative of the published figure's qualitative shape.)
# ==========================================================================
def fig_irt_patch_switch():
    # x positions: ...,-2,-1, | switch | ,1,2,3,4  (1 = first word of new patch)
    xlab = ["-2", "-1", "1", "2", "3", "4"]
    x = np.arange(len(xlab))
    human = [0.78, 0.92, 1.34, 0.55, 0.70, 0.83]
    model = [0.80, 0.95, 1.28, 0.58, 0.72, 0.85]
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.4), sharey=True)
    for ax, vals, title, col in [(axes[0], human, "Humans (Hills et al.)", ACCENT),
                                  (axes[1], model, "Random-walk model", ORANGE)]:
        bars = ax.bar(x, vals, color=col, edgecolor=WHITE, lw=0.8, width=0.66)
        # the first-in-patch bar (position "1", index 2) is the headline → emphasise
        bars[2].set_color(YELLOW)
        ax.axhline(1.0, ls="--", lw=1.6, color=DIM)
        ax.text(len(xlab) - 0.5, 1.03, "long-run average", ha="right", va="bottom",
                color=DIM, fontsize=10, style="italic")
        ax.set_xticks(x); ax.set_xticklabels(xlab, color=WHITE, fontsize=12)
        ax.set_ylim(0, 1.55)
        ax.set_title(title, color=YELLOW, fontsize=14, pad=8)
        ax.set_xlabel("order of entry relative to patch switch", color=WHITE, fontsize=11)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(DIM); ax.spines["bottom"].set_color(DIM)
        ax.tick_params(colors=DIM, labelsize=10)
    axes[0].set_ylabel("item IRT / average IRT", color=WHITE, fontsize=12)
    fig.text(0.5, -0.02, "Position 1 (first word of a new patch) is SLOWEST — the switch cost. "
             "The walk reproduces it with no explicit switch rule.",
             ha="center", color=DIM, fontsize=11.5, style="italic")
    fig.tight_layout()
    save(fig, "irt_patch_switch.png")


# ==========================================================================
# 11. Censoring worked example (Abbott et al. 2012, §4.2).
#     The latent walk visits many nodes (repeats + non-animals); the reported
#     fluency list = the FIRST time each unique ANIMAL is hit. Everything else
#     is CENSORED. IRT(k) = tau(k) - tau(k-1) + len(word).
# ==========================================================================
def fig_censoring():
    fig, ax = plt.subplots(figsize=(10.6, 3.8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
    seq = ["animal", "dog", "house", "dog", "cat"]
    # which are reported (first-time animal) vs censored
    reported = {1: True, 2: False, 3: False, 4: True}   # index into seq (dog,house,dog,cat)
    xs = np.linspace(1.0, 11.0, len(seq))
    ax.text(6.0, 4.6, "The latent walk (one step per node):", ha="center",
            color=WHITE, fontsize=14, fontweight="bold")
    for i, (w, xx) in enumerate(zip(seq, xs)):
        is_animal_first = reported.get(i, None)
        if i == 0:
            fc, ec, tc = "#1A1A2E", DIM, DIM        # start cue
        elif is_animal_first:
            fc, ec, tc = "#2a2a10", YELLOW, WHITE    # reported (kept)
        else:
            fc, ec, tc = "#1A1A2E", RED, DIM         # censored
        ax.add_patch(plt.matplotlib.patches.FancyBboxPatch(
            (xx - 0.62, 2.7), 1.24, 0.85, boxstyle="round,pad=0.02,rounding_size=0.08",
            fc=fc, ec=ec, lw=2.4, zorder=2))
        ax.text(xx, 3.12, w, ha="center", va="center", color=tc, fontsize=12,
                fontweight="bold", zorder=3)
        ax.text(xx, 2.45, f"n={i+1}", ha="center", va="center", color=DIM, fontsize=9)
        if i < len(seq) - 1:
            ax.add_patch(FancyArrowPatch((xx + 0.64, 3.12), (xs[i+1] - 0.64, 3.12),
                         arrowstyle="-|>", mutation_scale=16, lw=1.8, color=DIM, zorder=1))
        # mark censored
        if is_animal_first is False:
            ax.text(xx, 1.95, "✗ censored", ha="center", color=RED, fontsize=9.5, style="italic")
        elif is_animal_first:
            ax.text(xx, 1.95, "✓ reported", ha="center", color=YELLOW, fontsize=9.5, fontweight="bold")
    # reported list + IRT
    ax.text(6.0, 1.15, "Reported fluency list:  dog, cat", ha="center",
            color=YELLOW, fontsize=13, fontweight="bold")
    ax.text(6.0, 0.45,
            "IRT(cat) = τ(cat) − τ(dog) + len(cat) = 5 − 2 + 3 = 6",
            ha="center", color=ACCENT, fontsize=12.5)
    save(fig, "censoring.png")


# ==========================================================================
# 12. AD vs healthy semantic-network statistics (Zemla & Austerweil 2019).
#     Three structural differences (the "impaired representation" story):
#       - smaller MEAN DEGREE (fewer associates per concept)
#       - higher EDGE DENSITY (more spurious associations)
#       - less SMALL-WORLD-like (less organized / efficient)
#     Values are schematic (the paper reports group differences, not single
#     numbers); bars show direction + relative magnitude only.
# ==========================================================================
def fig_ad_network_stats():
    panels = [
        ("Mean degree", [1.00, 0.72], "AD: fewer associates\nper concept"),
        ("Edge density", [1.00, 1.34], "AD: more spurious\nassociations"),
        ("Small-world stat", [1.00, 0.66], "AD: less organized /\nefficient"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 4.2))
    for ax, (title, vals, note) in zip(axes, panels):
        x = np.arange(2)
        ax.bar(x, vals, color=[GREEN, RED], edgecolor=WHITE, lw=0.8, width=0.62)
        ax.set_xticks(x); ax.set_xticklabels(["Healthy", "AD"], color=WHITE, fontsize=12)
        ax.set_ylim(0, 1.55)
        ax.set_title(title, color=YELLOW, fontsize=14, pad=8)
        ax.set_yticks([])
        for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(DIM)
        ax.tick_params(colors=DIM, labelsize=11)
        # arrow annotation showing direction
        up = vals[1] > vals[0]
        ax.annotate("", xy=(1, vals[1]), xytext=(1, vals[0]),
                    arrowprops=dict(arrowstyle="-|>", color=YELLOW, lw=2.2))
        ax.text(0.5, -0.20, note, ha="center", va="top", transform=ax.transAxes,
                color=DIM, fontsize=10.5, style="italic")
    fig.text(0.5, -0.04, "Zemla & Austerweil (2019): AD changes the STRUCTURE of the estimated network — "
             "a representation deficit, measurable from fluency lists.",
             ha="center", color=DIM, fontsize=11.5, style="italic")
    fig.tight_layout()
    save(fig, "ad_network_stats.png")


if __name__ == "__main__":
    fig_irt_patch_switch()
    fig_censoring()
    fig_ad_network_stats()
    fig_markov_timeline()
    fig_card_shuffle()
    fig_chibany_bento()
    fig_ht_fsa()
    fig_power_iteration()
    fig_stationary_bar()
    fig_power_iteration_3state()
    fig_quiz3_network()
    fig_animal_net_base()
    fig_animal_net_degree()
    fig_animal_net_degree_nohi()
    fig_walk_steps()
    fig_fluency_communities()
    fig_er_vs_scalefree()
    fig_pagerank()
    print("done.")
