# Start here

This folder is your research portfolio website, plus everything Claude needs to keep it current for you. You will not need to edit code. Three steps get it online; after that, every change is one sentence to Claude.

## 1. Put the folder somewhere permanent

Move this folder out of Downloads to a place it will stay, for example `Documents/portfolio`. Claude always works on this same folder, so it should not move again.

## 2. Open it in Claude

Either:

- **Claude desktop app → Cowork:** start a new task, click *Add folder*, choose this folder. Or
- **Terminal:** `cd` into the folder and type `claude`.

Claude reads `CLAUDE.md` and the skills in `.claude/skills/` by itself. You do not have to point it at anything.

## 3. Say this

> Onboard me: set up this portfolio from scratch.

Claude will check what already exists, then walk you through, one step at a time: turning the folder into a git repository, connecting it to your GitHub repository (github.com/cantoniou/portfolio), switching on GitHub Pages, pointing your domain at it (you type a few records at your domain registrar; Claude tells you exactly which), and a first test change so you see the whole loop work. Budget 20 minutes. One moment needs you at a browser: the DNS records (and a GitHub login the first time you push); Claude cannot log in for you.

## From then on

Open the folder in Claude and say what happened:

- "Add a new doctoral researcher, M.Sc. Anna Beispiel, started in October."
- "AgiMo was extended to 2030."
- "My new Scopus numbers: 395 publications, h-index 54."
- "Put this photo in the hero."
- "Refresh the publication numbers."
- "Publish."

The complete list of situations, with sentences to copy, is in `help/index.html` (open it in a browser, or at `/help/` on your live site). `MAINTAINING.md` has the same in text.

## What you need

- A Claude plan with Cowork or Claude Code
- A GitHub account (free)
- Access to the DNS settings of your domain, once
- A Mac or Linux machine with git and Python 3 (both already on macOS); on Windows, install Git for Windows and Python 3 first

## If you get stuck

Say "I'm stuck" and describe what you see. Claude can read every file here and knows the procedures. Nothing you say to Claude goes online until you say "publish".
