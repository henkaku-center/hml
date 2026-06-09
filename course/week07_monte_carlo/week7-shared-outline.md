# Week 7: Shared Outline
## Friday, June 12, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Topic:** Approximation / sampling techniques — Monte Carlo, importance sampling, particle filtering, MCMC (Metropolis–Hastings + Gibbs), MCMC-with-People (MCMCP)
**Required reading (pre-class):** Sanborn & Griffiths (2007/2008), *Markov chain Monte Carlo with people* (NeurIPS). **Verify the presenter in `readings_map.yml` before class** — Sanborn & Griffiths and Vul et al. (2009) were SP25 presentations; if a presenter is confirmed, Block 8 converts to a 2-min bridge + handoff (see Contingencies).
**Textbook reading:** T3 Ch 12 (Hierarchical Bayes / approximate inference) — students have this from the Week 4 hand-off; Week 7 is where it pays off and gets sharpened from importance sampling to MCMC.
**Students:** ~6

---

## Key Design Decision

**This week reverses Week 6's arrow and cashes out three weeks of scaffolding.** Week 6 *found* the stationary distribution of a chain it was handed; Week 7 *picks a target* (a posterior) and *designs* a sampler that hits it. The session climbs a toolkit ladder of increasing power, then applies it twice:

1. **Monte Carlo** — estimate an expectation by averaging samples (pays off Week 6's hospital/LLN teaser: *this* is what Monte Carlo was).
2. **Importance sampling** — sample the wrong distribution, reweight (the textbook's "blunt tool" for the Kemp hierarchy).
3. **Particle filtering** — sequential importance sampling: yesterday's posterior is today's prior.
4. **MCMC (MH + Gibbs)** — design a chain whose stationary distribution *is* the target (the sharp tool; reprises Week 6's π as a named callback).
5. **Payoff A — MCMC with People** (Sanborn & Griffiths): humans *are* the accept step; the chain converges to the prior in their heads.
6. **Payoff B — a sampler for the Kemp/Perfors/Tenenbaum (2007) beta-binomial hierarchy** (Gibbs the conjugate θᵢ, Metropolis the non-conjugate hyperparameters) — the recipe students will implement.

Two cross-cutting threads run the whole deck:
- A **GenJAX / probabilistic-computing bridge**, taught **two ways** (author both, pick at rehearsal): a recurring "in GenJAX:" right-column callout on the MC/IS/MH slides + a one-slide summary (LIGHT, always runs), **and** a dedicated deep-dive block (HEAVY, fenced).
- The **custom interactive Gibbs+MH viz** (`interactive/mcmc-gmm.html`) as the centerpiece of the MCMC block.

**Confirmed design choices (planning session 2026-06-06):**

- **Clean hand-off from Week 6 — DO NOT re-teach Markov chains.** Week 6 covered the Markov property, transition matrix, stationary distribution (power iteration, ergodicity, πP=π), and card-shuffle mixing, and wrote the MC→MCMC bridge explicitly; it closed with the hospital/LLN poll **tagged as the Monte-Carlo teaser that pays off here.** Week 7 **opens by paying off** that poll, and at the MCMC block reprises "stationary distribution" as a **one-line named callback**, not a re-derivation.
- **Scope = methods + Kemp, MCMCP compressed; particle filtering kept (brief).** Full MC/IS/MCMC coverage + the viz + the **protected** Kemp recipe. MCMCP runs compressed (~6 min). Particle filtering is a **short core block** (~10 min), not fenced. *(Prof. note: slide timing tends to be over-estimated — methods stay full and PF stays in.)*
- **GenJAX both ways.** Author the LIGHT recurring callouts + summary slide **and** the HEAVY fenced deep-dive block; decide which lands better at rehearsal.
- **Interactive viz = full custom build** (`interactive/mcmc-gmm.html`, done): MH + Gibbs on a 4-blob 2-D GMM, proposal-σ slider, trajectory + trace + histogram panels, live acceptance-ratio + modes-visited readouts, the 5-demo teaching script.
- **No DPMM.** The Kemp recipe stays at the two-level Beta-Binomial with *learned* (a,b) — exactly the Week 4 Variant-B model, now given its sampler. Reparametrize (a,b) as mean φ=a/(a+b) and concentration κ=a+b.

**Authoring style** follows Week 4/Week 6: Quarto RevealJS, `theme: [dark, ../../sds-reveal/sds.scss]` (five-tier, in frontmatter per CLAUDE.md), EN/JA `.lang-en`/`.lang-ja` divs on every concept slide, KaTeX, sibling-slide build-ups, polls as bullet lists in **one** `.fragment` wrapping paired lang divs. Define every new term at first use (Monte Carlo estimator, indicator 𝟙[·], proposal, importance weight, acceptance ratio, mixing, mean/concentration reparametrization).

**"Where we are" recap slides.** `{.agenda .dense}` at each block boundary, bilingual bullets, `.done`/`.highlight` on **both** lang spans per the CLAUDE.md agenda rule.

---

## Source material (what to mine)

| Source | Path | What to take |
|---|---|---|
| **SP25 Week 7 deck** (70 slides) | `slides/Week07_MCApprox.pdf` (+ `.pptx`) | The **basics skeleton** — Marr "why approximate → rational process models" opener; MC principle + die-roll + consistent/unbiased/asymptotically-normal; inverse-CDF; rejection (π-via-darts); importance sampling (overlap diagrams, weight variance = quality, likelihood weighting, **Nosofsky "exemplar models ARE importance samplers"**); SIS/particle filtering; the MCMC intro (MH + Gibbs). |
| **COSMOS MCMCP tutorial** (73 slides) | repo root `MCMCPCulturalEvoCOSMOS2025.pptx` | Polished MCMC + MCMCP figures and narrative (slide refs below). |
| **SP25 quizzes** | `archive/canvas_export_sp25/gdf7280…` (Monte Carlo Estimation) + `gefe6f0…` (Markov chains and networks) | Poll mining (see poll table). |

### Figures — already built/extracted (in `images/`)

**Made (matplotlib, dark theme, `make_figures.py`):**
- `mc-die-convergence.png` — running MC estimate of E[die] → 3.5 (LLN).
- `mc-pi-darts.png` — π-via-darts build-up n=10/100/1000/10⁴, inside/outside colored, π̂→3.14 (the canonical two-uniform-draws MC example).
- `mh-anim-1.png … mh-anim-6.png` — dark-theme recreation of the COSMOS MH animation: current point → propose → accept (A=1) → propose → accept (A=0.5) → reject, on a multimodal p(x). **Use as the sibling-slide build-up.**
- `gibbs-trace.png` — Gibbs axis-aligned (L-shaped) moves on correlated 2-D contours.
- `kemp-hierarchy-plate.png` — two-level plate (φ,κ)→(a,b)→θᵢ→(kᵢ,nᵢ).
- `gibbs-metropolis-recipe.png` — the Kemp sampler loop: Gibbs θ (green/easy) + Metropolis (φ,κ) (red/needs-MH).
- `is-weight-variance.png` — good q (ESS≈230/400) vs bad q (ESS≈6/400) with weight histograms.
- `mcmc-gmm-fallback.png` — static still of the interactive viz (trapped-modes Demo 4) for the PDF export.

**Extracted from COSMOS (`images/cosmos_src/`):**
- `sanborn_stick_prototypes.png`, `sanborn_2d_scatter.png`, `sanborn_9d_stimulus.png` — the MCMCP animal-shapes payoff (Sanborn & Griffiths 2007).
- `human_mcmc_cartoon.png` — the data↔hypothesis loop (COSMOS s31).
- `subj_random_ladder1.png`, `subj_random_ladder2.png` — subjective-randomness regularity ladders (optional MCMCP extension).

**Reuse:** the Week 6 hospital-poll slide (pull from `course/week06_…/week6-slides.qmd` git history) for Poll 1.

---

## Session Plan

| Time | Block | Min | What happens |
|------|-------|-----|--------------|
| 0:00 | **1. Welcome + "what *was* Monte Carlo?"** | 8 | Admin (1 slide). **Poll 1 REVEAL** of the Week 6 hospital poll → smaller hospital (LLN); name it: *that* was Monte Carlo. Marr "why approximate? → rational process models." |
| 0:08 | **2. Basic Monte Carlo** | 15 | MC estimator; die-roll convergence; **π-via-darts** (two uniform draws → indicator → π̂=4·in/total, 4-stage build-up); consistent/unbiased/asymptotically-normal; inverse-CDF + rejection. GenJAX callout: `simulate`+`vmap`. |
| 0:23 | **3. Importance sampling** | 15 | Sample wrong q, reweight; weight variance = quality (good/bad q); likelihood weighting w∝p(d\|h); Nosofsky exemplar bridge; the **"blunt tool"** for Kemp. GenJAX callout: `importance`→(trace, log_weight); `assess`; `smc.ImportanceK`. Poll 4 (optional). |
| 0:38 | **4. Particle filtering** | 10 | SIS: yesterday's posterior = today's prior; particle-filter algorithm (weight→resample→propagate); rational process models. GenJAX callout: SMC chained over observations. |
| 0:48 | **5. MCMC — design a chain to hit a chosen target** | 15 | One-line callback to Week 6's π. MH (propose + A=min(1,P(x')/P(x)); **normalizer cancels**) — `mh-anim-1..6` sibling slides. Gibbs (resample one coord, always accept). Two-column MH \| Gibbs. Poll 2. GenJAX callout: MH is *assembled* from `update`/`regenerate`+`assess`. |
| 1:03 | **6. Interactive viz: Gibbs + MH on a multimodal GMM** | 12 | **Centerpiece** (`interactive/mcmc-gmm.html`). Live 5-demo script: tiny σ (accept→1, stuck) / huge σ (accept→0, frozen) / just-right / **trapped-between-modes finale** / Gibbs reaches all modes. Poll 3 (chains disagree → hasn't mixed). |
| 1:15 | **Break** | 5 | |
| 1:20 | **7. Programmable inference: GenJAX (LIGHT — always runs)** | 6 | One summary slide (classical \| GenJAX two-column). Thesis: *PP gives you IS for free and hands you the scoring primitive to assemble MCMC.* |
| 1:26 | **7b. GenJAX deep-dive (HEAVY — fenced; show OR skip)** | 0–10 | Live API walk: build a model, call `importance`, inspect `(trace, log_weight)`, assemble an MH step from `assess`/`update`. Fenced `<!-- BLOCK 7b GENJAX-HEAVY -->`. |
| 1:36 | **8. Payoff A — MCMC with People (compressed)** | 6 | Humans *are* the accept step (COSMOS s31); learners sample from posterior → chain converges to prior P(h) (s33/34); Sanborn stick-animals recovery (s36–38). Fenced extension: subjective-randomness + music Gibbs. |
| 1:42 | **9. Payoff B — a sampler for the Kemp hierarchy (PROTECTED)** | 15 | Week-4 two-level Beta-Binomial → its sampler. **Gibbs** θᵢ~Beta(a+kᵢ, b+nᵢ−kᵢ) [conjugate, Week 3]. **Metropolis** on (φ,κ): log-uniform prior on κ, log-space random walk, accept by ∏ᵢ BetaBin(kᵢ\|nᵢ,a,b). 5-slide build-up. This is what students implement. |
| 1:57 | **10. Close + Week 8 bridge** | 3 | Recap the ladder; assign the GenJAX sampling exercise; preview Week 8 (SDT/MDP/RL). |
| 2:00 | End | | |

**Cut order under time pressure** (Block 6 viz and Block 9 Kemp never cut): (1) Block 7b heavy GenJAX (show the light summary instead); (2) MCMCP extensions (subjective-randomness/music Gibbs); (3) Poll 4 + IS optimal-IS aside; (4) compress particle filtering to one schematic slide.

---

### Block 1: Welcome + "what *was* Monte Carlo?" (8 min)

- Admin (1 slide): the MC programming assignment + GenJAX sampling exercise; pooled late days. No re-tour.
- **Pay off the Week 6 teaser** (the "show" happened last week). Reprise the hospital-poll slide verbatim (git history); students already committed → here it's **reveal-only**: the *smaller* hospital, small samples vary more (LLN). Payoff line: *"You were doing Monte Carlo — estimating a quantity by averaging samples, and more samples means a better estimate. Today that's the central tool."*
- **Marr framing (SP25 opener):** exact Bayesian inference is intractable; borrow good samplers from CS/statistics, then ask whether they're *psychological processes* → **rational process models** (Sanborn 2010; Shi 2010). Umbrella for both payoffs. *Define:* Monte Carlo.

### Block 2: Basic Monte Carlo (15 min)

- **MC estimator:** $\hat\mu_n = \frac{1}{n}\sum_i f(x_i)$, $x_i\sim P$. Die-roll → 3.5; `mc-die-convergence.png` is the visual LLN that closes the hospital poll.
- **π-via-darts — the canonical worked example (build-up spine of the block).** Draw two independent uniforms $x,y\sim\text{Uniform}[0,1]$; the dart is **inside** the quarter-circle iff $x^2+y^2\le 1$. Quarter-circle area $=\pi/4$ ⇒ $\hat\pi = 4\cdot\frac{\#\text{inside}}{\#\text{total}}$. This is $\mathbb{E}_{\text{Uniform}}[f]$ with $f(x,y)=\mathbb{1}[x^2+y^2\le 1]$. **Sibling slides** `mc-pi-darts.png` at n=10/100/1000/10⁴ (π̂→3.14). *Define:* **indicator** $\mathbb{1}[\cdot]$. Pre-loads rejection sampling (inside/outside = accept/reject).
- **Properties** one-per-line: consistent / unbiased / asymptotically-normal (dim definitions, no derivation).
- **"Can't always sample P":** inverse-CDF ($F^{-1}(u)$); rejection sampling of a posterior. **Two-column:** inverse-CDF \| rejection.
- **GenJAX callout** (right column): `trace = model.simulate(key, args)`; `vmap` over keys; `μ̂ = jnp.mean(vmap(...)(...))`; the π example as two uniform draws + an indicator mean.

### Block 3: Importance sampling (15 min)

- **Idea:** $\mathbb{E}_P[f] = \mathbb{E}_q[f\cdot w]$, $w=p/q$ (define **importance weight**); note the unnormalized / self-normalized case.
- **Weight variance = sampler quality** (`is-weight-variance.png`): good q (broad overlap, even weights, high ESS) vs bad q (one weight dominates, ESS≈6/400). **Two-column:** good q \| bad q.
- **Likelihood weighting:** use the prior as proposal ($q=p(h)$) ⇒ $w\propto p(d\mid h)$ — "sample from prior, weight by likelihood."
- **Nosofsky exemplar bridge** (course through-line): exemplar models *are* importance samplers when stored exemplars are hypothesis samples. One equivalence slide.
- **Kemp hook (1 line):** the textbook (T3 Ch12) infers (a,b) by IS over the closed-form Beta-Binomial marginal — a **"blunt tool"** (noisy, high weight variance). Sets up Block 9.
- **GenJAX callout:** `trace, log_weight = model.importance(key, constraint, args)` (prior = default proposal); `model.assess(choices, args)` for custom q; `smc.ImportanceK(Target(model, args, constraint), k_particles=N)`.
- **Poll 4 (optional):** prior/posterior barely overlap → a few huge weights, noisy estimate (= the "blunt tool").

### Block 4: Particle filtering (10 min)

- **SIS:** recomputing $P(h\mid d_1..d_n)$ each step is wasteful → **"yesterday's posterior is today's prior."** Repeated IS over a growing dataset = a **particle filter** (a.k.a. SMC / bootstrap filter / condensation).
- **Algorithm** (one slide, build-up): init M particles from prior, uniform weights; per datum multiply weight by $P(d_n\mid h)$, normalize, **resample** if degenerate. Final particles ≈ posterior. (Reuse the SP25 Bishop weight→resample→propagate schematic if it extracts; else a simple made schematic.)
- **Rational process models:** particle filters of categorization (Sanborn 2006), associative learning, changepoint detection, sentence processing — limited memory + order effects fall out. Ties back to the Marr opener.
- **GenJAX callout:** a particle filter = `smc.*` chained over observations.

### Block 5: MCMC — designing a chain to hit a chosen target (15 min)

- **One-line callback to Week 6:** *"Last week you found a chain's π by running it; now we pick the target P(x) and design a chain whose π is that target."* Reprise π (πP=π) in one dim caption.
- **MCMC defined:** sample target P(x) via a Markov chain with P(x) as its stationary distribution. Two schemes: **MH** and **Gibbs**.
- **Metropolis–Hastings — sibling-slide build-up** (`mh-anim-1..6`): init → propose $x'\sim Q$ (symmetric) → accept $A=\min(1, P(x')/P(x))$. Walk it: accept uphill (A=1) → accept with A=0.5 → reject. Define **proposal** Q and **acceptance ratio** A. Emphasize the **normalizer cancels in $P(x')/P(x)$** — why MCMC beats exact inference for posteriors.
- **Gibbs** (`gibbs-trace.png`): resample one coord at a time, $x_i^{(t+1)}\sim P(x_i\mid x_{-i})$, always accept. **Preview Kemp:** "θᵢ step is pure Gibbs (conjugate); (a,b) needs Metropolis."
- **Two-column:** MH (any target; propose + accept; needs only ratios) \| Gibbs (needs conditionals; always accepts; one coord).
- **Poll 2:** two starts, long run → same histogram (ergodic forgets its start = π) — *"…if it mixed,"* which the demo tests next.
- **GenJAX callout:** in 0.10.3 MH is **not** a black box — assemble from `update`/`regenerate`+`assess`; v1.0.10 `hmc()`/`chain()` name-drop.

### Block 6: Interactive viz — Gibbs + MH on a multimodal GMM (12 min)

- **Centerpiece** — embed `interactive/mcmc-gmm.html` (background iframe, `background-interactive="true"`). One slide lists the beats; the demo does the teaching. Run the README's 5-demo script:
  - tiny σ (≈0.05): acceptance ≈ 0.94 but **stuck in one mode** (slow random walk).
  - huge σ (≈4.0): acceptance ≈ 0.05, chain barely moves.
  - just-right σ (≈0.4–0.6): acceptance ≈ 0.5, explores its mode.
  - **trapped finale:** good σ runs forever but **modes-visited stays 1/4**; histogram fills only one peak — *good local acceptance ≠ good global mixing; why multimodal is hard, why MCMCP is subtle.*
  - Gibbs: acceptance n/a, reaches all 4 modes — the contrast.
- **Poll 3:** two MH runs disagree after 1,000 steps → the chain hasn't mixed / is stuck. Lands *after* the demo shows a stuck chain.

### Break (5 min) — after Block 6.

### Block 7: Programmable inference — GenJAX (LIGHT, 6 min, always runs)

- **One summary slide** (two-column *classical method* \| *GenJAX surface*): basic MC → `simulate`+`vmap`; IS → `importance`→(trace, log_weight) + `assess` + `smc.ImportanceK`; particle filter → SMC over observations; MCMC → assemble from `update`/`regenerate`+`assess` (0.10.3), `hmc()`/`chain()` upstream.
- **Thesis line:** *"Probabilistic programming gives you importance sampling for free and hands you the scoring primitive (`assess`) to assemble MCMC — exactly what you'll do for the Kemp model."* Hinge into Block 9.

### Block 7b: GenJAX deep-dive (HEAVY, 0–10 min, fenced)

*Fence `<!-- BLOCK 7b GENJAX-HEAVY -->`. At rehearsal: show 7b OR the 7 summary.*

- Live API walk against **genjax 0.10.3**: define a tiny `@gen` model; `trace = model.simulate(key, args)` (inspect `get_retval`/`get_score`); `trace, log_weight = model.importance(key, constraint, args)` (the default-proposal IS); then **assemble an MH step**: propose via `update`/`regenerate`, score with `assess`, form the ratio, accept/reject. Doubles as the on-ramp to the Kemp GenJAX exercise.

### Block 8: Payoff A — MCMC with People (6 min, compressible)

- **Show-before-tell:** "which looks more like a cat?" — the human *is* the accept step (`cosmos_src/human_mcmc_cartoon.png`, COSMOS s31).
- **Analysis:** if learners **sample from their posterior** (Bayes-portrait s33), the chain on hypotheses **converges to the prior P(h) in their heads** (s34) — *you can read out someone's prior by running them as MCMC.* Connect to structure/process/behavior (Marr).
- **Result:** Sanborn & Griffiths (2007) stick animals (`sanborn_stick_prototypes.png`, `sanborn_2d_scatter.png`).
- **Fenced extension** (if time): subjective-randomness Gibbs-MCMCP (`subj_random_ladder*.png`, s40–46) + music Gibbs (s48–56) — both *Gibbs*, callback to Block 5.
- **Compression path:** cartoon + one stick-animal slide + one sentence = ~3 min.

### Block 9: Payoff B — a sampler for the Kemp hierarchy (15 min, PROTECTED)

*The implementable deliverable. Never cut. The reason Weeks 3 (conjugacy), 4 (hierarchy), 6 (chains) scaffolded.*

- **Callback to Week 4** (`kemp-hierarchy-plate.png`): θᵢ ~ Beta(a,b), kᵢ ~ Binomial(nᵢ, θᵢ), (a,b) learned (overhypotheses; Kemp/Perfors/Tenenbaum 2007; **no DPMM**).
- **Why a sampler:** the joint posterior $p(a,b,\{\theta_i\}\mid\text{data})$ has no clean closed form; IS was "blunt." Now build the sharp tool.
- **Two-step block sampler** (`gibbs-metropolis-recipe.png`), 5-slide build-up:
  1. the plate model;
  2. **Gibbs step (conjugate, easy):** holding (a,b), $\theta_i\mid a,b,k_i,n_i \sim \text{Beta}(a+k_i,\, b+n_i-k_i)$ — *exactly Week 3*;
  3. **(φ,κ) reparam + priors:** mean $\varphi=a/(a+b)$, concentration $\kappa=a+b$; log-uniform prior on κ, uniform/Beta on φ;
  4. **Metropolis step:** random walk $\log\kappa'=\log\kappa+\epsilon$; accept by the ratio of the **product-over-students Beta-Binomial marginals** $\prod_i\text{BetaBin}(k_i\mid n_i,a,b)$ (θᵢ integrated out analytically — the conjugacy payoff);
  5. the full loop schematic.
- **GenJAX callout / final slide** (two-column *math* \| *GenJAX*): Gibbs step = `Beta(...).sample`; Metropolis step = the `assess`-based kernel from Block 5/7 scoring the marginal — *"this is the sampler you assemble, and it's the assignment."*
- **Closing line:** the chain spends samples where the mass is (sharp) vs. IS weighting a prior cloud (blunt).
- **Authoring risk:** 4 new ideas (φ/κ reparam, log-space proposal, log-uniform prior, marginalizing θ) — rehearse for time; if it must shrink, present reparam + Gibbs half fully and defer the marginal-integration detail to the assignment stencil.

### Block 10: Close + Week 8 bridge (3 min)

- Recap the ladder (one slide): MC → IS → particle filter → MCMC (MH+Gibbs) → applied to people / the Kemp hierarchy. Each rung bought a sharper tool for a harder target.
- Assign the GenJAX sampling exercise (the Kemp sampler is the capstone).
- Week 8 preview: SDT / MDP / RL — "from inferring beliefs to choosing actions." Confirm Week 8 presenter.

---

## Per-block visual budget (audit checklist before "lecture-ready")

| Block | Figure(s) | Two-column | Build-up |
|---|---|---|---|
| 1 Welcome | (reuse Week 6 hospital poll) | — | — |
| 2 Basic MC | `mc-die-convergence`, `mc-pi-darts` | inverse-CDF \| rejection | π-darts n=10/100/1000/10⁴ |
| 3 Importance sampling | `is-weight-variance` | good q \| bad q | — |
| 4 Particle filtering | PF schematic | — | weight→resample→propagate |
| 5 MCMC | `mh-anim-1..6`, `gibbs-trace` | MH \| Gibbs | MH accept/reject sibling slides |
| 6 Interactive viz | the live demo + `mcmc-gmm-fallback` (PDF) | small-σ \| large-σ | (demo is the build-up) |
| 7 GenJAX light | (code-block slide) | classical \| GenJAX | — |
| 7b GenJAX heavy | (live code) | — | model→importance→MH |
| 8 MCMCP | `human_mcmc_cartoon`, `sanborn_*` | data→h \| h→data | (opt: subj-randomness ladders) |
| 9 Kemp | `kemp-hierarchy-plate`, `gibbs-metropolis-recipe` | math \| GenJAX | plate→Gibbs→(φ,κ)→ratio→loop |

---

## Polls (mined per the CLAUDE.md standing rule; bilingual; record source in speaker notes)

| # | Block | Source quiz item | Prompt → reveal |
|---|---|---|---|
| 1 | 1 (reveal-only) | *Monte Carlo Estimation* quiz, "Intuition" (hospital) | committed in Week 6 → reveal: **smaller** hospital (LLN). *That was Monte Carlo.* |
| 2 | 5 | *Markov chains and networks* quiz, Q4 (start-doesn't-matter) | two starts, long run → **same** histogram (ergodic forgets start = π) — *if it mixed.* |
| 3 | 6 | *Markov chains and networks* quiz, stationary item (recast) | two MH runs disagree @1000 steps → **hasn't mixed / stuck in a mode.** Lands after the demo. |
| 4 *(opt)* | 3 | fresh (IS overlap intuition) | prior/posterior barely overlap → **a few huge weights, noisy estimate** (= the "blunt tool"). |

All bilingual: options in **one** `.fragment` wrapping paired lang divs; paired-lang reveal answer line; options as bullet lists. **Poll 1 is a callback reveal** — reuse the Week 6 bilingual prompt verbatim and add only the reveal + "this is Monte Carlo" line.

---

## Contingencies

- **If a Week 7 presenter is confirmed** (`readings_map.yml`): convert Block 8 to a 2-min bridge ("MCMC with People = the MH accept step done by humans; watch the chain converge to the prior") + handoff (presentation ~20–25 min). Then cut Block 7b, and **Block 9 still runs** (protected). Highest-risk scope variable — verify first.
- **Basics overran:** cut Block 7b, compress Block 8 to its cartoon, protect Block 9.
- **Interactive viz fails to load:** fall back to `mh-anim-*` (Block 5) + `gibbs-trace` + the `mcmc-gmm-fallback.png` still; state the proposal-variance lesson verbally. Poll 3 still works against the static stuck-chain image.
- **Recommended hard cuts if tight:** optimal-IS (asymptotic-variance "optimal q") aside; the subjective-randomness/music Gibbs MCMCP extension.

---

## TODOs spawned by this outline

- [ ] Build `week7-slides.qmd` (Quarto RevealJS, theme line, EN/JA divs, KaTeX, 4 polls, recurring "in GenJAX:" callouts, fenced Block 7b + MCMCP extension, viz iframe + PNG fallback slide, `resources:` for the iframe).
- [ ] Author the GenJAX code-callouts against **genjax 0.10.3** (`simulate`/`importance`/`assess`/`smc.ImportanceK`, hand-assembled MH); name-drop v1.0.10 `hmc()`/`chain()`.
- [ ] Extract / make the particle-filter schematic (check SP25 deck first).
- [ ] Run the RevealJS fill audit (`SLIDE_VISUAL_QA.md`); spot-check the Kemp build-up + MH animation + viz-fallback with decktape + Read PNG. Toggle JA (`L`) through the polls.
- [ ] Native-speaker proof of the Week 7 JA translations.
- [ ] **Verify the Week 7 presenter in `readings_map.yml`** before class.
- [ ] `course/quizzes/README.md` Week-7 row maps to the *Bayes Net* quiz (predates SP26 re-sequence) while the polls mine *Monte Carlo Estimation* + *Markov chains and networks* — flag the mismatch.
- [ ] **Follow-on (separate session):** expand the textbook T2 GenJAX tutorial (Ch 0–4, 6; no MCMC/SMC yet) to cover MCMC + the Kemp sampler; per the chapter-ship checklist also update notebook_guide, glossary, HML homepage card. Author the GenJAX sampling exercise / Kemp assignment stencil into `assignments/`.
