# TSE portfolio site — guide for Claude

This repository is the public research portfolio of Prof. Dr. Constantinos Antoniou and the Chair of Transportation Systems Engineering (TSE) at TUM, published with GitHub Pages. The person asking you for changes is usually the professor himself. Keep replies short and do the work.

## Where things live

| Path | What it is | Who edits it |
|---|---|---|
| `data/profile.json` | Name, bio, roles, career, honours, next-decade directions, contact | hand |
| `data/metrics.json` | Headline numbers. `scopus` and `scholar` blocks are typed in from the profile pages; `people` and `teaching` are the chair's own counts; `openalex` is **written by the script only** | hand + script |
| `data/projects.json` | One entry per funded project, plus the active TUM funding shares | hand |
| `data/people.json` | Team today, alumni with current positions, visiting professors, industry partners | hand |
| `data/timeline.json` | Milestones and conferences organised | hand |
| `index.html`, `assets/site.js`, `assets/site.css` | The landing page; it renders everything from the JSON at load time | only for design changes |
| `anniversary/index.html` | The ten-year anniversary presentation (self-contained; numbers are embedded, so update it by hand or leave it as a 2026 snapshot) | rarely |
| `scripts/refresh_openalex.py` | Pulls fresh OpenAlex figures into `metrics.json` | run, don't edit |
| `scripts/check_consistency.py` | Checks that the numbers in the JSON files agree with each other | run before every deploy |
| `.claude/skills/*` | The procedures below, as skills (`onboard`, `update-portfolio`, `refresh-bibliometrics`, `deploy-site`, `check-consistency`) | — |
| `START-HERE.md`, `MAINTAINING.md` | The professor's own instructions | — |
| `help/index.html` | The professor's own task guide; keep its example sentences in step with the skills if a procedure changes | rarely |

## First session

If this folder is not yet a git repository (`git rev-parse --is-inside-work-tree` fails) or has no GitHub remote, the professor is starting from scratch: follow the `onboard` skill before anything else, and point him to `START-HERE.md`.

## Rules that always apply

1. **Data files are the single source of truth.** To change what the site says, change the JSON. Never hard-code a number into HTML or JS.
2. **Never invent a figure.** If a number is not in the JSON, in a source the professor gave you, or in the OpenAlex script output, ask for it. Leave a field empty rather than estimate.
3. **Precedence when sources disagree:** the professor's own statement > the chair's magazine or profile page > Scopus > OpenAlex. OpenAlex counts preprints and reports, so its totals run higher than Scopus; the site labels which database each number comes from, and so must you.
4. **Run `python3 scripts/check_consistency.py` after every data change** and fix anything it flags before deploying.
5. **Dates:** update the `as_of` field of any file you change to today's date (YYYY-MM-DD).
6. **People:** use the names and positions exactly as given; never guess where someone works now.
7. **Style:** the site is in the chair's voice ("we"). Short sentences. No superlatives you cannot back with a number.
8. **Do not touch** `.github/workflows`, `CNAME` or `.nojekyll` unless the task is about deployment.

## Typical requests and what to do

- "AgiMo got extended to 2030" → edit the project's `end` in `projects.json`, update `as_of`, run the checker.
- "Add a new PhD student, Maria Example" → append to `people.json` `team` with `type: doctoral`, bump `people.researchers_today` and `doctoral_researchers` in `metrics.json` (the checker will catch a mismatch), update both `as_of`.
- "Hao Wu moved to Tsinghua as Associate Professor" → edit his alumni entry (`now`, `where`); if `kind` changes, re-check `alumni_in_faculty_positions`.
- "Refresh the publication numbers" → use the `refresh-bibliometrics` skill (script, review diff, commit).
- "We organised a new conference" → add to `timeline.json` `conferences_organised` and an `events` entry; update the anniversary deck only if asked.
- "Publish the changes" → use the `deploy-site` skill.
- "New Scopus numbers: 395 publications, h 54" → edit `metrics.scopus` and its `as_of` by hand.

## Local preview

`python3 -m http.server 8000` in the repository folder, then open http://localhost:8000. Opening `index.html` straight from disk will not load the JSON.
