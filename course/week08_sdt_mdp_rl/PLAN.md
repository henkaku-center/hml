# Week 8 (Jun 19): SDT + MDPs + RL

## Topics
- Statistical decision theory (loss/risk, Bayes vs. minimax, loss→estimator)
- Markov decision processes (states/actions/transitions/reward/discount/policy; value iteration)
- Reinforcement learning (Q-learning, reward shaping & positive cycles, simulation-based RL)

## SP25 Content
- **Slides:** Week08_StatDecisionTheoryAndMDP.pptx (+ PDF) — *mined, not ported* (see below)
- **Transcript:** Week08_SDTAndMDPTranscript.docx
- **Wiki pages:** statistical-decision-theory-and-markov-decision-processes.html
- **Quiz:** Monte Carlo Estimation (computational Markov-chain items — not a fit for conceptual polls, so SP26 polls are authored)

## Textbook Chapters

<!-- Card links: order-robust NAME form `T3: <chapter-name>` (stable-name = slug minus NN_, _→spaces). -->
- T3: statistical decision theory — `intro2/20_statistical_decision_theory.md` (loss/risk, Bayes vs minimax, loss→estimator, one-and-done decisions)
- T3: markov decision processes — `intro2/21_markov_decision_processes.md` (MDPs, the Bellman equation, value iteration, the γ-flip, planning by simulation)
- T3: q learning — `intro2/22_q_learning.md` (model-free Q-learning, reward shaping & positive cycles, Dyna + MCTS, simulation-based RL)

Each chapter interweaves runnable GenJAX and interactive widgets (`decision-loss-explorer`, `mdp-value-iteration`, `mdp-rollout-simulator`, the ported `qlearning-gridworld`, `mcts-stepper-chibany`, `mcts-tictactoe`). A fourth chapter — **modern RL / world models** (MuZero, Dreamer, deep RL, RLHF) — is deferred to after the Week 9 POMDP material (see root `TODO.md`).

## GenJAX Integration
None in the lecture. The **RL assignment** GenJAX port is a post-lecture workstream (below).

## Contemporary ML Notes
Block 8 (modernization tail): simulation-based RL (Dyna→MCTS→AlphaZero→MuZero→Dreamer); deep-RL milestones; **reward hacking → RLHF** (callback to the lecture's own positive-cycle demo); **dopamine = TD error** + model-based/model-free dual systems (tees up the Daw, Niv & Dayan 2005 required reading). Plants the Weeks 11–13 alignment thread.

## Status
**SP26 rebuilt & lecture-ready (pending final rehearsal).** Three-act redesign: DECIDE (decision theory) → PLAN a *known* MDP (the Chibany wellbeing example + value iteration) → LEARN an *unknown* MDP (GardenPath + Q-learning) → SIMULATE (simulation-based RL). The two changes the professor asked for are done: (1) the disliked pre-GardenPath MDP (SP25's "final project / party" example) is replaced by the **Chibany wellbeing MDP** (Junk +1 / Trying −2 / Healthy +5; verified chokepoint, γ-flip ≈ 0.64); (2) value iteration is **applied back** to that MDP (SP25 never solved its own example). GardenPath is kept and is now the **interactive widget**.

### SP26 artifacts (this directory)
- `week8-shared-outline.md` — SOURCE OF TRUTH (timing, per-block key points, figure inventory, verified example numbers, polls, contingencies).
- `week8-slides.qmd` — bilingual Quarto RevealJS deck (52 slides). Theme `[dark, ../../sds-reveal/sds.scss]`; `include-in-header: week8-styles.html`.
- `week8-styles.html` — fill-the-slide layout + poll/figure/two-column CSS + eager-image script (copied from Week 7; break-cat selector → week8). **Must stay committed.**
- `make_figures.py` — 14 figures → `images/` (matplotlib, transparent dark theme). Cores mirror the verified MDP/GardenPath logic.
- `widgets/qlearning-gridworld.html` — interactive Q-learning on GardenPath. **Single-step the 6 algorithm stages with a live current-step indicator** (professor ask); reward-scheme toggle **rm / af / potential / human**; live Q-heatmap + policy arrows + cycle-detection verdict; "Train ▸▸" fast-forward. **Human mode** (professor ask): you are the teacher, giving 👍/➖/👎 feedback per move — the Ho et al. teaching setup. Verified: rm → learns the path; af → a **+20/lap positive cycle** (the SP25 action-feedback table, vindicating "how easy it is to get positive net cycles"); potential-based shaping → recovered. Fallback PNG: `images/qlearning-widget-fallback.png`.

### Visual QA
Fill audit run via Playwright (the repo's `scripts/audit_slide_fill.js` puppeteer path is stale on this machine; equivalent clip+fill measurement done in-browser at the deck's true 960×540). Result: **0 clipped slides; all content slides ~89% fill** (only the widget-iframe slide reads low, expected — the iframe is the background). Spot-checked the four riskiest two-column/figure slides visually (loss→estimator, Chibany MDP diagram, γ-sweep, potential-shaping) — figures, KaTeX, and column balance all render correctly. *Known publish-time item:* the theme's `sds_wordmark.png` 404s on a bare local render (cosmetic branding; handled by the docs build — confirm at publish, same as Week 7).

### Clarity review (durable record — 3 student-persona agents, 2026-06-14)
Spawned in parallel: a non-math design student, a CS-background student, and an easily-overwhelmed/returning student. All three independently reconstructed the three-act arc correctly (the spine held). Convergent issues found and **fixed in the qmd**:
- **ε / ε-greedy never defined** (all 3) → defined at first use; the Q-update is now a **6-step** list (matching the widget stepper) whose step 1 is "select $a$ by ε-greedy (explore w.p. ε)".
- **$\delta_t$ used on the dopamine slide but never named** (all 3) → the TD error is named $\delta$ on the update slide; the dopamine slide now says "the TD error $\delta_t$ from Q-learning."
- **Chibany→GardenPath bridge missing** ("why two examples?") (students 1 & 3) → added a bridging sentence ("Chibany was easy: we *knew* his matrices… now an agent that doesn't know its world").
- **"telescopes to zero" is wrong for γ<1** (CS student — a real math error; the widget runs γ=0.95) → replaced with the correct **policy-invariance** statement (shaping adds the same constant $-\Phi(s)$ to every action, so the best action is unchanged).
- **R(s) vs R(s,a)** inconsistency + loss/reward duality → one dim note on the MDP-definition slide.
- **$\mathbb{E}$, $\arg\max$, $\sum$, prime $'$** unglossed and the notation lock-in came late → glossed at first use (E on the risk slide) and the notation slide now lists the math shorthand.
- **value iteration "converges" unjustified** → dim caption ("γ-contraction → unique fixed point $v^*$").
- **horizon $T$ collided with transition $T$** → horizon renamed $H$.
- Plus: MAP reminder, $v$-vs-$V$ convention note, γ≈0.64 "for these probabilities", GardenPath determinism/terminal note, the "three acts/four bullets" title fixed, and the **"garden path" name** cashed in (the agent is led *down the garden path*). Re-rendered + re-audited: still **0 clips**.
- *Deferred (minor, instructor-narrated):* showing the +20 loop arithmetic on the static slide; the deterministic vs. expectation subtlety in the Q-target; Poll-2's answer crosses a section break by design.

### Post-review fixes (2026-06-14, from the professor's review)
- **Vertical space.** The fill-the-slide `justify-content: space-between` pinned a single content block to the bottom (dead void under the title), and most text slides were tagged `.smaller` (densest tier) despite sparse content → tiny + empty. Fixed: content now **centers** as a balanced group (`justify-content: center` + gap in `week8-styles.html`), and the sparse text slides were **re-tiered** (`.smaller` → `.midbig`/`.bigger`/`.biggest`, calibrated per-slide against clip). Deck now averages **~79% fill, 0 clips** (was ~40% voids). All 14 figures are referenced 1:1 (only the widget *fallback* PNG is unused, by design).
- **Widget — the "af works too well" trap.** The prominent "goals reached" counter counted goals hit during **ε-greedy exploration** (high under af), making action-feedback *look* successful even though the learned greedy policy loops. Numerically confirmed (af: Q-learning greedy reaches goal **1/40** trials; at (3,2) the agent prefers diving back to the garden, Q=52.8 > 20). Fixed: the **greedy-policy verdict is now a prominent banner** ("✗ the learned policy LOOPS — +20/lap, never reaching the goal"), the exploration counter is demoted + relabeled "goals hit *while exploring*", and a clarifier line states "still hits 🏠 by luck while exploring — but the policy it LEARNED just loops." Deck's "What to watch" slide updated to point at the verdict, not the counter.
- **Widget — arrow legend.** Added a legend distinguishing the three arrow types (gray = greedy policy per cell; thick colored route = path from start, green reaches 🏠 / red loops; yellow = the move being taken).
- **Admin slide.** Now an **active-deadlines list** (Generalization due Jun 19; proposal Jun 28; MC Jul 10) with the **RL assignment releasing next week** (not Jun 19).

### Shipped & published (2026-06-15) — professor signed off on the content
Deck + widget rendered and **published live**: `build-site.yml` CI succeeded for the pushed commit (`1031a4b`), so the styled deck + widget iframe serve on GitHub Pages. This session's refinements (these **supersede the stale numbers above** where they conflict):
- **af reward scheme made robust (corrects the "+20/lap, 1/40" note above).** The SP25 action-feedback table's positive cycle ran *through the garden* and only dominated after heavy training — at the ~2000-step demo it was a **coin-flip** (greedy reached the goal ~30/60), which read as "af works." Replaced with **on-path backtracking = +4 (`WEAK`), forward = +10** (a human positive-feedback bias): the cat now paces the *path* collecting praise — a **+14/lap** cycle that fails **0/40 at every training length**. Widget AND the static `feedback-rm-vs-af.png` updated to match (loop on the path, not the garden); `make_figures.py` and the widget keep identical af tables.
- **Widget defaults to human-teacher mode** (professor ask); in human mode the loops/reaches **verdict is hidden behind a reveal toggle** (discover-then-reveal). Auto modes show it immediately.
- **Chibany MDP diagram redrawn** as one complete graph — **all 14 transitions**, both actions, **probability-weighted** (thick/bright = dominant, thin/faint = rare), self-loops, each state's out-arrows sum to 1. Action colors blue=Invest / purple=Indulge, distinct from state colors.
- **Figure fixes:** `simulation-based-rl` (caption + arrow occlusion), `ho-modelbased-worse` (legend moved above the plot). Now **16 generated figures** (+ widget fallback). Deck grew to **57 slide headers** (value-iteration by-hand walkthrough + the neuroscience split).
- **Neuroscience split:** the "An opening" slide → the RLHF-opening slide + a new **"RL in the brain"** slide (dopamine-TD figure now legible).
- **Break photo** swapped to `week8CatPhoto.heic` → converted to JPG (browsers can't render HEIC) at `images/break-cat-week8.jpg`.
- **Fill-audit script repaired** — `scripts/audit_slide_fill.js` now uses user-local `puppeteer-core@22` + system Chrome (was a stale hardcoded puppeteer path). Final deck: **0 genuine clips**.
- **Runnable GenJAX backbone** `genjax_chibany_mdp.py` (value iteration + MC simulation; verified genjax 0.10.3 / jax 0.5.3). **Textbook companion chapter** is the next deliverable — handoff at `TEXTBOOK_HANDOFF.md` (new session).

## TODOs
- [ ] Final rehearsal pass; verify Week-8 presenter in `readings_map.yml` (instructor-led by default; Schultz 1997 is the natural hand-off if one is added) and wire the Block-8 contingency.
- [x] **Published (2026-06-15, CI-verified live).** `build-site.yml` succeeded for the pushed commit; styled deck + widget iframe serve on GitHub Pages; `week8-styles.html` committed.
- [ ] Native-speaker proof of the JA translations.
- [ ] **Post-lecture:** refresh `course/assignments/rl/` to the plan-then-learn framing + add a GenJAX stencil (MDP env as a generative function for simulation-based rollouts; confirm framing). Author a textbook MDP/RL chapter.
- [ ] `course/quizzes/README.md` Week-8 mapping still says "Monte Carlo Estimation" — note the conceptual mismatch (polls are authored).
