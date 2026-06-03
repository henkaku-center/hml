# Week 6 (Jun 5) — Slack discussion thread

**Topic:** Markov chains + random walks on networks
**Required reading:** Abbott, J. T., Austerweil, J. L., & Griffiths, T. L. (2012). *Human memory search as a random walk in a semantic network.* NeurIPS.
**Reflection eligibility:** Week 6 is a reflection-eligible week (counts toward your 5-of-11). ~200 words, posted in-thread **before class Fri Jun 5**.

---

## Root post (paste-ready)

> **📚 Week 6 reading discussion — Markov chains as a model of memory**
>
> This week's required reading is **Abbott, Austerweil & Griffiths (2012), *Human memory search as a random walk in a semantic network*** ([PDF](https://hml.chibatech.dev/readings/pdfs/abbott_nips2012_randomWalk.pdf)). It takes the Markov-chain machinery we cover Friday — states, transitions, stationary distributions — and points it at a cognitive question: *when you free-recall a list of animals, why do the words come out in the order they do?* Their answer: you're taking a random walk over a semantic network, and the data we see (which words, in which order, with what pauses) is just the sequence of states that walk visits.
>
> Post your **~200-word reflection as a reply in this thread before class Friday (Jun 5).** Not a summary — a reaction: something you found compelling, a doubt, or a connection to other work. A few prompts if you're stuck (pick one, or go your own way):
>
> 1. **Mechanism vs. fit.** The random walk reproduces human recall patterns well. But "it fits the data" and "this is what the mind actually does" aren't the same claim. What evidence in the paper pushes you toward the stronger reading — or what would you want to see before you'd believe it?
> 2. **Where does the network come from?** The walk runs on a semantic network whose edges are estimated from *other* behavioral data (e.g. free-association norms). Is that a clean test of the model, or is some of the explanatory work being smuggled in through how the network was built?
> 3. **The Markov assumption itself.** A random walk is memoryless — the next word depends only on the current one, not on what you've already said. Human recall clearly *avoids* repeating itself. Is that a fatal problem for the model, a fixable one, or evidence the brain isn't really memoryless? (Connect to the "given the present, the future is independent of the past" framing from lecture.)
> 4. **Stationary distribution = what?** If you let the walk run forever, it converges to a stationary distribution over concepts. Does that quantity correspond to anything psychologically real — salience, accessibility, frequency — or is it just a mathematical limit? (This is the same object behind PageRank, which we'll see Friday.)
>
> Reply to *each other*, not just to me — a good doubt deserves a counter-reply. I'll jump in where it's useful.
>
> **📖 You can write your reflection on any of these — pick whichever grabs you.** The Abbott paper above is the default, but these three are equally fair game for your discussion post:
> - 🔍 Griffiths, Steyvers & Firl (2007), *Google and the mind: Predicting fluency with PageRank* ([PDF](https://hml.chibatech.dev/readings/pdfs/Griffiths2007.pdf)) — uses PageRank (a random-walk algorithm) to predict human word-fluency; the direct bridge to prompt #4.
> - 🧠 Zemla & Austerweil (2019), *Analyzing knowledge retrieval impairments associated with Alzheimer's disease using network analyses* ([PDF](https://hml.chibatech.dev/readings/pdfs/ZemlaAusterweil2019.pdf)) — applies these network methods to a clinical population.
> - 🕸️ Stella (2018), *Cohort and rhyme priming emerge from the multiplex network structure of the mental lexicon* ([PDF](https://hml.chibatech.dev/readings/pdfs/Stella2018.pdf)) — a modern multiplex-network model of lexical priming.

---

## ⏰ Reminders (post as a follow-up reply, or fold into the root)

> Two quick deadline notes for today:
>
> **🧩 Assignment 1 (Clusters) is due TONIGHT, Fri Jun 5, 8:00pm.** Submit the notebook per the assignment instructions. Reminder on late days: you have **3 free late days pooled across the four programming assignments** — burning them here is fine, just know they're gone for later. Questions on the stencil → drop them in #assignments and I'll get to them before the deadline.
>
> **🎤 Looking ahead:** paper presentations resume later in the term (Imai in Week 11, Tenzin in Week 12). If that's you and you want the optional 1-on-1 prep meeting, DM me.

---

## Speaker / facilitation notes (not for Slack)

- Abbott et al. (2012) is the **default reflection anchor**; the three other papers in `readings_map.yml` (Griffiths 2007 PageRank, Zemla & Austerweil 2019 Alzheimer's networks, Stella 2018 multiplex lexicon) are listed in `readings_map.yml` as `presentation_candidates`, but for SP26 Week 6 there are no presenters, so they've been opened up as **alternative reflection readings** — a student can write their discussion post on any of the four.
- Prompt 4 deliberately seeds **PageRank**, which the Friday lecture reaches via the stationary-distribution slides (deck slides ~28, 40, plus the Griffiths/Steyvers fluency thread). If a student bites on it in-thread, that's a free lead-in for class.
- Jun 5 is the **Clusters due date** — keep the reminder in the thread so it's not buried in #assignments.
- This is a normal reflection-eligible week (Weeks 2–12 are eligible; Week 1 is not). No need to restate the 5-of-11 rule unless someone asks.
