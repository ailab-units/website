"""Builds papers.html from data/publications.json. Run after editing the data file."""
import html
from pubs_lib import load_json, sorted_papers, sub_html, PUBS_PATH, MEMBERS_PATH

HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Papers · AI Lab Trieste</title>\n<link rel="stylesheet" href="style.css">\n<script src="theme.js"></script>\n</head>\n<body>\n\n<nav>\n  <div class="wrap">\n    <a class="brand" href="index.html">\n      <img class="mark" src="logo.svg" alt="AI Lab Trieste logo">\n      AI Lab Trieste\n    </a>\n    <div class="navlinks">\n      <a href="index.html">Home</a>\n      <a href="people.html">People</a>\n      <a href="topics.html">Topics</a>\n      <a class="current" href="papers.html">Papers</a>\n      <a href="dissemination.html">Dissemination</a>\n      <a href="projects.html">Projects &amp; Theses</a>\n      <a href="behind-the-scenes.html">Behind the Scenes</a>\n      <a href="games.html">Games</a>\n      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"></button>\n    </div>\n  </div>\n</nav>\n\n'

HEADER = '<header class="page-head">\n  <div class="wrap">\n    <span class="eyebrow">Publications</span>\n    <h1>Papers.</h1>\n    <p>The full, consolidated publication record of the lab, 2020&ndash;2026. Also mirrored on our <a href="https://huggingface.co/ailab-units" target="_blank" rel="noopener" style="color:var(--teal)">Hugging Face org page</a>, organized into thematic collections with associated models and datasets.</p>\n  </div>\n</header>\n\n'

FOOT = '\n\n<footer>\n  <div class="wrap footer-row">\n    <span class="footer-note">&copy; 2026 AI Lab, University of Trieste</span>\n    <div class="footer-links">\n      <a href="https://github.com/ailab-units" target="_blank" rel="noopener">GitHub</a>\n      <a href="https://huggingface.co/ailab-units" target="_blank" rel="noopener">Hugging Face</a>\n      <a href="https://x.com/AILabTrieste" target="_blank" rel="noopener">X</a>\n    </div>\n  </div>\n</footer>\n</body>\n</html>\n'

N_YEAR_SECTIONS = 3   # newest years get their own section, the rest go under "YYYY & earlier"


def item(p):
    url = p.get("url") or "#"
    target = ' target="_blank" rel="noopener"' if url != "#" else ""
    return (f'      <a class="item" href="{html.escape(url)}"{target}>\n'
            f'        <span class="date">{html.escape(p.get("label") or str(p["year"]))}</span>\n'
            f'        <span><span class="title">{html.escape(p["title"])}</span>\n'
            f'        <span class="sub">{sub_html(p)}</span></span>\n'
            f'        <span class="arrow">&#8599;</span>\n'
            f'      </a>')


def main():
    since = load_json(MEMBERS_PATH).get("since_year", 2020)
    papers = [p for p in load_json(PUBS_PATH)["papers"]
              if p.get("on_lab_page", True) and (p.get("year") or 0) >= since]
    papers = sorted_papers(papers)
    years = sorted({p["year"] for p in papers}, reverse=True)
    own = years[:N_YEAR_SECTIONS]
    groups = [(str(y), [p for p in papers if p["year"] == y]) for y in own]
    rest = [p for p in papers if p["year"] not in own]
    if rest:
        groups.append((f"{own[-1] - 1} &amp; earlier", rest))

    body = ["<section>", '  <div class="wrap">', ""]
    for label, ps in groups:
        body.append(f'    <div class="section-label">{label}</div>')
        body.append('    <div class="item-list">')
        body.extend(item(p) for p in ps)
        body.append("    </div>")
        body.append("")
    body.append("  </div>")
    body.append("</section>")
    header = HEADER.replace("2020&ndash;2026", f"{since}&ndash;{years[0]}")
    with open("papers.html", "w", encoding="utf-8") as f:
        f.write(HEAD + header + "\n".join(body) + FOOT)
    print(f"wrote papers.html ({len(papers)} papers)")


if __name__ == "__main__":
    main()
