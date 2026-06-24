#!/usr/bin/env python3
"""Goal inference as inverse planning, in GenJAX — Week 9's core backbone.

Week 8 ran an MDP *forward*: a goal becomes a softmax policy becomes actions.
This script runs the SAME machinery *backward*: we watch a few actions and
infer *which goal* the agent was heading for —

    P(goal | actions) ∝ P(actions | goal) · P(goal),

where the likelihood P(actions | goal) is exactly the Week-8 softmax policy
(value iteration → Q → Boltzmann), evaluated on the observed actions. The goal
is the hidden state we condition on data to recover: the literal "which MDP are
we in?" inference (Baker, Tenenbaum & Saxe 2007; Baker, Saxe & Tenenbaum 2009).

Three things, mirroring genjax_chibany_mdp.py:
  (1) the FORWARD planner: tabular value iteration on a tiny gridworld, one per
      candidate goal, giving a softmax policy π_g(a|s) ∝ exp(β · Q_g(s,a));
  (2) the GENERATIVE MODEL of an observer: sample a goal from the prior, then
      sample the observed actions from that goal's policy (a GenJAX @gen);
  (3) INVERSION: the exact posterior over goals by enumerating the (few) goals
      with `model.assess`, plus the running "freeze-frame" posterior after each
      step (the Baker online-inference curve that drives the widget + figure).

Verified to run against genjax 0.10.3 + jax 0.5.3 (CPU).
Run:  python3 genjax_goal_inference.py
"""
import jax.numpy as jnp
from jax import random
from genjax import gen, categorical, ChoiceMap

# ── a tiny gridworld ────────────────────────────────────────────────────────
# 3×3 grid. state s = r*3 + c, with r=0 the bottom row, c=0 the left column.
# Actions: 0=UP (r+1), 1=DOWN (r-1), 2=LEFT (c-1), 3=RIGHT (c+1). Moves that
# would leave the grid are no-ops (clamp). The agent starts bottom-middle.
NROWS, NCOLS, NA = 3, 3, 4
NS = NROWS * NCOLS
START = 0 * NCOLS + 0                      # (0,0) bottom-left = state 0
GOALS = {"left": 2 * NCOLS + 0,            # (2,0) top-left  = state 6
         "mid":  2 * NCOLS + 1,            # (2,1) top-mid   = state 7
         "right": 2 * NCOLS + 2}           # (2,2) top-right = state 8
GOAL_NAMES = list(GOALS)
GOAL_STATES = jnp.array([GOALS[g] for g in GOAL_NAMES])
GAMMA = 0.9
BETA = 3.0                                 # softmax temperature (rationality)


def step(s, a):
    """Deterministic gridworld transition with boundary clamping."""
    r, c = s // NCOLS, s % NCOLS
    r = jnp.clip(jnp.where(a == 0, r + 1, jnp.where(a == 1, r - 1, r)), 0, NROWS - 1)
    c = jnp.clip(jnp.where(a == 2, c - 1, jnp.where(a == 3, c + 1, c)), 0, NCOLS - 1)
    return r * NCOLS + c


# transition table T[s, a] -> s'  (precomputed; the dynamics are shared by all goals)
TRANS = jnp.array([[int(step(s, a)) for a in range(NA)] for s in range(NS)])


def q_values_for_goal(goal_state):
    """Tabular value iteration on the deterministic grid for one goal.

    Reward = +1 on *entering* the goal cell (then absorbing, 0 after). This is
    the Week-8 forward solver — here we run it once per candidate goal."""
    reward = (TRANS == goal_state).astype(jnp.float32)        # r(s,a) = 1 if s'==goal
    is_goal = (jnp.arange(NS) == goal_state)
    V = jnp.zeros(NS)
    for _ in range(50):                                        # plenty for a 3×3 grid
        Q = reward + GAMMA * V[TRANS]                          # Q[s,a] = r + γ V(s')
        V = jnp.where(is_goal, 0.0, jnp.max(Q, axis=1))        # goal absorbing, V=0
    Q = reward + GAMMA * V[TRANS]
    return Q                                                   # (NS, NA)


# policy logits for every goal: LOGITS[g, s, a] = β · Q_g(s, a) (softmax → policy)
LOGITS = BETA * jnp.stack([q_values_for_goal(gs) for gs in GOAL_STATES])  # (G, NS, NA)
GOAL_PRIOR = jnp.ones(len(GOAL_NAMES)) / len(GOAL_NAMES)       # uniform over goals


# ── (2) the observer's GENERATIVE MODEL (a GenJAX @gen) ─────────────────────
# A goal is drawn from the prior; each observed action is drawn from that goal's
# softmax policy at the visited state. `states` is the (static-length) list of
# states at which actions were taken; actions live at addresses "a_0","a_1",...
def make_model(T):
    @gen
    def model(states):
        g = categorical(jnp.log(GOAL_PRIOR)) @ "goal"
        for t in range(T):
            categorical(LOGITS[g, states[t]]) @ f"a_{t}"
        return g
    return model


# ── (3) INVERSION: exact posterior over goals by enumeration (`assess`) ─────
def goal_posterior(states, actions):
    """Exact P(goal | actions) by enumerating the few goals.

    For each goal we score the fully-constrained trace {goal, a_0..a_{T-1}} with
    `model.assess`, which returns log P(goal, actions). Normalizing over goals
    gives the posterior — Bayes' rule, done by enumeration."""
    T = len(actions)
    model = make_model(T)
    states = jnp.asarray(states)
    logp = []
    for g in range(len(GOAL_NAMES)):
        cm = ChoiceMap.d({"goal": g, **{f"a_{t}": int(actions[t]) for t in range(T)}})
        score, _ = model.assess(cm, (states,))
        logp.append(score)
    logp = jnp.array(logp)
    return jnp.exp(logp - jax_logsumexp(logp))                # normalized posterior


def jax_logsumexp(x):
    m = jnp.max(x)
    return m + jnp.log(jnp.sum(jnp.exp(x - m)))


def rollout_states(start, actions):
    """The states visited *before* each action (so actions[t] is taken at s[t])."""
    s, states = start, []
    for a in actions:
        states.append(int(s))
        s = int(step(jnp.array(s), jnp.array(a)))
    return states


if __name__ == "__main__":
    # An observed trajectory that commits right — a *detour* away from the two
    # left-hand goals, which is exactly what makes it diagnostic of "right":
    # RIGHT, RIGHT, UP, UP  →  (0,0)→(0,1)→(0,2)→(1,2)→(2,2)=top-right goal.
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    actions = [RIGHT, RIGHT, UP, UP]
    states = rollout_states(START, actions)
    print("start = state", START, " observed states:", states,
          " actions:", ["UP DOWN LEFT RIGHT".split()[a] for a in actions])

    # Full posterior after the whole trajectory:
    post = goal_posterior(states, actions)
    print("\nposterior over goals after the full path:")
    for name, p in zip(GOAL_NAMES, post):
        print(f"  P({name:5s}) = {float(p):.3f}")

    # The Baker "freeze-frame" curve: posterior after each successive action.
    print("\nfreeze-frame posterior (after 1, 2, 3 actions):")
    print("  step  " + "  ".join(f"{n:>6s}" for n in GOAL_NAMES))
    for k in range(1, len(actions) + 1):
        pk = goal_posterior(states[:k], actions[:k])
        print(f"  {k:>3d}   " + "  ".join(f"{float(x):.3f}" for x in pk))

    # Rationality matters: a near-random agent (β→0) is barely informative.
    import sys
    BETA_SAVE = BETA
    for b in (0.1, 2.0, 6.0):
        BETA = b
        LOGITS = BETA * jnp.stack([q_values_for_goal(gs) for gs in GOAL_STATES])
        # rebind the globals the model closes over
        globals()["LOGITS"] = LOGITS
        pk = goal_posterior(states, actions)
        print(f"\nβ={b:>4}:  " + "  ".join(f"P({n})={float(x):.3f}" for n, x in zip(GOAL_NAMES, pk)))
    BETA = BETA_SAVE
