#!/usr/bin/env python3
"""Find or replace text inside the bundled site pages (index.html, projects.html, research.html).

The pages are exports from Claude Design: the real page is stored as a JSON string inside a
<script type="__bundler/template"> tag, so an ordinary editor search either misses it or
breaks the escaping. This tool does it safely.

Usage:
    python3 scripts/site_text.py find "15+ doctorates"
    python3 scripts/site_text.py replace "15+ doctorates" "16+ doctorates"
    python3 scripts/site_text.py replace "15+ doctorates" "16+ doctorates" --page index.html
    python3 scripts/site_text.py dump index.html > /tmp/index-template.html   # read the page's HTML

'find' prints every occurrence with context. 'replace' refuses to run when the text is
not found, and reports how many places changed per page. Always run 'find' first.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "projects.html", "research.html"]
TAG = re.compile(r'(<script type="__bundler/template">)(.*?)(</script>)', re.S)


def load(page):
    path = os.path.join(ROOT, page)
    html = open(path, encoding="utf-8").read()
    m = TAG.search(html)
    if not m:
        return path, html, None, None
    return path, html, m, json.loads(m.group(2))


def save(path, html, m, template):
    body = json.dumps(template, ensure_ascii=False).replace("</", "<\\/")  # keep </script> from closing the tag early
    new = html[: m.start(2)] + body + html[m.end(2):]
    open(path, "w", encoding="utf-8").write(new)


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    cmd = sys.argv[1]
    pages = PAGES
    if "--page" in sys.argv:
        i = sys.argv.index("--page"); pages = [sys.argv[i + 1]]; del sys.argv[i:i + 2]
    if cmd == "dump":
        _, _, _, t = load(sys.argv[2]); print(t); return
    needle = sys.argv[2]
    total = 0
    for page in pages:
        path, html, m, t = load(page)
        if t is None:
            continue
        hits = [x.start() for x in re.finditer(re.escape(needle), t)]
        if cmd == "find":
            for h in hits:
                ctx = re.sub(r"\s+", " ", t[max(0, h - 70): h + len(needle) + 70])
                print(f"{page}: …{ctx}…")
        elif cmd == "replace":
            if len(sys.argv) < 4:
                print("replace needs OLD and NEW"); sys.exit(2)
            if hits:
                t = t.replace(needle, sys.argv[3]); save(path, html, m, t)
                print(f"{page}: {len(hits)} replaced")
        total += len(hits)
    if total == 0:
        print(f"not found: {needle!r}"); sys.exit(1)
    if cmd == "find":
        print(f"{total} occurrence(s)")


if __name__ == "__main__":
    main()
