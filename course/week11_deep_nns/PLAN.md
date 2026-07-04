# Week 11 (Jul 10): Deep Neural Networks & LLMs

## Topics
- Neural networks from the probabilistic tradition: connectionism, distributed representations
- Perceptron → gradient descent → the delta rule → backpropagation (= autodiff)
- Depth & nonlinearity (the XOR crisis and its resolution)
- Architecture as inductive bias (= prior): CNN → RNN → **attention → the transformer**
- Scaling laws, emergent abilities (with the mirage caveat)
- **In-context learning as implicit Bayesian inference — taught as a live, contested debate**
- RLHF bridge to alignment (→ Week 12)

## SP25 Content
- **Slides:** Week11_NNs1.pptx (+ PDF) — perceptron/backprop core ported; figures salvaged into `images/sp25/`
- **Transcript:** Week11_NNs1Transcript.docx
- **Wiki pages:** intro-to-nns.html (note: SP25's CNN/RNN slides were authored but never delivered)
- **Quiz:** the SP25 bank has NO neural-network quiz (verified) — recap polls drawn from "Intro to Bayes Nonparametrics"; mid-deck polls are new for SP26.

## Textbook Chapters
- Bk: vectors and spaces — `deep/vectors-and-spaces.md` (the zero-LA on-ramp; REQUIRED before the rest)
- Bk: from rules to weights — `deep/from-rules-to-weights.md`
- Bk: neural net fundamentals — `deep/neural-net-fundamentals.md`
- Bk: transformers attention — `deep/transformers-attention.md`
- Bk: llms in context learning — `deep/llms-in-context-learning.md`
- Bk: world models imagination — `deep/world-models-imagination.md`
  (Part VIII of the restructured textbook; stubs today, authored as Phase D — the
  deck and chapters share `week11-shared-outline.md`'s spine.)

## GenJAX Integration
- One backprop-is-autodiff beat: `jax.grad` shown as the reverse-mode autodiff that
  IS backpropagation (illustrative cell, course-identity callback).

## Contemporary ML Notes
- The whole deck is organized as the *fourth answer* to Week 10's "where does the
  hypothesis space come from?" — **learn the features** (ridge / BNP / GP fixed the
  kernel; neural nets learn it; at infinite width it circles back to the GP).
- The modernization payoff is the ICL-as-empirical-Bayes block, taught with its
  counter-evidence (Falck et al. 2024) — not as settled fact.
- Lake et al. (2017) is the required reading and the standing critical voice (a
  running scorecard), so the lecture teaches the machinery *and* its limits.

## Status
**SP26 deck built and QA'd (2026-07-04).** 53 slides / 7 blocks / 4 polls / 2 new
widgets. Fill audit + present-slide clip check: zero real clips (EN presentation
state). Bilingual EN/JA throughout (124/124 paired). Pedagogical-structure audit run.

## SP26 artifacts
```
week11-shared-outline.md            source of truth (timing, blocks, visual budget)
week11-slides.qmd                   the deck
week11-styles.html                  fill-the-slide + poll CSS (cloned from Week 10)
week11-slides.html                  GENERATED
make_figures.py                     10 new matplotlib figures
images/                             new figures
images/sp25/                        14 salvaged SP25 figures
widgets/xor-playground.html         NEW — 2-2-1 ReLU net on XOR, trainable + hand-shapeable
widgets/attention-lookup.html       NEW — attention as soft dictionary lookup, β slider
widgets/bias-variance-explorer.html reused from Week 10 (double-descent callback)
```

## TODOs
- [ ] Author the five Part VIII textbook chapters from this deck's spine (Phase D).
- [ ] If a student presenter is assigned (readings_map presenter: null as of Jul 4),
      place the presentation after Block 4 and compress the CNN/RNN slides (contingency
      in the outline).
