#!/usr/bin/env python3
"""Builds people.html from data/people.json (current postdocs, current doctoral researchers, alumni).
Plain HTML, not a Claude Design export. Run: python3 scripts/build_people.py"""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "data", "people.json"), encoding="utf-8"))
e = html.escape
team, alumni = d["team"], d["alumni"]
postdocs = [p for p in team if p["type"] == "postdoc"]
phds = [p for p in team if p["type"] == "doctoral"]
ext = [p for p in team if p["type"] == "external"]
KINDS = [("faculty", "Academia: faculty"), ("research", "Academia: research"), ("industry", "Industry"), ("public", "Public sector")]

def person(name, line1="", line2="", url=""):
    nm = f'<a href="{e(url, quote=True)}" target="_blank" rel="noopener">{e(name)}</a>' if url else e(name)
    a = f'<div class="n">{nm}</div>'
    if line1: a += f'<div class="r">{e(line1)}</div>'
    if line2: a += f'<div class="w">{e(line2)}</div>'
    return f'<li>{a}</li>'

def block(num, title, intro, items, dark=False):
    cls = "dark" if dark else "light"
    return f'''<section class="{cls}"><div class="wrap">
<div class="eyebrow">/ {num} — {e(title)}</div>
<p class="intro">{e(intro)}</p>
{items}
</div></section>'''

pd = "<ul class='grid'>" + "".join(person(p["name"], p.get("role", ""), url=p.get("url", "")) for p in postdocs) + "</ul>"
ph = "<ul class='grid'>" + "".join(person(p["name"], p.get("note", ""), url=p.get("url", "")) for p in phds) + "</ul>"
if ext:
    ph += "<h3>External doctoral candidates</h3><ul class='grid'>" + "".join(person(p["name"], p.get("employer", "")) for p in ext) + "</ul>"
al = ""
for k, label in KINDS:
    rows = [a for a in alumni if a["kind"] == k]
    if rows:
        al += f"<h3>{e(label)}</h3><ul class='grid'>" + "".join(person(a["name"], a.get("now", ""), a.get("where", ""), a.get("url", "")) for a in rows) + "</ul>"

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>People · Constantinos Antoniou</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}}
body{{background:#f5f3ee;color:#16161d;font-family:'Space Grotesk',system-ui,sans-serif;overflow-x:hidden}}
a{{color:#16161d;text-decoration:none}} a:hover{{color:#3070B3}}
header{{position:fixed;top:0;left:0;right:0;z-index:60;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:15px clamp(20px,5vw,56px);background:#16161d;color:#f5f3ee;border-bottom:1px solid rgba(245,243,238,.14)}}
header a{{color:inherit;font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase}}
header .brand{{letter-spacing:.18em}}
header nav{{display:flex;gap:clamp(14px,2.4vw,28px);align-items:center;flex-wrap:wrap}}
header nav a{{opacity:.62}} header nav a.on{{opacity:1;border-bottom:2px solid #3070B3;padding-bottom:3px}}
.hero{{padding:clamp(120px,18vh,180px) clamp(20px,5vw,56px) clamp(50px,8vh,80px)}}
.wrap{{max-width:1280px;margin:0 auto}}
.eyebrow{{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#3070B3;margin-bottom:clamp(14px,3vh,20px)}}
h1{{font-weight:600;letter-spacing:-.03em;line-height:.9;font-size:clamp(52px,11vw,160px)}}
.lead{{margin-top:clamp(20px,3.5vh,34px);font-size:clamp(16px,1.7vw,23px);max-width:680px;line-height:1.45;color:#57544d}}
section.light,section.dark{{padding:clamp(60px,10vh,120px) clamp(20px,5vw,56px)}}
section.dark{{background:#16161d;color:#f5f3ee}} section.dark .eyebrow{{color:#5aa6e6}}
.intro{{font-size:clamp(16px,1.6vw,22px);max-width:700px;line-height:1.45;margin-bottom:clamp(30px,5vh,48px);color:#57544d}}
section.dark .intro{{color:#cdd6e2}}
h3{{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:400;margin:clamp(30px,5vh,46px) 0 14px;opacity:.7}}
.grid{{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));padding:1px 0 0 1px}}
.grid li{{padding:18px 20px;border:1px solid rgba(22,22,29,.14);margin:-1px 0 0 -1px}} .dark .grid li{{border-color:rgba(245,243,238,.14)}}
.n{{font-size:17px;font-weight:600;letter-spacing:-.01em}} .n a{{border-bottom:1px solid rgba(48,112,179,.5)}} .dark .n a{{color:#f5f3ee}} .dark .n a:hover{{color:#5aa6e6}}
.r{{margin-top:4px;font-size:14px;color:#2c2b31;line-height:1.35}} .w{{font-size:14px;color:#57544d;line-height:1.35}}
.dark .r{{color:#cdd6e2}} .dark .w{{color:#8a97ab}}
footer{{padding:clamp(44px,8vh,80px) clamp(20px,5vw,56px);background:#16161d;color:#8a97ab}}
footer div{{max-width:1280px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase}}
footer a{{color:inherit}}
</style>
</head>
<body>
<header>
  <a class="brand" href="index.html">Constantinos Antoniou</a>
  <nav>
    <a href="index.html">Profile</a>
    <a class="on" href="#top">People</a>
    <a href="projects.html">Projects</a>
    <a href="research.html">Research in numbers</a>
  </nav>
</header>
<section class="hero" id="top"><div class="wrap">
  <div class="eyebrow">Chair of Transportation Systems Engineering · TUM</div>
  <h1>People</h1>
  <p class="lead">The current research team, and the former members who now work in academia, industry and the public sector.</p>
</div></section>
{block("01", "Postdoctoral researchers", f"{len(postdocs)} current postdocs.", pd)}
{block("02", "Doctoral researchers", f"{len(phds)} doctoral researchers at the chair" + (f", and {len(ext)} external doctoral candidates." if ext else "."), ph, dark=True)}
{block("03", "Alumni", f"{len(alumni)} former doctoral researchers and postdocs, with their current positions.", al)}
<footer><div>
  <span>Univ.-Prof. Dr. Constantinos Antoniou · TUM</span>
  <span>Chair of Transportation Systems Engineering · <a href="impressum.html">Impressum</a></span>
</div></footer>
</body>
</html>
'''
open(os.path.join(ROOT, "people.html"), "w", encoding="utf-8").write(page)
print(f"people.html: {len(postdocs)} postdocs, {len(phds)} doctoral, {len(ext)} external, {len(alumni)} alumni")
