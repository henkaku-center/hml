# Week 8 → Textbook Tutorial — Handoff Bundle

*Transient handoff doc (untracked; delete after use). Paste this path into a fresh **planning session** to author the Week 8 textbook tutorial (MDPs / value iteration / Q-learning / simulation-based RL) with interwoven, runnable GenJAX — matching the last three weeks' tutorials.*

**Suggested opening prompt for the new session:**
> Plan a Week 8 textbook chapter on MDPs → value iteration → Q-learning → simulation-based RL with interwoven, runnable GenJAX, matching the structure/style of the last three weeks' tutorials in `textbook/content/intro2/`. Read this handoff: `course/week08_sdt_mdp_rl/TEXTBOOK_HANDOFF.md`. Reusable verified backbone: `course/week08_sdt_mdp_rl/genjax_chibany_mdp.py`. Follow `textbook/CLAUDE.md` (Hugo, date frontmatter, `validate_code_blocks.py`).

---

## 0. Process notes (what worked for the lecture, reuse for the tutorial)
- **Outline-first → author → verify.** The lecture used `weekN-shared-outline.md` as source of truth before authoring.
- **Mirror the lecture's examples and *exact numbers*** (below) so the textbook and lecture reinforce each other.
- **The GenJAX code already exists and is verified** — build the tutorial's code around it, don't re-derive.
- **Textbook is a SEPARATE project**: switch to `textbook/CLAUDE.md` conventions (date frontmatter, code-block validator, MT-Japanese `.ja.md` siblings). Do NOT carry over Quarto/RevealJS slide assumptions.

## 1. Concept arc (the lecture's three-act spine)
- **Act 0 — Statistical decision theory (brief):** loss $L(\theta,a)$, risk $R=\mathbb E[L]$, **Bayes vs. minimax**, and 0–1 / squared / absolute loss → **MAP / mean / median**. (May be optional for the tutorial depending on the 3-week scope — decide in planning.)
- **Act 1 — MDPs & planning (the core):** Markov chain → **+ reward** (one-action MDP) → **+ a choice of transition matrix** (= actions) → **policy**. Then **value $V$**, the **Bellman equation**, **value iteration**, and $\gamma$. Back-solve the Chibany MDP and watch the optimal policy take the chokepoint.
- **Act 2 — Learning when the model is unknown:** **Q-learning** on GardenPath (model-free). TD update, $\varepsilon$-greedy, $\alpha$.
- **Act 3 — Simulation-based RL (the synthesis):** learn a model, then *plan by simulating* (Dyna → MCTS → AlphaZero → MuZero → Dreamer). Direct callback to Week 7's Monte-Carlo simulation. *(This is where GenJAX shines: the MDP-as-generative-model lets you simulate rollouts.)*

**Natural textbook core:** Chibany MDP → value iteration (known model) → Q-learning on GardenPath (unknown model) → simulation-based RL (learn a model, simulate). The GenJAX `@gen` transition model is the through-line.

## 2. The two worked examples — USE THESE EXACT NUMBERS

### (a) Chibany wellbeing MDP — non-spatial intro, 3 states / 2 actions
- **States:** `0 = Junk rut` (R=+1), `1 = Trying` (R=−2), `2 = Healthy & happy` (R=+5). Reward is **state-only**: `R(s) = [1, −2, 5]`.
- **Actions:** `0 = Indulge` (order out), `1 = Invest` (cook / exercise).
- **Discount:** `γ = 0.9`.
- **Transition tensor** `T[a][s][s']` (each row sums to 1):
  - Indulge (a=0): `J→[.9,.1,0]`, `T→[.7,.3,0]`, `H→[.2,.5,.3]`
  - Invest (a=1): `J→[.4,.6,0]`, `T→[.1,.4,.5]`, `H→[0,.1,.9]`
- **Verified solution:** `V* = [25.6, 28.4, 39.8]`, **optimal policy = Invest in every state**. MC-simulated `V(Junk) = 25.7` vs exact `25.6`.
- **The chokepoint:** the only road to the +5 (Healthy) runs through the −2 trough (Trying) — Investing is *locally* bad but *globally* optimal. The Junk-state action flips Indulge→Invest at **γ ≈ 0.64** (a nice γ-sweep figure exists).
- **Value iteration by hand (lecture trace):** $V_0=0$; sweep 1 → $V_1=R=[1,-2,5]$; sweep 2 → $[1.6,-0.4,8.9]$ (Junk still picks Indulge); by **sweep 5** Junk flips to **Invest**; converges to `[25.6,28.4,39.8]`.

### (b) GardenPath — spatial, model-unknown (for Q-learning)
- 3×3 grid (**Ho, Littman, Cushman & Austerweil, 2015**). State `[row,col]`, row 1=bottom…3=top, col 1=left…3=right. **start (1,1)** bottom-left, **goal (3,3)** top-right (terminal). **garden** = bottom-right 2×2 `{(1,2),(1,3),(2,2),(2,3)}`. The **path** = left column + top row.
- Q-learning hyperparams: `α=0.9, γ=0.95, ε=0.1`. Deterministic moves; reaching the goal ends the episode.
- **Reward schemes (the teaching-signal contrast — Ho et al.):**
  - **reward-maximizing (rm):** sparse task reward → **learns the path**.
  - **action-feedback (af, "how people teach"):** **+10 forward** on the path, **+4 (WEAK) for backtracking** on the path (a human *positive-feedback bias*), −10 garden, +20 goal → a **farmable positive cycle**: the agent paces the good path collecting praise and **never finishes** (verified: greedy never reaches goal, +14/lap cycle).
  - **potential-based shaping (Ng, Harada & Russell, 1999):** $F=\gamma\Phi(s')-\Phi(s)$ with $\Phi=-\text{dist}$ → preserves the optimal policy, **no cycle** (the principled fix).

## 3. Reusable GenJAX code (the tutorial's backbone) — already VERIFIED
**File:** `course/week08_sdt_mdp_rl/genjax_chibany_mdp.py` — runs against **genjax 0.10.3 + jax 0.5.3 (CPU)**; install `pip install "genjax==0.10.3"`.
It demonstrates exactly the three pieces a tutorial wants:
1. **MDP transition as a GenJAX generative model** — the action selects the next-state distribution:
   `@gen def transition(s, a): return categorical(jnp.log(T[a, s])) @ "s_next"`
2. **Value iteration in JAX** — `bellman(V)` = `R[None,:] + γ*(T@V)` then `max`/`argmax`; `value_iteration()` uses `lax.scan`.
3. **Monte-Carlo value by simulating rollouts** — `mc_value()` uses `vmap` over `transition.simulate(...)`; matches value iteration (the "simulation-based" payoff).

Prof's framing to preserve: he calls model-based RL **"simulation-based RL"**; the hook is *decisions integrated into a probabilistic model*.

## 4. Key pedagogical decisions from the lecture (carry these in)
- **Term:** "**simulation-based RL**" (not "model-based").
- **Notation:** introduce a symbol *when you name the variable*. Value-iteration update: $V_{k+1}(s)=\max_a\big[R(s)+\gamma\sum_{s'}T(s'\mid s,a)V_k(s')\big]$, with $\gamma=0.9$. Use **$R(s)$** for Chibany (reward is state-only) but note the general form is $R(s,a)$.
- **Q-learning vs. value iteration — be precise:** *both* assume the **same stationary MDP**; the difference is **knowing** $T,R$ (value iteration) vs. only **sampling** them (Q-learning). Q-learning needs *more* for its convergence guarantee — exploration (every $(s,a)$ infinitely often) + a Robbins–Monro step size ($\sum\alpha=\infty,\sum\alpha^2<\infty$) — but those are conditions on the *learning process*, not the world. (Full note is in the deck's speaker notes on the "No model?" slide.)
- **Color convention (if the tutorial reuses/echoes the figures):** state colors orange/red/green = Junk/Trying/Healthy; action colors blue=Invest, purple=Indulge (kept distinct from state colors).

## 5. Where everything is

**Lecture artifacts** — `course/week08_sdt_mdp_rl/`:
- `week8-slides.qmd` — the full lecture: concept order, prose, notation, the worked traces.
- `week8-shared-outline.md` — timing table + per-block key points (source of truth).
- `PLAN.md` — topics / status / GenJAX-integration notes. **Note:** its "Textbook Chapters" section says *"None yet — author a textbook MDP/RL chapter (separate session)"* → this tutorial IS that chapter.
- `genjax_chibany_mdp.py` — the verified GenJAX backbone (§3).
- `make_figures.py` — all 16 figures (matplotlib; palette constants `ACCENT/PURPLE/ORANGE/RED/GREEN/...`). Reusable figure logic: the MDP graph, value-iteration-converge, γ-sweep, rm-vs-af, potential-shaping, simulation-based-rl schematic.
- `widgets/qlearning-gridworld.html` — interactive Q-learning (rm/af/potential/human schemes; the af positive-cycle; human-teacher default + verdict toggle).
- `images/` — rendered figures.

**Textbook project** — `textbook/` (SEPARATE conventions):
- `textbook/CLAUDE.md` — **read first**: Hugo, date frontmatter, `validate_code_blocks.py`, `.ja.md` MT-Japanese siblings.
- `textbook/content/intro2/` — recent chapters. **The 3-week precedent to match (most→least recent):**
  - **Week 7 (Monte Carlo):** `16_monte_carlo.md`, `17_particle_filtering.md`, `18_markov_chain_monte_carlo.md`, `19_sampling_the_mind.md` ← *freshest interwoven-GenJAX pattern; study these first.*
  - **Week 6 (Markov chains / networks):** `13_markov_chains.md`, `14_random_walks_networks.md`, `15_memory_search.md`
  - **Week 5 (Bayes nets / causal):** `08_bayes_nets.md`, `09_conditional_independence.md`, `10_causal_bayes_nets.md`
  - **Week 8 will be a NEW chapter** — next in sequence, ~`intro2/20_*.md` (confirm numbering + title in planning; an MDP/RL chapter). It directly extends `13_markov_chains` (a Markov chain + reward + a choice of matrix = an MDP).
- `textbook/content/genjax/` (`00_getting_started` … `06_building_models`) — the GenJAX API tutorials; match their code style/conventions.
- Published at **https://josephausterweil.github.io/probintro/** (this repo holds a working copy/drafts).

**Cross-refs:** `course/readings_map.yml` (weekly readings); `course/quizzes/README.md` Week-8 mapping still says "Monte Carlo Estimation" (known mismatch — polls are authored).

## 6. Open questions for the planning agent to resolve
1. **Chapter number + title** for the new MDP/RL chapter (likely `intro2/20_*`; confirm the sequence and whether decision theory gets its own chapter or folds in).
2. **Scope:** decision theory + MDP + RL, or just MDP → RL? Match the typical breadth of the last-3-weeks chapters.
3. **GenJAX depth:** how far past the `genjax_chibany_mdp.py` backbone (e.g., a GenJAX Q-learning / rollout section; a GardenPath generative env) — and confirm versions still install.
4. **Figures:** reuse/adapt `make_figures.py` outputs, or author chapter-native figures per the textbook's figure conventions.
5. **Bilingual:** the textbook uses `.ja.md` MT siblings — confirm whether to author the EN chapter only and let the MT pipeline handle JA (see the textbook-i18n memory).
