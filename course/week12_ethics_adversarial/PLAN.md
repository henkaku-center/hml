# Week 12 (Jul 17): Ethics + Adversarial

## Topics
- Neural networks continued
- Adversarial examples
- Ethics in machine learning
- **Semester retrospective — synthesis of all 10 papers**  (~25-30 min)
- Student final project presentations

## Semester retrospective — structure

The last 30 min of the course.  Students walk out with a one-page mental
map of the 10 papers they presented/saw presented across Weeks 4–12.

### Opening question (3 min)
"Which paper from this semester surprised you most?  Which one are you most
likely to go back and re-read in a year?"   Quick go-around, one answer each.
Not a discussion, a pulse.

### The synthesis diagram (15 min)

Show a single diagram on screen (a "map of the semester") that organizes
every paper by two axes:

- **Vertical: Marr's level.**   L1 (what?) / L2 (how?) / L3 (neural).
  Tenenbaum & Griffiths 2001 is pure L1.  Abbott et al 2012 is L2
  (memory via random walk).  Pereira et al 2018 is L3 (decoding meaning
  from fMRI).
- **Horizontal: what kind of computation.**
  1. Inference over categories    (generalization, conditioning)
  2. Inference over structure     (Bayes nets, causal, topic models, BNP)
  3. Inference over time          (MC, Markov chains, RL, IRL)
  4. Substrate / limits           (deep NNs, LLMs, bias, adversarial)

Every paper falls in one quadrant.  Show the spatial map with each paper
placed.  Then walk through it — 1 sentence per paper on what it contributes.

### Connections to contemporary ML (7 min)

The "classical" cog-sci work connects directly to what's happening in 2025-26:
- Hierarchical Bayes → in-context learning, few-shot adaptation.
- Bayes nets / causal → alignment, RLHF reward modeling.
- Monte Carlo → diffusion models, variational inference in LLMs.
- IRL → RLHF itself (learning reward from human demonstrations).
- BNP → open-ended concept learning in LLMs.
- NN work + Caliskan/Buolamwini → what alignment actually has to defeat.

Show this as one more slide — the bridge from "classical cog-sci" to
"today's AI."  Name connections students have seen this semester.

### Close (3 min)
"What you learned this semester is a toolkit — not a fixed set of answers.
Every paper we read was someone applying this toolkit to a specific
behavioral or computational question.  You now know the toolkit well
enough to read a 2026 paper and see what problem it's trying to solve."

Final thank-you.  End.

## SP25 Content
- **Slides:** Week12_NNs2.pptx (+ PDF)
- **Transcript:** Week12_NNs2Transcript.docx
- **Wiki pages:** nns-2-and-conclusions.html, student-final-project-presentation.html
- **Quiz:** Filler Quiz

## Textbook Chapters
None this week.

## GenJAX Integration
- Contemporary ML updates (needs planning)

## Contemporary ML Notes
- Update with recent AI safety and alignment developments
- RLHF and alignment techniques
- Foundation model risks and governance
- Mechanistic interpretability
- Multimodal models

## Status
Needs update for contemporary AI safety/alignment content.

## TODOs
- [ ] Update with recent AI safety/alignment developments
- [ ] Add RLHF content
- [ ] Review and update adversarial examples with recent work
- [ ] **Build the "map of the semester" poster diagram** — matplotlib or
      TikZ figure placing every paper in a 2D (Marr-level × computation-type)
      grid.  Generate from `course/readings_map.yml` so it updates when
      presentation assignments finalize.
- [ ] **Build the "classical cog-sci → modern ML" bridge slide** — 6-row
      table listing each connection (hierarchical Bayes → in-context
      learning, IRL → RLHF, etc.) with one citation per row for the
      modern side.
