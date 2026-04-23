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

## GenJAX Integration
- T2 Ch 4: `genjax/04_conditioning.md` (conditioning is the inference primitive for hierarchical models)
- Hands-on exercise: extend `bento_day()` from Week 2 to a hierarchical version where the tonkatsu rate is itself drawn from a Beta prior — infer the rate from observed bentos across multiple students

## Contemporary ML Notes
- In-context learning in LLMs can be framed as Bayesian generalization (Xie et al 2021, Wang et al 2023). Mention as optional reading.

## Status
Merged from the previous 13-session plan: this week now absorbs hierarchical-Bayes content that was formerly week05's first half. Bayes Nets (week05's second half) + Causal Bayes Nets (former week06) are consolidated into the new Week 5.

## SP26 artifacts
- Not yet built. Use the `course/week02_basic_bayes_cont/` triplet pattern when the week approaches (see repo CLAUDE.md → "How to build a week").

## TODOs
- [ ] Build SP26 Week 4 artifacts (shared-outline + build script + generated deck)
- [ ] Move `hierarchical-bayes.html` from the old `week05_hier_bayes_bayes_nets/wiki_pages/` into this directory's `wiki_pages/`
- [ ] Write the hierarchical `bento_day()` GenJAX exercise
- [ ] Optional: add in-context learning reading (contemporary ML)
