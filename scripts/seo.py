#!/usr/bin/env python3
"""Write the search-engine tags into every public page, plus sitemap.xml and robots.txt.

What it adds (all generated from data/profile.json, so there is nothing to keep in step by hand):
  * meta description, canonical URL, Open Graph / social preview tags
  * structured data (schema.org Person + WebSite) so search engines know the site is about
    Constantinos Antoniou, his job, TUM and his ORCID / Scholar / Scopus / OpenAlex profiles
  * on index/projects/research (Claude Design exports): a short plain-HTML version of the
    page (name, position, bio, links) that crawlers can read without running JavaScript.
    Visitors never see it: the page covers it while unpacking and then replaces it.

Usage:
    python3 scripts/seo.py           # write everything (safe to run again; it replaces its own blocks)
    python3 scripts/seo.py --check   # exit 1 if any page is missing its block or is out of date

The blocks sit between <!-- seo:start --> and <!-- seo:end --> markers. In the exported pages
the head block is written twice: in the outer file (read by crawlers before JavaScript) and in
the bundled template (what the browser and Google end up showing). If a git merge conflicts on
the long template line of index/projects/research.html, take the other side and run this script
again.

To add a profile link (e.g. LinkedIn), add it to "links" in data/profile.json and run the script.
"""
import datetime, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_text  # noqa: E402

ROOT = site_text.ROOT
BASE = "https://antoniou.org/"  # matches CNAME (apex domain, HTTPS)
START, END = "<!-- seo:start -->", "<!-- seo:end -->"
BSTART, BEND = "<!-- seo-body:start -->", "<!-- seo-body:end -->"

P = json.load(open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8"))
NAME = "Constantinos Antoniou"
TAGLINE = "Modelling, simulating and optimising how people and goods move."

# path -> (canonical path, og:type, description, index?)
PAGES = {
    "index.html": ("", "profile",
        f"Prof. Dr. {NAME}, Full Professor and head of the Chair of Transportation Systems "
        f"Engineering at the Technical University of Munich (TUM). {TAGLINE}", True),
    "projects.html": ("projects.html", "website",
        f"Funded research projects of Prof. {NAME} and the Chair of Transportation Systems "
        "Engineering at TUM: European, DFG and other national projects.", True),
    "research.html": ("research.html", "website",
        f"Research in numbers: publications, citations, co-authors and topics of Prof. {NAME} "
        "(TUM), with figures from Scopus, OpenAlex and Google Scholar.", True),
    "people.html": ("people.html", "website",
        f"The team of the Chair of Transportation Systems Engineering at TUM, led by Prof. {NAME}.", True),
    "anniversary/index.html": ("anniversary/", "website",
        "Ten years of the Chair of Transportation Systems Engineering at TUM (2016 to 2026), "
        f"led by Prof. {NAME}.", True),
    "help/index.html": ("help/", "website", None, False),  # the professor's own guide: keep out of search
}
BUNDLED = set(site_text.PAGES)


def profile_links():
    links = [
        ("ORCID", f"https://orcid.org/{P['orcid']}"),
        ("Google Scholar", f"https://scholar.google.com/citations?user={P['google_scholar_id']}"),
        ("Scopus", f"https://www.scopus.com/authid/detail.uri?authorId={P['scopus_author_id']}"),
        ("OpenAlex", f"https://openalex.org/{P['openalex_author_id']}"),
        ("TUM Chair of Transportation Systems Engineering", P["website"].rstrip("/") + "/"),
    ]
    for label, url in (P.get("links") or {}).items():  # optional extra profiles, e.g. LinkedIn
        links.append((label, url))
    return links


def person():
    return {
        "@type": "Person",
        "@id": BASE + "#person",
        "name": NAME,
        "alternateName": [P["short_name"], "Prof. Dr. Constantinos Antoniou", "Costas Antoniou", "C. Antoniou"],
        "honorificPrefix": "Prof. Dr.",
        "givenName": "Constantinos",
        "familyName": "Antoniou",
        "jobTitle": "Full Professor, Chair of Transportation Systems Engineering",
        "description": P["bio"],
        "url": BASE,
        "image": BASE + "assets/profile.jpg",
        "email": "mailto:" + P["email"],
        "worksFor": {"@type": "CollegeOrUniversity", "name": "Technical University of Munich",
                     "alternateName": ["TUM", "Technische Universität München"], "url": "https://www.tum.de/"},
        "affiliation": {"@type": "Organization", "name": "Chair of Transportation Systems Engineering",
                        "alternateName": P["chair_name_de"], "url": P["website"].rstrip("/") + "/",
                        "parentOrganization": {"@type": "CollegeOrUniversity", "name": "Technical University of Munich"}},
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "Massachusetts Institute of Technology", "alternateName": "MIT"},
            {"@type": "CollegeOrUniversity", "name": "National Technical University of Athens", "alternateName": "NTUA"},
        ],
        "knowsAbout": ["Transportation systems engineering", "Traffic simulation and modelling",
                       "Model calibration and optimisation", "Road safety", "Driver behaviour",
                       "Traveller behaviour", "Machine learning for transport",
                       "Automated and electric mobility", "Freight and logistics"],
        "sameAs": [u for _, u in profile_links()],
    }


def jsonld(page, canon, desc):
    graph = [person(), {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": NAME,
                        "alternateName": f"Prof. Dr. {NAME}", "inLanguage": "en", "publisher": {"@id": BASE + "#person"}}]
    if page != "index.html":
        graph = [{"@type": "WebPage", "url": BASE + canon, "description": desc, "inLanguage": "en",
                  "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#person"}}] + graph
    else:
        graph.insert(0, {"@type": "ProfilePage", "url": BASE, "description": desc, "inLanguage": "en",
                         "isPartOf": {"@id": BASE + "#website"}, "mainEntity": {"@id": BASE + "#person"}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=None).replace("</", "<\\/")


def head_block(page, title):
    canon, ogtype, desc, index = PAGES[page]
    e = lambda s: html.escape(s, quote=True)
    if not index:
        return f'{START}\n<meta name="robots" content="noindex, follow">\n{END}'
    url = BASE + canon
    lines = [
        START,
        f'<meta name="description" content="{e(desc)}">',
        f'<meta name="author" content="{NAME}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="{ogtype}">',
        f'<meta property="og:site_name" content="{NAME}">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}assets/profile.jpg">',
        '<meta property="og:image:width" content="800">',
        '<meta property="og:image:height" content="1000">',
        f'<meta property="og:image:alt" content="Portrait of Prof. Dr. {NAME}">',
        '<meta property="og:locale" content="en_GB">',
    ]
    if ogtype == "profile":
        lines += ['<meta property="profile:first_name" content="Constantinos">',
                  '<meta property="profile:last_name" content="Antoniou">']
    lines += ['<meta name="twitter:card" content="summary">',
              f'<script type="application/ld+json">{jsonld(page, canon, desc)}</script>', END]
    return "\n".join(lines)


def body_block(page):
    e = html.escape
    nav = [("Profile", ""), ("People", "people.html"), ("Projects", "projects.html"), ("Research in numbers", "research.html")]
    out = [BSTART, '<main id="seo-text" style="max-width:640px;padding:24px;font:16px/1.5 system-ui,sans-serif;color:#16161d">',
           f"<h1>Prof. Dr. {NAME}</h1>",
           "<p>Full Professor and head of the Chair of Transportation Systems Engineering, "
           "TUM School of Engineering and Design, Technical University of Munich (TUM).</p>",
           f"<p>{e(TAGLINE)}</p>", f"<p>{e(P['bio'])}</p>",
           "<nav><ul>" + "".join(f'<li><a href="{BASE}{h}">{e(t)}</a></li>' for t, h in nav) + "</ul></nav>",
           "<p>Profiles: " + " · ".join(f'<a href="{u}">{e(l)}</a>' for l, u in profile_links()) + "</p>",
           f'<p>Contact: <a href="mailto:{P["email"]}">{P["email"]}</a> · <a href="{BASE}impressum.html">Impressum</a></p>',
           "</main>", BEND]
    return "\n".join(out)


def put(text, block, start, end, anchor_re, after=True):
    """Replace an existing marker block, or insert it at the first match of anchor_re."""
    old = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.S)
    if old.search(text):
        return old.sub(lambda _: block + "\n", text, count=1)
    m = re.search(anchor_re, text)
    if not m:
        raise SystemExit(f"anchor {anchor_re!r} not found")
    i = m.end() if after else m.start()
    if after and not text[:i].endswith("\n"):
        block = "\n" + block
    return text[:i] + block + "\n" + text[i:]


def title_of(text):
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    return html.unescape(m.group(1).strip())


def build_page(page):
    path = os.path.join(ROOT, page)
    src = open(path, encoding="utf-8").read()
    title = title_of(src)
    head = head_block(page, title)
    if page in BUNDLED:
        # outer file: head block after <title>, readable text after <body>
        out = put(src, head, START, END, r"<title>.*?</title>\n?")
        out = put(out, body_block(page), BSTART, BEND, r"<body>\n?")
        m = site_text.TAG.search(out)
        t = json.loads(m.group(2))
        t = put(t, head, START, END, r"</head>", after=False)
        t = re.sub(r"<html>", '<html lang="en">', t, count=1)
        body = json.dumps(t, ensure_ascii=False).replace("</", "<\\/")
        out = out[: m.start(2)] + body + out[m.end(2):]
        out = re.sub(r"<html>", '<html lang="en">', out, count=1)
    else:
        out = put(src, head, START, END, r"<title>.*?</title>\n?")
    return path, src, out


def sitemap():
    today = datetime.date.today().isoformat()
    urls = [BASE + c for p, (c, _, _, idx) in PAGES.items() if idx]
    items = "\n".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


ROBOTS = f"""# antoniou.org
User-agent: *
Disallow: /design/
Disallow: /cv/
Disallow: /scripts/
Disallow: /data/

Sitemap: {BASE}sitemap.xml
"""


def main():
    check = "--check" in sys.argv
    stale = []
    for page in PAGES:
        path, src, out = build_page(page)
        if out != src:
            stale.append(page)
            if not check:
                open(path, "w", encoding="utf-8").write(out)
    for name, content in (("robots.txt", ROBOTS), ("sitemap.xml", None)):
        path = os.path.join(ROOT, name)
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if content is None:  # sitemap: only the URL list matters for --check, not the date
            content = sitemap()
            same = re.sub(r"<lastmod>.*?</lastmod>", "", cur) == re.sub(r"<lastmod>.*?</lastmod>", "", content)
        else:
            same = cur == content
        if not same:
            stale.append(name)
            if not check:
                open(path, "w", encoding="utf-8").write(content)
    if check:
        print("seo: up to date" if not stale else "seo: run scripts/seo.py for " + ", ".join(stale))
        sys.exit(1 if stale else 0)
    print("seo: updated " + (", ".join(stale) if stale else "nothing (already up to date)"))


if __name__ == "__main__":
    main()
