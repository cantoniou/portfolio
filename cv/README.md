# CV builds

One master, many CV versions. All content comes from `../data/` (`cv.json`, `metrics.json`, `projects.json`);
nothing is typed here. Numbers in `cv.json` are tokens such as `{metrics.scopus.publications}`
(see `../scripts/cv_tokens.py`).

| Path | What it is |
|---|---|
| `variants/*.yaml` | One file per CV version: layout, output name, spacing knobs. |
| `templates/*.tex.j2` | Layouts (XeLaTeX, Inter font, TUM blue #0065BD). No content. |
| `docx/onepager.js` | Word version of the one-pager (docx-js, Calibri). Same content. |
| `assets/CV_photo_circle.png` | Circular crop of `../assets/profile.jpg`. |
| `out/` | Built PDFs and Word files. Git-ignored: they are delivered to Costa, not published. |
| `data/private.yaml` | Fields kept out of this public repo (nationality). Git-ignored. Or set `CV_PRIVATE=<path>`. |

Build: `python3 cv/build.py` (all versions) or `python3 cv/build.py onepager`.
Needs xelatex (texlive-xetex, texlive-latex-extra, texlive-fonts-recommended), the Inter font,
python3 jinja2 and pyyaml, and node with the `docx` package (`NODE_PATH`).
The one-pager must stay exactly one A4 page; `build.py` prints the page count.

New version (funder CV, AI-focused one-pager, ...): copy a `variants/` file, point it to a template,
and put any version-specific text in `../data/cv.json`. Run `python3 scripts/check_consistency.py` first.
