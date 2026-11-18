"""Shared helpers for the publication data (data/publications.json).

The JSON file is the single source of truth for papers: gen_people.py builds each
person's "Selected publications" from it and gen_papers.py builds papers.html.
fetch_publications.py adds new papers from DBLP."""
import html, json, re, unicodedata
from difflib import SequenceMatcher

PUBS_PATH = "data/publications.json"
MEMBERS_PATH = "data/members.json"
MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def norm_title(t):
    t = unicodedata.normalize("NFKD", html.unescape(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def same_title(a, b, threshold=0.9):
    a, b = norm_title(a), norm_title(b)
    return a == b or SequenceMatcher(None, a, b).ratio() >= threshold


def sorted_papers(papers):
    """Newest year first; inside a year, by the editable 'order' field (lower = higher up)."""
    return sorted(papers, key=lambda p: (-(p.get("year") or 0), p.get("order", 0)))


def sub_html(p):
    """'Authors · Venue' line, HTML-escaped."""
    parts = [html.escape(p["authors"])] if p.get("authors") else []
    if p.get("venue"):
        parts.append(html.escape(p["venue"]))
    return " &middot; ".join(parts)


def papers_for(slug, papers):
    return sorted_papers([p for p in papers if slug in p.get("people", [])])
