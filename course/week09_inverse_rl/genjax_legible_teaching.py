#!/usr/bin/env python3
"""Teaching = inverse planning, flipped — legible vs. efficient, in GenJAX (Wk 9).

If an observer infers your goal from your actions (Block 2), you can *choose*
actions that make your goal obvious — that's teaching. Two paths to the SAME
goal, both optimal-length, can differ in how fast they reveal the goal:

  • the "doing" path goes straight up the middle — ambiguous early (it fits both
    goals), only resolving at the last step;
  • the "showing"/legible path commits to the goal's side immediately — the
    observer's posterior on the true goal jumps right away.

We score each path by the **observer's goal-posterior it induces** — reusing the
exact inverse-planning machinery of `genjax_goal_inference.py` (Ho, Littman,
MacGlashan, Cushman & Austerweil 2016; Dragan, Lee & Srinivasa 2013). The legible
path wins. (Teaching as inverse planning; CIRL shows efficient demonstration is
provably suboptimal — Hadfield-Menell et al. 2016.)

Verified to run against genjax 0.10.3 + jax 0.5.3 (CPU).
Run:  python3 genjax_legible_teaching.py
"""
import jax.numpy as jnp
from genjax import gen, categorical, ChoiceMap

# ── a 3×3 grid with TWO goals (cleaner for the legibility contrast) ──────────
NROWS, NCOLS, NA = 3, 3, 4
NS = NROWS * NCOLS
START = 0 * NCOLS + 1                      # (0,1) bottom-middle
GOALS = {"left": 2 * NCOLS + 0, "right": 2 * NCOLS + 2}   # top-left / top-right
GOAL_NAMES = list(GOALS)
GOAL_STATES = jnp.array([GOALS[g] for g in GOAL_NAMES])
GAMMA, BETA = 0.9, 3.0
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def step(s, a):
    r, c = s // NCOLS, s % NCOLS
    r = jnp.clip(jnp.where(a == 0, r + 1, jnp.where(a == 1, r - 1, r)), 0, NROWS - 1)
    c = jnp.clip(jnp.where(a == 2, c - 1, jnp.where(a == 3, c + 1, c)), 0, NCOLS - 1)
    return r * NCOLS + c


TRANS = jnp.array([[int(step(s, a)) for a in range(NA)] for s in range(NS)])


def q_for_goal(goal_state):
    reward = (TRANS == goal_state).astype(jnp.float32)
    is_goal = (jnp.arange(NS) == goal_state)
    V = jnp.zeros(NS)
    for _ in range(50):
        V = jnp.where(is_goal, 0.0, jnp.max(reward + GAMMA * V[TRANS], axis=1))
    return reward + GAMMA * V[TRANS]


LOGITS = BETA * jnp.stack([q_for_goal(gs) for gs in GOAL_STATES])   # (2, NS, NA)
GOAL_PRIOR = jnp.ones(len(GOAL_NAMES)) / len(GOAL_NAMES)


def make_model(T):
    @gen
    def model(states):
        g = categorical(jnp.log(GOAL_PRIOR)) @ "goal"
        for t in range(T):
            categorical(LOGITS[g, states[t]]) @ f"a_{t}"
        return g
    return model


def posterior_on(true_goal_idx, states, actions):
    """Observer's posterior probability on the TRUE goal after these actions."""
    model = make_model(len(actions))
    states = jnp.asarray(states)
    logp = []
    for g in range(len(GOAL_NAMES)):
        cm = ChoiceMap.d({"goal": g, **{f"a_{t}": int(actions[t]) for t in range(len(actions))}})
        score, _ = model.assess(cm, (states,))
        logp.append(score)
    logp = jnp.array(logp)
    post = jnp.exp(logp - (jnp.max(logp) + jnp.log(jnp.sum(jnp.exp(logp - jnp.max(logp))))))
    return float(post[true_goal_idx])


def states_of(actions):
    s, out = START, []
    for a in actions:
        out.append(int(s)); s = int(step(jnp.array(s), jnp.array(a)))
    return out


if __name__ == "__main__":
    true_goal = GOAL_NAMES.index("right")
    # both paths reach top-right (2,2) from (0,1) in 3 optimal steps:
    doing = [UP, UP, RIGHT]      # straight up the middle, then over — ambiguous early
    showing = [RIGHT, UP, UP]    # commit to the right column immediately — legible

    print("Observer's posterior on the TRUE goal (top-right), after each step:")
    print("  step      doing(efficient)   showing(legible)")
    for k in range(1, 4):
        pd = posterior_on(true_goal, states_of(doing)[:k], doing[:k])
        ps = posterior_on(true_goal, states_of(showing)[:k], showing[:k])
        print(f"   {k}            {pd:.3f}              {ps:.3f}")

    print("\nBoth paths are optimal-length (3 steps) — but the legible path makes")
    print("the goal obvious immediately, while the efficient path stays ambiguous")
    print("until the final move. Teaching = choosing the legible plan.")
