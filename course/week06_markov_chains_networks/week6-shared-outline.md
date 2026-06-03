# Week 6: Shared Outline
## Friday, June 5, 2026

**For:** Prof. Austerweil
**Course:** Human and Machine Learning SP26 (Chiba Tech SDS)
**Session length:** 2 hours
**Required reading (pre-class):** Abbott, J. T., Austerweil, J. L., & Griffiths, T. L. (2012). *Human memory search as a random walk in a semantic network.* NeurIPS. — the cognitive payoff of the whole session: memory retrieval **is** a random walk on a network.
**Textbook reading:** None this week (no MC/Markov chapter exists in the textbook yet).
**Students:** ~6
**Student presenter:** **None this week** — the cognitive content (Abbott 2012 random-walk-in-a-semantic-network; optionally Zemla foraging / Alzheimer's networks) is **instructor-led**. Prof. Austerweil has extensive prior material on this (see source decks below).

---

## Key Design Decision

**This week is the bridge from inference to *process*.** Weeks 1–5 were about *what* to infer (Bayes, generalization, Bayes nets, causality). Week 6 introduces the first **process** abstraction the course will lean on for the rest of the term: the **Markov chain** — a system whose next state depends only on its current state. The session builds one idea three times, each more concrete:

1. **Markov chain** — abstract: states + a transition matrix; the Markov property; convergence to a stationary distribution.
2. **Random walk on a network** — a Markov chain whose states are nodes of a graph; the stationary distribution is the node's **degree** (for an undirected graph). Networks become the *structure*, the walk becomes the *process*.
3. **Memory search as a random walk** (Abbott 2012) — the cognitive payoff: human semantic fluency (`cat, dog, lion, tiger, …`) looks exactly like the sequence of states visited by a random walk on a semantic network. This is the required reading, and it is **instructor-led** this year.

**Confirmed design choices (this planning session, 2026-06-01):**

- **No student presentation.** Full instructor-led lecture, **1 break**, **2–3 audience polls** mined from the SP25 *Markov chains and networks* quiz (and one from the *Monte Carlo Estimation* quiz as a bridge). Reserve a short open-discussion beat after the Abbott payoff if time allows.
- **Cognitive payoff depth: focused block (~15 min) minimum, extra if time.** Block 6 (Abbott 2012 random walk in a semantic net) is the guaranteed core. Block 7 (Zemla foraging / Marginal Value Theorem + Alzheimer's-network material) is an **optional extension** fenced in the deck — run it only if the foundations finished on time. Mirrors Week 4's Variant-A/Variant-B hier-Bayes pattern.
- **Stationary-distribution math: intuition + power iteration.** Show the stationary distribution by *running the chain / multiplying P by itself* ("multiply P a lot and the rows converge"), state "largest eigenvector, eigenvalue 1" as a **named fact** (one dim caption), and give the clean network result $\pi_i \propto \deg(i)$. **CUT the SP25 PCA/SVD eigenvector aside** — it is a Week-3-topics tangent and derails the process narrative. (The explicit eigenvector solve stays in the *assignment*, not the lecture — see the SP25 quiz Q5.)
- **Chibany opener + canonical examples.** Open the Markov-chain idea with a **Chibany** scenario (his daily bento choice depends only on yesterday's — a 2-state Markov chain over tonkatsu/hamburger), then use the **canonical** examples for the mechanics: card-shuffle (mixing), H/T coin finite-state-automaton (transition matrix ↔ FSA), and the **Meow/Lion/Cat/Dog animal semantic network** for the random walk. The animal network is already on-theme for the course; don't force a Chibany-flavored semantic net.
- **Flexible Week 6 ↔ Week 7 boundary.** Monte Carlo does **not** have to wait for Week 7. The stationary-distribution-by-simulation idea ("run the chain, count how often you visit each state") *is* a Monte Carlo idea, and it is the cleanest on-ramp to Week 7's MCMC. So Week 6 **opens** with a 1-poll Monte Carlo *teaser* (the hospital problem — law of large numbers as intuition) and **closes** with an explicit bridge: "we've been *estimating* a distribution by sampling from a Markov chain; next week we *design* a chain whose stationary distribution is a target we choose — that's MCMC." If the day runs long, the bridge compresses to one slide; if short, the MC teaser can expand.

**Authoring style** follows Week 4 (the canonical example): Quarto RevealJS, shared SCSS theme (`../../sds-reveal/sds.scss`, the Week-3+ five-tier system — **set `theme: [dark, ../../sds-reveal/sds.scss]` in the qmd frontmatter**, per CLAUDE.md), EN/JA `.lang-en`/`.lang-ja` divs on every concept-introducing slide, KaTeX math, sequential-reveal build-ups for the random-walk trace and the power-iteration convergence. Polls mined from the SP25 *Markov chains and networks* quiz (`gefe6f0bdb37a0476e57d5ebb0d3ffcb4`) and *Monte Carlo Estimation* quiz (`gdf7280c55bc721fc3d0909807925e93b`) per the CLAUDE.md standing rule.

**"Where we are" recap slides.** At each major block boundary, re-show the agenda as a `{.agenda .dense}` slide with finished blocks dimmed (`.done`) and the upcoming block highlighted (`.highlight`). Five recaps: before Markov-chain mechanics, before the stationary distribution, before networks, before the random-walk payoff, and before the Week-7 bridge. Each is a ~10s orientation beat, not read aloud.

---

## Source material (what to mine)

Three decks on disk hold all the content; **none is ported wholesale** — mine figures and sequencing.

| Source | Path | What to take |
|---|---|---|
| **SP25 Week 6 deck** (46 slides) | `slides/Week06_MarkovChainsNetworks.pptx` (+ `.pdf`) | The skeleton: Markov property, transition matrix, card shuffle, H/T FSA, stationary distribution, semantic networks, graphs→random-walks, **the Meow/Lion/Cat/Dog worked random-walk example**, $\pi_i \propto \deg(i)$, network terms, Erdős–Rényi vs. power-law. **Skip** the PCA/SVD eigenvector aside. |
| **COSMOS MCMC-with-People tutorial** (70 slides) | repo root: `MCMCPCulturalEvoCOSMOS2025.pptx` | The **polished** Markov-chain intro — the H/T two-views figure (FSA + transition matrix with U[0,1] sampling annotations), the card-shuffle "move random card to top → uniform" slide, sample sequences, "what's the stationary distribution?" These are cleaner than the SP25 versions. (The MCMC half of this deck is **Week 7** material — leave it.) |
| **Shizuoka talk** (100 slides) | repo root: `AusterweilShizuokaUJan2026.pptx` | The **cognitive payoff**: semantic networks, **random walk on a semantic network** (build-up), absorbing random walks / fluency-list mechanics, the Marginal-Value-Theorem foraging curves, the 7-method network comparison, Alzheimer's-network figures, SNAFU. This is the instructor-led Abbott/Zemla block. |

### Reusable figures (already inventoried — extract via LibreOffice/`unzip ppt/media/`)

The figure survey (full table in the planning notes) found these **existing** figures — name them in the qmd, don't re-make:

| Figure | Source deck / slide | What it shows |
|---|---|---|
| **Markov H/T two-views** | COSMOS s12–15 (`image1`-group) | FSA (0.9/0.1) *and* transition-matrix view with U[0,1] sampling — *best Markov-chain teaching figure* |
| **Card shuffle → uniform** | COSMOS s18 (`image18`+sprites) | "move random card to top" mixing example |
| **H/T sample sequences** | SP25 s + COSMOS | `HHHHHHHTTTTTTT…` runs starting from H — makes "stationary ≈ ½" concrete |
| **Random-walk-on-network build-up** | Shizuoka s101 (`image80–83`) | walk an edge at random, first-hitting time — cleanest RW mechanism figure |
| **Semantic-net random walk (animals)** | SP25 networks half | Meow/Lion/Cat/Dog graph + transition-matrix panel, step-by-step walk |
| **Absorbing-RW / Q-R-I matrix refactor** | Shizuoka s39–41 (`image17.emf`) | fluency-list transition refactor (EMF → convert) — *for the optional Block 7* |
| **MVT foraging curve** | Shizuoka s22 (`image9.png`) | optimal vs actual category-leave time (7,264 vs 7,310 ms) — *Block 7 optional* |
| **Control vs AD semantic networks** | Shizuoka s62 (`image45/46`) | side-by-side estimated networks — *Block 7 optional* |
| **Erdős–Rényi vs scale-free** | SP25 deck (final slides) | binomial vs power-law degree distributions |

**Figures-to-make** (none in any deck):
- `figure-todo: chibany-bento-markov.png` — a 2-state Markov chain over {tonkatsu, hamburger} with transition arrows, for the Block 1 Chibany opener. Small matplotlib/graphviz; ~5 min to make.
- `figure-todo: power-iteration-convergence.png` — three bar-charts showing the state distribution after 1, 3, 20 steps from two different starts, both converging to the same stationary π. Built from the SP25 quiz's 3×3 matrix (so the poll reveal and the figure agree). This is the visual that makes "the start doesn't matter" land.

---

## Session Plan

| Time | Block | Duration | What Happens |
|------|-------|----------|--------------|
| 0:00 | **1. Welcome + Chibany Markov opener** | 10 min | 2 min welcome/agenda. Chibany's bento depends only on yesterday's → the Markov property, shown before it's named. Poll 1 (hospital problem / LLN — MC teaser). |
| 0:10 | **2. Markov chains: states, transitions, the Markov property** | 15 min | Markov property formally; transition matrix $P$; the H/T coin as FSA ↔ matrix (two views); card-shuffle as a Markov chain. |
| 0:25 | **3. Stationary distribution (intuition + power iteration)** | 15 min | Run the chain / multiply $P$ a lot; rows converge; "largest eigenvector, λ=1" as a named fact. Poll 2 (does the start matter in the long run?). |
| 0:40 | **4. Networks: graphs as structure** | 12 min | Semantic networks (nodes=concepts, edges=relations); undirected/directed/weighted; from a graph to a transition matrix. |
| 0:52 | **5. Random walk on a network** | 15 min | The Meow/Lion/Cat/Dog worked walk (sibling-slide build-up). The sequence of visited nodes is a Markov chain. Stationary dist $\pi_i \propto \deg(i)$. Poll 3 (which node is visited most?). |
| 1:07 | **Break** | 5 min | |
| 1:12 | **6. Memory search as a random walk (Abbott 2012)** | 18 min | **Instructor-led, required-reading payoff.** Animal fluency = the walk; how the model predicts which animals are listed and in what order. Brief open-discussion beat. |
| 1:30 | **7. Optional extension: foraging + clinical networks** | 0–18 min | *Fenced, run if on time.* Zemla foraging / Marginal Value Theorem (when to switch categories); estimating networks from fluency; Alzheimer's-network differences; SNAFU. |
| 1:48 | **8. Network properties + PageRank + Week-7 bridge** | ~12 min | Shortest path / diameter; Erdős–Rényi vs. scale-free degree distributions; **PageRank = stationary distribution of a random walk** (Griffiths 2007, *Google and the mind* — promised in the Slack thread). Then the **MC→MCMC bridge**: we estimated a distribution by sampling a chain; next week we *design* a chain to sample a target we choose. |
| 2:00 | End | (buffer absorbed) | |

**Timing note.** Block 7 is the slack absorber, exactly like Week 4's hier-Bayes Variant B: it competes only with the optional material and the bridge, never with the core (Blocks 1–6 + the Week-7 bridge always run). If the foundations overran, **cut Block 7 entirely** and go straight to the bridge — the required reading (Abbott) is in Block 6, which is protected.

**Deck size target:** ~70–85 slides (the random-walk trace and power-iteration build-ups inflate the count; Block 7's optional material is ~10 slides that may not be shown).

---

### Block 1: Welcome + Chibany Markov opener (10 min)

- 2 min: welcome, one-line agenda. **Admin (one slide):** Assignment 1 (Clusters) is due **tonight, Fri Jun 5, 8:00 PM** — quick reminder only; the walkthrough already happened in Week 4. Note the 3 pooled late days across the four programming assignments. No Clusters re-tour. (No round-robin.)
- **Show before tell** (per the standing feedback): Chibany picks a bento each day. **Claim:** what he eats today depends *only* on what he ate yesterday — if tonkatsu yesterday, he's bored and likely picks hamburger today; if hamburger yesterday, likely tonkatsu today. Draw the 2-state chain ($\texttt{chibany-bento-markov.png}$) *before* naming "Markov."
  - Introduce the symbol when you name the variable (CLAUDE.md rule): **today's bento** ($X_t$), with $X_t \in \{\text{tonkatsu (T)}, \text{hamburger (H)}\}$.
  - Name it: this is the **Markov property** — $P(X_{t+1} \mid X_t, X_{t-1}, \dots, X_0) = P(X_{t+1} \mid X_t)$. "Given the present, the future is independent of the past." (The SP25 "Really Past / Past / Less Past" slide is the visual.)
- **Poll 1 — the hospital problem** (SP25 *Monte Carlo Estimation* quiz, item "Intuition"; a Kahneman–Tversky LLN classic): *"A large and a small hospital each record days where >60% of babies born are boys. Over a year, which records MORE such days?"* Options: **A.** smaller hospital · **B.** larger hospital · **C.** about the same. Commit before reveal. **Reveal (later, or here as a teaser):** the *smaller* hospital — small samples vary more (law of large numbers). This is the seed for *why we care about sampling and long-run frequencies*, which the whole Markov-chain machinery makes precise. (Tag the reveal as the MC teaser; it pays off at the Week-7 bridge.)
  - *Poll authoring (bilingual):* options in **one** `.fragment` wrapping paired `.lang-en`/`.lang-ja` option divs; the reveal answer line must be paired lang spans, not a bare `[…]{.yellow}`. Options as a **bullet list** (`- **A.** …`), never bare `A./B./C.` lines (they collapse to one paragraph). See CLAUDE.md poll rules.

### Block 2: Markov chains — states, transitions, the Markov property (15 min)

- **Notation lock-in** (define before use):
  - $X_t$ — the **state** at time $t$ (a member of a finite state space $\mathcal{S}$).
  - $P$ — the **transition matrix**; $P_{ij} = P(X_{t+1}=j \mid X_t=i)$. Each **row** sums to 1 (it's a distribution over next states). Define "row-stochastic" in a dim caption.
  - $\pi$ — the **stationary distribution** (introduced fully in Block 3; name the symbol here so Block 3's formula has nothing to decode).
- **Two views of the same object** (canonical COSMOS figure, `image1`-group): the H/T coin as (a) a **finite-state automaton** — two nodes H, T with arrows labeled 0.9/0.1; and (b) a **transition matrix**. Walk one transition by sampling $U[0,1]$ and comparing to 0.9 — makes "the matrix *is* a sampler" concrete.
  - Show the **sample sequences** (`HHHHHHHTTTTTTT…`) so students see runs and the rough ½/½ balance emerge.
- **Card shuffling as a Markov chain** (COSMOS s18): states = orderings of the deck; "move a random card to the top" is a transition; repeated shuffling converges to the **uniform** distribution over orderings — its stationary distribution. A concrete mixing example with no math. (This is also the cleanest intuition for "stationary distribution" before Block 3 formalizes it.)
- **Two-column slide** (structural parallelism, per the visual-density baseline): *FSA view* | *matrix view* side by side.

### Block 3: Stationary distribution — intuition + power iteration (15 min)

- The question: if I run the chain forever, what fraction of time do I spend in each state? Call that $\pi$.
- **Definition:** $\pi$ is stationary if $\pi P = \pi$ — running one more step doesn't change the distribution. (State it; don't derive.)
- **How to find it — power iteration (the intuition route):** start from *any* distribution, multiply by $P$ repeatedly. The rows of $P^k$ converge. Build-up as **sibling slides** (per the visual-density baseline), one per step count, using `power-iteration-convergence.png`:
  - $P^1$ from start A vs. start B — different.
  - $P^3$ — closer.
  - $P^{20}$ — identical regardless of start.
- **Named fact (one dim caption, not a derivation):** the stationary distribution is the **left eigenvector of $P$ with eigenvalue 1**; every valid transition matrix ("stochastic matrix") has one. Define "eigenvector" in one dim line — *a vector unchanged in direction when multiplied by the matrix* — and stop there. **Do NOT bring in PCA/SVD** (the SP25 aside is cut here).
- **Poll 2 — does the start matter?** (SP25 *Markov chains and networks* quiz, Q2 vs Q3 → Q4). Show the 3×3 transition matrix from the quiz. *"Start in state 1 vs. start in state 2. After 20 steps, is the probability of being in state 2 the same or different?"* Options: **A.** same · **B.** different · **C.** depends on the matrix. **Reveal:** essentially the **same** — after enough steps the chain *forgets* where it started (it's ergodic); the long-run distribution is the stationary one. (This is exactly quiz Q4's conceptual point, converted to a commit-before-reveal poll. Record the quiz source in speaker notes.)

### Block 4: Networks — graphs as structure (12 min)

- **(Semantic) networks:** represent concepts as **nodes/vertices** in a graph $G$; **edges** encode relationships. Introduce the symbol: a graph $G = (V, E)$.
  - Kinds: **undirected** vs **directed**; edges can be **weighted**. Cognitive examples: inheritance hierarchies (Collins & Quillian 1969), associative networks (Collins & Loftus 1975). Keep this brief — it's setup for the walk.
- **From a graph to a transition matrix:** define an adjacency/edge matrix $L$ ($L_{ij}=1$ if there's an edge $i\to j$, or a positive weight); normalize each row to get a transition matrix $P$ — *a random walk that, at each node, steps to a neighbor chosen proportional to edge weight.* This is the hinge that turns Block 4's structure into Block 2's process.
- **Two-column slide:** *graph picture* | *its $L$ / $P$ matrix*.

### Block 5: Random walk on a network (15 min)

- **The walk is a Markov chain whose states are nodes.** Worked example, **sibling-slide build-up** (SP25 networks figures, the Meow/Lion/Cat/Dog graph): start at a node, step to a random neighbor, record the visited sequence — `Cat → Meow → Cat → Dog → …`. Each step is its own slide with the graph + the growing visited list, exactly as the SP25 deck animated it.
- **Stationary distribution of a random walk** (the clean payoff, no eigen-solve needed): for an **undirected, unweighted** graph, $\pi_i \propto \deg(i)$ — the long-run visit frequency of a node is proportional to its **degree** (number of edges). State it, then *check it* against the worked example (the highest-degree node was visited most). Define "degree" inline when first used.
- **Poll 3 — which node is visited most?** Show a small 5-node animal network with one obvious hub. *"Run a random walk for a long time. Which node do you visit most often?"* Options = four named nodes (one is the hub). **Reveal:** the hub — because $\pi_i \propto \deg(i)$. Cheap, visual, lands the degree result. (Can be sourced fresh or adapted from the quiz's RW item; record in notes.)
- This block is the structural bridge to Block 6: *if memory is a network and retrieval is a walk, the order people name things should track this same process.*

### Break (5 min) — after Block 5.

### Block 6: Memory search as a random walk — Abbott 2012 (18 min, instructor-led, REQUIRED-READING payoff)

- **The phenomenon first** (show before tell): *"List as many animals as you can in 60 seconds."* (Bousfield & Sedgewick 1944; Troyer et al. 1997.) Run it live for 30–60s if the room is willing, or show a sample list. People list in **bursts by category** (`wolf, lion, giraffe, zebra` … then `dog, cat, horse`) — African animals, then pets.
- **The model (Abbott, Austerweil & Griffiths 2012):** human **semantic fluency** is the sequence of nodes visited by a **random walk on a semantic network**. The category-bursts and the switches fall out of the network's community structure — no separate "search strategy" needed. This is the required reading; this is the slide where the whole week's machinery (Markov chain → random walk on a network) becomes a *theory of memory*.
  - Use the Shizuoka random-walk-on-semantic-net figures (`image80–83`, and the searching-the-network build-up, Shizuoka s32–36).
  - The key claim to land: **structure (the network) + process (the random walk) jointly predict behavior (the fluency list)** — the same structure/process/behavior split the course has used since Marr in Week 2.
- **Open-discussion beat (~3 min):** "What would the network have to look like for *your* fluency list? What does it mean that older adults switch categories less — slower search, or a different network?" (Seeds Block 7.)

### Block 7: OPTIONAL extension — foraging + clinical networks (0–18 min, fenced; run only if on time)

*Fence this block in the qmd with `<!-- BLOCK 7 OPTIONAL: foraging + clinical -->` and treat it exactly like Week 4's Variant B — cut entirely if Blocks 1–6 overran.*

- **Optimal foraging / Marginal Value Theorem** (Zemla, Gooding & Austerweil 2023; Charnov 1976): retrieving within a category gives **diminishing returns**; the MVT says **switch categories when the time to get the next in-category item exceeds the global average retrieval rate.** People (and the random walk) approximate this. Figure: the MVT foraging curve (`image9.png`, optimal 7,264 ms vs actual 7,310 ms — a 46 ms difference).
  - Surprising result worth landing: **optimal switching is preserved with age** — older adults switch *less* but do so *strategically*, not because of a switch deficit (resolves H1 "general slowing" vs H2 "optimal with fewer resources").
- **Estimating networks from fluency** (Zemla & Austerweil 2018; U-INVITE): you can *invert* the walk — given fluency lists, infer the most likely network (prior = distance from the USF free-association norms; likelihood = absorbing random walk over the net). Figure: control-vs-AD estimated networks (`image45/46`); the 7-method comparison (`image28.tiff` — note this is a 3–4-method "best practices" panel, **not** a single 7-bar chart; if a clean comparison bar is wanted it's a figure-to-make from Zemla & Austerweil 2018). Tool: **SNAFU** (`github.com/AusterweilLab/snafu-py`).
- **Clinical application** (Zemla & Austerweil 2019 — a presentation candidate): Alzheimer's disease changes the *structure* of the estimated semantic network (lower mean degree, altered small-world stats), separating representation deficits from retrieval deficits.

### Block 8: Network properties + Week-7 bridge (~12 min, always runs)

- **A few network terms** (one slide, brief — these support the clinical figures and general literacy):
  - **Shortest path length / geodesic distance**; **average shortest path length**; **diameter** (largest shortest-path).
  - **Degree distribution:** histogram of node degrees.
- **Erdős–Rényi vs. scale-free** (one two-column slide): random ER networks have a **Binomial** degree distribution and *can't* be both sparse and clustered; real cognitive/social networks are **scale-free / power-law** (a few high-degree hubs). One figure each (SP25 final slides).
- **PageRank as a random walk (1–2 slides — the Slack thread promises it: "the same object behind PageRank, which we'll see Friday").** PageRank ranks web pages (or concepts) by the **stationary distribution of a random walk** over the link graph — exactly the $\pi$ from Block 3, now at web scale. Tie it back: a page is important if a random surfer visits it often; a concept is accessible if a random-walking mind visits it often. **Griffiths, Steyvers & Firl (2007), *Google and the mind*** showed PageRank over a semantic network predicts human word-fluency — a direct cognitive use of the *same* algorithm, and a presentation/discussion candidate this week. This makes the stationary distribution (Block 3) feel *real*, not just a limit, and reinforces the Abbott payoff. *(If running short, fold PageRank into a single sentence on the bridge slide; it's named in the discussion thread, so it should appear at least in passing.)*
- **Week-7 bridge (the MC→MCMC handoff — always show at least one slide):**
  - Reprise the MC teaser: the hospital poll (Block 1) was about *long-run frequencies from sampling*; the stationary distribution (Block 3) was a *distribution we estimated by running a chain*. **We've already been doing Monte Carlo** — estimating a distribution by sampling.
  - The flip for next week: so far the chain came first and we *found* its stationary distribution. **Next week we reverse it** — we start with a target distribution we *want* to sample (e.g. a posterior), and *design* a Markov chain whose stationary distribution **is** that target. That's **Markov chain Monte Carlo (MCMC)**, and it's how people may sample from their own posteriors (MCMC-with-People — Week 7).
  - If running long, compress Block 8 to: one network-terms slide + one bridge slide. If running short, expand the MC teaser (revisit the hospital reveal, add a "what is Monte Carlo?" one-liner).

---

## Per-block visual budget (audit checklist before "lecture-ready")

Per the visual-density baseline (CLAUDE.md), every non-break block needs ≥1 figure and ≥1 two-column slide where there's structural parallelism:

| Block | Figure(s) | Two-column | Build-up sequence |
|---|---|---|---|
| 1 Chibany opener | `chibany-bento-markov.png` (make) | — | — |
| 2 Markov chains | H/T two-views (COSMOS); card shuffle | FSA \| matrix | H/T sample sequences |
| 3 Stationary dist | `power-iteration-convergence.png` (make) | — | $P^1 → P^3 → P^{20}$ sibling slides |
| 4 Networks | graph + matrix | graph \| $L$/$P$ | — |
| 5 Random walk | Meow/Lion/Cat/Dog graph; RW-on-net (Shizuoka) | — | step-by-step walk trace |
| 6 Abbott payoff | searching-the-network (Shizuoka s32–36) | — | growing fluency list |
| 7 (optional) | MVT curve; control-vs-AD nets | H1 \| H2 hypotheses | — |
| 8 Properties + PageRank + bridge | ER vs scale-free degree dists; PageRank/random-surfer schematic | ER \| scale-free | — |

Two figures-to-make total (`chibany-bento-markov.png`, `power-iteration-convergence.png`) — both small matplotlib/graphviz, scaffold-then-generate before declaring the draft done.

---

## Polls (mined from SP25 quizzes, per the CLAUDE.md standing rule)

| # | Block | Source quiz item | Prompt → reveal |
|---|---|---|---|
| 1 | 1 (open) / pays off in 8 | *Monte Carlo Estimation* quiz, "Intuition" (hospital problem) | Which hospital records more >60%-boy days? → the smaller (LLN). MC teaser. |
| 2 | 3 | *Markov chains and networks* quiz, Q2/Q3/Q4 (3×3 matrix, start-1 vs start-2 @ 20 steps) | Does the start matter after 20 steps? → no, the chain forgets its start (ergodic) → that long-run distribution is $\pi$. |
| 3 | 5 | RW item (adapted) | Which node does a long random walk visit most? → the hub, because $\pi_i \propto \deg(i)$. |

All three: bilingual poll structure (options in one `.fragment` wrapping paired lang divs; paired-lang reveal answer line; options as bullet lists). Record the sourcing quiz item in each poll's speaker notes for traceability.

---

## TODOs spawned by this outline (for the build phase)

- [ ] Build `week6-slides.qmd` (Quarto RevealJS, shared SCSS theme line, EN/JA divs, KaTeX, the three polls).
- [ ] Make `chibany-bento-markov.png` (2-state Markov chain over {tonkatsu, hamburger}).
- [ ] Make `power-iteration-convergence.png` (state dist after 1/3/20 steps from two starts → same π; use the SP25 quiz's 3×3 matrix so poll + figure agree).
- [ ] Extract reusable figures from the three source decks (LibreOffice / `unzip ppt/media/`): H/T two-views + card shuffle (COSMOS); Meow/Lion/Cat/Dog walk (SP25); random-walk-on-net + MVT curve + control/AD nets (Shizuoka, several are EMF/TIFF → convert).
- [ ] Fence Block 7 (`<!-- BLOCK 7 OPTIONAL -->`) so it cuts cleanly under time pressure.
- [ ] Run the RevealJS fill audit (`SLIDE_VISUAL_QA.md`) before lecture-ready; spot-check riskiest slides with decktape + Read PNG.
- [ ] Native-speaker proof of the Week 6 JA translations (machine-authored, same as Weeks 2–4).
- [ ] Confirm there is genuinely no Week 6 presenter in `readings_map.yml` before class (currently `presenter: null`).
- [ ] Decide whether to assign the SP25 *Markov chains and networks* quiz (the 3×3 stationary-distribution computation) as a short homework/check — it pairs naturally with this lecture.
