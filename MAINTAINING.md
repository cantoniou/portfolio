# Keeping the portfolio up to date

Prefer pictures? The same guide as a page with copy-paste sentences: `help/index.html` (also live at `/help/` once published).

This folder is your research portfolio website: three pages (home, projects, research in numbers), the ten-year anniversary presentation, and a small fact sheet in `data/` that every number on the site is checked against. You never need to touch the HTML. Claude knows this repository: open the folder in Claude (Cowork with the folder added, or Claude Code in a terminal) and say what changed, in plain words.

## The five-minute version

1. Open the repository folder in Claude.
2. Tell Claude what changed. Examples that work well:
   - "Add a new doctoral researcher, M.Sc. Anna Beispiel, who started in October."
   - "Mohamed Abouelela has left; he is now Assistant Professor at Cairo University."
   - "We received a new DFG project, TRAFFIC-X, 2027 to 2030, I'm PI, on …"
   - "AgiMo has been extended to 2030."
   - "I was appointed to the editorial board of Transportation Science."
   - "Here are my new Scopus numbers: 395 publications, h-index 54, 11k citations."
   - "Put this photo in the hero carousel." (attach the photo)
   - "Refresh the publication numbers." (Claude runs the OpenAlex script, carries the figures onto the research page and shows you what moved.)
   - "Check the site for anything inconsistent."
   - "Publish." (Claude runs the checks, commits and pushes; the site is live a minute later.)
3. Claude changes the page text with a small tool that understands the page format, updates the fact sheet, runs the consistency check, and tells you what it did. Nothing is public until you say "publish".

## What is where

| You want to change… | Page | Fact sheet |
|---|---|---|
| Bio, career, honours, roles, headline numbers, team | `index.html` | `data/profile.json`, `data/metrics.json`, `data/people.json` |
| Projects, funders, funding figures | `projects.html` | `data/projects.json` |
| Bibliometrics: works per year, h-index, top papers, co-author map | `research.html` | `data/metrics.json` → `openalex` |
| Milestones, conferences organised | (anniversary deck) | `data/timeline.json` |

The pages come from Claude Design (`design/` has the source files). Small text and number changes are done in place by Claude; a new section or a new look means re-opening the design file, which Claude can also walk you through.

## Three sources of numbers, and which to trust

- **Scopus and Google Scholar**: your career totals. You read them from your profile and tell Claude; nobody can fetch them automatically.
- **OpenAlex**: free, open, scriptable. It drives the charts on the research page. It counts preprints and reports too, so its totals are higher than Scopus. The site always says which database a number comes from.
- **Your own records**: team, alumni, projects, funding. These are the ones only you can keep right, and the ones visitors notice first.

## Rhythms that keep it current

- **Each semester** (October, April): team changes, new projects, anyone who graduated. Ten minutes.
- **Each quarter**: "Refresh the publication numbers." Or let the monthly GitHub action do it and merge the pull request it opens.
- **When something happens**: an honour, a conference, a big paper. One sentence to Claude.
- **Before a talk or evaluation**: "Check the site for anything inconsistent."

## Publishing and the domain

The site is served by GitHub Pages from the `main` branch of https://github.com/cantoniou/portfolio at your own domain (`CNAME`). Setup steps (connecting the folder, Pages, DNS records) are in `.claude/skills/onboard/SKILL.md`; Claude walks you through them once. After that, "publish" is all you need to say.

If something goes wrong on the live site, say "roll back the last deploy" and Claude will revert the last commit.

## The anniversary presentation

`anniversary/` holds the ten-year presentation from 2026 as a self-contained page (linked from the site footer as "Ten years of TSE"). Its numbers are frozen as of September 2026 on purpose; if you ever want it refreshed, ask Claude and it will do so slide by slide.

## Files you should not need to touch

`assets/`, `scripts/`, `design/`, `.github/`, `.claude/`, `CNAME`, `.nojekyll`. Claude changes them only for design or deployment work you ask for.
