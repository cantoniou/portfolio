#!/usr/bin/env python3
"""Check that the numbers in data/*.json agree with each other.

Usage:  python3 scripts/check_consistency.py
Exit code 0 = all good, 1 = something to fix. Run it before every deploy.
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda n: json.load(open(os.path.join(ROOT, "data", n)))
problems, notes = [], []


def check(cond, msg):
    (notes if cond else problems).append(("ok  " if cond else "FIX ") + msg)


metrics, projects, people, timeline, profile = D("metrics.json"), D("projects.json"), D("people.json"), D("timeline.json"), D("profile.json")
year = datetime.date.today().year

# People counts vs lists
team = people["team"]
n = lambda t: sum(1 for p in team if p["type"] == t)
pm = metrics["people"]
check(pm["postdocs"] == n("postdoc"), f"postdocs: metrics {pm['postdocs']} vs people.json {n('postdoc')}")
check(pm["doctoral_researchers"] == n("doctoral") + n("external"), f"doctoral researchers (incl. external): metrics {pm['doctoral_researchers']} vs people.json {n('doctoral') + n('external')}")
check(pm["external_doctoral_candidates"] == n("external"), f"external candidates: metrics {pm['external_doctoral_candidates']} vs people.json {n('external')}")
check(pm["researchers_today"] == n("postdoc") + n("doctoral") + n("external"), f"researchers today: metrics {pm['researchers_today']} vs people.json {n('postdoc') + n('doctoral') + n('external')}")
check(pm["alumni"] == len(people["alumni"]), f"alumni: metrics {pm['alumni']} vs people.json {len(people['alumni'])}")
fac = sum(1 for a in people["alumni"] if a["kind"] == "faculty")
check(pm["alumni_in_faculty_positions"] == fac, f"alumni in faculty positions: metrics {pm['alumni_in_faculty_positions']} vs people.json {fac}")
check(pm["visiting_professors"] == len(people["visiting_professors"]), f"visiting professors: metrics {pm['visiting_professors']} vs list {len(people['visiting_professors'])}")

# Projects
P = projects["projects"]
groups = ["EU", "DFG", "German ministries", "TUM IGSSE", "DAAD", "Other"]
for p in P:
    check(p["funder_group"] in groups, f"{p['name']}: funder_group '{p['funder_group']}' must be one of {groups}")
    check(p["start"] <= p["end"], f"{p['name']}: start {p['start']} after end {p['end']}")
ids = [p["id"] for p in P]
check(len(ids) == len(set(ids)), "project ids are unique")
ongoing = [p for p in P if p.get("status", "ongoing" if p["end"] >= year else "finished") == "ongoing"]
ov = projects.get("funder_counts_override")
if ov:
    ov = {k: v for k, v in ov.items() if not k.startswith("_")}
    tot = sum(v["ongoing"] + v["finished"] for v in ov.values())
    on = sum(v["ongoing"] for v in ov.values())
    notes.append(f"note funder_counts_override in use: {tot} projects, {on} ongoing (list names {len(P)}, {len(ongoing)} ongoing)")
    check(tot >= len(P), f"override total {tot} is not below the number of listed projects {len(P)}")
else:
    notes.append(f"note {len(P)} projects listed, {len(ongoing)} ongoing (computed from end years)")
af = projects["active_funding_tum_share_eur"]
notes.append(f"note active TUM share: EUR {sum(af.values()):,}")

# Metrics by_year vs tum_era
ox = metrics["openalex"]
by = ox["by_year"]
check(sum(y["works"] for y in by) in (ox["tum_era"]["works"], ox["tum_era"]["works"] - 1, ox["tum_era"]["works"] + 1), f"by_year works sum {sum(y['works'] for y in by)} vs tum_era.works {ox['tum_era']['works']} (one off is normal: undated works)")
check(sum(y["citations"] for y in by) == ox["tum_era"]["citations"], f"by_year citations sum {sum(y['citations'] for y in by)} vs tum_era.citations {ox['tum_era']['citations']}")
check(len([p for p in ox["top_papers"] if p["citations"] >= 100]) == ox["tum_era"]["works_over_100_citations"], f"top_papers with >=100 citations {len([p for p in ox['top_papers'] if p['citations'] >= 100])} vs works_over_100_citations {ox['tum_era']['works_over_100_citations']}")
check(by[-1]["year"] >= year - 1, f"by_year ends at {by[-1]['year']}; run scripts/refresh_openalex.py")

# Staleness
for label, d in (("metrics", metrics["as_of"]), ("projects", projects["as_of"]), ("people", people["as_of"])):
    age = (datetime.date.today() - datetime.date.fromisoformat(d)).days
    check(age < 200, f"{label}.json as_of {d} is {age} days old")

# Timeline sanity
dates = [e["date"] for e in timeline["events"]]
check(all(len(x) == 10 for x in dates), "timeline dates are YYYY-MM-DD")
check(len(timeline["conferences_organised"]) == len({c["name"] for c in timeline["conferences_organised"]}), "conference names unique")

# Honours chronology
hy = [h["year"] for h in profile["honours"]]
check(hy == sorted(hy, reverse=True), "honours listed newest first")


# Site pages vs data (the pages embed their numbers; data/ is the fact sheet)
import re as _re
def page_text(name):
    try:
        html = open(os.path.join(ROOT, name), encoding="utf-8").read()
        m = _re.search(r'<script type="__bundler/template">(.*?)</script>', html, _re.S)
        return _re.sub(r"<[^>]+>", " ", json.loads(m.group(1))) if m else html
    except FileNotFoundError:
        return ""
idx, res = page_text("index.html"), page_text("research.html")
sc = metrics["scopus"]
# index.html stores its counters as {n:380,suffix:'+'}; rebuild the "380+" form before comparing
tiles = {}
for m in _re.finditer(r"\{n:(\d+),suffix:'([^']*)',label:'([^']*)'", idx):
    tiles[m.group(3).lower()] = m.group(1) + m.group(2)
pairs = (("scientific publications", sc["publications"]), ("h-index", str(sc["h_index"])), ("citations", sc["citations"]),
         ("co-authors", sc["coauthors"]), ("journal articles", sc["journal_articles"]), ("conference papers", sc["conference_papers"]),
         ("book chapters", sc["book_chapters"]))
for label, val in pairs:
    found = next((v for k, v in tiles.items() if label in k), None)
    check(found == str(val), f"index.html 'By the numbers' {label}: page {found} vs metrics.json {val}")
check(str(pm["doctorates_completed"]) in idx, f"doctorates completed {pm['doctorates_completed']} appears on index.html")
check(str(pm["theses_supervised"]) in idx, f"theses supervised {pm['theses_supervised']} appears on index.html")
if res:
    check(str(ox["h_index"]) in res, f"OpenAlex h-index {ox['h_index']} appears on research.html")
    check(str(ox["tum_era"]["works"]) in res or str(ox["tum_era"]["works"] - 1) in res, f"TUM-era works {ox['tum_era']['works']} appears on research.html")
for h in profile["honours"][:3]:
    check(h["what"].split(",")[0] in idx, f"honour '{h['what']}' appears on index.html")

oks = [l for l in notes if l.startswith("ok")]
for line in [l for l in notes if not l.startswith("ok")] + problems:
    print(line)
print(f"\n{len(oks)} check(s) passed, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)
