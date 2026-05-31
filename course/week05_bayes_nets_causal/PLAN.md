# Week 5 (May 29): Bayes Nets + Causal Bayes Nets

## Topics
- Bayesian networks / graphical models (bulk of the session — ~70 min)
- Causal Bayesian networks + the do-operator (smaller component — ~30 min)
- Brief gesture at information theory (as optional reading; don't lecture)

## SP25 Content
- **Slides:** `slides/sp25_reference/Week04_hierBayesAndBayesNets.pptx` (+ PDF) — **second half only** (the Bayes-nets half; the hierarchical-Bayes half was used in Week 4). Plus `slides/sp25_reference/Week05_CausalBayesNets.pptx` (+ PDF) for the causal segment.
- **Wiki pages:** `wiki_pages/bayesian-networks-slash-graphical-models.html`, `wiki_pages/more-resources-for-bayesian-networks.html`, `wiki_pages/bayes-nets-revisited-causal-bayes-nets-and-intro-to-information-theory.html`
- **Quiz:** "Bayesian Generalization" (ungraded self-check, covers Week 4 material)

## Textbook Chapters
- T3 Ch 5: `intro2/05_mixture_models.md` (review — overlaps with Week 4)
- T3 Ch 12: `intro2/12_hierarchical_bayes.md` (Hierarchical Bayes — review/bridge link from Week 4's second half)
- Bayes-nets chapter: none yet in the textbook; consider writing one during the semester (existing TODO under Textbook & GenJAX).

## GenJAX Integration
- T2 Ch 6: `genjax/06_building_models.md` (composing generative models — a Bayes net IS a structured generative model)
- Optional: a short "model comparison via intervention" GenJAX exercise (see TODO below)

## Contemporary ML Notes
None required. Information theory gets a pointer, not a lecture.

## Status
Merged from the previous 13-session plan: this week now consolidates Bayes Nets (formerly week05's second half) with Causal Bayes Nets (formerly week06). The causal portion is intentionally the smaller half of the session.

## SP26 artifacts
- Not yet built. Use the `course/week02_basic_bayes_cont/` triplet pattern when the week approaches.

## Session structure sketch (120 min, for building the shared-outline later)
1. Welcome + Week 4 carryover (5 min)
2. Bayes nets as structured joint distributions (30 min)
3. Inference in Bayes nets — d-separation, message passing sketch (30 min)
4. Break (10 min)
5. Causal Bayes nets + the do-operator (25 min)
6. Worked causal example (15 min)
7. Admin + Week 6 homework (5 min)

## TODOs
- [ ] Build SP26 Week 5 artifacts (shared-outline + build script + generated deck)
- [ ] Create a short GenJAX causal-model exercise (lightweight; one do-operator example)
- [ ] Decide whether to write a textbook chapter on Bayes nets this semester
