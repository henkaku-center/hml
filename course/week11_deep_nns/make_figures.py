#!/usr/bin/env python3
"""Week 11 — static teaching figures (dark SDS theme), deep neural networks.

Run from course/week11_deep_nns/:  python3 make_figures.py
Writes PNGs into images/. Figures are authored on the slide background (#111111) so they
composite cleanly onto the dark deck — light text, no white-on-white overflow.
Style-matched to course/week10_bayesian_nonparametrics/make_figures.py.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BG="#111111"; WHITE="#ffffff"; DIM="#999999"; ACC="#64B5F6"; RED="#EF5350"
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

# The shared four-box pipeline (used by figs 1 & 2)
PIPE=[("data\n$x$",0.4),("features\n$\\phi(x)$",2.85),("function\n$f$",5.3),
      ("prediction\n$\\hat{y}$",7.75)]
PW,PH=1.85,1.05
def draw_pipeline(ax,ybase):
    for i,(lab,x) in enumerate(PIPE):
        rbox(ax,x,ybase,PW,PH,lab,fc="#1a2230",ec=ACC,fs=14)
        if i<len(PIPE)-1:
            arrow(ax,x+PW+0.05,ybase+PH/2,PIPE[i+1][1]-0.08,ybase+PH/2,color=WHITE,lw=2.2)

# ---------------------------------------------------------------- Fig 1: master frame
def fig_four_answers_map():
    fig,ax=blank_axes((10.5,5.4))
    draw_pipeline(ax,3.0)
    # REPRESENT — spans features + function (above the pipeline)
    rbox(ax,2.55,4.75,4.9,0.95,"REPRESENT — what can it express?",
         fc="#161d16",ec=GRN,fs=14,tc=GRN,weight="bold",rs=0.15)
    for xc in (2.85+PW/2, 5.3+PW/2):
        arrow(ax,xc,4.70,xc,4.22,color=GRN,lw=1.4,ls=":",ms=11)
    # LEARN — arrow up into features/function (below the pipeline)
    rbox(ax,2.9,1.55,4.2,0.95,"LEARN — how do we find it?",
         fc="#1d1a10",ec=ORA,fs=14,tc=ORA,weight="bold",rs=0.15)
    arrow(ax,5.0,2.55,5.0,2.92,color=ORA,lw=2.2)
    # UNDERSTAND — spans the whole pipeline (bottom band)
    rbox(ax,0.4,0.15,9.2,0.95,"UNDERSTAND — why does it generalize?",
         fc="#131a20",ec=TEAL,fs=14,tc=TEAL,weight="bold",rs=0.15)
    fig.tight_layout(); fig.savefig("images/four_answers_map.png",dpi=150); plt.close(fig)
    print("wrote images/four_answers_map.png")

# ---------------------------------------------------------------- Fig 2: four answers
def fig_four_answers_close():
    fig,ax=blank_axes((10.5,5.8))
    draw_pipeline(ax,4.45)
    ax.text(0.45,3.7,"Four answers to “where does a good $f$ come from?”",
            fontsize=14,color=WHITE,ha="left",va="center")
    answers=[("1.  penalize complexity  →  ridge  (W10)",DIM),
             ("2.  grow with data  →  BNP  (W10)",DIM),
             ("3.  prior over functions  →  GP  (W10)",DIM),
             ("4.  LEARN the features  →  neural nets  (today)",YEL)]
    y=3.0
    for txt,c in answers:
        if c is YEL:
            ax.add_patch(FancyBboxPatch((0.55,y-0.34),6.9,0.72,
                         boxstyle="round,pad=0.02,rounding_size=0.12",
                         fc="#26230f",ec=YEL,lw=1.6,zorder=2))
        ax.text(0.8,y,txt,fontsize=14.5,color=c,ha="left",va="center",zorder=4,
                weight=("bold" if c is YEL else "normal"))
        y-=0.78
    fig.tight_layout(); fig.savefig("images/four_answers_close.png",dpi=150); plt.close(fig)
    print("wrote images/four_answers_close.png")

# ---------------------------------------------------------------- Fig 3: activations
def fig_activations():
    from scipy.special import erf
    x=np.linspace(-3,3,400)
    fig,ax=plt.subplots(figsize=(9,5))
    ax.axhline(0,color=EDGE,lw=1.0); ax.axvline(0,color=EDGE,lw=1.0)
    ax.plot(x,np.tanh(x),color=ACC,lw=2.8,label="tanh  (1986)")
    ax.plot(x,np.maximum(0,x),color=ORA,lw=2.8,label="ReLU  (2012)")
    ax.plot(x,0.5*x*(1+erf(x/np.sqrt(2))),color=GRN,lw=2.8,label="GELU  (today)")
    ax.set_xlim(-3,3); ax.set_ylim(-1.4,3.1)
    ax.set_xlabel("input to the unit"); ax.set_ylabel("activation  $g(x)$")
    ax.legend(facecolor=PANEL,edgecolor=EDGE,labelcolor="#dddddd",fontsize=13,loc="upper left")
    fig.tight_layout(); fig.savefig("images/activations.png",dpi=150); plt.close(fig)
    print("wrote images/activations.png")

# ---------------------------------------------------------------- Fig 4: embedding arithmetic
def fig_embedding_arith():
    man=np.array([2.4,0.6]); woman=np.array([2.0,1.8])
    roy=np.array([0.8,1.6])
    king=man+roy; queen=woman+roy
    fig,ax=blank_axes((9,5.6),xlim=(-0.2,4.4),ylim=(-0.25,4.0))
    ax.axhline(0,color=EDGE,lw=1.0); ax.axvline(0,color=EDGE,lw=1.0)
    for v,lab,c,dx,dy in [(man,"man",ACC,0.16,-0.16),(woman,"woman",ACC,-0.42,0.22),
                          (king,"king",ORA,0.18,-0.05),(queen,"queen",ORA,0.20,0.10)]:
        arrow(ax,0,0,v[0],v[1],color=c,lw=2.4,ms=15)
        ax.text(v[0]+dx,v[1]+dy,lab,color=c,fontsize=15,ha="left",va="center",weight="bold")
    # composition path: king -> (-man) -> (+woman) landing near queen
    arrow(ax,king[0],king[1],roy[0],roy[1],color=GRN,lw=2.0,ls="--",ms=13)
    ax.text((king[0]+roy[0])/2+0.10,(king[1]+roy[1])/2-0.22,"$-$ man",color=GRN,fontsize=14)
    arrow(ax,roy[0],roy[1],queen[0]-0.10,queen[1]-0.10,color=GRN,lw=2.0,ls="--",ms=13)
    ax.text((roy[0]+queen[0])/2-0.62,(roy[1]+queen[1])/2+0.22,"$+$ woman",color=GRN,fontsize=14)
    ax.scatter([queen[0]],[queen[1]],marker="*",s=330,color=YEL,zorder=6,
               edgecolor="#222222",linewidth=0.8)
    ax.text(queen[0]+0.14,queen[1]-0.30,"king $-$ man $+$ woman\n$\\approx$ queen",
            color=YEL,fontsize=13,ha="left",va="top")
    ax.text(4.3,-0.18,"embedding dim 1",color=DIM,fontsize=11,ha="right",va="top")
    ax.text(-0.14,3.92,"embedding dim 2",color=DIM,fontsize=11,ha="right",va="top",rotation=90)
    fig.tight_layout(); fig.savefig("images/embedding_arith.png",dpi=150); plt.close(fig)
    print("wrote images/embedding_arith.png")

# ---------------------------------------------------------------- Fig 5: delta rule anatomy
def fig_delta_rule_anatomy():
    fig,ax=blank_axes((10.5,5.2))
    # equation, composed from pieces at known x so callout arrows can target terms
    ey=4.1; fs=40
    pieces=[("$\\Delta w_j$",1.9,WHITE),("$=$",3.05,WHITE),("$\\eta$",3.75,GRN),
            ("$\\cdot$",4.35,WHITE),("$(t-y)$",5.45,RED),("$\\cdot$",6.55,WHITE),
            ("$x_j$",7.25,ACC)]
    for s,x,c in pieces:
        ax.text(x,ey,s,fontsize=fs,color=c,ha="center",va="center")
    # callouts: labels live in their OWN band at the bottom; arrows rise to the terms
    callouts=[(2.30,GRN,3.75,"step size $\\eta$ — same role as\nQ-learning's $\\alpha$  (Week 8)"),
              (5.45,RED,5.45,"error — how wrong\nwere we?"),
              (8.30,ACC,7.25,"input — who\ncontributed?")]
    for lx,c,tx,txt in callouts:
        ax.text(lx,1.05,txt,fontsize=13.5,color=c,ha="center",va="center")
        arrow(ax,lx,1.75,tx,3.35,color=c,lw=1.8,ms=13)
    fig.tight_layout(); fig.savefig("images/delta_rule_anatomy.png",dpi=150); plt.close(fig)
    print("wrote images/delta_rule_anatomy.png")

# ---------------------------------------------------------------- Fig 6: scaling laws
def fig_scaling_laws():
    rng=np.random.default_rng(11)
    fig,axs=plt.subplots(1,3,figsize=(11,3.9))
    panels=[("parameters  $N$",ACC,-0.076),("data  $D$",ORA,-0.095),("compute  $C$",GRN,-0.050)]
    for ax,(ttl,c,slope) in zip(axs,panels):
        x=np.logspace(0,6,40)
        y=3.2*x**slope
        y*=np.exp(rng.normal(0,0.012,len(x)))
        ax.loglog(x,y,color=c,lw=2.6,marker="o",ms=3.5,markerfacecolor=c)
        ax.set_title(f"loss vs {ttl}",fontsize=13.5,color=c,pad=8)
        ax.grid(True,which="major",color="#2a2a35",lw=0.7)
        ax.tick_params(which="both",length=0,labelleft=False,labelbottom=False)
        ax.set_xlabel(ttl+"  (log)",fontsize=12)
    axs[0].set_ylabel("test loss  (log)",fontsize=12)
    fig.suptitle("Scaling laws: loss falls as a power law in every resource",
                 color=WHITE,fontsize=14,y=0.99)
    fig.tight_layout(rect=[0,0,1,0.92])
    fig.savefig("images/scaling_laws.png",dpi=150); plt.close(fig)
    print("wrote images/scaling_laws.png")

# ---------------------------------------------------------------- Fig 7: in-context learning setup
def fig_icl_setup():
    fig,ax=blank_axes((10.5,5.4))
    # left: frozen-weights box with a small network glyph inside
    rbox(ax,0.45,1.9,3.3,3.0,"",fc="#1a2230",ec=ACC,lw=1.8,rs=0.15)
    ax.text(2.1,4.45,"frozen weights $\\theta$",fontsize=14.5,color=ACC,
            ha="center",va="center",weight="bold")
    ax.text(2.1,4.02,"(no update)",fontsize=12.5,color=DIM,ha="center",va="center")
    layers=[(1.15,[2.35,3.05]),(2.1,[2.15,2.7,3.25]),(3.05,[2.35,3.05])]
    for li in range(len(layers)-1):
        for y0 in layers[li][1]:
            for y1 in layers[li+1][1]:
                ax.plot([layers[li][0],layers[li+1][0]],[y0,y1],
                        color="#3f5a75",lw=1.0,zorder=4)
    for lx,ys in layers:
        ax.scatter([lx]*len(ys),ys,s=110,color=ACC,zorder=5,
                   edgecolor="#0d141c",linewidth=1.0)
    # right: prompt card (monospace-ish)
    rbox(ax,5.6,1.9,4.0,3.4,"",fc="#20201a",ec=ORA,lw=1.8,rs=0.15)
    ax.text(7.6,4.9,"prompt",fontsize=13,color=ORA,ha="center",va="center",weight="bold")
    lines=[("plip → blue",WHITE,4.30),("plap → red",WHITE,3.63),("plip → ?",YEL,2.96)]
    for txt,c,y in lines:
        ax.text(6.0,y,txt,fontsize=15,color=c,ha="left",va="center",family="DejaVu Sans Mono")
    ax.plot([6.0,9.2],[2.60,2.60],color="#4a4636",lw=1.0)
    ax.text(6.0,2.25,"model continues:",fontsize=11.5,color=DIM,ha="left",va="center")
    ax.text(8.1,2.25,"blue",fontsize=15,color=GRN,ha="left",va="center",
            family="DejaVu Sans Mono",weight="bold")
    # flow: prompt goes IN (top arrow), prediction comes OUT (bottom arrow) —
    # each label sits in its own clear band, never on the other arrow
    arrow(ax,5.5,2.96,3.85,2.96,color=DIM,lw=2.0)
    ax.text(4.68,3.24,"one forward pass",fontsize=11.5,color=DIM,ha="center",va="center")
    arrow(ax,3.85,2.25,5.5,2.25,color=GRN,lw=2.2)
    ax.text(4.68,1.95,"next-token prediction",fontsize=11.5,color=GRN,ha="center",va="center")
    ax.text(2.1,1.25,"learning happens with\nNO weight change",fontsize=12.5,color=YEL,
            ha="center",va="center")
    ax.text(7.6,1.25,"in-context learning: the “learning”\nis in the activations, not the weights",
            fontsize=11.5,color=DIM,ha="center",va="center")
    fig.tight_layout(); fig.savefig("images/icl_setup.png",dpi=150); plt.close(fig)
    print("wrote images/icl_setup.png")

# ---------------------------------------------------------------- Fig 8: the ICL debate
def fig_icl_debate():
    fig,ax=blank_axes((10.5,5.2))
    # left panel — implicit Bayes
    rbox(ax,0.3,0.5,4.55,5.0,"",fc="#131a24",ec=ACC,lw=2.0,rs=0.15)
    ax.text(2.575,4.95,"ICL = implicit Bayes?",fontsize=15.5,color=ACC,
            ha="center",va="center",weight="bold")
    ll=[("pretraining $\\approx$ fits a prior\nover latent patterns",4.05),
        ("prompt examples $\\approx$ observations",3.10),
        ("continuation $\\approx$ posterior\npredictive",2.25)]
    for txt,y in ll:
        ax.text(2.575,y,txt,fontsize=13,color=WHITE,ha="center",va="center")
    ax.text(2.575,1.05,"(Xie et al. 2022; Ye et al. 2024)",fontsize=11.5,color=DIM,
            ha="center",va="center")
    # right panel — not so fast
    rbox(ax,5.15,0.5,4.55,5.0,"",fc="#241315",ec=RED,lw=2.0,rs=0.15)
    ax.text(7.425,4.95,"Not so fast",fontsize=15.5,color=RED,
            ha="center",va="center",weight="bold")
    rl=[("exchangeability predicts\nmartingale behavior",3.55),
        ("LLM predictions violate it",2.45)]
    for txt,y in rl:
        ax.text(7.425,y,txt,fontsize=13,color=WHITE,ha="center",va="center")
    ax.text(7.425,1.05,"(Falck et al. 2024)",fontsize=11.5,color=DIM,
            ha="center",va="center")
    fig.tight_layout(); fig.savefig("images/icl_debate.png",dpi=150); plt.close(fig)
    print("wrote images/icl_debate.png")

# ---------------------------------------------------------------- Fig 9: attention as soft lookup
def fig_attention_lookup():
    fig,ax=blank_axes((10.5,5.6))
    weights=[0.7,0.2,0.07,0.03]
    kys=[4.7,3.5,2.3,1.1]
    # query
    rbox(ax,0.45,2.55,1.5,0.9,"query\n$q$",fc="#1a2230",ec=ACC,fs=13.5)
    # key–value rows
    for i,(w,y) in enumerate(zip(weights,kys),start=1):
        rbox(ax,4.35,y-0.42,1.25,0.84,f"$k_{i}$",fc="#20201a",ec=ORA,fs=14)
        rbox(ax,5.85,y-0.42,1.25,0.84,f"$v_{i}$",fc="#161d16",ec=GRN,fs=14)
        arrow(ax,2.05,3.0,4.28,y,color=ACC,lw=0.8+6.0*w,ms=11+9*w)
        # weight label rides just above ITS OWN arrow near the key end, where the
        # fan has separated the arrows — never at the same y as another arrow
        t=(3.9-2.05)/(4.28-2.05)
        ax.text(3.9,3.0+t*(y-3.0)+0.30,f"{w:.2f}",fontsize=13,
                color=ACC,ha="center",va="center")
        arrow(ax,7.15,y,8.35,3.0,color=GRN,lw=0.8+6.0*w,ms=11+9*w)
    ax.text(2.6,5.45,"softmax weights",fontsize=12,color=DIM,ha="center",va="center")
    # output
    rbox(ax,8.45,2.5,1.45,1.0,"$\\sum_i w_i v_i$",fc="#161d16",ec=GRN,fs=14)
    ax.text(9.175,2.15,"weighted mix",fontsize=11.5,color=DIM,ha="center",va="center")
    ax.text(5.7,0.25,"a dictionary lookup, but SOFT: every value contributes, weighted by key match",
            fontsize=12.5,color=DIM,ha="center",va="center")
    fig.tight_layout(); fig.savefig("images/attention_lookup.png",dpi=150); plt.close(fig)
    print("wrote images/attention_lookup.png")

# ---------------------------------------------------------------- Fig 10: transformer block
def fig_transformer_block():
    fig,ax=blank_axes((7.6,8.2),xlim=(0,7.6),ylim=(0,8.2))
    stack=[("token embeddings + positions","#1a2230",ACC,WHITE),
           ("self-attention\n(every token attends to every token)","#20201a",ORA,WHITE),
           ("+ residual, normalize","#1c1c22",DIM,"#cccccc"),
           ("MLP  (per token)","#161d16",GRN,WHITE),
           ("+ residual, normalize","#1c1c22",DIM,"#cccccc")]
    x0,w=1.05,4.3
    ys=[0.5,1.9,3.7,5.0,6.4]
    hs=[0.9,1.3,0.8,0.9,0.8]
    for (lab,fc,ec,tc),y,h in zip(stack,ys,hs):
        rbox(ax,x0,y,w,h,lab,fc=fc,ec=ec,tc=tc,fs=13.5,rs=0.12)
    for i in range(len(ys)-1):
        arrow(ax,x0+w/2,ys[i]+hs[i]+0.06,x0+w/2,ys[i+1]-0.10,color=WHITE,lw=2.2)
    arrow(ax,x0+w/2,ys[-1]+hs[-1]+0.06,x0+w/2,ys[-1]+hs[-1]+0.55,color=WHITE,lw=2.2)
    ax.text(x0+w/2,ys[-1]+hs[-1]+0.75,"to the next block …",fontsize=12,color=DIM,
            ha="center",va="center")
    # "× N layers" bracket spanning attention → final normalize
    bx=5.75; ytop=ys[-1]+hs[-1]; ybot=ys[1]
    ax.plot([bx,bx+0.18,bx+0.18,bx],[ybot,ybot+0.12,ytop-0.12,ytop],color=YEL,lw=2.0)
    ax.text(bx+0.42,(ybot+ytop)/2,"$\\times\\,N$ layers",fontsize=15,color=YEL,
            ha="left",va="center",rotation=90)
    fig.tight_layout(); fig.savefig("images/transformer_block.png",dpi=150); plt.close(fig)
    print("wrote images/transformer_block.png")

# ---------------------------------------------------------------- Fig 11: data → vector → point
def fig_data_to_vector():
    """Three stages, left→right: bento card → column vector [500, 8] → point on a 2-D plot."""
    fig=plt.figure(figsize=(11,4.4))
    gs=fig.add_gridspec(1,3,width_ratios=[1.15,0.8,1.25],wspace=0.5,
                        left=0.03,right=0.965,top=0.90,bottom=0.16)
    # ---- stage 1: the bento card (a thing in the world) ----
    a1=fig.add_subplot(gs[0]); a1.set_xlim(0,10); a1.set_ylim(0,10); a1.axis("off")
    rbox(a1,0.8,1.9,8.4,6.4,"",fc=PANEL,ec=ORA,lw=1.8,rs=0.35)
    a1.text(5.0,7.15,"tonkatsu bento",fontsize=15,color=ORA,weight="bold",
            ha="center",va="center")
    a1.text(2.0,5.55,"weight:  500 g",fontsize=14,color=WHITE,ha="left",va="center")
    a1.text(2.0,4.35,"crunch:  8 / 10",fontsize=14,color=WHITE,ha="left",va="center")
    a1.text(5.0,2.95,"(a thing in the world)",fontsize=11,color=DIM,ha="center",va="center")
    # ---- stage 2: the column vector, big brackets drawn as lines ----
    a2=fig.add_subplot(gs[1]); a2.set_xlim(0,10); a2.set_ylim(0,10); a2.axis("off")
    bl,br,bt,bb,tip=2.6,7.4,7.9,2.5,0.7
    a2.plot([bl+tip,bl,bl,bl+tip],[bt,bt,bb,bb],color=WHITE,lw=2.4)
    a2.plot([br-tip,br,br,br-tip],[bt,bt,bb,bb],color=WHITE,lw=2.4)
    a2.text(5.0,6.35,"500",fontsize=25,color=WHITE,ha="center",va="center")
    a2.text(5.0,4.05,"8",fontsize=25,color=WHITE,ha="center",va="center")
    a2.text(5.0,1.15,"the same bento,\nnow a column of numbers",fontsize=11,
            color=DIM,ha="center",va="center")
    # ---- stage 3: the point on a 2-D plot ----
    a3=fig.add_subplot(gs[2])
    a3.set_xlim(0,700); a3.set_ylim(0,10)
    a3.set_xticks([0,250,500,700]); a3.set_yticks([0,5,8,10])
    a3.set_xlabel("weight (g)",fontsize=12); a3.set_ylabel("crunch (0–10)",fontsize=12)
    a3.plot([500,500],[0,8],color=DIM,lw=1.0,ls="--",zorder=2)
    a3.plot([0,500],[8,8],color=DIM,lw=1.0,ls="--",zorder=2)
    a3.scatter([500],[8],s=130,color=ACC,zorder=5,edgecolor="#0d141c",linewidth=1.0)
    a3.text(478,7.0,"tonkatsu bento\n(500, 8)",fontsize=12,color=ACC,
            ha="right",va="top")
    # ---- arrows between stages (figure coordinates), labels in their own band above.
    # Arrow 2 is placed off the axes' TRUE positions so it clears stage 3's rotated
    # y-axis label ("crunch (0–10)" hangs ~0.07 fig-units left of the a3 spine).
    p2,p3=a2.get_position(),a3.get_position()
    for x0,x1,lab in [(0.335,0.385,"measure"),(p3.x0-0.125,p3.x0-0.075,"plot")]:
        fig.add_artist(FancyArrowPatch((x0,0.52),(x1,0.52),transform=fig.transFigure,
                       arrowstyle="-|>",mutation_scale=18,color=WHITE,lw=2.2))
        fig.text((x0+x1)/2,0.60,lab,fontsize=12,color=DIM,ha="center",va="center")
    fig.savefig("images/data_to_vector.png",dpi=150); plt.close(fig)
    print("wrote images/data_to_vector.png")

# ---------------------------------------------------------------- Fig 12: dot product, worked
def fig_dot_product_worked():
    """u=[3,4], v=[4,3] from the origin with the angle arc, beside the worked arithmetic."""
    from matplotlib.patches import Arc
    fig=plt.figure(figsize=(11,4.6))
    gs=fig.add_gridspec(1,2,width_ratios=[0.92,1.15],wspace=0.30,
                        left=0.06,right=0.965,top=0.93,bottom=0.13)
    # ---- left: the two vectors on a small grid ----
    ax=fig.add_subplot(gs[0]); ax.set_aspect("equal")
    ax.set_xlim(-0.3,5.3); ax.set_ylim(-0.3,5.3)
    ax.set_xticks(range(6)); ax.set_yticks(range(6))
    ax.grid(True,color="#2a2a35",lw=0.7)
    arrow(ax,0,0,3,4,color=ACC,lw=2.8,ms=17)
    arrow(ax,0,0,4,3,color=RED,lw=2.8,ms=17)
    ax.text(2.75,4.45,"u = [3, 4]",fontsize=14,color=ACC,ha="center",va="center",weight="bold")
    ax.text(4.4,2.4,"v = [4, 3]",fontsize=14,color=RED,ha="center",va="center",weight="bold")
    ax.add_patch(Arc((0,0),3.0,3.0,theta1=36.87,theta2=53.13,color=YEL,lw=2.0))
    # single-char θ fits INSIDE the narrow 16° wedge; the worked value lives in the panel
    ax.text(1.27,1.27,r"$\theta$",fontsize=13,color=YEL,ha="center",va="center")
    # ---- right: the arithmetic, one step per band, nothing over the plot ----
    a2=fig.add_subplot(gs[1]); a2.set_xlim(0,10); a2.set_ylim(0,10); a2.axis("off")
    rbox(a2,0.25,0.6,9.5,8.9,"",fc=PANEL,ec=EDGE,lw=1.4,rs=0.25)
    a2.text(1.1,8.35,r"$u \cdot v \;=\; 3{\times}4 \,+\, 4{\times}3$",
            fontsize=18,color=WHITE,ha="left",va="center")
    a2.text(2.25,6.85,r"$=\; 12 + 12 \;=\; 24$",fontsize=18,color=WHITE,ha="left",va="center")
    a2.text(1.1,5.35,r"$|u| = \sqrt{3^2+4^2} = 5, \quad |v| = \sqrt{4^2+3^2} = 5$",
            fontsize=14,color="#cccccc",ha="left",va="center")
    a2.text(1.1,3.75,r"$\cos\theta \;=\; 24 \,/\, (5{\times}5) \;=\; 0.96$",
            fontsize=18,color=YEL,ha="left",va="center")
    a2.text(1.1,2.15,"→  nearly the same direction",fontsize=14.5,color=GRN,
            ha="left",va="center")
    fig.savefig("images/dot_product_worked.png",dpi=150); plt.close(fig)
    print("wrote images/dot_product_worked.png")

if __name__=="__main__":
    fig_four_answers_map()
    fig_four_answers_close()
    fig_activations()
    fig_embedding_arith()
    fig_delta_rule_anatomy()
    fig_scaling_laws()
    fig_icl_setup()
    fig_icl_debate()
    fig_attention_lookup()
    fig_transformer_block()
    fig_data_to_vector()
    fig_dot_product_worked()
    print("done.")
