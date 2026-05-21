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

const PUPPETEER_PATH = '/home/jausterw/.nvm/versions/node/v22.20.0/lib/node_modules/decktape/node_modules/puppeteer';
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
    const columnSets = present.querySelectorAll('.columns');
    for (const cs of columnSets) {
      const cols = cs.querySelectorAll(':scope > .column');
      if (cols.length < 2) continue;             // not a real multi-column row

      // Measure every wide-enough column in this row first.
      const colBoxes = [];
      for (const col of cols) {
        const cr = col.getBoundingClientRect();
        if (cr.width < stageRect.width * 0.12) continue;  // ignore sliver columns
        const box = measureBox(col);
        if (!box) continue;                      // empty column (e.g. spacer)
        colBoxes.push(box);
        nColumns++;
        if (box.fill < columnFill) columnFill = box.fill;
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
      contentTop: Math.min(sectionContentTop, innerTopGap * stageH / 100),
      contentBottom: Math.max(sectionContentBottom, stageH - innerBottomGap * stageH / 100),
      title, framed, titleSlide,
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

function classify(m, threshold) {
  if (!m) return 'NO-DATA';
  if (m.framed || m.titleSlide) return 'SKIP-FRAMED';
  if (m.contentTop < -2 || m.contentBottom > m.stageH + 2) return 'OVERFLOW';
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
  return 'OK';
}

(async () => {
  const args = parseArgs();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const jsonPath = args.jsonPath || `${OUT_DIR}/slide-fill.json`;

  const sizes = args.allSizes ? ALL_SIZES : [NOMINAL];

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: NOMINAL.w, height: NOMINAL.h, deviceScaleFactor: 1 });
  await page.goto(DECK, { waitUntil: 'networkidle0' });
  await page.waitForFunction(() => window.Reveal && window.Reveal.isReady && window.Reveal.isReady(), { timeout: 30000 });

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
      const priority = { 'OVERFLOW': 6, 'FLOATING': 5, 'BOTTOM-GAP': 4, 'PUSHED-DOWN': 3, 'COLUMN-THIN': 3, 'COLUMN-SKEW': 3, 'SHORT': 2, 'OK': 1, 'SKIP-FRAMED': 0, 'NO-DATA': 0 };
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
    console.log(`${marker} ${String(i).padStart(3)}  [${worstFlag.padEnd(11)}] fill=${nominal.fillPct.toFixed(1).padStart(5)}%  top=${nominal.topGapPct.toFixed(1).padStart(5)}%  bot=${nominal.bottomGapPct.toFixed(1).padStart(5)}%  ${nominal.title}${colNote}`);

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

  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
