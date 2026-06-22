# Voxera Clone

A fully self-hosted, self-contained copy of the Framer site, exported and de-CDN'd so it
can be edited and hosted directly — no dependency on Framer's servers.

## Structure

```
.
├── index.html        # the page — edit content here
├── .nojekyll         # tells GitHub Pages to serve files/dirs verbatim (incl. the _-prefixed JS chunk)
└── assets/
    ├── images/       # all images
    ├── js/           # Framer runtime (ES module chunks)
    ├── fonts/        # woff2 fonts (Inter, Framer assets, Fontshare)
    ├── media/        # hero video
    └── data/         # search-index JSON
```

## Run locally

ES modules require HTTP (not `file://`):

```bash
python3 -m http.server 8787
# open http://localhost:8787
```

## Deploy

Hosted via GitHub Pages from the `main` branch root. Any push updates the live site.

## Notes

- All CDN URLs (framerusercontent.com, Google Fonts, Fontshare, catbox) were downloaded
  local and rewritten to relative `assets/` paths.
- The Framer analytics beacon (`events.framer.com`) was removed.
- A `<link rel="preconnect" href="https://fonts.gstatic.com">` hint remains in the head —
  inert (all fonts are local), harmless to leave.
