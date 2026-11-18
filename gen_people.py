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
    pubs=[
        ("2026","Scalable and reliable stochastic parametric verification with stochastic variational smoothed model checking","Cairoli, Bortolussi &middot; Int. J. Syst. Sci.","https://huggingface.co/papers/2605.19038"),
        ("2026","DeGAS: Gradient-Based Optimization of Probabilistic Programs without Sampling","Randone, Doz, Tribastone, Bortolussi &middot; TACAS 2026","https://arxiv.org/abs/2601.15167"),
        ("2026","Distilling Formal Logic into Neural Spaces: A Kernel Alignment Approach for STL","Candussio, Sarti, Saveri, Bortolussi &middot; NeSy 2026",""),
        ("2026","Graph-Conditional Flow Matching for Relational Data Generation","Scassola, Saccani, Bortolussi &middot; AAAI 2026","https://ojs.aaai.org/index.php/AAAI/article/view/39712"),
        ("2026","Beyond the Commitment Boundary: Probing Epiphenomenal Chain-of-Thought in Large Reasoning Models","Scalena, Candussio, Bortolussi, Fersini, Nissim, Sarti","https://arxiv.org/abs/2606.13603"),
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2026","Localized Anomaly Detection via Differentiable D-vine Copulas","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; CAESAR @ ECML-PKDD 2026","https://arxiv.org/abs/2607.25020"),
        ("2026","A Sobering Look at Tabular Data Generation via Probabilistic Circuits","Scassola, Ponsford, Javaloy, Saccani, Bortolussi, Gouk, Vergari",""),
        ("2025","Guiding Neuro-Symbolic Scenario Generation with Spatio-Temporal Logic","Bonin, Giacomarra, Bortolussi, Deshmukh, Cairoli","https://huggingface.co/papers/2605.19038"),
        ("2025","Bridging Logic and Learning: Decoding Temporal Logic Embeddings via Transformers","Candussio, Saveri, Sarti, Bortolussi &middot; ECML-PKDD 2025","https://arxiv.org/abs/2507.07808"),
        ("2025","Zero-Shot Conditioning of Score-Based Diffusion Models by Neuro-Symbolic Constraints","Scassola, Saccani, Carbone, Bortolussi &middot; AAAI 2025","https://arxiv.org/abs/2308.16534"),
        ("2025","Scaling Combinatorial Optimization Neural Improvement Heuristics with Online Search and Adaptation","Camerota Verd&ugrave;, Castelli, Bortolussi &middot; AAAI 2025",""),
        ("2025","Effective Analog ICs Floorplanning with Relational Graph Neural Networks and Reinforcement Learning","Basso, Bortolussi, Videnovic-Misic, Habal &middot; DATE 2025",""),
        ("2025","Evolutionary Synthesis of Probabilistic Programs","Doz, Randone, Medvet, Bortolussi &middot; GECCO 2025","https://dl.acm.org/doi/10.1145/3712256.3726388"),
        ("2025","Intrinsic Dimension Correlation: uncovering nonlinear connections in multimodal representations","Basile, Acevedo, Bortolussi, Anselmi, Rodriguez &middot; ICLR 2025",""),
        ("2025","Frequency maps reveal the correlation between Adversarial Attacks and Implicit Bias","Basile, Karantzas, d'Onofrio, Manzoni, Bortolussi, Rodriguez, Anselmi &middot; IJCNN 2025",""),
        ("2025","Neuro-Symbolic Discovery of Markov Population Processes","Bortolussi, Cairoli, Klein, Petrov &middot; NeuS 2025",""),
        ("2025","Enhancing Reinforcement Learning for the Floorplanning of Analog ICs with Beam Search","Della Rovere, Basso, Bortolussi, Videnovic-Misic, Habal &middot; SMACD 2025","https://arxiv.org/abs/2505.05059"),
        ("2025","CoCAI: Copula-Based Conformal Anomaly Identification for Multivariate Time-Series","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; RV 2025","https://arxiv.org/abs/2507.17796"),
        ("2025","Conformal Predictive Monitoring for Multi-modal Scenarios","Cairoli, Bortolussi, Deshmukh, Lindemann, Paoletti &middot; RV 2025","https://arxiv.org/abs/2509.01338"),
        ("2025","Blending adversarial training and representation-conditional purification via aggregation improves adversarial robustness","Ballarin, Ansuini, Bortolussi &middot; TMLR","https://arxiv.org/abs/2306.06081"),
        ("2025","ResiDual Transformer Alignment with Spectral Decomposition","Basile, Maiorca, Bortolussi, Rodol&agrave;, Locatello &middot; TMLR",""),
        ("2025","On the Robustness of Bayesian Neural Networks to Adversarial Attacks","Bortolussi, Carbone, Laurenti, Patane, Sanguinetti, Wicker &middot; IEEE TNNLS","https://arxiv.org/abs/2207.06154"),
        ("2025","Timeseria: An object-oriented time series processing library","Russo, Taffoni, Bortolussi &middot; SoftwareX",""),
        ("2025","Diffusion-based Time Series Forecasting for Sewerage Systems","Pearson, Cairoli, Bortolussi, Russo, Zanello","https://arxiv.org/abs/2506.08577"),
        ("2025","When Can You Trust Your Explanations? A Robustness Analysis on Feature Importances","Vascotto, Rodriguez, Bonaita, Bortolussi &middot; xAI 2025",""),
        ("2024","Deep Learning-Informed Bayesian Model-Based Analysis to Estimate Superspreading Events in Epidemic Outbreaks","Tasciotti, Urban, de Dea, Bortolussi, Caravagna, d'Onofrio &middot; IEEE Access",""),
        ("2024","Inference of Probabilistic Programs with Moment-Matching Gaussian Mixtures","Randone, Bortolussi, Incerto, Tribastone &middot; POPL 2024",""),
        ("2024","stl2vec: Semantic and Interpretable Vector Representation of Temporal Logic","Saveri, Nenzi, Bortolussi, Kret&iacute;nsk&yacute; &middot; ECAI 2024","https://arxiv.org/abs/2405.14389"),
        ("2024","Is Machine Learning Model Checking Privacy Preserving?","Bortolussi, Nenzi, Saveri, Silvetti &middot; ISoLA 2024",""),
        ("2024","Towards a Probabilistic Programming Approach to Analyse Collective Adaptive Systems","Randone, Doz, Cairoli, Bortolussi &middot; ISoLA 2024",""),
        ("2024","ECATS: Explainable-by-Design Concept-Based Anomaly Detection for Time Series","Ferfoglia, Saveri, Nenzi, Bortolussi &middot; NeSy 2024",""),
        ("2024","Retrieval-Augmented Mining of Temporal Logic Specifications from Data","Saveri, Bortolussi &middot; ECML-PKDD 2024","https://arxiv.org/abs/2405.14355"),
        ("2024","Fast ML-driven Analog Circuit Layout using Reinforcement Learning and Steiner Trees","Basso, Bortolussi, Videnovic-Misic, Habal &middot; SMACD 2024",""),
        ("2023","Data Symmetries and Learning in Fully Connected Neural Networks","Anselmi, Manzoni, d'Onofrio, Rodriguez, Caravagna, Bortolussi, Cairoli &middot; IEEE Access",""),
        ("2023","MoonLight: a lightweight tool for monitoring spatio-temporal properties","Nenzi, Bartocci, Bortolussi, Silvetti, Loreti &middot; STTT",""),
        ("2023","Generative abstraction of Markov population processes","Cairoli, Anselmi, d'Onofrio, Bortolussi &middot; Theor. Comput. Sci.",""),
        ("2023","Conformal Quantitative Predictive Monitoring of STL Requirements for Stochastic Processes","Cairoli, Paoletti, Bortolussi &middot; HSCC 2023","https://www.nicolapaoletti.com/assets/papers/CQR_HSCC23.pdf"),
        ("2023","Towards Invertible Semantic-Preserving Embeddings of Logical Formulae","Saveri, Bortolussi &middot; NeSy 2023",""),
        ("2023","Data-Driven Inference of Chemical Reaction Networks via Graph-Based Variational Autoencoders","Bortolussi, Cairoli, Klein, Petrov &middot; QEST 2023",""),
        ("2023","Model Abstraction and Conditional Sampling with Score-Based Diffusion Models","Bortolussi, Cairoli, Giacomarra, Scassola &middot; QEST 2023",""),
        ("2023","Scalable Stochastic Parametric Verification with Stochastic Variational Smoothed Model Checking","Bortolussi, Cairoli, Carbone, Pulcini &middot; RV 2023",""),
        ("2023","Learning-Based Approaches to Predictive Monitoring with Conformal Statistical Guarantees","Cairoli, Bortolussi, Paoletti &middot; RV 2023",""),
        ("2022","Efficient extraction of seismic reflection with Deep Learning","Roncoroni, Forte, Bortolussi, Pipan &middot; Comput. Geosci.",""),
        ("2022","A Logic for Monitoring Dynamic Networks of Spatially-distributed Cyber-Physical Systems","Nenzi, Bartocci, Bortolussi, Loreti &middot; Log. Methods Comput. Sci.",""),
        ("2022","Resilience of Bayesian Layer-Wise Explanations under Adversarial Attacks","Carbone, Bortolussi, Sanguinetti &middot; IJCNN 2022",""),
        ("2022","Neural Predictive Monitoring for Collective Adaptive Systems","Cairoli, Paoletti, Bortolussi &middot; ISoLA 2022",""),
        ("2022","Learning Model Checking and the Kernel Trick for Signal Temporal Logic on Stochastic Processes","Bortolussi, Gallo, Kret&iacute;nsk&yacute;, Nenzi &middot; TACAS 2022","https://arxiv.org/abs/2201.09928"),
        ("2021","Neural predictive monitoring and a comparison of frequentist and Bayesian approaches","Bortolussi, Cairoli, Paoletti, Smolka, Stoller &middot; STTT",""),
        ("2021","Abstraction of Markov Population Dynamics via Generative Adversarial Nets","Cairoli, Carbone, Bortolussi &middot; CMSB 2021","https://arxiv.org/abs/2106.12981"),
        ("2021","Random Projections for Improved Adversarial Robustness","Carbone, Sanguinetti, Bortolussi &middot; IJCNN 2021",""),
        ("2021","Neural Predictive Monitoring Under Partial Observability","Cairoli, Bortolussi, Paoletti &middot; RV 2021",""),
        ("2020","Fluid approximation of broadcasting systems","Bortolussi, Hillston, Loreti &middot; Theor. Comput. Sci.",""),
        ("2020","Robustness of Bayesian Neural Networks to Gradient-Based Attacks","Carbone, Wicker, Laurenti, Patan&eacute;, Bortolussi, Sanguinetti &middot; NeurIPS 2020",""),
        ("2020","MoonLight: A Lightweight Tool for Monitoring Spatio-Temporal Properties","Bartocci, Bortolussi, Loreti, Nenzi, Silvetti &middot; RV 2020",""),
    ]
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
    pubs=[
        # TODO: add the extended arXiv version when it is out
        ("2026","Certifiably Robust Reinforcement Learning under Spatio-Temporal Logic Specifications","Cairoli, Bortolussi &middot; CDC 2026",""),
        ("2026","Time Robustness for Point-Based Semantics of Metric Interval Temporal Logic","Silvetti, Compagnucci, Cairoli, Trubiani, Nenzi &middot; KR 2026","https://doi.org/10.24963/kr.2026/56"),
        ("2026","Scalable and reliable stochastic parametric verification with stochastic variational smoothed model checking","Cairoli, Bortolussi &middot; Int. J. Syst. Sci.",""),
        ("2026","Localized Anomaly Detection via Differentiable D-vine Copulas","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; CAESAR @ ECML-PKDD 2026","https://arxiv.org/abs/2607.25020"),
        ("2025","Conformal quantitative predictive monitoring of stochastic systems with conditional validity","Cairoli, Kuipers, Bortolussi, Paoletti &middot; Nonlinear Anal. Hybrid Syst.","https://doi.org/10.1016/j.nahs.2025.101606"),
        ("2025","Certified Guidance for Planning with Deep Generative Models","Giacomarra, Hosseini, Paoletti, Cairoli &middot; AAMAS 2025","https://dl.acm.org/doi/10.5555/3709347.3743606"),
        ("2025","CoCAI: Copula-Based Conformal Anomaly Identification for Multivariate Time-Series","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; RV 2025","https://arxiv.org/abs/2507.17796"),
        ("2025","Conformal Predictive Monitoring for Multi-modal Scenarios","Cairoli, Bortolussi, Deshmukh, Lindemann, Paoletti &middot; RV 2025","https://arxiv.org/abs/2509.01338"),
        ("2025","Diffusion-based Time Series Forecasting for Sewerage Systems","Pearson, Cairoli, Bortolussi, Russo, Zanello","https://arxiv.org/abs/2506.08577"),
        ("2025","Guiding Neuro-Symbolic Scenario Generation with Spatio-Temporal Logic","Bonin, Giacomarra, Bortolussi, Deshmukh, Cairoli","https://huggingface.co/papers/2605.19038"),
        ("2024","Towards a Probabilistic Programming Approach to Analyse Collective Adaptive Systems","Randone, Doz, Cairoli, Bortolussi &middot; ISoLA 2024",""),
        ("2023","Data Symmetries and Learning in Fully Connected Neural Networks","Anselmi, Manzoni, d'Onofrio, Rodriguez, Caravagna, Bortolussi, Cairoli &middot; IEEE Access",""),
        ("2023","Generative abstraction of Markov population processes","Cairoli, Anselmi, d'Onofrio, Bortolussi &middot; Theor. Comput. Sci.",""),
        ("2023","Conformal Quantitative Predictive Monitoring of STL Requirements for Stochastic Processes","Cairoli, Paoletti, Bortolussi &middot; HSCC 2023","https://www.nicolapaoletti.com/assets/papers/CQR_HSCC23.pdf"),
        ("2023","Data-Driven Inference of Chemical Reaction Networks via Graph-Based Variational Autoencoders","Bortolussi, Cairoli, Klein, Petrov &middot; QEST 2023",""),
        ("2023","Model Abstraction and Conditional Sampling with Score-Based Diffusion Models","Bortolussi, Cairoli, Giacomarra, Scassola &middot; QEST 2023",""),
        ("2023","Scalable Stochastic Parametric Verification with Stochastic Variational Smoothed Model Checking","Bortolussi, Cairoli, Carbone, Pulcini &middot; RV 2023",""),
        ("2023","Learning-Based Approaches to Predictive Monitoring with Conformal Statistical Guarantees","Cairoli, Bortolussi, Paoletti &middot; RV 2023",""),
        ("2022","Neural Predictive Monitoring for Collective Adaptive Systems","Cairoli, Paoletti, Bortolussi &middot; ISoLA 2022",""),
        ("2021","Abstraction of Markov Population Dynamics via Generative Adversarial Nets","Cairoli, Carbone, Bortolussi &middot; CMSB 2021","https://arxiv.org/abs/2106.12981"),
        ("2021","Neural Predictive Monitoring Under Partial Observability","Cairoli, Bortolussi, Paoletti &middot; RV 2021",""),
    ]
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
    pubs=[
        ("2026","Distilling Formal Logic into Neural Spaces: A Kernel Alignment Approach for STL","Candussio, Sarti, Saveri, Bortolussi &middot; NeSy 2026",""),
        ("2025","Guided by Stars: Interpretable Concept Learning Over Time Series via Temporal Logic Semantics","Ferfoglia, Silvetti, Saveri, Nenzi, Bortolussi","https://arxiv.org/abs/2511.04244"),
        ("2025","Bridging Logic and Learning: Decoding Temporal Logic Embeddings via Transformers","Candussio, Saveri, Sarti, Bortolussi &middot; ECML-PKDD 2025","https://arxiv.org/abs/2507.07808"),
        ("2024","stl2vec: Semantic and Interpretable Vector Representation of Temporal Logic","Saveri, Nenzi, Bortolussi, Kret&iacute;nsk&yacute; &middot; ECAI 2024","https://arxiv.org/abs/2405.14389"),
        ("2024","Is Machine Learning Model Checking Privacy Preserving?","Bortolussi, Nenzi, Saveri, Silvetti &middot; ISoLA 2024",""),
        ("2024","ECATS: Explainable-by-Design Concept-Based Anomaly Detection for Time Series","Ferfoglia, Saveri, Nenzi, Bortolussi &middot; NeSy 2024",""),
        ("2024","Retrieval-Augmented Mining of Temporal Logic Specifications from Data","Saveri, Bortolussi &middot; ECML-PKDD 2024","https://arxiv.org/abs/2405.14355"),
        ("2023","Towards Invertible Semantic-Preserving Embeddings of Logical Formulae","Saveri, Bortolussi &middot; NeSy 2023",""),
        ("2022","Graph Neural Networks for Propositional Model Counting","Saveri, Bortolussi","https://arxiv.org/abs/2205.04423"),
    ]
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
    pubs=[
        ("2026","Time Robustness for Point-Based Semantics of Metric Interval Temporal Logic","Silvetti, Compagnucci, Cairoli, Trubiani, Nenzi &middot; KR 2026","https://doi.org/10.24963/kr.2026/56"),
        ("2025","Guided by Stars: Interpretable Concept Learning Over Time Series via Temporal Logic Semantics","Ferfoglia, Silvetti, Saveri, Nenzi, Bortolussi","https://arxiv.org/abs/2511.04244"),
        ("2024","Is Machine Learning Model Checking Privacy Preserving?","Bortolussi, Nenzi, Saveri, Silvetti &middot; ISoLA 2024",""),
        ("2023","MoonLight: a lightweight tool for monitoring spatio-temporal properties","Nenzi, Bartocci, Bortolussi, Silvetti, Loreti &middot; STTT",""),
        ("2020","MoonLight: A Lightweight Tool for Monitoring Spatio-Temporal Properties","Bartocci, Bortolussi, Loreti, Nenzi, Silvetti &middot; RV 2020",""),
    ]
),
"ballarin": dict(
    name="Emanuele Ballarin",
    role="PhD Candidate &middot; also affiliated with IIT Genova",
    tags=tag("trustworthy GenAI","terracotta")+tag("adversarial robustness","terracotta")+tag("physics-inspired ML","yellow"),
    bio="Best known for CARSO, an adversarial defence mechanism combining adversarial training and purification &mdash; part of the lab's broader effort to make deep generative and discriminative models trustworthy under attack, not just accurate on clean data. Also a co-author of RogueAI, probing whether conversational AI can be trusted to be honest. His PhD thesis is broader still: it covers continuous-time quantum walks, Koopman operator learning, and the Forward-Forward algorithm as a biologically-plausible alternative to backpropagation.",
    pubs=[
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2025","Blending adversarial training and representation-conditional purification via aggregation improves adversarial robustness","Ballarin, Ansuini, Bortolussi &middot; TMLR","https://arxiv.org/abs/2306.06081"),
    ]
),
"candussio": dict(
    name="Sara Candussio",
    role="PhD Student (ADSAI programme)",
    tags=tag("LLM reasoning","green")+tag("chain-of-thought faithfulness","brown")+tag("trustworthy conversational AI","yellow"),
    bio="Studies how large reasoning models actually form their answers during chain-of-thought inference &mdash; and how much of that visible reasoning is real versus decorative. With Daniel Scalena, Gabriele Sarti (Northeastern University), Elisabetta Fersini and Malvina Nissim, she located a \"commitment boundary\" inside reasoning traces: a sharp point where the model locks in its answer, after which further CoT steps are largely epiphenomenal and can be safely cut. This connects to her broader interest in trustworthy and deceptive conversational AI, including RogueAI, a reverse Turing Test deployed as a public web game to test whether people can detect an LLM licensed to lie.",
    pubs=[
        ("2026","Beyond the Commitment Boundary: Probing Epiphenomenal Chain-of-Thought in Large Reasoning Models","Scalena, Candussio, Bortolussi, Fersini, Nissim, Sarti","https://arxiv.org/abs/2606.13603"),
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2026","Distilling Formal Logic into Neural Spaces: A Kernel Alignment Approach for STL","Candussio, Sarti, Saveri, Bortolussi &middot; NeSy 2026",""),
        ("2025","Bridging Logic and Learning: Decoding Temporal Logic Embeddings via Transformers","Candussio, Saveri, Sarti, Bortolussi &middot; ECML-PKDD 2025","https://arxiv.org/abs/2507.07808"),
    ]
),
"scassola": dict(
    name="Davide Scassola",
    role="PhD Candidate",
    tags=tag("neuro-explicit GenAI","terracotta")+tag("diffusion models")+tag("synthetic data","yellow"),
    bio="Works on neuro-explicit generative AI: score-based diffusion and flow-matching models whose outputs are shaped by explicit constraints rather than left to implicit statistical patterns. With Ginevra Carbone, conditions diffusion models on neuro-symbolic constraints; with Sebastiano Saccani and industry partner Aindo SpA, develops flow matching for synthetic relational/tabular data as a trustworthy, privacy-enhancing alternative to sharing real data.",
    pubs=[
        ("2026","Graph-Conditional Flow Matching for Relational Data Generation","Scassola, Saccani, Bortolussi &middot; AAAI 2026","https://ojs.aaai.org/index.php/AAAI/article/view/39712"),
        ("2025","Zero-Shot Conditioning of Score-Based Diffusion Models by Neuro-Symbolic Constraints","Scassola, Saccani, Carbone, Bortolussi &middot; AAAI 2025","https://arxiv.org/abs/2308.16534"),
    ]
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
    pubs=[
        # TODO: switch to the ACL anthology link once the proceedings are out
        ("2026","RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue","Candussio, Ballarin, Bonin, Della Rovere, Bortolussi","https://arxiv.org/abs/2606.13310"),
        ("2025","Enhancing Reinforcement Learning for the Floorplanning of Analog ICs with Beam Search","Della Rovere, Basso, Bortolussi, Videnovic-Misic, Habal &middot; SMACD 2025","https://ieeexplore.ieee.org/document/11092015"),
    ]
),
"della-siega": dict(
    name="Alessandro Della Siega",
    role="MSc Student, Data Science &amp; Artificial Intelligence",
    tags=tag("machine learning"),
    bio="Master's student in Data Science and Artificial Intelligence at the University of Trieste, working with the lab. No publications yet &mdash; add a short bio here once available.",
    pubs=[]
),
"doz": dict(
    name="Romina Doz",
    role="PhD Student (ADSAI programme)",
    tags=tag("neuro-explicit methods","terracotta")+tag("formal methods","yellow")+tag("probabilistic programs"),
    bio="First-year PhD student working in a probabilistic framework, on inference and gradient-based optimization of probabilistic programs &mdash; a neuro-explicit approach to generative modeling where program structure and uncertainty are made explicit rather than learned as a black box. Background in Physics (BSc) and Data Science and Scientific Computing (MSc). Also interested in explainable AI and causality.",
    pubs=[
        ("2026","DeGAS: Gradient-Based Optimization of Probabilistic Programs without Sampling","Randone, Doz, Tribastone, Bortolussi &middot; TACAS 2026","https://arxiv.org/abs/2601.15167"),
        ("2025","Evolutionary Synthesis of Probabilistic Programs","Doz, Randone, Medvet, Bortolussi &middot; GECCO 2025","https://dl.acm.org/doi/10.1145/3712256.3726388"),
    ]
),
"pearson": dict(
    name="Nicholas Andrea Pearson",
    role="PhD Student (ADSAI programme)",
    tags=tag("trustworthy GenAI","terracotta")+tag("diffusion models")+tag("conformal prediction","yellow"),
    bio="Applies neuro-explicit, trustworthy generative AI to a real industrial problem: forecasting and anomaly detection in urban sewerage systems, with conformal statistical guarantees on top of diffusion-based time series models. His most recent work develops differentiable D-vine copulas for localized anomaly detection, refining the conformal anomaly framework introduced with CoCAI. Supervised by prof. Bortolussi in collaboration with Idrostudi Srl. MSc in Data Science and Scientific Computing (2022), BSc in Statistics (2020); previously worked with NielsenIQ on computer vision and information retrieval.",
    pubs=[
        ("2026","Localized Anomaly Detection via Differentiable D-vine Copulas","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; CAESAR @ ECML-PKDD 2026","https://arxiv.org/abs/2607.25020"),
        ("2026","CoCAI: Copula-Based Conformal Anomaly Identification for Multivariate Time-Series","Pearson, Zanello, Russo, Bortolussi, Cairoli &middot; RV 2025","https://arxiv.org/abs/2507.17796"),
        ("2025","Diffusion-based Time Series Forecasting for Sewerage Systems","Pearson, Cairoli, Bortolussi, Russo, Zanello","https://arxiv.org/abs/2506.08577"),
    ]
),
"cusin": dict(
    name="Lorenzo Cusin",
    role="PhD Student",
    tags=tag("trustworthy GenAI","terracotta")+tag("LLM robustness"),
    bio="Bridges the AI Lab with the adjacent Genetic Programming group (Andrea De Lorenzo, Luca Manzoni) on a shared trustworthy-GenAI question: how robust are large language models to adversarial manipulation. Co-author of a genetic-algorithm framework for jailbreaking LLMs, work that feeds directly into the lab's broader effort to understand and close the vulnerabilities of generative models.",
    pubs=[
        ("2025","A Genetic Algorithm Framework for Jailbreaking Large Language Models","Bonin, Cusin, De Lorenzo, Castelli, Manzoni &middot; GECCO Companion 2025","https://dl.acm.org/doi/10.1145/3712255.3734301"),
    ]
),
}

for slug, p in people.items():
    pubs_html = "\n".join(pub(*args) for args in p["pubs"]) if p["pubs"] else '      <p style="color:var(--ink-soft); font-size:14.5px;">No publications listed yet.</p>'
    html = TEMPLATE.format(name=p["name"], role=p["role"], tags=p["tags"], bio=p["bio"], pubs=pubs_html, links=links_html(p.get("links")))
    path = f"people/{slug}/index.html"
    with open(path, "w") as f:
        f.write(html)
    print("wrote", path)
