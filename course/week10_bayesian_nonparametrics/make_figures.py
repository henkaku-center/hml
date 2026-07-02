#!/usr/bin/env python3
"""Week 10 — static teaching figures (dark SDS theme), Block 1 (bias-variance → double descent).

Run from course/week10_bayesian_nonparametrics/:  python3 make_figures.py
Writes PNGs into images/. Figures are authored on the slide background (#111111) so they
composite cleanly onto the dark deck — light text, no white-on-white overflow.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG="#111111"; WHITE="#ffffff"; DIM="#999999"; ACC="#64B5F6"; RED="#EF5350"
ORA="#FFA726"; GRN="#66BB6A"; YEL="#FFEB3B"; TEAL="#4DD0E1"; PUR="#BA68C8"
plt.rcParams.update({
    "figure.facecolor":BG, "axes.facecolor":BG, "savefig.facecolor":BG,
    "text.color":WHITE, "axes.labelcolor":"#cfcfcf",
    "xtick.color":DIM, "ytick.color":DIM, "axes.edgecolor":"#3a3a48",
    "font.size":12, "font.family":"DejaVu Sans",
})
os.makedirs("images", exist_ok=True)

def truef(x):
    return 1.7*(x-0.18)*(x-0.55)*(x-0.88)*5   # a cubic on [0,1], range ~[-1,1]

# ---------------------------------------------------------------- Fig 1: three fits
def fig_three_fits():
    rng=np.random.default_rng(3)
    xs=np.sort(rng.uniform(0.03,0.97,18)); ys=truef(xs)+0.17*rng.standard_normal(18)
    xg=np.linspace(0,1,300)
    fig,axs=plt.subplots(1,3,figsize=(11,3.5))
    panels=[(1,"Underfit  (degree 1)","high bias",RED),
            (3,"Good fit  (degree 3)","low bias, low variance",GRN),
            (12,"Overfit  (degree 12)","high variance",ORA)]
    for ax,(d,ttl,sub,c) in zip(axs,panels):
        coef=np.polyfit(xs,ys,d); yp=np.polyval(coef,xg)
        ax.plot(xg,truef(xg),color=WHITE,lw=2.2,label="truth")
        ax.plot(xg,np.clip(yp,-2.6,2.6),color=c,lw=2.4,label="fit")
        ax.scatter(xs,ys,color=YEL,s=52,zorder=6,edgecolor="white",linewidth=1.1)
        ax.set_title(ttl,fontsize=12,color=c,pad=8)
        ax.text(0.5,-0.10,sub,transform=ax.transAxes,ha="center",va="top",color=DIM,fontsize=10.5)
        ax.set_ylim(-2.6,2.6); ax.set_xlim(0,1); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Same data, three model complexities",color=WHITE,fontsize=14,y=0.99)
    fig.tight_layout(rect=[0,0.04,1,0.93])
    fig.savefig("images/bv_three_fits.png",dpi=150); plt.close(fig)
    print("wrote images/bv_three_fits.png")

# ---------------------------------------------------------------- Fig 2: the U-curve
def fig_ucurve():
    c=np.linspace(0,1,300)
    bias2=1.45*np.exp(-4.2*c)+0.03
    var=0.045*np.exp(3.4*c)
    tot=bias2+var
    fig,ax=plt.subplots(figsize=(6.6,4.2))
    ax.plot(c,bias2,color=RED,lw=2.2,label="bias²  (falls with complexity)")
    ax.plot(c,var,color=ORA,lw=2.2,label="variance  (rises with complexity)")
    ax.plot(c,tot,color=ACC,lw=3.0,label="test error = bias² + variance")
    imin=int(np.argmin(tot))
    ax.axvline(c[imin],color=DIM,ls=":",lw=1.3)
    ax.scatter([c[imin]],[tot[imin]],color=YEL,zorder=6,s=40,edgecolor="#222",linewidth=0.6)
    ax.annotate("sweet spot",(c[imin],tot[imin]),textcoords="offset points",
                xytext=(10,10),color=YEL,fontsize=11)
    ax.set_xlabel("model complexity  →"); ax.set_ylabel("error")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(0,1.7); ax.set_xlim(0,1)
    ax.legend(facecolor="#181820",edgecolor="#3a3a48",labelcolor="#dddddd",
              fontsize=10,loc="upper center")
    ax.set_title("The classical bias–variance tradeoff",color=WHITE,fontsize=13,pad=8)
    fig.tight_layout(); fig.savefig("images/bv_ucurve.png",dpi=150); plt.close(fig)
    print("wrote images/bv_ucurve.png")

# ---------------------------------------------------------------- Fig 3: double descent
def fig_double_descent():
    p=np.linspace(0.02,4.0,600)        # capacity in units of p/n; threshold at 1
    Uleft = 0.9*np.exp(-5*p)+0.16+0.5*p**2
    Uright = 0.16+0.62*np.exp(-1.9*(p-1))
    base = np.where(p<=1.0, Uleft, Uright)
    spike = 1.75/(1+((p-1)/0.05)**2)
    test = base + spike
    fig,ax=plt.subplots(figsize=(8.2,4.3))
    # classical U (the half we usually teach) — dashed, only up to the threshold
    mleft = p<=1.0
    ax.plot(p[mleft],Uleft[mleft],color=DIM,lw=1.8,ls="--",label="classical U-curve (the half we teach)")
    # full double-descent test error
    ax.plot(p,test,color=ACC,lw=3.0,label="test error (full picture)")
    ax.axvline(1.0,color=RED,ls=":",lw=1.4)
    ax.text(1.05,2.95,"p = n",color=RED,fontsize=11.5,va="top")
    ax.annotate("variance\nexplodes",(1.02,test.max()*0.62),textcoords="offset points",
                xytext=(16,-2),color=RED,fontsize=10)
    ax.annotate("second descent\n(min-norm = implicit prior)",(2.7,Uright[np.argmin(np.abs(p-2.7))]),
                textcoords="offset points",xytext=(-24,52),color=GRN,fontsize=10.5,
                arrowprops=dict(arrowstyle="->",color=GRN,lw=1.2))
    ax.text(0.52,0.094,"underparameterized",color=DIM,fontsize=9.5,ha="center")
    ax.text(2.85,0.094,"overparameterized",color=DIM,fontsize=9.5,ha="center")
    ax.set_yscale("log")
    ax.set_xlabel("capacity  (parameters ÷ training points,  p / n)  →")
    ax.set_ylabel("test error  (log)")
    ax.set_xticks([0,1,2,3,4]); ax.set_xticklabels(["0","n","2n","3n","4n"])
    ax.set_xlim(0,4); ax.set_ylim(0.08,3.2)
    ax.legend(facecolor="#181820",edgecolor="#3a3a48",labelcolor="#dddddd",fontsize=10,loc="upper right")
    ax.set_title("Double descent: the U-curve is only the left half",color=WHITE,fontsize=13,pad=8)
    fig.tight_layout(); fig.savefig("images/double_descent.png",dpi=150); plt.close(fig)
    print("wrote images/double_descent.png")

# ---------------------------------------------------------------- Fig 4: partition blow-up
def fig_partition_blowup():
    bell=[1]; row=[1]
    for n in range(1,16):
        nr=[row[-1]]
        for x in row: nr.append(nr[-1]+x)
        bell.append(nr[0]); row=nr
    ns=list(range(1,16)); Bn=bell[1:16]
    fig,ax=plt.subplots(figsize=(7.2,4.3))
    ax.semilogy(ns,[2**n for n in ns],color=DIM,lw=1.8,ls="--",label="$2^n$")
    ax.semilogy(ns,Bn,color=ACC,lw=3,marker="o",ms=5,
                label="ways to partition $n$ points  (Bell number $B_n$)")
    ax.annotate(f"$B_{{15}}$ = {Bn[-1]:,}",(15,Bn[-1]),textcoords="offset points",
                xytext=(-150,-6),color=ACC,fontsize=10.5)
    ax.set_xlabel("number of data points  n"); ax.set_ylabel("number of clusterings  (log)")
    ax.set_xlim(1,15.5); ax.set_xticks(range(1,16,2))
    ax.legend(facecolor="#181820",edgecolor="#3a3a48",labelcolor="#dddddd",fontsize=10.5,loc="upper left")
    ax.set_title("“How many clusters?” — the choices explode",color=WHITE,fontsize=13,pad=8)
    fig.tight_layout(); fig.savefig("images/partition_blowup.png",dpi=150); plt.close(fig)
    print("wrote images/partition_blowup.png")

# ---------------------------------------------------------------- Fig 5: GP prior vs posterior
def fig_gp_prior_posterior():
    rng=np.random.default_rng(1)
    x=np.linspace(0,1,140)
    def K(a,b,l=0.12): return np.exp(-(a[:,None]-b[None,:])**2/(2*l*l))
    Kxx=K(x,x)+1e-9*np.eye(len(x)); L=np.linalg.cholesky(Kxx)
    fig,(axp,axo)=plt.subplots(1,2,figsize=(11,4.0),sharey=True)
    cols=[ACC,RED,GRN,ORA,PUR]
    axp.fill_between(x,-2,2,color=ACC,alpha=0.08)
    for i in range(5):
        axp.plot(x,L@rng.standard_normal(len(x)),lw=1.6,alpha=0.9,color=cols[i])
    axp.set_title("Prior — samples before any data",color=WHITE,fontsize=12)
    xt=np.array([0.13,0.40,0.63,0.86]); yt=np.array([0.7,-0.9,0.5,-0.3])
    Ktt=K(xt,xt)+1e-6*np.eye(len(xt)); Kxt=K(x,xt)
    mu=Kxt@np.linalg.solve(Ktt,yt)
    cov=Kxx-Kxt@np.linalg.solve(Ktt,Kxt.T)
    sd=np.sqrt(np.clip(np.diag(cov),0,None))
    Lp=np.linalg.cholesky(cov+1e-8*np.eye(len(x)))
    axo.fill_between(x,mu-2*sd,mu+2*sd,color=GRN,alpha=0.13)
    for i in range(5):
        axo.plot(x,mu+Lp@rng.standard_normal(len(x)),lw=1.3,alpha=0.8,color=cols[i])
    axo.plot(x,mu,color=WHITE,lw=2.4)
    axo.scatter(xt,yt,color=YEL,zorder=6,s=45,edgecolor="#222",linewidth=0.6)
    axo.set_title("Posterior — samples must pass through the data",color=WHITE,fontsize=12)
    for ax in (axp,axo):
        ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel("input  x"); ax.set_ylim(-2.6,2.6)
    fig.suptitle("A Gaussian process is a prior over FUNCTIONS",color=WHITE,fontsize=14,y=0.99)
    fig.tight_layout(rect=[0,0,1,0.93]); fig.savefig("images/gp_prior_posterior.png",dpi=150); plt.close(fig)
    print("wrote images/gp_prior_posterior.png")

# ---------------------------------------------------------------- Fig 6: LDA topic emergence
def fig_lda_topic_emergence():
    vocab=["bento","rice","sauce","exam","study","grade","cat","nap","sun"]
    t1=np.array([.28,.24,.18,.02,.02,.02,.08,.07,.09]); t1/=t1.sum()
    t2=np.array([.03,.03,.02,.30,.26,.20,.05,.06,.05]); t2/=t2.sum()
    fig,axs=plt.subplots(1,2,figsize=(11,3.9),sharey=True)
    for ax,(t,ttl,c) in zip(axs,[(t1,"Topic 1 — “lunch”",ACC),(t2,"Topic 2 — “studying”",ORA)]):
        ax.bar(range(len(vocab)),t,color=c,width=0.72)
        ax.set_xticks(range(len(vocab))); ax.set_xticklabels(vocab,rotation=40,ha="right",fontsize=9.5,color="#cccccc")
        ax.set_title(ttl,color=c,fontsize=12); ax.set_yticks([]); ax.set_ylim(0,t1.max()*1.15)
    fig.suptitle("Topics that emerge from a tiny Chibany corpus  (each = a word distribution)",
                 color=WHITE,fontsize=13,y=0.99)
    fig.tight_layout(rect=[0,0,1,0.91]); fig.savefig("images/lda_topic_emergence.png",dpi=150); plt.close(fig)
    print("wrote images/lda_topic_emergence.png")

# ---------------------------------------------------------------- Fig 7: bento bimodal
def fig_bento_bimodal():
    rng=np.random.default_rng(7)
    w=np.concatenate([rng.normal(350,13,80), rng.normal(500,15,60), [275.0]])
    fig,ax=plt.subplots(figsize=(7.2,3.5))
    ax.hist(w,bins=30,range=(250,560),color=ACC,alpha=0.85,edgecolor="#111111",linewidth=0.5)
    ax.axvline(275,color=RED,ls=":",lw=1.6)
    ax.annotate("light outlier",(275,ax.get_ylim()[1]*0.78),textcoords="offset points",
                xytext=(8,0),color=RED,fontsize=9.5)
    ax.text(350,-1.6,"Hamburger\n≈ 350 g",ha="center",va="top",color=DIM,fontsize=9.5)
    ax.text(500,-1.6,"Tonkatsu\n≈ 500 g",ha="center",va="top",color=DIM,fontsize=9.5)
    ax.set_xlabel("bento weight  (g)"); ax.set_yticks([]); ax.set_xlim(250,560)
    ax.set_title("Bento weights cluster by type",color=WHITE,fontsize=12.5,pad=8)
    fig.tight_layout(); fig.savefig("images/bento_bimodal.png",dpi=150); plt.close(fig)
    print("wrote images/bento_bimodal.png")

# ---------------------------------------------------------------- Fig 8: kernel shapes
def fig_kernel_shapes():
    x=np.linspace(-1,1,400)
    fig,ax=plt.subplots(figsize=(7.2,3.6))
    for l,c,lab in [(0.10,RED,"short ℓ — wiggly functions"),
                    (0.25,ACC,"medium ℓ"),
                    (0.50,GRN,"long ℓ — smooth functions")]:
        ax.plot(x,np.exp(-x**2/(2*l*l)),color=c,lw=2.6,label=lab)
    ax.set_xlabel("distance between two inputs  (x − x′)")
    ax.set_ylabel("correlation  k(x, x′)")
    ax.set_yticks([0,1]); ax.set_xlim(-1,1); ax.set_ylim(0,1.05)
    ax.legend(facecolor="#181820",edgecolor="#3a3a48",labelcolor="#dddddd",fontsize=10,loc="upper right")
    ax.set_title("An RBF kernel: how far a point's influence reaches",color=WHITE,fontsize=12.5,pad=8)
    fig.tight_layout(); fig.savefig("images/kernel_shapes.png",dpi=150); plt.close(fig)
    print("wrote images/kernel_shapes.png")

# ---------------------------------------------------------------- Fig 9: DP — base measure G0 → a draw G
def fig_dp_g0_to_g():
    rng=np.random.default_rng(7)
    th=np.linspace(-3.6,3.6,500)
    def g0(x): return (0.58*np.exp(-(x+1.15)**2/(2*0.72**2))/(0.72*np.sqrt(2*np.pi))
                       +0.42*np.exp(-(x-1.45)**2/(2*0.95**2))/(0.95*np.sqrt(2*np.pi)))
    dens=g0(th)
    alpha=4.0; Kk=18
    comp=rng.random(Kk)<0.58
    locs=np.where(comp,rng.normal(-1.15,0.72,Kk),rng.normal(1.45,0.95,Kk))
    betas=rng.beta(1,alpha,Kk); rem=1.0; pis=[]
    for b in betas: pis.append(rem*b); rem*=(1-b)
    pis=np.array(pis)
    fig,axs=plt.subplots(1,2,figsize=(10,3.4))
    # left: the continuous base measure G0
    ax=axs[0]
    ax.fill_between(th,dens,color=ACC,alpha=0.22); ax.plot(th,dens,color=ACC,lw=2.3)
    ax.set_title(r"Base measure  $G_0$  —  continuous",color=WHITE,fontsize=12,pad=7)
    ax.set_xlabel(r"$\theta$  —  where cluster parameters can live",color="#cfcfcf",fontsize=10)
    ax.set_ylabel("density",color="#cfcfcf",fontsize=10)
    ax.set_xlim(-3.6,3.6); ax.set_ylim(0,dens.max()*1.18); ax.set_xticks([]); ax.set_yticks([])
    # right: a draw G — discrete weighted spikes at locations from G0
    ax=axs[1]
    sc=pis.max()*1.05
    ax.plot(th,dens/dens.max()*sc,color=DIM,lw=1.1,ls="--",alpha=0.6,label=r"$G_0$ (reference)")
    ax.vlines(locs,0,pis,color=PUR,lw=2.4)
    ax.scatter(locs,pis,color=PUR,s=24,zorder=5)
    ax.set_title(r"A draw  $G \sim \mathrm{DP}(\alpha,\,G_0)$  —  discrete",color=WHITE,fontsize=12,pad=7)
    ax.set_xlabel(r"$\theta_k \sim G_0$,   heights $=$ stick-breaking weights $\pi_k$",color="#cfcfcf",fontsize=10)
    ax.set_ylabel(r"weight  $\pi_k$",color="#cfcfcf",fontsize=10)
    ax.set_xlim(-3.6,3.6); ax.set_ylim(0,sc*1.12); ax.set_xticks([]); ax.set_yticks([])
    ax.legend(facecolor="#181820",edgecolor="#3a3a48",labelcolor="#dddddd",fontsize=8.5,loc="upper right")
    fig.tight_layout(); fig.savefig("images/dp_g0_to_g.png",dpi=150); plt.close(fig)
    print("wrote images/dp_g0_to_g.png")

# ---------------------------------------------------------------- Fig: bring it home
def fig_bring_it_home():
    # The double-descent curve, re-read as the whole week: classical U (bias/variance)
    # on the left, the interpolation spike at p=n, the benign second descent, and the
    # p->infinity end labelled as the GP / kernel limit. A dashed ridge curve shows
    # that ridge lambda = GP noise sigma^2 removes the spike.
    p=np.linspace(0.02,4.0,600)            # capacity in units of p/n; threshold at 1
    Uleft = 0.9*np.exp(-5*p)+0.16+0.5*p**2
    Uright = 0.16+0.506*np.exp(-1.9*(p-1))           # constant chosen so base is continuous at p=n
    base = np.where(p<=1.0, Uleft, Uright)
    spike = 1.75/(1+((p-1)/0.05)**2)
    test = base + spike
    # ridge lambda = GP noise sigma^2: spike gone. A small bias tax sits above the
    # interpolating curve, and it SHRINKS into the tail — far past p=n the min-norm
    # solution's implicit l2 bias already regularizes, so explicit ridge adds little.
    ridge = base*1.05 + 0.05*np.exp(-0.35*np.maximum(p-1.0,0.0))
    fig,ax=plt.subplots(figsize=(9.8,5.15))                     # wide aspect → fills the slide; bigger on-figure text
    ax.plot(p,test,color=ACC,lw=3.6,label="interpolate  (min-norm, $\\lambda=0$)")
    ax.plot(p,ridge,color=ORA,lw=3.0,ls="--",label="ridge $\\lambda$ = GP noise $\\sigma^2$")
    ax.axvline(1.0,color=RED,ls=":",lw=1.7)
    ax.text(1.06,2.62,"p = n",color=RED,fontsize=16,va="top")
    # shade the small gap where ridge sits above interpolation = the bias tax
    ax.fill_between(p,test,ridge,where=((p>1.05)&(ridge>test)),color="#9aa0a6",alpha=0.32,lw=0)
    # left half = the classical bias-variance U
    ax.text(0.30,1.20,"classical U\nbias $\\leftrightarrow$ variance",color=DIM,fontsize=13.5,ha="center")
    # second descent = benign overfitting  (text below-left of the curve, arrow up)
    ax.annotate("benign overfitting\n(kernel min-norm bias)",xy=(1.8,0.255),xytext=(1.5,0.108),
                textcoords="data",color=GRN,fontsize=13,ha="center",va="center",
                arrowprops=dict(arrowstyle="->",color=GRN,lw=1.4))
    # the gap = ridge's small bias tax, and it shrinks far out
    ax.annotate("ridge's bias tax\n(shrinks into the tail)",xy=(2.45,0.205),xytext=(2.3,0.44),
                textcoords="data",color="#d0d0d0",fontsize=12.5,ha="center",va="center",
                arrowprops=dict(arrowstyle="->",color="#9aa0a6",lw=1.3))
    # the far-right limit IS a GP  (text mid-right, arrow down to the floor)
    ax.annotate("GP / kernel limit\nNNGP (init) · NTK (GD)",xy=(3.93,Uright[-1]),xytext=(3.4,0.44),
                textcoords="data",color=ACC,fontsize=13,ha="center",va="center",
                arrowprops=dict(arrowstyle="->",color=ACC,lw=1.4))
    ax.set_yscale("log")
    ax.tick_params(labelsize=13.5)
    ax.set_xlabel("capacity  p / n   $\\longrightarrow$   width $\\to\\infty$",fontsize=16)
    ax.set_ylabel("test error  (log)",fontsize=16)
    ax.set_xticks([0,1,2,3,4]); ax.set_xticklabels(["0","n","2n","3n","$\\infty$"])
    ax.set_xlim(0,4.05); ax.set_ylim(0.08,3.2)
    ax.legend(facecolor="#181820",edgecolor="#3a3a48",labelcolor="#dddddd",fontsize=12.5,loc="upper right")
    ax.set_title("One curve, the whole week",color=WHITE,fontsize=19,pad=9)
    fig.tight_layout(); fig.savefig("images/bring_it_home.png",dpi=150); plt.close(fig)
    print("wrote images/bring_it_home.png")

if __name__=="__main__":
    fig_three_fits()
    fig_ucurve()
    fig_double_descent()
    fig_partition_blowup()
    fig_gp_prior_posterior()
    fig_lda_topic_emergence()
    fig_bento_bimodal()
    fig_kernel_shapes()
    fig_dp_g0_to_g()
    fig_bring_it_home()
    print("done.")
