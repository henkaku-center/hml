# Week 9 (Jun 26): Inverse RL

## Topics
- Inverse reinforcement learning (goal inference as inverse planning)
- Social cognition / Theory of Mind = IRL
- POMDPs & belief inference
- Teaching-as-inverse-planning & legibility
- IRL at scale: RLHF/DPO as IRL, CIRL, the LLM Theory-of-Mind debate

## SP25 Content
- **Slides:** Week09_IRLSocialCog.pptx, Week09_IRLPOMDPSocial.pptx (+ PDF) — kept as `slides/` reference; SP26 deck rebuilt from scratch (see below).
- **Transcript:** Week09_IRLSocialCogTranscript.docx
- **Wiki pages:** social-cognition-and-inverse-rl.html
- **Quiz:** "Social Cognition and Inverse Reinforcement Learning" (`archive/.../gb593d4394…`) — Q2 (which is NOT IRL) + Q1 (ToM functionalism) mined as live polls.

## Textbook Chapters
Planned (T3 series — next free weights after Ch 20–22; **authoring pending**). **Adapt the FINAL deck via `TEXTBOOK_HANDOFF.md`** — the deck was reordered "Recover → Teach → Align" after this PLAN's original block order, and the chapters follow the deck, not the old order:
- T3: inverse rl / recovering the objective — `intro2/23_inverse_rl_goal_inference.md` — goal inference (Bayes-rule anatomy, softmax, ill-posedness) **+ IRL methods** (MaxEnt → GAIL → AIRL); attribution Baker & Tenenbaum; Widgets A + D
- T3: pomdps, belief & teaching — `intro2/24_pomdps_belief_inference.md` — belief b(s), Tiger / α-vectors / decision-walk, then teaching / legibility / CIRL; Widgets B + C
- T3: modern rl / world models / alignment — `intro2/25_modern_rl_world_models.md` — RLHF/DPO as IRL (explain→model→code→example), LLM-ToM (skeptical), world models; clears the deferred Week-8 TODO; numpy-first/optional-JAX

## GenJAX Integration
**Done — 4 verified backbones** (genjax 0.10.3 + jax 0.5.3), one per major beat, each feeding the deck's runnable code-slides + figures:
- `genjax_goal_inference.py` ★ — invert the MDP; posterior over goals via `assess` (P(right)=0.54; freeze-frame 0.37→0.54; β-sweep flat→sharp).
- `genjax_tiger_pomdp.py` ★ — Tiger belief update (0.5→0.85→0.9698→0.9945; E[open-right] −6.50→+6.68).
- `genjax_legible_teaching.py` — efficient vs legible scored by observer posterior (legible 0.613 vs efficient 0.500 at step 1).
- `genjax_reward_from_prefs.py` — Bradley–Terry reward modeling = preference-based IRL (recovers A>B>C from 90 prefs).

## Contemporary ML Notes
- **IRL ↔ alignment:** RLHF & DPO framed as preference-based inverse RL (reward modeling); CIRL / assistance games (Hadfield-Menell 2016) as the alignment formalism; reward hacking = Week-8 positive cycle at scale.
- **Machine ToM:** ToMnet (Rabinowitz 2018) as amortized vs. Bayesian inversion.
- **LLM Theory of Mind (taught as a live debate, skeptical lean per instructor):** Kosinski 2024 / Strachan 2024 / Street 2024 (capability) vs. Ullman 2023 / Pang 2025 (perturbation failures, contamination). *Behavioral pass ≠ mechanism.* Seeds Weeks 11–13.

## Status
**SP26 lecture rebuilt & verified (not yet published).** Deck `week9-slides.qmd` (49 slides, bilingual EN/JA — 103 lang-ja blocks), 15 generated figures, 4 interactive widgets (browser-tested), 4 GenJAX backbones. Fill audit: **0 clips** (hard gate passed); under-fill flags are the centered-design + widget-iframe false positives. Student-persona clarity review run (non-math + CS personas) → micro-clarity fixes applied. **Remaining:** author textbook Ch 23–25; then publish (CI render + docs/index.html regen).

## SP26 artifacts (this directory)
```
RESEARCH_week9.md            deep-research report (cited; pedagogy + modern + POMDPs.jl)
week9-shared-outline.md       source of truth (timing, examples, polls, widget specs, chapter map)
week9-slides.qmd              the deck (theme [dark, sds.scss]; include week9-styles.html)
week9-styles.html             fill-the-slide layout (copied from Week 8)
make_figures.py               15 figures → images/ (numbers match the GenJAX backbones)
genjax_*.py                   4 verified GenJAX backbones (above)
widgets/                      goal-inference / pomdp-belief / showing-vs-doing / reward-recovery .html
images/                       figures + *-fallback.png (verified widget screenshots) + break-cat-week9.jpg
week9-audit/slide-fill.json   fill-audit output
```

## TODOs
- [ ] **Author the 3 textbook chapters** (Ch 23/24/25) — **start from `TEXTBOOK_HANDOFF.md`** (the final reordered spine, verified numbers, and chapter map) — per `textbook/CLAUDE.md` conventions (date frontmatter, `validate_code_blocks.py`, `*.ja.md` siblings, interwoven GenJAX cells, Colab links). Embed the 4 widgets via iframe. This also clears the root-`TODO.md` deferred **modern RL / world models** chapter (Ch 25).
- [ ] On chapter publish: cross-refs (notebook_guide.md ×3, glossary.md terms + chapter `*Glossary:*` lines, PLAN `T3:` lines) → regenerate `docs/index.html` via `python3 docs/_build.py`.
- [ ] Quiz mapping: `course/quizzes/README.md` lists Week 9 → "Monte Carlo Estimation" and the IRL quiz under Week 11 (an SP25-schedule carryover). Reconcile so the IRL quiz maps to this week.
- [ ] Native-speaker proof of the JA slide translations.
- [ ] Publish: CI render of the deck + widgets to GitHub Pages.
