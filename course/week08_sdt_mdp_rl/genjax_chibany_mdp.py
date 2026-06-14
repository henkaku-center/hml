#!/usr/bin/env python3
"""The Chibany wellbeing MDP in GenJAX — value iteration and simulation.

A short, runnable companion to the Week 8 lecture. It shows three things:

  (1) the MDP TRANSITION written as a GenJAX *generative model*, where the
      action selects which distribution governs the next state
      (decisions integrated into a probabilistic model);
  (2) VALUE ITERATION in JAX — when we know T and R, we *compute* the optimal
      values and policy exactly;
  (3) the SAME generative model SIMULATED — average discounted returns over many
      sampled rollouts; the Monte-Carlo estimate matches value iteration.

Verified to run against genjax 0.10.3 + jax 0.5.3 (CPU):

  value iteration  V* = [25.6, 28.4, 39.8]   policy = Invest everywhere
  simulated V(Junk) = 25.7  vs exact V*(Junk) = 25.6

Run:  pip install "genjax==0.10.3" && python3 genjax_chibany_mdp.py
"""
import jax.numpy as jnp
from jax import random, lax, vmap
from genjax import gen, categorical

# ── the Chibany MDP ────────────────────────────────────────────────────────
# states: 0 = Junk rut, 1 = Trying, 2 = Healthy
# actions: 0 = Indulge, 1 = Invest
T = jnp.array([[[.9, .1, 0.], [.7, .3, 0.], [.2, .5, .3]],    # Indulge: T[0, s, s']
               [[.4, .6, 0.], [.1, .4, .5], [0., .1, .9]]])   # Invest:  T[1, s, s']
R = jnp.array([1., -2., 5.])          # reward of being in each state
gamma = 0.9                           # discount factor


# (1) the transition as a GENERATIVE MODEL — the action picks the distribution
@gen
def transition(s, a):
    # categorical takes log-probabilities (logits); the row T[a, s] is the
    # next-state distribution chosen by action a from state s.
    return categorical(jnp.log(T[a, s])) @ "s_next"


# (2) VALUE ITERATION in JAX (we know T, R, so we can compute the answer)
def bellman(V):
    Q = R[None, :] + gamma * (T @ V)            # Q[a, s] = R(s) + γ Σ_s' T(s'|s,a) V(s')
    return jnp.max(Q, axis=0), jnp.argmax(Q, axis=0)


def value_iteration(n_sweeps=300):
    V, _ = lax.scan(lambda V, _: (bellman(V)[0], None),
                    jnp.zeros(3), None, length=n_sweeps)
    return V, bellman(V)[1]                      # converged values, greedy policy


# (3) OR ESTIMATE the value by SIMULATING rollouts of the generative model
def mc_value(s0, policy, key, horizon=80, n_traj=5000):
    def one_trajectory(key):
        def step(carry, _):
            s, disc, total, key = carry
            key, k = random.split(key)
            s_next = transition.simulate(k, (s, policy[s])).get_retval()
            return (s_next, disc * gamma, total + disc * R[s], key), None
        (_, _, total, _), _ = lax.scan(step, (s0, 1.0, 0.0, key), None, length=horizon)
        return total
    return vmap(one_trajectory)(random.split(key, n_traj)).mean()


if __name__ == "__main__":
    Vstar, pistar = value_iteration()
    print("value iteration  V* =", [round(float(v), 1) for v in Vstar],
          " policy =", ["Invest" if a else "Indulge" for a in pistar])

    vhat = mc_value(0, pistar, random.PRNGKey(1))          # V(Junk) by simulation
    print("simulated V(Junk) =", round(float(vhat), 1),
          " vs exact V*(Junk) =", round(float(Vstar[0]), 1))
