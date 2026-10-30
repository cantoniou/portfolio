# Constantinos Antoniou — research portfolio

Public portfolio of Prof. Dr. Constantinos Antoniou and the Chair of Transportation Systems Engineering (TSE), Technical University of Munich. Static site on GitHub Pages (https://github.com/cantoniou/portfolio → the domain in `CNAME`).

- `index.html`, `projects.html`, `research.html` — the site (Claude Design exports; sources in `design/`)
- `anniversary/` — the ten-year anniversary presentation (2026)
- `help/` — what to say to Claude for each maintenance task
- `data/` — the fact sheet every number on the site is checked against
- `scripts/site_text.py` — find/replace text inside the pages safely
- `scripts/refresh_openalex.py` — refresh bibliometrics from OpenAlex
- `scripts/check_consistency.py` — verify pages and data agree (run before publishing)

**New here?** Read `START-HERE.md`, then open the folder in Claude and say "Onboard me". **Updating content?** `MAINTAINING.md`, or just describe the change to Claude. **Preview locally:** `python3 -m http.server 8000` → http://localhost:8000.

Claude skills for these tasks are in `.claude/skills/` and load automatically when the repository is opened in Claude.
