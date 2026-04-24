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

TEXTBOOK_BASE = "https://josephausterweil.github.io/probintro"
TEXTBOOK_CONTENT = REPO_ROOT / "textbook" / "content"
# Tutorial shorthand → textbook URL fragment
TUTORIAL_PATH = {1: "intro", 2: "genjax", 3: "intro2"}
ASSIGNMENTS_URL = "assignments.html"


def build_chapter_map() -> dict:
    """Scan textbook/content/{tutorial}/ for numbered chapters (NN_slug.md).
    Returns {tutorial_number: {chapter_number: slug_without_ext}}."""
    CH_RE = re.compile(r"^(\d{2})_(.+)\.md$")
    out = {}
    for tnum, sub in TUTORIAL_PATH.items():
        tut_dir = TEXTBOOK_CONTENT / sub
        chapters = {}
        if tut_dir.is_dir():
            for f in tut_dir.iterdir():
                m = CH_RE.match(f.name)
                if m:
                    chapters[int(m.group(1))] = f.stem  # e.g. '01_goals'
        out[tnum] = chapters
    return out


CHAPTER_MAP = None  # populated lazily in main()

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

# Week dates (SP26 calendar: Apr 17 through Jul 17, no class May 1 or May 8)
# Keys are *directory* week numbers (weekNN_ dirs); values are display dates.
# Week 6 (Causal Bayes Nets) is dropped from the schedule.
WEEK_DATES = {
    1: "Apr 17",
    2: "Apr 24",
    3: "May 15",
    4: "May 22",
    5: "May 29",
    # 6 dropped (Causal Bayes Nets eliminated)
    7: "Jun 5",
    8: "Jun 12",
    9: "Jun 19",
    10: "Jun 26",
    11: "Jul 3",
    12: "Jul 10",
    13: "Jul 17",
}

# Display week number (1-12) for each directory week number
WEEK_DISPLAY_NUM = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
    # 6 skipped
    7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12,
}

# Short topic labels for schedule table (kept short even if PLAN.md h1 is longer)
TOPIC_OVERRIDES = {
    1: "Introduction & Basic Bayes",
    2: "Basic Bayes cont'd",
    3: "Conjugate Bayes & Topic Models",
    4: "Generalization & Hierarchical Bayes",
    5: "Hierarchical Bayes & Bayes Nets",
    # 6 dropped
    7: "Markov Chains & Networks",
    8: "Monte Carlo Methods",
    9: "SDT, MDPs & Reinforcement Learning",
    10: "Inverse Reinforcement Learning",
    11: "Bayesian Nonparametrics",
    12: "Deep Neural Networks",
    13: "Ethics & Adversarial ML",
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

    Examples:
      'T1 Ch 1-3' → https://.../intro/01_goals/  (first chapter in range)
      'T2 Ch 0'   → https://.../genjax/00_getting_started/
      'GenJAX'    → assignments.html
      unknown     → '' (renders as plain, unlinked tag)
    """
    m = re.match(r"T(\d)\s*Ch\s*(\d+)(?:-(\d+))?", label)
    if m:
        tnum = int(m.group(1))
        first_ch = int(m.group(2))
        tut = TUTORIAL_PATH.get(tnum)
        chapters = (CHAPTER_MAP or {}).get(tnum, {})
        slug = chapters.get(first_ch)
        if tut and slug:
            return f"{TEXTBOOK_BASE}/{tut}/{slug}/"
        if tut:  # chapter not found — fall back to tutorial index
            return f"{TEXTBOOK_BASE}/{tut}/"
    if label == "GenJAX":
        return ASSIGNMENTS_URL
    return ""


def extract_tags_from_plan(plan_text: str) -> list:
    """Pull short tags for the schedule: textbook shorthand + GenJAX markers.
    Returns list of {label, url} dicts (url may be empty)."""
    labels = []
    tb = parse_plan_section(plan_text, "Textbook Chapters")
    for m in re.finditer(r"\bT(\d)\s*Ch\s*([\d\-]+)\b", tb):
        labels.append(f"T{m.group(1)} Ch {m.group(2)}")
    gj = parse_plan_section(plan_text, "GenJAX Integration")
    if gj and gj.strip().lower() not in ("none this week.", "none this week", "none."):
        gj_labels = []
        for m in re.finditer(r"\bT(\d)\s*Ch\s*([\d\-]+)\b", gj):
            gj_labels.append(f"T{m.group(1)} Ch {m.group(2)}")
        if gj_labels:
            labels.extend(gj_labels)
        else:
            labels.append("GenJAX")
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
        images_src = qmd.parent / "images"
        if images_src.is_dir():
            dst_images = SLIDES_OUT_DIR / "images"
            if dst_images.exists():
                shutil.rmtree(dst_images)
            shutil.copytree(images_src, dst_images)
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
        slide_url = sync_slide_pdf(dir_num, d)
        # Only publish the HTML deck if a PDF is also present — that's our
        # signal that the deck is finalized for that week. Keeps WIP decks
        # out of the published schedule.
        slide_html_url = sync_slide_html(dir_num, d) if slide_url else ""
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
    return markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists", "tables"],
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
    global CHAPTER_MAP
    if not TEMPLATES_DIR.is_dir():
        print(f"ERROR: templates dir not found: {TEMPLATES_DIR}", file=sys.stderr)
        sys.exit(1)
    CHAPTER_MAP = build_chapter_map()
    env = make_env()
    print("Building course website...")
    render_landing(env)
    render_syllabus(env)
    render_assignments(env)
    render_readings(env)
    render_game_plan(env)
    render_presentation_guidelines(env)
    print("Done.")


if __name__ == "__main__":
    main()
