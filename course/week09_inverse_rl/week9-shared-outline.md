# Week 9: Shared Outline
## Friday, June 26, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Topic:** Inverse reinforcement learning → social cognition (Theory of Mind as IRL) → POMDPs & belief inference → teaching-as-inverse-planning → IRL at scale & alignment (the modern tail)
**Required reading (pre-class):** Baker, Tenenbaum & Saxe (2007), *Goal inference as inverse planning* (CogSci) — the assigned paper; the canonical goal-inference-as-inverse-planning result.
**Textbook reading:** New companion chapters authored this cycle — **T3 Ch 23** (Inverse RL / goal inference). Ch 24–25 published alongside for the curious.
**Students:** ~6. **Reflection-eligible week** (Weeks 2–12).
**Student presenter:** **None — instructor-led** (`readings_map.yml`: presenter: null). The four alternative readings (Ho et al. 2016/2015/2017, Jara-Ettinger 2019) are open as reflection readings and seed Blocks 6–7. **No presenter contingency to wire.**
**Research base:** `RESEARCH_week9.md` (deep-research workflow + 3 follow-up agents; all numbers cited there).

---

## Key Design Decision

**This week is the literal inversion of Week 8.** Week 8 ran RL *forward* — a goal/reward becomes a policy becomes actions (`goal → π → actions`). Week 9 runs *the same machinery backwards*: watch the actions, infer the goal, belief, or reward behind them (`actions → goal`). The thesis (Jara-Ettinger 2019): **action understanding = inverse reinforcement learning**, and that *is* the computational theory of social cognition. The whole deck hangs on one equation, introduced in Block 2 and reused every block after:

$$P(\text{goal}\mid\text{actions}) \;\propto\; \underbrace{P(\text{actions}\mid\text{goal})}_{\text{Week-8 softmax policy, run in reverse}}\;\cdot\;P(\text{goal}).$$

**REVISED SPINE (post-delivery rebuild — see `/home/jausterw/.claude/plans/i-just-finished-giving-giggly-swing.md`).** The first delivery was a topic-tour that re-derived Bayes every block, never defined theory of mind, introduced GANs without teaching them, and stated the unifying POMDP frame only at the very end. The rebuild fixes all of that by making **one master framework — the agent model (a POMDP) — the organizing frame from Block 1**, then working each hidden piece in turn.

**The master frame (Block 1, drawn as ONE diagram reused every block):** an agent acting under uncertainty = a POMDP with pieces world state $s$, transition $T$, observation model $O\!\to\!o$, reward/goal $R$, belief $b$, policy $\pi$. Week 8 ran it **forward** (all known → behavior); Week 9 is the **inverse** — observe behavior, infer one hidden piece. A **"map of unknowns"** slide assigns each block to a piece. The **same master diagram recurs at every block with the active piece highlighted** (`agent-model-{pomdp,R,belief}.png`) — so we *point at the lit box* instead of re-deriving Bayes (kills the repetition) and the framework stays visible throughout.

**Eight blocks = one model, worked piece by piece:**
1. **The agent model & its unknowns** (NEW frame) — master POMDP diagram + map-of-unknowns; Bayes inversion stated *once*; callback widget `mdp-value-iteration`/`qlearning` (the Week-8 forward model we invert).
2. **Infer $R$: goal inference / IRL** (world observed) — Baker; softmax-policy-as-likelihood; ill-posed; naive utility calculus; noisy-rationality folded in. Widget `goal-inference` (foreground).
3. **What is theory of mind?** (NEW, social-cognition heart) — ToM def (Premack & Woodruff 1978); Sally-Anne false belief (Baron-Cohen, Leslie & Frith 1985) + video; faux-pas; "decision theory run backwards" = inverse planning (Baker 2009); **richer import (APS-I Wk6):** Knobe side-effect, blame early/late (Malle), mind perception (agency×experience), autism & double-empathy methods lesson. Bridge: a false belief means $b\neq s$ ⇒ belief must be a separate latent ⇒ **POMDP**.
4. **Infer $b$: belief inference / POMDPs** — food-truck BToM; Tiger; belief MDP; α-vectors. Widget `pomdp-belief` (foreground) + callback `particle-filter`.
5. **Infer $R$ at scale: IRL → alignment** (leaner) — MaxEnt (= Block-2 softmax at scale); **GAN-free** GAIL/AIRL (critic-vs-imitator, "≈ a GAN" aside); Bradley-Terry one-liner; RLHF/DPO. Widget `reward-recovery` (foreground).
6. **Control the observer's belief: teaching** — flip; showing-vs-doing (Ho 2016) + widget `showing-vs-doing` (foreground); **recursive POMDP (Ho et al. 2021)** — the observer's belief is the hidden state you plan over (`recursive-pomdp-teaching.png`); Dragan; CIRL→POMDP as a *consequence* of the frame.
7. **Alignment & LLM theory of mind** (concrete) — ToMnet; RLHF=IRL; **concrete** worked Sally-Anne vignette + Ullman transparent-box perturbation + faux-pas structure. The autism outcome-null/process-difference lesson pays off here as "behavioral pass ≠ mechanism."
8. **Close** — master diagram one last time, every piece inferred; Week 10 bridge.

**Timing ≈ 2h05–2h15** (richer ToM adds ~15–20 min; de-repetition + leaner modern tail reclaim some). Cut order if over: trim modern-IRL detail (textbook carries it) → compress Knobe/blame/mind-perception to one slide → autism to one methods slide → Dragan to a name-drop. Protect Blocks 1 frame, 2 inversion, 4 Tiger, 7 LLM bottom-line.

**What is KEPT from SP25** (the two decks `Week09_IRLSocialCog.pptx` + `Week09_IRLPOMDPSocial.pptx`):
- The **core conceptual spine**: inverse RL as goal inference; social cognition / Theory of Mind as the application; the move to **POMDPs** for belief inference. (This sequencing is good and stays.)
- The **Baker et al. inverse-planning framework** as the anchor (it's the assigned reading).
- The **two SP25 quiz items** as live polls (see Polls).

**What CHANGES (the modernization — the SP25 material is ~decade-old and pre-dates the entire modern arc):**
1. **Make the inversion *literal and visual*.** SP25 stated the framework in prose; SP26 builds it as the **Week-8 MDP run backwards** (invert the *same* Chibany/GardenPath backbone students just coded) and shows the **posterior over goals updating frame-by-frame** in an interactive widget (Widget A) — the Baker "freeze-the-animation" paradigm made live.
2. **Add the belief-inference / POMDP depth properly.** Replace static POMDP slides with the **food-truck BToM demo** (★ infer a desire for a truck *not in the scene*) + the **Tiger problem** with an **interactive belief tracker** (Widget B) — belief sliding 0.5 → 0.85 → 0.97 as growls arrive, with the α-vector PWLC value picture. Teaching sequence mirrors *Algorithms for Decision Making* (Kochenderfer; the POMDPs.jl/AA228 line the professor likes).
3. **Add the teaching-as-inverse-planning block** (the instructor's own Ho et al. line + Dragan legibility + CIRL) with an interactive **showing-vs-doing** legibility toggle (Widget C). This is new to the lecture and ties prompt 4b + the alternative readings together.
4. **Add a modern tail that didn't exist in SP25:** IRL methods (MaxEnt → GAIL → AIRL), **machine ToM (ToMnet)** as amortized-vs-Bayesian, **IRL ↔ RLHF/DPO** (the alignment payoff; callback to Week-8 reward hacking), CIRL/assistance games, and the **genuinely unsettled LLM-Theory-of-Mind debate** (Kosinski/Street ↔ Ullman/Pang) — taught as a live debate, *behavioral pass ≠ mechanism*. Seeds Weeks 11–13.
5. **Interactive widgets ×4 + three interwoven-GenJAX textbook chapters** (Ch 23–25), per the Week-8 pipeline.

**Authoring style** follows Week 8 (the canonical recent example): Quarto RevealJS, `theme: [dark, ../../sds-reveal/sds.scss]` (five-tier, in frontmatter), `include-in-header: week9-styles.html` (copy `week8-styles.html` — fill-the-slide flex layout, poll boxes, two-column centering, eager-image; **must be committed**), EN/JA `.lang-en`/`.lang-ja` divs on every concept slide, KaTeX, sibling-slide build-ups, polls as bullet lists in **one** `.fragment` wrapping paired lang divs. **Heaviest-notation week after Week 8 — define every new symbol at first use** (see notation plan). Background-iframe widgets per the Week-8 `qlearning-gridworld.html` precedent, each with a static PNG fallback.

**"Where we are" recap slides.** `{.agenda}` at each beat boundary; bilingual bullets; `.done`/`.highlight` on **both** lang spans per the CLAUDE.md agenda rule. Five recaps map to the five beats.

---

## The worked examples (to VERIFY numerically — `/tmp/wk9_verify.py`, fold into `make_figures.py`)

### Example A — Inverse gridworld: recover the goal from a trajectory (inverts Week 8) ★ — VERIFIED (`genjax_goal_inference.py`)
The literal "run last week backwards," built in GenJAX (reuses the Week-8 value-iteration forward solver).
- **Setup:** a **3×3 gridworld**, start bottom-left **(0,0)**, **3 candidate goals** in the top row — left (2,0), mid (2,1), right (2,2). For each goal, value-iterate the MDP → Q → **softmax policy** `π_g(a|s) ∝ exp(β·Q_g(s,a))` (β=3, γ=0.9). One forward solve per hypothesized goal — *the Week-8 solver, reused.*
- **Inference:** uniform **prior** `P(g)`; observe a trajectory `τ`; likelihood `P(τ|g)=Π_t π_g(a_t|s_t)`; **posterior** `P(g|τ) ∝ P(τ|g)P(g)`, computed exactly by enumerating the 3 goals with GenJAX `model.assess`.
- **The worked trajectory:** **RIGHT, RIGHT, UP, UP** — a *detour* away from the two left goals that is exactly what makes it diagnostic of "right."
- **Verified numbers (for the figure + Widget A + Poll context):**
  - Full-path posterior: **P(left)=0.17, P(mid)=0.28, P(right)=0.54.**
  - **Freeze-frame** (Baker online inference; posterior on *right* after each action): **0.37 → 0.47 → 0.50 → 0.54** (ambiguous early — mid vs right tie at step 1 — resolves as the agent commits). The "ill-posed early, concentrates with evidence" story, in numbers.
  - **Rationality matters:** β=0.1 (near-random) → flat **0.33/0.33/0.34**; β=6 (highly rational) → sharp **0.08/0.20/0.72**. *The inference is only as good as the rationality assumption.*
- Drives **Widget A** + **Widget D** (reward recovery = the same inversion with a continuous reward as the latent) and the GenJAX walkthrough for Ch 23.

### Example B — The Tiger problem (POMDP belief tracking) ★ — VERIFIED
Kaelbling, Littman & Cassandra 1998. 2 states (tiger-left/right), 3 actions (listen, open-L, open-R), 2 observations (hear-L/R).
- **Rewards:** listen **−1**, open correct door **+10**, open tiger door **−100**. **Listen accuracy 0.85.** **γ = 0.95** (canonical — flag that the R `pomdp` package uses 0.75).
- **Belief update (verified by Bayes at 0.85):** `b = P(tiger-left)`; each consistent listen multiplies the odds by `0.85/0.15 ≈ 5.67`. From **0.5**, hearing left: **0.5 → 0.85 → 0.9698 → 0.9945**. hear-L then hear-R cancels back to 0.5.
- **Threshold rule:** keep listening in the uncertain middle; open once `b` crosses ~0.97. **One growl (b=0.85) is NOT enough — listen again; two agreeing growls and open.** → **Poll 2.**
- **Decision arithmetic (verified, `genjax_tiger_pomdp.py`):** immediate `E[open-right] = 110·b − 100`. After **1 growl** (b=0.85): **−6.50** — worse than the −1 listen cost → **listen again**. After **2 growls** (b=0.9698): **+6.68** → **open**. *This is the Poll-2 reveal, in arithmetic.* (hear-left then hear-right cancels back to 0.5.)
- **α-vector PWLC picture:** plot `V(b)` vs `b∈[0,1]`; each action = a line; optimal value = upper envelope; regions = optimal action. Drives **Widget B** + figure.

### Example C — The food-truck scenario (BToM belief inference) ★ — qualitative
Baker, Jara-Ettinger, Saxe & Tenenbaum 2017. ~5×10 gridworld; a **building occludes** part of the scene; trucks **Korean / Lebanese / Mexican** across two spots. The agent **walks around the building to check the far spot, doesn't find its favorite, returns to a nearer truck** → observers infer a **desire for a truck not in the scene**. Impossible for shortest-path goal accounts. The hinge from goal-inference (Block 2) to belief-inference (Block 5). Figure `food-truck-btom.png` ★.

---

## Source material (what to mine)

| Source | Path | What to take |
|---|---|---|
| **SP25 Week 9 decks** | `slides/Week09_IRLSocialCog.pptx`, `Week09_IRLPOMDPSocial.pptx` (+PDF), `…Transcript.docx` | The IRL→social-cognition→POMDP sequencing; the Baker inverse-planning framing; any reusable figures (extract via LibreOffice). **Replace** static prose with widgets + modern tail. |
| **SP25 wiki page** | `wiki_pages/social-cognition-and-inverse-rl.html` | Prose framing + the SP25 narrative to modernize. |
| **SP25 quiz** | `archive/canvas_export_sp25/gb593d4394ef21f60d12ac67866957b28/assessment_qti.xml` ("Social Cognition and Inverse Reinforcement Learning") | **Poll 1** (Q2: which is NOT IRL) + **Poll 3** seed (Q1: ToM functionalism). |
| **Week 8 backbone** | `../week08_sdt_mdp_rl/{genjax_chibany_mdp.py, make_figures.py, widgets/qlearning-gridworld.html, week8-styles.html, week8-slides.qmd, images/}` | The MDP/value-iteration core to **invert**; the figure-script template + palette; the widget scaffolding to clone; the styles file to copy; `gardenpath.png` + `chibany-mdp-diagram.png` to **reuse** for the "invert last week" callback. |
| **slack_discussion_week9.md** | `course/week09_inverse_rl/slack_discussion_week9.md` | The 4-prompt pedagogical spine → block structure; the Week-8→9 hinge framing. |
| **RESEARCH_week9.md** | `course/week09_inverse_rl/RESEARCH_week9.md` | All citations + verified numbers + widget design references (agentmodels.org, REINFORCEjs, Tiger, MaxEnt heatmaps). |
| **readings_map.yml** Week 9 | required Baker 2007; candidates Ho ×3 + Jara-Ettinger 2019 | Block 4 (Jara-Ettinger framing), Block 6 (Ho teaching line). |

---

## Figure inventory (scaffold-then-generate via `make_figures.py`; matplotlib, transparent dark-theme, dpi=150 → `images/`)

**To make:**
- `inverse-vs-forward.png` ★ — **two-column**: forward RL (goal→π→actions) | inverse RL (actions→goal). — Block 1/2.
- `bayes-inversion.png` — the `P(g|τ) ∝ P(τ|g)P(g)` anatomy, color-coded (likelihood = the softmax policy). — Block 2.
- `goal-inference-posterior.png` — gridworld trajectory + posterior-over-goals bars at freeze points. *(Widget A fallback.)* — Block 2.
- `ill-posed-inversion.png` — one short path consistent with multiple goals (the prior/rationality does the work). — Block 2.
- `softmax-rationality.png` — policy at β=0 (random) → β large (greedy); "blame the goal" for a detour. — Block 3.
- `tom-as-irl.png` — the Jara-Ettinger framing: forward = simulate the planner, inverse = invert it. — Block 4.
- `food-truck-btom.png` ★ — the food-truck gridworld (occluder, K/L/M trucks, the detour path). — Block 5.
- `tiger-belief-update.png` ★ — belief 0.5→0.85→0.97 sliding on the [0,1] line **+** the α-vector PWLC value function with action regions. *(Widget B fallback.)* — Block 5.
- `pomdp-to-belief-mdp.png` — POMDP→belief-MDP schematic + the Bayes belief-update formula. — Block 5.
- `legible-vs-efficient.png` ★ — **two-column**: efficient/predictable reach (ambiguous early) | legible reach (early veer toward true goal). *(Widget C fallback; Dragan geometry.)* — Block 6.
- `showing-vs-doing-grid.png` — **two-column**: "do" path | "show" path on the Ho-2016 gridworld, with the observer's goal-posterior under each. — Block 6.
- `reward-recovery-heatmap.png` — MaxEnt side-by-side: observed/visitation → recovered reward → ground truth. *(Widget D fallback.)* — Block 2/7.
- `irl-methods-timeline.png` — MaxEnt → GAIL → AIRL → RLHF/DPO. — Block 7.
- `amortized-vs-bayesian-tom.png` — **two-column**: ToMnet (learned/amortized) | Bayesian inversion (explicit planner). — Block 7.
- `llm-tom-debate.png` — the claim↔rebuttal structure (Kosinski/Street pro ↔ Ullman/Pang skeptical; *behavioral pass ≠ mechanism*). — Block 7.

**Reuse:** Week-8 `gardenpath.png` + `chibany-mdp-diagram.png` (the "invert last week" callback) — Block 1/2. Cat break-slide photo — break.

---

## Session Plan

> ⚠️ **The table + per-block detail below describe the ORIGINAL (delivered) lecture.** The post-delivery rebuild follows the **REVISED SPINE** at the top of this file (8 blocks, master-POMDP frame, new "What is theory of mind?" block, Ho-2021 recursive POMDP, GAN-free IRL, foreground widgets). Where the two differ, the revised spine wins. New assets added for the rebuild: figures `agent-model-{pomdp,R,belief}.png` + `recursive-pomdp-teaching.png` (in `make_figures.py`); ported APS-I figures `inverse_planning.png`, `knobe_bars.png`, `blame_path_model.png`, `asd_outcome_vs_process_stacked.png`, `pantelis_kennedy_asd_control.png`; callback widgets `mdp-value-iteration.html`, `qlearning-gridworld.html`, `particle-filter.html`; new reading **Ho et al. 2021** (*Communication in Action*, JEP:General).

| Time | Block | Min | What happens |
|------|-------|-----|--------------|
| 0:00 | **1. Welcome + "run the camera backwards"** | 7 | Admin (★ **final-project proposal due Sun Jun 28**; RL assignment out, due Jul 10; MC also Jul 10). The pivot: Week 8 mapped goal→actions; today actions→goal. `inverse-vs-forward.png`. |
| 0:07 | **2. Goal inference as inverse planning** | 20 | Baker; `P(g\|τ)∝P(τ\|g)P(g)`, likelihood = softmax policy; **invert the GardenPath** (Widget A); ill-posed → prior+rationality; r=0.97; naive utility calculus. **Poll 1.** |
| 0:27 | **3. Noisy rationality & explaining detours** | 10 | Softmax β; "assume rationality, blame the goal"; explain a detour by inferring an unseen obstacle / weirder goal. `softmax-rationality.png`. |
| 0:37 | **4. Theory of Mind = inverse RL** | 8 | Baker & Tenenbaum's inverse-planning framework (named "ToM = IRL" in Jara-Ettinger's 2019 review); this is what minds do. Bridge: so far the agent sees everything — what if beliefs are partial/false (a POMDP)? `tom-as-irl.png`. |
| 0:45 | **5. POMDPs — inferring beliefs, not just goals** | 22 | Food-truck BToM ★; forward POMDP, belief `b(s)`, Bayes update; **Tiger** (Widget B); belief-MDP; α-vector PWLC; solver taxonomy (1 slide). **Poll 2.** |
| 1:07 | **Break** | 5 | (cat break-slide) |
| 1:12 | **6. Teaching = inverse planning, flipped** | 18 | Showing-vs-doing (Widget C); legibility vs predictability (Dragan); reward-as-communication (Ho 2015 / GardenPath); CIRL — efficient demo is provably suboptimal. **Poll 4.** |
| 1:30 | **7. IRL at scale & alignment + LLM ToM** | 22 | MaxEnt→GAIL→AIRL (ill-posedness); ToMnet (amortized vs Bayesian); **IRL↔RLHF/DPO** (callback to Week-8 reward hacking); CIRL alignment; **LLM-ToM debate** (contested capstone). **Poll 3.** |
| 1:52 | **8. Close + Week 10 bridge** | 5 | Recap the five beats (goal→ToM→belief→teaching→alignment); reading + proposal reminders; Week 10 = Bayesian nonparametrics. |

**Cut order under time pressure** (Blocks 2 inversion-build and 5 Tiger never cut): (1) Block 7 LLM-ToM compresses to the 4-sentence bottom-line slide + Poll 3 (drop the method timeline detail); (2) Block 3 folds into Block 2's softmax slide; (3) Block 6 drops Dragan to a name-drop, keeps showing-vs-doing + CIRL; (4) Block 5 solver-taxonomy becomes a name-drop.

---

### Block 1 — Welcome + "run the camera backwards" (7 min)
- Admin (2 slides): ★ **Final-project proposal due Sun Jun 28, 8 PM** (two days out — headline); RL assignment (Assignment 4) is out, due Fri Jul 10; Monte Carlo also due Jul 10 — pace around the proposal. (Reuse Week-8 admin format; **verify dates**.)
- **The pivot (the spine):** Week 8 — goal/reward → policy → actions (we *acted*). Today — watch the actions, **infer the goal** (we *read minds*). One bilingual hinge slide + `inverse-vs-forward.png` (two-column). Name-drop: this is *inverse RL*, and when the agent is a person it's *social cognition*.

### Block 2 — Goal inference as inverse planning (20 min)
- **Notation lock-in** (dim reference box, bilingual): trajectory **τ** (= path of states+actions), goal **g**, posterior **P(g | τ)**, likelihood **P(τ | g)**, softmax temperature **β**, reward **R** / cost **C**. (Reuse Week-8 s,a,T,R,γ,π,Q,V.)
- **The inversion — sibling-slide build-up:** (1) forward: a goal g gives a **softmax policy** `π_g(a|s) ∝ exp(β Q_g(s,a))` — *Week 8's solver, one per candidate goal*; (2) likelihood `P(τ|g)=Π π_g(a_t|s_t)`; (3) prior `P(g)`; (4) **posterior** `P(g|τ) ∝ P(τ|g)P(g)`. `bayes-inversion.png`.
- **Invert the GardenPath (★ the literal continuity):** Widget A — the agent you trained last week, watched and inverted; freeze partway, read the posterior bars. (Also: Widget D — recover the *reward* itself, prompt 4a.)
- **GenJAX cell** (walk through live): `genjax_goal_inference.py` — per-goal softmax policy + `@gen` trajectory model + posterior over goals via `importance`. *This is the "which MDP are we in?" inference, in code.*
- **Ill-posed** (one slide): the same short path fits many goals; `ill-posed-inversion.png`. The **prior + rationality assumption** disambiguate — it's a *posterior*, not a unique answer. Baker Exp 1: **changing-goal model r=0.97** vs single-goal 0.82.
- **Naive utility calculus** (Jara-Ettinger et al.): people assume agents **maximize reward minus cost** — infer *both* from behavior.
- **Poll 1** (commit-before-reveal): "Which is NOT an example of inverse RL?" → **learning an optimal policy by interacting in an MDP** (that's forward RL). *Source: SP25 IRL quiz Q2.*

### Block 3 — Noisy rationality & explaining detours (10 min)
- **Softmax as the rationality knob:** `π(a|s) ∝ exp(β Q(s,a))`. β→∞ = perfectly rational (greedy); β→0 = random. `softmax-rationality.png` (build-up across β). Define β as named.
- **"Assume rationality, blame the goal":** when an agent blunders or detours, the model rationalizes by inferring a **weirder goal** or an **unseen obstacle** ("it went around something I can't see"). This is the same move BToM uses for false beliefs — tee up Block 5. (slack prompt 2: is this a bug or the whole point?)
- *Optional fold:* under time pressure this block merges into Block 2's softmax slide.

### Block 4 — Theory of Mind = inverse RL (8 min)
- **The framework is Baker & Tenenbaum's** (Baker, Tenenbaum & Saxe 2007; Baker, Saxe & Tenenbaum 2009 — *action understanding as inverse planning*, which they themselves call "inverse planning or inverse reinforcement learning"). The **framing slide** states it plainly: "mental-state inference from behavior **is** inverse RL — infer the agent's world-model and reward from observed actions; forward = simulate the planner, inverse = invert it." `tom-as-irl.png`.
- **Jara-Ettinger (2019) is the recent *review* that crystallizes the name** ("Theory of Mind as IRL") and adds the **naive utility calculus** (cost vs reward) — cite it as the clean modern synthesis, **not** the originator of the framework.
- **The bridge to POMDPs:** everything so far assumed the agent **sees the whole world** (an MDP). But people act on **partial and sometimes false beliefs**. To read *those* minds we must invert a model where **belief itself is hidden** → a POMDP. (Recap slide → Block 5.)

### Block 5 — POMDPs: inferring beliefs, not just goals (22 min) — *the heart*
- **Food-truck demo first (★ motivation before formalism):** `food-truck-btom.png` — the agent checks the far spot, returns to a nearer truck; observers infer a desire for a truck **not in the scene**. *You can only explain this by modeling what the agent BELIEVED.* (Baker 2017.) Shortest-path goal accounts fail here.
- **Forward POMDP** (keep it conceptual): the agent never sees state `s`, only observation `o`; it keeps a **belief** `b(s)=P(s | history)`, updated by **Bayes** after each (a,o): `b'(s') ∝ P(o|s',a) Σ_s P(s'|s,a) b(s)`. Define b, o, P(o|s,a) at first use.
- **Tiger problem — sibling-slide build-up (Widget B live):** b=0.5 → hear-left → **b=0.85** → hear-left again → **b=0.97** → cross threshold, open. Rewards −1/+10/−100, accuracy 0.85, γ=0.95. `tiger-belief-update.png`.
- **GenJAX cell:** `genjax_tiger_pomdp.py` — the belief update as Bayesian conditioning (`generate`/`importance`) reproducing 0.5→0.85→0.97; here the hidden state is the *world*, now genuinely unobserved.
- **Belief MDP + α-vectors:** the belief is a sufficient statistic → POMDP = MDP over beliefs; for 2 states the belief is a **point on a line**; value `V(b)` is **piecewise-linear convex** (each action a line; optimal = upper envelope; regions = optimal action). `pomdp-to-belief-mdp.png`.
- **Solver taxonomy (1 slide, name-drop, mirrors *Algorithms for Decision Making* Ch 19–22):** beliefs → **exact** (α-vector VI) → **offline** (QMDP, SARSOP) → **online** (POMCP, DESPOT). One line each.
- **Poll 2** (commit-before-reveal, Tiger): "You hear **one** growl from the left. Open the right door now, or **listen again**?" → **Listen again** — one growl only gets you to b=0.85, below the ~0.97 open threshold; you need ~2 agreeing growls. *Reveal with the belief numbers; Widget B proves it.*

### Break (5 min) — after Block 5. Cat break-slide.

### Block 6 — Teaching = inverse planning, flipped (18 min) — *new to the lecture*
- **The flip (slack prompt 4b):** if an observer infers your goal from your actions, you can **choose** actions that make your goal **legible** — that's teaching. One bilingual hinge slide.
- **Showing vs doing (Ho et al. 2016 — instructor's own work; Widget C):** people **doing** a task vs **showing** it move differently — demonstrators deviate from the efficient path to make the reward unambiguous. `showing-vs-doing-grid.png` (two-column do | show, with observer posterior). Toggle in Widget C.
- **Legibility vs predictability (Dragan et al. 2013):** `legible-vs-efficient.png` (two-column) — efficient reach is ambiguous early; legible reach **veers early** toward the true goal. Two inferences in opposite directions (goal→traj vs traj→goal) — the same axis as ToM.
- **Reward as communication (Ho et al. 2015):** reward as a **signal**, not just a reinforcer — *and this is the paper the GardenPath assignment comes from*; the Week-8 `af` feedback loop was the "communication" reading misfiring.
- **CIRL / assistance games (Hadfield-Menell et al. 2016):** value alignment as a cooperative game; **efficient expert demonstration is provably suboptimal** — you should deviate to teach. **Reduces to a POMDP** whose hidden state is the human's reward (callback to Block 5; the unifying frame made concrete). Pedagogical sampling (Shafto/Goodman) as the communication generalization.
- **GenJAX cell:** score two trajectories (efficient vs legible) by the **observer posterior** each induces (reuses `genjax_goal_inference`) — the legible one wins.
- **Poll 4** (commit-before-reveal): "You want to show a friend which of two exits to take. Walk the **shortest** path, or **exaggerate** toward it?" → **Exaggerate** (legible) — the efficient path is ambiguous; Widget C shows the observer's posterior commit earlier under the legible path.

### Block 7 — IRL at scale & alignment + LLM Theory of Mind (22 min)
- **IRL methods — sibling build-up (~6 min):** **MaxEnt IRL** (Ziebart 2008; soft-optimal demonstrator `P(τ)∝exp(reward)` — *the same softmax as inverse planning*) → **GAIL** (Ho & Ermon 2016; GAN imitation, skips the reward) → **AIRL** (Fu et al. 2018; recover a transferable reward). `irl-methods-timeline.png`. **Honesty note:** IRL is underconstrained — recovered reward = one explanation among many (callback to Block 2 ill-posedness).
- **Machine ToM — ToMnet (Rabinowitz et al. 2018, ~3 min):** a meta-learned observer net that predicts agents' behavior/false beliefs from behavior alone. `amortized-vs-bayesian-tom.png` (two-column): ToMnet = **learned/amortized** ToM vs Baker = **explicit Bayesian inversion** — same inverse problem, two ways.
- **IRL → alignment (~4 min):** **RLHF & DPO are preference-based IRL** — fit a reward model `r_θ(x,y)` to human preferences, freeze it, optimize the policy (RLHF/PPO); DPO folds the reward *into* the policy. **Callback to Week-8 reward hacking** — the GardenPath positive cycle is the same bug at frontier scale. CIRL/assistance games as the alignment frame. Seeds Weeks 11–13.
- **GenJAX cell:** `genjax_reward_from_prefs.py` — a Bradley–Terry preference model recovering a reward from pairwise preferences; the RLHF/DPO ↔ IRL link in ~12 lines.
- **LLM Theory of Mind — the contested capstone (~6 min; lean skeptical — instructor's call):** present the debate but **land skeptical**. Lead with the capability results (Kosinski 2024 — GPT-4 ~75%, 6-year-old level; Strachan 2024 — at/above human on false belief/irony/hinting; Street 2024 — higher-order), then **dismantle them**: Ullman 2023 (trivial, belief-preserving perturbations flip success to failure), the Strachan faux-pas result (apparent wins are response bias / hyperconservatism, not inference), Pang 2025 (Morgan's Canon; training-data contamination can't be ruled out). `llm-tom-debate.png`. **Bottom-line slide:** *behavioral pass ≠ mechanism — the positive results are real but fragile; current evidence does not show LLMs have human-like ToM.*
- **Poll 3** (commit-before-discuss): "GPT-4 passes ~75% of false-belief vignettes — a 6-year-old's level. Does it **have** a theory of mind?" → **Contested** — passes many vignettes, fails minimal perturbations; behavioral pass ≠ mechanism. *Source: adapts SP25 IRL quiz Q1 (ToM functionalism) to the modern debate.*

### Block 8 — Close + Week 10 bridge (5 min)
- Recap the **five beats** (goal → ToM → belief → teaching → alignment) as one inversion applied to richer hidden variables.
- Reminders: ★ proposal Jun 28; reflection before Friday; RL + MC due Jul 10.
- **Week 10 bridge:** we've been inferring *discrete* hidden causes (goals, beliefs); next week — **Bayesian nonparametrics**, inferring *how many* causes there are when you don't know in advance.

---

## Per-block visual budget (audit checklist before "lecture-ready")

| Block | Figure(s) | Two-column | Build-up |
|---|---|---|---|
| 1 Welcome | `inverse-vs-forward`★ | forward \| inverse | — |
| 2 Goal inference | `bayes-inversion`, `goal-inference-posterior`, `ill-posed-inversion` + Widget A/D | (forward\|inverse reprise) | inversion: policy→likelihood→prior→posterior |
| 3 Noisy rationality | `softmax-rationality` | — | softmax across β |
| 4 ToM = IRL | `tom-as-irl` | — | — |
| 5 POMDPs | `food-truck-btom`★, `tiger-belief-update`★, `pomdp-to-belief-mdp` + Widget B | — | Tiger belief 0.5→0.85→0.97 |
| 6 Teaching | `showing-vs-doing-grid`, `legible-vs-efficient`★ + Widget C | do \| show; efficient \| legible | — |
| 7 Modern | `irl-methods-timeline`, `amortized-vs-bayesian-tom`, `llm-tom-debate` | ToMnet \| Bayesian | MaxEnt→GAIL→AIRL |

---

## Interactive widget specifications (4 — vanilla JS + canvas, clone `../week08_sdt_mdp_rl/widgets/qlearning-gridworld.html`; each gets a static `*-fallback.png`; dual-purpose: deck iframe + textbook iframe)

1. **`goal-inference.html` (Widget A — Block 2, Ch 23).** Gridworld (reuse GardenPath geometry) with 2–3 candidate goal markers; an agent steps under a softmax-optimal policy; a **live posterior bar chart over goals** updates each step; a **freeze/scrub** control (Baker "where's it headed?") and a **β (rationality) slider** + **trajectory-length** to show identifiability. *Steal from agentmodels.org Ch 4 (likelihood = forward softmax) + REINFORCEjs rendering + Seeing-Theory morph animation.*
2. **`pomdp-belief.html` (Widget B — Block 5, Ch 24).** The **Tiger** belief tracker: two bars `[P(left),P(right)]` starting 0.5/0.5; buttons *Listen→hear-left / hear-right / Open-left / Open-right / Reset*; each listen reweights by 0.85/0.15 and renormalizes (animate 0.5→0.85→0.97); overlay the **α-vector PWLC value lines** with the optimal-action region shaded so students see the belief cross the open threshold. *(~30 lines of Bayes; the gridworld-belief variant uses per-cell opacity / contracting particle cloud — optional.)*
3. **`showing-vs-doing.html` (Widget C — Block 6, Ch 24).** Same start, two candidate goals; toggle **Efficient (doing)** ↔ **Legible (showing)** trajectory; a dot animates the selected path and a **live P(goal) bar** responds — legible commits early, efficient stays ~50/50 until late. *Geometry from Dragan; gridworld + colors (blue agent/yellow goal/red hazards) from Ho et al. 2016.*
4. **`reward-recovery.html` (Widget D — Block 2/7, Ch 23).** Feed observed GardenPath trajectories; show **side-by-side heatmaps** (observed/visitation → recovered reward → optional ground truth) with a **"#demonstrations" slider** that sharpens recovery. *MaxEnt-IRL heatmap convention; REINFORCEjs value-as-color rendering.*

---

## GenJAX code plan (lecture walkthrough + tutorial) — *as much runnable GenJAX as possible*

Goal (professor ask): every beat that *can* carry runnable GenJAX does — short cells in the deck the instructor can walk through live (à la Week-8's `genjax_chibany_mdp.py` section), and the full treatment interwoven in the textbook chapters. All verified to run (genjax 0.10.3 + jax 0.5.3, CPU); cores folded into `make_figures.py`, the deck code-slides, and the chapters. The through-line: **the latent we condition on observations to infer IS "which MDP we're in"** — the GenJAX makes that hidden variable explicit.

| Module | Beat / Ch | Status — what the GenJAX shows (verified numbers) |
|---|---|---|
| **`genjax_goal_inference.py`** ★ | 2–4 / Ch 23 | ✅ **built & verified.** Invert the Week-8 MDP: per-goal softmax policy + `@gen` trajectory model + posterior over goals via `assess`. *P(right)=0.54; freeze-frame 0.37→0.47→0.50→0.54; β-sweep flat (0.33) → sharp (0.72)* — the β-sweep also covers Block-3 rationality (no separate module needed). |
| **`genjax_tiger_pomdp.py`** ★ | 5 / Ch 24 | ✅ **built & verified.** Tiger belief update as Bayesian conditioning (`assess`). *belief 0.5→0.85→0.9698→0.9945; E[open-right] −6.50 (1 growl) → +6.68 (2 growls)* — the Poll-2 reveal in arithmetic. Widget B backbone. |
| **`genjax_legible_teaching.py`** | 6 / Ch 24 | ✅ **built & verified.** Score efficient vs legible paths by the observer posterior (reuses goal-inference). *legible 0.613 vs efficient 0.500 at step 1 — both optimal-length.* Widget C backbone. |
| **`genjax_reward_from_prefs.py`** | 7 / Ch 25 | ✅ **built & verified.** Bradley–Terry reward modeling = preference-based IRL (RLHF/DPO). *recovers A>B>C, reward +1.36/0/−1.36 from 90 prefs; identifiable only up to a constant — IRL's ill-posedness.* |
| reward recovery (continuous) | 2 / Ch 23 | ⏳ extend `goal_inference` with a continuous-reward latent → Widget D (during figures/chapter). |
| `genjax_btom_belief.py` (stretch) | 5 / Ch 24 | ⏳ optional joint belief+desire inference (food-truck flavor) — add during Ch-24 authoring if it earns its place. |

Deck integration: each backbone gets a short, runnable, **bilingual-captioned** code slide (syntax-highlighted, ≤ ~15 visible lines) the instructor can open and run; the full validated versions live in the textbook chapters (with `<!-- validate: -->` directives + `*.ja.md` siblings). Heavy compute stays **numpy-first with optional JAX** per [[genjax-perstep-vs-vectorized-perf]].

---

## Polls (bilingual; options as a bullet list in **one** `.fragment` wrapping paired lang divs; paired-lang reveal line; record provenance in speaker notes)

| # | Block | Prompt → reveal | Source |
|---|---|---|---|
| 1 | 2 | "Which is **NOT** an example of inverse RL?" (4 options) → **learning an optimal policy by interacting in an MDP** (that's *forward* RL). | SP25 IRL quiz Q2 (`gb593d…`) |
| 2 | 5 | "You hear **one** growl from the left. Open the right door, or **listen again**?" → **Listen again** — 1 growl → b=0.85, E[open-right]=**−6.50** (worse than −1 listen); 2 growls → b=0.97, E=**+6.68** → open. | Authored (Tiger, verified) |
| 4 | 6 | "Show a friend which of two exits to take — walk the **shortest** path or **exaggerate** toward it?" → **Exaggerate** (legible). | Authored (legibility / Widget C) |
| 3 | 7 | "GPT-4 passes ~75% of false-belief vignettes (6-year-old level). Does it **have** a theory of mind?" → **Contested** — passes vignettes, fails minimal perturbations; behavioral pass ≠ mechanism. | SP25 IRL quiz Q1 (ToM functionalism), modernized |

(Numbered by block order; Poll 3 lands last, in Block 7.) Translate all options to JA — SP25 quiz items are English-only.

---

## Textbook chapter map (T3 series; next free weight after Ch 20–22 → **23/24/25**; notebook_guide=99, glossary=100)

> ⚠️ **The deck was reordered/refined after this outline was written.** For the FINAL lecture spine, the verified numbers, and the chapter mapping the chapters should follow, read **`TEXTBOOK_HANDOFF.md`** in this directory — it is the source of truth for textbook adaptation. The table below is updated to match it. Key change: **IRL methods / reward recovery now come BEFORE teaching** ("Recover → Teach → Align"), so Ch 23 pairs goal inference with reward recovery and Ch 24 pairs belief inference with teaching.

| Chapter | `textbook/content/intro2/…` | Covers (final spine) | GenJAX | Widgets embedded |
|---|---|---|---|---|
| **23 — Inverse RL: recovering the objective** | `23_inverse_rl_goal_inference.md` | goal inference as inverse planning (Bayes-rule anatomy, softmax, ill-posedness) **+ IRL methods at scale** (MaxEnt → GAIL → AIRL); reward recovery is goal inference's continuation. **Attribution: Baker & Tenenbaum**, reviewed by Jara-Ettinger 2019 | invert the Week-8 MDP → posterior over goals (`genjax_goal_inference.py`); Bradley-Terry reward-from-prefs as a cross-link | Widget A + Widget D |
| **24 — POMDPs, belief inference & teaching** | `24_pomdps_belief_inference.md` | belief `b(s)=P(s\|history)`, Tiger, α-vectors, the **decision-walk** build-up; then **teaching** — showing-vs-doing, legibility (Dragan), CIRL (the flip) | `genjax_tiger_pomdp.py` (belief update); `genjax_legible_teaching.py` | Widget B + Widget C |
| **25 — Modern RL / world models / alignment** | `25_modern_rl_world_models.md` | RLHF/DPO **explained then coded** (Bradley-Terry = preference-based IRL); ToMnet; **LLM-ToM debate, taught skeptically**; + world models (MuZero/Dreamer — the deferred Week-8 chapter, now that POMDPs land). **numpy-first, optional-JAX** per [[genjax-perstep-vs-vectorized-perf]] | `genjax_reward_from_prefs.py`; numpy-first MCTS/world-model | (reuse Widgets A/B as cross-links) |

Every-time cross-refs on publish: Colab links in `notebook_guide.md` (×3), glossary terms + chapter `*Glossary:*` lines in `glossary.md`, `- T3:` lines in `PLAN.md` "Textbook Chapters", regenerate `docs/index.html` via `python3 docs/_build.py`.

---

## Contingencies
- **Behind schedule at the break:** compress Block 7 to the IRL→alignment slide + the LLM-ToM bottom-line + Poll 3 (drop the method timeline detail); Block 3 folds into Block 2; Block 6 drops Dragan to a name-drop. Block 2 (inversion build) and Block 5 (Tiger) are protected.
- **A widget fails to load:** fall back to its static PNG (`goal-inference-posterior`, `tiger-belief-update`, `legible-vs-efficient` / `showing-vs-doing-grid`, `reward-recovery-heatmap`); every poll works against the static figure.
- **POMDP runs long:** drop the solver-taxonomy slide and the belief-MDP α-vector formalism to a name-drop; keep the food-truck motivation + Tiger belief build-up + Poll 2.
- **A student raises "but the agent had wrong/partial info" in Block 2/3:** that's the free lead-in to Block 5 — acknowledge and defer ("hold that — it's the next beat").

---

## TODOs spawned by this outline
- [ ] **GenJAX backbones (verified, runnable):** `genjax_goal_inference.py` (★ + reward-recovery extension), `genjax_tiger_pomdp.py` (★), `genjax_softmax_rationality.py`, `genjax_reward_from_prefs.py`, stretch `genjax_btom_belief.py`. Fold cores into `make_figures.py`, the deck code-slides, and Ch 23–25. (Supersedes the throwaway `/tmp/wk9_verify.py`.)
- [ ] Copy `../week08_sdt_mdp_rl/week8-styles.html` → `week9-styles.html`; **commit it**.
- [ ] `make_figures.py` — generate the 15 figures above; reuse Week-8 `gardenpath.png` + `chibany-mdp-diagram.png`.
- [ ] Build `week9-slides.qmd` (theme line, `include-in-header: week9-styles.html`, EN/JA divs, KaTeX notation lock-in, 4 polls, 5 agenda recaps, 4 widget iframes + PNG fallbacks, `resources:` for the widgets).
- [ ] Build the 4 widgets (clone `qlearning-gridworld.html` scaffolding).
- [ ] Author JA translations for every concept slide + poll (translate the 2 SP25 quiz items).
- [ ] Author textbook Ch 23/24/25 (switch to `textbook/CLAUDE.md` conventions: date frontmatter, `validate_code_blocks.py`, `*.ja.md` siblings, GenJAX cells, glossary/notebook cross-refs).
- [ ] Run the RevealJS fill audit (`scripts/audit_slide_fill.js --threshold 75`) + **student iterative review (clarity-agent pass, 2–3 personas — confirmed with the professor)** → record in PLAN.md.
- [ ] Update `course/quizzes/README.md` (Week 9 maps to "Monte Carlo Estimation"; the IRL quiz is mislabeled Week 11 — reconcile) and root `TODO.md` (close the deferred Modern-RL chapter item).
- [ ] Update `PLAN.md`: Status (→ SP26 rebuilt), Textbook Chapters (T3 23/24/25), GenJAX Integration, Contemporary ML Notes.
