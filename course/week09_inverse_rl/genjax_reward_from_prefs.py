#!/usr/bin/env python3
"""Reward from preferences, in GenJAX — Week 9's IRL-at-scale backbone (RLHF/DPO).

The modern tail's punchline: **RLHF and DPO are inverse RL.** Instead of full
demonstrations, a human gives *pairwise preferences* ("response A is better than
B"); we fit a **reward model** to those preferences, then optimize a policy
against it. Fitting that reward IS the inverse problem — recover a hidden reward
from observed human choices. Here we do exactly the reward-modeling step.

The choice model is **Bradley–Terry** (the same logistic/MaxEnt form used in
RLHF): P(i ≻ j) = σ(r_i − r_j). We:
  (1) write it as a GenJAX @gen — latent item rewards with a normal prior, each
      observed comparison a `flip` with probability σ(r_i − r_j);
  (2) recover the reward by conditioning on the observed preferences (sampling–
      importance–resampling — vmapped GenJAX `importance`);
  (3) show the recovered reward matches the (held-out) true reward's *ordering*
      and rough spacing — preference-based IRL working.

Reward is identifiable only up to an additive constant (a shift cancels in every
σ(r_i − r_j)) — exactly IRL's ill-posedness, so we compare mean-centered rewards.

Verified to run against genjax 0.10.3 + jax 0.5.3 (CPU).
Run:  python3 genjax_reward_from_prefs.py
"""
import jax, jax.numpy as jnp
from jax import random, vmap
from genjax import gen, normal, flip, ChoiceMap

K = 3                                              # three items (e.g. candidate answers)
ITEMS = ["A", "B", "C"]
TRUE_R = jnp.array([2.0, 0.5, -1.0])               # hidden true quality (A > B > C)
PAIRS = jnp.array([[0, 1], [0, 2], [1, 2]])        # the three unordered comparisons


# ── (1) the GENERATIVE MODEL: Bradley–Terry preferences from latent rewards ──
@gen
def pref_model(pairs):
    r = jnp.array([normal(0.0, 2.0) @ f"r_{k}" for k in range(K)])   # reward prior
    for n in range(pairs.shape[0]):
        i, j = pairs[n, 0], pairs[n, 1]
        flip(jax.nn.sigmoid(r[i] - r[j])) @ f"pref_{n}"               # True ⇒ i ≻ j
    return r


def make_dataset(n_each=30, key=random.PRNGKey(0)):
    """Generate noisy human preferences from the TRUE reward (Bradley–Terry)."""
    pairs = jnp.repeat(PAIRS, n_each, axis=0)                         # balanced comparisons
    pi = jax.nn.sigmoid(TRUE_R[pairs[:, 0]] - TRUE_R[pairs[:, 1]])
    prefs = random.bernoulli(key, pi)                                 # 1 ⇒ first item preferred
    return pairs, prefs


# ── (2) INVERSION: recover the reward by conditioning on the preferences ─────
def recover_reward(pairs, prefs, key=random.PRNGKey(1), n_particles=40000):
    """Sampling–importance–resampling: P(reward | preferences) posterior mean."""
    cm = ChoiceMap.d({f"pref_{n}": bool(prefs[n]) for n in range(prefs.shape[0])})

    def one(k):
        tr, w = pref_model.importance(k, cm, (pairs,))
        ch = tr.get_choices()
        return jnp.array([ch[f"r_{i}"] for i in range(K)]), w

    rs, ws = vmap(one)(random.split(key, n_particles))
    wn = jax.nn.softmax(ws)                                           # normalized weights
    return (wn[:, None] * rs).sum(0)                                  # posterior-mean reward


def center(r):
    return r - jnp.mean(r)                                            # remove the unidentifiable shift


if __name__ == "__main__":
    pairs, prefs = make_dataset()
    n = prefs.shape[0]
    # how often each item won, as a sanity check on the data
    print(f"{n} pairwise human preferences generated from the hidden reward "
          f"{[float(x) for x in TRUE_R]} (A>B>C).")

    r_hat = recover_reward(pairs, prefs)
    print("\nrecovered reward from preferences alone (mean-centered):")
    print("  item   true     recovered")
    for k in range(K):
        print(f"   {ITEMS[k]}    {float(center(TRUE_R)[k]):+5.2f}     {float(center(r_hat)[k]):+5.2f}")

    order = [ITEMS[i] for i in jnp.argsort(-r_hat)]
    print(f"\nrecovered ranking: {' > '.join(order)}   "
          f"(true: {' > '.join(ITEMS[i] for i in jnp.argsort(-TRUE_R))})")
    print("\nThis is the RLHF reward-modeling step — preference-based inverse RL.")
    print("The reward is recovered only up to an additive constant (IRL's ill-posedness).")
