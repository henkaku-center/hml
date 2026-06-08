# Week 7 (Jun 12) — Slack discussion thread

**Topic:** Monte Carlo approximation + MCMC (importance sampling, particle filtering, Metropolis–Hastings + Gibbs, MCMC-with-People)
**Required reading:** Sanborn, A. N., & Griffiths, T. L. (2008). *Markov chain Monte Carlo with people.* NIPS.
**Reflection eligibility:** Week 7 is a reflection-eligible week (counts toward your 5-of-11). ~200 words, posted in-thread **before class Fri Jun 12**.
**No presenter this week** (`presenter: null`) — so the alternative papers below are open as reflection readings, same as Week 6.

---

## Root post (paste-ready) — Slack-native formatting

*📚 Week 7 reading discussion — turning a _person_ into an MCMC chain*

Last week we built the Markov-chain machinery — states, transitions, and the *stationary distribution* a chain settles into if you run it long enough — and ended by hinting at where it goes next: if you can _design_ a chain whose stationary distribution is a distribution you actually care about, you can sample from things you could never write down. That's *MCMC*, and Friday we build it (Metropolis–Hastings and Gibbs). This week's reading takes the wild final step.

*Sanborn & Griffiths (2008), _Markov chain Monte Carlo with people_* (PDF: https://hml.chibatech.dev/readings/pdfs/SanbornGriffiths2007.pdf) asks: what if the *accept/reject step of the chain is done by a human?* You show a person two stimuli and let their choice be the Metropolis accept step. Run that loop, and the chain's stationary distribution is _the category in the person's head_ — you've turned a participant into a sampler and read out their mental representation of "dog" or "a happy face." The Markov chain isn't a metaphor here; it's the experiment.

Post your *~200-word reflection as a reply in this thread before class Friday (Jun 12).* Not a summary — a reaction: something you found compelling, a doubt, or a connection to other work. A few prompts if you're stuck (pick one, or go your own way):

1. *Why does this work at all?* The whole method rests on one assumption: that a person's choice between two options behaves like the Metropolis accept rule (choose option B over A with a probability set by the ratio of how well each fits the category). If human choice _isn't_ exactly that rule, what breaks — do you get the wrong stationary distribution, a slower one, or no valid distribution at all?
2. *Has it mixed?* From Week 6: a chain only reaches its stationary distribution after it's _mixed_, and early samples are correlated and biased toward where you started. A human MCMC chain might run for a few hundred trials, tops — fatigue, boredom, drift. How would you even _know_ the human chain has converged, and how much should that worry you about the recovered "category"?
3. *Whose prior, whose posterior?* The pitch is "read the distribution out of someone's head." But the recovered distribution depends on the stimulus space _you_ chose to let them move through. How much of the result is the participant's mind versus the experimenter's design choices — and is there a clean way to tell those apart?
4. *Connect it back.* Pick another model from this course (the random walk on a semantic network from Week 6, Bayesian generalization from Week 4, a causal Bayes net from Week 5) and ask: could you run _it_ as an MCMC-with-people experiment? What would the stimuli be, what would the accept step ask, and what would the stationary distribution mean?

Reply to _each other_, not just to me — a good doubt deserves a counter-reply. I'll jump in where it's useful.

*📖 You can write your reflection on any of these — pick whichever grabs you.* Sanborn & Griffiths above is the default, but these two are equally fair game for your discussion post:
- 🎲 Vul, Goodman, Griffiths & Tenenbaum (2009), _One and done? Optimal decisions from very few samples_ (PDF: https://hml.chibatech.dev/readings/pdfs/VulGoodmanGriffithsTenenbaum-cogsci-2009.pdf) — argues people may look irrational simply because we decide after drawing only a _handful_ of samples, and that under a cost on thinking-time, "few samples" is actually _optimal_. The other side of the same coin: not reading a chain out of a person, but asking how many samples a person bothers to draw.
- 🔮 Griffiths & Tenenbaum (2006), _Optimal predictions in everyday cognition_ (PDF: https://hml.chibatech.dev/readings/pdfs/Griffiths06-preds.pdf) — people's everyday predictions (lifespans, movie grosses, poem lengths) track Bayesian posteriors strikingly well; the empirical backbone for the "people approximate the right distribution" view.

---

## ⏰ Reminders (post as a follow-up reply, or fold into the root) — Slack-native formatting

A couple of deadline + looking-ahead notes:

*🗓️ Two deadlines coming up:*
- *Generalization assignment* — due *Fri Jun 19, 8:00 PM* (7.5%). The PDF + GenJAX/Python/R stencils are on the assignments page: https://hml.chibatech.dev/assignments.html . Reminder: you have 3 free late days pooled across the four programming assignments. Questions → DM me or the class channel.
- *Final-project proposal* — due *Sun Jun 28, 8:00 PM* (pass/fail). ~1 page: background, question, method, and at least three references. Full details + guidelines: https://hml.chibatech.dev/project.html . Worth starting to think about your topic now.

*🧩 The Monte Carlo / GenJAX sampling exercise* lands with this week — building a sampler for the hierarchical model from Week 4 (Gibbs the easy part, Metropolis the hard part). We'll walk the recipe end-to-end in class Friday; the assignment is that recipe turned into code. Stencil + due date to follow.

*🎤 Looking ahead:* paper presentations resume later in the term (Imai in Week 11, Tenzin in Week 12). If that's you and you want the optional 1-on-1 prep meeting, DM me.

---

## Speaker / facilitation notes (not for Slack)

- **Formatting:** the paste-ready Root post + Reminders above are in *Slack-native* syntax (`*bold*`, `_italic_`, bare auto-linking URLs, no `>` blockquote) — copy them straight into Slack. Standard markdown (`**bold**`, `[text](url)`) pastes as literal characters into Slack's composer. These facilitation notes are not pasted, so they stay in plain markdown.
- **Required reading swapped to Sanborn & Griffiths (2008)** to make the discussion thread focus on MCMC/MCMCP, leaning on the Week 6 hand-off (Markov chains → MCMC → MCMCP). `readings_map.yml` Week 7 block updated to match: Sanborn & Griffiths is now `required`; Vul et al. (2009) demoted to `optional` (kept as an alternative reflection reading); Griffiths & Tenenbaum (2006) and de Zoete (2019) remain `presentation_candidates`. The swap is recorded in the `why:` field so it's traceable.
- **The thread is built on the Week 6 → Week 7 arc.** Week 6 covered states/transitions/stationary distribution/mixing and explicitly hinted at MCMC; this thread cashes that hint out. Prompts 1–2 reuse Week 6 vocabulary on purpose (accept rule, mixing, stationary distribution) — students who did the Week 6 reflection should feel the continuity.
- **Prompt 2 ("has it mixed?") deliberately seeds mixing/convergence** — early MCMC samples are correlated and the chain may not have mixed. The Friday interactive viz (Block 6, the trapped-between-modes demo) and Poll 3 land exactly this point, so an in-thread bite is a free lead-in to the centerpiece demo.
- **Prompt 4 (run another course model as MCMC-with-people)** is the integrative one — it connects to Week 6 (semantic-network random walk), Week 4 (Bayesian generalization), Week 5 (causal Bayes nets). Good to call on in class as a bridge across the term.
- Reading on **Vul et al.** primes the Marr "rational process models / are people samplers" opener (Block 1); reading on **Sanborn & Griffiths** (the default) primes Block 8 (MCMC with People) directly. Either is a useful student to call on.
- The third Week-7 presentation candidate in `readings_map.yml` — de Zoete et al. (2019), forensic voice comparison — is **deliberately omitted** from the alternatives in the thread. It's a forensic-acoustics application tangential to this week's cognition-as-sampling theme. Add it back only if a student specifically wants the forensic angle.
- Calendar note: an older Week-3-era handoff doc (`HANDOFF_announcements.md`) lists a stale topic order (Week 7 ≈ "Generalization release"). The authoritative sources — this PLAN, the shared-outline, and `readings_map.yml` — all agree **Week 7 (Jun 12) = Monte Carlo & MCMC.** Ignore the stale handoff calendar.
- Normal reflection-eligible week (Weeks 2–12 eligible; Week 1 is not). No need to restate the 5-of-11 rule unless asked.
