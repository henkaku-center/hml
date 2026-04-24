# Human and Machine Learning SP26 — Consolidated TODOs

### SP25 Carryovers
- [ ] More student discussion/activities in early weeks (Weeks 1-4) *(partially addressed by SP26 lecture+check-ins format; revisit after running Weeks 1–2)*
- [ ] Fix MC importance sampling figure legend (Week 8 slides)
- [ ] Fix Bayes Net quiz wording (Week 7 quiz)
- [ ] Modernize RL assignment: update Python/R code, add Julia variant *(fold into GenJAX port scoping)*

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

### SP26 New — Syllabus & Admin
- [x] Draft SP26 syllabus source (`course/syllabus/SP26_syllabus.md`) and publish to the site
- [x] Update grading to reflect 6 students / 12 sessions: reflections 15%→12.5% (8-of-13 → 6-of-12); new paper-presentation line at 7.5%; participation folded in
- [x] Add Paper presentations section to syllabus (rubric + Griffiths framing questions)
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

### SP26 New — Slide infrastructure
- [ ] **Write a Quarto-qmd → pptx converter.** The Quarto deck is now the canonical slide source (week2-slides.qmd, etc.); the hand-written `build_slides_weekN.py` pptx track has diverged and is no longer maintained. Need a single-entry tool that reads the .qmd and emits a python-pptx Office deck preserving speaker notes, math (KaTeX → equation/image), the yellow-frame theme, and section breaks, so the pptx artifact can be regenerated from the canonical source instead of hand-edited in parallel. Until this exists, ignore the per-week `build_slides_weekN.py` scripts.

### SP26 New — Textbook & GenJAX
- [ ] Map textbook homework readings to each week's PLAN.md
- [x] GenJAX setup pointer for students (Week 2 homework — Tutorial 2 Ch 0-1, referenced in Week 1 PLAN.md)
- [x] Clusters assignment — GenJAX stencil: `course/assignments/clusters/clusters.ipynb`
- [ ] **Separate planning session:** scope GenJAX ports for generalization / MC / RL (depth, textbook chapter mapping, solution-notebook sources, sequencing by due-week)
- [ ] Port generalization assignment to GenJAX *(blocked on scoping session above)*
- [ ] Port MC assignment to GenJAX *(blocked on scoping session above)*
- [ ] Port RL assignment to GenJAX *(blocked on scoping session above)*
- [ ] Plan which new textbook chapters to write during semester
- [ ] Add GenJAX exercises to Weeks 6, 8, 11

### SP26 New — Contemporary Content
- [ ] Review Weeks 11-13 for opportunities to include recent ML developments (LLMs, foundation models, RLHF, alignment)
- [ ] Update readings list with post-2023 papers where relevant
- [ ] Consider adding content on: scaling laws, in-context learning, mechanistic interpretability, multimodal models
- [ ] Week 12 (Deep NNs): consider transformer architecture, attention mechanisms
- [ ] Week 13 (Ethics): update with recent AI safety/alignment developments
