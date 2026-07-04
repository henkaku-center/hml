# Week 12 shared outline — Ethics, Adversarial ML & the Semester Retrospective (Fri Jul 17, 2026, LAST session)

SOURCE OF TRUTH for `week12-slides.qmd`. Edit here first.

## The hard constraint (Joe, 2026-07-05; recon-confirmed)

This is the final, massively over-subscribed session. It must fit: **1 student
paper presentation + 3 final-project presentations + the semester retrospective
+ a tiny ethics/adversarial segment**, in ~105 min. The arithmetic leaves
**~15 min of net-new lecture content — one tight segment, no more.** "NNs
continued" is DROPPED (taught in Week 11). The deck is mostly holder slides +
the retrospective; the ethics content is lean, and the deep treatment lives in
the **Part IX textbook chapters** (authored alongside this deck).

## Time budget (105 min, ~zero slack)

| Clock | Segment | Min | In deck? |
|---|---|---|---|
| 0:00–0:05 | Admin: final paper due Jul 24, submit slides, agenda | 5 | yes |
| 0:05–0:20 | **Ethics & adversarial mini-lecture** (Block 1) | 15 | yes — the only lecture content |
| 0:20–0:40 | Student paper presentation + short discussion | 20 | holder slide |
| 0:40–1:16 | 3 final-project presentations (~12 min each) | 36 | 3 holder slides |
| 1:16–1:45 | **Semester retrospective** (Block 2) | 29 | yes — the climax |

Contingencies: if no paper presenter is confirmed, that ~20 min reclaims to a
fuller ethics block or retrospective breathing room; if a 4th project talk
appears, fold ethics into the retrospective's Bucket-4 walkthrough. Holder
slides make either adjustment a no-op.

## Block 1 — Ethics & adversarial (15 min, ~8–9 slides)

The spine: **the machinery you learned has a shadow.** Every tool this
semester — embeddings, inference, optimization — inherits or amplifies what it
learns from. Anchor on the required reading (Caliskan) and connect each beat
to a prior week, so ethics isn't bolted on but *falls out* of the course.

1. **Section break** — "The machinery has a shadow."
2. **Embeddings carry society's biases** (Caliskan et al. 2017, required):
   the *same word-vector geometry* from Week 11 (callback to
   vectors-and-spaces / the embedding widget) encodes human stereotypes —
   WEAT: flowers↔pleasant vs insects↔unpleasant *and* names↔race,
   career↔gender. figure: `embedding_bias.png` (words projected on a
   gender/valence axis). Poll option here.
3. **Fairness is a conditional-probability statement** (the intellectual
   core — callback to Part I): demographic parity, equalized odds,
   calibration each written as $P(\hat{Y}\mid\dots)$ equalities. Two-column:
   the three definitions.
4. **You can't have them all** — the impossibility result (Kleinberg et al. /
   Chouldechova): with unequal base rates, calibration + equalized odds can't
   both hold. figure: `fairness_impossibility.png` (a 3-node "pick 2"
   triangle). Punchline: fairness is a *modeling choice*, stated in the
   language this course taught.
5. **Adversarial examples** (port SP25 human-in-the-loop framing): a tiny,
   human-imperceptible perturbation flips the classifier — the model's
   learned geometry is brittle where ours isn't. figure: `adversarial.png`
   (Chibany-flavored: a sticker on the bento fools the kiosk from tonkatsu
   to hamburger). One-line: robustness is unsolved.
6. **Alignment = teaching values is an inference problem** (callback to
   Week 9 RLHF + Week 8 reward hacking): RLHF fits a reward from preferences
   (Bradley–Terry, Week 9); reward hacking (Week 8 positive-cycle poll)
   returns as the safety failure mode. One slide, pointer to Part IX
   `alignment-safety` chapter.
7. **Textbook pointer** — the Part IX chapters (adversarial, fairness, bias,
   alignment) carry the full treatment + capstones.

Poll (1, fast, commit-before-reveal): "A hiring model is equally accurate for
every group. Is it fair?" → reveal: not necessarily — equal *accuracy* is not
equal *error composition*; which fairness you get is a choice (impossibility).
[New for SP26 — no ethics quiz in the SP25 bank.]

## Block 2 — Semester retrospective (29 min, the climax)

Per PLAN.md's spec (pulse 3 / synthesis 15 / bridge 7 / close 4):

1. **Pulse (3 min)** — one slide: "Which paper surprised you most? Which will
   you re-read in a year?" A go-around, not a discussion.
2. **The map of the semester (15 min)** — THE centerpiece. figure:
   `semester_map.png` — a 2D grid, **Marr's level** (L1 what / L2 how / L3
   neural) × **computation type** (categories / structure / time /
   substrate-limits), with ~10 papers placed (one core per week W3–12). Then
   walk it, one sentence per paper. Anchors the PLAN names: T&G/Tenenbaum
   (L1), Abbott 2012 (L2, memory-as-random-walk), Pereira 2018 (L3, decoding
   meaning from fMRI). Lock: **Shohei Yoshida presented Tenenbaum & Xu 2000
   (Week 4)** — mark that node. Build the map as sibling reveals (axes → a
   few papers lit → full) so it lands, not a wall.
3. **The bridge — classical cog-sci → contemporary ML (7 min)**: a 6-row
   table, each row a connection taught this term:
   - hierarchical Bayes → **in-context learning** (Week 11 flagship; Xie/Ye)
   - inverse RL → **RLHF** (Week 9; Christiano)
   - Monte Carlo / variational → **diffusion & VI in LLMs**
   - Bayes nets / causal → **alignment & reward modeling**
   - Bayesian nonparametrics → **open-ended concept learning**
   - NN geometry + Caliskan/Buolamwini → **what alignment must defeat**
   Bilingual table slide (no figure).
4. **Close (4 min)** — "What you learned is a *toolkit*, not a fixed set of
   answers. You can now read a 2026 paper and see what problem it's solving."
   Thank-you. A final callback to Chibany (the mascot who just wanted to know
   what was for lunch, and got a whole science of inference).

## Figures to build (`make_figures.py`)

- `semester_map.png` — the 2D Marr×computation map, ~10 papers placed, dark bg,
  quadrant labels, a highlighted "presented" node. THE must-build asset.
- `embedding_bias.png` — words on a gender/valence axis (Caliskan/WEAT visual).
- `fairness_impossibility.png` — 3-criterion "pick 2" triangle (calibration /
  equalized odds / demographic parity), with the base-rate caveat.
- `adversarial.png` — bento + ε-sticker → kiosk flips class (Chibany-flavored).
- Bridge + fairness-definitions are TABLE slides (no figure).

## Widgets

None required (15-min budget). Optionally *reference* the Week 11
`vector-space` / `attention-lookup` widgets when discussing embedding bias
(bias lives in the geometry those widgets already show). No new widget for the
final time-starved session.

## Presentation holders (design)

- One `## [Paper presentation]{...} {.section-break}` holder (student-driven).
- Three `## [Final project presentation N]{...} {.section-break}` holders — a
  simple numbered set; the presenting student drives their own slides. A dim
  line reminds: 10 min + brief Q&A (rubric).

## Polls

- P1 (Block 1): the fairness poll above. Sourced new (no SP25 ethics quiz).

## Design / bilingual / QA

Refreshed design system (theme tokens, tick, cards, gutter). Bilingual EN/JA
throughout (poll fully bilingual; fragment wraps lang divs). American
spellings. Terms defined at first use (WEAT, demographic parity, equalized
odds, calibration, adversarial example, RLHF re-anchored from Week 9). Fill +
clip audit; structural review; JA toggle check. Publish + PLAN + homepage card.

## Textbook tie-ins (PLAN "Textbook Chapters" + closing slide)

Bk: adversarial examples · Bk: fairness formalisms · Bk: bias in data ·
Bk: alignment safety (all `ethics/` — Part IX, authored alongside this deck).
