# Antoniou portfolio site — guide for Claude

This repository is the public research portfolio of Prof. Dr. Constantinos Antoniou and the Chair of Transportation Systems Engineering (TSE) at TUM, published with GitHub Pages at the domain in `CNAME`. The person asking you for changes is usually the professor himself. Keep replies short and do the work.

## Where things live

| Path | What it is | How to change it |
|---|---|---|
| `index.html` | Landing page (hero, career, honours, "By the numbers", roles, team) | text and numbers: `scripts/site_text.py`; layout: re-export from `design/` |
| `projects.html` | Funded projects page with funder logos | same |
| `research.html` | "Research in Numbers" data portrait (bibliometrics, co-author map) | same |
| `anniversary/index.html` | The ten-year anniversary presentation, 2026 snapshot (self-contained) | rarely; by hand |
| `help/index.html` | The professor's own task guide (sentences to copy) | keep in step with the skills |
| `data/*.json` | **The fact sheet**: profile, metrics, projects, people, timeline. Every number on the site must agree with it | hand; `metrics.openalex` by script only |
| `scripts/site_text.py` | Safe find/replace inside the three site pages (`find`, `replace`, `dump`) | run, don't edit |
| `scripts/refresh_openalex.py` | Pulls fresh OpenAlex figures into `data/metrics.json` | run, don't edit |
| `scripts/check_consistency.py` | Checks the JSON files against each other **and** against the numbers shown on the pages | run before every deploy |
| `design/*.dc.html`, `design/sources/` | The Claude Design source files the pages were exported from, and the raw material (CV text, bibliometrics) | only for redesigns |
| `assets/` | Funder logos, TUM logo | add files, don't rename |
| `.image-slots.state.json` | Which photo sits in which image slot on the landing page (`{}` = placeholders) | via the image-slot UI or by hand |
| `.claude/skills/*` | Procedures: `onboard`, `update-portfolio`, `refresh-bibliometrics`, `deploy-site`, `check-consistency` | — |
| `START-HERE.md`, `MAINTAINING.md` | The professor's own instructions | — |

## How the pages are built (important)

`index.html`, `projects.html` and `research.html` are exports from Claude Design. Each one stores the real page as a JSON string inside `<script type="__bundler/template">`. An ordinary text editor search will not find page text reliably, and editing the string by hand breaks the escaping. **Always use `python3 scripts/site_text.py find "…"` then `replace "old" "new"`**, which handles this. To read a page's full HTML, `python3 scripts/site_text.py dump index.html`.

The pages do not read `data/` at runtime. The JSON is the fact sheet you keep in step with the pages, and the checker verifies the two agree.

## First session

If this folder is not yet a git repository (`git rev-parse --is-inside-work-tree` fails) or has no GitHub remote, the professor is starting from scratch: follow the `onboard` skill before anything else, and point him to `START-HERE.md`.

## Rules that always apply

1. **Every change goes to two places:** the page (via `site_text.py`) and the matching field in `data/`. The checker will tell you if you forgot one.
2. **Never invent a figure.** If a number is not in `data/`, in a source the professor gave you, or in the OpenAlex script output, ask for it.
3. **Precedence when sources disagree:** the professor's own statement > the chair's magazine or profile page > Scopus > OpenAlex. OpenAlex counts preprints and reports, so its totals run higher than Scopus; the site labels which database each number comes from, and so must you.
4. **Run `python3 scripts/check_consistency.py` after every change** and fix anything it flags before deploying.
5. **Dates:** update the `as_of` field of any data file you change to today's date (YYYY-MM-DD).
6. **People:** use names and positions exactly as given; never guess where someone works now.
7. **Style:** short sentences, no superlatives you cannot back with a number. Match the wording already on the page.
8. **Do not touch** `.github/workflows`, `CNAME`, `.nojekyll` or `design/` unless the task is about deployment or a redesign.

## Typical requests and what to do

- "AgiMo got extended to 2030" → `site_text.py find "AgiMo"` to see how the end year is written on projects.html, `replace` it, edit `end` in `data/projects.json`, update `as_of`, run the checker.
- "New Scopus numbers: 395 publications, h 54" → `replace "{n:380,suffix:'+',label:'Scientific publications'" "{n:395,…"` on index.html, edit `data/metrics.json` `scopus`, run the checker.
- "Add a new PhD student, Maria Example" → if the page lists the team, `find` a current team member to see the format and add her next to them; append to `data/people.json` `team`, bump the `people` counts in `metrics.json`.
- "Refresh the publication numbers" → `refresh-bibliometrics` skill (script, review diff, update research.html counters, commit).
- "Change the photo in the hero" → open the landing page locally, use the image-slot picker in the hero (it writes `.image-slots.state.json`), or ask for the file and put it in `assets/`.
- "The layout should change / add a section" → that is a redesign: open the matching `design/*.dc.html` in Claude Design, edit, export, and replace the page file (keep the `<title>` and the footer link to `anniversary/`).
- "Publish the changes" → `deploy-site` skill.

## Local preview

`python3 -m http.server 8000` in the repository folder, then open http://localhost:8000 (also `/projects.html`, `/research.html`, `/anniversary/`, `/help/`). The research page loads a world map from a CDN; it needs internet.
