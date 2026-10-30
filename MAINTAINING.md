# Keeping the portfolio up to date

Prefer pictures? The same guide as a page with copy-paste sentences: `help/index.html` (also live at `/help/` once published).

This folder is your research portfolio website. Everything the site shows comes from five small text files in `data/`. You never need to touch the HTML. Claude knows this repository: open the folder in Claude (Cowork with the folder added, or Claude Code in a terminal) and say what changed, in plain words.

## The five-minute version

1. Open the repository folder in Claude.
2. Tell Claude what changed. Examples that work well:
   - "Add a new doctoral researcher, M.Sc. Anna Beispiel, who started in October."
   - "Mohamed Abouelela has left; he is now Assistant Professor at Cairo University."
   - "We received a new DFG project, TRAFFIC-X, 2027 to 2030, I'm PI, on … "
   - "AgiMo has been extended to 2030."
   - "I was appointed to the editorial board of Transportation Science."
   - "Here are my new Scopus numbers: 395 publications, h-index 54, 11k citations."
   - "Refresh the publication numbers." (Claude runs the OpenAlex script and shows you what moved.)
   - "Check the site for anything inconsistent."
   - "Publish." (Claude runs the checks, commits and pushes; the site is live a minute later.)
3. Claude edits the data files, runs the consistency check, and tells you what it did. Nothing is public until you say "publish".

## What is where

| You want to change… | File |
|---|---|
| Your bio, roles, career, honours, contact, next-decade themes | `data/profile.json` |
| Headline numbers (Scopus, Scholar, people counts, courses) | `data/metrics.json` |
| Projects and the active funding figures | `data/projects.json` |
| Team, alumni and their current positions, visiting professors | `data/people.json` |
| Milestones and conferences organised | `data/timeline.json` |

The files are plain text; you can also edit them yourself in any editor. Keep the quotes and commas as they are.

## Three sources of numbers, and which to trust

- **Scopus and Google Scholar**: your career totals. You read them from your profile and tell Claude; nobody can fetch them automatically.
- **OpenAlex**: free, open, scriptable. It drives the charts (works per year, most-cited papers, partner institutions). It counts preprints and reports too, so its totals are higher than Scopus. The site always says which database a number comes from.
- **Your own records**: team, alumni, projects, funding. These are the ones only you can keep right, and the ones visitors notice first.

## Rhythms that keep it current

- **Each semester** (October, April): team changes, new projects, anyone who graduated. Ten minutes.
- **Each quarter**: "Refresh the publication numbers." Or let the monthly GitHub action do it and merge the pull request it opens.
- **When something happens**: an honour, a conference, a big paper. One sentence to Claude, one line on the timeline.
- **Before a talk or evaluation**: "Check the site for anything inconsistent."

## Publishing and the domain

The site is served by GitHub Pages from this repository's `main` branch at your own domain. Setup steps (repository, Pages, DNS records) are in `.claude/skills/deploy-site/SKILL.md`; Claude can walk you through them once. After that, "publish" is all you need to say.

If something goes wrong on the live site, say "roll back the last deploy" and Claude will revert the last commit.

## The anniversary presentation

`anniversary/` holds the ten-year presentation from 2026 as a self-contained page (linked from the site menu as "Ten years"). Its numbers are frozen as of September 2026 on purpose; if you ever want it refreshed, ask Claude to update it and it will do so slide by slide.

## Files you should not need to touch

`index.html`, `assets/`, `scripts/`, `.github/`, `.claude/`, `CNAME`, `.nojekyll`. Claude will change them only for design or deployment work you ask for.
