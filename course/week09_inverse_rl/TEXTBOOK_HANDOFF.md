# Week 9 → Textbook Tutorial — Handoff Bundle

*Handoff doc capturing the **final, reviewed** Week-9 lecture (Inverse RL, social cognition / ToM, POMDPs, teaching, alignment) so the textbook chapters adapt the lecture as it actually shipped — not the original outline. The deck was reordered and refined heavily after the first build; **this doc reflects the shipped deck**, which is the version to adapt.*

**Suggested opening prompt for the new session:**
> Author the Week 9 textbook chapters (T3: `intro2/23`, `24`, `25`) on inverse RL / goal inference, POMDPs+belief+teaching, and modern RL / alignment, with interwoven runnable GenJAX, matching the structure/style of `textbook/content/intro2/` (study the Week 7/8 chapters first). Read this handoff: `course/week09_inverse_rl/TEXTBOOK_HANDOFF.md`. Verified backbones live in `course/week09_inverse_rl/genjax_*.py`. Follow `textbook/CLAUDE.md` (Hugo, date frontmatter, `validate_code_blocks.py`, `.ja.md` MT siblings).

---

## 0. Process notes (reuse for the tutorial)
- **The shipped deck ≠ the first build.** The lecture was reordered (see §4) and many figures/widgets were reworked after review. Adapt the **final** `week9-slides.qmd`, not `week9-shared-outline.md`'s original block order. Where this doc and the outline disagree, **this doc wins.**
- **Outline-first → author → verify** still holds, but mirror the **deck's** examples and *exact numbers* (§2) so chapter and lecture reinforce each other.
- **The GenJAX backbones already exist and are verified** (§3) — build the chapter code around them, don't re-derive.
- **Textbook is a SEPARATE project**: switch to `textbook/CLAUDE.md` conventions (date frontmatter, `validate_code_blocks.py`, MT-Japanese `.ja.md` siblings). Do NOT carry over Quarto/RevealJS slide assumptions.
- **Apply the chapter quality bar** (now in `textbook/CLAUDE.md`) before declaring any chapter done: (a) **maximize runnable GenJAX** — reuse the §3 backbones; every cell either passes the validator with a matching `**Output:**` or is deliberately `validate: skip` with a reason; (b) **embed the matching widget(s)** via iframe (A/B/C/D, each with a fallback PNG); (c) **run the student-agent clarity-review loop** — iterate one diligent-student persona ~2–3 rounds (each round verifying the prior round's fixes) until the feedback is minimal (~8/10 + targeted fixes resolved), recording the per-round ratings. None of these are optional. (Full spec — persona template, 6-point rubric, convergence rule — is in `textbook/CLAUDE.md`.)

## 1. Concept arc — the FINAL (reordered) spine

One idea, applied to richer and richer hidden variables: **run the camera backwards** — invert a forward model to recover what's hidden. The deck's closing recap is literally "One inversion, six times."

1. **Goal inference as inverse planning** — last week's MDP gives Q-values; wrap them in a **softmax** (noisy-rational policy, *new this week*); the inversion is just **Bayes' rule**: `P(goal | actions) ∝ P(actions | goal)·P(goal)`, where **the likelihood is a policy** (the goal-seeker's softmax, run in reverse). Ill-posed → the prior + rationality assumption disambiguate.
2. **Theory of Mind = inverse RL** — the same inversion *is* mind-reading (food-truck BToM). **Attribution: Baker & Tenenbaum's inverse planning, *reviewed* as "ToM = IRL" by Jara-Ettinger 2019** (do not credit the framework to Jara-Ettinger).
3. **POMDPs — inferring beliefs** — the hidden variable gets richer: not just a goal but a **belief** `b(s) = P(s | history)` (stress: a belief *is* a probability). Tiger problem; belief update; **α-vectors / belief-MDP**; the **decision walk** (the belief rides the value envelope until it crosses a threshold, then you act).
4. **Inverse RL — recovering rewards** *(moved BEFORE teaching — see §4)* — the machine-scale version: recover a whole **reward function** from behavior. **MaxEnt IRL** (max-entropy resolves the ill-posedness) → **GAIL** (imitation as a GAN, no reward) → **AIRL** (a transferable reward) → RLHF/DPO. Reward recovery is goal inference's continuation, not a separate topic.
5. **Teaching = inverse planning, flipped** — if you know you'll be inverted, you act to be **legible**. Showing-vs-doing (Ho et al. 2016); legibility vs predictability (Dragan 2013); **CIRL** (Hadfield-Menell 2016): efficient expert demonstration is provably suboptimal — you should deviate to *teach*.
6. **Alignment & LLM Theory of Mind** — ToMnet (amortized vs Bayesian); **RLHF/DPO *are* inverse RL** (Bradley-Terry reward model = preference-based IRL); the **LLM-ToM debate, taught skeptically**: a behavioral pass ≠ the mechanism.

**The unifying frame to thread through all three chapters:** *every beat is a POMDP over "which MDP are we in?"* — the latent (goal / belief / reward / the human's objective) is what we condition observations on to infer. Say it explicitly at the seams.

## 2. Worked examples — USE THESE EXACT NUMBERS (they match the deck + the verified backbones)

### (a) Goal inference (invert the Week-8 gridworld)
- Candidate goals; softmax-optimal policy per goal; posterior by enumeration. **P(heading right) = 0.54** at the freeze-frame; freezing earlier vs later moves it **0.37 → 0.54**; a **β-sweep** goes flat (β→0, random) → sharp (β→∞, greedy/**pure exploit**, *not* "optimal").
- The inversion as Bayes' rule (its own anatomy slide): posterior (yellow) ∝ likelihood (blue, = a policy) × prior (green).

### (b) Tiger POMDP (Kaelbling, Littman & Cassandra 1998)
- 2 states, 3 actions (listen / open-left / open-right); listening accuracy **0.85**; rewards **listen −1, correct +10, tiger −100**.
- **Belief sequence after repeated agreeing growls: 0.5 → 0.85 → 0.9698 → 0.9945.**
- α-vectors: open-right value `= 110b − 100`; at **b = 0.5 it's a −45 gamble** (listen, −1, wins); the **decision threshold is b ≈ 0.90** (open-right overtakes listen). `E[open-right]` runs **−6.50 → +6.68** across the walk.
- The **decision-walk build-up** (3 sibling slides): b=0.5 (listen) → 0.85 (listen, still < 0.90) → 0.97 (cross 0.90 → open). The widget is configurable (adjust accuracy / costs / rewards).

### (c) Legible teaching (showing vs doing)
- Two goals, shared start; legible path commits early. **Observer's P(true goal) at step 1: legible 0.613 vs efficient 0.500** (both paths optimal-length).

### (d) Reward from preferences (RLHF reward model = preference-based IRL)
- Bradley-Terry: `P(A ≻ B) = σ(r_A − r_B)`. True quality **A=+2, B=+0.5, C=−1**; sample **90 pairwise preferences**; condition → recover **A=+1.36, B=0.00, C=−1.36 → A > B > C** (identifiable only up to an additive constant — IRL's ill-posedness again).

## 3. Reusable GenJAX backbones (already VERIFIED — genjax 0.10.3 + jax 0.5.3, CPU)
All in `course/week09_inverse_rl/`:
- `genjax_goal_inference.py` ★ — invert the MDP; posterior over goals via `assess` (the §2a numbers). Also the reward-recovery extension.
- `genjax_tiger_pomdp.py` ★ — Tiger belief update (the §2b sequence; `E[open-right]` −6.50 → +6.68).
- `genjax_legible_teaching.py` — efficient vs legible scored by the observer posterior (§2c).
- `genjax_reward_from_prefs.py` — Bradley-Terry reward modeling (§2d).

**Pattern that recurs:** the forward model is an `@gen` policy/transition; inference enumerates or importance-samples the latent and normalizes. `categorical` takes **logits** (it softmaxes internally) — `LOGITS = beta * Q`. Per the [[genjax-perstep-vs-vectorized-perf]] memory, **numpy-first / optional-JAX** for the Ch-25 MCTS/world-model code so `validate_code_blocks.py` stays fast.

## 4. Key pedagogical decisions from the lecture (carry these into the chapters)
- **The reorder (the big one): "Recover → Teach → Align."** The deck was reordered so **IRL methods / reward recovery come BEFORE teaching/legibility** — because legibility/CIRL are a *response* to inverse RL (act so you're easy to invert), and the whole back third is a "demonstrations" thread: recover a reward from demonstrations (MaxEnt/GAIL/AIRL) → shape demonstrations to be legible (Ho/Dragan/CIRL) → align at scale (RLHF/LLM-ToM). **Chapters should follow this order**, not the original outline's "teaching before IRL-at-scale."
- **Attribution:** inverse-planning ToM = **Baker & Tenenbaum**; Jara-Ettinger (2019) *reviewed* it as "ToM = IRL."
- **Softmax is NEW this week**, wrapping last week's value-iteration Q-values — do NOT say "last week's softmax" (Week 8 taught value iteration / ε-greedy, not softmax).
- **A belief is a probability.** Motivate `b(s)` explicitly as `P(s | history)` so the switch from `P(s|history)` to `b(s)` doesn't read as a new object.
- **Explain RLHF/DPO before the code**, then the model (Bradley-Terry), then the GenJAX, then sampled data + recovered inference (the §2d arc). Same "concept before notation/code" rule as the deck.
- **LLM-ToM is taught skeptically** (instructor's lean): present the capability wins (Kosinski / Strachan / Street), then dismantle them (Ullman 2023 belief-preserving perturbations; Pang 2025 contamination / Morgan's Canon). Bottom line: *a behavioral pass is not the mechanism; current evidence does not show LLMs have human-like ToM.* Seeds Weeks 11–13.
- **Widgets are configurable** (mirror in any chapter-embedded version): goal-inference has a drive-the-agent mode; the Tiger tracker has adjustable accuracy/cost/reward/penalty; reward-recovery uses **MaxEnt-style recovery** (reward ∝ where the agent is drawn vs. a random walker) with a **click-to-paint true-reward grid** (edit on the *true-reward* panel). The recovery honestly shows IRL's ill-posedness (a cell merely *on the way* lights up too).

## 5. Where everything is
**Lecture artifacts** — `course/week09_inverse_rl/`:
- `week9-slides.qmd` — the FINAL deck (concept order = §1, prose, notation, worked traces, full speaker notes). **Adapt this.**
- `week9-shared-outline.md` — original timing/blocks. **Stale on block order** — see §4; trust the deck.
- `PLAN.md` — topics / status / GenJAX / contemporary-ML notes; the "Textbook Chapters" T3 lines.
- `genjax_*.py` — the four verified backbones (§3).
- `make_figures.py` — ~17 figures (matplotlib; palette constants `ACCENT/PURPLE/RED/GREEN/YELLOW/DIM`). Reusable logic: Bayes-rule anatomy, inverse-vs-forward, ToM-as-IRL, food-truck, Tiger belief/α-vectors/decision-walk, POMDP→belief-MDP, legible-vs-efficient, reward-recovery, IRL-methods timeline, amortized-vs-Bayesian, LLM-ToM debate.
- `widgets/` — `goal-inference.html` (A), `pomdp-belief.html` (B), `showing-vs-doing.html` (C), `reward-recovery.html` (D); each has a `*-fallback.png`.
- `images/` — rendered figures + widget fallbacks.

**Textbook project** — `textbook/` (SEPARATE conventions): read `textbook/CLAUDE.md` first. Match the freshest interwoven-GenJAX chapters (Week 8 = `intro2/20–22`; Week 7 = `16–19`). **Next free weights → 23/24/25**; `notebook_guide.md` and `glossary.md` cross-refs on publish, then regenerate `docs/index.html` via `python3 docs/_build.py`.

## 6. Chapter map (reflects the reorder) + open questions

| Ch | `intro2/…` | Covers (final spine) | GenJAX | Widgets |
|---|---|---|---|---|
| **23 — Inverse RL: recovering the objective** | `23_inverse_rl_goal_inference.md` | §1 beats 1–2 + 4 — goal inference (Bayes-rule anatomy, softmax, ill-posedness) **and** IRL methods at scale (MaxEnt → GAIL → AIRL); reward recovery as goal inference's continuation | `genjax_goal_inference.py` (+ reward-recovery); reward-from-prefs cross-link | A + D |
| **24 — POMDPs, belief & teaching** | `24_pomdps_belief_inference.md` | §1 beats 3 + 5 — belief `b(s)`, Tiger, α-vectors, the decision-walk; then teaching/legibility/CIRL (the flip) | `genjax_tiger_pomdp.py`, `genjax_legible_teaching.py` | B + C |
| **25 — Modern RL / world models / alignment** | `25_modern_rl_world_models.md` | §1 beat 6 — RLHF/DPO as IRL (Bradley-Terry), ToMnet, LLM-ToM (skeptical) + world models (MuZero/Dreamer; the deferred Week-8 chapter, now that POMDPs land) | `genjax_reward_from_prefs.py`; **numpy-first** MCTS/world-model | reuse A/B as cross-links |

**Open questions for the planning agent:**
1. **Where does "ToM = IRL" (beat 2) live** — close of Ch 23 or open of Ch 24? It's the bridge; pick one and cross-link.
2. **Ch 25 scope** — how much world-models (MuZero/Dreamer) vs. alignment (RLHF/LLM-ToM)? It clears the deferred Week-8 world-models chapter *and* carries the alignment tail; confirm the balance.
3. **Reward-recovery exposition** — the *widget* uses MaxEnt-style visitation matching; the *backbone* (`genjax_goal_inference.py`) does Bayesian goal-posterior. Decide which the chapter teaches as "the method" (and note the other), so the text and the embedded widget agree.
4. **Figures** — reuse `make_figures.py` outputs or author chapter-native figures per the textbook's conventions.
5. **Bilingual** — author EN only and let the MT `.ja.md` pipeline handle JA (see the textbook-i18n memory).
