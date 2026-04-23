# Password-protecting the readings site

The readings-game-plan doc tells students to visit a password-protected
readings page. This file records how to actually set that up.

## Constraints

- We're on GitHub Pages, which is a static host (no server-side auth).
- We're willing to trade security for simplicity: the goal is to keep PDFs
  out of Google's index and away from casual re-sharing, NOT to defend
  against a determined adversary. The students are all enrolled and we can
  rotate the password via Slack.

## Approach: staticrypt

Use [`staticrypt`](https://github.com/robinmoisson/staticrypt) (npm).
It AES-encrypts the HTML of a given page at build time, producing a
single self-contained HTML file that decrypts in-browser when the reader
enters the password. No backend, no bundling — fits perfectly with
GitHub Pages.

```bash
# One-time install.
npm install -g @staticrypt/cli

# Build step (add to whatever script renders docs/readings/):
staticrypt docs/readings/index.html --password "<SP26 password>" -d docs/readings/
# Overwrites docs/readings/index.html with the encrypted version.
# Keep the original source in a separate location that's gitignored.
```

## Where the password lives

- Primary: pinned message in Slack `#announcements`.
- Rotate once mid-semester (after Week 6) or if it leaks.
- Never check the password into the repo. Use an environment variable
  (`READINGS_PW`) and consume it in a script:

```bash
READINGS_PW="$(pass show class/sp26)"  # or 1Password / env var
npm exec staticrypt -- docs/readings/index.html -p "$READINGS_PW" -d docs/readings/
```

## Where the PDFs live

The PDFs in `resources/readings/` should NOT be served unencrypted. Two options:

1. **Upload PDFs to a private Google Drive folder**, and in the encrypted
   index-page embed Drive-viewer links. Simplest.
2. **Put PDFs in `docs/readings/assets/`** and rely on the fact that the
   encrypted index is the only discoverable link. A determined user could
   still guess PDF URLs, but Google won't index them if there's no
   public path. Add a `robots.txt` and `<meta name="robots" content="noindex">`
   for belt-and-suspenders.

Recommendation: **option 1** (Google Drive). It's the same level of
practical security, and Drive handles access revocation if a PDF needs
to be pulled.

## What goes on the readings page

The `_build.py` in this directory already consumes `course/readings_map.yml`.
Extend it to emit `docs/readings/index.html` with:

- Table of contents: one row per Week, with theme + date.
- Per-week section: required readings (citations + Drive links),
  optional readings, presentation candidates, current presenter
  (filled after Week 2 signup).
- Link to `reading-game-plan.md` at the top so students have the rules
  in one click.

## TODO

- [ ] Decide: Google Drive folder vs. in-repo PDFs. (Prof. Austerweil.)
- [ ] Extend `docs/_build.py` to render `docs/readings/index.html` from
      `course/readings_map.yml`.
- [ ] Install staticrypt; integrate into the build step.
- [ ] Pick initial SP26 password, pin to Slack `#announcements`.
- [ ] After Week 2 class: fill `presenter:` fields in `readings_map.yml`
      and rebuild.
