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

people = {
"bortolussi": dict(
    name="Luca Bortolussi",
    role="Principal Investigator &middot; Full Professor",
    tags=tag("formal methods")+tag("neuro-symbolic AI","terracotta")+tag("stochastic systems","yellow"),
    bio="Leads the AI Lab. His work spans two decades, from mean-field approximation and stochastic model checking to today's neuro-symbolic generative AI and adversarial robustness. He supervises most of the lab's PhD students and holds long-running collaborations with the University of Edinburgh, Saarland University, and King's College London.",
    pubs=[
        ("2026","Scalable and reliable stochastic parametric verification with stochastic variational smoothed model checking","Cairoli, Bortolussi &middot; Int. J. Syst. Sci.","https://huggingface.co/papers/2605.19038"),
        ("2025","Zero-Shot Conditioning of Score-Based Diffusion Models by Neuro-Symbolic Constraints","Scassola, Saccani, Carbone, Bortolussi &middot; AAAI 2025","https://arxiv.org/abs/2308.16534"),
        ("2025","On the Robustness of Bayesian Neural Networks to Adversarial Attacks","Bortolussi, Carbone, Laurenti, Patane, Sanguinetti, Wicker &middot; IEEE TNNLS","https://arxiv.org/abs/2207.06154"),
        ("2022","Learning Model Checking and the Kernel Trick for Signal Temporal Logic on Stochastic Processes","Bortolussi, Gallo, Kretínský, Nenzi &middot; TACAS 2022","https://arxiv.org/abs/2201.09928"),
    ]
),
"cairoli": dict(
    name="Francesca Cairoli",
    role="Postdoctoral Researcher",
    tags=tag("predictive monitoring")+tag("conformal prediction","terracotta")+tag("generative modeling","yellow"),
    bio="Works on predictive monitoring of stochastic and cyber-physical systems with formal statistical guarantees (conformal prediction), and on generative abstraction of Markov population models. Long-running collaboration with Nicola Paoletti (King's College London) since 2019.",
    pubs=[
        ("2025","Conformal Predictive Monitoring for Multi-modal Scenarios","Cairoli, Bortolussi, Deshmukh, Lindemann, Paoletti &middot; RV 2025","https://arxiv.org/abs/2509.01338"),
        ("2025","CoCAI: Copula-Based Conformal Anomaly Identification for Multivariate Time-Series","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; RV 2025","https://arxiv.org/abs/2507.17796"),
        ("2023","Conformal Quantitative Predictive Monitoring of STL Requirements for Stochastic Processes","Cairoli, Paoletti, Bortolussi &middot; HSCC 2023","https://www.nicolapaoletti.com/assets/papers/CQR_HSCC23.pdf"),
        ("2021","Abstraction of Markov Population Dynamics via Generative Adversarial Nets","Cairoli, Carbone, Bortolussi &middot; CMSB 2021","https://arxiv.org/abs/2106.12981"),
    ]
),
"cina": dict(
    name="Antonio Emanuele Cin\u00e0",
    role="Collaborator",
    tags=tag("adversarial ML","terracotta")+tag("ML security","terracotta"),
    bio="External collaborator working on adversarial machine learning and the security of learning systems &mdash; understanding how models can be attacked, and how to make them resilient.",
    pubs=[]
),
"saveri": dict(
    name="Gaia Saveri",
    role="Research Collaborator &middot; PhD (national AI programme)",
    tags=tag("temporal logic")+tag("neuro-symbolic AI","terracotta")+tag("explainability","yellow"),
    bio="Works on continuous, invertible embeddings of Signal Temporal Logic formulae, and on concept-based explainability for time series (the STELLE framework, with Irene Ferfoglia and Simone Silvetti). Bridges symbolic specifications and deep learning representations.",
    pubs=[
        ("2025","Guided by Stars: Interpretable Concept Learning Over Time Series via Temporal Logic Semantics","Ferfoglia, Silvetti, Saveri, Nenzi, Bortolussi","https://arxiv.org/abs/2511.04244"),
        ("2025","Bridging Logic and Learning: Decoding Temporal Logic Embeddings via Transformers","Candussio, Saveri, Sarti, Bortolussi &middot; ECML-PKDD 2025","https://arxiv.org/abs/2507.07808"),
        ("2024","stl2vec: Semantic and Interpretable Vector Representation of Temporal Logic","Saveri, Nenzi, Bortolussi, Kretínský &middot; ECAI 2024","https://arxiv.org/abs/2405.14389"),
        ("2024","Retrieval-Augmented Mining of Temporal Logic Specifications from Data","Saveri, Bortolussi &middot; ECML-PKDD 2024","https://arxiv.org/abs/2405.14355"),
    ]
),
"ballarin": dict(
    name="Emanuele Ballarin",
    role="PhD Candidate &middot; also affiliated with IIT Genova",
    tags=tag("adversarial robustness","terracotta")+tag("representation learning")+tag("physics-inspired ML","yellow"),
    bio="Best known for CARSO, an adversarial defence mechanism combining adversarial training and purification. His PhD thesis is broader than robustness alone: it also covers continuous-time quantum walks, Koopman operator learning, and the Forward-Forward algorithm as a biologically-plausible alternative to backpropagation.",
    pubs=[
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2025","Blending adversarial training and representation-conditional purification via aggregation improves adversarial robustness","Ballarin, Ansuini, Bortolussi &middot; TMLR","https://arxiv.org/abs/2306.06081"),
    ]
),
"candussio": dict(
    name="Sara Candussio",
    role="PhD Student (ADSAI programme)",
    tags=tag("temporal logic")+tag("LLM interpretability","terracotta")+tag("trustworthy conversational AI","yellow"),
    bio="Works across three lines: temporal logic embeddings with Gaia Saveri; LLM interpretability and answer-commitment in chain-of-thought reasoning, with Gabriele Sarti (Groningen); and trustworthy/deceptive conversational AI, including RogueAI, a reverse Turing Test deployed as a public web game.",
    pubs=[
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2026","Distilling Formal Logic into Neural Spaces: A Kernel Alignment Approach for STL","Candussio, Sarti, Saveri, Bortolussi &middot; NeSy 2026",""),
        ("2025","Bridging Logic and Learning: Decoding Temporal Logic Embeddings via Transformers","Candussio, Saveri, Sarti, Bortolussi &middot; ECML-PKDD 2025","https://arxiv.org/abs/2507.07808"),
    ]
),
"scassola": dict(
    name="Davide Scassola",
    role="PhD Candidate",
    tags=tag("diffusion models")+tag("flow matching","terracotta")+tag("synthetic data","yellow"),
    bio="Works on score-based diffusion and flow-matching generative models. One line, with Ginevra Carbone, conditions diffusion models on neuro-symbolic constraints; another, with Sebastiano Saccani and industry partner Aindo SpA, develops flow matching for synthetic relational/tabular data as a privacy-enhancing technology.",
    pubs=[
        ("2026","Graph-Conditional Flow Matching for Relational Data Generation","Scassola, Saccani, Bortolussi &middot; AAAI 2026","https://ojs.aaai.org/index.php/AAAI/article/view/39712"),
        ("2025","Zero-Shot Conditioning of Score-Based Diffusion Models by Neuro-Symbolic Constraints","Scassola, Saccani, Carbone, Bortolussi &middot; AAAI 2025","https://arxiv.org/abs/2308.16534"),
    ]
),
"della-rovere": dict(
    name="Sandro Junior Della Rovere",
    role="Researcher",
    tags=tag("reinforcement learning")+tag("analog IC design","terracotta")+tag("trustworthy conversational AI","yellow"),
    bio="Works on reinforcement learning for the floorplanning of analog integrated circuits, in collaboration with Infineon Technologies (Villach/Munich). Also co-author of RogueAI, on detecting deception in LLM dialogue &mdash; a second, unrelated line of work within the lab.",
    pubs=[
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2025","Enhancing Reinforcement Learning for the Floorplanning of Analog ICs with Beam Search","Della Rovere, Basso, Bortolussi, Videnovic-Misic, Habal &middot; SMACD 2025","https://arxiv.org/abs/2505.05059"),
    ]
),
"della-siega": dict(
    name="Alessandro Della Siega",
    role="MSc Student, Data Science &amp; Artificial Intelligence",
    tags=tag("machine learning"),
    bio="Master's student in Data Science and Artificial Intelligence at the University of Trieste, working with the lab. No publications yet &mdash; add a short bio here once available.",
    pubs=[]
),
}

for slug, p in people.items():
    pubs_html = "\n".join(pub(*args) for args in p["pubs"]) if p["pubs"] else '      <p style="color:var(--ink-soft); font-size:14.5px;">No publications listed yet.</p>'
    html = TEMPLATE.format(name=p["name"], role=p["role"], tags=p["tags"], bio=p["bio"], pubs=pubs_html)
    path = f"people/{slug}/index.html"
    with open(path, "w") as f:
        f.write(html)
    print("wrote", path)
