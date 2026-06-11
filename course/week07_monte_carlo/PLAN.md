# Week 7 (Jun 12): Monte Carlo &amp; MCMC

## Topics
- Monte Carlo estimation
- Importance sampling
- Particle filtering
- MCMC (Metropolis–Hastings + Gibbs)
- MCMC with People (MCMCP)
- A sampler for the Kemp (2007) hierarchical beta-binomial model

## SP25 Content
- **Slides:** Week07_MCApprox(1)_PTT.pptx (+ PDF) — mined for the basics arc (MC / IS / particle filter / MCMC intro), not ported wholesale.
- **Wiki pages:** introduction-to-monte-carlo-approximation.html, importance-sampling.html, introduction-to-particle-filtering.html, intro-to-markov-chain-monte-carlo.html
- **Quiz:** Markov chains and networks (+ Monte Carlo Estimation for polls)
- **Also mined:** COSMOS 2025 MCMCP deck (`MCMCPCulturalEvoCOSMOS2025.pptx`, repo root) — MH animation, Gibbs trace, Human-MCMC, Sanborn & Griffiths stick animals.

## Textbook Chapters
- **Assign T3 Ch 12** (Hierarchical Bayes / approximate inference) — students carry it from the Week 4 hand-off; Week 7 is where it pays off and gets sharpened from importance sampling to MCMC.

<!-- Card links: order-robust NAME form `T3: <chapter-name>` (stable-name = slug minus NN_, _→spaces). -->
- T3: monte carlo — `intro2/16_monte_carlo.md` (Monte Carlo estimator, rejection/importance sampling, effective sample size — supports Assignment 3 Problems 1 & 3)
- T3: particle filtering — `intro2/17_particle_filtering.md` (sequential importance sampling, weight→resample→propagate, particles as a process model)
- T3: markov chain monte carlo — `intro2/18_markov_chain_monte_carlo.md` (Metropolis–Hastings, Gibbs, mixing/burn-in — supports the Assignment 3 sampler mechanics)
- T3: sampling the mind — `intro2/19_sampling_the_mind.md` (MCMC with People + a Gibbs/Metropolis sampler for the Kemp hierarchical Beta-Binomial)

## GenJAX Integration
- **In the lecture (built):** classical-method ⇄ GenJAX bridge, authored **both ways** — recurring "in GenJAX:" callouts on the MC/IS/MH slides + a one-slide summary (LIGHT), and a fenced dedicated deep-dive block (HEAVY) that assembles an MH kernel from `simulate`/`importance`/`assess`/`update`. Authored against genjax 0.10.3; names v1.0.10 `hmc()`/`chain()` as upstream-only.
- **Follow-on (needs creation):** the GenJAX sampling exercise = the Kemp sampler (the lecture gives the recipe; the assignment is the artifact). Expand the T2 GenJAX tutorial (currently Ch 0–4, 6; no MCMC/SMC) to cover MCMC + the Kemp sampler — per the "slides first, then tutorial" workflow.

## Contemporary ML Notes
None this week.

## Status
**Lecture-ready (SP26 built 2026-06-06; expanded 2026-06-09).** Quarto RevealJS deck + custom interactive viz + all figures done; fill audit clean (remaining flags are intentional: the iframe-placeholder demo slide, centered section-breaks, and borderline code-beside-text columns that read fine — visually verified). 2026-06-09 additions: a **particle-filter worked example** (1-D tracking: 3 step figures weight→resample→propagate + setup slide) plus a **GenJAX particle-filter** code + real-output slide pair (1000-particle bootstrap filter tracking a noisy track; verified output); the **MCMC demo is now click-to-set-state** (click the trajectory plot to teleport the chain there and continue — verified via headless click test); and a full-deck visual-layout review pass (4 batched Explore agents) that surfaced + fixed a mid-slide dead band on the Metropolis–Hastings slide. 2026-06-11: added a second admin slide (Block 1) announcing the **final project proposal** (due Sun Jun 28, 8:00 PM — four sections, categories, pre-deadline chat, project.html link; bilingual, verified no-clip in EN and JA via Playwright).

## SP26 artifacts (built this session)
- `week7-shared-outline.md` — source of truth (timing table, per-block detail, polls, GenJAX both-ways, Kemp recipe, viz placement).
- `week7-slides.qmd` — Quarto RevealJS, `theme: [dark, ../../sds-reveal/sds.scss]`, bilingual EN/JA, KaTeX, 4 polls, MH + Kemp sibling-slide build-ups, both GenJAX treatments, viz iframe + PDF-fallback slide. Renders to `week7-slides.html` (+ `.pptx`).
- `widgets/mcmc-gmm.html` — custom single-file (vanilla JS + Canvas, no build, offline) Gibbs + MH on a 4-blob 2-D GMM: proposal-σ slider, trajectory + trace + histogram panels, live acceptance-ratio + modes-visited readouts, auto-seed on load, and **click-to-set-state** (click the trajectory plot → the chain teleports there and continues; manual teleports are excluded from the histogram/mode tallies so they don't bias the estimate). **Verified:** the trapped-between-modes demo reproduces (σ≈0.4 → acceptance ≈0.6 but modes visited 1/4); Gibbs reaches all 4 modes; the click handler teleports + continues with no JS errors (headless puppeteer test).
- `make_figures.py` → `images/` — `mc-die-convergence`, `mc-pi-darts` (π via two uniform draws, 4-stage convergence), `mh-anim-1..6` (dark-theme MH animation), `gibbs-trace`, `kemp-hierarchy-plate`, `gibbs-metropolis-recipe`, `is-weight-variance`, `particle-filter`, `pf-step1-weight`/`pf-step2-resample`/`pf-step3-propagate` (the 1-D worked-example walkthrough), `mcmc-gmm-fallback` (PDF still).
- `images/cosmos_src/` — extracted COSMOS rasters: Sanborn stick animals + 2-D scatter + 9-D stimulus, Human-MCMC cartoon, subjective-randomness ladders.

## TODOs
- [ ] **Verify the Week 7 presenter** in `readings_map.yml` before class (Sanborn & Griffiths / Vul et al. were SP25 presentations). If confirmed, convert MCMCP Block 8 to a 2-min bridge + handoff (see outline Contingencies).
- [ ] Native-speaker proof of the Week 7 JA translations (machine-authored, as Weeks 2–6).
- [ ] Decide at rehearsal: show the GenJAX **deep-dive (7b)** or the **summary (7)** — both authored; the deep-dive is the on-ramp to the assignment.
- [ ] **Follow-on (separate session):** author the GenJAX sampling exercise / Kemp assignment stencil into `assignments/`; expand the T2 GenJAX textbook tutorial to cover MCMC + the Kemp sampler (per the chapter-ship checklist, also update notebook_guide, glossary, HML homepage card).
- [ ] `course/quizzes/README.md` Week-7 row maps to the *Bayes Net* quiz (predates the SP26 re-sequence) while the polls mine *Monte Carlo Estimation* + *Markov chains and networks* — flag/reconcile the mismatch.
- [x] ~~Add the hospital-problem poll~~ — done (Poll 1 reveal, reuses the Week 6 bilingual prompt; pays off the Week 6 teaser).
- [x] ~~Fix importance sampling figure~~ — superseded; new `is-weight-variance.png` (good q vs bad q, ESS) authored for SP26.
