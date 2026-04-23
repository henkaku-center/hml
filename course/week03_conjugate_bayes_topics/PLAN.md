# Week 3 (May 15): Conjugate Bayes + Topics

Note: No class May 1 or May 8. This is the first class after the two-week skip.

## Prerequisites from Week 2
Week 2 (April 24) now lays down the full continuous-probability backbone:
- Expected value, Bernoulli, Binomial (Block 5)
- PMF → PDF, the Gaussian formula, Bayes with a continuous likelihood (Block 6)
- **A complete worked Gaussian-Gaussian conjugate update** (Block 7)
  — prior μ ~ N(500, 20²), one observation 510g, posterior ≈ N(503.3, 16.6²).
  Week 3 opens by picking up from here.

This means Week 3 does NOT need to re-teach continuous probability or Gaussians. It opens at the level of "conjugacy as a pattern."

## Topics
- Conjugacy as a pattern: prior × likelihood → posterior in the same family
- Beta-Binomial (for inferring p from counts; back to the bento 70/30 split)
- Gaussian-Gaussian with N observations and unknown σ (Week 2 did known σ only)
- Dirichlet-Multinomial if time (multinomial bentos: tonkatsu / hamburger / curry)
- Mixture modeling teaser (full treatment pushed later)

## SP25 Content
- **Slides:** NONE — need to create. Week 2's build-up style (sequential slides for math reveals) is the canonical approach; use the same pattern.
- **Wiki pages:** `wiki_pages/` (to be populated from SP25 export): discrete-distribution.html, binomial-distribution.html, beta-distribution.html, beta-binomial-posterior-update.html, discrete-multinomial-and-dirichlet-distributions.html, mixture-modeling.html
- **Quiz:** Intro to Prob Theory Quiz 2

## Textbook Chapters
- T3 Ch 4: `intro2/04_bayesian_learning.md` — REQUIRED before class. Picks up directly from Week 2's Block 7.
- T1 Ch 6: `intro/06_glossary.md` — review

## GenJAX Integration
- T2 Ch 2–3: `genjax/02_first_model.md`, `genjax/03_traces.md` (students' own time)
- Consider a short live demo: `beta_binomial_update()` generative model. Optional.

## Contemporary ML Notes
None this week.

## Status
Content outline set above. SP26 artifacts (shared-outline, build script, deck) not yet built — follow the Week 2 canonical pattern when building.

## TODOs
- [ ] Build SP26 Week 3 artifacts (shared-outline + build script + generated deck)
- [ ] Copy relevant wiki pages from `archive/canvas_export_sp25/web_resources/wiki_content/` into `wiki_pages/`
- [ ] Add student discussion/activities
