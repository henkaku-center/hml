# Week 4 (May 22): Generalization + Hierarchical Bayes

## Topics
- Bayesian generalization (Tenenbaum-style concept learning, size principle)
- No Free Lunch theorem
- Hierarchical Bayesian models: priors over priors
- Back to Chibany's bentos: if each student has their own tonkatsu/hamburger ratio, can we learn the distribution of ratios?

## SP25 Content
- **Slides:** `slides/sp25_reference/Week03_BayesGeneralization.pptx` (+ PDF) — generalization; plus the **first half** of the former `Week04_hierBayesAndBayesNets.pptx` deck (the hierarchical-Bayes half — copy that over when building the SP26 deck; the Bayes-nets half goes to Week 5)
- **Wiki pages:** `wiki_pages/bayesian-generalization-and-no-free-lunch.html`; `hierarchical-bayes.html` to be moved in from the old week05 directory when that directory is merged in
- **Quiz:** "Gaussian and Binomial Bayes"

## Textbook Chapters
- T3 Ch 4: `intro2/04_bayesian_learning.md` (Bayesian learning — natural bridge from Week 3's conjugacy)
- T3 Ch 5: `intro2/05_mixture_models.md` (mixture models — touchstone for hierarchical structure)
- T3 Ch 7: `intro2/07_generalization/` (Bayesian Generalization — the direct companion: number game, size principle, Shepard's law, No Free Lunch)
- T3 Ch 12: `intro2/12_hierarchical_bayes.md` (Hierarchical Bayes — the second half of this lecture)

## GenJAX Integration
- T2 Ch 4: `genjax/04_conditioning.md` (conditioning is the inference primitive for hierarchical models)
- Hands-on exercise: extend `bento_day()` from Week 2 to a hierarchical version where the tonkatsu rate is itself drawn from a Beta prior — infer the rate from observed bentos across multiple students

## Contemporary ML Notes
- In-context learning in LLMs can be framed as Bayesian generalization (Xie et al 2021, Wang et al 2023). Mention as optional reading.

## Status
Merged from the previous 13-session plan: this week now absorbs hierarchical-Bayes content that was formerly week05's first half. Bayes Nets (week05's second half) + Causal Bayes Nets (former week06) are consolidated into the new Week 5.

## SP26 artifacts
- `week4-shared-outline.md` — SOURCE OF TRUTH: timing table + per-block key points + contingencies.
- `week4-slides.qmd` — Quarto RevealJS deck (61 slides). Shared SCSS theme (`../../sds-reveal/sds.scss`, Week 3+ five-tier system); EN↔JA `.lang-*` divs on all concept slides; KaTeX math; three polls mined from the SP25 *Bayesian Generalization* quiz.
- `week4-slides.html` — generated (`quarto render week4-slides.qmd`).
- `week4-audit/` — fill-audit JSON from `scripts/audit_slide_fill.js`.

**Session design.** 2-hour session structured around Shohei's ~25-min paper presentation (Tenenbaum & Xu 2000, *Word learning as Bayesian inference* — 15 talk + 5 discussion + 5 swap). All core content — generalization framework, size principle, rectangle game (continuous) AND number game (discrete) — is delivered **before the break**. Opens with an 8-min Clusters-assignment walkthrough (Assignment 1 due Fri Jun 5, 8 PM). A dedicated bridge slide primes Shohei's paper as "the number game applied to word meanings."

**Hierarchical Bayes is authored two ways** (instructor selects live by timing): Variant A = 3-slide teaser (~5 min); Variant B = teaser + full worked two-level Beta-Binomial with shrinkage (~10 min more). The variants are fenced with `<!-- HIER-BAYES VARIANT A/B -->` HTML comments in the qmd; A's three slides are also B's opening. T3 Ch 5 assigned as the Week 5 pre-read either way.

**Visual QA.** Passed the RevealJS fill audit (`SLIDE_VISUAL_QA.md` workflow): 0 FLOATING/PUSHED-DOWN defects, 0 real overflows across all 8 viewport sizes. The lone audit flag is the `.agenda.dense` slide, which legitimately fills the stage.

## TODOs
- [x] Build SP26 Week 4 artifacts (shared-outline + Quarto deck) — done 2026-05-20.
- [ ] Move `hierarchical-bayes.html` from the old `week05_hier_bayes_bayes_nets/wiki_pages/` into this directory's `wiki_pages/` *(note: `wiki_pages/hierarchical-bayes.html` is already present)*
- [ ] Write the hierarchical `bento_day()` GenJAX exercise (referenced on slide B6)
- [ ] Confirm Week 5's student presenter against `course/readings_map.yml` before class — the deck's "Next week" slide deliberately does not name one.
- [ ] Native-speaker proof of the Week 4 JA translations (machine-authored, same as Weeks 2–3).
- [ ] Optional: add in-context learning reading (contemporary ML)
