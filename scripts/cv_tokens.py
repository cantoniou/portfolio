"""Fill the number tokens in data/cv.json from data/metrics.json.

A token is {metrics.<path>} or {metrics.<path>|words}, e.g. {metrics.cv.publications}.
'|words' turns '>600' or '600+' into 'more than 600' for running text.
CV build scripts call render(); scripts/check_consistency.py uses it to check every token resolves.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = re.compile(r"\{metrics\.([a-z0-9_.]+)(\|words)?\}")


def load_metrics():
    return json.load(open(os.path.join(ROOT, "data", "metrics.json"), encoding="utf-8"))


def lookup(metrics, path):
    v = metrics
    for part in path.split("."):
        v = v[part]  # KeyError = unknown token
    return str(v)


def words(v):
    if v.startswith(">"):
        return "more than " + v[1:].strip()
    if v.endswith("+"):
        return "more than " + v[:-1]
    return v


def render(obj, metrics=None):
    """Return obj (str, list or dict) with every token replaced."""
    metrics = metrics or load_metrics()
    if isinstance(obj, str):
        return TOKEN.sub(lambda m: (words if m.group(2) else str)(lookup(metrics, m.group(1))), obj)
    if isinstance(obj, list):
        return [render(x, metrics) for x in obj]
    if isinstance(obj, dict):
        return {k: render(v, metrics) for k, v in obj.items()}
    return obj


def tokens(obj):
    return TOKEN.findall(json.dumps(obj, ensure_ascii=False))
