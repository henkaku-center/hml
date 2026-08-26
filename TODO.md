# Human and Machine Learning SP26 — Consolidated TODOs

### SP25 Carryovers
- [ ] More student discussion/activities in early weeks (Weeks 1-4) *(partially addressed by SP26 lecture+check-ins format; revisit after running Weeks 1–2)*
- [ ] Fix MC importance sampling figure legend (Week 8 slides)
- [ ] Fix Bayes Net quiz wording (Week 7 quiz)
- [x] Modernize RL assignment (2026-06-20): rebuilt as Assignment 4 — GenJAX + Python + R stencils, shared `rl_gridworld.py` env+viz, diagnose-and-fix-reward-hacking core. *(Julia variant not pursued; superseded by the GenJAX port.)*

### SP26 New — Week 1
- [ ] Build SP26 Week 1 slide deck from `course/week01_intro_basic_bayes/PLAN.md` (SP25 `.pptx` files stay as reference) *(superseded by Week-2-onward triplet pattern; Week 1 stays on LECTURE_NOTES.md as-is)*
- [x] Week 1 PLAN.md and LECTURE_NOTES.md
- [x] SP26 grading scheme decided (see Week 1 PLAN.md)

### SP26 New — Week 2
- [x] Adopt APS per-week triplet pattern (shared-outline + build script + generated pptx/notes)
- [x] Week 2 shared outline: `course/week02_basic_bayes_cont/week2-shared-outline.md`
- [x] Week 2 build script + generated deck: `course/week02_basic_bayes_cont/build_slides_week2.py` → `slides/sp26/week2-slides.pptx`
- [x] Week 2 Chibany-narrative adaptation (bento scenario anchors Marr L1/L2/L3)
- [x] Week 2 PLAN.md updated with SP26 artifacts section
- [x] Port Week 2 to Quarto RevealJS (108 slides, KaTeX math, decktape PDF pipeline) — `course/week02_basic_bayes_cont/week2-slides.qmd`
- [x] Rewrite Block 4 around two-meals joint + new independence/dependence sub-block (2026-04-23)
- [ ] Verify GenJAX conditioning API (Block 4 Cell 3) against textbook T2 Ch 4 before class
- [ ] **Tighten Block 7 before class:** cut the "Why Gaussian × Gaussian = Gaussian (derivation sketch)" 4-slide sub-block; state the conjugacy result + plug in numbers, defer the derivation to Week 3 / T3 Ch 4 homework. Frees ~8–10 min.
- [ ] **Trim Block 5 redundancy:** collapse EV build-up from 4 → 2 slides and Bernoulli from 3 → 1 slide (students have seen E[X] in T1 Ch 6). Frees ~5 min.
- [ ] **Trim Block 6 redundancy:** cut the 6-slide "Bayes with continuous likelihoods" sub-block to a 2-slide mini-demo; let Block 7's single-variable Gaussian-Gaussian be the payoff. Frees ~5 min.
- [ ] Add one "What's changing" contrast slide before Block 7 (three-row table: prior = number / number / distribution over parameter) to make the conceptual leap explicit.
- [x] Add one audience-poll prompt per major block ("before I compute: higher or lower?") so students commit before each reveal. *(done 2026-04-24; three polls added — posterior definition after Notation lock-in, Derek's density before PMF→PDF 4/4, Jamal's conjugacy before the Gaussian × Gaussian derivation. All sourced from SP25 quiz bank per the new CLAUDE.md standing rule.)*
- [ ] Reposition the "Two changes since Week 1" slide to the end, under admin — keep the cold open on Chibany.
- [ ] Acknowledge A/B vs. H/D notation shift on the Block 4 setup slide (one dim line suffices).
- [ ] After Week 2 class: transcribe paper-presentation signups into `course/readings_map.yml` `presenter:` fields

### SP26 New — Week 4
- [x] Build SP26 Week 4 artifacts — `week4-shared-outline.md` + `week4-slides.qmd` (61-slide Quarto RevealJS deck), done 2026-05-20. Generalization framework + size principle + rectangle game + number game all before the break; Shohei's presentation (~25 min) after; No Free Lunch + hierarchical-Bayes close. Opens with an 8-min Clusters-assignment walkthrough.
- [x] Hierarchical Bayes authored two ways (teaser / full block) — instructor selects live by timing; both fenced in the qmd.
- [ ] Write the hierarchical `bento_day()` GenJAX exercise (referenced on Week 4 slide B6)
- [ ] Native-speaker proof of Week 4 JA translations (machine-authored)
- [ ] Confirm Week 5 presenter against `readings_map.yml` before the Week 4 class — Week 4's "next week" slide intentionally names none

### SP26 New — Week 6 (Markov Chains + Networks)
- [x] **Shipped + linked to the site (2026-06-03, commit d518ea5).** Final deck is 64 slides (grew from the Chibany-consistency rework, the Abbott censoring + IRT-result additions, the explicit-L slide, and the AD network-stats slide). CI auto-rebuilds + deploys; `docs/slides/week06.html` linked from the schedule. **Fixed `docs/_build.py`** along the way: stale week→dir map (skipped a dropped "week 6", expected week 13) corrected to a 1:1 map for dirs 1-12 — this had mislabeled topics for dirs 7-12 too; and fixed a clobber bug where each week's build `rmtree`'d the shared `docs/slides/images/` (now merges, restoring Weeks 2-5 figures).
- [x] Plan SP26 Week 6 — `week6-shared-outline.md` written 2026-06-01 (full instructor-led lecture, 1 break, 3 polls, no presentation). Spine: Markov chain → random walk on a network → memory search as a random walk (Abbott 2012). Stationary dist via intuition + power iteration (PCA/SVD aside cut). Chibany opens; canonical examples (card shuffle, H/T FSA, animal semantic net) carry mechanics. Block 7 (Zemla foraging/MVT + Alzheimer's networks) is optional/fenced like Week 4's hier-Bayes Variant B. Source decks to mine: SP25 Week 6 deck + `MCMCPCulturalEvoCOSMOS2025.pptx` + `AusterweilShizuokaUJan2026.pptx`.
- [x] Build `week6-slides.qmd` from the shared-outline — done 2026-06-01. 52-slide Quarto deck, 8 blocks + fenced optional Block 7, 3 polls, EN/JA throughout, multi-slide build-ups (H/T run, power-iteration, 4-slide walk trace), two-column figure layouts. Passed RevealJS fill audit (0 OVERFLOW) + a student-perspective clarity review (verdict MOSTLY CLEAR, comprehension check passed; all flagged gaps fixed).
- [x] Make figures via `make_figures.py` — Chibany bento chain, H/T FSA, power-iteration bars (SP25 3×3 matrix), animal-net walk trace ×4, fluency communities, ER vs scale-free, PageRank, card shuffle.
- [x] Extract real research-data panels (MVT foraging, control-vs-AD networks) from the Shizuoka deck for the optional Block 7.
- [ ] Native-speaker proof of Week 6 JA translations once authored.
- [x] Corrected Week 6 PLAN quiz line: was "Bayes Net" (the Week-5 quiz), now "Markov chains and networks" (`gefe6f0bdb37a0476e57d5ebb0d3ffcb4`). The "fix Bayes Net quiz wording" carryover belongs to Week 5.

### SP26 New — Week 7 (Monte Carlo &amp; MCMC)
- [x] **Built (2026-06-06).** Plan + `week7-shared-outline.md` + `week7-slides.qmd` + custom interactive viz + all figures. Spine: Monte Carlo → importance sampling → particle filtering → MCMC (MH + Gibbs) → two payoffs (MCMC with People; a sampler for the Kemp 2007 beta-binomial hierarchy, no DPMM). Clean Week 6 hand-off (does NOT re-teach Markov chains; opens by paying off Week 6's hospital/LLN teaser). Mined the SP25 Week 7 deck + the COSMOS MCMCP deck. Fill audit clean (overflow flags resolved/verified; remaining flags are poll fragments + centered section-breaks). Renders to `week7-slides.html` (+ `.pptx`); JA toggle verified.
- [x] **Custom interactive viz** `interactive/mcmc-gmm.html` (vanilla JS + Canvas, single file, offline): Gibbs + MH on a 4-blob 2-D GMM, proposal-σ slider, trajectory + trace + histogram panels, live acceptance-ratio + modes-visited readouts, auto-seed on load. Teaches proposal-variance → mixing → acceptance; the trapped-between-modes demo reproduces (σ≈0.4 → acc≈0.6 but 1/4 modes). 5-demo teaching script in `interactive/README.md`.
- [x] **GenJAX bridge authored both ways** (LIGHT recurring callouts + summary slide; HEAVY fenced deep-dive that assembles an MH kernel from `simulate`/`importance`/`assess`/`update`). Against genjax 0.10.3; names v1.0.10 `hmc()`/`chain()` as upstream-only. Decide at rehearsal which to show.
- [x] Hospital-problem poll added (Poll 1 reveal; reuses the Week 6 bilingual prompt; pays off the Week 6 teaser).
- [x] **Linked Week 7 to the site** (2026-06-10) — committed the deck (qmd + 28 figures + interactive widget + shared-outline) so CI rebuilds `docs/slides/week07.html` and the schedule card.
- [ ] Verify the Week 7 presenter in `readings_map.yml` (Sanborn & Griffiths / Vul et al. were SP25 presentations); convert MCMCP block to a bridge + handoff if confirmed.
- [ ] Native-speaker proof of Week 7 JA translations.
- [x] **Authored the MC / Kemp-sampler assignment (2026-06-10).** `course/assignments/mc/`: `mc_approx.tex`+PDF (P1 MC/IS, P2 hybrid Gibbs-θ + MH on φ/log-κ with a weak proper κ prior, P3 ESS with the IS-vs-MC puzzle), GenJAX/Python/R stencils (all verified to run), README wired (due Fri Jul 10 8pm). Deck edited to align (bridge slide + ESS slide). Verified answer-keys gitignored in `.solution_reference/`.
- [ ] **Fix two stencil bugs in the MC assignment before it runs again** (found 2026-08-26 by
  the audit-grading pass over the SP26 submissions; neither was charged to any student, and
  the "never deduct for following an instruction you gave them" rule was applied).
  1. **Recorded-sweeps undercount by 500.** `course/assignments/mc/mc_approx.ipynb`
     (GenJAX), lines 206/214 — **verified 2026-08-26**: the scaffold's comment says "run T = 3000 sweeps (after a few
     hundred burn-in)" and its worked example does exactly that — but the handout's Problem
     2(d) asks for "T = 3000 **recorded** sweeps (after discarding burn-in)". Following the
     stencil literally yields 2500 recorded sweeps. Fix: 3000 total → discard a few hundred →
     3000 *recorded*, and make the comment and worked example agree with the handout.
  2. **Acceptance rate counts burn-in in the denominator.** `mc_approx.ipynb` line 227 (and 179)
     and `mc_approx_python.ipynb` line 155 — **verified 2026-08-26**: both report acceptance as the mean of the
     accepted-flags array over *all* recorded sweeps including burn-in, rather than
     post-burn-in only. Fix the denominator in both scaffolds (and check the R stencil for the
     same pattern — it was not covered by this cohort's submissions).
  **Both copies need the edit:** `docs/assignments/mc/` is byte-identical to
  `course/assignments/mc/`, so fixing only the course source leaves the published stencil
  wrong. Check the R stencil for the same acceptance-rate pattern — no submission in this
  cohort used it, so it is unverified either way.

  Why this matters beyond the arithmetic: every student working from a scaffold inherits its
  error identically, so three students making "the same mistake" is the signal to check the
  scaffold rather than the students. One submission corrected the default on its own (ran
  T=3500 to get 3000 recorded) and that correction was credited as genuinely earned.
- [ ] **Follow-on:** expand the T2 GenJAX textbook tutorial (Ch 0–4, 6 today; no MCMC/SMC) to cover MCMC + the Kemp sampler (per chapter-ship checklist: also notebook_guide, glossary, HML homepage card).
- [ ] `course/quizzes/README.md` Week-7 row maps to the *Bayes Net* quiz (predates the SP26 re-sequence) while the polls mine *Monte Carlo Estimation* + *Markov chains and networks* — reconcile.

### SP26 New — Week 8 (SDT + MDPs + RL)
- [x] **Built (2026-06-14).** Three-act redesign — DECIDE (decision theory) → PLAN a *known* MDP (new **Chibany wellbeing** example: Junk +1 / Trying −2 / Healthy +5; verified chokepoint, value iteration applied *back* to it, γ-flip ≈0.64) → LEARN an *unknown* MDP (GardenPath + Q-learning) → SIMULATE (simulation-based RL + reward-hacking/RLHF + dopamine/dual-systems → tees up the Daw 2005 reading). Replaces SP25's disliked pre-GardenPath "final-project/party" MDP; keeps GardenPath. `week8-shared-outline.md` + `week8-slides.qmd` (52 slides, EN/JA) + `week8-styles.html` + `make_figures.py` (14 figs). Verified example numbers in the outline.
- [x] **Interactive Q-learning widget** `widgets/qlearning-gridworld.html` (vanilla JS + Canvas): **single-step the 6 algorithm stages with a live current-step indicator** (prof ask), reward-scheme toggle **rm / af / potential / human**, live Q-heatmap + policy arrows + cycle-detection verdict, "Train ▸▸" fast-forward. **Human mode** (prof ask): you are the teacher (👍/➖/👎 per move). Verified: rm → path; **af → +20/lap positive cycle** (the SP25 action-feedback table) ; potential → recovered. Fallback PNG saved.
- [x] **Visual QA:** Playwright clip+fill audit (the repo's puppeteer audit path is stale on this box) — **0 clips, ~89% fill** on all content slides; 4 riskiest slides spot-checked visually.
- [x] **Clarity review** (3 student personas) → fixes recorded in `course/week08_sdt_mdp_rl/PLAN.md`: defined ε-greedy/δ, added the Chibany→GardenPath bridge, **corrected the "telescopes to zero" potential-shaping claim** (→ policy-invariance), glossed E/Σ/argmax, etc. Re-audited clean.
- [x] **Refined & published (2026-06-15; prof signed off on content).** af scheme made robust (**corrects the "+20/lap" note above**): on-path backtrack +4 / forward +10 → **+14/lap** cycle, fails **0/40 at all training lengths** (old SP25 table was a coin-flip at the ~2000-step demo); widget defaults to **human-teacher mode** + loops/reaches verdict hidden behind a **reveal toggle**; Chibany MDP redrawn as one **complete probability-weighted graph** (all 14 transitions); figure fixes (sim-RL caption/arrows, ho-modelbased legend); neuroscience slide split ("RL in the brain"); break photo → `week8CatPhoto` (HEIC→JPG); **fill-audit script repaired** (`puppeteer-core@22` + system Chrome). Now **16 figs / 57 slide headers**; runnable `genjax_chibany_mdp.py` added.
- [ ] Final rehearsal; verify Week-8 presenter in `readings_map.yml` (instructor-led default; Schultz 1997 is the natural hand-off).
- [x] **Published (2026-06-15, CI-verified).** `build-site.yml` succeeded for the pushed commit; styled deck + widget iframe serve on GitHub Pages.
- [ ] Native-speaker proof of Week 8 JA translations.
- [ ] **Post-lecture:** refresh `course/assignments/rl/` to the plan-then-learn framing + add a GenJAX stencil (MDP env as a generative function for simulation-based rollouts).
- [x] **Textbook MDP/RL chapters authored (2026-06-15).** Three interwoven-GenJAX chapters in `textbook/content/intro2/`: `20_statistical_decision_theory.md` (+ one-and-done), `21_markov_decision_processes.md`, `22_q_learning.md` (+ MCTS capstone). Six interactive widgets (decision-loss, value-iteration, rollout-sim, ported GardenPath Q-learning, MCTS stepper, MCTS tic-tac-toe); all code blocks pass `validate_code_blocks.py`; glossary + notebook_guide + homepage card wired; student-critique loops run per chapter.
- [x] **Deferred textbook chapter — modern RL / world models** — DONE: authored as `intro2/25_modern_rl_world_models.md` in the Week-9 cycle (RLHF/DPO as preference-based IRL, ToMnet, world models — MuZero/Dreamer, the skeptical LLM-ToM debate). Being revised in the Week-9 **post-delivery rebuild** (GAN-free GAIL, a proper theory-of-mind definition, Ho et al. 2021 recursive POMDP, Bradley-Terry/σ gloss) — see `/home/jausterw/.claude/plans/i-just-finished-giving-giggly-swing.md`.
- [ ] Author companion `.ipynb` notebooks with full prose (current `notebooks/2{0,1,2}_*.ipynb` are code-only extractions from the chapters).

### SP26 New — Syllabus & Admin
- [x] Draft SP26 syllabus source (`course/syllabus/SP26_syllabus.md`) and publish to the site
- [x] Update grading to reflect 6 students / 12 sessions: reflections 15%→12.5% (8-of-13 → 6-of-12); new paper-presentation line at 7.5%; participation folded in
- [x] Add Paper presentations section to syllabus (rubric + Griffiths framing questions)
- [x] Port SP25 project guidelines to SP26 (`course/syllabus/SP26_project_guidelines.md` + `docs/project.html`); pinned dates: proposal Sun Jun 28 8:00 PM, presentation Fri Jul 17, paper Fri Jul 24 8:00 PM. Standardized all deadline times to 8:00 PM. *(done 2026-05-29)*
- [ ] Fill in late-policy details (placeholder in SP26_syllabus.md)
- [ ] Pick office hours, update syllabus, rebuild site
- [x] Reconcile 13 course/week directories vs. 12 actual sessions — done: merged old week4/5/6 (generalization/hier-bayes/causal) into new weeks 4 (generalization + hier-bayes) and 5 (bayes nets + causal); renumbered weeks 7–13 down to 6–12. All 12 directories now match the 12-session calendar.

### SP26 New — Website (docs/)
- [x] Phase 1: generator + templates + syllabus/assignments pages live (`docs/_build.py`)
- [ ] Phase 2: per-week detail pages rendered from PLAN.md (rolled out week-by-week as sessions approach)
- [x] Phase 3 (scaffolding): `course/readings_map.yml` created with schema + Weeks 1–2 populated. Remaining weeks are stubs.
- [x] Phase 3 (content): populate `readings_map.yml` Weeks 3–12 required readings + presentation candidates *(done 2026-04-23; SP25 backbone + 2023–2026 modern additions on Weeks 10–12)*
- [ ] Phase 3 (website): extend `docs/_build.py` to render `docs/readings/index.html` from `course/readings_map.yml` (per-week sections with citation, links, presentation candidates, presenter)
- [ ] Phase 3 (hosting): decide between private Google Drive vs. in-repo PDFs for the reading assets (see `docs/README-password-protected-readings.md`)
- [ ] Phase 3 (auth): install staticrypt, pick initial SP26 password, pin to Slack `#announcements`, wire into the build
- [ ] Phase 3 (Slack): create `#paper-signups` and `#weekly-discussion` channels before Week 3; post per-week threads in `#paper-signups` after Week 2 class
- [ ] Phase 4 (optional): GitHub Actions to auto-build on push
- [ ] Fill in `presenter:` fields in `course/readings_map.yml` after Slack signups close (Fri May 15)
- [x] **Slide EN↔JA toggle infrastructure.** Built (2026-04-24). `sds-reveal/lang-toggle.{css,js}` + Quarto include wiring. Press `L` to switch; localStorage persists. Authoring pattern documented in CLAUDE.md. Week 2 has 3 slides wrapped as a minimal example.
- [x] **Auto-scaffold EN↔JA toggle for every future week deck.** Done 2026-04-24 via project-level `_quarto.yml`: new `course/week*/week*-slides.qmd` files pick up `lang-toggle.css` + `lang-toggle.js` automatically, no per-file frontmatter needed.
- [x] **Week 2 full JA retrofit.** Done 2026-04-24. All 110 slides translated: concept intros, build-ups, numerical variations, agendas, titles, section breaks, break slide, polls, admin. ~447 lang-divs / inline spans. Translations are machine-authored and need a native-speaker pass before Week 2 rerun.
- [ ] **Extend EN↔JA to the course *site* (home, syllabus, assignments, game plan, guidelines).** The slide toggle only covers deck HTML. Site pages are separate Jinja templates and would need their own markup + toggle wiring.
- [ ] **JA translations for Weeks 3-12 slides** as those decks are authored — the infrastructure is auto-wired, just use the `.lang-en` / `.lang-ja` div pattern.
- [ ] **Native-speaker proof of Week 2 JA translations.** ALL 110 slides are now machine-translated. Technical vocabulary likely correct (事後確率, 尤度, 独立, 同時分布, 条件付き分布, 周辺化) but prose phrasings need a native-speaker polish pass before the first lecture where JA matters. The high-risk slides are the ones with idiomatic English (Marr L3 deep-NN disclaimer, the "shift in what's hidden" pivot slide, and any slide with "students coordinate to avoid two tonkatsu" type narrative prose).
- [ ] **Week 1 EN/JA retrofit.** Blocked on infrastructure: Week 1 uses Marp, not Quarto. Pandoc-style `::: {.lang-en}` fenced divs don't work in Marp. Options: (a) port week01.md to a .qmd (biggest effort, but unifies the stack); (b) rewrite Week 1's lang wrappers as raw HTML `<div class="lang-en">...</div>` and add the CSS/JS to Marp's custom theme. Week 1 already happened (Apr 17), so lower priority — but needed for future re-runs of the course. Recommendation: do (a) as part of any future Week 1 refresh.

### SP26 New — Slide infrastructure
- [x] **Fix section-break centering regression in `sds-reveal/sds.scss`** (2026-06-02). The `.section-break` flex-centering rule was scoped to `section.title-slide.section-break`, but Quarto only adds `.title-slide` to LEVEL-1 (`#`) headings — the standard LEVEL-2 (`## Title {.section-break}`) form gets no `.title-slide`, so the rule silently missed and section-break titles jammed against the top edge of the yellow frame (empty-looking giant box). Rescoped to plain `div.reveal div.slides section.section-break` (matches both heading levels). Week 4's HTML predates the regression so it looked fine; newly-rendered decks did not.
- [x] **APS `lecture-plans` audit re-sync (2026-06-03).** After adding CAPTION-MISALIGN + RUNON-CAPTION checks to HML's `audit_slide_fill.js`, re-copied it to APS and re-applied the APS patches (REPO path, week3 DECK/OUT_DIR defaults, `center-name` framed class); documented both checks in APS `CLAUDE.md`. Smoke-tested on APS week3. The audit script + its QA documentation are now in sync across both repos.
- [x] **APS `lecture-plans` cross-repo sync (2026-06-02).** (a) Audit script: copied HML's `audit_slide_fill.js` (393 lines) over APS's stale 208-line version — APS was missing the entire two-column checks AND the new EMPTY-FRAME/JAMMED-TITLE checks; preserved APS's `REPO`/`DECK`/`OUT_DIR` defaults + `center-name` framed class; smoke-tested on APS week3 (114 slides, 3 legit FLOATING flags, 0 false positives). (b) APS `CLAUDE.md`: documented the Puppeteer fill audit + all failure modes (APS keeps its QA method in CLAUDE.md; there is no APS `SLIDE_VISUAL_QA.md`). (c) SCSS: APS's `sds.scss` already independently carries a `section.section-break:not(.title-slide)` rule that fixes the same section-break bug — functionally equivalent to HML's consolidated `section.section-break` rule, so left as-is (forcing byte-identity would risk breaking APS's working version).
- [ ] Check **Week 2's pinned `sds-reveal-week2.scss`** — if it carries the buggy `.title-slide.section-break`-only scoping (no `:not(.title-slide)` or plain `section.section-break` rule), its `##`-level section breaks jam their titles. Week 2 is frozen/pinned, so verify before its next re-run.
- [x] **Extend the slide fill audit** (`scripts/audit_slide_fill.js`, 2026-06-02) to catch two defect classes it previously skipped: **EMPTY-FRAME** (a section-break/framed slide with no title and no content — e.g. a bare `# {.section-break}` empty yellow box; the audit used to blanket-`SKIP-FRAMED` these) and **JAMMED-TITLE** (a framed title pinned to the top edge instead of centered). Documented both in `SLIDE_VISUAL_QA.md`. Regression-tested: the broken deck flags 7 bare-`#` empties + jammed titles; the fixed deck flags neither.

- [x] **Mirror the new `sds.scss` rules to lecture-plans** — done 2026-07-16 as part of the layout-scheme v2 sync: `sds-reveal/sds.scss` and the new `sds-reveal/fig-size.js` were copied verbatim (byte-identical), which carried the four older additive rules (`.v-center`, `.v-spread`, `.agenda .done`, `.photo-break`) along with the v2 figure-first rules.
- [x] **Layout-scheme v2 (2026-07-16) — figures can no longer be silently crushed; bullets and layout variety are audited.** The rewrite the professor requested after tiny-figure/prose-wall/mono-layout defects recurred across Weeks 9–12 despite clean audits. (a) **Theme (`sds-reveal/sds.scss`):** standalone figures on content slides are now the flex-GROW element with hard min-height floors (150px default, 300px `.big-figure`, 340px `.bih`) and `object-fit: contain` everywhere — a figure can't shrink below legibility or distort; over-long text now fails loudly as OVERFLOW instead. `.columns` rows are grow-only (`flex: 1 0 auto` — a shrinkable row let cards spill invisibly), `.cmp-cols` promoted from per-deck copies, new `.statement` hero archetype, new `.fig-inline` opt-out, poll option boxes widened to 86%. (b) **Shared `sds-reveal/fig-size.js`** (eager-load + r-stretch strip, guarded to v2-theme decks only so pinned Week 2 is safe) wired project-wide via `_quarto.yml` — new decks need zero per-deck figure CSS/JS. (c) **Audit (`scripts/audit_slide_fill.js`):** new TINY-FIGURE (largest figure < 24% of stage, contain-aware), SQUISHED-FIGURE (aspect distortion), PROSE-WALL (4+-line paragraph) flags, a per-deck layout-mix histogram with MONO-LAYOUT advisory, the `scrollHeight>clientHeight` clip test implemented (was only documented), and measurement moved to the deck's EXACT logical size (960×540) — the enlarged 1244×700 viewport let zoom rounding hide a real clip (Week 12 slide 7). (d) **Docs:** `SLIDE_VISUAL_QA.md` design-system section rewritten as "The layout scheme (v2)" with the Rule-0 archetype decision table + bullet discipline; CLAUDE.md lecture-authoring sections updated to match. (e) **Validated on Week 12** (see its PLAN.md): 10 initial flags → 0, all figures 47–63% of stage. Audit + theme mirrored to `lecture-plans` (APS defaults preserved in its audit copy).
- [ ] **Write a Quarto-qmd → pptx converter.** The Quarto deck is now the canonical slide source (week2-slides.qmd, etc.); the hand-written `build_slides_weekN.py` pptx track has diverged and is no longer maintained. Need a single-entry tool that reads the .qmd and emits a python-pptx Office deck preserving speaker notes, math (KaTeX → equation/image), the yellow-frame theme, and section breaks, so the pptx artifact can be regenerated from the canonical source instead of hand-edited in parallel. Until this exists, ignore the per-week `build_slides_weekN.py` scripts.

### SP26 New — Textbook & GenJAX
- [ ] Map textbook homework readings to each week's PLAN.md
- [x] GenJAX setup pointer for students (Week 2 homework — Tutorial 2 Ch 0-1, referenced in Week 1 PLAN.md)
- [x] Clusters assignment — GenJAX stencil: `course/assignments/clusters/clusters.ipynb`
- [x] Generalization assignment — three stencils (GenJAX/Python/R) + PDF: `course/assignments/generalization/`, done 2026-05-27
- [ ] **Separate planning session:** scope GenJAX ports for MC / RL (depth, textbook chapter mapping, solution-notebook sources, sequencing by due-week)
- [ ] Port MC assignment to GenJAX *(blocked on scoping session above)*
- [x] Port RL assignment to GenJAX (2026-06-20): `course/assignments/rl/` — `rl_genjax.ipynb` (env as a `@gen` model) + `rl_python.ipynb` + `rl_nosoln.Rmd`, shared `rl_gridworld.py`, solutions in `solutions/rl/`, rl.tex rebuilt (Assignment 4). Maps to textbook intro2/21–22.
- [ ] **Write Tutorial 3 Bayesian-Generalization chapter** — see `textbook/CHIBANY_T3_GENERALIZATION_PLAN.md`. Week 4 has no textbook reading; generalization.pdf + course/assignments/README.md currently link to a forthcoming URL.
- [ ] **Write Tutorial 3 Hierarchical-Bayes chapter** — see `textbook/CHIBANY_T3_GENERALIZATION_PLAN.md`. Also Week 4. Decision on numbering (insert vs. append, relative to `CHIBANY_T3_CH7-10_PLAN.md`) deferred until the writing agent picks up either plan.
- [ ] Write Tutorial 3 Bayes-nets / causal / info-theory chapters — see `textbook/CHIBANY_T3_CH7-10_PLAN.md` (Week 5). *(Ch 8–11 are now BUILT per that plan; the file header records it.)*
- [ ] **Write Tutorial 3 Markov-chains chapters (Ch 13–15) — see `textbook/CHIBANY_T3_MARKOV_NETWORKS_PLAN.md`** (Week 6, plan written 2026-06-03, committed to probintro `95a1cde`). Ch 13 Markov chains / 14 random walks on networks / 15 memory search (Abbott 2012 censored walk). NOT yet built — start a fresh session with the briefing at the top of that plan. Source: the shipped Week 6 lecture (`course/week06_markov_chains_networks/`).
- [ ] Plan which new textbook chapters to write during semester
- [ ] Add GenJAX exercises to Weeks 6, 8, 11

### SP26 New — Contemporary Content
- [ ] Review Weeks 11-13 for opportunities to include recent ML developments (LLMs, foundation models, RLHF, alignment)
- [ ] Update readings list with post-2023 papers where relevant
- [ ] Consider adding content on: scaling laws, in-context learning, mechanistic interpretability, multimodal models
- [ ] Week 12 (Deep NNs): consider transformer architecture, attention mechanisms
- [ ] Week 13 (Ethics): update with recent AI safety/alignment developments

### Next-year (SP27) revisions — defer
- [ ] **Move the final-project proposal deadline earlier.** SP26 landed it on Sun Jun 28 (one week after the Generalization assignment, Week 9 of 12) to avoid moving a date students may already have planned around. That leaves only ~3 weeks between proposal feedback and the presentation/paper — tight for a 50%-weight capstone. For SP27, set the proposal in the first half of the term (target ~Week 4–5) so students get feedback with real runway to execute. Identified 2026-05-29 while porting the project guidelines to SP26.
- [ ] **Generalization assignment: add a reflective follow-up to Problem 5.** After computing the NFL collapse, ask the student to look back at their *own* hypothesis space and answer: which features of the properties they chose made the model generalize well, and could they predict (without running code) which animal pairs would generalize? Converts the assignment from "compute these things" to "introspect on what you built." Identified 2026-05-27 in conversation while solving the SP26 stencils end-to-end — deferred to SP27 so we keep momentum on tutorials + lectures for SP26.
- [ ] **Reconsider the hand-rolled MCMC assignment's slot given where ML has moved.** The MC assignment (Problem 2: hand-assemble a Gibbs+MH sampler for the Kemp Beta-Binomial hierarchy) is the most "classical" artifact in the course — modern ML does inference variationally/amortized, and nobody hand-writes an accept ratio in 2026. It currently earns its place via (a) the cognitive-modeling thread (MCMCP, sampling accounts of cognition — still current) and (b) inference literacy ("assemble inference from primitives and reason about whether it's correct"). The Week 7 deck now frames the modern connection explicitly (diffusion = learned reverse-MCMC; RLHF/best-of-N = sample+reweight). Open question for SP27: is hand-rolled MCMC still the best use of this slot, or should some of it yield to more transformer/RLHF/alignment time (Weeks 11–13 territory)? Not a clear cut — the sampling-cognition link is genuinely active research — but worth a deliberate decision rather than inheriting SP26 by default. Identified 2026-06-10 while reviewing the Week 7 deck against the assignment.
- [ ] **Add a bias-variance dilemma section (restore/modernize the SP25 treatment), with a better home than it had.** SP25 covered the bias-variance tradeoff but folded it into the **Bayesian nonparametrics** lecture (SP26 Week 12) — where it lands awkwardly and late; nonparametrics is a strange first place for a student to meet over/underfitting. For a future year (likely SP27, not necessarily SP26), give it a deliberate slot: bias-variance is the natural complement to **generalization / model complexity**, so an earlier home fits better — e.g. alongside **Week 4 (generalization + hierarchical Bayes)** or as a dedicated model-selection / overfitting beat — and then *call back* to it when Week 12 introduces complexity that grows with the data (the nonparametric payoff: let the data choose the capacity). Worth tying to the contemporary thread too (double descent / overparameterized models complicate the classic U-curve story). Starting point: pull the SP25 bias-variance material from the archived Week 12 (Bayesian Nonparametrics) slides in `archive/canvas_export_sp25/`. Identified 2026-06-24 in conversation while building Week 9 — flagged as a course-structure gap, not Week-9 work.
