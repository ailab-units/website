"""Adds new publications of lab members from DBLP to data/publications.json.

DBLP also indexes arXiv preprints (as "CoRR"), so one source covers both.
Run weekly by .github/workflows/update-publications.yml, which opens a pull request.

  python fetch_publications.py                 # normal run
  python fetch_publications.py --bootstrap     # mark everything currently on DBLP as seen, add nothing
  python fetch_publications.py --offline DIR   # read DBLP responses from DIR (tests)

Rules
- A paper is "new" if none of its DBLP keys is in seen_dblp_keys and its title does not
  match a paper already in the file. Every key the script looks at is recorded in
  seen_dblp_keys, so deleting a paper from the JSON in review drops it for good.
- A preprint and its published version are merged; the published one wins.
- Papers already in the file are never rewritten. The script only fills an empty url,
  and adds lab members who are authors to 'people'.
"""
import argparse, html, json, os, re, sys, time
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

from pubs_lib import (load_json, save_json, norm_title, same_title, MONTHS,
                      PUBS_PATH, MEMBERS_PATH)

UA = "ailab-units-website (+https://github.com/ailab-units/website)"
KEEP_TYPES = {"article", "inproceedings", "incollection"}
PARTICLES = {"de", "della", "del", "di", "da", "dal", "van", "von", "der", "le", "la", "dos", "das", "du"}
JOURNAL_SHORT = {
    "Trans. Mach. Learn. Res.": "TMLR",
    "IEEE Trans. Neural Networks Learn. Syst.": "IEEE TNNLS",
    "Int. J. Softw. Tools Technol. Transf.": "STTT",
}


# ---------------------------------------------------------------- network --
class Source:
    def __init__(self, offline=None):
        self.offline = offline

    def _get(self, url):
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                time.sleep(1.5)  # be gentle with dblp.org
                return data
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    raise
                time.sleep(5 * (attempt + 1))

    def search_author(self, name):
        if self.offline:
            path = os.path.join(self.offline, "search", re.sub(r"\W+", "_", name) + ".json")
            return json.load(open(path)) if os.path.exists(path) else {"result": {"hits": {}}}
        q = urllib.parse.urlencode({"q": name, "format": "json", "h": 20})
        return json.loads(self._get(f"https://dblp.org/search/author/api?{q}"))

    def person_xml(self, pid):
        if self.offline:
            path = os.path.join(self.offline, "pid", pid.replace("/", "_") + ".xml")
            return open(path, "rb").read() if os.path.exists(path) else b"<dblpperson/>"
        return self._get(f"https://dblp.org/pid/{pid}.xml")


# ---------------------------------------------------------------- parsing --
def clean_name(n):
    return re.sub(r"\s+\d{4}$", "", n).strip()   # "Luca Bortolussi 0001" -> "Luca Bortolussi"


def norm_name(n):
    return norm_title(clean_name(n))


def resolve_pid(src, name):
    hits = src.search_author(name).get("result", {}).get("hits", {}).get("hit", [])
    exact = [h["info"] for h in hits if norm_name(h["info"].get("author", "")) == norm_name(name)]
    pids = sorted({re.sub(r"^https?://dblp\.org/pid/", "", i["url"]) for i in exact})
    return pids


def parse_records(xml_bytes):
    root = ET.fromstring(xml_bytes)
    for r in root.findall("r"):
        for rec in r:
            if rec.tag not in KEEP_TYPES or rec.get("publtype") == "withdrawn":
                continue
            title = "".join(rec.find("title").itertext()).strip().rstrip(".") if rec.find("title") is not None else ""
            authors = [(clean_name("".join(a.itertext())), a.get("pid", "")) for a in rec.findall("author")]
            year = int(rec.findtext("year", "0") or 0)
            journal, booktitle = rec.findtext("journal"), rec.findtext("booktitle")
            ees = [e.text for e in rec.findall("ee") if e.text]
            yield dict(key=rec.get("key"), type=rec.tag, title=title, authors=authors, year=year,
                       journal=journal, booktitle=booktitle, volume=rec.findtext("volume", ""), ees=ees,
                       corr=(journal == "CoRR"))


def arxiv_id(rec):
    m = re.search(r"abs/(\d{4})\.(\d{4,5})", rec["volume"]) or re.search(r"abs-(\d{4})-(\d{4,5})", rec["key"])
    return f"{m.group(1)}.{m.group(2)}" if m else None


# ------------------------------------------------------------- formatting --
def surname(full, known):
    toks = full.split()
    for k in (3, 2, 1):
        cand = " ".join(toks[-k:])
        if len(toks) > k and cand in known:
            return cand
    if len(toks) >= 3 and toks[-2].lower() in PARTICLES:
        return " ".join(toks[-2:])
    return toks[-1] if toks else full


def to_paper(rec, known_surnames):
    authors = ", ".join(surname(n, known_surnames) for n, _ in rec["authors"])
    month = None
    if rec["corr"]:
        venue, aid = "", arxiv_id(rec)
        url = f"https://arxiv.org/abs/{aid}" if aid else (rec["ees"][0] if rec["ees"] else "")
        if aid:
            month = int(aid[2:4])
        label = MONTHS[month - 1] if month else str(rec["year"])
    elif rec["booktitle"]:
        bt = re.sub(r"\s*\(\d+\)$", "", rec["booktitle"]).replace("/", "-")
        venue, label = f"{bt} {rec['year']}", re.split(r"[-\s]", bt)[0]
        url = next((e for e in rec["ees"] if "doi.org" in e), rec["ees"][0] if rec["ees"] else "")
    else:
        j = rec["journal"] or ""
        venue = JOURNAL_SHORT.get(j, j)
        label = JOURNAL_SHORT.get(j, str(rec["year"])).split()[-1]
        url = next((e for e in rec["ees"] if "doi.org" in e), rec["ees"][0] if rec["ees"] else "")
    return dict(title=rec["title"], authors=authors, venue=venue, year=rec["year"], label=label,
                month=month, url=url, people=[], on_lab_page=True, source="dblp")


# ------------------------------------------------------------------ main ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", action="store_true")
    ap.add_argument("--offline")
    ap.add_argument("--summary", default="publications-summary.md")
    args = ap.parse_args()

    src = Source(args.offline)
    cfg = load_json(MEMBERS_PATH)
    data = load_json(PUBS_PATH)
    since = cfg.get("since_year", 2020)
    papers, seen = data["papers"], set(data.get("seen_dblp_keys", []))
    notes = {"new": [], "people": [], "url": [], "published": [], "pid": [], "warn": []}

    # 1. resolve missing DBLP ids
    for m in cfg["members"]:
        if m.get("fetch", True) and not m.get("dblp_pid"):
            pids = resolve_pid(src, m["name"])
            if len(pids) == 1:
                m["dblp_pid"] = pids[0]
                notes["pid"].append(f'{m["name"]} → [`{pids[0]}`](https://dblp.org/pid/{pids[0]}.html)')
            elif pids:
                notes["warn"].append(f'{m["name"]}: several DBLP profiles ({", ".join(pids)}), set `dblp_pid` by hand in data/members.json')
            else:
                notes["warn"].append(f'{m["name"]}: no DBLP profile yet, will retry next week')

    by_pid = {m["dblp_pid"]: m for m in cfg["members"] if m.get("dblp_pid")}
    by_name = {norm_name(m["name"]): m for m in cfg["members"]}

    # 2. download every member's record list
    recs = {}
    for m in cfg["members"]:
        if m.get("fetch", True) and m.get("dblp_pid"):
            for rec in parse_records(src.person_xml(m["dblp_pid"])):
                if rec["year"] >= since:
                    recs[rec["key"]] = rec

    # 3. group preprint + published versions of the same paper
    groups = []
    for rec in sorted(recs.values(), key=lambda r: r["corr"]):        # published first
        g = next((g for g in groups if same_title(g[0]["title"], rec["title"])), None)
        (g.append(rec) if g else groups.append([rec]))

    known = {a.strip() for p in papers for a in html.unescape(p.get("authors", "")).split(",")}
    known.discard("")

    def lab_people(group):
        slugs = []
        for rec in group:
            for name, pid in rec["authors"]:
                m = by_pid.get(pid) or by_name.get(norm_name(name))
                if m and m.get("slug") and m["slug"] not in slugs:
                    slugs.append(m["slug"])
        return slugs

    new = []
    for g in groups:
        keys = [r["key"] for r in g]
        best = g[0]                                                    # published if any
        existing = next((p for p in papers if same_title(p["title"], best["title"])
                         or any(same_title(p["title"], r["title"]) for r in g)), None)
        if args.bootstrap:
            seen.update(keys); continue
        if existing:
            people = lab_people(g)
            added = [s for s in people if s not in existing.setdefault("people", [])]
            if added:
                existing["people"].extend(added)
                notes["people"].append(f'{existing["title"]} — now also on: {", ".join(added)}')
            if not existing.get("url"):
                cand = to_paper(best, known)["url"]
                if cand:
                    existing["url"] = cand
                    notes["url"].append(f'{existing["title"]} — {cand}')
            if not existing.get("venue") and not best["corr"] and not set(keys) <= seen:
                notes["published"].append(f'{existing["title"]} — DBLP has a published version: '
                                          f'{to_paper(best, known)["venue"]} (left unchanged, update by hand if you want)')
            seen.update(keys)
            continue
        if set(keys) & seen:
            seen.update(keys); continue                                # rejected earlier
        p = to_paper(best, known)
        p["people"] = lab_people(g)
        p["dblp_keys"] = keys
        new.append(p)
        seen.update(keys)
        notes["new"].append(f'{p["year"]} · {p["title"]} — {p["authors"]}'
                            f'{" · " + p["venue"] if p["venue"] else " (preprint)"} — on: {", ".join(p["people"]) or "lab page only"}')

    # 4. new papers go to the top of their year, newest month first
    for y in {p["year"] for p in new}:
        top = min([p.get("order", 0) for p in papers if p.get("year") == y] or [0])
        batch = sorted([p for p in new if p["year"] == y], key=lambda p: -(p["month"] or 0))
        for i, p in enumerate(batch):
            p["order"] = top - 10 * (len(batch) - i)
    papers.extend(new)

    data["seen_dblp_keys"] = sorted(seen)
    save_json(PUBS_PATH, data)
    save_json(MEMBERS_PATH, cfg)
    write_summary(args.summary, notes, args.bootstrap, len(seen))
    print(open(args.summary).read())


def write_summary(path, notes, bootstrap, n_seen):
    out = ["Automatic weekly update from [DBLP](https://dblp.org) (includes arXiv preprints).", ""]
    if bootstrap:
        out.append(f"**Bootstrap run:** {n_seen} existing DBLP records marked as seen, no papers added.")
    sections = [("new", "New papers", "Check them; delete any you don't want from `data/publications.json` in this PR, they won't come back."),
                ("people", "Lab members added to existing papers", ""),
                ("url", "Missing links filled in", ""),
                ("published", "Preprints that now have a published version", ""),
                ("pid", "DBLP profiles found", "Check these are the right people."),
                ("warn", "Needs attention", "")]
    for k, title, hint in sections:
        if notes[k]:
            out += [f"### {title} ({len(notes[k])})", hint, ""] if hint else [f"### {title} ({len(notes[k])})", ""]
            out += [f"- {x}" for x in notes[k]] + [""]
    if not any(notes.values()) and not bootstrap:
        out.append("No changes.")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    main()
