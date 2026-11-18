import os
import html
from pubs_lib import load_json, papers_for, sub_html, PUBS_PATH

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} · AI Lab Trieste</title>
<link rel="stylesheet" href="../../style.css">
<script src="../../theme.js"></script>
</head>
<body>

<nav>
  <div class="wrap">
    <a class="brand" href="../../index.html">
      <img class="mark" src="../../logo.svg" alt="AI Lab Trieste logo">
      AI Lab Trieste
    </a>
    <div class="navlinks">
      <a href="../../index.html">Home</a>
      <a class="current" href="../../people.html">People</a>
      <a href="../../topics.html">Topics</a>
      <a href="../../papers.html">Papers</a>
      <a href="../../dissemination.html">Dissemination</a>
      <a href="../../projects.html">Projects &amp; Theses</a>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"></button>
    </div>
  </div>
</nav>

<header>
  <div class="wrap" style="padding-top:32px;">
    <a class="back-link" href="../../people.html">&larr; back to people</a>
    <div class="profile-head">
      <div class="profile-avatar"><img src="photo.jpg" alt="{name}" onerror="this.parentElement.style.background='linear-gradient(135deg, var(--teal-light), var(--bg-raised))'; this.remove();"></div>
      <div>
        <h1 class="profile-name">{name}</h1>
        <div class="profile-role">{role}</div>
        <div class="profile-tags">{tags}</div>
{links}      </div>
    </div>
  </div>
</header>

<section class="profile-section">
  <div class="wrap">
    <h2>About</h2>
    <p>{bio}</p>
  </div>
</section>

<section class="profile-section">
  <div class="wrap">
    <h2>Selected publications</h2>
    <div class="pub-list">
{pubs}
    </div>
  </div>
</section>

<footer>
  <div class="wrap footer-row">
    <span class="footer-note">&copy; 2026 AI Lab, University of Trieste</span>
    <div class="footer-links">
      <a href="https://github.com/ailab-units" target="_blank" rel="noopener">GitHub</a>
      <a href="https://huggingface.co/ailab-units" target="_blank" rel="noopener">Hugging Face</a>
      <a href="https://x.com/AILabTrieste" target="_blank" rel="noopener">X</a>
    </div>
  </div>
</footer>
</body>
</html>
"""

def tag(t, cls=""):
    c = f' {cls}' if cls else ''
    return f'<span class="tag{c}">{t}</span>'

def pub(year, title, authors, url):
    return f'''      <a class="pub" href="{url}" target="_blank" rel="noopener" style="text-decoration:none; color:inherit;">
        <span class="yr">{year}</span>
        <span><span class="t">{title}</span><span class="a">{authors}</span></span>
      </a>'''

LINK_LABELS = [("website","Website"),("email","Email"),("scholar","Google Scholar"),("scopus","Scopus"),
               ("orcid","ORCID"),("github","GitHub"),("linkedin","LinkedIn"),("x","X")]

def links_html(links):
    if not links:
        return ""
    items = "".join(f'<a href="{links[k]}" target="_blank" rel="noopener">{label}</a>'
                    for k, label in LINK_LABELS if links.get(k))
    return f'        <div class="profile-links">{items}</div>\n'

people = {
"bortolussi": dict(
    name="Luca Bortolussi",
    role="Principal Investigator &middot; Full Professor",
    tags=tag("trustworthy GenAI")+tag("neuro-explicit methods","terracotta")+tag("formal verification","yellow"),
    bio="Leads the AI Lab's research on making generative AI trustworthy by construction: constraining diffusion and flow-based models with explicit symbolic and logical structure (neuro-explicit methods), and verifying their behavior formally rather than trusting it empirically. His two-decade background in stochastic model checking underpins the lab's current push to make generative models auditable, constrainable, and provably safe. He supervises most of the lab's PhD students and holds long-running collaborations with the University of Edinburgh, Saarland University, and King's College London.",
),
"cairoli": dict(
    name="Francesca Cairoli",
    role="Tenure-Track Assistant Professor (RTT)",
    tags=tag("safe autonomy","yellow")+tag("multi-agent systems","blue")+tag("neuro-symbolic AI","terracotta")+tag("uncertainty quantification"),
    bio="Francesca is a tenure-track assistant professor of computer science in the Department of Mathematics, Informatics and Geosciences at the University of Trieste. Her research focuses on the safety assurance of autonomous systems, strategically integrating the scalability of machine learning with the rigorous, verifiable guarantees of formal methods. She combines scientific machine learning and neuro-symbolic AI to embed structured domain knowledge and safety constraints directly into the learning process &mdash; using deep generative models to reason about complex, stochastic systems and developing efficient, statistically grounded quantifications of uncertainty for safety-critical applications.",
    links=dict(
        website="https://francescacairoli.github.io/",
        email="mailto:francesca.cairoli@units.it",
        scholar="https://scholar.google.it/citations?user=3s1GGlIAAAAJ",
        scopus="https://www.scopus.com/authid/detail.uri?authorId=57211159271",
        orcid="https://orcid.org/0000-0002-6994-6553",
        github="https://github.com/francescacairoli",
        linkedin="https://www.linkedin.com/in/francesca-cairoli-18a485160/",
    ),
),
"saveri": dict(
    name="Gaia Saveri",
    role="Postdoc",
    tags=tag("neuro-symbolic","terracotta")+tag("BPMN","blue")+tag("GenAI","green"),
    bio="She is a postdoctoral researcher in neuro-symbolic computing (with a focus on integrating temporal logic requirements in learning architectures) and business process modelling and simulation. Besides, she is involved in projects promoting the use of generative AI (especially that with a neuro-symbolic flavour!) in healthcare and public administration.",
    links=dict(
        scholar="https://scholar.google.com/citations?user=AH33w6EAAAAJ",
        linkedin="https://www.linkedin.com/in/gaia-saveri-b7059a1b7/",
    ),
),
"silvetti": dict(
    name="Simone Silvetti",
    role="Postdoc",
    tags=tag("formal methods","yellow")+tag("neuro-explicit","terracotta")+tag("interpretability","pink"),
    bio="Simone Silvetti is a postdoctoral fellow at the Department of Engineering and Architecture of the University of Trieste. His research combines machine learning with quantitative formal methods to verify and design complex systems, with contributions to temporal logic specification languages and the monitoring of cyber-physical systems. His current interests include neuro-symbolic approaches that embed temporal logic formulae into continuous spaces, with applications to time series analysis and reinforcement learning. He is exploring how interpretable temporal logic patterns can be extracted from inference-time trajectories of large language models, to monitor generation at runtime and anticipate failures such as hallucinations. He also works on machine learning for edge devices, compressing computer vision models and developing audio models for insect sound recognition. He studied mathematics at Sapienza University of Rome, received a PhD in computer science from the University of Udine, and spent ten years at Esteco before joining the University of Trieste.",
    links=dict(
        website="https://simonesilvetti.com",
        scholar="https://scholar.google.com/citations?user=q_ax9IUAAAAJ",
        github="https://github.com/simonesilvetti",
        linkedin="https://www.linkedin.com/in/simonesilvetti/",
    ),
),
"ballarin": dict(
    name="Emanuele Ballarin",
    role="PhD Candidate &middot; also affiliated with IIT Genova",
    tags=tag("trustworthy GenAI","terracotta")+tag("adversarial robustness","terracotta")+tag("physics-inspired ML","yellow"),
    bio="Best known for CARSO, an adversarial defence mechanism combining adversarial training and purification &mdash; part of the lab's broader effort to make deep generative and discriminative models trustworthy under attack, not just accurate on clean data. Also a co-author of RogueAI, probing whether conversational AI can be trusted to be honest. His PhD thesis is broader still: it covers continuous-time quantum walks, Koopman operator learning, and the Forward-Forward algorithm as a biologically-plausible alternative to backpropagation.",
),
"candussio": dict(
    name="Sara Candussio",
    role="PhD Student (ADSAI programme)",
    tags=tag("LLM reasoning","green")+tag("chain-of-thought faithfulness","brown")+tag("trustworthy conversational AI","yellow"),
    bio="Studies how large reasoning models actually form their answers during chain-of-thought inference &mdash; and how much of that visible reasoning is real versus decorative. With Daniel Scalena, Gabriele Sarti (Northeastern University), Elisabetta Fersini and Malvina Nissim, she located a \"commitment boundary\" inside reasoning traces: a sharp point where the model locks in its answer, after which further CoT steps are largely epiphenomenal and can be safely cut. This connects to her broader interest in trustworthy and deceptive conversational AI, including RogueAI, a reverse Turing Test deployed as a public web game to test whether people can detect an LLM licensed to lie.",
),
"scassola": dict(
    name="Davide Scassola",
    role="PhD Candidate",
    tags=tag("neuro-explicit GenAI","terracotta")+tag("diffusion models")+tag("synthetic data","yellow"),
    bio="Works on neuro-explicit generative AI: score-based diffusion and flow-matching models whose outputs are shaped by explicit constraints rather than left to implicit statistical patterns. With Ginevra Carbone, conditions diffusion models on neuro-symbolic constraints; with Sebastiano Saccani and industry partner Aindo SpA, develops flow matching for synthetic relational/tabular data as a trustworthy, privacy-enhancing alternative to sharing real data.",
),
"della-rovere": dict(
    name="Sandro Junior Della Rovere",
    role="PhD Student",
    tags=tag("electronic design automation","slate")+tag("analog integrated circuit layout","rose")+tag("reinforcement learning"),
    bio="My research is in the Electronic Design Automation field, with a focus on analog integrated circuit layout automation. My current research combines reinforcement learning for device placement, sequential pathfinding for net routing, and tree search extensions for whole-layout optimization.</p>\n    <p>Going forward, I plan to explore LLM agents in the loop and surrogate models for post-layout simulation, with the aim of building AI-based tools for a field that remains largely unexplored.</p>\n    <p>Beyond the lab, I am an enthusiast of all things science and technology.",
    links=dict(
        scholar="https://scholar.google.com/citations?user=bDF_aCEAAAAJ",
        orcid="https://orcid.org/0009-0005-8881-5339",
        github="https://github.com/5JDR",
        linkedin="https://www.linkedin.com/in/sandrojuniordellarovere",
        x="https://x.com/5JDR0",
    ),
),
"della-siega": dict(
    name="Alessandro Della Siega",
    role="MSc Student, Data Science &amp; Artificial Intelligence",
    tags=tag("machine learning"),
    bio="Master's student in Data Science and Artificial Intelligence at the University of Trieste, working with the lab. No publications yet &mdash; add a short bio here once available.",
),
"doz": dict(
    name="Romina Doz",
    role="PhD Student (ADSAI programme)",
    tags=tag("neuro-explicit methods","terracotta")+tag("formal methods","yellow")+tag("probabilistic programs"),
    bio="First-year PhD student working in a probabilistic framework, on inference and gradient-based optimization of probabilistic programs &mdash; a neuro-explicit approach to generative modeling where program structure and uncertainty are made explicit rather than learned as a black box. Background in Physics (BSc) and Data Science and Scientific Computing (MSc). Also interested in explainable AI and causality.",
),
"pearson": dict(
    name="Nicholas Andrea Pearson",
    role="PhD Student (ADSAI programme)",
    tags=tag("trustworthy GenAI","terracotta")+tag("diffusion models")+tag("conformal prediction","yellow"),
    bio="Applies neuro-explicit, trustworthy generative AI to a real industrial problem: forecasting and anomaly detection in urban sewerage systems, with conformal statistical guarantees on top of diffusion-based time series models. His most recent work develops differentiable D-vine copulas for localized anomaly detection, refining the conformal anomaly framework introduced with CoCAI. Supervised by prof. Bortolussi in collaboration with Idrostudi Srl. MSc in Data Science and Scientific Computing (2022), BSc in Statistics (2020); previously worked with NielsenIQ on computer vision and information retrieval.",
),
"cusin": dict(
    name="Lorenzo Cusin",
    role="PhD Student",
    tags=tag("trustworthy GenAI","terracotta")+tag("LLM robustness"),
    bio="Bridges the AI Lab with the adjacent Genetic Programming group (Andrea De Lorenzo, Luca Manzoni) on a shared trustworthy-GenAI question: how robust are large language models to adversarial manipulation. Co-author of a genetic-algorithm framework for jailbreaking LLMs, work that feeds directly into the lab's broader effort to understand and close the vulnerabilities of generative models.",
),
}

PAPERS = load_json(PUBS_PATH)["papers"]

for slug, p in people.items():
    mine = papers_for(slug, PAPERS)
    pubs_html = "\n".join(pub(x["year"], html.escape(x["title"]), sub_html(x), x.get("url") or "#") for x in mine) if mine else '      <p style="color:var(--ink-soft); font-size:14.5px;">No publications listed yet.</p>'
    html_out = TEMPLATE.format(name=p["name"], role=p["role"], tags=p["tags"], bio=p["bio"], pubs=pubs_html, links=links_html(p.get("links")))
    path = f"people/{slug}/index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("wrote", path)
