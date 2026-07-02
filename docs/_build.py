#!/usr/bin/env python3
"""Build the course website from structured source content.

Reads:
  course/weekNN_*/PLAN.md      - per-week metadata for the schedule
  course/assignments/README.md - assignments index
  course/syllabus/SP26_syllabus.md - syllabus source

Writes:
  docs/index.html        - landing page (schedule driven from PLAN files)
  docs/syllabus.html     - rendered syllabus
  docs/assignments.html  - rendered assignments index
  docs/project.html      - rendered final-project guidelines (from docs/project.md)

Run from the repo root: python docs/_build.py
"""

from pathlib import Path
import re
import shutil
import sys
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSE_DIR = REPO_ROOT / "course"
DOCS_DIR = REPO_ROOT / "docs"
TEMPLATES_DIR = DOCS_DIR / "_templates"
SLIDES_OUT_DIR = DOCS_DIR / "slides"
READINGS_OUT_DIR = DOCS_DIR / "readings"
READINGS_PDF_SRC = REPO_ROOT / "resources" / "readings"
ASSIGNMENTS_OUT_DIR = DOCS_DIR / "assignments"
ASSIGNMENTS_SRC = COURSE_DIR / "assignments"

# Stencil files to publish per assignment: {assignment_slug: [filenames]}.
# These are copied from course/assignments/<slug>/ into docs/assignments/<slug>/
# so students can download them from hml.chibatech.dev. Solution files under
# course/assignments/solutions/ are deliberately NOT staged.
ASSIGNMENT_STENCILS = {
    "clusters": [
        "clusters.ipynb",
        "clusters_python.ipynb",
        "clusters_nosoln.Rmd",
        "clusters.pdf",
    ],
    "generalization": [
        "generalization.ipynb",
        "generalization_python.ipynb",
        "generalization_nosoln.Rmd",
        "generalization.pdf",
    ],
    "mc": [
        "mc_approx.pdf",
        "mc_approx.ipynb",
        "mc_approx_python.ipynb",
        "mcmc_approx.Rmd",
    ],
    "rl": [
        "rl.pdf",
        "rl_genjax.ipynb",
        "rl_python.ipynb",
        "rl_nosoln.Rmd",
        "rl_gridworld.py",   # shared env + viz module the stencils import
    ],
}

TEXTBOOK_BASE = "https://josephausterweil.github.io/probintro"
TEXTBOOK_CONTENT = REPO_ROOT / "textbook" / "content"
# The textbook's restructure migration map (old numbered URLs -> new Part
# paths); the source of truth for resolving legacy NUMERIC tags.
TEXTBOOK_URL_MAP = REPO_ROOT / "textbook" / "scripts" / "url_map.csv"
# Legacy tutorial shorthand (T1/T2/T3) → pre-restructure section dir. Kept only
# to interpret legacy numeric tags; new PLAN tags use the `Bk: <slug>` form.
TUTORIAL_PATH = {1: "intro", 2: "genjax", 3: "intro2"}
ASSIGNMENTS_URL = "assignments.html"


def build_chapter_map() -> dict:
    """Return {tutorial_number: {chapter_number: 'part/slug' path}} derived from
    the textbook's migration url_map.csv. This keeps legacy NUMERIC tags
    (``T1 Ch 4-5``) resolving after the restructure removed number prefixes
    from chapter slugs: the old numbers survive only in the migration map."""
    OLD_RE = re.compile(r"^/(intro|genjax|intro2)/(\d{2})[a-z]?_[^/]+/$")
    tut_of = {v: k for k, v in TUTORIAL_PATH.items()}
    out = {tnum: {} for tnum in TUTORIAL_PATH}
    if TEXTBOOK_URL_MAP.is_file():
        import csv
        with TEXTBOOK_URL_MAP.open() as f:
            for row in csv.DictReader(f):
                m = OLD_RE.match(row["old_path"])
                if not m:
                    continue
                tnum, chnum = tut_of[m.group(1)], int(m.group(2))
                # setdefault: '05a_...' rows must not shadow '05_...'
                out[tnum].setdefault(chnum, row["new_path"].strip("/"))
    return out


def build_chapter_name_map() -> dict:
    """Return one global {stable_name: 'part/slug'} map for NAME-based links.

    Chapters are scanned from every textbook Part (a top-level content section
    whose _index.md sets ``book_part = true``); the *stable name* is the
    chapter slug with separators normalized (``bayes-nets`` → ``bayes_nets``).
    This is what makes landing-page links robust to reordering AND to the Part
    restructure: a PLAN tags a chapter as ``Bk: generalization`` (legacy
    ``T3: generalization`` still accepted) and the builder re-derives the URL.
    """
    out = {}
    if not TEXTBOOK_CONTENT.is_dir():
        return out
    for part_dir in sorted(TEXTBOOK_CONTENT.iterdir()):
        idx = part_dir / "_index.md"
        if not (part_dir.is_dir() and idx.is_file()):
            continue
        if not re.search(r"^book_part\s*=\s*true", idx.read_text(encoding="utf-8"),
                         re.MULTILINE):
            continue
        for f in sorted(part_dir.iterdir()):
            if f.is_file() and f.suffix == ".md" and not f.name.endswith(".ja.md") \
                    and f.name != "_index.md":
                out[_norm_name(f.stem)] = f"{part_dir.name}/{f.stem}"
            elif f.is_dir() and (f / "_index.md").is_file():
                out[_norm_name(f.name)] = f"{part_dir.name}/{f.name}"
    return out


CHAPTER_MAP = None       # {tut: {num: 'part/slug'}} — populated lazily in main()
CHAPTER_NAME_MAP = None  # {stable_name: 'part/slug'} — populated lazily in main()

# ---------- hand-curated bits that live with the generator, not in Markdown ----------

HIGHLIGHTS = [
    {"title": "Bayesian Foundations",
     "body": "Build intuition for probability from counting to conjugate models, hierarchical Bayes, and Bayesian nonparametrics."},
    {"title": "Hands-on GenJAX",
     "body": "Write probabilistic programs from Week 2 onward. Model, condition, and run inference using GenJAX on JAX — no toy examples."},
    {"title": "Cognitive Models That Explain",
     "body": "Causal reasoning, generalization, reinforcement learning, and social cognition — framed as computational-level theories of the mind."},
    {"title": "Contemporary ML Connections",
     "body": "Bridge to transformers, scaling laws, RLHF, and AI alignment — see where classical models meet modern deep learning."},
    {"title": "Living Textbook",
     "body": "A free, open-source textbook on probability and probabilistic computing that grows alongside the course."},
    {"title": "Discussion-Driven",
     "body": "Weekly reflections, in-class exercises, and collaborative problem-solving — not just lectures."},
]

INFO_CARDS = {
    "assignments": [
        "Clusters (mixture models)",
        "Bayesian Generalization",
        "Monte Carlo Estimation",
        "Reinforcement Learning",
    ],
    "prerequisites": [
        "Graduate standing or instructor consent",
        "Comfort with basic probability & statistics",
        "Programming experience (Python preferred)",
        "Curiosity about how minds compute",
    ],
    "resources": [
        "Free online textbook with Colab notebooks",
        "Weekly readings from primary literature",
        "Probability cheatsheet",
        "GenJAX setup guide & tutorials",
    ],
}

GRADING = [
    ("Final project", "50%"),
    ("Programming assignments (4)", "30%"),
    ("Weekly discussion posts", "12.5%"),
    ("Paper presentation", "7.5%"),
]

# Per-week curated *section* deep-links into the textbook. When a week (keyed by
# its directory number) appears here, these labelled section anchors REPLACE the
# auto-derived chapter-top tags in the schedule's Textbook column — used where one
# session spans several chapters and the lecture maps onto specific sections (the
# anchors are the built Hugo heading slugs under TEXTBOOK_BASE). Non-textbook tags
# (e.g. the GenJAX → assignments link) are preserved. Paths are relative to
# TEXTBOOK_BASE; verify the #anchors against the built chapter HTML when editing.
WEEK_TEXTBOOK_LINKS = {
    # Week 8 (Jun 19) — DECIDE → PLAN (known MDP) → LEARN (unknown MDP) → SIMULATE,
    # across intro2 chapters 20/21/22.
    8: [
        ("Decision theory", "decisions/decision-theory/"),
        ("Loss → estimator", "decisions/decision-theory/#what-loss-are-you-minimizing"),
        ("MDPs & Bellman", "decisions/mdps/"),
        ("Value iteration & γ", "decisions/mdps/#value-iteration"),
        ("Q-learning", "decisions/q-learning/"),
        ("Reward shaping", "decisions/q-learning/#reward-shaping-and-positive-cycles"),
        ("Simulation-based RL & MCTS", "decisions/q-learning/#planning-by-search-mcts"),
        ("Two-step task (MB vs MF)", "decisions/q-learning/#telling-model-free-from-model-based-the-two-step-task"),
    ],
    # Week 10 (Jul 3) — Bias-Variance + Bayesian Nonparametrics. "How complex?" →
    # three answers (ridge / grow capacity / prior over functions). Now Part VII
    # of the restructured book: complexity/{bias-variance, dpmm, gaussian-processes}.
    10: [
        ("Bias-variance dilemma", "complexity/bias-variance/"),
        ("Ridge = a Gaussian prior", "complexity/bias-variance/#ridge-regression-is-a-gaussian-prior"),
        ("Double descent", "complexity/bias-variance/#double-descent"),
        ("Discrete BNP: DP / CRP / DPMM", "complexity/dpmm/"),
        ("One object, three lenses", "complexity/dpmm/#one-object-three-lenses"),
        ("Gaussian processes", "complexity/gaussian-processes/"),
        ("GP → NNGP / NTK", "complexity/gaussian-processes/#from-gaussian-processes-to-neural-networks"),
        ("It all comes home", "complexity/gaussian-processes/#it-all-comes-home"),
    ],
}

# Week dates (SP26 calendar: Apr 17 through Jul 17, no class May 1 or May 8)
# Keys are *directory* week numbers (weekNN_ dirs); values are display dates.
# Course directories were renumbered to 12 contiguous sessions (week01..week12),
# so directory number == display week number == the dates below. (Earlier this
# map skipped a dropped "week 6" and ran to 13 — that predated the renumber.)
WEEK_DATES = {
    1: "Apr 17",
    2: "Apr 24",
    3: "May 15",
    4: "May 22",
    5: "May 29",
    6: "Jun 5",
    7: "Jun 12",
    8: "Jun 19",
    9: "Jun 26",
    10: "Jul 3",
    11: "Jul 10",
    12: "Jul 17",
}

# Display week number == directory number (1:1 after the renumber).
WEEK_DISPLAY_NUM = {n: n for n in range(1, 13)}

# Short topic labels for schedule table (kept short even if PLAN.md h1 is longer)
TOPIC_OVERRIDES = {
    1: "Introduction & Basic Bayes",
    2: "Levels of Analysis & Bayes cont'd",
    3: "Conjugate Bayes & Topic Models",
    4: "Generalization & Hierarchical Bayes",
    5: "Bayes Nets & Causal Bayes Nets",
    6: "Markov Chains & Networks",
    7: "Monte Carlo Methods",
    8: "SDT, MDPs & Reinforcement Learning",
    9: "Inverse Reinforcement Learning",
    10: "Bayesian Nonparametrics",
    11: "Deep Neural Networks",
    12: "Ethics & Adversarial ML",
}

# ---------- PLAN.md parsing ----------

WEEK_DIR_RE = re.compile(r"week(\d{2})_")


def find_week_dirs():
    dirs = []
    for d in sorted(COURSE_DIR.iterdir()):
        m = WEEK_DIR_RE.match(d.name)
        if m and d.is_dir():
            dirs.append((int(m.group(1)), d))
    return dirs


def parse_plan_section(plan_text: str, section_name: str) -> str:
    """Return the body of a ## H2 section (up to the next ## or EOF)."""
    pattern = re.compile(
        rf"^##\s+{re.escape(section_name)}\s*\n(.*?)(?=^##\s|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = pattern.search(plan_text)
    return m.group(1).strip() if m else ""


def _tag_url(label: str) -> str:
    """Map a tag label to its destination URL.

    Two textbook-tag forms are supported:
      NUMERIC   'T1 Ch 1-3' → https://.../intro/01_goals/  (first chapter in range)
                'T2 Ch 0'   → https://.../genjax/00_getting_started/
      NAME      'T3 Generalization' → resolves by stable name (order-robust;
                see build_chapter_name_map). The name is matched case- and
                separator-insensitively against the chapter slug.
      'GenJAX'  → assignments.html
      unknown   → '' (renders as plain, unlinked tag)
    """
    # NUMERIC form (legacy): 'T3 Ch 7' / 'T1 Ch 1-3' — resolved via url_map.csv
    m = re.match(r"T(\d)\s*Ch\s*(\d+)(?:-(\d+))?$", label)
    if m:
        tnum = int(m.group(1))
        first_ch = int(m.group(2))
        path = (CHAPTER_MAP or {}).get(tnum, {}).get(first_ch)
        if path:
            return f"{TEXTBOOK_BASE}/{path}/"
        return f"{TEXTBOOK_BASE}/"  # chapter not found — fall back to book home
    # NAME forms: canonical 'Bk <name>' or legacy 'T3 <name>' — both resolve
    # against the one global chapter-name map (the T-number is ignored).
    mn = re.match(r"(?:Bk|T\d)\s+(.+)$", label)
    if mn:
        path = _resolve_chapter_name(mn.group(1))
        if path:
            return f"{TEXTBOOK_BASE}/{path}/"
        return f"{TEXTBOOK_BASE}/"
    if label == "GenJAX":
        return ASSIGNMENTS_URL
    return ""


def _norm_name(s: str) -> str:
    """Canonicalize a chapter name for matching: lowercase, non-alnum → '_'."""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _resolve_chapter_name(name: str):
    """Find a chapter's 'part/slug' path from a stable name, separator- and
    case-insensitively: 'Generalization' / 'Hierarchical Bayes' / 'q learning'
    all resolve. Names are matched against the global chapter-name map."""
    target = _norm_name(name)
    names = CHAPTER_NAME_MAP or {}
    if target in names:
        return names[target]
    # Restructure renames: keep historical stable names (old slugs minus the
    # NN_ prefix) resolving to the renamed chapters.
    LEGACY_NAMES = {
        "markov_chain_monte_carlo": "mcmc",
        "markov_decision_processes": "mdps",
        "statistical_decision_theory": "decision_theory",
        "continuous_bnp": "gaussian_processes",
        "inverse_rl_goal_inference": "inverse_rl",
        "pomdps_belief_inference": "pomdps_belief",
        "prob_count": "probability_as_counting",
        "conditional": "conditional_probability",
        "bayes": "bayes_rule",
    }
    alias = LEGACY_NAMES.get(target)
    if alias and alias in names:
        return names[alias]
    return None


def _labels_from_section(text: str) -> list:
    """Extract textbook-chapter tag labels from one PLAN section, supporting both
    the NUMERIC form (``T3 Ch 7``, ``T1 Ch 1-3``) and the order-robust NAME form
    (``T3: generalization``). Labels are returned in PLAN source order.

    The name form is written ``T<tut>: <name-or-csv>`` and yields a label
    ``T<tut> <Title Case Name>`` that renders on the card and resolves via the
    chapter name map (so reordering chapters never touches the PLAN). The numeric
    form is matched only when NOT immediately followed by ``:`` so ``T3: foo`` is
    never mis-read as a numeric tag."""
    # One alternation scanned left-to-right keeps tags in PLAN line order
    # regardless of which form each tag uses. `Bk: <name>` is the canonical
    # post-restructure form; `T<d>: <name>` and `T<d> Ch <n>` are legacy.
    BK = r"Bk\s*:\s*(?P<bkname>[A-Za-z][\w ,&\-]*)"
    NAME = r"T(?P<nt>\d)\s*:\s*(?P<name>[A-Za-z][\w ,&\-]*)"
    NUM = r"T(?P<ct>\d)\s*Ch\s*(?P<ch>[\d\-]+)\b"
    labels = []
    for m in re.finditer(rf"{BK}|{NAME}|{NUM}", text):
        if m.group("bkname") is not None:
            for raw in m.group("bkname").split(","):
                name = raw.strip()
                if name:
                    labels.append(f"Bk {name.replace('_', ' ').title()}")
        elif m.group("name") is not None:
            for raw in m.group("name").split(","):
                name = raw.strip()
                if name:
                    labels.append(f"T{m.group('nt')} {name.replace('_', ' ').title()}")
        else:
            labels.append(f"T{m.group('ct')} Ch {m.group('ch')}")
    return labels


def extract_tags_from_plan(plan_text: str) -> list:
    """Pull short tags for the schedule: textbook shorthand + GenJAX markers.
    Returns list of {label, url} dicts (url may be empty)."""
    labels = list(_labels_from_section(parse_plan_section(plan_text, "Textbook Chapters")))
    # The GenJAX-Integration section may name specific textbook chapters (kept as
    # links); the bare "GenJAX" placeholder card is no longer shown on the schedule.
    gj = parse_plan_section(plan_text, "GenJAX Integration")
    if gj and gj.strip().lower() not in ("none this week.", "none this week", "none."):
        labels.extend(_labels_from_section(gj))
    seen = set()
    out = []
    for label in labels:
        if label in seen:
            continue
        seen.add(label)
        out.append({"label": label, "url": _tag_url(label)})
    return out


def sync_slide_pdf(wk_num: int, wk_dir: Path) -> str:
    """If a rendered slide PDF exists under slides/sp26/weekNN.pdf, copy it into
    docs/slides/ and return the relative URL. Otherwise return ''."""
    src = wk_dir / "slides" / "sp26" / f"week{wk_num:02d}.pdf"
    if not src.is_file():
        return ""
    SLIDES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    dst = SLIDES_OUT_DIR / f"week{wk_num:02d}.pdf"
    # Only re-copy if source is newer
    if not dst.is_file() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    return f"slides/week{wk_num:02d}.pdf"


def sync_slide_html(wk_num: int, wk_dir: Path) -> str:
    """Locate a standalone .html deck for this week and publish it under
    docs/slides/weekNN.html. Supports two sources in order:
      1. course/weekNN/slides/sp26/weekNN.html  (legacy, self-contained)
      2. course/weekNN/weekN-slides.html + weekN-slides_files/  (Quarto output)
    For the Quarto case, the entire companion _files dir is copied alongside.
    Returns the relative URL or '' if neither source exists."""
    legacy = wk_dir / "slides" / "sp26" / f"week{wk_num:02d}.html"
    if legacy.is_file():
        SLIDES_OUT_DIR.mkdir(parents=True, exist_ok=True)
        dst = SLIDES_OUT_DIR / f"week{wk_num:02d}.html"
        if not dst.is_file() or legacy.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(legacy, dst)
        return f"slides/week{wk_num:02d}.html"

    # Quarto-rendered case: look for any .qmd and its companion .html.
    for qmd in wk_dir.glob("week*-slides.qmd"):
        html_src = qmd.with_suffix(".html")
        files_src = qmd.parent / f"{qmd.stem}_files"
        if not html_src.is_file():
            continue
        SLIDES_OUT_DIR.mkdir(parents=True, exist_ok=True)
        dst_html = SLIDES_OUT_DIR / f"week{wk_num:02d}.html"
        if not dst_html.is_file() or html_src.stat().st_mtime > dst_html.stat().st_mtime:
            # Rewrite the _files/ references from the qmd-stem path to the
            # published weekNN_files path, so the copied HTML finds its assets.
            content = html_src.read_text(encoding="utf-8")
            content = content.replace(
                f"{qmd.stem}_files/", f"week{wk_num:02d}_files/"
            )
            # Also rewrite ../../sds-reveal/ refs → ./sds-reveal/ (same trick
            # as preview_deck.sh) so the yellow-frame PNGs resolve.
            content = content.replace("../../sds-reveal/", "sds-reveal/")
            dst_html.write_text(content, encoding="utf-8")
        # Copy the _files tree, and also copy sds-reveal/ next to it.
        if files_src.is_dir():
            dst_files = SLIDES_OUT_DIR / f"week{wk_num:02d}_files"
            if dst_files.exists():
                shutil.rmtree(dst_files)
            shutil.copytree(files_src, dst_files)
            # Copy sds-reveal frame + wordmark into the theme dir so
            # background-image:url(sds_frame.png) in the theme CSS resolves.
            theme_dir = dst_files / "libs" / "revealjs" / "dist" / "theme"
            if theme_dir.is_dir():
                sds_root = REPO_ROOT / "sds-reveal"
                for asset in ("sds_frame.png", "sds_wordmark.png"):
                    a = sds_root / asset
                    if a.is_file():
                        shutil.copy2(a, theme_dir / asset)
        # Also copy sds-reveal dir next to the deck so any ./sds-reveal/... refs
        # in the .qmd (like per-slide background-image attrs) resolve.
        sds_root = REPO_ROOT / "sds-reveal"
        if sds_root.is_dir():
            dst_sds = SLIDES_OUT_DIR / "sds-reveal"
            if dst_sds.exists():
                shutil.rmtree(dst_sds)
            shutil.copytree(sds_root, dst_sds)
        # Copy images referenced from the qmd dir (e.g., binomial_pmf.png).
        # MERGE into the shared docs/slides/images/ dir — do NOT rmtree it, or
        # each week clobbers the previous weeks' figures (all decks share this
        # one images dir). dirs_exist_ok overwrites same-named files in place.
        images_src = qmd.parent / "images"
        if images_src.is_dir():
            dst_images = SLIDES_OUT_DIR / "images"
            dst_images.mkdir(parents=True, exist_ok=True)
            shutil.copytree(images_src, dst_images, dirs_exist_ok=True)
        # Copy any interactive widgets the deck embeds via a relative iframe
        # (e.g., <iframe src="widgets/bayes_ball.html">). The iframe path is
        # resolved relative to docs/slides/weekNN.html, so the widgets dir must
        # land at docs/slides/widgets/ — otherwise GitHub Pages 404s the embed.
        widgets_src = qmd.parent / "widgets"
        if widgets_src.is_dir():
            dst_widgets = SLIDES_OUT_DIR / "widgets"
            if dst_widgets.exists():
                shutil.rmtree(dst_widgets)
            shutil.copytree(widgets_src, dst_widgets)
        return f"slides/week{wk_num:02d}.html"

    return ""


def build_schedule():
    rows = []
    weeks = dict(find_week_dirs())
    for dir_num in range(1, 14):
        if dir_num not in WEEK_DATES:
            continue  # skip dropped weeks (e.g., 6)
        d = weeks.get(dir_num)
        if d is None:
            continue
        plan = (d / "PLAN.md").read_text(encoding="utf-8")
        topic = TOPIC_OVERRIDES.get(dir_num)
        tags = extract_tags_from_plan(plan)
        section_links = WEEK_TEXTBOOK_LINKS.get(dir_num)
        if section_links:
            # Replace auto-derived chapter-top tags with curated section deep-links,
            # keeping any non-textbook tags (e.g. the GenJAX → assignments link).
            kept = [t for t in tags if TEXTBOOK_BASE not in (t.get("url") or "")]
            curated = [{"label": lbl, "url": f"{TEXTBOOK_BASE}/{path}"} for lbl, path in section_links]
            tags = curated + kept
        slide_url = sync_slide_pdf(dir_num, d)
        slide_html_url = sync_slide_html(dir_num, d)
        rows.append({
            "kind": "week",
            "week": WEEK_DISPLAY_NUM[dir_num],
            "date": WEEK_DATES[dir_num],
            "topic": topic,
            "tags": tags,
            "slide_url": slide_url,
            "slide_html_url": slide_html_url,
        })
        # Insert "no class" breaks after Week 2 (May 1 & May 8)
        if dir_num == 2:
            rows.append({
                "kind": "break",
                "date": "May 1",
                "label": "No class",
            })
            rows.append({
                "kind": "break",
                "date": "May 8",
                "label": "No class (holiday)",
            })
    return rows


# ---------- Markdown -> HTML helpers ----------

def md_to_html(md_text: str) -> str:
    # `attr_list` lets markdown headings carry an explicit id (e.g.
    # `### Clusters {#clusters}`) so in-page anchor links are stable.
    return markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists", "tables", "attr_list"],
        output_format="html5",
    )


def render_syllabus_content(md_text: str) -> str:
    """Convert syllabus markdown to HTML, stripping the H1 (we render it as page header).
    Also upgrade plain <table> to class=data-table for styling."""
    # Strip the first H1 line
    lines = md_text.split("\n")
    out = []
    stripped_h1 = False
    for line in lines:
        if not stripped_h1 and line.startswith("# "):
            stripped_h1 = True
            continue
        out.append(line)
    html = md_to_html("\n".join(out))
    html = html.replace("<table>", '<table class="data-table">')
    return html


def render_assignments_content(md_text: str) -> str:
    """Convert assignments README markdown to HTML, stripping the H1."""
    lines = md_text.split("\n")
    out = []
    stripped_h1 = False
    for line in lines:
        if not stripped_h1 and line.startswith("# "):
            stripped_h1 = True
            continue
        out.append(line)
    html = md_to_html("\n".join(out))
    html = html.replace("<table>", '<table class="data-table">')
    return html


# ---------- Jinja env ----------

def make_env():
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


# ---------- Page renderers ----------

def render_landing(env):
    schedule = build_schedule()
    template = env.get_template("landing.html")
    html = template.render(
        page_key="landing",
        rel_root="",
        highlights=HIGHLIGHTS,
        schedule=schedule,
        info=INFO_CARDS,
        grading=GRADING,
    )
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"  wrote index.html ({len(html):,} bytes)")


def render_syllabus(env):
    src = (COURSE_DIR / "syllabus" / "SP26_syllabus.md").read_text(encoding="utf-8")
    content = render_syllabus_content(src)
    template = env.get_template("page.html")
    html = template.render(
        page_key="syllabus",
        rel_root="",
        page_title="Syllabus",
        eyebrow="Spring 2026",
        page_sub="Human and Machine Learning — Chiba Institute of Technology, School of Design & Science",
        content=content,
    )
    (DOCS_DIR / "syllabus.html").write_text(html, encoding="utf-8")
    print(f"  wrote syllabus.html ({len(html):,} bytes)")


def _stage_reading_pdf(pdf_name: str) -> str:
    """Copy a PDF from resources/readings/ into docs/readings/pdfs/ and return
    the URL path relative to docs/readings.html. Returns '' if the source
    doesn't exist."""
    src = READINGS_PDF_SRC / pdf_name
    if not src.is_file():
        return ""
    dst_dir = READINGS_OUT_DIR / "pdfs"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / pdf_name
    if not dst.is_file() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    # URL relative to docs/readings.html
    return f"readings/pdfs/{pdf_name}"


def stage_assignment_stencils() -> None:
    """Copy each assignment's stencil files from course/assignments/<slug>/ into
    docs/assignments/<slug>/ so they publish to hml.chibatech.dev/assignments/.
    Skips (with a warning) any source file that doesn't exist."""
    for slug, filenames in ASSIGNMENT_STENCILS.items():
        src_dir = ASSIGNMENTS_SRC / slug
        dst_dir = ASSIGNMENTS_OUT_DIR / slug
        for name in filenames:
            src = src_dir / name
            if not src.is_file():
                print(f"  WARNING: assignment stencil not found: {src}")
                continue
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst = dst_dir / name
            if not dst.is_file() or src.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(src, dst)
                print(f"  staged assignments/{slug}/{name}")


def _resolve_reading_link(entry: dict) -> str:
    """Prefer local PDF, fall back to external URL, empty if neither."""
    pdf = entry.get("pdf")
    if pdf:
        staged = _stage_reading_pdf(pdf)
        if staged:
            return staged
    return entry.get("url") or ""


def _prepare_readings(entries):
    """Attach a link_href to each entry (possibly empty)."""
    out = []
    for e in entries or []:
        item = dict(e)
        item["link_href"] = _resolve_reading_link(e)
        out.append(item)
    return out


def render_game_plan(env):
    src_path = DOCS_DIR / "reading-game-plan.md"
    if not src_path.is_file():
        return
    src = src_path.read_text(encoding="utf-8")
    content = render_assignments_content(src)  # strips H1, turns markdown into HTML
    template = env.get_template("page.html")
    html = template.render(
        page_key="readings",
        rel_root="",
        page_title="Readings & Discussion Game Plan",
        eyebrow="Spring 2026",
        page_sub="How readings, Slack signups, and discussion posts fit together.",
        content=content,
    )
    (DOCS_DIR / "reading-game-plan.html").write_text(html, encoding="utf-8")
    print(f"  wrote reading-game-plan.html ({len(html):,} bytes)")


def render_readings(env):
    src = (COURSE_DIR / "readings_map.yml").read_text(encoding="utf-8")
    data = yaml.safe_load(src)
    weeks = []
    for w in data.get("weeks", []):
        weeks.append({
            "number": w["number"],
            "date": w["date"],
            "theme": w["theme"],
            "required": _prepare_readings(w.get("required")),
            "optional": _prepare_readings(w.get("optional")),
            "candidates": _prepare_readings(w.get("presentation_candidates")),
            "presenter": w.get("presenter"),
            "presented": w.get("presented"),
        })
    template = env.get_template("readings.html")
    html = template.render(
        page_key="readings",
        rel_root="",
        page_title="Readings",
        eyebrow="Spring 2026",
        page_sub="Weekly readings, presentation candidates, and the Slack rhythm for discussion posts.",
        weeks=weeks,
    )
    (DOCS_DIR / "readings.html").write_text(html, encoding="utf-8")
    print(f"  wrote readings.html ({len(html):,} bytes, {len(weeks)} weeks)")


def render_assignments(env):
    stage_assignment_stencils()
    src = (COURSE_DIR / "assignments" / "README.md").read_text(encoding="utf-8")
    content = render_assignments_content(src)
    template = env.get_template("page.html")
    html = template.render(
        page_key="assignments",
        rel_root="",
        page_title="Assignments",
        eyebrow="Spring 2026",
        page_sub="Four programming assignments in GenJAX, spread across the semester.",
        content=content,
    )
    (DOCS_DIR / "assignments.html").write_text(html, encoding="utf-8")
    print(f"  wrote assignments.html ({len(html):,} bytes)")


def render_project(env):
    src_path = DOCS_DIR / "project.md"
    if not src_path.is_file():
        return
    src = src_path.read_text(encoding="utf-8")
    content = render_assignments_content(src)  # strips H1, turns markdown into HTML
    template = env.get_template("page.html")
    html = template.render(
        page_key="project",
        rel_root="",
        page_title="Final Project",
        eyebrow="Spring 2026",
        page_sub="Proposal, in-class presentation, and final paper — the capstone of the course.",
        content=content,
    )
    (DOCS_DIR / "project.html").write_text(html, encoding="utf-8")
    print(f"  wrote project.html ({len(html):,} bytes)")


def render_presentation_guidelines(env):
    src_path = DOCS_DIR / "presentation-guidelines.md"
    if not src_path.is_file():
        return
    src = src_path.read_text(encoding="utf-8")
    content = render_assignments_content(src)  # strips H1, turns markdown into HTML
    template = env.get_template("page.html")
    html = template.render(
        page_key="game-plan",
        rel_root="",
        page_title="Paper presentation guidelines",
        eyebrow="Spring 2026",
        page_sub="How to prepare your 15-minute paper presentation.",
        content=content,
    )
    (DOCS_DIR / "presentation-guidelines.html").write_text(html, encoding="utf-8")
    print(f"  wrote presentation-guidelines.html ({len(html):,} bytes)")


def main():
    global CHAPTER_MAP, CHAPTER_NAME_MAP
    if not TEMPLATES_DIR.is_dir():
        print(f"ERROR: templates dir not found: {TEMPLATES_DIR}", file=sys.stderr)
        sys.exit(1)
    CHAPTER_MAP = build_chapter_map()
    CHAPTER_NAME_MAP = build_chapter_name_map()
    env = make_env()
    print("Building course website...")
    render_landing(env)
    render_syllabus(env)
    render_assignments(env)
    render_project(env)
    render_readings(env)
    render_game_plan(env)
    render_presentation_guidelines(env)
    print("Done.")


if __name__ == "__main__":
    main()
