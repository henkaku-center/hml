# Course Website

This directory is the public-facing course website, served by GitHub Pages from `/docs`.

## Files in this directory

**Generated (do not hand-edit — they get overwritten by the next build):**

- `index.html` — landing page (schedule driven from `course/weekNN_*/PLAN.md`)
- `syllabus.html` — generated from `course/syllabus/SP26_syllabus.md`
- `assignments.html` — generated from `course/assignments/README.md`

**Hand-maintained:**

- `_style.css` — all styling. Shared across pages.
- `_build.py` — the generator script.
- `_templates/` — Jinja2 templates (`base.html`, `landing.html`, `page.html`). Not served by GitHub Pages.
- `assets/` — images (Chiba Tech SDS logos).
- `.nojekyll` — empty file that disables Jekyll on GitHub Pages (we serve plain static files).

## Build workflow

```bash
# From the repo root:
python docs/_build.py
```

The generator reads:
- Every `course/weekNN_*/PLAN.md` for schedule rows (pulls textbook-chapter tags from the "Textbook Chapters" and "GenJAX Integration" sections).
- `course/syllabus/SP26_syllabus.md` for the syllabus page.
- `course/assignments/README.md` for the assignments page.

Edit those source files, rerun the build, commit the regenerated HTML. GitHub Pages picks it up within ~60 seconds.

## Dependencies

- Python 3.10+
- `jinja2`
- `markdown`

Both already available in the repo's environment.

## Extending

To add a new page type (e.g., per-week detail pages for Phase 2):

1. Add a template under `_templates/`.
2. Add a renderer function in `_build.py` following the pattern of `render_syllabus()`.
3. Call it from `main()`.
4. Link to it from `base.html`'s `topnav` block or wherever appropriate.
