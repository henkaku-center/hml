# Week 2 (Apr 24): Levels of Analysis + Bayes Continued

## Topics
- **Meet Chibany** — bento scenario introduced in class (no pre-read assumed beyond T1 Ch 4–5)
- Marr's three levels of analysis (compressed to 7 min — a framing unit, not the centerpiece)
- Notation lock-in: H (hypothesis) / D (data) — fixed for the rest of the course
- **Week 1's sick-friend problem reframed in H/D notation** (explicit bridge from Week 1)
- Joint, marginalization, and conditional from the Chibany 2×2 bento table
- Expected value, Bernoulli, Binomial (with a real PMF plot)
- Continuous probability: PMF → PDF (with a visualization), the Gaussian formula (with a visualization), two Gaussian likelihoods visualized
- Bayes with a continuous likelihood (worked: weight = 450g posterior)
- **Gaussian-Gaussian conjugate update** — motivated, derived via completing-the-square, posterior curve visualized, precision visualized, N-observation generalization as its own build-up. Launchpad for Week 3.
- Paper presentation rubric + signup (Weeks 4–12)
- SP26 syllabus updates: 12 sessions, 6-of-12 reflections, presentations as a new grade component

## SP25 Content
- **Slides:** `slides/sp25_reference/Week01_levelsofanalysisBasicBayes2.pptx` (+ PDF). Retained as reference only. SP25's second-half math content (expected value, continuous prob, Gaussian, Gaussian-Gaussian update) is the structural basis for SP26 Blocks 5–7.
- **Wiki pages:** `wiki_pages/admin-+-levels-of-analysis.html`, `wiki_pages/basic-bayes-2.html`, `wiki_pages/first-paper-presentation.html` (the last is functionally replaced by Block 8 of the SP26 session).
- **Quiz:** "Intro Probability Theory 1" — available as ungraded self-check, covers Block 4 material.

## Textbook Chapters
- T1 Ch 4–5: `intro/04_conditional.md`, `intro/05_bayes.md` (required reading before class — reinforces Week 1)
- T3 Ch 1: `intro2/01_mystery_bentos.md` — source of the Chibany bento scenario used throughout
- T3 Ch 2–3: `intro2/02_continuous.md`, `intro2/03_gaussian.md` — useful companion reading for Blocks 6–7

## GenJAX Integration
- T2 Ch 0–1 (Getting started / Python basics) — required reading before class; GenJAX Colab setup is self-directed
- **No live GenJAX demo this session.** Class time is devoted to math foundations (PMF → PDF → Gaussian → Gaussian-Gaussian conjugacy) so Week 3 can open with conjugacy proper. GenJAX model-building returns in Week 4.
- Homework for Week 3: continue T2 Ch 2–4 on students' own time

## Contemporary ML Notes
None this week. Week 2 is foundations; contemporary content enters at Weeks 11–12.

## Status
SP26 artifacts built. 105-slide deck with sequential-reveal math build-ups (SP25 style) + six pre-generated matplotlib figures for continuous-probability and Gaussian content. Ready to run Friday Apr 24.

## SP26 artifacts
- **Shared outline:** `week2-shared-outline.md` (source of truth for timing and content)
- **Build script:** `build_slides_week2.py` (uses `sds_slides.SDSDeck.build_slides()` for multi-step math reveals and `content_image_slide()` for figures; speaker notes embedded as `notes=` kwargs per step)
- **Figure generator:** `generate_images.py` (produces `images/*.png` via matplotlib — re-run when figure parameters change)
- **Figures:** `images/pmf_to_pdf.png`, `gaussian_shape.png`, `tonk_hamb.png`, `precision.png`, `gg_update.png`, `binomial_pmf.png`
- **Slide deck:** `slides/sp26/week2-slides.pptx` (105 slides; generated — do not hand-edit)
- **Speaker notes:** `week2-speaker-notes.md` (generated from build script — do not hand-edit)
- **Branding asset:** `sds_branding.svg` (source of the yellow frame + SDS wordmark PNGs)
- **Helpers added to `sds_slides.py`:**
  - `SDSDeck.build_slides(title, steps, notes)` — sequential-reveal body content
  - `SDSDeck.content_image_slide(title, image_path, caption, notes)` — title + centered PNG + caption

## TODOs
- [ ] After class: transcribe paper-presentation signups into `course/readings_map.yml` `presenter:` fields
- [ ] After class: refresh `week2-shared-outline.md` "Contingencies" section with anything that actually came up during delivery
- [ ] Re-run `generate_images.py` any time figure parameters change; re-run `build_slides_week2.py` to rebuild deck + notes
- [ ] If Block 7 lands for students, push the same build-up + pre-generated-figure style into subsequent weeks as they're built
