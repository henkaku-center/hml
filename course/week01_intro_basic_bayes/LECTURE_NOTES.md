# Week 1 — Lecture Notes

Teaching notes for the 2-hour SP26 Week 1 session. See `PLAN.md` for the block-level structure; this file is the running-room copy: exact prompts, worked numbers, expected student responses, and slide-by-slide reference into the SP25 decks.

**SP25-reference decks** (under `slides/sp25_reference/`): `Week00_intro_and_admin.pptx`, `Week00_BasicBayes.pptx`. All slide numbers below refer to these. These are reference material only — the SP26 deck for the session will live in `slides/sp26/` when built.

---

## Block 1 — Welcome + framing (5 min)

Keep brief. Avoid opening with policies.

- Course title: "Human and Machine Learning."
- Schedule: 13 Fridays, Apr 17 – Jul 17, 2026; no class May 1.
- Student round-robin. Prompt each: **"Your name, your background, and one thing you're hoping to get out of this course."** With 2-4 students this gives you real diagnostic signal — note who sounds more math/CS vs. cog sci and adjust Block 3 emphasis on the fly.

---

## Block 2 — Inductive inference (25 min)

### Checkershadow illusion (6 min)
SP25-ref `intro_and_admin` slides 2-4.

- Slide 3: show the image. **Ask: "Which square is darker, A or B?"** Don't reveal.
- Reveal with the connecting bar image (the standard "same gray" demo — slide 4 has it conceptually).
- Debrief script: *"Your visual system just solved `? + ? = 5`. The retinal image is the 5; the two things to the left of `=` are the square's actual color and the shadow. The visual system is making the best guess it can under ambiguity — and it's committed enough to override what the pixels literally show."*

### Heider-Simmel video (8 min)
SP25-ref `intro_and_admin` slides 10-11. Video link: https://www.youtube.com/watch?v=VTNmLt7QX8E

- Play ~90 seconds (not the whole thing).
- **Ask: "Describe what happened."** Let each student answer.
- They'll spontaneously use mental-state language ("the big triangle was bullying," "she was scared," "they escaped"). That's the point.
- Debrief: *"None of those things were in the video. Shapes moved on a plane. Your mind inferred goals and beliefs from pure motion. What's the hidden variable? What's the data?"*
  - Hidden: goals / intentions / relationships.
  - Data: 2D motion trajectories.

### Concept/word learning — "jumbuck" (8 min)
SP25-ref `intro_and_admin` slide 14 (Quine's rabbit).

- Setup: *"You're in the Australian outback. Someone points at a hopping animal and says 'jumbuck.' What does 'jumbuck' mean?"*
- Expected first answer: "kangaroo" or "rabbit" (the animal itself).
- Then push: *"Why not 'undetached kangaroo parts'? Or 'the temporal cross-section of a kangaroo at this instant'? Or 'mammal'? Or 'dinner'?"* These are all logically consistent with the one example.
- Payoff: **The child must bring strong prior expectations about what words mean — which constrain the hypothesis space before any evidence arrives.** We'll formalize "hypothesis space" and "prior" in a few minutes.

### Check-in (3 min)
**Ask: "What's the common structure across all three?"**

Target: hidden variable `h` + noisy/sparse data `d` + prior knowledge → best guess about `h`.

Write on board, don't explain yet:
```
P(h | d) ∝ P(d | h) · P(h)
```
Say: *"By the end of the next hour you'll know what every symbol here means and why the proportion holds."*

---

## Block 3 — Basic Bayes foundations (25 min)

Compact-but-rigorous. Map to SP25-ref `BasicBayes` slides 3-13.

### Sets, events, event space (5 min) — slides 3-5
Two-coin-flip running example.
- Outcome set `S = {HH, HT, TH, TT}`.
- `|S| = 4`.
- Event = subset of S. *"At least one head"* = `{HH, HT, TH}`.
- Event space = set of events (powerset for finite `S`). Mention continuous case briefly; defer.

### Random variables (4 min) — slide 6
*"A random variable is a function from the outcome space to some value space."*
- Example: `Y` = "at least one H" maps outcomes to `{True, False}`.
  - Y(HH) = T, Y(HT) = T, Y(TH) = T, Y(TT) = F.
- **Key framing for math/CS students:** "It's literally a function. Nothing mysterious — the word 'random' is about the input, not the mapping."

### Joint probability (3 min) — slide 8
Probability of multiple RVs taking specified values.
- Example: P(first coin = H AND second coin = T) = 1/4.

### Conditional probability as set restriction (5 min) — slides 9-11
**The pedagogical moment of this block.** Do it on the board, not from slides.

Draw the 2×2 grid:
```
HH  HT
TH  TT
```
- *"What's P(first = H | at least one H)?"*
- **Students often say 3/4 (outcomes with at least one H that also have first=H, over all outcomes). The correct answer is 2/3.**
- Walk through: conditioning = restricting the universe. The new universe is `{HH, HT, TH}` (3 outcomes). Of those, 2 have first = H. So 2/3.
- Then give the ratio definition:
  ```
  P(A | B) = P(A ∩ B) / P(B)
  ```
  Confirm: P({first=H} ∩ {≥1 H}) = P({HH, HT}) = 2/4; P(≥1 H) = 3/4; 2/4 ÷ 3/4 = 2/3. ✓

### Marginalization (3 min) — slide 12
`P(X) = Σ_c P(X, C=c)`. One sentence, then move on.

### Bayes' rule derivation (5 min) — slide 13
One line on the board:
```
P(A | B) P(B) = P(A, B) = P(B | A) P(A)
                                              ⟹  P(A | B) = P(B | A) P(A) / P(B)
```
Have students confirm each equality. This is the product rule + symmetry — nothing else.

### Check-in (3 min)
**Ask: "In the cab problem I'm about to give you, what's `d` and what's `o`?"** (Primes next block without revealing the answer.)

---

## Block 4 — Bayes in action (35 min)

### Sick-friend intuition (10 min) — SP25-ref `BasicBayes` slides 15-26

Setup from slide 15:
- 50-year-old friend, chain smoker since 18.
- Nasty cold going around.
- You hear them cough.
- Three hypotheses: cold, stomach virus, lung cancer.

**Do it qualitatively first** (slide 21 table). Have students fill in on the board:

| | Prior | Likelihood P(cough \| d) | Prior × Likelihood |
|---|---|---|---|
| Cold | **high** (cold going around) | **high** | high |
| Stomach virus | medium | low | low |
| Lung cancer | **medium** (smoker) | **high** | medium |

Then put numbers on it (slide 23):
- Priors: cold 0.45, stomach virus 0.10, lung cancer 0.10.
- Likelihoods: P(cough | cold) = 0.9, P(cough | stomach virus) = 0.45, P(cough | lung cancer) = 0.9.
- Numerators: 0.405, 0.045, 0.090. Sum = 0.540.
- Posteriors: **0.75, 0.083, 0.167**.

**Pedagogical punchline:** Even though the friend is a chain smoker, the posterior probability of lung cancer is ~17% — not the dominant hypothesis. The cold wins at 75% because its prior is ~4.5× larger (colds are going around; lung cancer is rare in any given week, even for smokers) *and* it has a high likelihood. The point: *priors are not enough — likelihoods matter. And neither is enough alone: you need the full rule.*

### Kahneman-Tversky cab problem (20 min) — SP25-ref `BasicBayes` slides 32-41

Setup from slide 32:
- Two cab companies: Blue (15%) and Green (85%).
- Hit-and-run at night; a witness identifies the cab as **blue**.
- Witness is correct 80% of the time.
- **What's P(cab is blue | witness said blue)?**

**Pass 1 — cold attempt (3 min).** Ask students to commit to a number before any math. Most will say something in the 70-80% range (the witness's accuracy). Write predictions on board.

**Pass 2 — area diagram (5 min) — slides 37-39.** Concrete counting:
- Imagine 100 cabs. 85 green, 15 blue.
- Of the 15 blue: witness correctly says "blue" for 80% × 15 = **12**.
- Of the 85 green: witness incorrectly says "blue" for 20% × 85 = **17**.
- Total "blue" reports: 12 + 17 = 29.
- P(cab is blue | witness says blue) = 12/29 ≈ **41%**.

Reaction: students are typically surprised it's below 50%.

**Pass 3 — formal Bayes (7 min).**
- Observation `o` = witness says blue (W=b).
- Hypotheses: B (blue) with prior 0.15, G (green) with prior 0.85.
- Likelihoods: P(W=b | B) = 0.80; P(W=b | G) = 0.20.
- Numerators: P(B) · P(W=b | B) = 0.15 × 0.80 = 0.12. P(G) · P(W=b | G) = 0.85 × 0.20 = 0.17.
- Denominator: 0.12 + 0.17 = 0.29.
- Posterior: P(B | W=b) = 0.12 / 0.29 ≈ **0.41**. Same answer — intentional. Show the algebra and area diagram are the same computation.

**Pass 4 — discussion (5 min) — slides 34-35.**
- **Ask: "Why do people neglect the base rate?"** Let them speculate.
- Name it: *base-rate neglect* (Kahneman & Tversky, 1972; Bar-Hillel, 1980).
- Framing: *heuristic* (rule of thumb, usually works) vs. *bias* (knowledge that produces errors when misapplied).
- Preview: coming weeks look at when people *do* show Bayesian behavior — framing, causal structure, and representation all matter.

### Synthesis (5 min) — SP25-ref `BasicBayes` slide 43

Put on board the 5-step Bayesian-modeling recipe:

1. Formalize the problem people face.
2. Formalize the knowledge they bring to it.
3. Apply Bayes' rule — compute what an ideal learner would infer.
4. Characterize that ideal learner's behavior.
5. Identify what knowledge (and what constraints on learning/inference) must be assumed for model and human behavior to match.

*"This is the course's method. Every week we pick a different cognitive domain and run this loop."*

---

## Block 5 — GenJAX + admin + homework (20 min)

### GenJAX orientation (10 min)

Have Colab open and ready. Share screen.

**Frame (30 sec):** *"Bayes' rule is easy to write. Enumerating all the hypotheses is usually not. And once you have continuous distributions, you can't enumerate them at all. GenJAX is a programming language for probability — you write the generative process as code, and the machine does the enumeration and counting for you."*

**Live example (~5 min).** Type this, don't paste. From `textbook/content/genjax/02_first_model.md`:

```python
import genjax
from genjax import gen, flip

@gen
def chibany_day():
    lunch = flip(0.5) @ "lunch"
    dinner = flip(0.5) @ "dinner"
    return (lunch, dinner)
```

As you type:
- `@gen` — *"This decorator tells GenJAX: 'what follows is a generative model, not a regular function.'"*
- `flip(0.5)` — *"A Bernoulli random variable. Probability 0.5 of True."*
- `@ "lunch"` — *"This names the random choice. We'll use those names later to condition — to ask 'given we observed lunch happened, what's the distribution over dinner?'"*
- *"This function IS the outcome space Ω we drew on the board 20 minutes ago. Every run samples one point from Ω."*

Run `chibany_day()` a few times. Show the output looks like `Array(0, dtype=int32), Array(1, dtype=int32)`. Preempt confusion: *"JAX displays arrays even for scalars. Treat them as 0s and 1s."*

**Preemptive callouts (~2 min):**
- *"Use `flip(p)`, not `bernoulli(p)`. If you write `bernoulli(0.9)`, you'll get True ~71% of the time, not 90% — `bernoulli` takes a **logit**, not a probability. It's a known foot-gun."*
- *"The `@` operator here is not matrix multiplication. GenJAX overloads it."*
- *"Everything runs in Google Colab. No local install, no conda env. Just open the notebook."*

**Pointer (~2 min):** *"For next week, read Tutorial 2 Ch 0 and 1 in the textbook. Ch 0 walks through Colab setup; Ch 1 is the minimum Python you need to read GenJAX code. You're not learning Python from scratch — you're learning to read a language that happens to look like Python."*

### Admin (7 min)

Walk through the grading table from `PLAN.md`. Keep it brief — the written syllabus will have the full version.

Emphasize:
- **50% final project.** Start thinking about topics now. Proposal due mid-semester (exact date TBD).
- **30% programming assignments.** All four in GenJAX.
- **15% weekly written reflections.** ~200 words, pre-class, ~8 of 13 required. This replaces the SP25 paper-presentation format — with 2-4 students, written works better than formal talks.
- **5% participation.** Show up, engage.
- **0% quizzes.** They exist in the textbook as self-check, not graded.

Note verbally:
- Office hours: TBD — I'll send a poll.
- AI policy: welcome as a resource for technical problems; must cite; **not for quiz/assignment answers**. Full policy in the written syllabus.
- Email: best-effort 36-hour response; 48 hours on weekends.

### Homework (3 min)

Post on Canvas/course site after class:
1. Read **T1 Ch 1-3** — `textbook/content/intro/01_goals.md`, `02_hungry.md`, `03_prob_count.md`. Reinforces what we did in Block 3.
2. Read **T2 Ch 0-1** — `textbook/content/genjax/00_getting_started.md`, `01_python_basics.md`. Gets GenJAX running in Colab before Week 2.
3. Think about a final project topic — we'll talk briefly Week 2.

Week 2 has a short quiz ("Intro Probability Theory 1"), self-check only.

---

## Contingencies

- **Class is quiet / students slow to engage:** lean harder on the checkershadow and sick-friend examples; they produce visible reactions. Cut the jumbuck discussion short.
- **Class runs long:** skip the 5-step recipe slide in Block 4's synthesis — mention it verbally in Block 5 instead. Don't skip the cab problem.
- **Class runs short:** use buffer time to pull the monty-hall or medical-testing classic forward from Week 2 as a second cab-problem analog; or extend Q&A on GenJAX.
- **A student pushes on continuous probability:** acknowledge, point at T1 Ch 4-5 (Week 2), defer.
- **A student asks about the project:** give the elevator version ("you pick a question, formalize it as a model or experiment or both, write a 6-page paper"), promise more in Week 2 or Week 3.
