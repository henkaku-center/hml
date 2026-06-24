# Week 9 (Jun 26) — Slack discussion thread

**Topic:** Inverse reinforcement learning + social cognition (goal inference as inverse planning, teaching as inverse planning, POMDPs)
**Required reading:** Baker, C. L., Tenenbaum, J. B., & Saxe, R. R. (2007). *Goal inference as inverse planning.* Proc. CogSci.
**Reflection eligibility:** Week 9 is a reflection-eligible week (counts toward your 5-of-11). ~200 words, posted in-thread **before class Fri Jun 26**.
**No presenter this week** (`presenter: null`) — so the alternative papers below are open as reflection readings, same as Weeks 6–8.

---

## Root post (paste-ready) — Slack-native formatting

*🕵️ Week 9 reading discussion — running the agent backwards: from "what should I do?" to "what is she trying to do?"*

Last week we built reinforcement learning *forward*. An MDP — last week's Markov chain plus *actions* and *rewards* — turns a goal into a policy: tell it what you want, it tells you what to do. This week we run the camera backwards. You watch someone move through the world — a few steps, a hesitation, a detour around something you can't see — and you infer *what they wanted*. That inversion is *inverse RL*, and when the "agent" is another person, it's the computational story of *social cognition*: reading goals, beliefs, and intentions straight off of behavior. Friday we build it, then push into *POMDPs*, where you infer not just what someone wants but what they *believe*.

*Baker, Tenenbaum & Saxe (2007), _Goal inference as inverse planning_* (PDF: https://hml.chibatech.dev/readings/pdfs/Bakeretal2007.pdf) shows people a little animated agent moving through a simple maze toward one of several possible goals, freezes the clip partway, and asks: *where is it headed?* Their model casts the observer as a Bayesian who inverts a model of *rational* action — P(goal | path) ∝ P(path | goal) · P(goal), where P(path | goal) is exactly the MDP policy from last Friday, just run in reverse. The striking result: this inversion tracks human goal attributions trial by trial. We read intention, they argue, by assuming you're an (approximately) rational planner and asking "what goal would make these actions make sense?"

Post your *~200-word reflection as a reply in this thread before class Friday (Jun 26).* Not a summary — a reaction: something you found compelling, a doubt, or a connection to other work. A few prompts if you're stuck (pick one, or go your own way):

1. *The inversion is ill-posed.* A handful of steps is consistent with many goals — walking toward the door fits "leave," "answer it," and "block it" equally well. So where does a single confident answer come from? In the model, the *prior* P(goal) and the *rationality assumption* do the disambiguating. Is that a satisfying account of how *you* pin down someone's goal, or does it just relocate the mystery into the prior?
2. *What if the agent isn't rational?* Inverse planning assumes the observed agent is (noisily) optimal — it took the actions a good planner would. People are clumsy, distracted, and wrong. When the agent blunders, the model tends to infer a *weirder goal* to rationalize the blunder — the same move it uses to "explain" a detour as avoiding an unseen obstacle. Is "assume rationality, blame the goal" a bug, or is it the whole point?
3. *A mind, or a curve that fits?* The model predicts human goal judgments well. But "fits the judgments" and "this is the computation the brain runs" are different claims — the same tension as the Week 6 random-walk reading and the Week 8 dopamine reading. What in the paper pushes you toward the stronger reading, and what would you need to see before you'd believe a brain actually inverts a planner?
4. *Connect it back — then flip it once more.* (a) Inverse RL literally inverts the MDP from Week 8: forward RL maps goals → actions; this maps actions → goals. If you've started the RL assignment's GardenPath agent, what would it take to watch *its* trajectory and recover *its* reward function? (b) Now flip the flip: if I know you'll infer my goal from my actions, I can *choose* actions that make my goal obvious — that's teaching-as-inverse-planning (the Ho papers below). When you wave someone toward the exit, are you *acting*, or *communicating*?

Reply to _each other_, not just to me — a good doubt deserves a counter-reply. I'll jump in where it's useful.

*📖 You can write your reflection on any of these — pick whichever grabs you.* Baker et al. above is the default, but any of these are equally fair game for your discussion post:
- 🧠 Jara-Ettinger (2019), _Theory of mind as inverse reinforcement learning_ (https://doi.org/10.1016/j.cobeha.2019.04.010) — a short, recent review that says the quiet part out loud: the everyday *theory of mind* you use to read other people *is* IRL. The cleanest big-picture version of the whole week if you'd rather react to a framing than to one experiment.
- 👋 Ho, Littman, MacGlashan, Cushman & Austerweil (2016), _Showing versus doing: Teaching by demonstration_ (PDF: https://hml.chibatech.dev/readings/pdfs/Hoetal2016NIPS.pdf) — what changes when you know you're being *watched*? People *doing* a task and people *demonstrating* it move differently: demonstrators exaggerate and make the goal legible. Inverse planning run in the other direction. (Full disclosure: this one's from my own group.)
- 🔧 Ho, Littman & Austerweil (2017), _Teaching by intervention: Working backwards, undoing mistakes, or correcting mistakes?_ (PDF: https://hml.chibatech.dev/readings/pdfs/Hoetal2017.pdf) — when you correct someone mid-task — grab their hand, undo their move — what are you signaling? Extends teaching-as-inverse-planning into live correction; pairs with Friday's social-cognition thread.
- 🍎 Ho, Littman, Cushman & Austerweil (2015), _Teaching with rewards and punishments: Reinforcement or communication?_ (PDF: https://hml.chibatech.dev/readings/pdfs/Hoetal2015CogSciProc.pdf) — reward as a *signal* vs. as a *reinforcer*. (This was also offered as a Week-8 alternative — skip it if you already read it, but it's the paper the RL assignment's GardenPath world comes from, so it's doubly on-topic this week.)

---

## ⏰ Reminders (post as a follow-up reply, or fold into the root) — Slack-native formatting

A few deadline + looking-ahead notes:

*🗳️ The big one — your final-project proposal is due Sun Jun 28, 8:00 PM* (pass/fail), two days after class. ~1 page: background, the question you're asking, your method, and at least three references. Full guidelines: https://hml.chibatech.dev/project.html . If you're still deciding, this Friday's social-cognition / inverse-planning material is fair game for a topic. DM me if you want a sanity check on your idea before you write it up.

*🧩 Assignment 4 (Reinforcement Learning) is now out* — due *Fri Jul 10, 8:00 PM* (4.5%). Q-learning on the GardenPath grid: fill in the one-line TD update, watch a human-style feedback scheme create a *+14/lap* reward-hacking loop that never reaches the goal, then fix it the principled way with potential-based shaping. PDF + GenJAX/Python/R stencils (and an interactive widget to play with first) are on the assignments page: https://hml.chibatech.dev/assignments.html . It's the same GardenPath world from last Friday's demo — and, fittingly, from this week's Ho (2015) reading.

*🗓️ Heads-up — two programming assignments land on the same day.* Both the *Monte Carlo* exercise (10.5%) and the *RL* assignment (4.5%) are due *Fri Jul 10, 8:00 PM*. With the proposal due Jun 28 in between, spread the work across the next two weeks rather than stacking it all on Jul 9. Reminder: you have 3 free late days pooled across the four programming assignments.

*🎤 Looking ahead:* paper presentations resume soon — Imai in Week 11 (word2vec), Tenzin in Week 12 (AI hyperrealism). If that's you and you want the optional 1-on-1 prep meeting, DM me at least a week before your slot.

---

## Speaker / facilitation notes (not for Slack)

- **Formatting:** the paste-ready Root post + Reminders above are in *Slack-native* syntax (`*bold*`, `_italic_`, bare auto-linking URLs, no `>` blockquote) — copy them straight into Slack. Standard markdown (`**bold**`, `[text](url)`) pastes as literal characters into Slack's composer. These facilitation notes are not pasted, so they stay in plain markdown. (Same convention as the Week 7 and 8 threads.)
- **All four reading PDFs are live** at `https://hml.chibatech.dev/readings/pdfs/` (verified present in `docs/readings/pdfs/`: `Bakeretal2007.pdf`, `Hoetal2016NIPS.pdf`, `Hoetal2017.pdf`, `Hoetal2015CogSciProc.pdf`). Jara-Ettinger (2019) is linked by DOI — it has no PDF in the repo (`url:` in `readings_map.yml`, no `pdf:` field).
- **The thread is built on the Week 8 → Week 9 hinge** (forward RL → inverse RL). Week 8 ran the MDP forward (goals → policy → actions); this week inverts it (actions → goals), and the root post's opener cashes out that arc. "P(path | goal) is the MDP policy run in reverse" is the literal connective tissue — students who did the Week 8 reflection should feel the continuity, and prompt 4(a) makes the inversion concrete against the GardenPath agent they're coding this week.
- **Required reading is Baker, Tenenbaum & Saxe (2007)** (`required` in `readings_map.yml`) — the canonical goal-inference-as-inverse-planning paper. It tees up Friday's social-cognition block directly and sets up the POMDP extension (goal inference → belief inference under partial observability).
- **Prompt → lecture mapping** (each prompt seeds a slide so an in-thread bite is a free lead-in):
  - Prompt 1 (ill-posed inversion / the prior does the work) → the Bayesian-inversion setup slides; also the natural lead-in to POMDPs, where the hidden variable is the agent's *belief*.
  - Prompt 2 (rationality assumption / blaming the goal) → the noisy-rationality / softmax-policy thread, and the "infer an unseen obstacle to explain a detour" demo from Baker et al.
  - Prompt 3 (mechanism vs. fit) → deliberately reuses Week 6 prompt 1 and Week 8 prompt 3; good to call on as the recurring epistemics question of the course.
  - Prompt 4 (invert the MDP / teaching as inverse planning) → bridges to the RL assignment (recover a reward function from GardenPath trajectories) and forward to the teaching alternatives (Ho papers) and the Weeks 11–13 alignment thread.
- **Four alternative readings in the thread, opened because `presenter: null`** (same treatment as Weeks 6–8). All four are `presentation_candidates` in `readings_map.yml`; all fit the inverse-planning / theory-of-mind spine, so none were dropped:
  - **Jara-Ettinger (2019)** — featured first as the cleanest big-picture framing (ToM *is* IRL). DOI-only.
  - **Ho et al. (2016)** — Austerweil's own; teaching-by-demonstration as inverse planning run the other way (legible vs. efficient action).
  - **Ho et al. (2017)** — teaching by live intervention; the correction-as-signal extension.
  - **Ho et al. (2015)** — *deliberately retained despite the Week-8 overlap.* It was a featured Week-8 alternative (reward as communication vs. reinforcement), and it's a Week-9 presentation candidate. The in-thread note tells students who already read it to skip — but it's flagged as doubly on-topic here because the RL assignment's **GardenPath domain is from this exact paper** (`\citep*{ho15}` in `rl.tex`). Not a stealth duplicate; the overlap is called out.
- **POMDP angle is set up but not pre-empted.** Friday pushes past goal inference into *belief* inference (POMDPs — inferring what the agent knows, not just what it wants). Prompts 1 and 2 both lead there. If a student raises "but what if the agent has wrong/partial information?" in-thread, that's a free lead-in to the POMDP block — don't resolve it fully in replies.
- **Deadline facts verified before posting:**
  - *Final-project proposal due Sun Jun 28, 8:00 PM* (pass/fail) — `docs/assignments.html` (and the Week 7/8 threads). This is the headline item for Week 9: it's due two days after class.
  - *RL assignment (Assignment 4) is now published* — `course/assignments/rl/rl.pdf` + GenJAX/Python/R stencils are in the repo and on the assignments page (commits `397bf17`, `26bc6c9`). The Week-8 thread said it "releases next week"; it has. Due **Fri Jul 10, 8:00 PM** (4.5%), per `rl.tex` and `assignments.html`.
  - *+14/lap* is the **net reward per lap of the reward-hacking loop** (authoritative figure on `assignments.html`); the *+20* in `rl.tex` is the one-time goal reward — different quantities, don't conflate. The thread uses +14/lap for the loop.
  - *Monte Carlo assignment also due Fri Jul 10, 8:00 PM* (10.5%) — `assignments.html`. Both programming assignments land the same day; the thread flags this so students pace around the Jun 28 proposal.
- Normal reflection-eligible week (Weeks 2–12 eligible; Week 1 is not). No need to restate the 5-of-11 rule unless someone asks.
