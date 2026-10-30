#!/usr/bin/env python3
"""Refresh the 'openalex' block of data/metrics.json from the OpenAlex API.

Usage:
    python3 scripts/refresh_openalex.py            # update data/metrics.json in place
    python3 scripts/refresh_openalex.py --dry-run  # print what would change, write nothing

Only the "openalex" block is touched. Scopus, Scholar, people and teaching
figures are typed in by hand and are never overwritten.

Needs only the Python standard library. OpenAlex is free and needs no key;
set OPENALEX_MAILTO=you@example.com to be put in their polite pool.
"""
import json, os, sys, time, urllib.request, urllib.parse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS = os.path.join(ROOT, "data", "metrics.json")
PROFILE = os.path.join(ROOT, "data", "profile.json")
PEOPLE = os.path.join(ROOT, "data", "people.json")
BASE = "https://api.openalex.org"


def get(path, params):
    mailto = os.environ.get("OPENALEX_MAILTO")
    if mailto:
        params = dict(params, mailto=mailto)
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # rate limit or hiccup: back off and retry
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def short_name(display_name):
    parts = display_name.split()
    if len(parts) == 1:
        return display_name
    return f"{parts[0][0]}. {parts[-1]}"


def main():
    dry = "--dry-run" in sys.argv
    metrics = json.load(open(METRICS))
    profile = json.load(open(PROFILE))
    people = json.load(open(PEOPLE))
    author_id = profile["openalex_author_id"]
    from_year = metrics["openalex"].get("tum_era", {}).get("from_year", 2016)
    this_year = datetime.date.today().year
    filt = f"authorships.author.id:{author_id}"
    era = f"{filt},publication_year:{from_year}-{this_year}"

    author = get(f"/authors/{author_id}", {})
    by_year = {c["year"]: c for c in author.get("counts_by_year", [])}
    years = [{"year": y, "works": by_year.get(y, {}).get("works_count", 0),
              "citations": by_year.get(y, {}).get("cited_by_count", 0)}
             for y in range(from_year, this_year + 1)]

    era_total = get("/works", {"filter": era, "per_page": 1})["meta"]["count"]
    era_cites = sum(y["citations"] for y in years)
    over100 = get("/works", {"filter": era + ",cited_by_count:>99", "per_page": 1})["meta"]["count"]
    oa = get("/works", {"filter": era, "group_by": "open_access.is_oa"})["group_by"]
    oa_true = next((g["count"] for g in oa if g["key"] == "1"), 0)

    top = get("/works", {"filter": era, "sort": "cited_by_count:desc", "per_page": 12,
                         "select": "title,publication_year,cited_by_count,doi,authorships"})["results"]
    tse_names = {a["name"].split(". ")[-1].split()[-1].lower() for a in people["team"] + people["alumni"]}
    top_papers = []
    for w in top:
        first = next((a for a in w["authorships"] if a["author_position"] == "first"), None)
        fa = first["author"]["display_name"] if first else ""
        top_papers.append({"title": w["title"], "first_author": short_name(fa), "year": w["publication_year"],
                           "citations": w["cited_by_count"], "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                           "tse": fa.split()[-1].lower() in tse_names if fa else False})

    inst = get("/works", {"filter": era, "group_by": "authorships.institutions.id", "per_page": 16})["group_by"]
    alumni_hosts = {a["where"].lower() for a in people["alumni"] if a.get("where")}
    partners = []
    for g in inst:
        name = g["key_display_name"]
        if "Technical University of Munich" in name:
            continue
        partners.append({"institution": name, "works": g["count"],
                         "alumni_host": any(h and (h in name.lower() or name.lower() in h) for h in alumni_hosts)})
    countries = get("/works", {"filter": era, "group_by": "authorships.institutions.country_code", "per_page": 100})["meta"]["groups_count"]

    new = {
        "as_of": datetime.date.today().isoformat(),
        "author_id": author_id,
        "works_count": author["works_count"],
        "cited_by_count": author["cited_by_count"],
        "h_index": author["summary_stats"]["h_index"],
        "i10_index": author["summary_stats"]["i10_index"],
        "tum_era": {"from_year": from_year, "works": era_total, "citations": era_cites,
                    "works_over_100_citations": over100, "open_access_share": round(oa_true / max(era_total, 1), 2)},
        "by_year": years,
        "top_papers": top_papers,
        "partners_since_2016": partners[:14],
        "countries_since_2016": countries,
    }

    old = metrics["openalex"]
    print(f"OpenAlex {old.get('as_of')} -> {new['as_of']}")
    for k in ("works_count", "cited_by_count", "h_index", "i10_index"):
        print(f"  {k:16} {old.get(k)} -> {new[k]}")
    print(f"  tum_era.works    {old.get('tum_era', {}).get('works')} -> {era_total}")
    print(f"  tum_era.cites    {old.get('tum_era', {}).get('citations')} -> {era_cites}")
    if dry:
        print("dry run: nothing written")
        return
    metrics["openalex"] = new
    metrics["as_of"] = new["as_of"]
    json.dump(metrics, open(METRICS, "w"), indent=2, ensure_ascii=False)
    open(METRICS, "a").write("\n")
    print(f"wrote {METRICS}")


if __name__ == "__main__":
    main()
