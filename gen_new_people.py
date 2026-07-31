import os

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
      <a href="../../behind-the-scenes.html">Behind the Scenes</a>
      <a href="../../games.html">Games</a>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"></button>
    </div>
  </div>
</nav>

<header>
  <div class="wrap" style="padding-top:32px;">
    <a class="back-link" href="../../people.html">&larr; back to people</a>
    <div class="profile-head">
      <div class="profile-avatar"><img src="{photo}" alt="{name}" onerror="this.parentElement.style.background='linear-gradient(135deg, var(--teal-light), var(--bg-raised))'; this.remove();"></div>
      <div>
        <h1 class="profile-name">{name}</h1>
        <div class="profile-role">{role}</div>
        <div class="profile-tags">{tags}</div>
      </div>
    </div>
  </div>
</header>

<section class="profile-section">
  <div class="wrap">
    <h2>About</h2>
    <p>{bio}</p>
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

people = {
"vascotto": dict(
    name="Ilaria Vascotto",
    role="PhD Candidate",
    photo="photo.jpg",
    tags=tag("interpretability")+tag("XAI robustness","terracotta")+tag("trustworthy GenAI","yellow"),
    bio="Works on explainable AI, focusing on the robustness of feature-attribution methods and on aggregating explanations across multiple models for more trustworthy decision support. Applies this mainly to the insurance and asset management domains, with the support of Assicurazioni Generali, and is also interested in clinical and medical applications of XAI."
),
"blasone": dict(
    name="Valentina Blasone",
    role="PhD Candidate",
    photo="photo.jpg",
    tags=tag("interpretability")+tag("environmental ML","olive")+tag("XAI robustness","terracotta"),
    bio="Works on the reliability and robustness of explainable AI methods, including on unbalanced datasets, with applications spanning environmental modelling (frost event prediction, atmosphere/ocean/seabed monitoring) alongside more standard tabular domains."
),
"giacomarra": dict(
    name="Francesco Giacomarra",
    role="PhD Candidate",
    photo="photo.jpg",
    tags=tag("neuro-explicit GenAI","terracotta")+tag("formal methods","yellow"),
    bio="Co-author of the lab's STREL-guided diffusion work on neuro-symbolic scenario generation for autonomous driving safety, combining generative models with formal spatio-temporal logic specifications."
),
"plasencia": dict(
    name="Milton Nicolas Plasencia Palacios",
    role="PhD Candidate",
    photo="photo.jpg",
    tags=tag("synthetic data","olive")+tag("privacy","slate")+tag("trustworthy GenAI"),
    bio="Works on privacy-preserving synthetic tabular data, including contrastive-learning-based privacy metrics for evaluating how safely synthetic datasets can substitute real, sensitive ones."
),
"mecchina": dict(
    name="Andrea Mecchina",
    role="Research Fellow &middot; PhD Student",
    photo="photo.png",
    tags=tag("econometrics","blue")+tag("ML systems","slate"),
    bio="Works on statistical and neural-network-based econometric models for factorial portfolio optimization and tactical asset allocation, in collaboration with Generali Investments. More recently also works on AI solutions for port and hinterland connectivity management and sustainability."
),
"bonin": dict(
    name="Lorenzo Bonin",
    role="Researcher",
    photo="photo.jpg",
    tags=tag("neuro-explicit GenAI","terracotta")+tag("environmental ML","olive"),
    bio="PhD researcher working within the iNEST project on digital twins of the North Adriatic Sea, for real-time monitoring and simulation. Also co-author of the lab's STREL-guided neuro-symbolic scenario generation work, and of a genetic-algorithm framework for jailbreaking LLMs with the Genetic Programming group."
),
}

for slug, p in people.items():
    html = TEMPLATE.format(name=p["name"], role=p["role"], tags=p["tags"], bio=p["bio"], photo=p["photo"])
    path = f"people/{slug}/index.html"
    with open(path, "w") as f:
        f.write(html)
    print("wrote", path)
