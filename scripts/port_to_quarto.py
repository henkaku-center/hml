#!/usr/bin/env python3
"""Port a Week N build_slides_weekN.py deck into a Quarto weekN-slides.qmd.

Strategy: mock out SDSDeck with a recorder that captures every slide-helper
call (title_slide, agenda_slide, section_break, content_slide, build_slides,
content_image_slide, break_slide). Execute the build script so Python
evaluates all the constants for us. Then walk the recorded calls and emit
a .qmd that matches the weekN-slides.qmd convention used in Week 3.

Usage:
    python3 scripts/port_to_quarto.py \\
        course/week02_basic_bayes_cont/build_slides_week2.py \\
        course/week02_basic_bayes_cont/week2-slides.qmd

Theme reference: ../../sds-reveal/sds.scss (relative to the weekN dir).
"""

import argparse
import importlib.util
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace


# --- Color-name mapping: RGBColor(r,g,b) → inline CSS class in the .qmd.
# These mirror the theme color slots declared in sds.scss (.dim, .accent, .yellow, etc.).
# Detected from deck.DIM / deck.ACCENT / deck.YELLOW / deck.RED / deck.GREEN / deck.ORANGE.
_COLOR_CLASSES = {
    "DIM": "dim",
    "ACCENT": "accent",
    "YELLOW": "yellow",
    "RED": "red",
    "GREEN": "green",
    "ORANGE": "orange",
    "TEXT_WHITE": None,      # default
    "TEXT_DIM": "dim",
    "TEXT_ACCENT": "accent",
    "TEXT_YELLOW": "yellow",
    "TEXT_RED": "red",
    "TEXT_GREEN": "green",
    "TEXT_ORANGE": "orange",
    "SDS_YELLOW": "yellow",
}


class Recorder:
    """Drop-in replacement for SDSDeck that records every call verbatim."""

    # Mirror the theme-color attributes so build scripts that reference
    # `deck.ACCENT` (etc.) resolve to sentinels we can map back to CSS classes.
    DIM = object()
    ACCENT = object()
    YELLOW = object()
    RED = object()
    GREEN = object()
    ORANGE = object()
    TEXT_WHITE = object()
    TEXT_DIM = DIM
    TEXT_ACCENT = ACCENT
    TEXT_YELLOW = YELLOW
    TEXT_RED = RED
    TEXT_GREEN = GREEN
    TEXT_ORANGE = ORANGE
    SDS_YELLOW = YELLOW

    _COLOR_NAME = {
        DIM: "dim",
        ACCENT: "accent",
        YELLOW: "yellow",
        RED: "red",
        GREEN: "green",
        ORANGE: "orange",
        TEXT_WHITE: None,
    }

    def __init__(self, *args, **kwargs):
        self.course_label = kwargs.get("course_label", "")
        self.calls = []  # list of (method_name, args, kwargs)

    def _record(self, method):
        def fn(*args, **kwargs):
            self.calls.append((method, args, kwargs))
        return fn

    def __getattr__(self, name):
        # Any unseen attribute access yields a recorder function.
        if name in {"title_slide", "agenda_slide", "section_break",
                    "content_slide", "build_slides", "content_image_slide",
                    "break_slide"}:
            return self._record(name)
        if name in {"save", "export_notes_md", "render_previews"}:
            return lambda *a, **kw: None
        raise AttributeError(name)


# ---------- Body-block serialization ----------

def _color_class(color_obj):
    return Recorder._COLOR_NAME.get(color_obj)


def _opts_wrap(text: str, opts: dict) -> str:
    """Wrap `text` with inline CSS spans reflecting opts (bold/italic/color/size).

    Markdown's bold/italic markers MUST be adjacent to the text they wrap —
    leading/trailing whitespace breaks parsing and the asterisks render
    literally. So we peel off outer whitespace, apply formatting, restore.
    """
    if not text:
        return ""
    bold = opts.get("bold", False)
    italic = opts.get("italic", False)
    color = opts.get("color")
    # Peel outer whitespace so markdown markers can hug the content.
    lead = len(text) - len(text.lstrip())
    trail = len(text) - len(text.rstrip())
    lead_ws = text[:lead]
    trail_ws = text[len(text) - trail:] if trail else ""
    core = text[lead:len(text) - trail] if trail else text[lead:]
    out = core
    if bold:
        out = f"**{out}**"
    if italic:
        out = f"*{out}*"
    cls = _color_class(color) if color is not None else None
    if cls:
        out = f"[{out}]{{.{cls}}}"
    # Restore whitespace OUTSIDE the formatting span. For leading whitespace
    # that has meaning (indentation in ASCII tables), emit as non-breaking
    # spaces so markdown doesn't collapse them.
    if lead_ws:
        out = lead_ws.replace(" ", "&nbsp;") + out
    if trail_ws:
        out = out + trail_ws.replace(" ", "&nbsp;")
    return out


def _body_to_md(body) -> str:
    """Convert a body list-of-(text, opts) into markdown lines."""
    lines = []
    for item in body:
        if isinstance(item, str):
            text, opts = item, {}
        else:
            text, opts = item
        if not text:
            lines.append("")  # blank spacer
            continue
        lines.append(_opts_wrap(text, opts))
    return "\n\n".join(lines)


# ---------- Speaker-notes serialization ----------

def _notes_block(notes) -> str:
    if notes is None:
        return ""
    if isinstance(notes, list):
        # build_slides takes a list of notes, one per step. We emit them on
        # each emitted slide separately, so this path is handled by the caller.
        return ""
    text = notes.strip()
    if not text:
        return ""
    return "\n::: {.notes}\n" + text + "\n:::\n"


# ---------- Emitters, one per helper ----------

def emit_title_slide(args, kwargs, out, yaml_ctx):
    title = kwargs.get("title", args[0] if args else "")
    subtitle = kwargs.get("subtitle", "")
    authors = kwargs.get("authors", "")
    notes = kwargs.get("notes", "")
    yaml_ctx["title"] = title
    yaml_ctx["subtitle"] = subtitle
    yaml_ctx["author"] = authors
    # Title slide is emitted by the YAML frontmatter. Notes for the title
    # slide have to go on the first content section after the frontmatter
    # since Quarto doesn't expose notes on the auto-generated title slide.
    # Stash them; the driver will prepend.
    if notes:
        yaml_ctx["_title_notes"] = notes.strip()


def emit_agenda_slide(args, kwargs, out, yaml_ctx):
    items = args[0] if args else kwargs.get("items", [])
    highlight = kwargs.get("highlight")
    notes = kwargs.get("notes", "")
    out.append("## Agenda {.agenda}\n")
    for label, time in items:
        if label == highlight:
            out.append(f"- [{label}]{{.highlight}} [{time}]{{.time}}")
        else:
            out.append(f"- {label} [{time}]{{.time}}")
    out.append("")
    if notes:
        out.append(_notes_block(notes))


def emit_section_break(args, kwargs, out, yaml_ctx):
    name = kwargs.get("segment_name", args[0] if args else "")
    notes = kwargs.get("notes", "")
    frame = yaml_ctx.get("_frame_path", "")
    bg = f' background-image="{frame}" background-size="cover"' if frame else ""
    out.append(f"## {name} {{.section-break{bg}}}\n")
    if notes:
        out.append(_notes_block(notes))


def emit_content_slide(args, kwargs, out, yaml_ctx):
    title = kwargs.get("title", "")
    body = kwargs.get("body", [])
    notes = kwargs.get("notes", "")
    out.append(f"## {title}\n")
    out.append(_body_to_md(body) + "\n")
    if notes:
        out.append(_notes_block(notes))


def emit_build_slides(args, kwargs, out, yaml_ctx):
    title = kwargs.get("title", "")
    steps = kwargs.get("steps", [])
    notes = kwargs.get("notes")
    # Each step accumulates — slide N shows steps[0] + ... + steps[N].
    # Emit one Quarto slide per step. Notes can be a str (applies to last) or
    # a list with one entry per step.
    if isinstance(notes, str) or notes is None:
        notes_list = [None] * (len(steps) - 1) + [notes]
    else:
        notes_list = list(notes) + [None] * (len(steps) - len(notes))

    accumulated = []
    for idx, (step, step_notes) in enumerate(zip(steps, notes_list)):
        accumulated = accumulated + list(step)
        out.append(f"## {title}" + (f" ({idx+1}/{len(steps)})" if idx > 0 else "") + "\n")
        out.append(_body_to_md(accumulated) + "\n")
        if step_notes:
            out.append(_notes_block(step_notes))


def emit_content_image_slide(args, kwargs, out, yaml_ctx):
    title = kwargs.get("title", "")
    image_path = kwargs.get("image_path", "")
    caption = kwargs.get("caption")
    notes = kwargs.get("notes", "")
    # Resolve image path relative to the weekN directory. The .qmd lives in
    # the same dir as the build script, so paths already work as-is.
    img_rel = Path(str(image_path)).name if Path(str(image_path)).is_absolute() else str(image_path)
    # If image_path is a Path object resolving under images/, keep the
    # relative "images/foo.png" so the .qmd can find it.
    img_rel_to_qmd = _rel_image_path(str(image_path))
    out.append(f"## {title}\n")
    out.append(f"![]({img_rel_to_qmd}){{fig-align=\"center\" width=\"75%\"}}\n")
    if caption:
        out.append(_body_to_md(caption) + "\n")
    if notes:
        out.append(_notes_block(notes))


def emit_break_slide(args, kwargs, out, yaml_ctx):
    text = kwargs.get("text", args[0] if args else "Break")
    notes = kwargs.get("notes", "")
    frame = yaml_ctx.get("_frame_path", "")
    bg = f' background-image="{frame}" background-size="cover"' if frame else ""
    out.append(f"## {text} {{.section-break{bg}}}\n")
    if notes:
        out.append(_notes_block(notes))


def _rel_image_path(image_path: str) -> str:
    """Return a path from the .qmd directory to the image."""
    p = Path(image_path)
    # Heuristic: if it contains 'images/', keep from there down.
    parts = p.parts
    for i, part in enumerate(parts):
        if part == "images":
            return "/".join(parts[i:])
    return p.name


EMITTERS = {
    "title_slide": emit_title_slide,
    "agenda_slide": emit_agenda_slide,
    "section_break": emit_section_break,
    "content_slide": emit_content_slide,
    "build_slides": emit_build_slides,
    "content_image_slide": emit_content_image_slide,
    "break_slide": emit_break_slide,
}


# ---------- Driver ----------

def port(build_script: Path, out_qmd: Path, theme_rel: str):
    build_script = build_script.resolve()
    out_qmd = out_qmd.resolve()

    # Inject Recorder as sds_slides.SDSDeck in a throwaway module registry.
    class FakeSDS:
        SDSDeck = Recorder

    sys.modules["sds_slides"] = FakeSDS

    # Make the weekN directory importable so any relative imports (e.g. its
    # own sds_slides) resolve to our mock first, not the real one.
    sys.path.insert(0, str(build_script.parent))

    # Capture the deck instance by patching Recorder's __init__ so we retain
    # a reference to the last-constructed recorder.
    instances = []
    orig_init = Recorder.__init__
    def capture_init(self, *a, **kw):
        orig_init(self, *a, **kw)
        instances.append(self)
    Recorder.__init__ = capture_init

    # Stop build scripts that parse CLI args from choking on our translator's argv.
    saved_argv = sys.argv
    sys.argv = [str(build_script)]
    try:
        runpy.run_path(str(build_script), run_name="__main__")
    finally:
        sys.argv = saved_argv
        Recorder.__init__ = orig_init

    if not instances:
        raise RuntimeError("Build script ran but never constructed an SDSDeck")
    deck = instances[-1]

    # Emit the .qmd.
    # Theme PNG paths, derived from theme_rel (which points at sds.scss).
    theme_dir = str(Path(theme_rel).parent)
    frame_path = f"{theme_dir}/sds_frame.png"
    yaml_ctx = {"_frame_path": frame_path}
    body_lines = []
    for method, args, kwargs in deck.calls:
        fn = EMITTERS.get(method)
        if fn is None:
            body_lines.append(f"<!-- unhandled: deck.{method}(...) -->")
            continue
        fn(args, kwargs, body_lines, yaml_ctx)

    # If title_slide left notes, prepend them before the first ## after the title.
    title_notes = yaml_ctx.pop("_title_notes", None)
    if title_notes:
        # Drop them into the first slide that comes after the title.
        body_lines.insert(0, _notes_block(title_notes))

    title = yaml_ctx.get("title", f"{build_script.stem}")
    subtitle = yaml_ctx.get("subtitle", "")
    author = yaml_ctx.get("author", "")

    yaml = [
        "---",
        f'title: "{title}"',
    ]
    if subtitle:
        yaml.append(f'subtitle: "{subtitle}"')
    if author:
        yaml.append(f'author: "{author}"')
    yaml += [
        "title-slide-attributes:",
        f'  data-background-image: "{frame_path}"',
        '  data-background-size: "cover"',
        "format:",
        "  revealjs:",
        f"    theme: [dark, {theme_rel}]",
        "  pptx: default",
        "---",
        "",
    ]

    out_qmd.write_text("\n".join(yaml) + "\n".join(body_lines) + "\n")
    print(f"Wrote {out_qmd}")
    print(f"Total slides recorded: {sum(1 for m, _, _ in deck.calls if m != 'title_slide')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build_script", type=Path,
                    help="Path to build_slides_weekN.py")
    ap.add_argument("out_qmd", type=Path,
                    help="Output .qmd path")
    ap.add_argument("--theme", default="../../sds-reveal/sds.scss",
                    help="Relative path from the .qmd to sds.scss")
    args = ap.parse_args()
    port(args.build_script, args.out_qmd, args.theme)


if __name__ == "__main__":
    main()
