# Week 8: Shared Outline
## Friday, June 19, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Topic:** Statistical decision theory → Markov Decision Processes → Reinforcement learning (Q-learning, reward shaping, simulation-based RL)
**Required reading (pre-class):** Daw, Niv & Dayan (2005), *Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control* (Nature Neuroscience) — the canonical **model-based vs. model-free** dual-systems paper. The Block-8 cog-sci thread tees this up directly.
**Textbook reading:** None this week (no MDP/RL chapter exists in the textbook yet — flagged TODO).
**Students:** ~6
**Student presenter:** **None assigned yet** (`readings_map.yml`: presenter: null). SP26 is **instructor-led by default**; candidates if one is confirmed are Schultz et al. 1997 (dopamine = TD error), Körding & Wolpert 2004 (SDT in motor control), Sims 2018 (SDT + efficient coding). **Verify before class** — if a presenter is confirmed, the Block-8 cog-sci thread compresses to a 2-min bridge + handoff (see Contingencies). *(Note: the Ho et al. teaching papers that anchored SP25's Week-8 presentations have moved to Week 9, Inverse RL.)*

---

## Key Design Decision

**This week makes the jump from inference to *agency*: from "what should I believe?" (Weeks 1–7, Bayes) to "what should I *do*?"** It is built as a **three-act arc** that makes the model-based/model-free distinction concrete through *two* worked examples, then synthesizes them:

1. **Decision theory (one-shot):** the normative frame — observe, then act to minimize expected loss. The hinge from belief-updating to acting.
2. **Act I — Plan on a *known* MDP (Chibany):** sequential decisions; the MDP framework built as *Markov chain + decisions + rewards*; **value iteration** solves it because we know the model. *"If you know the dynamics, you can sit and simulate the optimal policy."*
3. **Act II — Learn on an *unknown* MDP (GardenPath):** when we **don't** know the dynamics, **Q-learning** learns from experience. Reward shaping bites here: the way you give feedback can create **positive reward cycles**.
4. **Act III — Synthesis (simulation-based RL):** learn a model, then plan by simulating with it (Dyna → MCTS → AlphaZero → MuZero → Dreamer). The modernization tail, with three callback threads (reward-hacking/RLHF, dopamine/dual-systems, deep-RL milestones).

**What is KEPT from SP25** (professor's likes — verified against the SP25 deck `Week08_StatDecisionTheoryAndMDP.pdf`):
- The **short, general decision-theory intro**: loss $L(\theta,a)$, risk $R=\mathbb{E}[L]$, Bayes vs. minimax (with the U-curve risk plot), and the punchline **0-1 → MAP / squared → mean / absolute → median**.
- The **global framing**: "an action sequence is just one big action variable" → intractable (|A|^T sequences) → **the Markov assumption buys tractable dynamic programming**. (SP25 "Multiple actions" slide.)
- The beloved **"Markov Chains + Decisions + Rewards = MDPs"** build: a Markov chain is *a one-action MDP*; an **action = which transition matrix to use**; a **policy** maximizes discounted reward. (SP25 MDP-definition slide.)
- The **GardenPath 3×3 grid** and the **detailed step-by-step Q-learning trace** (the 3 algorithm steps: list actions+Q → ε-greedy select *with the actual Uniform draw* → the update arithmetic). The professor explicitly likes GardenPath — it stays.
- The **Ho et al. (2015)** feedback contrast (reward-maximizing vs. action-feedback) showing **positive net reward cycles**.

**What CHANGES (professor's asks):**
1. **Replace the disliked pre-GardenPath MDP.** SP25's intro MDP was the **"MDP for final project / party"** example (Work for +100 vs. Party for +10, with a "distracted by a cute guy" outcome) — silly and dated. It was *already non-spatial*; the professor disliked *that specific example*, not the non-spatial idea. **Replace it with the Chibany wellbeing MDP** (below): same chokepoint structure, on-brand (upgrades the Week-6 bento Markov chain), clean numbers.
2. **Apply MDP solutions *back* to the example.** SP25 jumped straight from the Bellman recursion to Q-learning — it **never showed value/policy iteration solving an MDP**. Block 5 fixes this: value iteration back-solves the Chibany MDP (V converges; the optimal policy braves the chokepoint; a **γ-sweep** shows the policy flip).
3. **Interactive Q-learning.** Replace the Matlab demo with a **vanilla-JS canvas widget** (`widgets/qlearning-gridworld.html`) that **single-steps the algorithm with an on-screen "current step" indicator**, live Q-heatmap + policy arrows, a reward-scheme toggle (rm / af / potential-based), and a **positive-cycle counter**. (Professor's explicit ask: step-by-step with visual updating showing which algorithm step it is in.)
4. **Modernize the tail** (a decade-overdue wish): **simulation-based RL** (the professor's preferred term for "model-based") as the spine + reward-hacking→RLHF + dopamine/dual-systems + deep-RL milestones — all as callbacks. The SP25 deck's own final slide already sets this up: *"if we knew the transition and reward functions, we could just sit and **simulate** to compute the optimal policy."*
5. **Scope beyond the lecture:** interactive widget **+** GenJAX port of the RL assignment **+** refresh the homework (post-lecture workstream; GardenPath stays, so it's modernization not a rewrite).

**Authoring style** follows Week 7 (the canonical recent example): Quarto RevealJS, `theme: [dark, ../../sds-reveal/sds.scss]` (five-tier, in frontmatter per CLAUDE.md), `include-in-header: week8-styles.html` (copied from `week7-styles.html` — **must be committed**), EN/JA `.lang-en`/`.lang-ja` divs on every concept slide, KaTeX, sibling-slide build-ups, polls as bullet lists in **one** `.fragment` wrapping paired lang divs. **Define every new symbol at first use** (the heaviest-notation week — see the notation plan). Background-iframe interactive widget per the Week-7 `mcmc-gmm.html` precedent.

**"Where we are" recap slides.** `{.agenda .dense}` at each act boundary; bilingual bullets; `.done`/`.highlight` on **both** lang spans per the CLAUDE.md agenda rule. Four recaps: before MDPs, before solving, before learning, before the modernization tail.

---

## The two worked examples (VERIFIED numerically — `/tmp/wk8_verify.py`, fold into `make_figures.py`)

### Example A — Chibany wellbeing MDP (the non-spatial intro MDP; upgrades the Week-6 bento chain)

Non-spatial, **3 states, 2 actions**, small enough to display the full transition matrices (the "action = pick the matrix" point).

- **States:** S0 = **Junk rut**, S1 = **Trying** (the chokepoint trough), S2 = **Healthy & happy**.
- **Actions:** a0 = **Indulge** (comfort; drifts down), a1 = **Invest** (effort; climbs up).
- **Reward on state:** R(Junk)=**+1**, R(Trying)=**−2**, R(Healthy)=**+5**. (Trying is a *trough* — effort with no payoff yet.)
- **Transition matrices** (rows = from-state {Junk,Trying,Healthy}, cols = to-state):

  Indulge: `[[.9,.1,0],[.7,.3,0],[.2,.5,.3]]`  Invest: `[[.4,.6,0],[.1,.4,.5],[0,.1,.9]]`

- **Chokepoint (verified):** "Trying" (R=−2) is the **only** route Junk→Healthy. A myopic agent stays in the Junk rut (Indulge, +1 forever); a far-sighted one eats the −2 trough to reach +5.
- **γ-sweep (verified):** the Junk-state optimal action **flips Indulge → Invest at γ ≈ 0.64**. Below it, Chibany stays in the rut; above it, he invests and gets healthy. *This is the discounting payoff figure and Poll 2.* (At γ=0.9, V≈[25.6, 28.4, 39.8], policy = Invest everywhere.)
- **Diagram style:** redraw in the clean SP25 convention — states = circles, actions = labeled branches, P and R on the outcome arcs (the SP25 *party* MDP's layout, de-cluttered).

### Example B — GardenPath 3×3 (the Q-learning walkthrough; from the SP25 Matlab tables)

- **Grid:** 3×3, `s=(row,col)`, row 1 = bottom, col 1 = left. **Start (1,1)** bottom-left, **Goal (3,3)** top-right (terminal). **Garden** = bottom-right 2×2 = {(1,2),(1,3),(2,2),(2,3)}. **Path** = left column + top row (the L). Actions UP/DOWN/LEFT/RIGHT (boundary moves invalid).
- **Hyperparameters (SP25):** α (learnRate) = 0.9, γ (discRate) = 0.95, ε (randActProb) = 0.1, Q₀ = 0.
- **Feedback magnitudes:** POS=+10, NEG=−10, NO=0, GOAL=+20.
- **Three reward schemes (verified policies via value iteration):**
  - **`rm` (reward-maximizing / outcome):** 0 for path moves, −10 toward garden, +20 into goal → Q-learning learns the **correct L-path** `(1,1)→(2,1)→(3,1)→(3,2)→(3,3)`. ✓
  - **`af` (action-feedback / Ho et al. "how people teach"):** +10 per "good" action, −10 per "bad" → the optimal policy is a **POSITIVE CYCLE** `(1,1)→(2,1)→(3,1)→(3,2)→(2,2)→(1,2)→(1,1)→…` that **never reaches the goal** (the 6-step loop nets +20 in feedback, so looping forever beats finishing once). ✗ **This is the centerpiece** — the professor's "how easy it is to get positive net cycles," vindicated by their own action-feedback table.
  - **`potential` (potential-based shaping, Ng/Harada/Russell 1999):** F = γΦ(s′)−Φ(s) with Φ = −dist-to-goal → **recovers the correct path**, provably **cannot create cycles** (telescopes to 0). ✓ The fix.
- **Step-by-step trace (SP25, keep + make interactive):** for each step show (1) possible actions + their current Q-values, (2) ε-greedy choice *with the actual Uniform[0,1] draw vs. 1−ε and the `ceil(k·U)` index*, (3) the update arithmetic, e.g. `Q ← 0 + 0.9·(−10 + 0.95·0 − 0) = −9`. The early garden moves all give −9; the first move *onto the path* (e.g. (2,2)→UP) gives `0 + 0.9·(+10 + …) = +9`. These three numbered steps **are** the widget's stepper stages.

---

## Source material (what to mine)

| Source | Path | What to take |
|---|---|---|
| **SP25 Week 8 deck** (28 slides) | `slides/Week08_StatDecisionTheoryAndMDP.pdf` (+ `.pptx`) | DT formalism + **risk U-curve plot** (Bayes vs minimax); "Multiple actions"/discounting framing; **"Markov Chains+Decisions+Rewards=MDPs"** definition slide; policy/value/Q + Bellman recursion slides; the **GardenPath step-by-step Q-learning trace** (grids + ε-greedy draws + update arithmetic); the **model-free vs model-based** closing slides (the "sit and simulate" hook). **Skip/replace** the *party* MDP. |
| **SP25 RL assignment** | `course/assignments/rl/{rl.tex, figs/gardenpath.png}` + Matlab `af_feedback.m`/`rm_feedback.m`/`transState.m` (in `archive/.../matlab_code_for_rl_assign.zip`, extracted to `/tmp/wk8_matlab`) | Exact GardenPath geometry + the rm/af feedback tables (encoded in `/tmp/wk8_verify.py`); the `gardenpath.png` figure to reuse. |
| **Week 6 deck** | `course/week06_markov_chains_networks/{week6-shared-outline.md, make_figures.py, images/chibany-bento-markov.png}` | The 2-state Chibany bento Markov chain to **upgrade into the MDP**; `make_figures.py` `save()` helper + palette. |
| **Week 7 deck** | `course/week07_monte_carlo/{week7-slides.qmd, week7-styles.html, make_figures.py, widgets/mcmc-gmm.html}` | The qmd skeleton, the styles file to copy, the figure-script template, and the **interactive-widget pattern** to model the Q-learning widget after. |
| **readings_map.yml** Week 8 | required Daw 2005; candidates Schultz 1997 / Körding-Wolpert 2004 / Sims 2018 | Decision-theory cog-sci name-drops (Körding-Wolpert); the dual-systems thread (Daw); dopamine thread (Schultz). |

---

## Figure inventory (scaffold-then-generate via `make_figures.py`; reuse where noted)

**To make** (matplotlib, transparent bg, dark-theme palette, dpi=150 → `images/`):
- `dt-risk-curve.png` — U-curve $\mathbb{E}^x[L(\theta,d(x))]$ vs θ + horizontal minimax line + uniform-prior Bayes shading. *(redraw SP25 risk plot.)* — Block 2.
- `dt-loss-estimators.png` — a posterior with **MAP / mean / median** marked, beside the three loss shapes (0-1 / squared / absolute). **Two-column.** — Block 2.
- `chibany-mdp-diagram.png` — **★** the 3-state Chibany MDP (circles + Indulge/Invest branches + P,R labels). Replaces the SP25 party MDP. — Block 4.
- `chibany-transition-matrices.png` — **two-column 50/50**: Indulge matrix | Invest matrix (the "action = pick the matrix" figure). — Block 4.
- `chibany-chain-to-mdp.png` — the upgrade: Week-6 2-state bento chain → +reward → +action choice. *(annotate/reuse `week6 chibany-bento-markov.png`.)* — Block 4.
- `value-iteration-converge.png` — V(Junk/Trying/Healthy) per iteration converging + optimal-policy arrows. — Block 5.
- `gamma-sweep-policy.png` — **★** Junk-state optimal action (Indulge↔Invest) vs γ, flip at ≈0.64. The discounting payoff. — Block 5.
- `qlearning-update-anatomy.png` — the TD update color-coded: target $r+\gamma\max_{a'}Q$, error = target−Q, $Q\leftarrow Q+\alpha\cdot$error. — Block 6.
- `feedback-rm-vs-af.png` — **★ two-column 50/50**: rm pattern (→ correct path) | af pattern (→ the positive-cycle loop drawn on the grid). — Block 7.
- `potential-shaping.png` — naive cycle | potential-based no-cycle (before/after). — Block 7.
- `simulation-based-rl.png` — Dyna/MuZero schematic: learn model → simulate rollouts → plan. — Block 8.
- `rl-timeline.png` — tabular → DQN/Atari → AlphaGo → AlphaZero → MuZero → Dreamer (function-approx + simulation arc). — Block 8.
- `dopamine-td.png` — TD-error/dopamine schematic (Schultz-style: reward, prediction, δ). — Block 8.

**Reuse:** `course/assignments/rl/figs/gardenpath.png` (the GardenPath domain) — Block 6. Week-6 `chibany-bento-markov.png` — Block 4. Week-1..7 cat break-slide photo — break.

**Widget renders live (with static PNG fallbacks):** the GardenPath grid, Q-heatmap, policy arrows, the step-by-step trace, the learning curve, and the positive cycle. The widget is the centerpiece of Blocks 6–7.

---

## Session Plan

| Time | Block | Min | What happens |
|------|-------|-----|--------------|
| 0:00 | **1. Welcome + "from beliefs to actions"** | 6 | Admin (Assignment 3/4 status; final-project pulse). The pivot: Weeks 1–7 inferred *beliefs*; now we *act*. |
| 0:06 | **2. Statistical decision theory** | 15 | Formalism (θ, x, A, d(x), L); risk $R=\mathbb{E}[L]$; **Bayes vs minimax** (risk U-curve); **0-1→MAP / squared→mean / absolute→median** on Chibany (Week-2 weight callback). **Poll 1.** |
| 0:21 | **3. From one decision to a sequence** | 8 | One action = a whole sequence → $|A|^T$ blow-up (intractable) → **Markov assumption → dynamic programming**; discount future reward ($10 now vs in 1000 yr). |
| 0:29 | **4. MDPs = Markov chains + decisions + rewards** | 17 | A Markov chain = a 1-action MDP; **action = pick the transition matrix**; S,A,T,R,γ,π. The **Chibany MDP** (upgrade Week-6 chain). **Notation lock-in.** **Poll 2** (γ teaser). |
| 0:46 | **5. Solving MDPs — back-solve Chibany** | 18 | $G_t$, $v_\pi$, $q_\pi$, $\pi^*$, **Bellman**; **value iteration** (DP); apply *back* to Chibany (V converges, optimal policy braves the chokepoint); **γ-sweep** flip. "Know the model ⇒ sit and simulate." |
| 1:04 | **Break** | 5 | (cat break-slide) |
| 1:09 | **6. Learning an *unknown* MDP — Q-learning on GardenPath** | 18 | Model-free motivation (we don't know T,R); **Q-learning** TD update (sibling build-up); GardenPath; the **step-by-step trace**. **Poll 3** (reward-design). |
| 1:27 | **7. Interactive: reward shaping & positive cycles** | 15 | The **widget**. rm learns the path; **af (Ho et al.) loops forever — positive cycle**; **potential-based shaping** fixes it. *How you give feedback matters.* |
| 1:42 | **8. Modernization: simulation-based RL & where RL is now** | 16 | model-free/based → **simulation-based** (Dyna→MCTS→AlphaZero→MuZero→Dreamer); deep-RL bridge (DQN→AlphaGo); **reward hacking→RLHF** (callback to B7); **dopamine/dual-systems** (tee up Daw 2005). Recap + Week-9 bridge (inverse RL). |
| 1:58 | **Close** | 2 | Recap the three acts; assignment reminder; Week-9 preview. |

**Cut order under time pressure** (Blocks 5 value-iteration and 7 widget never cut): (1) Block 8 deep-RL + dopamine threads compress to one slide each (keep simulation-based + reward-hacking); (2) Block 3 folds into Block 4's opening; (3) Block 2 minimax risk-plot becomes a name-drop; (4) the Q-learning trace shrinks to 3 sibling slides + "and the widget does the rest."

---

### Block 1 — Welcome + "from beliefs to actions" (6 min)
- Admin (2 slides): Assignment status + final-project pulse (reuse the Week-7 admin slide format; **verify dates** before class).
- **The pivot (the spine of the whole week):** Weeks 1–7 answered *"given data, what should I believe?"* (Bayes). Today: *"given beliefs, what should I do?"* One bilingual hinge slide. Name-drop that the brain seems to do this too (Körding & Wolpert 2004 — sensorimotor SDT; this week's reading is Daw 2005).

### Block 2 — Statistical decision theory (15 min)
- **Formalism** (one build-up slide): state of world **θ**, observation **x**, actions **A**, decision rule **d(x)**, loss **L(θ,a)**. *Define each symbol as named.*
- **Chibany one-shot decision** (re-skin SP25's bridge/tunnel): Chibany must commit to tonkatsu vs hamburger under uncertainty about freshness (discrete, 0-1 loss); *or* estimate his bento's **weight** (continuous — **Week-2 Gaussian callback**).
- **Risk** $R(\theta,d(x))=\mathbb{E}_x[L(\theta,d(x))]$ — "how good is the rule, in expectation."
- **Two criteria** (two-column): **Bayesian** $\arg\min_d \mathbb{E}_\theta\mathbb{E}_x[L]$ (have a prior) vs **minimax** $\arg\min_d \max_\theta \mathbb{E}_x[L]$ (worst case). `dt-risk-curve.png`.
- **The punchline table** (the part to remember): **0-1 loss → MAP**, **squared (L²) → mean**, **absolute (L¹) → median**. `dt-loss-estimators.png` (two-column: loss shapes | posterior with the 3 points). *Keep it short — this is the hinge, not the destination.*
- **Poll 1** (decision theory): graded by **absolute** error → report the **median**.

### Block 3 — From one decision to a sequence (8 min)
- SP25 "Multiple actions" framing: decision theory says how to take *one* action — what about a *sequence*? "In theory no difference: the action variable just takes a whole sequence as its value."
- **Why that's hopeless:** there are $|A|^T$ sequences (combinatorial blow-up) — you can't enumerate them. *(This is the intractability the professor wants foregrounded.)*
- **The rescue:** if the world is **Markov** (next state depends only on current state + action), the problem factorizes and we can solve it by **dynamic programming** (a recursion, Block 5). One bilingual slide stating the assumption.
- **Discounting:** we won't just sum rewards — **discount** the future by γ. "$10 now or $10 in 1000 years?" Introduces γ informally (formalized in Block 4).

### Block 4 — MDPs = Markov chains + decisions + rewards (17 min)
- **The build (professor's beloved sequence), as sibling slides:**
  1. **Recall the Week-6 Chibany bento chain** — one transition matrix P, no agency. `chibany-chain-to-mdp.png` (panel 1).
  2. **+ Reward** ⇒ a **one-action MDP**. "A Markov chain with a reward attached is the simplest MDP."
  3. **+ a choice of matrix** ⇒ **actions**: Chibany can **Indulge** or **Invest**, each a *different transition matrix*. *An action selects which transition matrix governs tomorrow.* `chibany-transition-matrices.png` (two-column Indulge | Invest).
  4. **Policy** $\pi(a\mid s)=P(a_t\mid s_t)$ — Markov, depends only on current state.
- **MDP definition slide** (keep SP25's): **S** (states), **A** (actions = decision rules), **T** = $P(s_{t+1}\mid a_t,s_t)$ (a transition matrix per action; *MC = 1-action special case*), **R(s,a)** = reward (= −Loss), **γ** = discount.
- **The Chibany MDP, assembled:** `chibany-mdp-diagram.png` (★). States Junk/Trying/Healthy, rewards +1/−2/+5, the chokepoint visible. Pose the question (SP25): *"What's the optimal policy?"* — answered in Block 5.
- **Notation lock-in slide** before Block 5: collect s, a, T, R, γ, π in one dim reference box (bilingual).
- **Poll 2** (γ teaser, commit-before-reveal): "Chibany's in the Junk rut. If he barely weighs the future, should he Invest?" → No (stay) — set up the Block-5 γ-sweep reveal.

### Block 5 — Solving MDPs, and back-solving Chibany (18 min) — *the SP25 gap-fix*
- **Return & value** (keep SP25 slides): $G_t=\sum_k \gamma^k R_{t+k+1}$; **state value** $v_\pi(s)=\mathbb{E}_\pi[G_t\mid s]$; **action value** $q_\pi(s,a)=\mathbb{E}_\pi[G_t\mid s,a]$; **optimal** $\pi^*=\arg\max_\pi v_\pi$.
- **Bellman recursion** (keep SP25): $q_\pi(s,a)=\mathbb{E}_\pi[R_{t+1}+\gamma q_\pi(S_{t+1},A_{t+1})]$ — "a recursive definition ⇒ dynamic programming."
- **Value iteration** (NEW — the fix): the DP algorithm $V_{k+1}(s)=\max_a\big[R(s,a)+\gamma\sum_{s'}T(s'\mid s,a)V_k(s')\big]$. One build-up slide + intuition ("back up values from the future").
- **Apply it BACK to Chibany** (the professor's explicit ask): `value-iteration-converge.png` — V(Junk/Trying/Healthy) climbing to ≈[25.6, 28.4, 39.8] (γ=0.9); the **optimal policy = Invest** (brave the −2 trough). *This is what SP25 never did.*
- **γ-sweep — the discounting payoff** (★): `gamma-sweep-policy.png` — sweep γ; the Junk-state action **flips Indulge→Invest at ≈0.64**. "How far Chibany looks ahead decides whether he escapes the rut." Reveals Poll 2.
- **Hinge to Act II:** value iteration needed the **full model** (T, R). *"If you know the dynamics you can sit and simulate the optimal policy — no learning needed."* But in the real world we **don't** know T, R → Block 6.

### Break (5 min) — after Block 5. Cat break-slide.

### Block 6 — Learning an unknown MDP: Q-learning on GardenPath (18 min)
- **Model-free motivation** (keep SP25's framing): we don't know T or R; learn $Q(s,a)$ from experience by **trial, feedback, update**.
- **Q-learning update — sibling-slide build-up** (the TD anatomy): observe $(r,s')$ → best next $\max_{a'}Q(s',a')$ → **target** $r+\gamma\max_{a'}Q(s',a')$ → **TD error** = target − $Q(s,a)$ → **update** $Q\leftarrow Q+\alpha\cdot$error. Define **α**, **TD error** as named. `qlearning-update-anatomy.png`.
- **The GardenPath domain** (reuse `gardenpath.png`): 3×3, start/goal/garden/path; α=0.9, γ=0.95, ε=0.1.
- **The step-by-step trace** (keep SP25; 3 sibling slides then "the widget does the rest"): for one or two steps, show the **3 algorithm steps** — list actions+Q; ε-greedy with the actual Uniform draw and `ceil(k·U)`; the update arithmetic `Q ← 0 + 0.9·(−10 + 0.95·0 − 0) = −9`. The first onto-path move gives +9.
- **Poll 3** (reward-design, commit-before-reveal — sets up Block 7): "Reward the agent +10 for every *good* move toward the goal. Will Q-learning reach the goal?" → **No — it can loop forever** (positive cycle). The widget then *proves* it.

### Block 7 — Interactive: reward shaping & positive cycles (15 min) — *the centerpiece*
- Embed `widgets/qlearning-gridworld.html` (background-iframe, `background-interactive="true"`; static fallback PNG). The widget **single-steps** the algorithm with the **current-step indicator** (the professor's ask), shows the live Q-heatmap + policy arrows + a **positive-cycle / episode counter**.
- **Live demo script (three presets, reveals Poll 3):**
  1. **`rm` (outcome reward):** run → Q-learning learns the **correct L-path**. The baseline that works.
  2. **`af` (action-feedback, Ho et al. — "how people naturally teach"):** run → the policy **loops** `(1,1)→(2,1)→(3,1)→(3,2)→(2,2)→(1,2)→…` and **never reaches the goal**. The **positive cycle** — *good local feedback, globally broken.* `feedback-rm-vs-af.png`.
  3. **`potential` (potential-based shaping, Ng et al. 1999):** run → **back to the correct path.** Why: F = γΦ(s′)−Φ(s) telescopes to 0 over any cycle, so it can't create one. `potential-shaping.png`.
- **The lesson** (bilingual): reward you can *farm in a loop* destroys the task; **shaping must be potential-based** to preserve the optimal policy. This is the Ho et al. result and the bridge to Block 8's **reward hacking**. *(Deep teaching-signals discussion → Week 9, inverse RL.)*

### Block 8 — Modernization: simulation-based RL & where RL is now (16 min, fenced threads)
- **Spine — simulation-based RL (~6 min):** SP25's own hook — *"if you knew the model you'd just simulate the optimal policy."* So **learn a model, then plan by simulating with it.** **Dyna** (learn T, imagine rollouts) → **MCTS** → **AlphaZero** (MCTS + learned value/policy) → **MuZero** (learned *latent* dynamics) → **Dreamer / world models**. `simulation-based-rl.png`. *Reframe "model-based" → "simulation-based"* explicitly (the professor's preferred term) and call back to **Week 7** (this *is* Monte-Carlo simulation) and to Act I vs Act II (planning vs learning; simulation-based RL is the synthesis).
- **Deep-RL bridge (~3 min, fence-compressible):** tabular Q can't scale → **function approximation**: **DQN/Atari** → policy gradients / actor-critic / **PPO** → **AlphaGo**. `rl-timeline.png`. "How we got from a 3×3 grid to beating Go."
- **Reward hacking → RLHF (~3 min):** **callback to Block 7's positive cycle** — *reward hacking is the same bug at frontier scale.* How LLMs are aligned: reward models + KL-regularized RL; why reward hacking is hard to rule out. Plants the Weeks 11–13 thread.
- **Cognitive science of RL (~3 min, hand-off-able to a Schultz presenter):** **dopamine = TD error** (`dopamine-td.png`; Schultz/Montague/Dayan 1997) and **model-based vs model-free = goal-directed vs habitual** brain systems — **tee up the Daw et al. 2005 required reading**. Returns RL to the course's cog-sci roots.
- **Close (2 min):** recap the three acts (plan known → learn unknown → simulate-and-plan); Week-9 bridge: *we've watched agents act; next week we invert it — **inferring goals from behavior** (inverse RL).*

---

## Per-block visual budget (audit checklist before "lecture-ready")

| Block | Figure(s) | Two-column | Build-up |
|---|---|---|---|
| 2 Decision theory | `dt-risk-curve`, `dt-loss-estimators` | Bayes \| minimax; loss \| posterior | formalism build-up |
| 3 One→sequence | (text + γ teaser) | — | — |
| 4 MDPs | `chibany-mdp-diagram`★, `chibany-transition-matrices`, `chibany-chain-to-mdp` | Indulge \| Invest matrices | chain→+reward→+action |
| 5 Solving | `value-iteration-converge`, `gamma-sweep-policy`★ | — | value-iteration steps |
| 6 Q-learning | `qlearning-update-anatomy`, `gardenpath` | — | TD-update anatomy; trace steps |
| 7 Interactive | widget + `feedback-rm-vs-af`★, `potential-shaping` | rm \| af | (demo is the build-up) |
| 8 Modernization | `simulation-based-rl`, `rl-timeline`, `dopamine-td` | planning \| learning | Dyna→MCTS→AlphaZero→MuZero |

---

## Polls (authored — no fitting SP25 conceptual quiz exists for SDT/MDP; record provenance in speaker notes)

| # | Block | Prompt → reveal |
|---|---|---|
| 1 | 2 | "You'll be graded by **absolute** error on your estimate. Which posterior summary do you report?" → **median** (L¹). |
| 2 | 4→5 | "Chibany's in the Junk rut and barely weighs the future. Should he **Invest**?" → **No, stay** — revealed by the Block-5 γ-sweep (flips at γ≈0.64). |
| 3 | 6→7 | "Reward +10 for **every good move toward the goal**. Will Q-learning reach the goal?" → **No — positive cycle, loops forever** — proven live by the widget's `af` preset. |

All bilingual: options as a bullet list inside **one** `.fragment` wrapping paired `.lang-en`/`.lang-ja` divs; paired-lang reveal answer line.

---

## Contingencies

- **If a Week-8 presenter is confirmed** (`readings_map.yml`): the natural fit is **Schultz 1997** — convert the Block-8 dopamine thread to a 2-min bridge + handoff. Körding-Wolpert would attach to Block 2; Sims 2018 to Block 2 + a Week-4 generalization callback. Verify first.
- **Behind schedule at the break:** compress Block 8 to simulation-based + reward-hacking (drop deep-RL timeline + dopamine to one slide each); the widget (Block 7) and value iteration (Block 5) are protected.
- **Widget fails to load:** fall back to `feedback-rm-vs-af.png` + `potential-shaping.png` + the static trace PNGs; narrate the positive cycle. Poll 3 still works against the static af-loop image.
- **DT runs long:** drop the minimax risk-plot to a name-drop; keep the loss→estimator table (the part worth remembering).

---

## TODOs spawned by this outline

- [ ] Build `week8-slides.qmd` (theme line, `include-in-header: week8-styles.html`, EN/JA divs, KaTeX, 3 polls, 4 agenda recaps, the widget iframe + PNG fallback, `resources:` for the widget).
- [ ] Copy `week7-styles.html` → `week8-styles.html` (adjust break-cat selector); **commit it**.
- [ ] `make_figures.py` — generate the 13 figures above (fold in `/tmp/wk8_verify.py`'s MDP + GardenPath cores); reuse `gardenpath.png` + Week-6 chain figure.
- [ ] Build `widgets/qlearning-gridworld.html` — steppable Q-learning w/ current-step indicator, rm/af/potential toggle, Q-heatmap + arrows, positive-cycle counter (model after `mcmc-gmm.html`).
- [ ] Author JA translations for every concept slide + poll; native-speaker proof later.
- [ ] Run the RevealJS fill audit (`scripts/audit_slide_fill.js --threshold 75`, early + final `--all-sizes`); clarity-agent pass (2–3 personas) → record findings+fixes in PLAN.md.
- [ ] **Verify the Week-8 presenter** in `readings_map.yml` before class; wire the Block-8 contingency accordingly.
- [ ] Update `course/quizzes/README.md` Week-8 mapping if it still points at "Monte Carlo Estimation" (conceptual mismatch — polls are authored).
- [ ] **Post-lecture workstream:** refresh `course/assignments/rl/` to the plan-then-learn framing + add a GenJAX stencil (MDP env as a generative function for simulation-based rollouts; confirm framing). Author a textbook MDP/RL chapter (separate session).
