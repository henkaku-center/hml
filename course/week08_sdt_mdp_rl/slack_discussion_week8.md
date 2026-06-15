# Week 8 (Jun 19) — Slack discussion thread

**Topic:** Statistical decision theory → Markov decision processes → reinforcement learning (value iteration, Q-learning, reward shaping & positive cycles, simulation-based RL)
**Required reading:** Daw, N. D., Niv, Y., & Dayan, P. (2005). *Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control.* Nature Neuroscience.
**Reflection eligibility:** Week 8 is a reflection-eligible week (counts toward your 5-of-11). ~200 words, posted in-thread **before class Fri Jun 19**.
**No presenter this week** (`presenter: null`) — so the alternative papers below are open as reflection readings, same as Weeks 6 and 7.

---

## Root post (paste-ready) — Slack-native formatting

*🤖 Week 8 reading discussion — from "what should I believe?" to "what should I do?"*

For seven weeks we've done *inference*: given the data, what should you _believe_? Friday we make the jump to *agency*: given the world, what should you _do_? The machinery is a Markov decision process — last week's Markov chain, plus *actions* (you pick which transition to take) and *rewards*. If you _know_ the world's dynamics you can plan the optimal policy by sitting and simulating (*value iteration*). If you _don't_, you learn one from experience (*Q-learning*). This week's reading asks whether your brain runs *both*.

*Daw, Niv & Dayan (2005), _Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control_* (PDF: https://hml.chibatech.dev/readings/pdfs/Dawetal2005.pdf) proposes that behavior is arbitrated between two controllers: a *model-based* system that builds a map of the world and plans on it (flexible, but slow and expensive) and a *model-free* system that just caches "how good was this action last time" (fast and cheap, but rigid). Their twist: the brain trusts whichever system is *more certain* on a given decision. Habits are the cached system winning; deliberation is the planner winning. The same model-based/model-free split *is* the two halves of Friday's lecture.

Post your *~200-word reflection as a reply in this thread before class Friday (Jun 19).* Not a summary — a reaction: something you found compelling, a doubt, or a connection to other work. A few prompts if you're stuck (pick one, or go your own way):

1. *Why two systems?* It seems wasteful — why would a brain run a cheap-but-rigid learner _and_ an expensive-but-flexible planner instead of one good system? What does each one buy you that the other genuinely can't? (Map it to Friday: value iteration on a _known_ MDP is the planner; Q-learning on an _unknown_ one is the cacher.)
2. *Is uncertainty the right referee?* The paper's specific claim is that the two systems compete and the _more certain_ one wins. Is "whichever is more confident" the right currency for arbitration? What would a simpler story (habit strength, how recently you were rewarded) predict differently — and is there an experiment that would actually tell them apart?
3. *Where's the algorithm in the brain?* The model-free system learns from a _prediction error_: the gap between the reward you expected and the reward you got (the TD error). Dopamine neurons look uncannily like that signal (Schultz, below). How convincing is "the brain is literally running this algorithm" versus "this algorithm fits the recordings"? What would move you from the weaker claim to the stronger one? (Same mechanism-vs-fit tension as the Week 6 random-walk reading.)
4. *Connect it back.* Pick another model from this course — Bayesian generalization (Week 4), a causal Bayes net (Week 5), the semantic-network walk (Week 6), MCMC-with-people (Week 7) — and ask: is the agent in it *model-based* or *model-free*? Does it represent the world and plan, or just cache what worked? And a freebie: which one are *you*, right now, deciding what to eat for lunch?

Reply to _each other_, not just to me — a good doubt deserves a counter-reply. I'll jump in where it's useful.

*📖 You can write your reflection on any of these — pick whichever grabs you.* Daw et al. above is the default, but any of these are equally fair game for your discussion post:
- 🤖 *Zhong, Prystawski, Wu, Fascendini, Saeedpour & Austerweil (2026), _Interpretational alignment: How agents learn from physical guidance depends on how they interpret it_* (PDF: https://hml.chibatech.dev/readings/pdfs/Zhongetal2026CogSci.pdf) — *hot off the press, out at CogSci this year.* Human teachers train a Q-learning agent by physically _moving_ it; whether the agent actually learns depends on how it reads that nudge — a suggestion, a correction, or just noise. The exact teach-an-RL-agent problem behind Friday's reward-shaping demo. (Full disclosure: this one's from my own group.)
- 🍎 Ho, Littman, Cushman & Austerweil (2015), _Teaching with rewards and punishments: Reinforcement or communication?_ (PDF: https://hml.chibatech.dev/readings/pdfs/Hoetal2015CogSciProc.pdf) — when people give an agent 👍 / 👎, are they _reinforcing_ it or _communicating_ with it? The predecessor to Zhong et al., and the source of Friday's action-feedback positive-cycle example.
- 🧠 Schultz, Dayan & Montague (1997), _A neural substrate of prediction and reward_ (PDF: https://hml.chibatech.dev/readings/pdfs/Schultz1997.pdf) — the famous recordings where dopamine neurons fire like a *TD prediction error*: to the reward at first, then to the cue that predicts it. The direct neural bridge for prompt #3.
- 📐 Sims (2018), _Efficient coding explains the universal law of generalization in human perception_ (PDF: https://hml.chibatech.dev/readings/pdfs/sims2018.pdf) — derives perceptual generalization from an information bottleneck: decision theory with a hard limit on how much you can encode. Ties straight back to Week 4 generalization.

---

## ⏰ Reminders (post as a follow-up reply, or fold into the root) — Slack-native formatting

A couple of deadline + looking-ahead notes:

*🧩 Generalization assignment is due TONIGHT — Fri Jun 19, 8:00 PM* (7.5%). Submit per the assignment instructions; PDF + GenJAX/Python/R stencils are on the assignments page: https://hml.chibatech.dev/assignments.html . Reminder: you have 3 free late days pooled across the four programming assignments — burning them here is fine, just know they're gone for later. Questions → DM me or the class channel.

*🗓️ A couple more dates on the horizon:*
- *Monte Carlo / sampling assignment* (the GenJAX exercise that landed in Week 7) — due *Fri Jul 10, 8:00 PM*. Stencil + details on the assignments page.
- *Final-project proposal* — due *Sun Jun 28, 8:00 PM* (pass/fail). ~1 page: background, question, method, and at least three references. Full guidelines: https://hml.chibatech.dev/project.html . Good week to lock in a topic.

*🛠️ The RL assignment* (Q-learning on the GardenPath grid — the interactive demo we'll run Friday) *releases next week*, not today. Heads-up so you can pace the proposal and the MC exercise around it.

*🎤 Looking ahead:* paper presentations resume later in the term (Imai in Week 11, Tenzin in Week 12). If that's you and you want the optional 1-on-1 prep meeting, DM me.

---

## Speaker / facilitation notes (not for Slack)

- **Formatting:** the paste-ready Root post + Reminders above are in *Slack-native* syntax (`*bold*`, `_italic_`, bare auto-linking URLs, no `>` blockquote) — copy them straight into Slack. Standard markdown (`**bold**`, `[text](url)`) pastes as literal characters into Slack's composer. These facilitation notes are not pasted, so they stay in plain markdown. (Same convention as the Week 7 thread.)
- **All six reading PDFs are live** at `https://hml.chibatech.dev/readings/pdfs/` (verified present in `docs/readings/pdfs/`: `Dawetal2005.pdf`, `Zhongetal2026CogSci.pdf`, `Hoetal2015CogSciProc.pdf`, `Schultz1997.pdf`, `KordingWolpert2004.pdf`, `sims2018.pdf`). Filenames track `readings_map.yml`'s Week-8 `pdf:` fields. The Zhong PDF was copied from `~/SynologyDrive/final_papers/` into `resources/readings/` and staged to `docs/` by `_build.py`'s reading-PDF stager.
- **The thread is built on the Week 7 → Week 8 hinge** (inference → agency). The root post's opener cashes out the arc the lecture itself runs on (the shared-outline's "Key Design Decision": *from "what should I believe?" to "what should I do?"*). The MDP = "Markov chain + actions + rewards" line previews the beloved SP25 build that opens the MDP block.
- **Required reading is Daw, Niv & Dayan (2005)** (`required` in `readings_map.yml`) — the canonical model-based vs. model-free dual-systems paper. It tees up Block 8's cog-sci thread (dopamine = TD error, dual systems) directly, and the model-based/model-free split is the spine of the whole lecture (Act I value iteration = model-based; Act II Q-learning = model-free; Act III simulation-based RL = "learn a model, then plan").
- **Prompt → lecture mapping** (each prompt seeds a slide so an in-thread bite is a free lead-in):
  - Prompt 1 (why two systems) → the Act I/Act II split (plan a *known* MDP vs. learn an *unknown* one).
  - Prompt 2 (arbitration by uncertainty) → the Daw thread in the modernization tail; good to call on as the bridge into Block 8.
  - Prompt 3 (TD error / dopamine) → the *dopamine = TD error $\delta_t$* slide and the Schultz candidate. The mechanism-vs-fit framing deliberately reuses Week 6 prompt 1's move.
  - Prompt 4 (model-based vs model-free across the course) → the integrative one; bridges Weeks 4–7 and previews the Weeks 11–13 alignment thread (reward hacking → RLHF).
- **Four alternative readings in the thread, opened because `presenter: null`** (same treatment as Weeks 6–7). They sit in two `readings_map.yml` buckets: `optional` (the genuine reflection alternatives — **Zhong et al. 2026** and **Ho et al. 2015**, added this round) and `presentation_candidates` (**Schultz 1997**, **Sims 2018**).
  - **Zhong et al. (2026)** — *added per professor request.* Brand-new CogSci 2026 in-house paper (Austerweil is an author): human teachers train a Q-learning agent by physical "state intervention," and learning hinges on how the agent interprets the nudge. The tightest possible fit to Friday's reward-shaping centerpiece and the widget's "human teaching mode." Featured first in the alternatives list. The root post's "(Full disclosure: this one's from my own group.)" line is optional — cut it if you'd rather not flag authorship.
  - **Ho et al. (2015)** — *pulled back from SP25's Week-8 unit per professor request.* The teaching-as-communication predecessor to Zhong et al. and the source of the action-feedback positive-cycle table. (Still also a Week-9 presentation candidate — that's intentional, not a duplicate to clean up.)
  - **Schultz 1997** primes the dopamine slide (prompt #3); **Sims 2018** links the SDT frame back to Week 4 generalization. If a Week-8 presenter is later confirmed, Schultz 1997 is the natural pick — move it out of the alternatives and set the in-thread role to "presented."
  - **Körding & Wolpert (2004) is deliberately omitted from the thread alternatives** — it's a sensorimotor/SDT paper with no tie to the RL / teaching / dual-systems spine the rest of the thread is built on (the same call made for de Zoete in Week 7). It **stays a `presentation_candidates` entry** in `readings_map.yml` and on the published readings page, so it's not lost — add it back to the thread only if a student wants the motor-control / SDT angle.
- **Reward-shaping / positive-cycle teaser:** prompt 3 stops short of the reward-hacking demo on purpose (the centerpiece GardenPath widget — action-feedback creating a +20/lap loop — is a Friday reveal). If a student raises reward hacking or RLHF in-thread, that's a free lead-in to the widget; don't pre-empt the demo in replies.
- **Deadline facts to verify before posting:**
  - *Generalization due Fri Jun 19, 8:00 PM* — carried from the Week 7 thread (consistent with the PLAN admin slide).
  - *MC / sampling assignment due Fri Jul 10* — from the PLAN's admin-slide deadline list ("MC Jul 10"). The Week 7 thread said the stencil + due date were still "to follow," so **confirm the Jul 10 date and that the stencil is actually posted on the assignments page** before sending; if not yet posted, soften to "due Jul 10 — stencil to follow."
  - *RL assignment releases next week (not Jun 19)* — explicit in the PLAN post-review fixes.
  - *Proposal due Sun Jun 28, 8:00 PM* — carried from the Week 7 thread.
- Normal reflection-eligible week (Weeks 2–12 eligible; Week 1 is not). No need to restate the 5-of-11 rule unless asked.
