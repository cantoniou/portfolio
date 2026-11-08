#!/usr/bin/env python3
"""Build every CV version from the master data in the portfolio repo (data/cv.json,
data/metrics.json, data/projects.json) plus cv/data/private.yaml (fields kept out of the
public repo).

  python3 build.py              # all variants in variants/
  python3 build.py onepager     # one variant

Each variant file in variants/ names a layout template and options. Content lives only
in the repo's data/ folder; set CV_DATA_ROOT to the repo clone (default /home/claude/portfolio). Outputs go to out/. Needs: xelatex, Inter font, python3-jinja2,
python3-yaml; for Word, node with the 'docx' package.
"""
import json, os, re, shutil, subprocess, sys, tempfile
import jinja2, yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")

def tex(s):
    s = str(s)
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
           "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}"}
    s = "".join(rep.get(ch, ch) for ch in s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*(.+?)\*", r"\\textit{\1}", s)
    s = s.replace("€", r"\texteuro{}")
    return s

DATA_ROOT = os.environ.get("CV_DATA_ROOT", os.path.dirname(ROOT))  # the repo root (this folder is cv/ inside it)

MONTHS = "January February March April May June July August September October November December".split()

def kilo(s):
    """'10k' -> '10,000' (reads better in print)."""
    return re.sub(r"\b(\d+)k\b", r"\1,000", s)

def month(s):
    """'2026-09-30' -> 'September 2026'."""
    return re.sub(r"\b(\d{4})-(\d{2})-\d{2}\b", lambda m: f"{MONTHS[int(m.group(2)) - 1]} {m.group(1)}", s)

def display(v):
    """Number style for the CV boxes: '20+' -> '>20', '>€4M' -> '>4 M€'.
    'a/b' (Google Scholar/Scopus) is styled part by part: '18k+/10k+' -> '>18,000/>10,000'."""
    if "/" in str(v):
        return "/".join(display(x) for x in str(v).split("/"))
    v = kilo(str(v))
    m = re.fullmatch(r"(>?)€(\d+(?:[.,]\d+)?)M", v)
    if m:
        return f"{m.group(1)}{m.group(2)} M€"
    if v.endswith("+"):
        return ">" + v[:-1]
    return v

def load_data():
    sys.path.insert(0, os.path.join(DATA_ROOT, "scripts"))
    from cv_tokens import render
    rd = lambda f: json.load(open(os.path.join(DATA_ROOT, "data", f), encoding="utf-8"))
    metrics = rd("metrics.json")
    cv = rd("cv.json")
    # boxes keep the compact CV style; running text uses the |words form from the tokens
    for key in ("metrics_box", "publication_breakdown"):
        cv[key] = [{**m, "value": display(render(m["value"], metrics))} for m in cv[key]]
    cv = render(cv, metrics)
    cv["profile_long"] = kilo(cv["profile_long"])
    cv["metrics_source_label"] = month(cv["metrics_source_label"])
    cv["metrics"] = cv.pop("metrics_box")
    cv["metrics_as_of"] = cv.pop("metrics_as_of_label")
    projects = {p["id"]: p for p in rd("projects.json")["projects"]}
    year = int(str(cv.get("as_of", "2026"))[:4])
    def resolve(e):
        if "id" in e or "ids" in e:
            ps = [projects[i] for i in ([e["id"]] if "id" in e else e["ids"])]
            start, end = min(p["start"] for p in ps), max(p["end"] for p in ps)
            closed = all(p.get("status") == "finished" or p["end"] < year for p in ps)
            return {"name": e.get("name") or ps[0]["name"], "funder": ps[0]["funder"],
                    "years": f"{start}–{end}", "status": "closed" if closed else "active",
                    "role": "; ".join(dict.fromkeys(p["role"] for p in ps if p.get("role")))}
        return {k: v for k, v in e.items() if k != "not_in_projects_json"}
    cv["projects"] = {k: [resolve(e) for e in v] for k, v in cv.pop("projects_as_pi").items() if not k.startswith("_")}
    priv = os.environ.get("CV_PRIVATE", os.path.join(ROOT, "data", "private.yaml"))  # never commit this file; see cv/README.md
    if os.path.exists(priv):
        for k, v in (yaml.safe_load(open(priv)) or {}).items():
            cv["person"][k] = v
    cv["person"]["photo"] = "assets/CV_photo_circle.png"
    return cv

def env():
    e = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(ROOT, "templates")),
        block_start_string="((*", block_end_string="*))", variable_start_string="(((",
        variable_end_string=")))", comment_start_string="((=", comment_end_string="=))",
        trim_blocks=True, lstrip_blocks=True, undefined=jinja2.ChainableUndefined)
    e.filters["tex"] = tex
    return e

def build(name, data):
    v = yaml.safe_load(open(os.path.join(ROOT, "variants", name + ".yaml")))
    src = env().get_template(v["template"]).render(d=data, v=v)
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(tmp, "assets"))
        texf = os.path.join(tmp, v["output"] + ".tex")
        open(texf, "w").write(src)
        for _ in range(2):
            r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(texf)],
                               cwd=tmp, capture_output=True, text=True)
            if r.returncode:
                print(r.stdout[-3000:]); sys.exit(f"xelatex failed for {name}")
        shutil.copy(texf.replace(".tex", ".pdf"), OUT)
        shutil.copy(texf, OUT)  # keep the generated .tex for reference
    pages = subprocess.run(["pdfinfo", os.path.join(OUT, v["output"] + ".pdf")], capture_output=True, text=True).stdout
    npages = re.search(r"Pages:\s+(\d+)", pages).group(1)
    print(f"{name}: out/{v['output']}.pdf ({npages} page{'s' if npages != '1' else ''})")
    if v.get("word"):
        js = os.path.join(ROOT, "docx", name + ".js")
        dj = os.path.join(OUT, ".data.json")
        json.dump(data, open(dj, "w"), ensure_ascii=False, default=str)
        r = subprocess.run(["node", js, dj, os.path.join(OUT, v["output"] + ".docx")], cwd=ROOT,
                           capture_output=True, text=True, env={**os.environ, "NODE_PATH": os.environ.get("NODE_PATH", "/home/claude/node-tools/node_modules")})
        os.remove(dj)
        if r.returncode:
            print(r.stderr); sys.exit("docx build failed")
        print(f"{name}: out/{v['output']}.docx")

if __name__ == "__main__":
    data = load_data()
    names = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, "variants")) if f.endswith(".yaml"))
    for n in names:
        build(n, data)
