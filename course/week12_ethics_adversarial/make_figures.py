#!/usr/bin/env python3
"""Week 12 — static teaching figures (dark SDS theme), ethics / adversarial + semester map.

Run from course/week12_ethics_adversarial/:  python3 make_figures.py
Writes PNGs into images/. Figures are authored on the slide background (#111111) so they
composite cleanly onto the dark deck — light text, no white-on-white overflow.
Style-matched to course/week11_deep_nns/make_figures.py.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

BG="#111111"; WHITE="#ffffff"; LIGHT="#e8e8e8"; DIM="#999999"; ACC="#64B5F6"; RED="#EF5350"
ORA="#FFA726"; GRN="#66BB6A"; YEL="#FFEB3B"; TEAL="#4DD0E1"; PUR="#BA68C8"
PANEL="#181820"; EDGE="#3a3a48"
plt.rcParams.update({
    "figure.facecolor":BG, "axes.facecolor":BG, "savefig.facecolor":BG,
    "text.color":WHITE, "axes.labelcolor":"#cfcfcf",
    "xtick.color":DIM, "ytick.color":DIM, "axes.edgecolor":EDGE,
    "font.size":13, "font.family":"DejaVu Sans",
})
os.makedirs("images", exist_ok=True)

def rbox(ax,x,y,w,h,text,fc="#1a2230",ec=ACC,fs=13,tc=WHITE,lw=1.6,weight="normal",rs=0.12):
    """Rounded box with centered text. (x,y)=lower-left, in data units."""
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.02,rounding_size={rs}",
                                fc=fc,ec=ec,lw=lw,zorder=3))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color=tc,
            weight=weight,zorder=4)

def arrow(ax,x0,y0,x1,y1,color=DIM,lw=2.0,style="-|>",ms=16,ls="-",zorder=2,rad=0.0):
    ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle=style,mutation_scale=ms,
                                 color=color,lw=lw,linestyle=ls,zorder=zorder,
                                 connectionstyle=f"arc3,rad={rad}"))

def blank_axes(figsize,xlim=(0,10),ylim=(0,6)):
    fig,ax=plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    return fig,ax

# ---------------------------------------------------------------- Fig 1: the semester map
def fig_semester_map():
    """2-D map: Marr's level (rows) x kind of computation (cols), ~11 papers as dots."""
    fig,ax=blank_axes((11,6.5),xlim=(-2.35,5.75),ylim=(-0.35,4.3))
    # --- grid: 4 columns (x 0..4), 3 rows (y 0..3) ---
    for gx in range(5):
        ax.plot([gx,gx],[0,3],color="#2b2b36",lw=0.9,zorder=1)
    for gy in range(4):
        ax.plot([0,4],[gy,gy],color="#2b2b36",lw=0.9,zorder=1)
    ax.add_patch(Rectangle((0,0),4,3,fill=False,ec=EDGE,lw=1.6,zorder=1))
    # --- column headers (outside grid, top) ---
    heads=[("Categories",0.5),("Structure",1.5),("Time /\ndynamics",2.5),("Substrate\n& limits",3.5)]
    for t,x in heads:
        ax.text(x,3.42,t,ha="center",va="center",fontsize=12.5,color=WHITE,weight="bold")
    # --- row-band labels (outside grid, left) ---
    rows=[("L1 · what & why\n(computational)",2.5),("L2 · how\n(algorithmic)",1.5),
          ("L3 · neural",0.5)]
    for t,y in rows:
        ax.text(-0.20,y,t,ha="right",va="center",fontsize=10.8,color="#cfcfcf")
    # --- meta axis + title ---
    ax.text(-2.18,1.5,"Marr's level",ha="center",va="center",rotation=90,fontsize=11,color=DIM)
    ax.text(2.0,3.98,"The semester as a map:  Marr's level  ×  kind of computation",
            ha="center",va="center",fontsize=14.5,color=WHITE,weight="bold")
    # --- papers: (label, dx, dy, color, lx, ly, ha, va, ring, tag) ---
    nodes=[
        ("Tenenbaum 1999",        0.40,2.66, ACC, 0.56,2.66,"left","center", False,None),
        ("Tenenbaum & Xu 2000",   0.40,2.26, ACC, 0.56,2.26,"left","center", True,"presented"),
        ("Tenenbaum et al. 2011", 1.85,2.62, GRN, 2.00,2.62,"left","center", False,None),
        ("Austerweil et al. 2015",1.05,2.90, GRN, 1.05,3.05,"center","bottom", False,None),
        ("Baker et al. 2007",     2.30,2.18, ORA, 2.45,2.18,"left","center", False,None),
        ("Daw et al. 2005",       2.30,1.80, ORA, 2.45,1.80,"left","center", False,None),
        ("Abbott et al. 2012",    2.30,1.42, ORA, 2.45,1.42,"left","center", False,None),
        ("Sanborn & Griffiths 2008",2.30,1.05, ORA, 2.45,1.05,"left","center", False,None),
        ("Lake et al. 2017",      3.55,2.86, PUR, 3.68,2.86,"left","center", False,None),
        ("Caliskan et al. 2017",  3.55,2.50, PUR, 3.68,2.50,"left","center", False,None),
        ("Pereira et al. 2018",   3.55,0.55, PUR, 3.68,0.55,"left","center", False,None),
    ]
    for (lab,x,y,col,lx,ly,ha,va,ring,tag) in nodes:
        if ring:
            ax.scatter([x],[y],s=300,facecolors="none",edgecolors=YEL,linewidths=2.4,zorder=4)
        ax.scatter([x],[y],s=95,color=col,edgecolor="#0d0d12",linewidth=0.8,zorder=5)
        ax.text(lx,ly,lab,ha=ha,va=va,fontsize=10,color=LIGHT,zorder=6)
        if tag:
            ax.text(lx,ly-0.205,tag,ha=ha,va="center",fontsize=8.5,color=YEL,
                    style="italic",zorder=6)
    fig.tight_layout(); fig.savefig("images/semester_map.png",dpi=150); plt.close(fig)
    print("wrote images/semester_map.png")

# ---------------------------------------------------------------- Fig 2: embedding bias
def fig_embedding_bias():
    """Occupation words projected onto a learned gender axis (Caliskan/WEAT visual)."""
    fig,ax=blank_axes((11,4.6),xlim=(-1.28,1.28),ylim=(-1.22,0.98))
    # axis line (a learned gender direction)
    arrow(ax,-1.06,0,1.06,0,color="#8a8a8a",lw=2.2,style="<->",ms=18)
    ax.plot([0,0],[-0.16,0.16],color=EDGE,lw=1.2,ls="--")
    ax.text(0,0.22,"neutral",ha="center",va="bottom",fontsize=10,color=DIM)
    # end labels (the axis)
    ax.text(-1.12,0,"← she / female",ha="right",va="center",fontsize=13,color="#cfcfcf",
            weight="bold")
    ax.text(1.12,0,"he / male →",ha="left",va="center",fontsize=13,color="#cfcfcf",
            weight="bold")
    # title + legend
    ax.text(0,0.78,"Occupations carry a gender projection they shouldn't",
            ha="center",va="center",fontsize=14,color=WHITE,weight="bold")
    ax.text(0,0.56,"yellow ◆ = genuinely gendered (reference)     blue ● = occupation",
            ha="center",va="center",fontsize=10.5,color=DIM)
    # (word, projection, up/down side, is-reference)
    words=[("queen",-0.95,"up",True),("homemaker",-0.82,"down",False),("nurse",-0.62,"up",False),
           ("teacher",-0.12,"down",False),("scientist",0.12,"up",False),("doctor",0.33,"down",False),
           ("boss",0.52,"up",False),("engineer",0.70,"down",False),("programmer",0.86,"up",False),
           ("king",0.99,"down",True)]
    for w,x,side,ref in words:
        c = YEL if ref else ACC
        mk = "D" if ref else "o"
        ax.scatter([x],[0],s=(115 if ref else 90),color=c,marker=mk,
                   edgecolor="#0d0d12",linewidth=0.8,zorder=5)
        yl    = 0.32 if side=="up" else -0.32
        ystem = 0.17 if side=="up" else -0.17
        ax.plot([x,x],[0.0,ystem],color=c,lw=1.0,alpha=0.7,zorder=3)
        ax.text(x,yl,w,ha="center",va=("bottom" if side=="up" else "top"),
                fontsize=12,color=c,zorder=6,weight=("bold" if ref else "normal"))
    # caption band (own row)
    ax.text(0,-1.06,"Word2vec-style embeddings place occupation words along a gender axis "
            "learned from the corpus — a bias inherited, not designed.",
            ha="center",va="center",fontsize=11.5,color=DIM,zorder=6)
    fig.tight_layout(); fig.savefig("images/embedding_bias.png",dpi=150); plt.close(fig)
    print("wrote images/embedding_bias.png")

# ---------------------------------------------------------------- Fig 3: fairness impossibility
def fig_fairness_impossibility():
    """Three fairness criteria in a triangle — pick (at most) two."""
    fig,ax=blank_axes((10,6.5),xlim=(0,10),ylim=(0,6.4))
    # (title, cx, cy, box-width, color, gloss)
    nodes=[("Calibration",       5.0,5.15,2.7,ACC,"scores mean the same\nacross groups"),
           ("Equalized odds",    2.5,1.90,3.1,ORA,"equal error rates\nacross groups"),
           ("Demographic parity",7.5,1.90,3.7,GRN,"equal positive rates\nacross groups")]
    cen=[(cx,cy) for (_,cx,cy,_,_,_) in nodes]
    # edges first (behind everything)
    for i in range(3):
        for j in range(i+1,3):
            ax.plot([cen[i][0],cen[j][0]],[cen[i][1],cen[j][1]],color=EDGE,lw=1.6,zorder=1)
    # title
    ax.text(5.0,6.05,"Three fairness criteria — you can't have all three",
            ha="center",va="center",fontsize=14,color=WHITE,weight="bold")
    # nodes + glosses (gloss in its own band, masked over the edge lines)
    for (title,cx,cy,w,col,gloss) in nodes:
        rbox(ax,cx-w/2,cy-0.42,w,0.84,title,fc="#15161c",ec=col,fs=14,tc=col,
             weight="bold",rs=0.14)
        ax.text(cx,cy-0.42-0.30,gloss,ha="center",va="top",fontsize=11,color="#cfcfcf",
                zorder=6,bbox=dict(boxstyle="round,pad=0.30",fc=BG,ec="none"))
    # center badge
    rbox(ax,4.05,2.63,1.9,0.78,"Pick (at most) 2",fc="#26230f",ec=YEL,fs=13.5,tc=YEL,
         weight="bold",rs=0.16)
    # caption band
    ax.text(5.0,0.42,"When base rates differ across groups, no classifier satisfies all three\n"
            "(Kleinberg et al. 2016; Chouldechova 2017).",
            ha="center",va="center",fontsize=11.5,color=DIM,zorder=6)
    fig.tight_layout(); fig.savefig("images/fairness_impossibility.png",dpi=150); plt.close(fig)
    print("wrote images/fairness_impossibility.png")

# ---------------------------------------------------------------- Fig 4: adversarial example
def _bento(ax,x0,y0,w,h,ec=ORA):
    """A simple bento icon (rice + tonkatsu) inside a lacquer box."""
    ax.add_patch(FancyBboxPatch((x0,y0),w,h,boxstyle="round,pad=0.02,rounding_size=0.14",
                 fc="#2a1d14",ec=ec,lw=2.2,zorder=3))
    # rice compartment (left)
    ax.add_patch(Rectangle((x0+0.12*w,y0+0.16*h),0.40*w,0.68*h,fc="#efe9dc",
                 ec="#cbb88f",lw=1.2,zorder=4))
    # tonkatsu cutlet (right)
    ax.add_patch(Rectangle((x0+0.58*w,y0+0.20*h),0.30*w,0.60*h,fc="#c8862c",
                 ec="#9c6a20",lw=1.2,zorder=4))
    for k in range(3):
        yy=y0+0.30*h+k*0.18*h
        ax.plot([x0+0.58*w,x0+0.88*w],[yy,yy],color="#7a5015",lw=1.0,zorder=5)

def fig_adversarial():
    """bento + tiny sticker (epsilon) -> the kiosk flips tonkatsu -> hamburger."""
    rng=np.random.default_rng(0)
    fig,ax=blank_axes((11,4.7),xlim=(0,11),ylim=(0,6.1))
    # panel 1: the bento photo
    _bento(ax,0.7,2.5,2.4,2.4,ec=ORA)
    # panel 2: the adversarial noise (deterministic speckle)
    n=rng.random((18,18))
    ax.imshow(n,extent=[4.5,6.5,2.7,4.7],cmap="gray",zorder=3,aspect="auto")
    ax.add_patch(Rectangle((4.5,2.7),2.0,2.0,fill=False,ec=DIM,lw=1.6,zorder=4))
    # panel 3: the SAME bento, now misclassified
    _bento(ax,7.9,2.5,2.4,2.4,ec=RED)
    # connectors — own clear band in the gaps, never over a box
    ax.text(3.78,3.7,"+",fontsize=42,color=WHITE,ha="center",va="center")
    ax.text(7.18,3.7,"=",fontsize=42,color=WHITE,ha="center",va="center")
    # panel top titles
    for cx,t in [(1.9,"bento photo"),(5.5,"adversarial noise"),(9.1,"same photo + sticker")]:
        ax.text(cx,5.18,t,fontsize=12.5,color=DIM,ha="center",va="center")
    # panel bottom labels
    ax.text(1.9,1.95,"kiosk: TONKATSU (99%)",fontsize=13,color=GRN,ha="center",
            va="center",weight="bold")
    ax.text(5.5,1.95,"tiny sticker (ε)",fontsize=12.5,color=DIM,ha="center",va="center")
    ax.text(9.1,1.95,"kiosk: HAMBURGER (97%)",fontsize=13,color=RED,ha="center",
            va="center",weight="bold")
    # caption band
    ax.text(5.5,0.7,"A perturbation too small for you to notice flips the model's answer — "
            "its learned geometry is brittle where yours is not.",
            fontsize=11.5,color=DIM,ha="center",va="center")
    fig.tight_layout(); fig.savefig("images/adversarial.png",dpi=150); plt.close(fig)
    print("wrote images/adversarial.png")

if __name__=="__main__":
    fig_semester_map()
    fig_embedding_bias()
    fig_fairness_impossibility()
    fig_adversarial()
    print("done.")
