#!/usr/bin/env python3
"""Write the numbers in data/metrics.json into the 'By the numbers' tiles of index.html.

Usage:
    python3 scripts/sync_numbers.py          # show what would change (default, changes nothing)
    python3 scripts/sync_numbers.py --apply  # write the changes, then run check_consistency.py

Scope: the ten tiles of the landing page ({n:380,suffix:'+',label:'Scientific publications'} and so on).
The OpenAlex figures on research.html are written by scripts/refresh_openalex.py; other page text
is still changed with scripts/site_text.py. Values like "10k+" become n:10 and suffix 'k+'.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_text

ROOT = site_text.ROOT
m = json.load(open(os.path.join(ROOT, "data", "metrics.json"), encoding="utf-8"))
sc, pe = m["scopus"], m["people"]

# tile label -> value from metrics.json
TILES = {
    "Scientific publications": sc["publications"],
    "Citations": sc["citations"],
    "h-index": sc["h_index"],
    "Co-authors": sc["coauthors"],
    "Journal articles": sc["journal_articles"],
    "Conference papers": sc["conference_papers"],
    "Book chapters": sc["book_chapters"],
    "Books published": sc["books"],
    "Institution collaborations": pe["partner_institutions"],
    "Countries": pe["partner_countries"],
}


def split(value):
    mm = re.fullmatch(r"(\d+)(.*)", str(value))
    return mm.group(1), mm.group(2)


def main():
    apply = "--apply" in sys.argv
    path, html, tag, t = site_text.load("index.html")
    changes = 0
    for label, value in TILES.items():
        n, suffix = split(value)
        pat = re.compile(r"\{n:(\d+),suffix:'([^']*)',label:'" + re.escape(label) + r"'")
        found = pat.search(t)
        if not found:
            print(f"MISSING tile '{label}' on index.html")
            continue
        if (found.group(1), found.group(2)) == (n, suffix):
            continue
        changes += 1
        print(f"{label}: page {found.group(1)}{found.group(2)} -> metrics.json {n}{suffix}")
        new = f"{{n:{n},suffix:'{suffix}',label:'{label}'"
        t = t[:found.start()] + new + t[found.end():]
    if not changes:
        print("index.html tiles already match metrics.json")
        return
    if apply:
        site_text.save(path, html, tag, t)
        print(f"{changes} tile(s) written. Now run: python3 scripts/check_consistency.py")
    else:
        print(f"{changes} tile(s) differ. Run with --apply to write them.")


if __name__ == "__main__":
    main()
