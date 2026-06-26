#!/usr/bin/env python3
"""Generate Week 9 (Inverse RL / social cognition / POMDPs) figures.

Transparent background, light strokes/text for the dark SDS RevealJS theme
(#111111); colours mirror sds-reveal/sds.scss. Run:  python3 make_figures.py
Outputs land in images/.

The gridworld goal-inference numbers and the Tiger belief numbers are re-derived
here in numpy and MATCH the GenJAX-verified backbones (genjax_goal_inference.py,
genjax_tiger_pomdp.py, genjax_legible_teaching.py).

Figures:
  inverse-vs-forward.png        forward RL (goal->actions) | inverse RL (actions->goal)
  bayes-inversion.png           P(g|tau) ∝ P(tau|g) P(g) anatomy (likelihood = the policy)
  goal-inference-posterior.png  gridworld trajectory + posterior-over-goals bars (freeze-frame)
  ill-posed-inversion.png       one short path, many goals consistent
  softmax-rationality.png       goal posterior sharpening with beta (flat -> sharp)
  tom-as-irl.png                forward = simulate planner | inverse = invert it
  food-truck-btom.png           food-truck gridworld: occluder + K/L/M + detour
  tiger-belief-update.png       belief 0.5->0.85->0.97 on the line + alpha-vector PWLC
  pomdp-to-belief-mdp.png       POMDP -> belief-MDP schematic + Bayes update
  legible-vs-efficient.png      Dragan reach: efficient (ambiguous) | legible (early veer)
  showing-vs-doing-grid.png     gridworld do | show + observer posterior (verified numbers)
  reward-recovery-heatmap.png   visitation -> recovered reward -> ground truth heatmaps
  irl-methods-timeline.png      MaxEnt -> GAIL -> AIRL -> RLHF/DPO
  amortized-vs-bayesian-tom.png ToMnet (learned) | Bayesian inversion (explicit)
  llm-tom-debate.png            capability claims <-> skeptical rebuttals; pass != mechanism
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch, Rectangle, Wedge
import matplotlib.patheffects as pe

# ---- theme (mirror sds-reveal/sds.scss) ----------------------------------
BG, WHITE, DIM = "#111111", "#FFFFFF", "#999999"
ACCENT, YELLOW, RED = "#64B5F6", "#FFEB3B", "#EF5350"
GREEN, ORANGE, PURPLE, TEAL = "#66BB6A", "#FFA726", "#BA68C8", "#4DD0E1"

plt.rcParams.update({
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
    "text.color": WHITE, "axes.edgecolor": DIM, "axes.labelcolor": WHITE,
    "xtick.color": DIM, "ytick.color": DIM, "font.size": 15, "font.family": "DejaVu Sans",
})

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
os.makedirs(IMG, exist_ok=True)


def save(fig, name):
    p = os.path.join(IMG, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", transparent=True, pad_inches=0.15)
    plt.close(fig)
    print("wrote", os.path.relpath(p, HERE))


def box(ax, xy, w, h, text, fc="none", ec=WHITE, tc=WHITE, fs=14, lw=2, z=2):
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, lw=lw,
                boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec=ec, zorder=z))
    ax.text(x, y, text, ha="center", va="center", color=tc, fontsize=fs, zorder=z + 1)


def arrow(ax, p0, p1, color=ACCENT, lw=2.5, ls="-", z=1):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=18,
                lw=lw, color=color, ls=ls, shrinkA=6, shrinkB=6, zorder=z))


# ==========================================================================
# VERIFIED CORES — gridworld inverse planning (matches genjax_goal_inference.py)
# ==========================================================================
NR = NC = 3
NS, NA = NR * NC, 4
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def step(s, a):
    r, c = divmod(s, NC)
    if a == UP:    r = min(r + 1, NR - 1)
    elif a == DOWN:  r = max(r - 1, 0)
    elif a == LEFT:  c = max(c - 1, 0)
    elif a == RIGHT: c = min(c + 1, NC - 1)
    return r * NC + c


TRANS = np.array([[step(s, a) for a in range(NA)] for s in range(NS)])


def q_for_goal(goal, gamma=0.9):
    reward = (TRANS == goal).astype(float)
    isg = np.arange(NS) == goal
    V = np.zeros(NS)
    for _ in range(60):
        V = np.where(isg, 0.0, (reward + gamma * V[TRANS]).max(1))
    return reward + gamma * V[TRANS]


def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()


def goal_posterior(goals, states, actions, beta=3.0):
    Q = {g: q_for_goal(g) for g in goals}
    logp = np.array([sum(np.log(softmax(beta * Q[g][s])[a]) for s, a in zip(states, actions))
                     for g in goals])
    p = np.exp(logp - logp.max())
    return p / p.sum()


def rollout(start, actions):
    s, states = start, []
    for a in actions:
        states.append(s); s = step(s, a)
    return states


def cell_xy(s):
    r, c = divmod(s, NC)
    return c + 0.5, r + 0.5


def draw_grid(ax, goals_named, start, path_actions=None, path_color=YELLOW, title=None,
              start_label="start"):
    for x in range(NC + 1):
        ax.plot([x, x], [0, NR], color=DIM, lw=1, alpha=0.5)
    for y in range(NR + 1):
        ax.plot([0, NC], [y, y], color=DIM, lw=1, alpha=0.5)
    cols = {"left": RED, "mid": YELLOW, "right": GREEN, "G1": RED, "G2": GREEN}
    for name, s in goals_named.items():
        x, y = cell_xy(s)
        ax.add_patch(Rectangle((x - .5, y - .5), 1, 1, fc=cols.get(name, ACCENT), alpha=.22, ec="none"))
        ax.text(x, y + .3, name, ha="center", va="center", color=cols.get(name, ACCENT), fontsize=12)
        ax.plot(x, y, "*", color=cols.get(name, ACCENT), ms=18)
    sx, sy = cell_xy(start)
    ax.plot(sx, sy, "o", color=WHITE, ms=12)
    ax.text(sx, sy - .32, start_label, ha="center", va="center", color=WHITE, fontsize=11)
    if path_actions:
        states = rollout(start, path_actions) + [step(rollout(start, path_actions)[-1], path_actions[-1])]
        xs = [cell_xy(s)[0] for s in states]
        ys = [cell_xy(s)[1] for s in states]
        ax.plot(xs, ys, "-", color=path_color, lw=3, zorder=3,
                path_effects=[pe.Stroke(linewidth=5, foreground=BG), pe.Normal()])
        ax.plot(xs[-1], ys[-1], "o", color=path_color, ms=9, zorder=4)
    ax.set_xlim(-.2, NC + .2); ax.set_ylim(-.2, NR + .2)
    ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, color=WHITE, fontsize=14)


# ==========================================================================
# 0. THE MASTER FRAME — the agent model (a POMDP) and its unknowns.
#    One diagram, reused every block with a different piece highlighted.
# ==========================================================================
def _agent_model(ax, highlight=()):
    """Draw the POMDP agent-loop. `highlight` = names to light up in YELLOW.
    pieces: R (reward/goal), b (belief), s (world state), o (observation),
            pi (policy), a (action)."""
    ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis("off")

    def pc(name):                      # edge/text colour, brightened if highlighted
        on = name in highlight
        base = dict(R=GREEN, b=YELLOW, s=RED, o=ACCENT, pi=WHITE, a=GREEN)[name]
        return (YELLOW if on else base, on)

    def piece(name, xy, w, h, text, fs=12):
        col, on = pc(name)
        if on:                          # glow behind the highlighted piece
            ax.add_patch(FancyBboxPatch((xy[0] - w/2 - .12, xy[1] - h/2 - .12), w + .24, h + .24,
                        boxstyle="round,pad=0.02,rounding_size=0.08", fc=YELLOW, ec="none",
                        alpha=.16, zorder=1))
        box(ax, xy, w, h, text, ec=col, tc=col, fs=fs, lw=(3 if on else 2), z=3)

    # loop layout: reward (top) drives policy; belief from observations; action observed
    piece("R",  (6.0, 6.4), 3.4, 0.95, "reward / goal  R", fs=12)
    piece("b",  (2.4, 3.9), 3.0, 1.05, "belief  b(s)\n= P(s | history)", fs=11)
    piece("pi", (6.0, 3.9), 2.3, 0.95, "policy  π", fs=12)
    piece("a",  (9.7, 3.9), 3.0, 0.95, "action  a", fs=12)
    piece("o",  (2.4, 1.2), 3.0, 0.95, "observation  o", fs=12)
    piece("s",  (9.7, 1.2), 3.0, 0.95, "world state  s", fs=12)
    # arrows of the loop
    arrow(ax, (6.0, 5.9), (6.0, 4.4), color=DIM)                 # R -> pi
    arrow(ax, (3.9, 3.9), (4.8, 3.9), color=DIM)                 # b -> pi
    arrow(ax, (7.2, 3.9), (8.2, 3.9), color=DIM)                 # pi -> a
    arrow(ax, (9.7, 3.4), (9.7, 1.7), color=DIM)                 # a -> s'  (transition T)
    ax.text(10.0, 2.55, "T", color=DIM, fontsize=11, ha="left")
    arrow(ax, (8.2, 1.2), (3.9, 1.2), color=DIM)                 # s -> o   (observation O)
    ax.text(6.05, 1.45, "O", color=DIM, fontsize=11, ha="center")
    arrow(ax, (2.4, 1.7), (2.4, 3.35), color=DIM)                # o -> b   (Bayes update)
    ax.text(1.95, 2.55, "Bayes", color=DIM, fontsize=9, ha="right", rotation=90)
    ax.text(9.7, 4.62, "observed", color=GREEN, fontsize=9.5, ha="center", style="italic")
    ax.text(9.7, 0.46, "hidden", color=RED, fontsize=9.5, ha="center", style="italic")


def fig_agent_model():
    variants = [
        ("agent-model-pomdp.png", (),
         "Week 8 ran this FORWARD (all pieces known → behavior).  "
         "Week 9: watch the behavior, infer a hidden piece."),
        ("agent-model-R.png", ("R",),
         "Infer the reward / goal R from behavior  →  goal inference & inverse RL"),
        ("agent-model-belief.png", ("b", "s"),
         "Infer the agent's belief b (it may be FALSE: b ≠ s)  →  Theory of Mind, POMDPs"),
    ]
    for name, hl, cap in variants:
        fig, ax = plt.subplots(figsize=(8.8, 5.4))
        _agent_model(ax, highlight=hl)
        ax.text(6.0, 0.18, cap, ha="center", color=(YELLOW if hl else DIM), fontsize=11)
        save(fig, name)


def fig_recursive_teaching():
    """Ho et al. 2021: showing = belief-directed planning. The observer inverts
    your actions (level 0); you plan actions to drive the observer's belief
    (level 1) — a POMDP whose hidden state is the OBSERVER'S belief."""
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.4); ax.axis("off")
    # level 0 — the observer doing inverse planning on you
    ax.text(6.0, 6.05, "level 0 — the observer reads you (inverse planning)",
            color=ACCENT, fontsize=11.5, ha="center")
    box(ax, (2.6, 4.9), 3.2, 0.9, "your action  a", ec=GREEN, tc=GREEN, fs=12)
    box(ax, (9.0, 4.9), 4.0, 0.9, "observer's belief\nabout your goal", ec=ACCENT, tc=ACCENT, fs=11)
    arrow(ax, (4.3, 4.9), (6.9, 4.9), color=ACCENT)
    ax.text(5.6, 5.18, "infers", color=ACCENT, fontsize=9.5, ha="center")
    # level 1 — you, planning over that belief
    ax.text(6.0, 3.25, "level 1 — you plan actions to shape that belief",
            color=YELLOW, fontsize=11.5, ha="center")
    box(ax, (9.0, 1.9), 4.0, 0.95, "observer's belief\n(hidden state to you)", ec=YELLOW, tc=YELLOW, fs=11)
    box(ax, (2.6, 1.9), 3.2, 0.95, "your action  a", ec=GREEN, tc=GREEN, fs=12)
    arrow(ax, (6.9, 1.9), (4.3, 1.9), color=YELLOW)
    ax.text(5.6, 2.18, "choose a to maximize it", color=YELLOW, fontsize=9, ha="center")
    ax.text(6.0, 0.5, "you are uncertain about the observer's belief and act to move it "
            "→ a POMDP whose hidden state is the observer's belief  (Ho et al. 2021)",
            ha="center", color=DIM, fontsize=10.5)
    save(fig, "recursive-pomdp-teaching.png")


# ==========================================================================
# 1. forward vs inverse RL
# ==========================================================================
def fig_inverse_vs_forward():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax = axes[0]
    ax.set_title("forward RL  (Week 8)", color=ACCENT, fontsize=16, pad=2)
    box(ax, (1.7, 2), 2.6, 1.2, "goal /\nreward", ec=ACCENT, tc=ACCENT)
    box(ax, (5, 2), 2.2, 1.2, "policy π", ec=WHITE)
    box(ax, (8.3, 2), 2.6, 1.2, "actions", ec=GREEN, tc=GREEN)
    arrow(ax, (3.0, 2), (3.9, 2)); arrow(ax, (6.1, 2), (7.0, 2))
    ax.text(5, 0.5, "plan: what should I do?", ha="center", color=DIM, fontsize=12)
    ax = axes[1]
    ax.set_title("inverse RL  (this week)", color=YELLOW, fontsize=16, pad=2)
    box(ax, (1.7, 2), 2.6, 1.2, "actions", ec=GREEN, tc=GREEN)
    box(ax, (5, 2), 2.2, 1.2, "invert", ec=YELLOW, tc=YELLOW)
    box(ax, (8.3, 2), 2.6, 1.2, "goal /\nreward", ec=ACCENT, tc=ACCENT)
    arrow(ax, (3.0, 2), (3.9, 2), color=YELLOW); arrow(ax, (6.1, 2), (7.0, 2), color=YELLOW)
    ax.text(5, 0.5, "read minds: what did they want?", ha="center", color=DIM, fontsize=12)
    save(fig, "inverse-vs-forward.png")


# ==========================================================================
# 2. Bayes inversion anatomy
# ==========================================================================
def fig_bayes_inversion():
    fig, ax = plt.subplots(figsize=(10.5, 3.2))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.text(0.2, 2.0, r"$P(\,\mathrm{goal}\mid\mathrm{actions}\,)$", color=YELLOW, fontsize=24, va="center")
    ax.text(3.7, 2.0, r"$\propto$", color=WHITE, fontsize=24, va="center")
    ax.text(4.4, 2.0, r"$P(\,\mathrm{actions}\mid\mathrm{goal}\,)$", color=ACCENT, fontsize=24, va="center")
    ax.text(7.7, 2.0, r"$\cdot$", color=WHITE, fontsize=24, va="center")
    ax.text(8.0, 2.0, r"$P(\,\mathrm{goal}\,)$", color=GREEN, fontsize=24, va="center")
    ax.text(1.7, 0.8, "posterior\n(what we infer)", color=YELLOW, fontsize=13, ha="center", va="center")
    ax.text(5.9, 0.8, "likelihood = a policy\n(how a goal-seeker acts:\nsoftmax over Q), in reverse", color=ACCENT, fontsize=13, ha="center", va="center")
    ax.text(9.0, 0.8, "prior\nover goals", color=GREEN, fontsize=13, ha="center", va="center")
    save(fig, "bayes-inversion.png")


# ==========================================================================
# 3. goal inference posterior (freeze-frame)  + 4. ill-posed
# ==========================================================================
def fig_goal_inference_posterior():
    goals = {"left": 6, "mid": 7, "right": 8}
    start, acts = 0, [RIGHT, RIGHT, UP, UP]
    states = rollout(start, acts)
    fig = plt.figure(figsize=(11, 4.2))
    axg = fig.add_axes([0.02, 0.08, 0.42, 0.86])
    draw_grid(axg, goals, start, acts, title="observed path:  →  →  ↑  ↑")
    axb = fig.add_axes([0.56, 0.18, 0.40, 0.72])
    names = ["left", "mid", "right"]
    cols = [RED, YELLOW, GREEN]
    steps = range(1, len(acts) + 1)
    width = 0.24
    for i, nm in enumerate(names):
        vals = [goal_posterior(list(goals.values()), states[:k], acts[:k])[i] for k in steps]
        axb.bar(np.array(list(steps)) + (i - 1) * width, vals, width, color=cols[i], label=nm, alpha=.9)
    axb.set_xticks(list(steps)); axb.set_xlabel("actions observed")
    axb.set_ylabel("P(goal | actions)"); axb.set_ylim(0, 1)
    axb.set_title("posterior concentrates on 'right'", color=WHITE, fontsize=14)
    axb.legend(facecolor="none", edgecolor=DIM, labelcolor=WHITE, fontsize=11, ncol=3, loc="upper center")
    for sp in axb.spines.values():
        sp.set_color(DIM)
    save(fig, "goal-inference-posterior.png")


def fig_ill_posed():
    goals = {"left": 6, "mid": 7, "right": 8}
    start = 0
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    draw_grid(ax, goals, start, [UP], path_color=WHITE,
              title="one step up — heading where?")
    # dashed lines from current pos to all goals
    cur = cell_xy(step(start, UP))
    for s in goals.values():
        gx, gy = cell_xy(s)
        ax.plot([cur[0], gx], [cur[1], gy], "--", color=DIM, lw=1.5, alpha=.8, zorder=2)
    ax.text(1.5, -.15, "a short path fits every goal — the prior + rationality decide",
            ha="center", color=DIM, fontsize=11)
    save(fig, "ill-posed-inversion.png")


# ==========================================================================
# 5. softmax rationality (posterior sharpens with beta)
# ==========================================================================
def fig_softmax_rationality():
    goals = {"left": 6, "mid": 7, "right": 8}
    start, acts = 0, [RIGHT, RIGHT, UP, UP]
    states = rollout(start, acts)
    betas = [0.1, 1.0, 2.0, 3.0, 5.0, 8.0]
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    names = ["left", "mid", "right"]
    cols = [RED, YELLOW, GREEN]
    for i, nm in enumerate(names):
        ys = [goal_posterior(list(goals.values()), states, acts, beta=b)[i] for b in betas]
        ax.plot(betas, ys, "-o", color=cols[i], lw=2.5, ms=6, label=nm)
    ax.set_xlabel(r"rationality  $\beta$  (0 = random,  large = greedy / exploit)")
    ax.set_ylabel("P(goal | the rightward path)"); ax.set_ylim(0, 1)
    ax.set_title("same rightward path (→→↑↑), varying β — the inference is only as good as the rationality assumption",
                 color=WHITE, fontsize=10.5)
    ax.axhline(1/3, color=DIM, ls=":", lw=1.5)
    ax.text(0.2, 0.36, "uninformative (1/3)", color=DIM, fontsize=10)
    ax.legend(facecolor="none", edgecolor=DIM, labelcolor=WHITE, fontsize=11)
    for sp in ax.spines.values():
        sp.set_color(DIM)
    save(fig, "softmax-rationality.png")


# ==========================================================================
# 6. ToM = IRL
# ==========================================================================
def fig_tom_as_irl():
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.0); ax.axis("off")
    # forward row — label sits in its own band ABOVE the boxes (no overlap)
    ax.text(5, 4.62, "forward: simulate the planner", color=ACCENT, fontsize=11.5, ha="center")
    box(ax, (2, 3.55), 3.0, 1.0, "mind\n(goal, belief, reward)", ec=ACCENT, tc=ACCENT, fs=12)
    box(ax, (8, 3.55), 3.0, 1.0, "behavior\n(actions)", ec=GREEN, tc=GREEN, fs=12)
    arrow(ax, (3.6, 3.55), (6.4, 3.55), color=ACCENT)
    # inverse row — label in the clear gap between the two rows
    ax.text(5, 2.45, "inverse: invert it = Theory of Mind", color=YELLOW, fontsize=11.5, ha="center")
    arrow(ax, (6.4, 1.4), (3.6, 1.4), color=YELLOW)
    box(ax, (2, 1.4), 3.0, 1.0, "mind", ec=ACCENT, tc=ACCENT, fs=12)
    box(ax, (8, 1.4), 3.0, 1.0, "behavior", ec=GREEN, tc=GREEN, fs=12)
    ax.text(5, 0.35, "Baker & Tenenbaum's inverse planning;  reviewed as 'ToM = IRL' (Jara-Ettinger 2019)",
            color=DIM, fontsize=11, ha="center")
    save(fig, "tom-as-irl.png")


# ==========================================================================
# 7. food-truck BToM
# ==========================================================================
def fig_food_truck():
    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    W, H = 6, 4
    for x in range(W + 1):
        ax.plot([x, x], [0, H], color=DIM, lw=.6, alpha=.3)
    for y in range(H + 1):
        ax.plot([0, W], [y, y], color=DIM, lw=.6, alpha=.3)
    ax.text(W / 2, H + 0.72, "Chibany wants:   Mexican (favorite)  >  Korean  >  Lebanese",
            ha="center", color=WHITE, fontsize=12)
    # building — hides the far spot from the start; he must round it to see the far truck
    ax.add_patch(Rectangle((4.0, 1.2), 1.05, 1.7, fc=DIM, alpha=.5, ec=WHITE, lw=1.4))
    ax.text(4.52, 2.0, "building", ha="center", va="center", color=WHITE, fontsize=9.5)
    # Korean truck — VISIBLE, upper-left
    ax.add_patch(Rectangle((0.35, 2.85), 0.8, 0.58, fc=YELLOW, alpha=.85, ec="none"))
    ax.text(0.75, 3.14, "K", ha="center", va="center", color=BG, fontsize=12, weight="bold")
    ax.text(0.75, 2.62, "Korean — can see it", ha="center", color=GREEN, fontsize=8.5)
    # Lebanese truck — HIDDEN behind/above the building; only visible once he rounds it
    ax.add_patch(Rectangle((4.12, 3.05), 0.8, 0.55, fc=ACCENT, alpha=.85, ec="none"))
    ax.text(4.52, 3.32, "L", ha="center", va="center", color=BG, fontsize=12, weight="bold")
    ax.text(4.52, 3.78, "Lebanese — hidden", ha="center", color=RED, fontsize=8.5)
    # Mexican — his favorite, absent today
    ax.text(1.95, 3.82, "Mexican? his favorite —\nnot here today", ha="center", va="center",
            color=GREEN, fontsize=8.5, style="italic")
    # start
    ax.plot(3.0, 0.3, "o", color=WHITE, ms=11)
    ax.text(3.0, -0.02, "start", ha="center", color=WHITE, fontsize=9.5)
    # dashed: the efficient grab IF Korean were all he wanted
    ax.plot([3.0, 0.78], [0.46, 2.82], "--", color=DIM, lw=1.3, alpha=.7)
    ax.text(1.32, 1.2, "direct to Korean\n(if that's all he wanted)", ha="center",
            color=DIM, fontsize=7.5, rotation=34)
    # path ①: detour UP to peek at the hidden far spot — stops where L becomes visible
    ax.plot([3.0, 3.35, 3.62], [0.5, 2.0, 3.0], "-", color=WHITE, lw=2.6, zorder=3,
            path_effects=[pe.Stroke(linewidth=4, foreground=BG), pe.Normal()])
    ax.annotate("", xy=(3.98, 3.2), xytext=(3.62, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=2.3))
    ax.text(2.74, 2.2, "① detours to peek\n→ it's Lebanese", color=WHITE, fontsize=8, ha="center")
    # path ②: NOW he can see it's Lebanese — efficient straight line back to Korean
    ax.plot([3.6, 1.2], [3.12, 3.06], "-", color=YELLOW, lw=2.6, zorder=3,
            path_effects=[pe.Stroke(linewidth=4, foreground=BG), pe.Normal()])
    ax.annotate("", xy=(1.18, 3.06), xytext=(1.5, 3.07),
                arrowprops=dict(arrowstyle="-|>", color=YELLOW, lw=2.3))
    ax.text(2.45, 3.3, "② efficient path to Korean", color=YELLOW, fontsize=8, ha="center")
    ax.set_xlim(-0.4, W + 0.4); ax.set_ylim(-0.3, H + 1.1); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("He skips the visible Korean to peek at the hidden spot — only worth it if he hoped for Mexican",
                 color=WHITE, fontsize=11, pad=6)
    save(fig, "food-truck-btom.png")


# ==========================================================================
# 8. Tiger belief update + alpha-vector PWLC
# ==========================================================================
def tiger_beliefs():
    acc = 0.85
    b = 0.5; seq = [0.5]
    for _ in range(3):
        b = (b * acc) / (b * acc + (1 - b) * (1 - acc))
        seq.append(b)
    return seq  # [0.5, 0.85, 0.9698, 0.9945]


def fig_tiger_belief():
    """Belief-only: the belief slides toward tiger-left as growls arrive, with a
    stick figure between two doors. NO alpha-vectors here (introduced later)."""
    seq = tiger_beliefs()
    fig, (axd, axb) = plt.subplots(2, 1, figsize=(8.6, 5.2),
                                   gridspec_kw=dict(height_ratios=[1, 1.5]))
    # ---- top: a person between two doors ----
    axd.set_xlim(0, 10); axd.set_ylim(-0.4, 3.4); axd.set_aspect("equal"); axd.axis("off")
    axd.add_patch(Rectangle((1.2, 0.3), 1.1, 2.2, fill=False, ec=RED, lw=2.2))
    axd.add_patch(Circle((2.05, 1.4), 0.07, color=RED))
    axd.text(1.75, 0.0, "LEFT door", ha="center", color=RED, fontsize=9.5)
    axd.text(1.75, 2.95, "tiger likely here\nas b → 1", ha="center", color=RED, fontsize=8.5)
    axd.add_patch(Rectangle((7.7, 0.3), 1.1, 2.2, fill=False, ec=GREEN, lw=2.2))
    axd.add_patch(Circle((7.95, 1.4), 0.07, color=GREEN))
    axd.text(8.25, 0.0, "RIGHT door", ha="center", color=GREEN, fontsize=9.5)
    axd.text(8.25, 2.95, "correct / safe\nas b → 1", ha="center", color=GREEN, fontsize=8.5)
    sx, sy = 5.0, 1.1
    axd.add_patch(Circle((sx, sy + 0.78), 0.26, fill=False, ec=WHITE, lw=2))   # head
    axd.plot([sx, sx], [sy + 0.52, sy - 0.35], color=WHITE, lw=2)              # body
    axd.plot([sx - 0.5, sx + 0.5], [sy + 0.3, sy + 0.3], color=WHITE, lw=2)    # arms
    axd.plot([sx, sx - 0.42], [sy - 0.35, sy - 1.0], color=WHITE, lw=2)        # leg
    axd.plot([sx, sx + 0.42], [sy - 0.35, sy - 1.0], color=WHITE, lw=2)        # leg
    axd.text(5.0, 2.8, "which door?", ha="center", color=WHITE, fontsize=9.5)
    # ---- bottom: belief sliding toward tiger-left ----
    axb.set_xlim(-0.04, 1.04); axb.set_ylim(0, len(seq)); axb.invert_yaxis()
    labels = ["start", "+1 growl L", "+2 growls L", "+3 growls L"]
    for i, (b, lab) in enumerate(zip(seq, labels)):
        axb.plot([0, 1], [i + .5, i + .5], color=DIM, lw=1, alpha=.4)
        axb.plot(b, i + .5, "o", color=YELLOW, ms=15, zorder=3)
        axb.text(b, i + .12, f"{b:.3f}", ha="center", color=YELLOW, fontsize=10.5)
        axb.text(-0.02, i + .5, lab, ha="right", va="center", color=WHITE, fontsize=10.5)
    axb.annotate("", xy=(1.0, len(seq) - 0.5), xytext=(0.55, len(seq) - 0.5),
                 arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5))
    axb.text(0.77, len(seq) - 0.16, "surer it's LEFT → open RIGHT", color=GREEN, fontsize=9, ha="center")
    axb.set_xlabel("belief  b = P(tiger-left)"); axb.set_yticks([])
    axb.set_title("each growl shifts the belief by Bayes — open the correct door once you're sure enough",
                  color=WHITE, fontsize=11)
    for sp in axb.spines.values():
        sp.set_color(DIM)
    save(fig, "tiger-belief-update.png")


def fig_tiger_alpha():
    """Each action's EXPECTED value vs belief is a straight line — a weighted
    average of its two outcomes (its alpha-vector). Full y-range so b=0.5 shows."""
    fig, ax = plt.subplots(figsize=(8.9, 5.1))
    b = np.linspace(0, 1, 200)
    v_listen = np.full_like(b, -1.0)
    v_openR = 110 * b - 100        # open RIGHT: +10 if tiger-LEFT (prob b), -100 if tiger-RIGHT
    v_openL = -110 * b + 10        # open LEFT:  mirror image
    ax.plot(b, v_openL, color=RED, lw=2.3)
    ax.plot(b, v_openR, color=GREEN, lw=2.3)
    ax.plot(b, v_listen, color=ACCENT, lw=2.3)
    env = np.maximum.reduce([v_listen, v_openR, v_openL])
    ax.plot(b, env, color=YELLOW, lw=7, alpha=.30, zorder=0)
    # direct line labels (clearer than a legend over the X-shape)
    ax.text(0.30, -27, "open LEFT", color=RED, fontsize=9, rotation=-37, ha="center")
    ax.text(0.70, -27, "open RIGHT", color=GREEN, fontsize=9, rotation=37, ha="center")
    ax.text(0.16, 3.5, "listen (−1)", color=ACCENT, fontsize=9)
    ax.text(0.5, 14, "optimal value = the max (envelope)", color="#b9a93a", fontsize=8.5, ha="center")
    # open-RIGHT's two ENDPOINTS *are* its alpha-vector — its value in each world
    ax.plot([0, 1], [-100, 10], "o", color=GREEN, ms=6, zorder=4)
    ax.annotate("b=1: tiger surely LEFT →\nopen RIGHT is safe (+10)", xy=(1, 10),
                xytext=(0.60, 33), color=GREEN, fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1))
    ax.annotate("b=0: tiger surely RIGHT →\nopen RIGHT = tiger (−100)", xy=(0, -100),
                xytext=(0.26, -92), color=GREEN, fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1))
    ax.text(0.02, 26, "(open LEFT is\nthe mirror)", color=RED, fontsize=8, ha="left", va="top")
    # b = 0.5 — the two open lines meet at -45 (a coin flip on a tiger); listen wins
    ax.axvline(0.5, color=DIM, ls=":", lw=1.2)
    ax.plot(0.5, -45, "o", color=WHITE, ms=7, zorder=5)
    ax.plot(0.5, -1, "o", color=ACCENT, ms=6, zorder=5)
    ax.annotate("b=0.5: a −45 gamble — listen wins", xy=(0.5, -45), xytext=(0.5, -67),
                color=WHITE, fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=1))
    # open threshold: open-RIGHT overtakes listen at b = 0.90
    ax.axvline(0.90, color=GREEN, ls="--", lw=1.3, alpha=.8)
    ax.plot(0.90, -1, "o", color=YELLOW, ms=8, zorder=6, mec=BG)
    ax.annotate("b ≈ 0.90: open RIGHT\nfinally beats listen → open", xy=(0.90, -1),
                xytext=(0.84, 30), color=YELLOW, fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=YELLOW, lw=1))
    ax.set_ylim(-116, 46); ax.set_xlim(0, 1)
    ax.set_xlabel("belief  b = P(tiger-left)"); ax.set_ylabel("value of acting now")
    ax.set_title("each action's value = a weighted average of its two outcomes → a straight line (its α-vector)",
                 color=WHITE, fontsize=10)
    for sp in ax.spines.values():
        sp.set_color(DIM)
    save(fig, "tiger-alpha-vectors.png")


def _env_val(b):
    """Optimal value (upper envelope of the three alpha-vectors) at belief b."""
    return max(-110 * b + 10, 110 * b - 100, -1.0)


def fig_tiger_walk():
    """A 3-frame walk: the belief marker rides the envelope as growls arrive,
    sliding along the LISTEN line, then hopping up onto OPEN-RIGHT past b=0.90."""
    bs = [0.5, 0.85, 0.9698]
    caps = [
        "Start uncertain: b = 0.5.  The top line is LISTEN → so you listen.",
        "A growl from the LEFT → b jumps to 0.85.  Still left of 0.90 → listen again.",
        "Another LEFT growl → b = 0.97.  Crossed 0.90 — OPEN-RIGHT is now on top → open!",
    ]
    acts = ["listen", "listen", "open"]
    for i in range(3):
        fig, ax = plt.subplots(figsize=(8.8, 4.7))
        b = np.linspace(0, 1, 200)
        vL = -110 * b + 10; vR = 110 * b - 100; vLi = np.full_like(b, -1.0)
        env = np.maximum.reduce([vLi, vR, vL])
        ax.axvspan(0, 0.10, color=RED, alpha=.05)
        ax.axvspan(0.10, 0.90, color=ACCENT, alpha=.05)
        ax.axvspan(0.90, 1.0, color=GREEN, alpha=.05)
        ax.plot(b, vL, color=RED, lw=1.7, alpha=.85)
        ax.plot(b, vR, color=GREEN, lw=1.7, alpha=.85)
        ax.plot(b, vLi, color=ACCENT, lw=1.7, alpha=.85)
        ax.plot(b, env, color=YELLOW, lw=6, alpha=.28, zorder=0)
        ax.axvline(0.90, color=DIM, ls="--", lw=1, alpha=.6)
        ax.text(0.90, -108, "threshold 0.90", color=DIM, fontsize=7.5, ha="center")
        ax.text(0.50, 20, "LISTEN region", color=ACCENT, fontsize=8.5, ha="center")
        ax.text(0.965, 20, "open R", color=GREEN, fontsize=8.5, ha="center")
        ax.text(0.035, 20, "open L", color=RED, fontsize=8.5, ha="center")
        # trail: faded past positions + arrows showing each belief jump
        for j in range(i):
            ax.plot(bs[j], _env_val(bs[j]), "o", color=WHITE, ms=6, alpha=.35, zorder=3)
            ax.annotate("", xy=(bs[j + 1], _env_val(bs[j + 1])), xytext=(bs[j], _env_val(bs[j])),
                        arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=1.7, alpha=.7))
        # current belief marker, riding the envelope (its colour = the action on top)
        col = GREEN if acts[i] == "open" else ACCENT
        ax.plot(bs[i], _env_val(bs[i]), "o", color=col, ms=15, zorder=5, mec=WHITE, mew=1.5)
        ax.axvline(bs[i], color=col, ls=":", lw=1.2, alpha=.55)
        ax.text(bs[i], _env_val(bs[i]) + 13, f"b = {bs[i]:.2f}", color=col, fontsize=11,
                ha="center", weight="bold")
        ax.set_ylim(-114, 32); ax.set_xlim(0, 1)
        ax.set_xlabel("belief  b = P(tiger-left)"); ax.set_ylabel("value of acting now")
        ax.set_title(caps[i], color=WHITE, fontsize=10.5)
        for sp in ax.spines.values():
            sp.set_color(DIM)
        save(fig, f"tiger-walk-{i + 1}.png")


# ==========================================================================
# 9. POMDP -> belief MDP
# ==========================================================================
def fig_pomdp_belief_mdp():
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    box(ax, (1.6, 2.6), 2.4, 1.1, "hidden state s\n(unobserved)", ec=RED, tc=RED, fs=12)
    box(ax, (5, 2.6), 2.4, 1.1, "observation o\nP(o | s, a)", ec=ACCENT, fs=12)
    box(ax, (8.4, 2.6), 2.6, 1.1, "belief b(s)\n= P(s | history)", ec=YELLOW, tc=YELLOW, fs=12)
    arrow(ax, (2.8, 2.6), (3.8, 2.6)); arrow(ax, (6.2, 2.6), (7.1, 2.6))
    ax.text(5, 0.9, r"$b'(s') \;\propto\; P(o\mid s',a)\,\sum_s P(s'\mid s,a)\,b(s)$",
            ha="center", color=WHITE, fontsize=17)
    ax.text(5, 0.15, "belief is a sufficient statistic ⇒ a POMDP is an MDP over beliefs",
            ha="center", color=DIM, fontsize=12)
    save(fig, "pomdp-to-belief-mdp.png")


# ==========================================================================
# 10. legible vs efficient (Dragan reach)
# ==========================================================================
def fig_legible_vs_efficient():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))
    for ax, (ttl, legible) in zip(axes, [("efficient / 'doing'", False), ("legible / 'showing'", True)]):
        ax.set_xlim(-1.4, 1.4); ax.set_ylim(-0.2, 2.2); ax.axis("off")
        ax.set_title(ttl, color=(YELLOW if legible else ACCENT), fontsize=15)
        # two goals
        for gx, nm, col in [(-1.0, "G1", RED), (1.0, "G2 (true)", GREEN)]:
            ax.plot(gx, 2.0, "*", color=col, ms=22)
            ax.text(gx, 2.18, nm, ha="center", color=col, fontsize=11)
        ax.plot(0, 0, "o", color=WHITE, ms=11)
        ax.text(0, -0.18, "start", ha="center", color=WHITE, fontsize=10)
        t = np.linspace(0, 1, 60)
        if not legible:                       # straight up the ambiguous midline, veer at end
            x = 0.0 * t + (t**4) * 1.0
            y = 2.0 * t
        else:                                 # veer toward G2 early and conspicuously
            x = np.sin(t * np.pi / 2) * 1.0
            y = 2.0 * t
        ax.plot(x, y, "-", color=(YELLOW if legible else ACCENT), lw=3.5)
        ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-2], y[-2]),
                    arrowprops=dict(arrowstyle="-|>", color=(YELLOW if legible else ACCENT), lw=3))
    fig.suptitle("same goal, two plans: the legible one commits early so the goal is obvious",
                 color=WHITE, fontsize=13, y=1.02)
    save(fig, "legible-vs-efficient.png")


# ==========================================================================
# 11. showing vs doing gridworld + observer posterior (verified numbers)
# ==========================================================================
def fig_showing_vs_doing():
    goals = {"left": 6, "right": 8}
    start = 1
    doing, showing = [UP, UP, RIGHT], [RIGHT, UP, UP]
    fig = plt.figure(figsize=(11.5, 4.3))
    axd = fig.add_axes([0.02, 0.12, 0.30, 0.78])
    draw_grid(axd, {"G1": 6, "G2": 8}, start, doing, path_color=ACCENT, title="doing  ↑ ↑ →")
    axs = fig.add_axes([0.35, 0.12, 0.30, 0.78])
    draw_grid(axs, {"G1": 6, "G2": 8}, start, showing, path_color=YELLOW, title="showing  → ↑ ↑")
    axb = fig.add_axes([0.74, 0.20, 0.24, 0.66])
    steps = [1, 2, 3]
    pd = [goal_posterior(list(goals.values()), rollout(start, doing)[:k], doing[:k])[1] for k in steps]
    ps = [goal_posterior(list(goals.values()), rollout(start, showing)[:k], showing[:k])[1] for k in steps]
    axb.plot(steps, pd, "-o", color=ACCENT, lw=2.5, label="doing")
    axb.plot(steps, ps, "-o", color=YELLOW, lw=2.5, label="showing")
    axb.set_ylim(0.4, 1); axb.set_xticks(steps); axb.set_xlabel("step")
    axb.set_ylabel("observer P(true goal)")
    axb.set_title("legible commits early", color=WHITE, fontsize=12)
    axb.legend(facecolor="none", edgecolor=DIM, labelcolor=WHITE, fontsize=10)
    for sp in axb.spines.values():
        sp.set_color(DIM)
    save(fig, "showing-vs-doing-grid.png")


# ==========================================================================
# 12. reward recovery heatmaps
# ==========================================================================
def fig_reward_recovery():
    goal = 8
    Q = q_for_goal(goal)
    V = Q.max(1).reshape(NR, NC)
    ground = np.zeros((NR, NC)); ground[2, 2] = 1.0
    # "observed visitation": softmax-greedy rollouts toward goal -> occupancy proxy
    visit = (V - V.min()) / (V.max() - V.min())
    recovered = 0.5 * visit + 0.5 * ground       # schematic: sharpens toward ground truth
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
    for ax, M, ttl, cmap in zip(
            axes, [visit, recovered, ground],
            ["observed visits", "recovered reward", "true reward"],
            ["magma", "viridis", "viridis"]):
        im = ax.imshow(M, origin="lower", cmap=cmap, alpha=.92)
        ax.set_title(ttl, color=WHITE, fontsize=13)
        ax.set_xticks([]); ax.set_yticks([])
        for (j, i), v in np.ndenumerate(M):
            ax.text(i, j, f"{v:.1f}", ha="center", va="center", color=WHITE, fontsize=10)
    fig.suptitle("inverse RL: recover the reward from where the agent goes (more paths → sharper)",
                 color=DIM, fontsize=12, y=1.04)
    save(fig, "reward-recovery-heatmap.png")


# ==========================================================================
# 13. IRL methods timeline
# ==========================================================================
def fig_irl_timeline():
    fig, ax = plt.subplots(figsize=(11, 3.0))
    ax.set_xlim(0, 11); ax.set_ylim(0, 3); ax.axis("off")
    items = [("MaxEnt IRL\nZiebart '08", "soft-optimal\ndemonstrator", ACCENT),
             ("GAIL\nHo & Ermon '16", "adversarial\nimitation", TEAL),
             ("AIRL\nFu et al. '18", "transferable\nreward", GREEN),
             ("RLHF / DPO\n'22–'23", "reward from\npreferences", YELLOW)]
    xs = [1.4, 4.0, 6.6, 9.4]
    ax.plot([0.8, 10.2], [2.0, 2.0], color=DIM, lw=1.5, zorder=0)
    for x, (t, sub, col) in zip(xs, items):
        ax.plot(x, 2.0, "o", color=col, ms=13, zorder=2)
        ax.text(x, 2.5, t, ha="center", color=col, fontsize=12)
        ax.text(x, 1.2, sub, ha="center", color=DIM, fontsize=10.5)
    ax.text(5.5, 0.3, "all infer a hidden objective from behavior — and all are ill-posed",
            ha="center", color=WHITE, fontsize=12)
    save(fig, "irl-methods-timeline.png")


# ==========================================================================
# 14. amortized (ToMnet) vs Bayesian inversion
# ==========================================================================
def fig_amortized_vs_bayesian():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax = axes[0]
    ax.set_title("Bayesian inverse planning", color=ACCENT, fontsize=14)
    box(ax, (5, 3.1), 8.4, 0.9, "explicit planner, inverted by Bayes", ec=ACCENT, fs=11)
    box(ax, (2.2, 1.4), 3.0, 0.9, "behavior", ec=GREEN, tc=GREEN, fs=12)
    box(ax, (7.4, 1.4), 3.0, 0.9, "goal / belief", ec=YELLOW, tc=YELLOW, fs=11)
    arrow(ax, (3.7, 1.4), (5.9, 1.4), color=ACCENT)
    ax.text(5, 0.4, "interpretable, sample-efficient, hand-built model", ha="center", color=DIM, fontsize=10)
    ax = axes[1]
    ax.set_title("Machine ToM — ToMnet (2018)", color=PURPLE, fontsize=14)
    box(ax, (5, 3.1), 8.4, 0.9, "neural net trained on many agents", ec=PURPLE, tc=PURPLE, fs=11)
    box(ax, (2.2, 1.4), 3.0, 0.9, "behavior", ec=GREEN, tc=GREEN, fs=12)
    box(ax, (7.4, 1.4), 3.0, 0.9, "goal / belief", ec=YELLOW, tc=YELLOW, fs=11)
    arrow(ax, (3.7, 1.4), (5.9, 1.4), color=PURPLE)
    ax.text(5, 0.4, "learned / amortized, scalable, less interpretable", ha="center", color=DIM, fontsize=10)
    save(fig, "amortized-vs-bayesian-tom.png")


# ==========================================================================
# 15. LLM ToM debate
# ==========================================================================
def fig_llm_tom_debate():
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.axis("off")
    ax.text(2.6, 4.6, "capability claims", color=GREEN, fontsize=15, ha="center")
    ax.text(8.4, 4.6, "skeptical rebuttals", color=RED, fontsize=15, ha="center")
    pro = ["Kosinski '24 — GPT-4 ~75%\n(6-year-old level)",
           "Strachan '24 — at/above human\non false belief, irony, hinting",
           "Street '24 — adult-level\nhigher-order ToM"]
    con = ["Ullman '23 — trivial perturbations\nflip success to failure",
           "Strachan '24 — faux-pas:\nbias / over-conservatism, not inference",
           "Pang '25 — Morgan's Canon;\ntraining-data contamination"]
    for i, (p, c) in enumerate(zip(pro, con)):
        y = 3.7 - i * 1.05
        box(ax, (2.6, y), 4.4, 0.85, p, ec=GREEN, fs=10.5)
        box(ax, (8.4, y), 4.4, 0.85, c, ec=RED, fs=10.5)
        ax.annotate("", xy=(5.9, y), xytext=(5.1, y),
                    arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.5))
    box(ax, (5.5, 0.62), 8.6, 1.05,
        "behavioral pass ≠ mechanism —\ncurrent evidence does not show LLMs have human-like ToM",
        ec=YELLOW, tc=YELLOW, fs=11)
    save(fig, "llm-tom-debate.png")


if __name__ == "__main__":
    fig_agent_model()
    fig_recursive_teaching()
    fig_inverse_vs_forward()
    fig_bayes_inversion()
    fig_goal_inference_posterior()
    fig_ill_posed()
    fig_softmax_rationality()
    fig_tom_as_irl()
    fig_food_truck()
    fig_tiger_belief()
    fig_tiger_alpha()
    fig_tiger_walk()
    fig_pomdp_belief_mdp()
    fig_legible_vs_efficient()
    fig_showing_vs_doing()
    fig_reward_recovery()
    fig_irl_timeline()
    fig_amortized_vs_bayesian()
    fig_llm_tom_debate()
    print("\nVerify: goal posterior right =",
          round(float(goal_posterior([6, 7, 8], rollout(0, [RIGHT, RIGHT, UP, UP]), [RIGHT, RIGHT, UP, UP])[2]), 3),
          "| tiger beliefs =", [round(x, 4) for x in tiger_beliefs()])
