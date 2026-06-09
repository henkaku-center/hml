#!/usr/bin/env python3
"""Generate Week 7 (Monte Carlo / Approximation) figures.

All figures render on a TRANSPARENT background with light strokes/text so they
sit on the dark SDS RevealJS theme (#111111). Theme colours mirror
sds-reveal/sds.scss. Run:  python3 make_figures.py
Outputs land in images/.

Figures:
  mc-die-convergence.png   running MC estimate of E[die] -> 3.5 (LLN)
  mc-pi-darts.png          pi-via-darts build-up n=10/100/1000/10^4
  mh-anim-1..6.png         Metropolis-Hastings animation (dark-theme recreation
                           of COSMOS s21-26): point on multimodal p(x) -> propose
                           -> accept A=1 -> propose -> accept A=0.5 -> reject
  gibbs-trace.png          Gibbs coordinate-wise resampling on 2-D contours
  kemp-hierarchy-plate.png two-level Beta-Binomial plate (phi,kappa)->theta_i->k_i
  gibbs-metropolis-recipe.png  Kemp sampler loop: Gibbs theta (easy) + MH (phi,kappa)
  is-weight-variance.png   importance-sampling weight variance (good vs bad q)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

# ---- theme ---------------------------------------------------------------
BG       = "#111111"
WHITE    = "#FFFFFF"
DIM      = "#999999"
ACCENT   = "#64B5F6"   # blue
YELLOW   = "#FFEB3B"
RED      = "#EF5350"
GREEN    = "#66BB6A"
ORANGE   = "#FFA726"
PURPLE   = "#BA68C8"
TEAL     = "#4DD0E1"

plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor":   "none",
    "savefig.facecolor": "none",
    "text.color":       WHITE,
    "axes.edgecolor":   DIM,
    "axes.labelcolor":  WHITE,
    "xtick.color":      DIM,
    "ytick.color":      DIM,
    "font.size":        15,
    "font.family":      "DejaVu Sans",
})

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
os.makedirs(IMG, exist_ok=True)
RNG = np.random.default_rng(7)


def save(fig, name):
    p = os.path.join(IMG, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", transparent=True, pad_inches=0.15)
    plt.close(fig)
    print("wrote", os.path.relpath(p, HERE))


# ==========================================================================
# 0. Hospital-problem SIMULATION: simulate one year (365 days) for each
#    hospital. Each day, draw the births (Binomial), compute the boy-fraction,
#    and histogram the 365 daily fractions. The >60% days are shaded and
#    counted — the SMALL hospital lands there on many more days.
# ==========================================================================
def fig_hospital_tails():
    n_large, n_small = 90, 12       # babies/day at each hospital
    p = 0.5                         # true boy probability
    thr = 0.60                      # ">60% boys" threshold
    DAYS = 365                      # one year
    rng = np.random.default_rng(2026)
    # simulate the daily boy-fraction across the year
    frac_large = rng.binomial(n_large, p, DAYS) / n_large
    frac_small = rng.binomial(n_small, p, DAYS) / n_small
    n_days_large = int((frac_large > thr).sum())
    n_days_small = int((frac_small > thr).sum())

    bins = np.linspace(0.0, 1.0, 31)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6), sharey=True)
    panels = [(axes[0], frac_large, ACCENT, f"large hospital (~{n_large}/day)", n_days_large),
              (axes[1], frac_small, ORANGE, f"small hospital (~{n_small}/day)", n_days_small)]
    for ax, frac, color, label, ndays in panels:
        below = frac <= thr
        ax.hist(frac[below], bins=bins, color=color, alpha=0.55, edgecolor="none")
        # the >60% days: solid, highlighted
        ax.hist(frac[~below], bins=bins, color=color, alpha=1.0, edgecolor="white", lw=0.4)
        ax.axvline(thr, color=WHITE, ls="--", lw=1.4, alpha=0.8, zorder=4)
        ax.set_title(label, color=color, fontsize=13, fontweight="bold", pad=6)
        ax.text(0.62, 0.96, f">60% on\n{ndays} of 365 days",
                transform=ax.transAxes, color=color, fontsize=13, fontweight="bold",
                ha="left", va="top")
        ax.text(thr - 0.01, 0.0, "60%", color=DIM, fontsize=10.5, ha="right", va="bottom",
                transform=ax.get_xaxis_transform())
        ax.set_xlim(0.15, 0.95)
        ax.set_xlabel("boys / births, per day")
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.set_yticks([])
    axes[0].set_ylabel("number of days")
    fig.suptitle("Simulate one year: same 50% rate, but the small hospital's daily "
                 "fraction swings wider — far more >60% days.",
                 color=WHITE, fontsize=12.5, y=1.02)
    fig.tight_layout()
    save(fig, "hospital-tails.png")


# ==========================================================================
# 1. Monte Carlo: die-roll convergence to 3.5 (LLN)
# ==========================================================================
def fig_die_convergence():
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    n = 2000
    rolls = RNG.integers(1, 7, size=n)
    running = np.cumsum(rolls) / np.arange(1, n + 1)
    ax.axhline(3.5, color=YELLOW, lw=2, ls="--", zorder=1)
    ax.text(n * 0.78, 3.62, r"true mean $= 3.5$", color=YELLOW, fontsize=14)
    ax.plot(np.arange(1, n + 1), running, color=ACCENT, lw=1.8, zorder=2)
    ax.set_xscale("log")
    ax.set_xlim(1, n)
    ax.set_ylim(1, 6)
    ax.set_xlabel("number of samples  $n$  (log scale)")
    ax.set_ylabel(r"running estimate  $\hat\mu_n$")
    ax.set_title(r"$\hat\mu_n = \frac{1}{n}\sum_{i=1}^{n} x_i \;\to\; \mathbb{E}[x]$",
                 color=WHITE, fontsize=16, pad=10)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "mc-die-convergence.png")


# ==========================================================================
# 2. pi-via-darts build-up (n = 10, 100, 1000, 10000)
# ==========================================================================
def fig_pi_darts():
    Ns = [10, 100, 1000, 10000]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 4.2))
    # one shared stream so each panel is a superset of the previous
    maxN = Ns[-1]
    xs = RNG.random(maxN)
    ys = RNG.random(maxN)
    inside_all = xs**2 + ys**2 <= 1.0
    theta = np.linspace(0, np.pi / 2, 200)
    for ax, N in zip(axes, Ns):
        x, y, ins = xs[:N], ys[:N], inside_all[:N]
        # point sizes shrink as N grows so dense panels stay legible
        ms = {10: 60, 100: 22, 1000: 6, 10000: 1.6}[N]
        ax.scatter(x[ins], y[ins], s=ms, c=GREEN, alpha=0.8, edgecolors="none")
        ax.scatter(x[~ins], y[~ins], s=ms, c=RED, alpha=0.7, edgecolors="none")
        ax.plot(np.cos(theta), np.sin(theta), color=YELLOW, lw=2.0, zorder=3)
        ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=DIM, lw=1.2))
        pi_hat = 4 * ins.mean()
        ax.set_title(f"$n={N:,}$\n" + r"$\hat\pi=" + f"{pi_hat:.3f}$",
                     color=WHITE, fontsize=15)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle(r"$x,y\sim\mathrm{Uniform}[0,1]\quad$"
                 r"$\hat\pi = 4\cdot\dfrac{\#\,\mathrm{inside}\;(x^2+y^2\leq 1)}{\#\,\mathrm{total}}$",
                 color=YELLOW, fontsize=16, y=1.05)
    save(fig, "mc-pi-darts.png")


# ==========================================================================
# 2a. rejection-sampling SCHEMATIC: easy box containing a blobby target P,
#     green points kept (under P), red points rejected (in the box, not P).
# ==========================================================================
def fig_rejection_schematic():
    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    # the easy "box" we can sample from
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=WHITE, lw=2.4, zorder=2))
    ax.text(0.5, 1.06, "easy box (sample here)", color=DIM, fontsize=13, ha="center")
    # Target region P = the UNION of two overlapping ellipses. Render the
    # union with UNIFORM opacity (not two stacked translucent ellipses, whose
    # overlap would double up and wrongly highlight the intersection). Build a
    # boolean union mask on a fine grid and imshow it once as a single flat
    # semi-transparent RGBA layer, plus a crisp union outline.
    blobs = [(0.42, 0.46, 0.42, 0.34, 18), (0.58, 0.54, 0.30, 0.5, -22)]

    def in_P(px, py):
        for (cx, cy, w, h, ang) in blobs:
            t = np.deg2rad(ang)
            dx, dy = px - cx, py - cy
            xr = dx * np.cos(t) + dy * np.sin(t)
            yr = -dx * np.sin(t) + dy * np.cos(t)
            if (xr / (w / 2))**2 + (yr / (h / 2))**2 <= 1:
                return True
        return False

    GR = 600
    gx = np.linspace(0, 1, GR)
    GX, GY = np.meshgrid(gx, gx)
    mask = np.zeros((GR, GR), dtype=bool)
    for (cx, cy, w, h, ang) in blobs:
        t = np.deg2rad(ang)
        dx, dy = GX - cx, GY - cy
        xr = dx * np.cos(t) + dy * np.sin(t)
        yr = -dx * np.sin(t) + dy * np.cos(t)
        mask |= (xr / (w / 2))**2 + (yr / (h / 2))**2 <= 1
    # flat RGBA: accent blue at uniform alpha INSIDE the union, transparent out
    from matplotlib.colors import to_rgb
    rgba = np.zeros((GR, GR, 4))
    rgba[..., :3] = to_rgb(ACCENT)
    rgba[..., 3] = np.where(mask, 0.28, 0.0)
    ax.imshow(rgba, extent=[0, 1, 0, 1], origin="lower", zorder=1,
              interpolation="bilinear")
    # crisp union outline (contour of the mask)
    ax.contour(GX, GY, mask.astype(float), levels=[0.5], colors=[ACCENT],
               linewidths=2.0, zorder=1)
    ax.text(0.5, 0.5, r"$P$", color="white", fontsize=22, ha="center", va="center",
            fontweight="bold", zorder=4)

    rng = np.random.default_rng(11)
    pts = rng.random((90, 2))
    keep = np.array([in_P(*p) for p in pts])
    ax.scatter(pts[keep, 0], pts[keep, 1], s=42, c=GREEN, edgecolors="white",
               lw=0.5, zorder=3, label="keep (under $P$)")
    ax.scatter(pts[~keep, 0], pts[~keep, 1], s=42, c=RED, edgecolors="white",
               lw=0.5, alpha=0.85, zorder=3, label="reject")
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.15)
    ax.set_aspect("equal"); ax.axis("off")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.13), ncol=2,
              frameon=False, fontsize=12.5, labelcolor=WHITE)
    save(fig, "rejection-schematic.png")


# ==========================================================================
# 2b. pi-via-darts SCHEMATIC: labeled unit square + quarter circle
# ==========================================================================
def fig_pi_schematic():
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    # unit square
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=WHITE, lw=2.2, zorder=2))
    # quarter circle arc + light fill
    theta = np.linspace(0, np.pi / 2, 240)
    cx, cy = np.cos(theta), np.sin(theta)
    ax.fill(np.concatenate([[0], cx, [0]]), np.concatenate([[0], cy, [0]]),
            color=YELLOW, alpha=0.07, zorder=1)
    ax.plot(cx, cy, color=YELLOW, lw=2.6, zorder=3)
    # a few example darts: green inside, red outside
    exx = np.array([0.30, 0.55, 0.20, 0.80, 0.92, 0.66, 0.45, 0.85])
    eyy = np.array([0.40, 0.30, 0.78, 0.25, 0.80, 0.70, 0.92, 0.62])
    ins = exx**2 + eyy**2 <= 1
    ax.scatter(exx[ins], eyy[ins], s=80, c=GREEN, edgecolors="white", lw=0.8, zorder=4)
    ax.scatter(exx[~ins], eyy[~ins], s=80, c=RED, edgecolors="white", lw=0.8, zorder=4)
    # arc label x^2 + y^2 = 1 — placed OUTSIDE the arc (upper-right corner, on
    # the dark background) with a dark bbox so the yellow text stays high-
    # contrast and readable (it was murky when sitting on the filled interior).
    ax.annotate(r"$x^2+y^2=1$",
                xy=(np.cos(np.deg2rad(33)) + 0.012, np.sin(np.deg2rad(33)) + 0.012),
                xytext=(0.995, 0.74), color=YELLOW, fontsize=17, fontweight="bold",
                ha="right", va="center",
                bbox=dict(boxstyle="round,pad=0.28", fc="#0d0d0d", ec=YELLOW, lw=1.1, alpha=0.97),
                arrowprops=dict(arrowstyle="-", color=YELLOW, lw=1.4))
    # an example point with x,y guide lines
    px, py = 0.55, 0.30
    ax.plot([px, px], [0, py], color=ACCENT, lw=1.3, ls=":", zorder=3)
    ax.plot([0, px], [py, py], color=ACCENT, lw=1.3, ls=":", zorder=3)
    ax.text(px, -0.06, r"$x$", color=ACCENT, fontsize=15, ha="center", va="top")
    ax.text(-0.06, py, r"$y$", color=ACCENT, fontsize=15, ha="right", va="center")
    # axis ticks 0..1
    ax.set_xlim(-0.16, 1.16); ax.set_ylim(-0.16, 1.12)
    ax.set_aspect("equal"); ax.axis("off")
    # 0 and 1 corner labels
    for v in (0, 1):
        ax.text(v, -0.10, f"{v}", color=DIM, fontsize=12, ha="center", va="top")
        ax.text(-0.10, v, f"{v}", color=DIM, fontsize=12, ha="right", va="center")
    ax.text(0.5, 1.13, "unit square", color=DIM, fontsize=12, ha="center")
    save(fig, "mc-pi-schematic.png")


# ==========================================================================
# 3. Metropolis-Hastings animation (dark recreation of COSMOS s21-26)
# ==========================================================================
def _multimodal(x):
    """A 1-D multimodal density on [0, 10] (unnormalised is fine for display)."""
    g = lambda mu, s, a: a * np.exp(-0.5 * ((x - mu) / s) ** 2)
    return (g(2.0, 0.7, 0.55) + g(3.3, 0.45, 1.0) + g(5.6, 1.1, 0.78)
            + g(8.4, 0.32, 1.15) + g(9.2, 0.5, 0.35))


def _mh_base(ax):
    xx = np.linspace(0, 10, 600)
    ax.plot(xx, _multimodal(xx), color=WHITE, lw=2.2, zorder=2)
    ax.text(9.2, _multimodal(np.array([8.4]))[0] + 0.05, r"$p(x)$",
            color=DIM, fontsize=16)
    ax.axhline(0, color=DIM, lw=1.0)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.06, 1.45)
    ax.axis("off")


def _proposal_bump(ax, center, scale=0.6, amp=0.18, color=TEAL):
    xx = np.linspace(center - 3 * scale, center + 3 * scale, 100)
    yy = amp * np.exp(-0.5 * ((xx - center) / scale) ** 2)
    ax.plot(xx, yy, color=color, lw=1.6, alpha=0.9, zorder=3)


def fig_mh_animation():
    """Six panels: cur point -> propose -> accept(A=1) -> propose -> accept(A=.5,reject)."""
    panels = [
        ("init",      2.0, None, None),     # 1: just the current point
        ("propose",   2.0, 3.3,  None),     # 2: proposal bump + candidate
        ("accept1",   2.0, 3.3,  1.0),      # 3: uphill -> A=1 accept
        ("propose2",  3.3, 2.0,  None),     # 4: propose downhill
        ("acceptp5",  3.3, 2.0,  0.5),      # 5: A=0.5 (sometimes accept)
        ("reject",    3.3, 5.6,  0.0),      # 6: far low-density -> reject
    ]
    for i, (kind, cur, prop, A) in enumerate(panels, 1):
        fig, ax = plt.subplots(figsize=(8.6, 3.6))
        _mh_base(ax)
        pcur = _multimodal(np.array([cur]))[0]
        # current point
        ax.plot([cur], [0], "o", ms=13, color=YELLOW, zorder=6)
        ax.plot([cur, cur], [0, pcur], color=YELLOW, lw=1.4, ls=":", zorder=4)
        if prop is not None:
            _proposal_bump(ax, cur)
            pprop = _multimodal(np.array([prop]))[0]
            # candidate marker colour: green=accept, orange=A=0.5, red=reject, dim=pending
            if A is None:
                cand_col = DIM
            elif A >= 1.0:
                cand_col = GREEN
            elif A == 0.0:
                cand_col = RED
            else:
                cand_col = ORANGE
            ax.plot([prop], [0], "o", ms=12, mfc="none", mec=cand_col, mew=2.4, zorder=6)
            ax.plot([prop, prop], [0, pprop], color=cand_col, lw=1.2, ls=":", zorder=4)
            # arrow current -> candidate
            ax.annotate("", xy=(prop, 0), xytext=(cur, 0),
                        arrowprops=dict(arrowstyle="-|>", color=cand_col,
                                        lw=2.0, shrinkA=10, shrinkB=10), zorder=5)
            if A is not None:
                if A >= 1.0:
                    txt, tcol = r"$A=\min(1,\,p(x')/p(x))=1$  accept", GREEN
                elif A == 0.0:
                    txt, tcol = r"low $p(x')$  $\Rightarrow$  likely reject", RED
                else:
                    txt, tcol = rf"$A={A:.1f}$  accept w.p. $\frac{{1}}{{2}}$", ORANGE
                ax.text(5.0, 1.28, txt, color=tcol, fontsize=15, ha="center",
                        fontweight="bold")
        else:
            ax.text(5.0, 1.28, r"current state  $x^{(t)}$", color=DIM,
                    fontsize=15, ha="center")
        save(fig, f"mh-anim-{i}.png")


# ==========================================================================
# 4. Gibbs sampling on 2-D contours (axis-aligned moves)
# ==========================================================================
def fig_gibbs_trace():
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    # correlated 2-D Gaussian contours
    xs = np.linspace(-3.4, 3.4, 200)
    X, Y = np.meshgrid(xs, xs)
    rho = 0.75
    Z = np.exp(-(X**2 - 2 * rho * X * Y + Y**2) / (2 * (1 - rho**2)))
    ax.contour(X, Y, Z, levels=6, colors=[ACCENT], linewidths=1.1, alpha=0.7)
    # Gibbs walk: alternate resampling x|y then y|x -> L-shaped steps
    pts = [(-2.6, 2.6)]
    cur = np.array([-2.6, 2.6])
    for t in range(7):
        # x | y  (conditional mean rho*y, var 1-rho^2)
        cur = np.array([RNG.normal(rho * cur[1], np.sqrt(1 - rho**2)), cur[1]])
        pts.append(tuple(cur))
        # y | x
        cur = np.array([cur[0], RNG.normal(rho * cur[0], np.sqrt(1 - rho**2))])
        pts.append(tuple(cur))
    pts = np.array(pts)
    for k in range(len(pts) - 1):
        ax.plot(pts[k:k+2, 0], pts[k:k+2, 1], color=YELLOW, lw=1.6,
                alpha=0.5 + 0.5 * k / len(pts), zorder=3)
    ax.plot(pts[:, 0], pts[:, 1], "o", ms=5, color=YELLOW, zorder=4)
    ax.plot([pts[0, 0]], [pts[0, 1]], "o", ms=11, color=GREEN, zorder=5)
    ax.text(pts[0, 0], pts[0, 1] + 0.35, "start", color=GREEN, fontsize=13, ha="center")
    ax.set_title(r"Gibbs: resample $x_i^{(t+1)}\sim P(x_i\mid x_{-i})$"
                 "\n(one axis at a time — L-shaped moves)",
                 color=WHITE, fontsize=14)
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(-3.4, 3.4)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color(DIM)
    save(fig, "gibbs-trace.png")


# ==========================================================================
# 5. Kemp hierarchy plate diagram
# ==========================================================================
def fig_kemp_plate():
    fig, ax = plt.subplots(figsize=(8.4, 5.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8.6); ax.axis("off")

    def node(cx, cy, label, color, r=0.62, obs=False, sub=None):
        fc = "#2a2a2a" if not obs else color
        ax.add_patch(Circle((cx, cy), r, fc=fc, ec=color, lw=2.6, zorder=3))
        ax.text(cx, cy, label, ha="center", va="center", color=WHITE,
                fontsize=16, fontweight="bold", zorder=4)
        if sub:
            ax.text(cx, cy - r - 0.34, sub, ha="center", va="top", color=DIM,
                    fontsize=11, zorder=4)

    def arrow(p0, p1, color=WHITE):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=20,
                                     lw=2.2, color=color, zorder=2,
                                     shrinkA=14, shrinkB=14))

    ax.text(6.0, 8.3, "Kemp et al. (2007) hierarchy — learned hyperparameters",
            color=WHITE, fontsize=15, ha="center", fontweight="bold")
    # hyperparameters (top) — inline labels to the side, not below (keeps the band clear)
    node(2.8, 6.7, r"$\varphi$", YELLOW)
    node(4.9, 6.7, r"$\kappa$", YELLOW)
    ax.text(2.8, 7.45, "mean", color=DIM, fontsize=11, ha="center")
    ax.text(4.9, 7.45, "concentration", color=DIM, fontsize=11, ha="center")
    ax.text(7.2, 6.7, r"$\Rightarrow\;(a,b)=(\varphi\kappa,\,(1-\varphi)\kappa)$",
            color=DIM, fontsize=12.5, va="center")
    # generative-model line, clear above the plate
    ax.text(6.0, 5.5, r"$\theta_i\sim\mathrm{Beta}(a,b)\qquad k_i\sim\mathrm{Binomial}(n_i,\theta_i)$",
            color=WHITE, fontsize=13.5, ha="center")
    # plate rectangle for students
    ax.add_patch(FancyBboxPatch((1.4, 0.5), 9.2, 4.3,
                                boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="none", ec=DIM, lw=1.6, ls="--", zorder=1))
    ax.text(10.4, 4.5, r"students $i=1\ldots S$", color=DIM, fontsize=12,
            ha="right", va="top", style="italic")
    # theta_i and k_i for three example students
    for j, cx in enumerate((3.0, 5.8, 8.6)):
        node(cx, 3.3, r"$\theta_i$", ACCENT)
        node(cx, 1.5, r"$k_i$", GREEN, obs=True)
        arrow((cx, 3.3 - 0.62), (cx, 1.5 + 0.62), color=ACCENT)
        # hyperparams -> theta_i
        arrow((3.9, 6.6 - 0.55), (cx, 3.3 + 0.62), color=YELLOW)
    ax.text(8.6, 0.78, r"$n_i$ tries each", color=DIM, fontsize=10.5, ha="center")
    save(fig, "kemp-hierarchy-plate.png")


# ==========================================================================
# 6. Gibbs+Metropolis recipe for the Kemp sampler
# ==========================================================================
def fig_recipe():
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")

    ax.text(6.0, 5.65, "one sweep of the block sampler", color=WHITE, fontsize=14,
            ha="center", fontweight="bold")
    # Gibbs box (green / easy)
    ax.add_patch(FancyBboxPatch((0.3, 2.5), 4.9, 2.6,
                                boxstyle="round,pad=0.05,rounding_size=0.25",
                                fc="#14241a", ec=GREEN, lw=2.6, zorder=2))
    ax.text(2.75, 4.78, "Gibbs step", color=GREEN, fontsize=15, ha="center", fontweight="bold")
    ax.text(2.75, 4.3, "(conjugate — easy)", color=GREEN, fontsize=11, ha="center")
    ax.text(2.75, 3.62, r"$\theta_i \mid a,b,k_i,n_i$", color=WHITE, fontsize=14, ha="center")
    ax.text(2.75, 3.05, r"$\sim \mathrm{Beta}(a+k_i,\, b+n_i-k_i)$", color=WHITE,
            fontsize=13, ha="center")
    ax.text(2.75, 2.66, "direct draw — Week 3 conjugacy", color=DIM, fontsize=10, ha="center")

    # Metropolis box (red / needs MH)
    ax.add_patch(FancyBboxPatch((6.8, 2.5), 4.9, 2.6,
                                boxstyle="round,pad=0.05,rounding_size=0.25",
                                fc="#241414", ec=RED, lw=2.6, zorder=2))
    ax.text(9.25, 4.78, "Metropolis step", color=RED, fontsize=15, ha="center", fontweight="bold")
    ax.text(9.25, 4.32, r"on $(\varphi,\,\ell{=}\log\kappa)$, flat priors", color=RED, fontsize=10.5, ha="center")
    ax.text(9.25, 3.74, r"propose $(\varphi,\,\log\kappa)$; accept by", color=WHITE, fontsize=11.5, ha="center")
    ax.text(9.25, 3.18, r"ratio of $\prod_i \mathrm{BetaBin}(k_i\mid n_i,a,b)$", color=WHITE, fontsize=11.5, ha="center")
    ax.text(9.25, 2.66, r"($\theta_i$ integrated out; full ratio next)", color=DIM, fontsize=10, ha="center")

    # loop arrows between boxes
    ax.add_patch(FancyArrowPatch((5.2, 4.0), (6.8, 4.0), arrowstyle="-|>",
                                 mutation_scale=20, lw=2.2, color=WHITE, zorder=3))
    ax.add_patch(FancyArrowPatch((6.8, 3.1), (5.2, 3.1), arrowstyle="-|>",
                                 mutation_scale=20, lw=2.2, color=WHITE, zorder=3))
    ax.text(6.0, 2.15, "repeat", color=DIM, fontsize=12, ha="center", style="italic")
    save(fig, "gibbs-metropolis-recipe.png")


# ==========================================================================
# 7. Importance-sampling weight variance: good q vs bad q
# ==========================================================================
def fig_is_weight_variance():
    # Taller aspect (≈1.18) so the figure occupies more vertical space on the
    # slide — at full slide width it renders ~25% taller than the old 1.72 ratio.
    fig, axes = plt.subplots(2, 2, figsize=(10.0, 8.5),
                             gridspec_kw=dict(height_ratios=[2, 1]))
    xx = np.linspace(-4, 8, 500)
    p = np.exp(-0.5 * ((xx - 4.0) / 0.7) ** 2)          # target/posterior
    p /= np.trapz(p, xx)
    cases = [("good $q$ — broad overlap", 4.2, 1.6, GREEN),
             ("bad $q$ — poor overlap", 0.5, 1.4, RED)]
    for col, (title, mu, s, col_c) in enumerate(cases):
        q = np.exp(-0.5 * ((xx - mu) / s) ** 2); q /= np.trapz(q, xx)
        axtop = axes[0, col]
        axtop.plot(xx, p, color=WHITE, lw=2.2, label=r"$p(x)$ target")
        axtop.fill_between(xx, q, color=col_c, alpha=0.25)
        axtop.plot(xx, q, color=col_c, lw=2.0, label=r"$q(x)$ proposal")
        axtop.set_title(title, color=col_c, fontsize=15)
        axtop.legend(fontsize=11, frameon=False, labelcolor=WHITE)
        axtop.set_xlim(-4, 8); axtop.set_yticks([])
        for sp in ("top", "right", "left"):
            axtop.spines[sp].set_visible(False)
        # draw samples from q, weight by p/q
        samp = RNG.normal(mu, s, 400)
        pv = np.exp(-0.5 * ((samp - 4.0) / 0.7) ** 2)
        qv = np.exp(-0.5 * ((samp - mu) / s) ** 2)
        w = pv / np.clip(qv, 1e-9, None)
        w /= w.sum()
        axb = axes[1, col]
        axb.hist(w, bins=30, color=col_c, alpha=0.8)
        ess = 1.0 / np.sum(w**2)
        axb.set_title(f"weights  (ESS $\\approx$ {ess:.0f} / 400)", color=DIM, fontsize=12)
        axb.set_yticks([])
        for sp in ("top", "right", "left"):
            axb.spines[sp].set_visible(False)
    fig.suptitle("Variance of the importance weights = quality of the sampler",
                 color=YELLOW, fontsize=16, y=1.02)
    fig.tight_layout()
    save(fig, "is-weight-variance.png")


# ==========================================================================
# 8. Particle-filter schematic: weight -> resample -> propagate
# ==========================================================================
def fig_particle_filter():
    fig, ax = plt.subplots(figsize=(10.5, 4.6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 7); ax.axis("off")
    cols_x = [1.6, 5.2, 8.8, 12.4]
    stage_titles = ["prior\nparticles", "weight by\n" + r"$P(d_1\mid h)$",
                    "resample", "propagate, weight\n" + r"by $P(d_2\mid h)$"]
    rng = np.random.default_rng(3)
    ys = np.linspace(1.2, 5.6, 6)
    # column 1: equal weights
    w1 = np.ones(6) / 6
    # column 2: skewed weights (some particles fit d1 better)
    w2 = np.array([0.05, 0.30, 0.40, 0.10, 0.10, 0.05])
    # column 3: resampled (duplicates of high-weight, back to uniform)
    res_src = [1, 2, 2, 1, 2, 3]   # which particle each resampled copy came from
    # column 4: propagated (jittered) + reweighted
    w4 = np.array([0.18, 0.22, 0.10, 0.25, 0.10, 0.15])

    def blob(cx, cy, w, color):
        r = 0.12 + 1.3 * w
        ax.add_patch(Circle((cx, cy), r, fc=color, ec="white", lw=1.2, alpha=0.92, zorder=3))

    for i, y in enumerate(ys):
        blob(cols_x[0], y, w1[i], ACCENT)
        blob(cols_x[1], y, w2[i], ACCENT)
    for i, y in enumerate(ys):
        blob(cols_x[2], y, 1/6, GREEN)
        jy = y + rng.normal(0, 0.18)
        blob(cols_x[3], jy, w4[i], ORANGE)
    # arrows between stages
    for k in range(3):
        ax.add_patch(FancyArrowPatch((cols_x[k] + 1.5, 3.4), (cols_x[k+1] - 1.5, 3.4),
                                     arrowstyle="-|>", mutation_scale=22, lw=2.2,
                                     color=WHITE, zorder=1))
    for cx, t in zip(cols_x, stage_titles):
        ax.text(cx, 6.5, t, ha="center", va="center", color=WHITE, fontsize=13)
    ax.text(7.0, 0.2, "particle size = weight; resampling kills light particles, copies heavy ones",
            ha="center", color=DIM, fontsize=12, style="italic")
    save(fig, "particle-filter.png")


# ==========================================================================
# 9b. Particle-filter WORKED EXAMPLE: tracking a 1-D position over time.
#     5 particles, a noisy observation each step. Three figures: (1) weight by
#     the observation likelihood, (2) resample (kill light, copy heavy),
#     (3) propagate (move + add noise) for the next step.
# ==========================================================================
def _pf_particles(ax, xs, weights=None, color=ACCENT, y=0.0, label_w=False,
                  obs=None, max_s=900, base_s=180):
    """Draw particles as dots on a number line; size ∝ weight."""
    ax.axhline(y, color=DIM, lw=1.2, zorder=1)
    if obs is not None:
        ax.axvline(obs, color=YELLOW, lw=2.2, ls="--", zorder=2)
        # label sits clearly above the line on ONE line, the z inline at the same
        # size as the word (the old stacked "observation\n$z$" put a tiny z right
        # on the dashed line, which was unreadable).
        ax.text(obs, y + 0.78, "observation $z$", color=YELLOW, fontsize=13,
                ha="center", va="bottom", fontweight="bold")
    if weights is None:
        sizes = np.full(len(xs), base_s)
    else:
        w = np.array(weights); w = w / w.max()
        sizes = base_s * 0.5 + max_s * w
    ax.scatter(xs, np.full(len(xs), y), s=sizes, c=color, edgecolors="white",
               lw=1.2, zorder=4)
    if label_w and weights is not None:
        wn = np.array(weights) / np.sum(weights)
        order = np.argsort(xs)
        prev_x, prev_low = None, False
        for idx in order:
            x, wi = xs[idx], wn[idx]
            # If this label would collide with the previous one (< 0.7 apart),
            # drop it to a lower row so the two weights stay readable.
            low = prev_x is not None and (x - prev_x) < 0.7 and not prev_low
            dy = -1.02 if low else -0.6
            ax.text(x, y + dy, f"{wi:.2f}", color=color, fontsize=11,
                    ha="center", va="top", fontweight="bold")
            prev_x, prev_low = x, low
    ax.set_xlim(0, 10); ax.set_ylim(-1.2, 1.4)
    ax.set_yticks([]); ax.set_xlabel("position", color=DIM, fontsize=12)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)


def fig_pf_worked():
    # 5 particles after propagating to time t; the object is really near 6.
    xs0 = np.array([2.6, 4.4, 5.8, 6.3, 8.1])
    obs = 6.0
    # observation likelihood: Gaussian around obs (sigma=1.2)
    sig = 1.2
    w = np.exp(-0.5 * ((xs0 - obs) / sig) ** 2)

    # ---- Step 1: weight by the observation ----
    fig, ax = plt.subplots(figsize=(9.0, 2.7))
    _pf_particles(ax, xs0, weights=w, color=ACCENT, obs=obs, label_w=True)
    ax.set_title("Step 1 — weight each particle by how well it explains the "
                 "observation  $w_i \\propto P(z\\mid x_i)$",
                 color=WHITE, fontsize=13, pad=10)
    save(fig, "pf-step1-weight.png")

    # ---- Step 2: resample (draw 5 with replacement ∝ weight) ----
    wn = w / w.sum()
    # deterministic-ish resample for a clean teaching picture: copy the heavy
    # middle ones, drop the far light ones.
    resampled = np.array([4.4, 5.8, 6.3, 6.3, 5.8])  # 5.8 & 6.3 copied, 2.6/8.1 dropped
    fig, ax = plt.subplots(figsize=(9.0, 2.7))
    # show old (faint) + resampled (solid)
    _pf_particles(ax, xs0, weights=None, color="#3a3a3a", y=0.0, base_s=120)
    ax.scatter(resampled + np.array([0, 0, -0.07, 0.07, 0]), np.full(5, 0.0),
               s=320, c=GREEN, edgecolors="white", lw=1.2, zorder=5)
    ax.axvline(obs, color=YELLOW, lw=2.2, ls="--", zorder=2)
    ax.set_xlim(0, 10); ax.set_ylim(-1.2, 1.4); ax.set_yticks([])
    ax.set_xlabel("position", color=DIM, fontsize=12)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Step 2 — resample: draw 5 new particles ∝ weight "
                 "(heavy ones copied, light ones dropped)",
                 color=WHITE, fontsize=13, pad=10)
    ax.text(2.6, -0.7, "dropped", color=RED, fontsize=11, ha="center", fontweight="bold")
    ax.text(8.1, -0.7, "dropped", color=RED, fontsize=11, ha="center", fontweight="bold")
    save(fig, "pf-step2-resample.png")

    # ---- Step 3: propagate (move + noise) ----
    rng = np.random.default_rng(5)
    moved = resampled + 1.0 + rng.normal(0, 0.5, 5)   # object drifts +1, add noise
    fig, ax = plt.subplots(figsize=(9.0, 2.7))
    # arrows from resampled to moved
    for x0, x1 in zip(resampled, moved):
        ax.annotate("", xy=(x1, 0.0), xytext=(x0, 0.0),
                    arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6, alpha=0.7),
                    zorder=3)
    _pf_particles(ax, moved, weights=None, color=ACCENT, base_s=300)
    ax.set_title("Step 3 — propagate: move each particle by the motion model "
                 "(+ noise), ready for the next observation",
                 color=WHITE, fontsize=13, pad=10)
    save(fig, "pf-step3-propagate.png")


def _animal(ax, x, y, kind="cat", s=1.0, color=WHITE, lw=2.0, alpha=1.0, var=None):
    """Tiny stick-figure animal icon: head circle + two ears + dot eyes.
    cat = upright pointy (triangle) ears; dog = drooping (oval) ears.
    `s` scales the icon. `var` is a per-instance heterogeneity dict so no two
    exemplars look identical:
        rh   head-roundness (head x/y aspect)     ~1.0
        er   ear size multiplier                  ~1.0
        ea   extra ear angle/lean (deg)           ~0
        eye  eye-spacing multiplier               ~1.0
        tilt whole-icon tilt (deg, via ear/eye shifts) ~0
        tail tail length multiplier (dogs) / whisker spread (cats) ~1.0
    Returns the (x,y) anchor so callers can draw lines to it.
    """
    from matplotlib.patches import Polygon
    import numpy as _np
    v = {"rh": 1.0, "er": 1.0, "ea": 0.0, "eye": 1.0, "tilt": 0.0, "tail": 1.0}
    if var:
        v.update(var)
    rx = 0.16 * s * (1.0 / v["rh"] ** 0.5)
    ry = 0.16 * s * (v["rh"] ** 0.5)
    head = Ellipse((x, y), 2*rx, 2*ry, angle=v["tilt"],
                   fill=False, ec=color, lw=lw, alpha=alpha, zorder=5)
    ax.add_patch(head)
    if kind == "cat":
        # two upright triangle ears, size/lean varied per instance
        er, ea, tl = v["er"], v["ea"], v["tilt"]
        for sgn in (-1, 1):
            ex = x + sgn * 0.10 * s
            tip_x = ex + sgn*0.02*s + _np.deg2rad(tl)*0.18*s
            ear = Polygon([[ex - 0.06*s*er, y + 0.10*s],
                           [ex + 0.06*s*er, y + 0.10*s],
                           [tip_x + sgn*_np.deg2rad(ea)*0.4*s, y + (0.20+0.08*er)*s]],
                          closed=True, fill=False, ec=color, lw=lw, alpha=alpha, zorder=5)
            ax.add_patch(ear)
        # whiskers, spread varied
        sp = v["tail"]
        for sgn in (-1, 1):
            ax.plot([x + sgn*rx, x + sgn*(rx+0.10*s*sp)], [y, y+0.02*s],
                    color=color, lw=lw*0.6, alpha=alpha, zorder=5)
            ax.plot([x + sgn*rx, x + sgn*(rx+0.10*s*sp)], [y, y-0.03*s],
                    color=color, lw=lw*0.6, alpha=alpha, zorder=5)
    else:  # dog: drooping oval ears on the sides, droop/size varied
        er, ea = v["er"], v["ea"]
        for sgn in (-1, 1):
            ear = Ellipse((x + sgn*0.14*s, y - 0.02*s), 0.10*s*er, 0.22*s*er,
                          angle=sgn*(20 + ea), fill=False, ec=color, lw=lw,
                          alpha=alpha, zorder=5)
            ax.add_patch(ear)
        # a little tail stub, length varied (a dog-only feature)
        ax.plot([x + rx, x + rx + 0.12*s*v["tail"]], [y - ry*0.4, y - ry*0.4 + 0.06*s],
                color=color, lw=lw*0.8, alpha=alpha, zorder=4, solid_capstyle="round")
    # eyes + nose, eye-spacing varied
    es = 0.06 * v["eye"]
    for sgn in (-1, 1):
        ax.plot(x + sgn*es*s, y + 0.03*s, marker=".", ms=4*s, color=color, alpha=alpha, zorder=6)
    ax.plot(x, y - 0.05*s, marker=".", ms=5*s, color=color, alpha=alpha, zorder=6)
    return (x, y)


def fig_exemplar_vote():
    """Exemplar model as a similarity-weighted vote: a NEW query exemplar comes
    in at top; two stored categories (cats left, dogs right) hold exemplars; lines
    from the query to each stored exemplar are weighted by similarity (the vote).
    The query is more cat-like, so the cat lines are bold and the dog lines faint.
    """
    fig, ax = plt.subplots(figsize=(9.6, 3.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")

    # per-instance heterogeneity so NO two exemplars look identical — each varies
    # on simple dimensions (head roundness, ear size/lean, eye spacing, tilt, tail).
    qvar    = {"rh": 1.10, "er": 1.05, "ea": 4,  "eye": 1.15, "tilt": -6, "tail": 1.1}
    catvars = [
        {"rh": 0.92, "er": 1.15, "ea": 6,  "eye": 0.9,  "tilt": 8,   "tail": 1.2},
        {"rh": 1.18, "er": 0.85, "ea": -5, "eye": 1.2,  "tilt": -7,  "tail": 0.8},
        {"rh": 1.00, "er": 1.30, "ea": 10, "eye": 1.0,  "tilt": 3,   "tail": 1.0},
    ]
    dogvars = [
        {"rh": 1.20, "er": 1.15, "ea": 10, "eye": 1.1,  "tilt": 6,   "tail": 1.3},
        {"rh": 0.88, "er": 0.85, "ea": -8, "eye": 0.85, "tilt": -9,  "tail": 0.7},
        {"rh": 1.05, "er": 1.30, "ea": 4,  "eye": 1.25, "tilt": 4,   "tail": 1.0},
    ]

    # --- the new query exemplar, top center ---
    qx, qy = 5.0, 2.75
    _animal(ax, qx, qy, kind="cat", s=1.25, color=YELLOW, lw=2.6, var=qvar)
    ax.text(qx, qy + 0.42, "new exemplar  $x$?", color=YELLOW, fontsize=13,
            ha="center", va="bottom", fontweight="bold")

    # --- stored exemplars: cats (left cluster), dogs (right cluster) ---
    # each tuple: (x, y, similarity-to-query). cats are similar; dogs are not.
    cats = [(1.4, 0.95, 0.92), (2.5, 1.35, 0.78), (2.0, 0.55, 0.85)]
    dogs = [(7.6, 0.95, 0.22), (8.6, 1.35, 0.14), (8.1, 0.55, 0.18)]

    def sim_line(x, y, w, col):
        # line width + opacity encode similarity (the vote weight)
        ax.plot([qx, x], [qy - 0.18, y + 0.18], color=col,
                lw=0.6 + 4.2*w, alpha=0.18 + 0.62*w, zorder=2,
                solid_capstyle="round")

    for (x, y, w) in cats:
        sim_line(x, y, w, ACCENT)
    for (x, y, w) in dogs:
        sim_line(x, y, w, DIM)
    for (x, y, w), cv in zip(cats, catvars):
        _animal(ax, x, y, kind="cat", s=0.95, color=ACCENT, lw=2.0, var=cv)
    for (x, y, w), dv in zip(dogs, dogvars):
        _animal(ax, x, y, kind="dog", s=0.95, color=WHITE, lw=2.0, alpha=0.85, var=dv)

    # --- category labels ---
    ax.text(2.0, 0.02, "category: CAT  ($f=$ cat)", color=ACCENT, fontsize=12.5,
            ha="center", va="bottom", fontweight="bold")
    ax.text(8.1, 0.02, "category: DOG  ($f=$ dog)", color=DIM, fontsize=12.5,
            ha="center", va="bottom", fontweight="bold")

    # --- legend for the line encoding (placed clear of the similarity lines) ---
    ax.text(6.7, 1.95, "line = similarity $s(x, x_i)$  (the vote weight)",
            color=WHITE, fontsize=11, ha="center", va="center", style="italic")

    save(fig, "exemplar-vote.png")


if __name__ == "__main__":
    fig_hospital_tails()
    fig_die_convergence()
    fig_pi_darts()
    fig_rejection_schematic()
    fig_pi_schematic()
    fig_mh_animation()
    fig_gibbs_trace()
    fig_kemp_plate()
    fig_recipe()
    fig_is_weight_variance()
    fig_particle_filter()
    fig_pf_worked()
    fig_exemplar_vote()
    print("all Week 7 figures done")
