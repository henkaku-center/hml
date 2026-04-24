# SP26 Syllabus

- **Course:** Human and Machine Learning
- **Institution:** Chiba Institute of Technology, School of Design & Science (SDS)
- **Instructor:** Prof. Joseph Austerweil
- **Term:** Spring 2026 (Apr 17 – Jul 17, 2026; no class May 1 or May 8)
- **Format:** Seminar, 12 Friday sessions, 2 hours each
- **Enrollment:** ~6 students
- **Language:** English

---

## Course description

A graduate seminar on *computational cognitive science*: the study of the mind as an information-processing system that performs inference, learning, and decision-making under uncertainty. The course covers Bayesian foundations, hierarchical and causal models, Markov chains and Monte Carlo methods, reinforcement learning and inverse reinforcement learning, Bayesian nonparametrics, and connections to contemporary machine learning (deep neural networks, ethics, adversarial ML). Throughout, we use the probabilistic programming language [GenJAX](https://github.com/ChiSym/genjax) to move fluidly between mathematical models and executable code.

The companion textbook is [*A Narrative Introduction to Probability*](https://josephausterweil.github.io/probintro/), a free, open-source resource written alongside this course.

## Learning goals

Students who successfully complete the course will be able to:

1. Understand state-of-the-art machine learning techniques in the context of probabilistic modeling.
2. Formulate a probabilistic model of a problem the human mind solves — ideally one relevant to the student's own research interests.
3. Analyze how model assumptions (explicit or implicit) enable learning.
4. Think critically about the role of computational modeling in explaining human behavior.

## Prerequisites

- Graduate standing, or instructor consent.
- Comfort with basic probability and statistics.
- Programming experience. The course uses Python / GenJAX / Colab; prior experience with another language is fine.
- Linear algebra is helpful but not required.

## Grading scheme

| Component | Weight | Notes |
|---|---|---|
| Final project | **50%** | Proposal 5% · In-class presentation 7.5% · Final paper 37.5% |
| Programming assignments (4) | **30%** | Clusters 7.5% · Generalization 7.5% · Monte Carlo 10.5% · RL 4.5%. All in GenJAX. |
| Weekly written reflections | **12.5%** | ~200 words on one assigned reading, pre-class. 6 of 12 required (student's choice). Pass/fail each. |
| Paper presentation | **7.5%** | One 20-minute presentation of an assigned reading, followed by ~15 minutes of discussion you facilitate. See the "Paper presentations" section below. |
| Quizzes | **0%** | Self-check only, available via the textbook. |
| **Total** | **100%** | |

Assignment weight rationale: the Monte Carlo assignment is weighted highest because it is the most demanding; the reinforcement-learning assignment is lightest because it comes with the most scaffolding code.

With ~6 students in a seminar, attendance is self-evident and the paper presentation serves as the visible engagement signal — so participation is folded into those two components rather than graded separately.

## Final project

The project is the capstone of the course and the largest single grade component. It is an opportunity to explore a question related to human and machine learning that the student is personally interested in. The project does not need to use a specific topic or technique from class.

Three (non-exclusive) categories of project:

1. **Experiment** — conduct a behavioral experiment that tests a prediction of a model from class (or a straightforward extension).
2. **Modeling / ML** — take some human behavior (from class, from the literature, or from data you scrape) and model it with your own or an advanced ML method.
3. **Math / theory** — a mathematical analysis of a learning problem or model.

Project deliverables:

- **Proposal** (~1 page, due mid-semester; exact date announced in class): background, question, method, and at least three references. Pass/fail.
- **In-class presentation** (late semester): ~10 minutes. Background, question, method, preliminary results.
- **Final paper** (~6 pages single-spaced): motivate and present your results clearly. Detailed guidelines will be announced.

## Weekly written reflections

Each week, students write a ~200-word reaction to one of the assigned readings. Reflections are not summaries — they are thoughtful engagements (a point you find compelling, a doubt, a connection to other work). Submit before class. Students choose any 6 of the 12 weeks. Pass/fail each.

## Paper presentations

Each student gives one 20-minute presentation of an assigned reading, followed by 10–15 minutes of discussion that the presenter facilitates. Presentations are slotted across Weeks 4–12; signup happens in Week 2 class.

The focus of the presentation is **how the mathematical model connects to cognitive science, and the evidence the authors provide for that connection**. Plan to meet with Joe in office hours at least one week before your slot.

Grading (out of 5 points):

| Criterion | Points |
|---|---|
| Understanding of the paper | 1.5 |
| Covering key aspects of the paper | 1.5 |
| Presentation clarity | 1.0 |
| Appropriate discussion questions (at least 3) | 0.5 |
| Appropriate use of time | 0.5 |

Useful framing questions (adapted from Tom Griffiths — use these to organize your talk):

1. What is the cognitive science question the paper explores?
2. What is the context — what previous approaches exist?
3. What is the underlying computational problem, and how does the paper formulate it?
4. What is the solution the paper presents? Explain the core mathematical ideas clearly (intuition over rigor).
5. How does the solution connect to human behavior — how does the model compare to human performance?
6. What can we conclude? What is your own interpretation?

See `resources/classPresentationGuidelines.pdf` for the full SP25 guidelines (reused for SP26).

## Policies

### Late work

- If you have a serious illness, please contact Joe as soon as possible. Once you are feeling well enough, we will decide together on a set of revised course deadlines.
- You get 3 *free* late days that can be used across the programming assignments.
- For other coursework, late work is not accepted (except for serious illness or other life emergencies). For weekly written reflections, just do a different week. If you will need to be late, please notify Joe as soon as possible.

### AI tools

You are welcome to use AI tools (ChatGPT, Claude, Copilot, etc.) as a resource for technical problems — debugging, looking up syntax, understanding a new concept. The real bar is understanding, not provenance:

- **You must understand everything you submit** well enough to defend and discuss it orally, without AI assistance. If you can't explain what your solution does and why, it isn't really yours yet — keep working on it before submitting.
- **You are responsible for everything you submit.** If an AI tool produces something incorrect and you turn it in, the mistake is counted as yours.

### Plagiarism

All submitted work will be checked. Do not plagiarize. Self-plagiarism (reusing your own work from another class without explicit permission) also counts. Plagiarism cases are handled individually.

### Email

I do my best to respond within 36 hours (48 on weekends). Please keep emails clear and concise.


## Office hours

We are still deciding on whether there will be explicit office hours. If you would like to meet, please email Joe to schedule a 1-1 meeting.

## Textbook and readings

- **Textbook:** [*A Narrative Introduction to Probability*](https://josephausterweil.github.io/probintro/) — free, with interactive notebooks.
- **Weekly primary readings** drawn from the computational cognitive science and machine learning literature. The reading list lives in `course/readings_map.yml` and is published to the course website as it is finalized week by week.

## Tools

- **Google Colab** for all GenJAX work. No local installation required.
- **GenJAX** — a probabilistic programming language on JAX. Introduced Week 2; used throughout.
- The companion textbook includes tutorials for Colab setup and GenJAX basics (Tutorial 2, Chapters 0-1).

---

*This syllabus is provisional and may be adjusted as the semester progresses. Any changes will be announced in class and reflected on the course website.*
