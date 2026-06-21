"""GardenPath gridworld — shared env + visualization for the RL assignment.

Single source of truth for the Spring-2026 Reinforcement-Learning assignment.
It is imported by both the GenJAX and the plain-Python stencils so the world,
the reward schemes, and the pictures are defined in exactly one place.

The conventions match the textbook Q-learning widget
(``qlearning-gridworld.html``) so the figures you make here look like the
interactive tool you played with in Chapter 22:

    * state ``s = (row, col)``, 1-indexed, **row 1 = bottom**, col 1 = left
    * actions ``'U' 'D' 'L' 'R'``
    * start = (1, 1) bottom-left,  goal = (3, 3) top-right (terminal)
    * garden = the bottom-right 2x2 block {(1,2),(1,3),(2,2),(2,3)}

Three layers:

    1. the ENV          -- states, moves, and the RM / AF / shaped rewards
    2. plot_gridworld() -- a STATIC picture (Q-wedges, greedy arrows, the
                           rollout route, a verdict title) for your report
    3. interactive_gridworld() -- the in-notebook explorer (sliders + Step /
                           Run / Train buttons + a live equation) driven by
                           *your own* Q-learning update.  Needs ipywidgets;
                           runs live in Jupyter/Colab but does NOT render in a
                           static PDF export, so use plot_gridworld() for the
                           figures you hand in.

Pure Python + numpy + matplotlib; no JAX is required to import this module.
"""

from __future__ import annotations

import math
import random as _random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# ─────────────────────────────────────────────────────────────────────────────
#  THE WORLD  (constants ported verbatim from the Chapter-22 widget)
# ─────────────────────────────────────────────────────────────────────────────
START = (1, 1)
GOAL = (3, 3)
GARDEN = {(1, 2), (1, 3), (2, 2), (2, 3)}
ACTIONS = ("U", "D", "L", "R")
_DR = {"U": 1, "D": -1, "L": 0, "R": 0}
_DC = {"U": 0, "D": 0, "L": -1, "R": 1}

POS, NEG, NO, GFB, WEAK = 10, -10, 0, 20, 4   # reward magnitudes
MAXSTEP = 30                                   # episode step cap -> "cycling"

# reward tables keyed (row, col) then action.  Only the moves that exist from a
# cell are listed (the goal cell (3,3) is terminal and has no outgoing rewards).
#
# RM ("reward-maximizing"): outcome-based.  Stepping toward the goal along the
# path is neutral (0); stepping into the garden is punished; reaching the goal
# pays GFB.  This is the reward you'd write if you cared only about the outcome.
RM = {
    (1, 1): {"U": NO, "R": NEG},
    (2, 1): {"U": NO, "R": NEG, "D": NO},
    (3, 1): {"R": NO, "D": NO},
    (1, 2): {"R": NEG, "U": NEG, "L": NO},
    (2, 2): {"R": NEG, "U": NO, "L": NO, "D": NEG},
    (3, 2): {"R": GFB, "L": NO, "D": NEG},
    (1, 3): {"U": NEG, "L": NEG},
    (2, 3): {"U": GFB, "D": NEG, "L": NEG},
}
# AF ("action-feedback"): how a *person* tends to teach.  Forward progress along
# the path earns praise (POS); backtracking along the path earns only faint
# praise (WEAK) instead of punishment -- a human positive-feedback bias.  Both
# directions are positive, so the path becomes a farmable reward cycle.
AF = {
    (1, 1): {"U": POS, "R": NEG},
    (2, 1): {"U": POS, "R": NEG, "D": WEAK},
    (3, 1): {"R": POS, "D": WEAK},
    (1, 2): {"R": NEG, "U": NEG, "L": POS},
    (2, 2): {"R": NEG, "U": POS, "L": NEG, "D": NEG},
    (3, 2): {"R": GFB, "L": WEAK, "D": NEG},
    (1, 3): {"U": POS, "L": NEG},
    (2, 3): {"U": POS, "D": NEG, "L": NEG},
}


# ─────────────────────────────────────────────────────────────────────────────
#  ENV HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def states():
    """All nine cells (row, col), row & col in 1..3."""
    return [(r, c) for r in range(1, 4) for c in range(1, 4)]


def is_goal(s):
    return tuple(s) == GOAL


def is_garden(s):
    return tuple(s) in GARDEN


def manhattan_to_goal(s):
    """Manhattan distance from s to the goal (used by the default potential)."""
    return abs(GOAL[0] - s[0]) + abs(GOAL[1] - s[1])


def valid_actions(s):
    """The moves that stay on the 3x3 board from state s."""
    r, c = s
    out = []
    if r < 3:
        out.append("U")
    if r > 1:
        out.append("D")
    if c > 1:
        out.append("L")
    if c < 3:
        out.append("R")
    return out


def step(s, a):
    """Deterministic next state from taking action a in state s."""
    return (s[0] + _DR[a], s[1] + _DC[a])


# ─────────────────────────────────────────────────────────────────────────────
#  REWARD SCHEMES  (each returns a callable  reward_fn(s, a) -> float)
# ─────────────────────────────────────────────────────────────────────────────
def reward_rm():
    """Reward-maximizing (outcome-based) feedback."""
    return lambda s, a: float(RM[tuple(s)][a])


def reward_af():
    """Action-feedback (human-style) feedback -- contains the positive cycle."""
    return lambda s, a: float(AF[tuple(s)][a])


def phi_distance(s):
    """Default potential Phi(s) = -(distance to goal): higher closer to home."""
    return float(-manhattan_to_goal(s))


def reward_shaped(base_reward, phi, gamma):
    """Potential-based shaping of an existing reward (Ng, Harada & Russell 1999).

        r'(s, a) = base(s, a) + gamma * Phi(s') - Phi(s)

    The extra term telescopes over any trajectory, so it changes how fast an
    agent learns (and can break a reward cycle) WITHOUT changing which policy
    is optimal.  `base_reward` is a reward_fn(s, a); `phi` is a function of a
    single state.
    """
    def r(s, a):
        s2 = step(s, a)
        return float(base_reward(s, a) + gamma * phi(s2) - phi(s))
    return r


# ─────────────────────────────────────────────────────────────────────────────
#  Q-TABLE  (dict of dicts:  Q[state][action], only over valid actions)
# ─────────────────────────────────────────────────────────────────────────────
def fresh_Q():
    """A zeroed Q-table over every (state, valid-action) pair."""
    return {s: {a: 0.0 for a in valid_actions(s)} for s in states()}


def q_max(Q, s):
    """max_a Q(s, a) over valid actions; 0 at the terminal goal."""
    if is_goal(s):
        return 0.0
    return max(Q[tuple(s)][a] for a in valid_actions(s))


def greedy_action(Q, s, rng=None):
    """Best valid action in s, ties broken at random."""
    A = valid_actions(s)
    best = max(Q[tuple(s)][a] for a in A)
    ties = [a for a in A if Q[tuple(s)][a] == best]
    pick = (rng or _random).choice(ties)
    return pick


def eps_greedy(Q, s, eps, rng=None):
    """Epsilon-greedy action selection."""
    rng = rng or _random
    A = valid_actions(s)
    if rng.random() < eps:
        return rng.choice(A)
    return greedy_action(Q, s, rng)


# The reference TD update.  In the *stencil* the student writes the one
# `pred_error = ...` line; this is the filled-in version the solution / the
# interactive explorer fall back on when no student update is supplied.
def reference_td_update(Q, s, a, r, s_next, alpha, gamma):
    pred_error = r + gamma * q_max(Q, s_next) - Q[tuple(s)][a]
    Q[tuple(s)][a] += alpha * pred_error
    return pred_error


# ─────────────────────────────────────────────────────────────────────────────
#  TRAINING
# ─────────────────────────────────────────────────────────────────────────────
def train(Q, reward_fn, n_steps=2000, alpha=0.9, gamma=0.95, eps=0.1,
          td_update=reference_td_update, seed=0, step_fn=step):
    """Run n_steps of Q-learning in place.  Episodes restart at START and end at
    the goal or after MAXSTEP steps.  `td_update(Q, s, a, r, s2, alpha, gamma)`
    is *your* learning rule -- pass your own to watch your code train.

    `step_fn(s, a) -> s'` supplies the next state.  It defaults to the built-in
    deterministic move; the GenJAX stencil passes a model-backed step that draws
    s' from a `@gen` transition, so Q-learning learns *by sampling the world*.
    """
    rng = _random.Random(seed)
    s = START
    t = 0
    for _ in range(n_steps):
        a = eps_greedy(Q, s, eps, rng)
        s2 = step_fn(s, a)
        r = reward_fn(s, a)
        td_update(Q, s, a, r, s2, alpha, gamma)
        t += 1
        if is_goal(s2) or t >= MAXSTEP:
            s, t = START, 0
        else:
            s = s2
    return Q


# ─────────────────────────────────────────────────────────────────────────────
#  GREEDY ROLLOUT + VERDICT  (does the *learned* policy reach the goal or loop?)
# ─────────────────────────────────────────────────────────────────────────────
def greedy_rollout(Q, reward_fn=None, gamma=0.95, max_len=40):
    """Follow the greedy policy from START.  Returns a dict with:

        path     -- list of visited states
        reached  -- True if it lands on the goal
        cycles   -- True if it revisits a state (a loop) before reaching goal
        net_lap  -- summed reward around that loop (the AF "+N/lap" number),
                    or None if reward_fn is None / no loop
    """
    # deterministic greedy (no random tie-break) so the verdict is stable
    def greedy_det(s):
        A = valid_actions(s)
        best = max(Q[tuple(s)][a] for a in A)
        return next(a for a in A if Q[tuple(s)][a] == best)

    p = START
    path = [p]
    seen = {p: 0}
    cyc = False
    net = None
    for _ in range(max_len):
        if is_goal(p):
            break
        a = greedy_det(p)
        np_ = step(p, a)
        path.append(np_)
        if np_ in seen:                      # the loop closes
            cyc = True
            if reward_fn is not None:
                j = seen[np_]
                net = sum(reward_fn(path[t], greedy_det(path[t]))
                          for t in range(j, len(path) - 1))
            break
        seen[np_] = len(path) - 1
        p = np_
    return {"path": path, "reached": is_goal(path[-1]), "cycles": cyc, "net_lap": net}


def verdict(Q, reward_fn=None, gamma=0.95):
    """A one-line headline about what the learned greedy policy does."""
    if all(abs(v) < 1e-9 for s in Q for v in Q[s].values()):
        return "untrained — train first", "untrained"
    tr = greedy_rollout(Q, reward_fn, gamma)
    if tr["reached"]:
        return "✓ the learned policy REACHES THE GOAL", "reaches"
    if tr["cycles"]:
        if tr["net_lap"] is not None and tr["net_lap"] > 0:
            return (f"✗ the learned policy LOOPS — a +{tr['net_lap']:.0f}/lap "
                    f"reward cycle, never reaching the goal"), "loops"
        return "✗ the learned policy LOOPS — never reaches the goal", "loops"
    return "• the learned policy hasn't settled yet", "unsettled"


# ─────────────────────────────────────────────────────────────────────────────
#  EXACT SOLUTION  (Q-value iteration on the known deterministic model)
#  Used by the GenJAX bonus: the model-based optimum the learner should match.
# ─────────────────────────────────────────────────────────────────────────────
def q_value_iteration(reward_fn, gamma=0.95, sweeps=200):
    """Exact optimal Q* by Bellman backups on the deterministic env.

        Q*(s, a) = r(s, a) + gamma * (0 if s' terminal else max_a' Q*(s', a'))
    """
    Q = fresh_Q()
    for _ in range(sweeps):
        newQ = fresh_Q()
        for s in states():
            if is_goal(s):
                continue
            for a in valid_actions(s):
                s2 = step(s, a)
                future = 0.0 if is_goal(s2) else max(Q[s2][b] for b in valid_actions(s2))
                newQ[s][a] = reward_fn(s, a) + gamma * future
        Q = newQ
    return Q


def greedy_policy(Q):
    """The greedy action in every non-terminal cell, as a dict {state: action}."""
    return {s: greedy_action(Q, s) for s in states() if not is_goal(s)}


# ─────────────────────────────────────────────────────────────────────────────
#  STATIC RENDERER  (the picture that goes in your report)
# ─────────────────────────────────────────────────────────────────────────────
_COL = {
    "bg": "#111111", "panel": "#181820", "dim": "#999999", "white": "#ffffff",
    "accent": "#64B5F6", "red": "#EF5350", "green": "#66BB6A", "yellow": "#FFEB3B",
    "garden": "#241015", "path": "#10241a", "goal": "#2a2410",
}


def _wedge_xy(r, c, a):
    """Triangle vertices (center -> the two corners of the cell edge for a)."""
    cx, cy = c, r
    h = 0.5
    if a == "U":
        return [(cx, cy), (cx - h, cy + h), (cx + h, cy + h)]
    if a == "D":
        return [(cx, cy), (cx - h, cy - h), (cx + h, cy - h)]
    if a == "L":
        return [(cx, cy), (cx - h, cy - h), (cx - h, cy + h)]
    return [(cx, cy), (cx + h, cy - h), (cx + h, cy + h)]   # R


def plot_gridworld(Q, reward_fn=None, gamma=0.95, ax=None, title=None,
                   show_policy=True, show_route=True):
    """Draw the gridworld with Q-value wedges, the greedy policy, and the route
    the greedy policy takes from the start.  Mirrors the Chapter-22 widget.

        * wedges   -- one per action, green (>=0) / red (<0), opacity ~ |Q|
        * arrows   -- the greedy action in each cell (white)
        * route    -- the greedy path from start: green reaches home, red loops
        * title    -- the verdict (or a title you pass)

    Returns the matplotlib Axes.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(5.2, 5.4))
    ax.set_facecolor(_COL["bg"])
    if ax.figure is not None:
        ax.figure.set_facecolor(_COL["bg"])

    # cells + wedges
    for s in states():
        r, c = s
        face = _COL["garden"] if is_garden(s) else _COL["path"]
        if is_goal(s):
            face = _COL["goal"]
        ax.add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor=face,
                               edgecolor="#2f3a36", lw=1.5, zorder=1))
        if is_goal(s):
            continue
        for a in valid_actions(s):
            v = Q[s][a]
            mag = min(1.0, abs(v) / 18.0)
            color = _COL["green"] if v > 1e-3 else (_COL["red"] if v < -1e-3 else "#444444")
            ax.add_patch(Polygon(_wedge_xy(r, c, a), closed=True, facecolor=color,
                                 edgecolor="none", alpha=0.18 + 0.62 * mag, zorder=2))
            if abs(v) >= 0.5:
                tx, ty = c, r
                if a == "U":
                    ty = r + 0.31
                elif a == "D":
                    ty = r - 0.31
                elif a == "L":
                    tx = c - 0.31
                else:
                    tx = c + 0.31
                ax.text(tx, ty, f"{v:.0f}", color=_COL["white"], fontsize=8,
                        ha="center", va="center", zorder=4)
        if is_garden(s):
            ax.text(c - 0.45, r + 0.4, "garden", color=_COL["red"], fontsize=7.5,
                    ha="left", va="center", alpha=0.7, zorder=3)

    trained = any(abs(v) > 1e-9 for s in Q for v in Q[s].values())

    # greedy policy arrows
    if show_policy and trained:
        for s in states():
            if is_goal(s):
                continue
            a = greedy_action(Q, s)
            dx, dy = _DC[a] * 0.34, _DR[a] * 0.34
            ax.annotate("", xy=(s[1] + dx, s[0] + dy),
                        xytext=(s[1] - dx * 0.4, s[0] - dy * 0.4),
                        arrowprops=dict(arrowstyle="-|>", color=_COL["white"], lw=2.0),
                        zorder=5)

    # greedy rollout route
    if show_route and trained:
        tr = greedy_rollout(Q, reward_fn, gamma)
        col = _COL["green"] if tr["reached"] else _COL["red"]
        xs = [p[1] for p in tr["path"]]
        ys = [p[0] for p in tr["path"]]
        ax.plot(xs, ys, color=col, lw=4.0, alpha=0.55, solid_capstyle="round", zorder=6)

    # glyphs (plain markers — emoji are not in matplotlib's default font)
    ax.plot(GOAL[1], GOAL[0], marker="*", markersize=24, color=_COL["yellow"],
            markeredgecolor="#806000", zorder=7)
    ax.text(GOAL[1], GOAL[0] - 0.36, "GOAL", color=_COL["yellow"], fontsize=8,
            fontweight="bold", ha="center", va="center", zorder=7)
    ax.plot(START[1], START[0], marker="o", markersize=12, color=_COL["accent"],
            markeredgecolor="#06121f", zorder=7)
    ax.text(START[1] - 0.4, START[0] - 0.4, "start", color=_COL["dim"], fontsize=7.5,
            ha="left", va="center", zorder=7)

    if title is None:
        title = verdict(Q, reward_fn, gamma)[0]
    ax.set_title(title, color=_COL["white"], fontsize=11, pad=10)

    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax


# ─────────────────────────────────────────────────────────────────────────────
#  INTERACTIVE EXPLORER  (ipywidgets; lazy-imported so this module imports w/o it)
# ─────────────────────────────────────────────────────────────────────────────
_STEPPER = [
    "1  select action a (ε-greedy)",
    "2  take a → observe reward r, next state s′",
    "3  look up best next value  max Q(s′,·)",
    "4  form target = r + γ·max",
    "5  TD error = target − Q(s,a)",
    "6  update Q(s,a) ← Q(s,a) + α·error",
]


def interactive_gridworld(td_update=reference_td_update, scheme="rm",
                          alpha=0.9, gamma=0.95, eps=0.1, phi=phi_distance):
    """In-notebook explorer that mirrors the Chapter-22 widget, but steps using
    *your* `td_update`.  Sliders for alpha / gamma / epsilon, a feedback-scheme
    dropdown (rm / af / shaped), Step / Run / Train / Reset buttons, a 6-step
    stepper, and a live equation readout.

    Requires ipywidgets (preinstalled on Colab).  Interactivity is live in a
    running notebook only -- it does not appear in a static PDF export, so use
    plot_gridworld() for the figures you submit.
    """
    try:
        import ipywidgets as W
        from IPython.display import display, clear_output
    except ImportError as e:                      # pragma: no cover
        raise ImportError(
            "interactive_gridworld() needs ipywidgets + IPython (preinstalled on "
            "Colab).  For static figures use plot_gridworld() instead."
        ) from e

    def reward_for(name):
        if name == "rm":
            return reward_rm()
        if name == "af":
            return reward_af()
        # "shaped" = the TRUE outcome reward (RM) made dense the principled way:
        # potential-based shaping.  This is dense feedback done RIGHT (cf. AF).
        return reward_shaped(reward_rm(), phi, st["gamma"])

    st = {"Q": fresh_Q(), "s": START, "t": 0, "phase": 0, "cur": {},
          "alpha": alpha, "gamma": gamma, "eps": eps, "scheme": scheme}
    rng = _random.Random(0)

    a_sl = W.FloatSlider(value=alpha, min=0.05, max=1.0, step=0.05, description="α")
    g_sl = W.FloatSlider(value=gamma, min=0.5, max=0.99, step=0.01, description="γ")
    e_sl = W.FloatSlider(value=eps, min=0.0, max=0.5, step=0.01, description="ε")
    sch = W.Dropdown(options=[("reward-maximizing", "rm"), ("action-feedback", "af"),
                              ("shaped (your Φ)", "shaped")], value=scheme,
                     description="feedback")
    b_step = W.Button(description="Step ▸", button_style="primary")
    b_run = W.Button(description="▶ Run")
    b_train = W.Button(description="Train ▸▸ 2000")
    b_reset = W.Button(description="⟲ Reset")
    stepper = W.HTML()
    eqn = W.HTML()
    canvas = W.Output()

    def render():
        with canvas:
            clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(4.8, 5.0))
            plot_gridworld(st["Q"], reward_for(st["scheme"]), st["gamma"], ax=ax)
            plt.show()
        rows = []
        for i, label in enumerate(_STEPPER):
            on = (i == st["phase"])
            color = "#64B5F6" if on else "#888888"
            weight = "700" if on else "400"
            rows.append(f"<div style='color:{color};font-weight:{weight};"
                        f"font-size:13px;padding:2px 0'>{label}</div>")
        stepper.value = "".join(rows)
        c = st["cur"]
        eqn.value = (
            "<div style='font-family:monospace;font-size:13px;color:#ccc'>"
            f"Q({c.get('s','s')},{c.get('a','a')}) ← {_f(c.get('qold'))} + "
            f"{st['alpha']:.2f}·( {_f(c.get('r'))} + {st['gamma']:.2f}·"
            f"{_f(c.get('maxq'))} − {_f(c.get('qold'))} ) = "
            f"<b style='color:#FFEB3B'>{_f(c.get('qnew'))}</b></div>"
        )

    def _f(x):
        return "·" if x is None else f"{x:.2f}"

    def advance():
        Q, s = st["Q"], st["s"]
        ph = st["phase"]
        rf = reward_for(st["scheme"])
        c = st["cur"]
        if ph == 0:
            a = eps_greedy(Q, s, st["eps"], rng)
            st["cur"] = {"s": s, "a": a, "qold": Q[s][a]}
            st["phase"] = 1
        elif ph == 1:
            c["s2"] = step(c["s"], c["a"])
            c["r"] = rf(c["s"], c["a"])
            st["phase"] = 2
        elif ph == 2:
            c["maxq"] = q_max(Q, c["s2"])
            st["phase"] = 3
        elif ph == 3:
            c["target"] = c["r"] + st["gamma"] * c["maxq"]
            st["phase"] = 4
        elif ph == 4:
            c["err"] = c["target"] - c["qold"]
            st["phase"] = 5
        else:
            # commit using the STUDENT's update, then read back the new value
            td_update(Q, c["s"], c["a"], c["r"], c["s2"], st["alpha"], st["gamma"])
            c["qnew"] = Q[c["s"]][c["a"]]
            st["t"] += 1
            st["s"] = START if (is_goal(c["s2"]) or st["t"] >= MAXSTEP) else c["s2"]
            if is_goal(c["s2"]) or st["t"] >= MAXSTEP:
                st["t"] = 0
            st["phase"] = 0
        render()

    def on_train(_):
        train(st["Q"], reward_for(st["scheme"]), 2000, st["alpha"], st["gamma"],
              st["eps"], td_update, seed=rng.randint(0, 10**6))
        st["phase"] = 0
        st["cur"] = {}
        render()

    def on_reset(_):
        st["Q"] = fresh_Q()
        st["s"], st["t"], st["phase"], st["cur"] = START, 0, 0, {}
        render()

    def on_run(_):
        for _ in range(60):                # a short burst of single steps
            advance()

    def sync(_):
        st["alpha"], st["gamma"], st["eps"] = a_sl.value, g_sl.value, e_sl.value
        st["scheme"] = sch.value

    for w in (a_sl, g_sl, e_sl, sch):
        w.observe(sync, names="value")
    b_step.on_click(lambda _: advance())
    b_run.on_click(on_run)
    b_train.on_click(on_train)
    b_reset.on_click(on_reset)

    controls = W.HBox([b_step, b_run, b_train, b_reset])
    sliders = W.HBox([a_sl, g_sl, e_sl, sch])
    right = W.VBox([W.HTML("<b>Q-learning — one step at a time</b>"), stepper, eqn])
    render()
    display(W.VBox([sliders, controls, W.HBox([canvas, right])]))


# ─────────────────────────────────────────────────────────────────────────────
#  GenJAX HOOK  (optional; only used by the GenJAX stencil)
# ─────────────────────────────────────────────────────────────────────────────
def transition_tensor():
    """Build the (A, S, S') one-hot transition tensor and the index <-> state
    maps for the GenJAX `@gen transition` model and value iteration.

    Deterministic moves; an invalid action self-loops (it is masked out of the
    greedy max anyway).  Returns (T, idx, inv) where T has shape (4, 9, 9),
    idx maps a state tuple -> flat index, and inv is the inverse list.
    """
    S = states()
    idx = {s: i for i, s in enumerate(S)}
    inv = list(S)
    n = len(S)
    T = np.zeros((len(ACTIONS), n, n), dtype=np.float32)
    for ai, a in enumerate(ACTIONS):
        for s in S:
            s2 = step(s, a) if a in valid_actions(s) else s
            T[ai, idx[s], idx[s2]] = 1.0
    return T, idx, inv
