// Audit RevealJS slides for poor vertical fill.
//
// Two distinct rendering modes need to be handled:
//
//   center: true   — RevealJS sets section.present to position:absolute,
//                    sizes it to its content, and centers it vertically
//                    in .slides. Dead space appears symmetrically top+bottom.
//                    Measure: section.height vs slides.height.
//
//   center: false  — section.present fills the stage, content sits at top.
//                    Dead space appears at bottom. section.height ≈ slides.height
//                    always, so we have to measure the content bbox INSIDE the
//                    section, not the section itself.
//
// We measure both and use the more conservative (lower) fill value.
//
// The script also tests multiple viewport sizes including ±50px wobble around
// the deck's nominal logical size (1050x700), plus several 16:9 ratios. If a
// slide is robust at nominal but breaks ±50px off, we want to flag it.
//
// Usage:
//   node scripts/audit_slide_fill.js [--from N] [--to M] [--threshold P] [--all-sizes]

const path = require('path');
const fs = require('fs');

// puppeteer-core (library only — no bundled Chromium) installed user-locally so it
// survives nvm/global churn; it drives the system google-chrome via executablePath
// below. Reinstall with: PUPPETEER_SKIP_DOWNLOAD=1 npm install \
//   --prefix ~/.local/lib/node-tools puppeteer-core@22   (pin v22: CommonJS + node-18 OK).
const PUPPETEER_PATH = process.env.PUPPETEER_PATH
  || '/home/jausterw/.local/lib/node-tools/node_modules/puppeteer-core';
const puppeteer = require(PUPPETEER_PATH);

const REPO = '/home/jausterw/work/hummachlearn/spring2026';
// DECK / OUT_DIR default to Week 3 but are overridable per-week via env vars:
//   DECK=course/week04_generalization_hier_bayes/week4-slides.html \
//   OUT_DIR=course/week04_generalization_hier_bayes/week4-audit \
//   node scripts/audit_slide_fill.js --threshold 75
const DECK = process.env.DECK
  ? `file://${path.resolve(REPO, process.env.DECK)}`
  : `file://${REPO}/course/week03_conjugate_bayes_topics/week3-slides.html`;
const OUT_DIR = process.env.OUT_DIR
  ? path.resolve(REPO, process.env.OUT_DIR)
  : `${REPO}/course/week03_conjugate_bayes_topics/week3-audit`;

const NOMINAL = { w: 1050, h: 700, label: 'nominal' };
const ALL_SIZES = [
  NOMINAL,
  { w: 1000, h: 700, label: 'narrow-50' },
  { w: 1100, h: 700, label: 'wide+50' },
  { w: 1050, h: 650, label: 'short-50' },
  { w: 1050, h: 750, label: 'tall+50' },
  { w: 1280, h: 720, label: '16:9-720p' },
  { w: 1920, h: 1080, label: '16:9-1080p' },
  { w: 1366, h: 768, label: '16:9-laptop' },
];

function parseArgs() {
  const args = { from: 1, to: Infinity, threshold: 75, allSizes: false, jsonPath: null, verbose: false };
  for (let i = 2; i < process.argv.length; i++) {
    const a = process.argv[i];
    if (a === '--from') args.from = parseInt(process.argv[++i], 10);
    else if (a === '--to') args.to = parseInt(process.argv[++i], 10);
    else if (a === '--threshold') args.threshold = parseFloat(process.argv[++i]);
    else if (a === '--all-sizes') args.allSizes = true;
    else if (a === '--verbose') args.verbose = true;
    else if (a === '--json') args.jsonPath = process.argv[++i];
  }
  return args;
}

async function measureSlideAtSize(page, slideIdx, size, slideIndices) {
  await page.setViewport({ width: size.w, height: size.h, deviceScaleFactor: 1 });
  await page.evaluate(() => window.Reveal && window.Reveal.layout && window.Reveal.layout());
  await new Promise((r) => setTimeout(r, 120));
  // Use precomputed (h,v) indices so we navigate the 2D grid correctly
  // when slide-level produces nested vertical sub-slides.
  const coords = slideIndices[slideIdx - 1];
  await page.evaluate((h, v) => window.Reveal.slide(h, v, 0), coords.h, coords.v);
  await new Promise((r) => setTimeout(r, 200));

  // Reveal ALL fragments before measuring. Un-revealed fragments are
  // visibility:hidden (NOT display:none) — laid out but excluded by the
  // measureBox visibility filter — so poll-option / answer / build-up
  // fragments are invisible to the measurement and the slide false-flags as
  // sparse (BOTTOM-GAP / FLOATING). Adding `.visible` flips each descendant's
  // computed visibility to visible so we measure the TRUE filled state.
  // `.fade-out`-style fragments are skipped: their true final state is hidden.
  await page.evaluate(() => {
    document.querySelectorAll('section.present .fragment').forEach((f) => {
      if (f.classList.contains('fade-out') ||
          f.classList.contains('fade-in-then-out') ||
          f.classList.contains('semi-fade-out')) return;
      f.classList.add('visible');
    });
    window.Reveal && window.Reveal.layout && window.Reveal.layout();
  });
  await new Promise((r) => setTimeout(r, 150));

  return await page.evaluate(() => {
    // Multiple `section.present` exist for nested vertical slides — the
    // horizontal parent AND its active vertical child both carry .present.
    // Pick the deepest one (the actual visible content sub-slide).
    const allPresent = document.querySelectorAll('section.present');
    const present = allPresent[allPresent.length - 1];
    const slides = document.querySelector('.reveal .slides');
    if (!present || !slides) return null;

    const stageRect = slides.getBoundingClientRect();
    const sectRect = present.getBoundingClientRect();
    const stageH = stageRect.height;
    const stageTop = stageRect.top;

    // SECTION measurement (catches center:true floating)
    const sectionContentTop = sectRect.top - stageTop;
    const sectionContentBottom = sectRect.bottom - stageTop;
    const sectionFill = (sectRect.height / stageH) * 100;
    const sectionTopGap = (sectionContentTop / stageH) * 100;
    const sectionBottomGap = ((stageH - sectionContentBottom) / stageH) * 100;

    // measureBox: bounding box of the rendered content inside `root`, in
    // stage-relative percentages. Ignores hidden language divs and fixed
    // branding. Returns null when `root` has no visible content.
    const measureBox = (root) => {
      const els = root.querySelectorAll(
        'h1, h2, h3, h4, p, li, table, .math, img, blockquote, pre');
      let top = Infinity, bottom = -Infinity;
      for (const el of els) {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        if (cs.position === 'fixed') continue;
        if (r.top < top) top = r.top;
        if (r.bottom > bottom) bottom = r.bottom;
      }
      if (top === Infinity) return null;
      return {
        fill: ((bottom - top) / stageH) * 100,
        topGap: ((top - stageTop) / stageH) * 100,
        bottomGap: ((stageTop + stageH - bottom) / stageH) * 100,
        top: top - stageTop,
        bottom: bottom - stageTop,
      };
    };

    // INNER CONTENT measurement (catches center:false short-content slides):
    // the bounding box across ALL content on the slide.
    const inner = measureBox(present);
    let innerFill = 0, innerTopGap = 0, innerBottomGap = 100;
    if (inner) {
      innerFill = inner.fill;
      innerTopGap = inner.topGap;
      innerBottomGap = inner.bottomGap;
    }

    // PER-COLUMN measurement (catches the two-column failure modes). A tall
    // figure column can fill the slide while the text column beside it is
    // (a) sparse — too little content — or (b) top-jammed — content pooled at
    // the top of the column with a void below. The whole-slide inner box sees
    // neither: the figure sets the bounds. So measure each Quarto
    // `.columns > .column` on its own.
    //
    // Two things are measured per column, and BOTH are vs. the column's own
    // `.columns` ROW (not the whole stage): the content fill, and where that
    // content sits within the row. A column's content vertical spread is
    // therefore handled independently for each column.
    //  - columnFill   = min content-fill across columns (the sparse case).
    //  - columnSkew   = max |topGap - bottomGap| within the row across columns
    //                   (the imbalance case — content not vertically centered
    //                   in its row). 0 = perfectly centered.
    let columnFill = Infinity;       // min fill across columns; Infinity = no columns
    let columnSkew = 0;              // worst within-row vertical imbalance
    let nColumns = 0;
    // CAPTION ALIGNMENT (multi-column figure rows): when each column ends in a
    // short text "caption" directly under an image, the captions should share a
    // baseline (vertical alignment) and sit centred under their figure
    // (horizontal alignment). Measured per `.columns` row:
    //  - captionVMisalign = max vertical spread of caption baselines across the
    //    row, as a % of stage height. 0 = all captions on one line.
    //  - captionHMisalign = worst |captionCenterX − figureCenterX| in a column,
    //    as a % of that column's width. 0 = every caption centred under its image.
    let captionVMisalign = 0;
    let captionHMisalign = 0;
    let hasCaptions = false;
    // helper: the "caption" of a column = its last visible block-text element
    // (p / figcaption / li) that sits BELOW the column's image, if any.
    const captionOf = (col) => {
      const img = col.querySelector('img');
      if (!img) return null;
      const ir = img.getBoundingClientRect();
      if (ir.height === 0) return null;
      const texts = col.querySelectorAll('p, figcaption, .dim, li');
      let best = null;
      for (const t of texts) {
        const r = t.getBoundingClientRect();
        const cs = getComputedStyle(t);
        if (r.width === 0 || r.height === 0) continue;
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        if (cs.position === 'fixed') continue;
        if (t.querySelector('img')) continue;       // skip the image's own wrapper
        if (r.top < ir.bottom - 2) continue;         // must be BELOW the image
        if (!best || r.top > best.top) best = r;     // lowest text = the caption
      }
      return best ? { capCx: best.left + best.width / 2, capY: best.bottom,
                      figCx: ir.left + ir.width / 2, colW: col.getBoundingClientRect().width }
                  : null;
    };
    const columnSets = present.querySelectorAll('.columns');
    for (const cs of columnSets) {
      const cols = cs.querySelectorAll(':scope > .column');
      if (cols.length < 2) continue;             // not a real multi-column row

      // Measure every wide-enough column in this row first.
      const colBoxes = [];
      const caps = [];
      for (const col of cols) {
        const cr = col.getBoundingClientRect();
        if (cr.width < stageRect.width * 0.12) continue;  // ignore sliver columns
        const box = measureBox(col);
        if (!box) continue;                      // empty column (e.g. spacer)
        colBoxes.push(box);
        nColumns++;
        if (box.fill < columnFill) columnFill = box.fill;
        const cap = captionOf(col);
        if (cap) caps.push(cap);
      }
      // Caption alignment only meaningful when ≥2 columns each have a caption.
      if (caps.length >= 2) {
        hasCaptions = true;
        const capYs = caps.map((c) => c.capY);
        const vSpread = (Math.max(...capYs) - Math.min(...capYs)) / stageH * 100;
        if (vSpread > captionVMisalign) captionVMisalign = vSpread;
        for (const c of caps) {
          const h = c.colW > 0 ? Math.abs(c.capCx - c.figCx) / c.colW * 100 : 0;
          if (h > captionHMisalign) captionHMisalign = h;
        }
      }
      if (colBoxes.length < 2) continue;

      // Within-row vertical balance: the row spans from the topmost column's
      // content-top to the bottommost column's content-bottom. A short column
      // is well-placed if its content is CENTERED in that span; it is
      // top-jammed if its content hugs the span's top with a void below.
      // columnSkew = how far the worst column's center sits from the row's
      // center, as a % of the row span. 0 = every column centered.
      // (Measured stage-relative — robust regardless of how the flexbox
      // container itself reports its height.)
      const rowTop = Math.min(...colBoxes.map((b) => b.top));
      const rowBottom = Math.max(...colBoxes.map((b) => b.bottom));
      const rowSpan = rowBottom - rowTop;
      if (rowSpan > 0) {
        const rowCenter = (rowTop + rowBottom) / 2;
        for (const b of colBoxes) {
          const colCenter = (b.top + b.bottom) / 2;
          const skew = (Math.abs(colCenter - rowCenter) / rowSpan) * 100;
          if (skew > columnSkew) columnSkew = skew;
        }
      }
    }
    const hasColumns = columnFill !== Infinity;

    // fillPct is the WHOLE-SLIDE fill: the more conservative of the section
    // box (catches center:true floating) and the all-content inner box
    // (catches center:false short content). Per-column fill is deliberately
    // NOT folded in here — otherwise a figure-heavy two-column slide gets
    // mislabeled SHORT/FLOATING when the slide as a whole is fine and only
    // the text column is thin. The thin-column case has its own signal:
    // `columnFill` below + the COLUMN-THIN flag in classify().
    const fillPct = Math.min(sectionFill, innerFill);
    const topGapPct = Math.max(sectionTopGap, innerTopGap);
    const bottomGapPct = Math.max(sectionBottomGap, innerBottomGap);

    const titleEl = present.querySelector('h1, h2');
    let title = titleEl ? titleEl.innerText.trim().split('\n')[0] : '';
    if (title.length > 60) title = title.slice(0, 57) + '...';

    const framed = present.classList.contains('sds-framed') || present.classList.contains('section-break');
    const titleSlide = present.classList.contains('title-slide') || present.classList.contains('quarto-title-block');

    // EMPTY-SLIDE detection. A bare `# {.section-break}` (no title, no body)
    // renders as an empty frame — the most embarrassing defect, and one the
    // old SKIP-FRAMED blanket let through. Count the slide's VISIBLE,
    // non-hidden-language, non-fixed content elements (excluding the title
    // itself), and record whether the slide has a real title at all.
    let contentCount = 0;
    {
      const els = present.querySelectorAll('h3, h4, p, li, table, .math, img, blockquote, pre');
      for (const el of els) {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        if (cs.position === 'fixed') continue;
        // skip the in-frame language badge / nav chrome if any slipped through
        if (el.closest('.lang-badge, .controls, .progress')) continue;
        contentCount++;
      }
    }
    const hasTitle = !!(titleEl && titleEl.innerText.trim().length > 0);

    // Title vertical position within the stage (for jammed-title detection on
    // framed slides — a section-break title should sit comfortably inside the
    // frame, not pinned to its top edge).
    let titleTopPct = null;
    if (titleEl) {
      const tr = titleEl.getBoundingClientRect();
      if (tr.height > 0) titleTopPct = ((tr.top - stageTop) / stageH) * 100;
    }

    // FIGURE metrics (layout-scheme v2). The fill metric alone REWARDS
    // text-stuffing: a slide whose figure has been flex-crushed to a sliver
    // still audits ~100% full because the text fills the stage. So measure the
    // figures themselves:
    //  - figVisibleH: the LARGEST figure's *visible content* height (as % of
    //    stage). Under object-fit:contain the painted content can be smaller
    //    than the img box (letterboxing), so compute the contain-scaled size
    //    from naturalWidth/naturalHeight rather than trusting the box.
    //  - figAspectSkew: worst |rendered aspect / natural aspect − 1| among
    //    figures NOT protected by object-fit:contain — a squished/stretched
    //    figure. Should be ~0 everywhere now that the theme sets contain;
    //    kept as a regression guard.
    // Only "main" figures count (naturalWidth ≥ 400px): icons, badges, and
    // branding are ignored.
    let figCount = 0;
    let figVisibleH = null;        // largest figure's visible height, % of stage
    let figAspectSkew = 0;
    {
      const imgs = present.querySelectorAll('img');
      for (const img of imgs) {
        if (!img.naturalWidth || img.naturalWidth < 400) continue;
        const r = img.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        const cs = getComputedStyle(img);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        if (cs.position === 'fixed') continue;
        figCount++;
        const natAspect = img.naturalWidth / img.naturalHeight;
        let visW = r.width, visH = r.height;
        if (cs.objectFit === 'contain' || cs.objectFit === 'scale-down') {
          const scale = Math.min(r.width / img.naturalWidth, r.height / img.naturalHeight);
          visW = img.naturalWidth * scale;
          visH = img.naturalHeight * scale;
        } else {
          const skew = Math.abs((r.width / r.height) / natAspect - 1);
          if (skew > figAspectSkew) figAspectSkew = skew;
        }
        const hPct = (visH / stageH) * 100;
        if (figVisibleH === null || hPct > figVisibleH) figVisibleH = hPct;
      }
    }

    // PROSE-WALL detection. A continuous paragraph that wraps to 4+ rendered
    // lines is a wall of text — the recurring authoring defect (Week 11 "it's
    // just a giant block of text", Week 12 slides 8/11). Slides want bullets,
    // a two-column split, or speaker notes; the textbook is where prose lives.
    // Only VISIBLE paragraphs count (the hidden language div is skipped by the
    // size check), and only real prose (≥ 200 chars) — a 4-line equation or a
    // wrapped caption of modest length doesn't fire.
    let proseWall = false;
    {
      const paras = present.querySelectorAll('p');
      for (const p of paras) {
        if (p.closest('.notes, aside')) continue;
        const r = p.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        const cs = getComputedStyle(p);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        if (cs.position === 'fixed') continue;
        if (p.querySelector('img')) continue;
        const text = (p.innerText || '').trim();
        if (text.length < 200) continue;
        const lineH = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.5;
        const lines = Math.round(r.height / lineH);
        if (lines >= 4) { proseWall = true; break; }
      }
    }

    // LAYOUT ARCHETYPE (for the deck-level layout-mix report). Coarse but
    // useful: a deck where most content slides classify as "bullets/prose"
    // is a mono-layout deck — the recurring "not using different layouts
    // when it would be effective" complaint.
    let archetype = 'bullets/prose';
    if (present.classList.contains('poll-slide') || present.classList.contains('poll-reveal')) archetype = 'poll';
    else if (present.classList.contains('widget-slide')) archetype = 'widget';
    else if (present.classList.contains('statement')) archetype = 'statement';
    else if (present.querySelector('.columns')) archetype = 'columns';
    else if (figCount > 0) archetype = 'figure';
    else if (present.querySelector('table')) archetype = 'table';
    else if (present.querySelector('pre')) archetype = 'code';
    else if (present.querySelector('.note-card')) archetype = 'cards';

    // RUN-ON CAPTION detection. A caption/description paragraph that packs 2+
    // parallel bold-led clauses ("**State** = … . **Transition** = … .") onto
    // ONE line is hard to scan — each clause should get its own line (a bullet
    // list) when the slide has the vertical room. We look at visible <p>
    // elements (Quarto wraps a bracketed `[…]{.dim}` caption in a <p>) that:
    //   - contain ≥2 <strong>/<b> children whose bold text is immediately
    //     followed by '=' or ':' (the "labeled clause" signature), AND
    //   - render as essentially ONE line (height ≈ a single line-box).
    // runonCaption = true if any such paragraph exists. The classify() step
    // additionally requires the slide to have spare vertical room, so we only
    // nag when splitting onto more lines would actually fit.
    let runonCaption = false;
    {
      const paras = present.querySelectorAll('p');
      for (const p of paras) {
        const r = p.getBoundingClientRect();
        const cs = getComputedStyle(p);
        if (r.width === 0 || r.height === 0) continue;
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        if (cs.position === 'fixed') continue;
        // count bold-led "label =" / "label:" clauses
        const bolds = p.querySelectorAll('strong, b');
        if (bolds.length < 2) continue;
        let labeledClauses = 0;
        for (const bEl of bolds) {
          // text right after the bold run, within the same paragraph
          let after = '';
          let n = bEl.nextSibling;
          while (n && after.trim().length === 0) {
            after += (n.textContent || '');
            n = n.nextSibling;
          }
          const head = after.replace(/^\s+/, '').slice(0, 2);
          if (head.startsWith('=') || head.startsWith(':') || head.startsWith('：') ||
              head.startsWith('＝')) labeledClauses++;
        }
        // 2+ bold-led "label =/:" clauses in ONE paragraph is the run-on
        // signature — flag it regardless of whether it wraps to 1 or 2 lines
        // (a run-on that already wraps is still the defect; splitting each
        // clause onto its own bullet is the fix). The "is there room to split"
        // judgement is left to classify()'s bottom-gap gate.
        if (labeledClauses >= 2) { runonCaption = true; break; }
      }
    }

    return {
      stageH,
      sectionH: sectRect.height,
      innerH: inner ? inner.bottom - inner.top : 0,
      fillPct, topGapPct, bottomGapPct,
      sectionFill, sectionTopGap, sectionBottomGap,
      innerFill, innerTopGap, innerBottomGap,
      hasColumns,
      nColumns,
      columnFill: hasColumns ? columnFill : null,
      columnSkew: hasColumns ? columnSkew : null,
      hasCaptions,
      captionVMisalign: hasCaptions ? captionVMisalign : null,
      captionHMisalign: hasCaptions ? captionHMisalign : null,
      runonCaption,
      figCount, figVisibleH, figAspectSkew, proseWall, archetype,
      contentTop: Math.min(sectionContentTop, innerTopGap * stageH / 100),
      contentBottom: Math.max(sectionContentBottom, stageH - innerBottomGap * stageH / 100),
      title, framed, titleSlide, contentCount, hasTitle, titleTopPct,
    };
  });
}

// A text column legitimately runs shorter than a figure beside it, so the
// column threshold is well below the whole-slide one — flag only a genuinely
// sparse column (a few words floating beside a full-height figure), not a
// substantive 3-5 element text panel that simply isn't as tall as the figure.
// Calibrated against real slides: genuinely-bad columns measured 20-38%;
// substantive text panels beside a chart measured 44-60%. 42% cleanly
// separates them. (The whole-slide threshold stays the stricter 75%.)
const COLUMN_THRESHOLD = 42;
// Max acceptable within-row vertical imbalance: how lopsided a column's
// content may be inside its `.columns` row (|topGap - bottomGap|, % of row
// height). A `.v-center`ed column should be ~0; a top-jammed column with a
// big void below skews high. >34 means visibly off-center.
const COLUMN_SKEW_LIMIT = 34;
// Caption alignment in a multi-column figure row (e.g. three portraits each
// with a label beneath). Captions should share a baseline and sit centred
// under their figure. Calibrated against the broken Markov-timeline slide
// (captions on three different lines, one left-aligned): vertical spread was
// ~6% of stage and horizontal offset ~30% of column width. Aligned captions
// measure ~0 on both. Thresholds leave headroom for a one-line font-descender
// difference (~1.5% V) and a hair of centring slop (~8% H).
const CAPTION_V_LIMIT = 2.5;   // max caption baseline spread, % of stage height
const CAPTION_H_LIMIT = 12;    // max caption-vs-figure horizontal offset, % of col width
// Figure legibility floor (layout-scheme v2): the LARGEST figure on a slide
// must paint at least this % of the stage height to be readable from the back
// row. 24% of a 540px stage ≈ 130px — matplotlib axis labels and box text are
// gone well before that. Calibrated against the Week 12 defects: slide 8's
// crushed figure measured ~23% (illegible), the same figure given the flex
// floor measures ~55%+.
const FIG_MIN_PCT = 24;
// A figure painted at a wrong aspect (squished/stretched). The theme's
// object-fit:contain makes this impossible; the check is a regression guard
// for a deck that overrides it. 12% distortion is clearly visible.
const FIG_ASPECT_SKEW_LIMIT = 0.12;

function classify(m, threshold) {
  if (!m) return 'NO-DATA';
  // EMPTY-FRAME: a slide (framed or not) with no title AND essentially no
  // content is a rendering defect — e.g. a bare `# {.section-break}` that
  // renders as an empty yellow frame. This is checked BEFORE the framed-slide
  // skip so section-breaks can no longer hide an empty slide. The Quarto title
  // slide is exempt (its title lives in a separate block).
  if (!m.titleSlide && !m.hasTitle && m.contentCount === 0) return 'EMPTY-FRAME';
  // A framed/section-break slide is SUPPOSED to be title-only — but only if it
  // actually has a title. Title present → skip the fill checks (legit sparse).
  if ((m.framed || m.titleSlide) && (m.hasTitle || m.titleSlide)) {
    // JAMMED-TITLE: a framed title pinned to the very top edge of the frame
    // (title top < 6% of stage) reads as broken — it should sit inside the
    // frame, vertically centered-ish. Flag it; otherwise the framed slide is OK.
    if (m.framed && m.titleTopPct !== null && m.titleTopPct < 6) return 'JAMMED-TITLE';
    return 'SKIP-FRAMED';
  }
  // OVERFLOW = content genuinely spills past the frame (would be clipped on a
  // real projector). A small tolerance (~1.5% of stage height) absorbs the
  // sub-pixel "filled exactly to the edge" case produced by space-between
  // fill layouts — those are GOOD (the slide is full), not overflowing. Only
  // a real spill beyond that tolerance is a defect.
  const ovTol = m.stageH * 0.015;
  if (m.contentTop < -ovTol || m.contentBottom > m.stageH + ovTol) return 'OVERFLOW';
  // SQUISHED-FIGURE: a figure painted at the wrong aspect ratio (a flexed
  // height fighting an inline width, with object-fit:contain overridden).
  // Regression guard — the theme makes this structurally impossible.
  if (m.figCount > 0 && m.figAspectSkew > FIG_ASPECT_SKEW_LIMIT) return 'SQUISHED-FIGURE';
  // TINY-FIGURE: the slide's LARGEST figure paints below the legibility floor.
  // This is the marquee recurring defect (Weeks 9, 10, 12): a figure starved
  // of height by the text stacked around it. The fill metric cannot see it —
  // text fills the stage while the figure dies. Remediation is NEVER "shrink
  // something else a bit": trim the text to ≤2 caption lines, split to a
  // two-column, or give the figure its own slide.
  if (m.figCount > 0 && m.figVisibleH !== null && m.figVisibleH < FIG_MIN_PCT) return 'TINY-FIGURE';
  // PROSE-WALL: a paragraph wrapping to 4+ rendered lines (~200+ chars) is a
  // wall of text — slides carry bullets and punchlines, prose belongs in the
  // textbook or the speaker notes. Rewrite as bullets (one clause per line),
  // split to columns, or move detail to ::: {.notes}. Statement slides are
  // exempt: they are deliberate hero prose (short by their own contract).
  if (m.proseWall && m.archetype !== 'statement') return 'PROSE-WALL';
  // RUNON-CAPTION: a caption paragraph crams 2+ bold-led clauses onto one line,
  // AND the slide has vertical room to spare (bottom gap > 10%), so splitting
  // each clause onto its own line would fit. Checked BEFORE the fill flags: a
  // run-on caption is a content/scannability issue independent of fill, and a
  // slide with a run-on caption usually ALSO trips a borderline BOTTOM-GAP
  // (the unused room is exactly why the split would fit) — the caption is the
  // actionable defect, so report it first. Only nag when the fix is free.
  if (m.runonCaption && m.bottomGapPct > 10) return 'RUNON-CAPTION';
  if (m.fillPct < threshold && m.topGapPct > 8 && m.bottomGapPct > 8) return 'FLOATING';
  if (m.fillPct < threshold && m.bottomGapPct > 20) return 'BOTTOM-GAP';
  if (m.fillPct < threshold && m.topGapPct > 15) return 'PUSHED-DOWN';
  if (m.fillPct < threshold) return 'SHORT';
  // Whole-slide fill is fine. But on a two-column slide a tall figure can
  // mask the column beside it in two ways, each measured per-column:
  //  - columnFill: the text column is too SPARSE (too little content), or
  //  - columnSkew: a column's content is not vertically centered in its row
  //    — top-jammed with a void below (add `.v-center` to the columns div).
  // Either trips COLUMN-THIN; the whole-slide box sees neither.
  if (m.hasColumns && m.columnFill !== null && m.columnFill < COLUMN_THRESHOLD) {
    return 'COLUMN-THIN';
  }
  if (m.hasColumns && m.columnSkew !== null && m.columnSkew > COLUMN_SKEW_LIMIT) {
    return 'COLUMN-SKEW';
  }
  // CAPTION-MISALIGN: in a multi-column figure row, the per-column captions are
  // either on different baselines (V) or not centred under their figure (H).
  // Fix by composing the panels into ONE figure, or padding the images to a
  // common height + centring the caption text.
  if (m.hasCaptions &&
      ((m.captionVMisalign !== null && m.captionVMisalign > CAPTION_V_LIMIT) ||
       (m.captionHMisalign !== null && m.captionHMisalign > CAPTION_H_LIMIT))) {
    return 'CAPTION-MISALIGN';
  }
  return 'OK';
}

(async () => {
  const args = parseArgs();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const jsonPath = args.jsonPath || `${OUT_DIR}/slide-fill.json`;

  const sizes = args.allSizes ? ALL_SIZES : [NOMINAL];

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: process.env.CHROME_BIN || '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: NOMINAL.w, height: NOMINAL.h, deviceScaleFactor: 1 });
  await page.goto(DECK, { waitUntil: 'networkidle0' });
  await page.waitForFunction(() => window.Reveal && window.Reveal.isReady && window.Reveal.isReady(), { timeout: 30000 });

  // Match the audit viewport's ASPECT RATIO to the deck's actual logical size
  // (from Reveal's config: e.g. 960×540 = 16:9). A hardcoded 1050×700 (3:2)
  // makes content that fits the real 16:9 slide overflow the taller test
  // viewport — a pure measurement artifact. Scale the deck's logical size up
  // to a comfortable measurement resolution, preserving aspect.
  const deckSize = await page.evaluate(() => {
    const c = window.Reveal.getConfig ? window.Reveal.getConfig() : {};
    return { w: c.width || 1050, h: c.height || 700 };
  });
  const aspect = deckSize.w / deckSize.h;
  const measH = 700;                      // fixed measurement height
  const measW = Math.round(measH * aspect);
  NOMINAL.w = measW; NOMINAL.h = measH;
  NOMINAL.label = `nominal ${deckSize.w}x${deckSize.h}`;
  console.log(`Deck logical size ${deckSize.w}x${deckSize.h} (aspect ${aspect.toFixed(3)}) → measuring at ${measW}x${measH}`);
  await page.setViewport({ width: NOMINAL.w, height: NOMINAL.h, deviceScaleFactor: 1 });
  await page.evaluate(() => window.Reveal.layout && window.Reveal.layout());

  // Build flat list of (h, v) coordinates so we can navigate the 2D Reveal grid
  // (slide-level pairings create nested vertical sub-slides).
  const slideIndices = await page.evaluate(() => {
    const horizontalSections = document.querySelectorAll('.reveal .slides > section');
    const out = [];
    horizontalSections.forEach((hs, h) => {
      const verticals = hs.querySelectorAll(':scope > section');
      if (verticals.length === 0) {
        out.push({ h, v: 0 });
      } else {
        verticals.forEach((_, v) => out.push({ h, v }));
      }
    });
    return out;
  });
  const totalSlides = slideIndices.length;
  const to = Math.min(args.to, totalSlides);
  console.log(`Total slides: ${totalSlides}`);
  console.log(`Auditing ${args.from}..${to} at ${sizes.length} viewport size(s), threshold ${args.threshold}%`);
  console.log('');

  const allResults = [];

  for (let i = args.from; i <= to; i++) {
    const perSize = [];
    let worstFlag = 'OK';
    for (const size of sizes) {
      const m = await measureSlideAtSize(page, i, size, slideIndices);
      const flag = classify(m, args.threshold);
      perSize.push({ size: size.label, ...m, flag });
      const priority = { 'EMPTY-FRAME': 8, 'JAMMED-TITLE': 7, 'SQUISHED-FIGURE': 6.6, 'TINY-FIGURE': 6.5, 'OVERFLOW': 6, 'CAPTION-MISALIGN': 5.5, 'FLOATING': 5, 'PROSE-WALL': 4.8, 'RUNON-CAPTION': 4.5, 'BOTTOM-GAP': 4, 'PUSHED-DOWN': 3, 'COLUMN-THIN': 3, 'COLUMN-SKEW': 3, 'SHORT': 2, 'OK': 1, 'SKIP-FRAMED': 0, 'NO-DATA': 0 };
      if (priority[flag] > priority[worstFlag]) worstFlag = flag;
    }

    const nominal = perSize[0];
    const marker = worstFlag === 'OK' || worstFlag === 'SKIP-FRAMED' ? '  ' : '>>';
    // Show the thinnest-column fill and worst within-row skew in the trailing
    // note when columns exist, so a two-column slide's report is legible
    // without opening the JSON.
    const colNote = nominal.hasColumns
      ? `  (col=${nominal.columnFill.toFixed(1)}% skew=${nominal.columnSkew.toFixed(0)})`
      : '';
    const capNote = nominal.hasCaptions
      ? `  (capV=${nominal.captionVMisalign.toFixed(1)}% capH=${nominal.captionHMisalign.toFixed(0)}%)`
      : '';
    const figNote = nominal.figCount > 0 && nominal.figVisibleH !== null
      ? `  (fig=${nominal.figVisibleH.toFixed(0)}%)`
      : '';
    console.log(`${marker} ${String(i).padStart(3)}  [${worstFlag.padEnd(11)}] fill=${nominal.fillPct.toFixed(1).padStart(5)}%  top=${nominal.topGapPct.toFixed(1).padStart(5)}%  bot=${nominal.bottomGapPct.toFixed(1).padStart(5)}%  ${nominal.title}${colNote}${capNote}${figNote}`);

    if ((sizes.length > 1 || args.verbose) && worstFlag !== 'OK' && worstFlag !== 'SKIP-FRAMED') {
      for (const r of perSize) {
        if (r.flag === 'OK' || r.flag === 'SKIP-FRAMED') continue;
        console.log(`         ${r.size.padEnd(14)} fill=${r.fillPct.toFixed(1).padStart(5)}%  top=${r.topGapPct.toFixed(1).padStart(5)}%  bot=${r.bottomGapPct.toFixed(1).padStart(5)}%  [${r.flag}]`);
      }
    }

    allResults.push({ slide: i, title: nominal.title, worstFlag, perSize });
  }

  fs.writeFileSync(jsonPath, JSON.stringify(allResults, null, 2));
  console.log('');
  console.log(`Wrote ${jsonPath}`);
  const flagged = allResults.filter((r) => r.worstFlag !== 'OK' && r.worstFlag !== 'SKIP-FRAMED');
  console.log(`Flagged: ${flagged.length} / ${allResults.length} slides`);
  if (flagged.length > 0) {
    console.log('Flagged slide numbers:', flagged.map((r) => r.slide).join(', '));
  }

  // LAYOUT-MIX REPORT (layout-scheme v2). A deck that answers every content
  // slide with "title + bullets" reads flat — the recurring "not using
  // different layouts when it would be effective" complaint. This is an
  // ADVISORY, not a per-slide flag: eyeball the histogram, and if bullets/prose
  // dominates (> ~55% of content slides), look for slides whose content shape
  // wanted a figure, columns, cards, or a statement (see SLIDE_VISUAL_QA.md
  // "Choosing the layout").
  const contentSlides = allResults.filter((r) => {
    const n = r.perSize[0];
    return n && !n.framed && !n.titleSlide;
  });
  if (contentSlides.length > 0) {
    const mix = {};
    for (const r of contentSlides) {
      const a = r.perSize[0].archetype || 'bullets/prose';
      mix[a] = (mix[a] || 0) + 1;
    }
    console.log('');
    console.log('Layout mix (content slides):');
    const entries = Object.entries(mix).sort((a, b) => b[1] - a[1]);
    for (const [a, n] of entries) {
      const pct = (n / contentSlides.length) * 100;
      console.log(`  ${a.padEnd(14)} ${String(n).padStart(3)}  ${pct.toFixed(0)}%`);
    }
    const bp = mix['bullets/prose'] || 0;
    if (bp / contentSlides.length > 0.55) {
      console.log(`  >> MONO-LAYOUT advisory: ${((bp / contentSlides.length) * 100).toFixed(0)}% of content slides are bullets/prose — look for slides whose content shape wanted columns, a figure, cards, or a statement.`);
    }
  }

  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
