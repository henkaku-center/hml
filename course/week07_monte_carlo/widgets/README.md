# Interactive MCMC viz — `mcmc-gmm.html`

A single self-contained HTML file (vanilla JS + Canvas, **no build step, no
dependencies, works offline from `file://`**) that samples from a multimodal 2-D
Gaussian-mixture target with **Metropolis–Hastings** or **Gibbs**, with a live
proposal-variance control and an acceptance-ratio readout. Built for Week 7
(approximation techniques) to teach **chain mixing**, how **proposal variance**
drives mixing, and how that shows up in the **acceptance ratio**.

## What's on screen

- **Left (trajectory):** the target density as a heatmap, the chain's path (faded
  yellow trail), the current point (yellow dot), and for MH the proposal circle
  (radius ≈ σ) plus the last proposal endpoint (**green = accepted, red = rejected**).
- **Top-right (trace):** the x-coordinate vs. iteration. Flat = stuck in one mode;
  hopping between levels = mixing. Faint horizontal lines mark the modes' x-values.
- **Bottom-right (histogram):** accumulated samples (blue bars) vs. the *true*
  x-marginal (yellow curve). When the sampler has explored all modes the bars match
  the curve; when trapped, only one peak fills in.
- **Hero readout:** **acceptance ratio = accepted / total**, colour-coded
  (green ≈ 0.2–0.5, orange in between, red near 0 or 1), plus `n` and a
  **modes-visited** counter — the quantitative "did it actually explore?" number.

## Controls

`target` (4-blob / 3-blob / 2-blob) · `sampler` (MH / Gibbs) · **proposal σ**
(log slider, greyed for Gibbs) · Run/Pause (or Spacebar) · Step · Reset · speed ·
density/proposal toggles.

## The live demo script (rehearse this order)

All on the default **4 blobs (separated)** target. Hit **Reset** before each.

| # | Setting | What students see | Lesson |
|---|---------|-------------------|--------|
| 0 | Gibbs, Run | axis-aligned L-moves; acceptance **n/a**; visits all 4 modes | Gibbs always accepts; conditional moves |
| 1 | MH, σ ≈ **0.05**, Run | proposal circle tiny; acceptance **≈ 0.94**; **stuck in 1 mode** | high acceptance ≠ good mixing (slow random walk) |
| 2 | MH, σ ≈ **4.0**, Run | huge circle; acceptance **≈ 0.05**; chain barely moves | too-big steps reject everything → also bad |
| 3 | MH, σ ≈ **0.4–0.6**, Run | acceptance **≈ 0.5–0.6**; explores its mode well | the Goldilocks regime *within* a mode |
| 4 | **same σ ≈ 0.4, run long** | healthy acceptance, but **modes visited stays 1/4**; histogram fills only one peak | **good local acceptance ≠ good global mixing** — well-separated modes trap local MH. *Why multimodal is hard, and why MCMCP is subtle.* |

Demo 4 is the punchline. Contrast it with Demo 0 (Gibbs reaches all modes) and the
point lands: the acceptance number can look fine while the chain has explored
nothing.

## Tuning

The trap demo depends on mode separation vs. σ. The constants are at the top of the
`<script>`: `DOMAIN`, `BLOB_SIGMA` (0.45), and `TARGETS` (mean locations). If the
"good" σ from Demo 3 ever manages to cross modes, push the means farther apart or
shrink `BLOB_SIGMA`.

## Embedding in the deck & PDF fallback

The slide embeds this via a RevealJS background iframe with
`background-interactive="true"` (required, or the sliders won't receive clicks). The
project must copy this dir into the build — see the `resources:` entry in the week7
qmd frontmatter. The viz **auto-seeds 60 steps on load**, so even a static screenshot
(decktape/PDF export) shows a meaningful frame. For the PDF a static still
(`../images/mcmc-gmm-fallback.png`, the trapped-modes Demo 4) sits on a following
slide captioned "open `week07.html` to drive it live."

In-canvas labels are English (math/UI terms); the bilingual EN/JA framing lives on
the surrounding slide text.
