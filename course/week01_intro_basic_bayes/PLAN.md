# Week 1 (Apr 17): Intro + Basic Bayes

## Topics
- Why this course exists: inductive inference as the shared substrate of human cognition and ML
- Basic probability: sets, events, random variables, joint/conditional, marginalization
- Bayes' rule — derivation and two worked examples (sick friend, Kahneman-Tversky cab)
- Heuristics & biases framing; 5-step Bayesian-modeling recipe
- GenJAX orientation (motivation + setup pointer, not a tutorial)
- SP26 admin and grading scheme

## SP25 Content
- **Slides:** `slides/sp25_reference/Week00_intro_and_admin.pptx`, `slides/sp25_reference/Week00_BasicBayes.pptx` (+ PDFs). Retained as reference only — do not present as-is. Session Plan below maps specific SP25-reference slides into the 2-hour SP26 session. The SP26 deck will land in `slides/sp26/` (TODO).
- **Wiki pages:** `wiki_pages/intro-and-big-qs.html`, `wiki_pages/basic-bayes.html`
- **Quiz:** Paper presentation preferences *(not carried forward — presentations replaced with written reflections for SP26)*

## Textbook Chapters
- Bk: hungry, probability as counting (`foundations/`; with the `start/` reading guide) *(homework after class)*

## GenJAX Integration
- End-of-class orientation (~10 min): motivation + one short generative-model example from `textbook/content/genjax/02_first_model.md`
- Homework: Bk: getting started, python basics (`genjax/`) so students can self-onboard before Week 2

## Contemporary ML Notes
None this week. Week 1 is foundations.

## Status
SP26 session plan finalized (this file). Follow-on tasks: build SP26 slide deck; update PLAN.md when slide deck lands.

---

## Session Plan (120 min, ~10 min buffer)

**Structural changes from SP25:** 3 hours → 2 hours; 10+ students → 2-4 students. Format is lecture + frequent check-ins (every 15-20 min). Time budget: ~30 min intro / ~80 min Bayes / ~20 min admin+GenJAX+homework. Student background assumed: strong math/CS, lighter cog sci.

### Block 1 — Welcome + framing (~5 min)
Introduce self, course title, meeting cadence (Fridays, 13 sessions, no class May 1). Round-robin student intros: name, background, *one thing you hope to get out of the course*. In a 2-4 person seminar this doubles as the diagnostic. **No admin yet** — deferred to Block 5 to preserve momentum.

### Block 2 — Why this course exists: inductive inference (~25 min)
Three concrete demos, each framed as "? + ? = 5":

1. **Checkershadow illusion** (~6 min). SP25-ref `intro_and_admin` slides 2-4. Show image; students say which square is darker; reveal they're identical. Debrief: visual system is *solving an inductive problem* (square color + shadow = intensity) using priors.
2. **Heider-Simmel video** (~8 min). SP25-ref `intro_and_admin` slides 10-11. Play ~90s clip. Ask students to narrate. Debrief: from bare motion cues, everyone constructs a goals/beliefs story — inference under massive ambiguity.
3. **Concept/word learning — "jumbuck"** (~8 min). SP25-ref `intro_and_admin` slide 14. Quine's rabbit puzzle. Why, given any finite example, does a child pick one hypothesis over logically-equivalent alternatives (undetached rabbit parts, temporal stages)? Motivates hypothesis spaces and priors — previews Week 3+.

**Check-in (~3 min):** "What's the common structure across these three?" Target answer: hidden variable + noisy/sparse data + prior knowledge → best guess. Write on board as `P(h | d) ∝ P(d | h) · P(h)` (notation only — to be revisited).

### Block 3 — Basic Bayes: foundations (~25 min)
Compact-but-rigorous. Map to SP25-ref `BasicBayes` slides 3-13.

- Sets, outcome space, events, event space (~5 min). Two-coin-flip running example.
- Random variables as functions (~4 min). Concrete: `Y` = "at least one H".
- Joint probability (~3 min).
- **Conditional probability as set restriction** (~5 min) — SP25-ref `BasicBayes` slide 9. The 2/3 vs 3/4 contrast: `P(first=H | at least one H) = 2/3`, *not* 3/4. See conditioning visually on the 4-outcome grid, then give the ratio definition.
- Marginalization (~3 min).
- Bayes' rule derivation from product rule (~5 min). One line on the board; students confirm each step.

**Check-in (~3 min):** "In the cab problem I'm about to give you, what's `d` and what's `o`?"

### Block 4 — Bayes in action: sick friend + cab problem (~35 min)

1. **Sick-friend intuition (~10 min).** SP25-ref `BasicBayes` slides 15-26. Three hypotheses (cold, stomach virus, lung cancer), observation = cough, chain-smoker prior. Qualitative first (high/medium/low — SP25-ref `BasicBayes` slide 21), then numeric: priors × likelihoods → 0.75 / 0.08 / 0.17 posteriors. Emphasize the counterintuitive result: cold wins despite smoking history, because of prior.
2. **Kahneman-Tversky cab problem (~20 min).** SP25-ref `BasicBayes` slides 32-41. Three passes:
   - Students attempt cold (~3 min). Most will say ~80%.
   - Area-diagram depiction (~5 min): 85 green / 15 blue; 80% of 15 = 12; 20% of 85 = 17; so 12/(12+17) ≈ 41%.
   - Formal Bayes pass (~7 min): same numbers via the equation. They agree. Name: *base-rate neglect*.
   - Discussion (~5 min): why does the mind do this? Heuristics-and-biases framing (SP25-ref `BasicBayes` slides 34-35). Preview: future weeks test whether people are Bayesian under other framings.
3. **Synthesis (~5 min).** 5-step Bayesian-modeling recipe (SP25-ref `BasicBayes` slide 43): formalize problem → formalize knowledge → apply Bayes → see what ideal learner does → identify knowledge/constraints needed to match human behavior. *This is the course's method.*

### Block 5 — GenJAX orientation + admin + homework (~20 min)

1. **GenJAX orientation (~10 min).** Not a tutorial — a motivated pointer.
   - Frame: "Bayes' rule is easy to write; enumerating hypothesis spaces by hand is not. GenJAX is how we'll do it."
   - Live example (from `textbook/content/genjax/02_first_model.md`):
     ```python
     @gen
     def chibany_day():
         lunch = flip(0.5) @ "lunch"
         dinner = flip(0.5) @ "dinner"
         return (lunch, dinner)
     ```
     Verbally map: `@gen` = generative model; `flip(0.5)` = Bernoulli RV; `@ "lunch"` = name the choice for later conditioning. *This function **is** the outcome space Ω from Block 3.*
   - Preemptive callouts: Colab-only (no local install); `flip()` not `bernoulli()` (logit trap); `@` is GenJAX-specific (not matmul); outputs display as `Array(0, dtype=int32)` not plain `0`.
   - Do NOT teach Python basics or the full tutorial. Point at the chapters and trust them.

2. **Admin (~7 min).** Cover:
   - Meeting time/location; textbook URL (https://josephausterweil.github.io/probintro/).
   - GenJAX via Colab, no local setup needed.
   - **Weekly written reflections** replace SP25 paper presentations (doesn't fit a 2-4 person seminar).
   - **SP26 grading scheme** (see table below).
   - Office hours TBD; email policy; AI policy (welcome as a resource, must cite; not for quiz/assignment answers).

3. **Homework (~3 min).**
   - Read T1 Ch 1-3 (reinforces Block 3).
   - Read T2 Ch 0-1 (sets up GenJAX for Week 2).
   - Week 2 quiz: "Intro Probability Theory 1."

### Buffer (~10 min)
Absorb overruns in Block 2 (Heider-Simmel gets chatty) or Block 4 (cab-problem discussion spills). If nothing to absorb: open Q&A or pull one more concept-learning wrinkle forward from Week 3.

---

## SP26 Grading Scheme

| Component | Weight | Sub-breakdown |
|---|---|---|
| Final project | **50%** | Proposal 5% · In-class presentation 7.5% · Final paper 37.5% |
| Programming assignments (4) | **30%** | Clusters 7.5% · Generalization 7.5% · MC 10.5% · RL 4.5%. **All four target GenJAX.** |
| Weekly written reflections | **15%** | ~200 words per assigned reading, pre-class. ~8 of 13 required (student's choice). Pass/fail each. *Replaces SP25 paper presentations.* |
| Participation | **5%** | Discussion engagement. Small on purpose — attendance self-evident in a 2-4 person seminar. |
| Quizzes | **0%** | Self-check only. Weekly quizzes in `course/quizzes/README.md` available but ungraded. |
| **Total** | **100%** | |

Assignment ratio rationale: MC weighted highest (SP25's "assignment 3 is harder" 1.5× logic); RL lightest because scaffolding code carries more of the load.

---

## TODOs
- [ ] Build SP26 Week 1 slide deck in `slides/sp26/` from this plan (SP25-reference `.pptx` files stay in `slides/sp25_reference/`)
- [ ] Add more student discussion/activities beyond the three check-ins (SP25 carryover — partially addressed by format shift, revisit after running it)
- [ ] Draft clusters GenJAX stencil (tracked separately; see `course/assignments/README.md`)
- [ ] Separate planning session needed to scope GenJAX ports for generalization / MC / RL
