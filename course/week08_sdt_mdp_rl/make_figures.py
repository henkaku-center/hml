#!/usr/bin/env python3
"""Generate Week 8 (Decision theory / MDP / RL) figures.

All figures render on a TRANSPARENT background with light strokes/text so they
sit on the dark SDS RevealJS theme (#111111). Theme colours mirror
sds-reveal/sds.scss. Run:  python3 make_figures.py
Outputs land in images/.

The Chibany MDP and the GardenPath feedback tables are the SAME ones verified
in the planning step (see week8-shared-outline.md "two worked examples").

Figures:
  dt-risk-curve.png            Bayes (avg) vs minimax (worst-case) on a risk curve
  dt-loss-estimators.png       0-1/squared/absolute loss -> MAP/mean/median
  chibany-mdp-diagram.png      3-state Chibany wellbeing MDP (the intro MDP)
  chibany-transition-matrices.png  Indulge | Invest matrices ("action = pick the matrix")
  chibany-chain-to-mdp.png     Markov chain -> +reward -> +action build
  value-iteration-converge.png V(s) per sweep converging; optimal policy
  gamma-sweep-policy.png       Junk-state action flips Indulge->Invest at gamma~0.64
  qlearning-update-anatomy.png the TD update, colour-coded (target/error/rate)
  gardenpath-grid.png          dark-theme GardenPath domain
  feedback-rm-vs-af.png        rm learns the path | af loops forever (positive cycle)
  potential-shaping.png        potential field + recovered path (the fix)
  simulation-based-rl.png      Dyna loop: learn model -> simulate -> plan
  rl-timeline.png              tabular -> DQN -> AlphaGo -> MuZero -> Dreamer
  dopamine-td.png              TD error = dopamine prediction-error signal
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch, Rectangle
import matplotlib.patheffects as pe

# ---- theme (mirror sds-reveal/sds.scss) ----------------------------------
BG     = "#111111"
WHITE  = "#FFFFFF"
DIM    = "#999999"
ACCENT = "#64B5F6"   # blue
YELLOW = "#FFEB3B"
RED    = "#EF5350"
GREEN  = "#66BB6A"
ORANGE = "#FFA726"
PURPLE = "#BA68C8"
TEAL   = "#4DD0E1"

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
# VERIFIED CORES (mirror /tmp/wk8_verify.py)
# ==========================================================================
# Chibany wellbeing MDP: states 0=Junk, 1=Trying, 2=Healthy; actions 0=Indulge,1=Invest
CHI_S = ["Junk\nrut", "Trying", "Healthy\n& happy"]
CHI_R = np.array([1.0, -2.0, 5.0])
CHI_T = {
    0: np.array([[.9, .1, 0], [.7, .3, 0], [.2, .5, .3]]),   # Indulge
    1: np.array([[.4, .6, 0], [.1, .4, .5], [0, .1, .9]]),   # Invest
}

def chi_value_iteration(gamma, n_iter=400, tol=1e-12, record=False):
    V = np.zeros(3); hist = [V.copy()]
    for _ in range(n_iter):
        Q = np.stack([CHI_R + gamma * (CHI_T[a] @ V) for a in (0, 1)], axis=1)
        Vn = Q.max(axis=1)
        hist.append(Vn.copy())
        if np.max(np.abs(Vn - V)) < tol:
            V = Vn; break
        V = Vn
    pol = Q.argmax(axis=1)
    return (V, pol, np.array(hist)) if record else (V, pol)

# GardenPath: s=(row,col), row1 bottom, col1 left; start (1,1), goal (3,3) terminal
GOAL = (3, 3)
GARDEN = {(1, 2), (1, 3), (2, 2), (2, 3)}
UP, DOWN, LEFT, RIGHT = 'U', 'D', 'L', 'R'
POS, NEG, NO, GFB, WEAK = 10, -10, 0, 20, 4     # WEAK = faint praise for staying on the path
RM = {(1,1):{UP:NO,RIGHT:NEG},(2,1):{UP:NO,RIGHT:NEG,DOWN:NO},(3,1):{RIGHT:NO,DOWN:NO},
      (1,2):{RIGHT:NEG,UP:NEG,LEFT:NO},(2,2):{RIGHT:NEG,UP:NO,LEFT:NO,DOWN:NEG},
      (3,2):{RIGHT:GFB,LEFT:NO,DOWN:NEG},(1,3):{UP:NEG,LEFT:NEG},(2,3):{UP:GFB,DOWN:NEG,LEFT:NEG}}
# action-feedback ("how people teach"): +POS forward on the path, but only +WEAK (faint
# praise, NOT punishment) for BACKTRACKING along it — a human positive-feedback bias. The
# path becomes a farmable +reward cycle (the cat paces it, never finishing). Backtrack
# entries (2,1)DOWN, (3,1)DOWN, (3,2)LEFT were NEG → now WEAK. MUST match the widget's AF.
AF = {(1,1):{UP:POS,RIGHT:NEG},(2,1):{UP:POS,RIGHT:NEG,DOWN:WEAK},(3,1):{RIGHT:POS,DOWN:WEAK},
      (1,2):{RIGHT:NEG,UP:NEG,LEFT:POS},(2,2):{RIGHT:NEG,UP:POS,LEFT:NEG,DOWN:NEG},
      (3,2):{RIGHT:GFB,LEFT:WEAK,DOWN:NEG},(1,3):{UP:POS,LEFT:NEG},(2,3):{UP:POS,DOWN:NEG,LEFT:NEG}}
DELTA = {UP:(1,0), DOWN:(-1,0), LEFT:(0,-1), RIGHT:(0,1)}

def gp_step(s, a):
    dr, dc = DELTA[a]; return (s[0]+dr, s[1]+dc)
def gp_poss(s):
    r, c = s; A = []
    if r > 1: A.append(DOWN)
    if r < 3: A.append(UP)
    if c > 1: A.append(LEFT)
    if c < 3: A.append(RIGHT)
    return A
def gp_mdist(s): return abs(GOAL[0]-s[0]) + abs(GOAL[1]-s[1])

def gp_vi(reward_fn, gamma=0.95, n_iter=4000, tol=1e-9):
    states = [(r, c) for r in range(1, 4) for c in range(1, 4)]
    nz = [s for s in states if s != GOAL]
    V = {s: 0.0 for s in states}
    for _ in range(n_iter):
        d = 0
        for s in nz:
            best = max(reward_fn(s, a) + gamma*(0.0 if gp_step(s, a) == GOAL else V[gp_step(s, a)])
                       for a in gp_poss(s))
            d = max(d, abs(best - V[s])); V[s] = best
        if d < tol: break
    pol = {}
    for s in nz:
        qa = {a: reward_fn(s, a) + gamma*(0.0 if gp_step(s, a) == GOAL else V[gp_step(s, a)])
              for a in gp_poss(s)}
        pol[s] = max(qa, key=qa.get)
    return V, pol

def gp_rollout(pol, start=(1, 1), maxn=24):
    s = start; path = [s]
    for _ in range(maxn):
        if s == GOAL: break
        s = gp_step(s, pol[s]); path.append(s)
    return path, (s == GOAL)


# ==========================================================================
# 1. Decision theory: Bayes (average) vs minimax (worst-case) risk
# ==========================================================================
def fig_dt_risk_curve():
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    th = np.linspace(-3, 3, 400)
    risk = 0.45 + 0.13 * th**2                   # Bayes rule: risk varies with theta (a U)
    mmx = 1.46                                    # minimax rule: flat risk, pushed UP near the Bayes peak
    ax.fill_between(th, 0, risk, color=ACCENT, alpha=0.10, zorder=0)
    ax.plot(th, risk, color=ACCENT, lw=3, zorder=3, label="Bayes rule")
    ax.axhline(mmx, color=RED, lw=2.6, ls="--", zorder=2, label="minimax rule")
    # highlight the tiny sliver where Bayes exceeds minimax — all minimax buys you
    ax.fill_between(th, mmx, risk, where=(risk > mmx), color=RED, alpha=0.30, zorder=1)
    cross = th[np.where(np.diff(np.sign(risk - mmx)))[0]]
    for x in cross:
        ax.plot([x], [mmx], "o", mfc=BG, mec=RED, mew=2, ms=8, zorder=5)
    ax.text(0, 0.30, "Bayes: low where θ\nusually is (the prior's mass)", color=ACCENT,
            ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.text(-2.92, mmx + 0.05, "minimax: this high — everywhere", color=RED, ha="left", va="bottom",
            fontsize=11, fontweight="bold")
    ax.annotate("…to dodge only\nthis rare sliver", xy=(2.9, (mmx + 0.45 + 0.13*2.9**2)/2),
                xytext=(1.2, 1.66), color=RED, fontsize=10.5, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.legend(loc="upper center", frameon=False, labelcolor="linecolor", fontsize=12.5,
              ncol=2, bbox_to_anchor=(0.5, 1.13))
    ax.set_xlabel("state of the world  $\\theta$")
    ax.set_ylabel("expected loss  $E^x[L]$")
    ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(0, 1.85); ax.set_xlim(-3, 3)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    save(fig, "dt-risk-curve.png")


# ==========================================================================
# 2. Loss -> estimator: 0-1/squared/absolute  ->  MAP/mean/median
# ==========================================================================
def fig_dt_loss_estimators():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.4, 4.0))
    # left: the three loss shapes
    e = np.linspace(-2.4, 2.4, 400)
    axL.plot(e, (np.abs(e) > 0.18).astype(float), color=ORANGE, lw=3, label="0–1  → MAP (mode)")
    axL.plot(e, 0.42*e**2, color=ACCENT, lw=3, label="squared $L^2$ → mean")
    axL.plot(e, 0.62*np.abs(e), color=GREEN, lw=3, label="absolute $L^1$ → median")
    axL.set_title("loss  $L(\\theta, a)$", color=WHITE, fontsize=15)
    axL.set_xlabel("error  $\\theta - d(x)$"); axL.set_yticks([]); axL.set_xticks([0])
    axL.set_ylim(-0.1, 1.5); axL.legend(fontsize=11, frameon=False, labelcolor=WHITE, loc="upper center")
    for sp in ("top", "right"): axL.spines[sp].set_visible(False)
    # right: a skewed posterior with the three estimates marked
    x = np.linspace(0, 10, 600)
    post = (x**2.3) * np.exp(-x/1.15); post /= np.trapz(post, x)
    mode = x[post.argmax()]
    mean = np.trapz(x*post, x)
    cdf = np.cumsum(post); cdf /= cdf[-1]; med = x[np.searchsorted(cdf, 0.5)]
    axR.fill_between(x, 0, post, color=PURPLE, alpha=0.18)
    axR.plot(x, post, color=PURPLE, lw=2.6)
    for val, col, lab in [(mode, ORANGE, "MAP"), (med, GREEN, "median"), (mean, ACCENT, "mean")]:
        axR.axvline(val, color=col, lw=2.6, ls="--")
        axR.text(val, post.max()*1.02, lab, color=col, ha="center", va="bottom",
                 fontsize=12, fontweight="bold")
    axR.set_title("posterior over $\\theta$", color=WHITE, fontsize=15)
    axR.set_yticks([]); axR.set_xticks([]); axR.set_ylim(0, post.max()*1.18)
    for sp in ("top", "right", "left"): axR.spines[sp].set_visible(False)
    fig.tight_layout()
    save(fig, "dt-loss-estimators.png")


# ==========================================================================
# 3. Chibany MDP diagram (the intro MDP) — Trying is a literal trough
# ==========================================================================
def _arrow(ax, p0, p1, rad, color, lw=2.6, z=1):
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>", mutation_scale=20, lw=lw, color=color, zorder=z))

def _wt(p):
    """Probability -> (line width, arrow alpha, arrowhead scale, label size, label alpha).
    Main transitions render thick & bright; rare ones thin & faint, so the dominant
    flow reads at a glance while the small probabilities stay present for completeness."""
    lw = 0.7 + 3.6 * p          # 0.1 -> 1.06   0.5 -> 2.5    0.9 -> 3.94
    alpha = min(1.0, 0.28 + 0.80 * p)   # 0.1 -> 0.36   0.9 -> 1.0
    head = 8 + 7 * p            # 0.1 -> 8.7    0.9 -> 14.3
    fs = 8.5 + 4.5 * p          # 0.1 -> 8.95   0.9 -> 12.6
    return lw, alpha, head, fs, max(0.7, alpha)


def _loop(ax, center, color, p, ang_deg, r_node, rad=2.3, spread=22, lab_gap=0.86):
    """A self-loop on a node rim, pointing outward at ang_deg; weight ~ probability."""
    lw, al, head, fs, lal = _wt(p)
    a = np.deg2rad(ang_deg); d = np.deg2rad(spread)
    p0 = (center[0] + r_node*np.cos(a - d), center[1] + r_node*np.sin(a - d))
    p1 = (center[0] + r_node*np.cos(a + d), center[1] + r_node*np.sin(a + d))
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>", mutation_scale=head, lw=lw, color=color, alpha=al, zorder=3))
    lab = (center[0] + (r_node + lab_gap)*np.cos(a), center[1] + (r_node + lab_gap)*np.sin(a))
    t = ax.text(lab[0], lab[1], f"{p:.1f}", color=color, fontsize=fs, fontweight="bold",
                ha="center", va="center", zorder=6, alpha=lal)
    t.set_path_effects([pe.withStroke(linewidth=2.8, foreground=BG)])


def _dir_edge(ax, c0, c1, rad, color, p, r_node):
    """Curved directed edge between node centres, trimmed to the rims; weight ~ probability.
    Parallel same-direction edges fan apart via different |rad|; opposite directions
    bow to opposite sides automatically (arc3 bends left of travel for +rad)."""
    lw, al, head, fs, lal = _wt(p)
    p0 = np.array(c0, float); p1 = np.array(c1, float)
    u = p1 - p0; L = float(np.hypot(*u)); u = u / L
    a = p0 + u*r_node; b = p1 - u*r_node
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>", mutation_scale=head, lw=lw, color=color, alpha=al, zorder=3))
    n = np.array([-u[1], u[0]])                   # left normal; arc3 +rad bows toward it
    apex = (a + b) / 2 + n * (rad * L * 0.55)
    t = ax.text(apex[0], apex[1], f"{p:.1f}", color=color, fontsize=fs, fontweight="bold",
                ha="center", va="center", zorder=6, alpha=lal)
    t.set_path_effects([pe.withStroke(linewidth=2.8, foreground=BG)])


def fig_chibany_mdp_diagram():
    INV, IND = ACCENT, PURPLE                     # ACTION colors — distinct from STATE colors
    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    ax.set_xlim(0, 11); ax.set_ylim(0, 8.2); ax.axis("off")
    P = {0: (2.3, 5.4), 1: (5.5, 2.1), 2: (8.7, 5.4)}     # Junk, Trying (trough), Healthy
    scol = {0: ORANGE, 1: RED, 2: GREEN}
    name = {0: "Junk", 1: "Trying", 2: "Healthy"}
    rn = 1.0
    MAG = {0: 0.15, 1: 0.36}                       # Indulge inner / Invest outer — fan parallels apart
    COL = {0: IND, 1: INV}
    LOOP_ANG = {(0, 0): 152, (1, 0): 198,          # Junk:    Indulge / Invest (out to the upper-left)
                (0, 1): 243, (1, 1): 297,          # Trying:  Indulge / Invest (down, outside the trough)
                (0, 2): 33,  (1, 2): 77}           # Healthy: Indulge / Invest (out to the upper-right)
    # draw EVERY non-zero transition straight from the matrices (so each row sums to 1)
    for a in (1, 0):                               # Invest under, Indulge over (cosmetic z-order)
        Tm = CHI_T[a]
        for i in range(3):
            for j in range(3):
                p = float(Tm[i, j])
                if p < 1e-6:
                    continue
                if i == j:
                    _loop(ax, P[i], COL[a], p, LOOP_ANG[(a, i)], rn)
                else:
                    _dir_edge(ax, P[i], P[j], MAG[a], COL[a], p, rn)
    for i, c in P.items():                          # nodes on top of the edges
        ax.add_patch(Circle(c, rn, fc="#141414", ec=scol[i], lw=3, zorder=4))
        ax.text(c[0], c[1] + 0.22, name[i], ha="center", va="center", color=WHITE,
                fontsize=11.5, fontweight="bold", zorder=5)
        ax.text(c[0], c[1] - 0.36, f"R={int(CHI_R[i]):+d}", ha="center", va="center",
                color=WHITE, fontsize=10.5, fontweight="bold", zorder=5)
    # legend
    ax.add_patch(FancyArrowPatch((0.5, 7.8), (1.5, 7.8), arrowstyle="-|>", mutation_scale=15, lw=2.4, color=INV))
    ax.text(1.65, 7.8, "Invest (cook / exercise)", color=INV, va="center", fontsize=11.5, fontweight="bold")
    ax.add_patch(FancyArrowPatch((6.2, 7.8), (7.2, 7.8), arrowstyle="-|>", mutation_scale=15, lw=2.4, color=IND))
    ax.text(7.35, 7.8, "Indulge (order out)", color=IND, va="center", fontsize=11.5, fontweight="bold")
    ax.text(5.5, 0.04, "every transition for both actions — each state's out-arrows sum to 1 per action",
            color=DIM, ha="center", fontsize=10.5, style="italic")
    save(fig, "chibany-mdp-diagram.png")


# ==========================================================================
# 4. Transition matrices: "an action = pick the matrix"
# ==========================================================================
def _matrix(ax, M, title, tcol):
    ax.imshow(M, cmap="Blues", vmin=0, vmax=1, alpha=0.55)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{M[i,j]:.1f}", ha="center", va="center",
                    color=WHITE, fontsize=15, fontweight="bold")
    ax.set_xticks(range(3)); ax.set_yticks(range(3))
    ax.set_xticklabels(["J", "T", "H"], color=DIM); ax.set_yticklabels(["J", "T", "H"], color=DIM)
    ax.set_title(title, color=tcol, fontsize=15, fontweight="bold", pad=8)
    ax.set_xlabel("to", color=DIM, fontsize=11); ax.set_ylabel("from", color=DIM, fontsize=11)
    for sp in ax.spines.values(): sp.set_color(DIM)

def fig_chibany_transition_matrices():
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(9.0, 3.9))
    _matrix(a0, CHI_T[0], "Indulge  $T(\\cdot\\,|\\,s,\\,\\mathrm{Indulge})$", PURPLE)
    _matrix(a1, CHI_T[1], "Invest  $T(\\cdot\\,|\\,s,\\,\\mathrm{Invest})$", ACCENT)
    fig.tight_layout()
    save(fig, "chibany-transition-matrices.png")


def fig_chibany_rewards():
    # compact reminder of the reward function R(s) with the J/T/H abbreviations
    fig, ax = plt.subplots(figsize=(4.6, 2.6))
    labels = ["Junk\n(J)", "Trying\n(T)", "Healthy\n(H)"]
    vals = [1, -2, 5]
    cols = [ORANGE, RED, GREEN]
    ax.bar(range(3), vals, color=cols, alpha=0.45, edgecolor=cols, lw=2.4, width=0.62)
    ax.axhline(0, color=DIM, lw=1.2)
    for i, (v, c) in enumerate(zip(vals, cols)):
        ax.text(i, v + (0.35 if v >= 0 else -0.35), f"{v:+d}", ha="center",
                va="bottom" if v >= 0 else "top", color=c, fontsize=15, fontweight="bold")
    ax.set_xticks(range(3)); ax.set_xticklabels(labels, color=WHITE, fontsize=12.5)
    ax.set_yticks([]); ax.set_ylim(-3.4, 6.6)
    ax.set_title("reward  $R(s)$", color=DIM, fontsize=13)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(DIM)
    ax.tick_params(length=0)
    save(fig, "chibany-rewards.png")


# ==========================================================================
# 5. chain -> +reward -> +action  (the build)
# ==========================================================================
def fig_chibany_chain_to_mdp():
    fig, axs = plt.subplots(1, 3, figsize=(10.4, 3.2))
    titles = ["Markov chain\n(one matrix $P$)", "+ reward\n= one-action MDP",
              "+ a choice of matrix\n= MDP (actions)"]
    cols = [DIM, YELLOW, GREEN]
    for k, (ax, t, col) in enumerate(zip(axs, titles, cols)):
        ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
        c0, c1 = (2.6, 4.0), (7.4, 4.0)
        ax.add_patch(Circle(c0, 1.05, fc="#1c1c1c", ec=ACCENT, lw=2.6))
        ax.add_patch(Circle(c1, 1.05, fc="#1c1c1c", ec=ACCENT, lw=2.6))
        ax.text(*c0, "s", color=WHITE, fontsize=18, ha="center", va="center", fontweight="bold")
        ax.text(*c1, "s'", color=WHITE, fontsize=18, ha="center", va="center", fontweight="bold")
        _arrow(ax, (c0[0]+1.1, c0[1]+0.35), (c1[0]-1.1, c1[1]+0.35), -0.25, DIM if k == 0 else ACCENT)
        if k >= 1:
            ax.text(5.0, 1.7, "R(s)", color=YELLOW, fontsize=15, ha="center", fontweight="bold")
        if k == 2:
            _arrow(ax, (c0[0]+1.1, c0[1]-0.35), (c1[0]-1.1, c1[1]-0.35), 0.25, GREEN)
            ax.text(5.0, 5.7, "action a", color=ORANGE, fontsize=12, ha="center", fontweight="bold")
            ax.text(5.0, 2.55, "action b", color=GREEN, fontsize=12, ha="center", fontweight="bold")
        ax.set_title(t, color=col, fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, "chibany-chain-to-mdp.png")


# ==========================================================================
# 6. Value iteration converges; print optimal policy
# ==========================================================================
def fig_value_iteration_converge():
    V, pol, hist = chi_value_iteration(0.9, record=True)
    hist = hist[:55]
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    cols = [ORANGE, RED, GREEN]
    for i in range(3):
        ax.plot(hist[:, i], color=cols[i], lw=3, label=f"V({CHI_S[i].splitlines()[0]})  → {V[i]:.1f}")
        ax.scatter([len(hist)-1], [V[i]], color=cols[i], s=45, zorder=5)
    ax.set_xlabel("value-iteration sweep $k$"); ax.set_ylabel("V(s)")
    ax.legend(fontsize=12, frameon=False, labelcolor=WHITE, loc="lower right")
    ax.set_ylim(-4, 49)
    ax.text(0.8, 47.5, "optimal policy: Invest in every state (brave the −2 trough)",
            color=WHITE, fontsize=11.5, va="top")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    save(fig, "value-iteration-converge.png")


# ==========================================================================
# 7. gamma sweep: Junk-state action flips Indulge->Invest at ~0.64
# ==========================================================================
def fig_gamma_sweep_policy():
    gammas = np.linspace(0.0, 0.99, 300)
    invest = np.array([chi_value_iteration(g)[1][0] for g in gammas])   # action at Junk
    # threshold
    thr = gammas[np.argmax(invest == 1)]
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.axvspan(0, thr, color=PURPLE, alpha=0.16)
    ax.axvspan(thr, 0.99, color=ACCENT, alpha=0.16)
    ax.axvline(thr, color=WHITE, lw=2.4, ls="--")
    ax.text(thr/2, 0.5, "stay in\nthe rut\n(Indulge)", color=PURPLE, ha="center", va="center",
            fontsize=13, fontweight="bold")
    ax.text((thr+0.99)/2, 0.5, "invest &\nget healthy\n(Invest)", color=ACCENT, ha="center", va="center",
            fontsize=13, fontweight="bold")
    ax.text(thr, 1.04, f"flip at γ ≈ {thr:.2f}", color=WHITE, ha="center", fontsize=12, fontweight="bold")
    ax.set_xlabel("discount factor  γ  (how far Chibany looks ahead)")
    ax.set_yticks([]); ax.set_ylim(0, 1.16); ax.set_xlim(0, 0.99)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    save(fig, "gamma-sweep-policy.png")


# ==========================================================================
# 8. Q-learning update anatomy (colour-coded)
# ==========================================================================
def fig_qlearning_update_anatomy():
    fig, ax = plt.subplots(figsize=(10.2, 3.8))
    ax.set_xlim(0, 13); ax.set_ylim(0, 4.6); ax.axis("off")
    y = 2.6
    def box(x, w, txt, col, fs=16):
        ax.add_patch(FancyBboxPatch((x, y-0.5), w, 1.0, boxstyle="round,pad=0.05",
                     fc="none", ec=col, lw=2.4))
        ax.text(x+w/2, y, txt, ha="center", va="center", color=col, fontsize=fs, fontweight="bold")
    # LHS (white — shows on the dark slide)
    ax.text(0.2, y, "$Q(s,a)\\;\\leftarrow\\;Q(s,a)\\;+$", ha="left", va="center",
            color=WHITE, fontsize=16)
    box(5.3, 0.8, "α", ACCENT)
    ax.text(6.25, y, "$[$", ha="center", va="center", color=WHITE, fontsize=24)
    box(6.5, 3.5, "$r + \\gamma\\,\\max_{a'} Q(s',a')$", GREEN, fs=15)
    ax.text(10.2, y, "$-$", ha="center", va="center", color=WHITE, fontsize=20)
    box(10.5, 1.8, "$Q(s,a)$", ORANGE)
    ax.text(12.45, y, "$]$", ha="center", va="center", color=WHITE, fontsize=24)
    # labels — TARGET above; the other three BELOW (no collisions)
    ax.annotate("target = reward + discounted best future", xy=(8.25, y+0.55), xytext=(8.25, 4.15),
                color=GREEN, fontsize=12, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=GREEN))
    ax.annotate("learning\nrate", xy=(5.7, y-0.55), xytext=(5.7, 0.75), color=ACCENT,
                fontsize=11, ha="center", arrowprops=dict(arrowstyle="-", color=ACCENT))
    ax.annotate("current\nestimate", xy=(11.4, y-0.55), xytext=(11.4, 0.75), color=ORANGE,
                fontsize=11, ha="center", arrowprops=dict(arrowstyle="-", color=ORANGE))
    ax.text(8.4, 1.25, "TD error = target − current", color=YELLOW, ha="center",
            fontsize=13, fontweight="bold")
    save(fig, "qlearning-update-anatomy.png")


# ==========================================================================
# GardenPath drawing helpers
# ==========================================================================
def _draw_grid(ax, title=None):
    for r in range(1, 4):
        for c in range(1, 4):
            fc = "#241015" if (r, c) in GARDEN else "#10241a"
            if (r, c) == GOAL: fc = "#2a2410"
            ax.add_patch(Rectangle((c-0.5, r-0.5), 1, 1, fc=fc, ec=DIM, lw=1.6))
    ax.text(1, 1, "start", ha="center", va="center", color=DIM, fontsize=11)
    ax.text(3, 3, "GOAL", ha="center", va="center", color=YELLOW, fontsize=12, fontweight="bold")
    for (r, c) in GARDEN:
        ax.text(c, r-0.34, "garden", ha="center", va="center", color=RED, fontsize=9, alpha=0.8)
    ax.set_xlim(0.4, 3.6); ax.set_ylim(0.4, 3.6); ax.set_aspect("equal"); ax.axis("off")
    if title: ax.set_title(title, color=WHITE, fontsize=14, fontweight="bold")

def _draw_policy(ax, pol, color=ACCENT, cycle=None):
    for s, a in pol.items():
        if cycle and s in cycle: continue
        dr, dc = DELTA[a]
        ax.add_patch(FancyArrowPatch((s[1]-0.28*dc, s[0]-0.28*dr), (s[1]+0.30*dc, s[0]+0.30*dr),
                     arrowstyle="-|>", mutation_scale=16, lw=2.4, color=color, zorder=4))
    if cycle:
        for s in cycle:
            a = pol[s]; dr, dc = DELTA[a]
            ax.add_patch(FancyArrowPatch((s[1]-0.28*dc, s[0]-0.28*dr), (s[1]+0.30*dc, s[0]+0.30*dr),
                         arrowstyle="-|>", mutation_scale=17, lw=3.0, color=RED, zorder=5))


def fig_gardenpath_grid():
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    _draw_grid(ax)
    # the L-path highlighted faintly
    ax.text(2, 0.3, "Path = left column + top row;  Garden = bottom-right 2×2",
            ha="center", color=DIM, fontsize=10)
    save(fig, "gardenpath-grid.png")


# ==========================================================================
# 9. rm vs af: the positive cycle
# ==========================================================================
def fig_feedback_rm_vs_af():
    _, pol_rm = gp_vi(lambda s, a: RM[s][a])
    _, pol_af = gp_vi(lambda s, a: AF[s][a])
    path_rm, ok_rm = gp_rollout(pol_rm)
    path_af, ok_af = gp_rollout(pol_af)
    cycle = set(path_af)   # the loop cells
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(9.4, 4.8))
    _draw_grid(a0, "reward-maximizing (outcome)")
    _draw_policy(a0, pol_rm, color=GREEN)
    a0.text(2, 0.25, "→ learns the path ✓", ha="center", color=GREEN, fontsize=13, fontweight="bold")
    _draw_grid(a1, "action-feedback (how people teach)")
    _draw_policy(a1, pol_af, color=DIM, cycle=cycle)
    a1.text(2, 0.25, "→ loops forever, never reaches goal ✗", ha="center", color=RED,
            fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "feedback-rm-vs-af.png")


# ==========================================================================
# 10. Potential-based shaping (the fix)
# ==========================================================================
def fig_potential_shaping():
    g = 0.95
    def pot(s): return -gp_mdist(s)
    def pbs(s, a):
        s2 = gp_step(s, a)
        base = GFB if s2 == GOAL else (NEG if s2 in GARDEN else 0.0)
        return base + g*pot(s2) - pot(s)
    _, pol = gp_vi(pbs)
    fig, ax = plt.subplots(figsize=(4.9, 4.9))
    # potential field heatmap (closer to goal = brighter)
    for r in range(1, 4):
        for c in range(1, 4):
            v = -gp_mdist((r, c))
            ax.add_patch(Rectangle((c-0.5, r-0.5), 1, 1,
                         fc=plt.cm.viridis((v+4)/4.0), ec=DIM, lw=1.6, alpha=0.55))
            ax.text(c, r+0.32, f"Φ={v}", ha="center", color=WHITE, fontsize=9, alpha=0.8)
    _draw_policy(ax, pol, color=WHITE)
    ax.text(3, 3, "GOAL", ha="center", va="center", color=YELLOW, fontsize=11, fontweight="bold")
    ax.set_xlim(0.4, 3.6); ax.set_ylim(0.4, 3.6); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("potential-based shaping  $F=\\gamma\\Phi(s')-\\Phi(s)$", color=WHITE, fontsize=13)
    ax.text(2, 0.25, "Φ = −dist;  path recovered, no cycle possible ✓", ha="center",
            color=GREEN, fontsize=11, fontweight="bold")
    save(fig, "potential-shaping.png")


# ==========================================================================
# 11. Simulation-based RL (Dyna loop)
# ==========================================================================
def fig_simulation_based_rl():
    fig, ax = plt.subplots(figsize=(8.6, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(-1.1, 6); ax.axis("off")   # extra room below for the caption
    boxes = {
        "world": (1.6, 4.4, "real\nexperience", ACCENT),
        "model": (6.0, 4.4, "learn a MODEL\n$\\hat T, \\hat R$", YELLOW),
        "sim":   (10.2, 4.4, "SIMULATE\nrollouts\n(imagine)", GREEN),
        "plan":  (6.0, 1.3, "plan / improve\nthe policy", ORANGE),
    }
    for k, (x, y, t, col) in boxes.items():
        ax.add_patch(FancyBboxPatch((x-1.4, y-0.8), 2.8, 1.6, boxstyle="round,pad=0.08",
                     fc="none", ec=col, lw=2.6))
        ax.text(x, y, t, ha="center", va="center", color=col, fontsize=13, fontweight="bold")
    _arrow(ax, (3.0, 4.4), (4.6, 4.4), 0, DIM)
    _arrow(ax, (7.4, 4.4), (8.8, 4.4), 0, DIM)
    _arrow(ax, (10.1, 3.6), (7.62, 2.30), -0.2, DIM)   # SIMULATE → plan: stop OUTSIDE the box corner
    _arrow(ax, (4.55, 1.55), (3.18, 3.42), -0.2, DIM)  # plan → real experience: stop OUTSIDE the box corner
    ax.text(6.0, -0.55, "Dyna / AlphaZero / MuZero / Dreamer — plan by simulating a learned model",
            ha="center", color=DIM, fontsize=11, style="italic")
    save(fig, "simulation-based-rl.png")


# ==========================================================================
# 12. RL timeline
# ==========================================================================
def fig_rl_timeline():
    fig, ax = plt.subplots(figsize=(9.8, 2.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
    ax.plot([0.3, 9.7], [1.5, 1.5], color=DIM, lw=2.5)
    items = [("1989", "tabular\nQ-learning", ACCENT), ("2015", "DQN\n(Atari)", TEAL),
             ("2016", "AlphaGo", GREEN), ("2017", "AlphaZero", YELLOW),
             ("2019", "MuZero", ORANGE), ("2023", "Dreamer\nworld models", PURPLE)]
    xs = np.linspace(0.8, 9.2, len(items))
    for x, (yr, lab, col) in zip(xs, items):
        ax.scatter([x], [1.5], s=90, color=col, zorder=4)
        ax.text(x, 2.15, lab, ha="center", va="bottom", color=col, fontsize=12, fontweight="bold")
        ax.text(x, 0.95, yr, ha="center", va="top", color=DIM, fontsize=11)
    ax.annotate("", xy=(9.6, 0.5), xytext=(0.6, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=DIM))
    ax.text(5, 0.18, "function approximation  +  simulation", ha="center", color=DIM,
            fontsize=11, style="italic")
    save(fig, "rl-timeline.png")


def fig_ho_modelbased():
    # Ho et al.: with human evaluative feedback, model-BASED RL does even worse
    # than model-free, because it propagates the miscalibrated signal further.
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    t = np.linspace(0, 1, 120)
    rm = 0.15 + 0.78 * (1 - np.exp(-4.5 * t))          # outcome reward: learns the task
    af_mf = 0.15 + 0.17 * (1 - np.exp(-3.0 * t))       # human feedback, model-free: poor
    af_mb = 0.15 - 0.11 * (1 - np.exp(-3.2 * t))       # human feedback, model-based: WORSE
    ax.plot(t, rm, color=GREEN, lw=3, label="outcome reward — learns ✓")
    ax.plot(t, af_mf, color=ORANGE, lw=2.8, label="human feedback · model-free")
    ax.plot(t, af_mb, color=RED, lw=3, label="human feedback · model-based")
    ax.annotate("model-based does EVEN WORSE —\nit propagates the miscalibrated\nhuman signal further",
                xy=(0.74, 0.15 - 0.11 * (1 - np.exp(-3.2 * 0.74))), xytext=(0.30, 0.46),
                color=RED, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlabel("training →"); ax.set_ylabel("task performance")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(0, 1.0)
    ax.legend(fontsize=10.5, frameon=False, labelcolor="linecolor", loc="center right")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    save(fig, "ho-modelbased-worse.png")


# ==========================================================================
# 13. Dopamine = TD error
# ==========================================================================
def fig_dopamine_td():
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.4); ax.axis("off")
    ax.text(6, 3.7, "$\\delta_t = r_{t+1} + \\gamma\\,V(s_{t+1}) - V(s_t)$",
            ha="center", color=WHITE, fontsize=20)
    ax.text(6, 2.75, "the TD error", ha="center", color=YELLOW, fontsize=14, fontweight="bold")
    ax.annotate("", xy=(6, 2.0), xytext=(6, 2.5), arrowprops=dict(arrowstyle="-|>", color=DIM))
    ax.text(6, 1.7, "= midbrain DOPAMINE prediction-error signal",
            ha="center", color=GREEN, fontsize=14, fontweight="bold")
    ax.text(6, 0.7, "Schultz, Dayan & Montague (1997) — reward learning in the brain\n"
            "model-based vs model-free ≈ goal-directed vs habitual (Daw et al. 2005)",
            ha="center", color=DIM, fontsize=11, style="italic")
    save(fig, "dopamine-td.png")


if __name__ == "__main__":
    fig_dt_risk_curve()
    fig_dt_loss_estimators()
    fig_chibany_mdp_diagram()
    fig_chibany_transition_matrices()
    fig_chibany_rewards()
    fig_chibany_chain_to_mdp()
    fig_value_iteration_converge()
    fig_gamma_sweep_policy()
    fig_qlearning_update_anatomy()
    fig_gardenpath_grid()
    fig_feedback_rm_vs_af()
    fig_potential_shaping()
    fig_simulation_based_rl()
    fig_rl_timeline()
    fig_ho_modelbased()
    fig_dopamine_td()
    print("\nAll Week 8 figures written to images/.")
