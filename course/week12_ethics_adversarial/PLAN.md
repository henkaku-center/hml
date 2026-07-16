# Week 12 (Jul 17): Ethics, Adversarial ML & the Semester Retrospective — LAST session

## Scheduling constraint (Joe, 2026-07-05)
Over-subscribed final session: 1 paper presentation (~20 min) + 3 final-project
presentations (~36 min) + retrospective (~29 min) + admin leave only **~15 min for
net-new lecture content**. "NNs continued" is DROPPED (taught in Week 11). Full time
budget in `week12-shared-outline.md`. Deck = holder slides + retrospective + a lean,
heavily-callback'd ethics block; the depth lives in the textbook's Part IX.

## Topics
- Ethics & adversarial ML (one tight ~15-min segment — embedding bias, fairness as
  conditional probability + impossibility, adversarial examples, alignment as inference)
- **Semester retrospective — synthesis of all 10 papers**  (~28-30 min)
- Student paper presentation + three final-project presentations

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
- Bk: adversarial examples — `ethics/adversarial-examples.md`
- Bk: fairness formalisms — `ethics/fairness-formalisms.md` (fairness as conditional probability + the impossibility result — the Part IX flagship)
- Bk: bias in data — `ethics/bias-in-data.md`
- Bk: alignment safety — `ethics/alignment-safety.md` (the book's final chapter)

## GenJAX Integration
- None on slides (time-starved session); the Part IX chapters carry runnable code
  (FGSM via `jax.grad` w.r.t. input; the fairness impossibility demo; WEAT; a
  Bradley–Terry reward fit + reward-hacking demo).

## Contemporary ML Notes
- Every ethics beat is a callback: bias → Week 11 embeddings; fairness → Part I
  conditional probability; brittleness → the Part VIII learned boundary; alignment →
  Week 9 RLHF + Week 8 reward hacking. Ethics falls OUT of the course, not bolted on.
- The retrospective's bridge slide IS the "classical → contemporary" synthesis below.

## Status
**SP26 deck built and QA'd; re-authored onto the layout-scheme v2 theme (2026-07-16).**
23 slides / lean ethics + retrospective + presentation holders / 1 poll / 4 figures.
The 2026-07-05 build had shipped the classic silent defects (slide 8's figure crushed
to 520×124 and distorted; 4–5-line prose walls on slides 8/10/11/12) — the v2 pass
restructured them (columns split on 8, bullets on 10/11/12, notation line + rebalanced
columns on 7, `.agenda-roomy` on 3) and re-audited with the upgraded script: **0 flags
of any kind at the true 960×540 logical size** (incl. the new TINY-FIGURE /
SQUISHED-FIGURE / PROSE-WALL checks and the scrollHeight clip test); all figure slides
paint at 47–63% of stage height. Layout mix: 47% bullets / 20% figure / 13% columns /
13% poll / 7% table. Bilingual EN/JA verified on the restructured slides (L-toggle).
Time-budgeted to the presentation-heavy final session.

## SP26 artifacts
```
week12-shared-outline.md   source of truth (time budget + blocks)
week12-slides.qmd          the deck
week12-styles.html         per-deck overrides (shared design system in the theme)
make_figures.py            4 figures
images/                    semester_map, embedding_bias, fairness_impossibility, adversarial
```

## Done (were TODOs)
- [x] "Map of the semester" 2D diagram — built (`images/semester_map.png`).
- [x] "Classical cog-sci → modern ML" bridge — built as a bilingual table slide.
- [x] Adversarial examples refreshed (FGSM framing; full runnable demo in the Part IX chapter).
- [x] RLHF / AI-safety content — the alignment beat + the `ethics/alignment-safety` chapter.

## Open TODOs
- [ ] Confirm the Week 12 paper presenter (readings_map presenter: null) — the holder
      slide accommodates either way; if none, that ~20 min folds into the retrospective.
- [ ] Confirm final-project presenter count (3 assumed) — add/remove a holder if needed.
