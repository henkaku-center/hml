#!/usr/bin/env python3
"""The Tiger POMDP belief update, in GenJAX — Week 9's belief-inference backbone.

In Block 2 the hidden thing was the agent's *goal*. Here it's the hidden *world
state*: a tiger behind one of two doors. We never see it — we only *listen*, and
the growl is right only 85% of the time. The agent (and the observer) maintains a
**belief** b(s) = P(state), updated by Bayes after each observation:

    b'(s) ∝ P(observation | s) · b(s).

This is the same conditioning move as goal inference, now over world state — and
it's the forward model an observer *inverts* to read another mind's beliefs
(Bayesian Theory of Mind; Baker, Jara-Ettinger, Saxe & Tenenbaum 2017). Tiger:
Kaelbling, Littman & Cassandra (1998).

  (1) the GENERATIVE MODEL: sample a state from the current belief, then a growl
      from the 0.85-accurate observation model (a GenJAX @gen);
  (2) the BELIEF UPDATE: the exact posterior over states given the growl, by
      enumeration with `model.assess` — Bayes' rule;
  (3) the DECISION: the immediate expected value of opening a door, which shows
      *why one growl isn't enough and two are* (the Poll-2 reveal).

Verified to run against genjax 0.10.3 + jax 0.5.3 (CPU).
Run:  python3 genjax_tiger_pomdp.py
"""
import jax.numpy as jnp
from genjax import gen, categorical, ChoiceMap

# ── the Tiger POMDP ─────────────────────────────────────────────────────────
# states:       0 = tiger-LEFT,  1 = tiger-RIGHT
# observations: 0 = hear-LEFT,   1 = hear-RIGHT
# listening is 85% accurate: P(hear-left | tiger-left) = 0.85
ACC = 0.85
OBS = jnp.array([[ACC, 1 - ACC],          # tiger-left  -> hear-left .85 / hear-right .15
                 [1 - ACC, ACC]])          # tiger-right -> hear-left .15 / hear-right .85
# rewards (canonical KLC 1998): listen -1, open correct +10, open tiger -100
R_LISTEN, R_CORRECT, R_TIGER = -1.0, 10.0, -100.0


# ── (1) the GENERATIVE MODEL of one listen ──────────────────────────────────
@gen
def listen(belief):
    s = categorical(jnp.log(belief)) @ "s"        # the (hidden) state, drawn from belief
    categorical(jnp.log(OBS[s])) @ "o"            # the growl we actually hear
    return s


# ── (2) the BELIEF UPDATE: exact posterior over state given the growl ────────
def update_belief(belief, obs):
    """b'(s) ∝ P(obs | s) b(s), computed by enumerating the 2 states with assess."""
    logp = []
    for s in range(2):
        cm = ChoiceMap.d({"s": s, "o": int(obs)})
        score, _ = listen.assess(cm, (belief,))   # = log[ b(s) · P(obs|s) ]
        logp.append(score)
    logp = jnp.array(logp)
    m = jnp.max(logp)
    p = jnp.exp(logp - m)
    return p / jnp.sum(p)                          # normalized posterior belief


# ── (3) the DECISION: immediate expected value of each action at a belief ────
def open_values(belief):
    """Expected reward of opening each door. b = [P(tiger-left), P(tiger-right)]."""
    bL, bR = float(belief[0]), float(belief[1])
    open_left = bL * R_TIGER + bR * R_CORRECT     # tiger-left ⇒ -100, else +10
    open_right = bL * R_CORRECT + bR * R_TIGER
    return open_left, open_right


if __name__ == "__main__":
    HEAR_LEFT, HEAR_RIGHT = 0, 1
    b = jnp.array([0.5, 0.5])                      # uniform prior: no idea
    print("belief P(tiger-left) start:", round(float(b[0]), 4))

    print("\nhearing LEFT growls (the tiger keeps sounding left):")
    for k in range(1, 4):
        b = update_belief(b, HEAR_LEFT)
        oL, oR = open_values(b)
        verdict = ("OPEN right" if max(oL, oR) > R_LISTEN else "LISTEN again")
        print(f"  after {k} growl(s): P(tiger-left) = {float(b[0]):.4f}"
              f"   E[open-right] = {oR:+.2f}   (listen = {R_LISTEN:+.0f})  →  {verdict}")

    # The Poll-2 reveal, in arithmetic: one growl is not enough; two are.
    b1 = update_belief(jnp.array([0.5, 0.5]), HEAR_LEFT)
    b2 = update_belief(b1, HEAR_LEFT)
    print("\nPoll 2 — 'open the right door now, or listen again?'")
    print(f"  1 growl : b={float(b1[0]):.3f}, E[open-right]={open_values(b1)[1]:+.2f}"
          f"  < listen cost ⇒ LISTEN again")
    print(f"  2 growls: b={float(b2[0]):.3f}, E[open-right]={open_values(b2)[1]:+.2f}"
          f"  > listen cost ⇒ OPEN the right door")

    # A growl from each side cancels exactly back to total uncertainty.
    b_cancel = update_belief(update_belief(jnp.array([0.5, 0.5]), HEAR_LEFT), HEAR_RIGHT)
    print(f"\nhear-left then hear-right cancels: P(tiger-left) = {float(b_cancel[0]):.4f}")
