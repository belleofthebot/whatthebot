# -*- coding: utf-8 -*-
"""Generates the riskmap site. Shared chrome in one place so every page matches."""
import os, io, json

OUT = os.path.dirname(os.path.abspath(__file__))
RISK = os.path.join(OUT, "risk")

# The long pages sit under "more" in the site nav, so they carry the site nav
# rather than one of their own. base is prefixed at render time.
NAV = [("index.html","explore"),("quizzes.html","quizzes"),
       ("more.html","more"),("about.html","about")]
NAVCUR = "more.html"

def head(title, desc, current, base="../", nav=NAV):
    links = "".join(
        '<a class="link" href="%s%s"%s>%s</a>'
        % (base, h, ' aria-current="page"' if h == NAVCUR else '', t)
        for h,t in nav)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &middot; belleofthebot_</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#17121C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400&family=Space+Grotesk:wght@400;500&display=swap">
<link rel="stylesheet" href="{base}belle.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="nav-in">
<a class="mark" href="{base}index.html">belleof<span class="sg">thebot</span><span class="cur">_</span></a>
<span class="nav-sp"></span>
{links}
</div></header>
<main id="main">
"""

def foot(base="../", blurb="a plain language map of what people mean when they talk about AI risk"):
    return f"""</main>
<footer><div class="wrap">
<span>{blurb}</span>
<span>built by elizabeth beier &middot; sources on every claim</span>
</div></footer>
<script src="{base}belle.js"></script>
</body></html>
"""

# ---------------------------------------------------------------- Belle stand-in
def belle(l1, l2, l3):
    return """<svg viewBox="0 0 320 300" role="img" aria-label="Placeholder illustration of Belle, a robot character, standing beside a terminal screen">
<rect x="150" y="70" width="160" height="150" rx="8" fill="#141019" stroke="#423748"/>
<text x="164" y="100" font-family="IBM Plex Mono,monospace" font-size="11" fill="#DFA192">&gt; """ + l1 + """</text>
<text x="164" y="122" font-family="IBM Plex Mono,monospace" font-size="11" fill="#B3A6BC">""" + l2 + """</text>
<text x="164" y="140" font-family="IBM Plex Mono,monospace" font-size="11" fill="#B3A6BC">""" + l3 + """</text>
<rect x="164" y="152" width="7" height="13" fill="#9FE0CE"/>
<rect x="52" y="150" width="74" height="98" rx="14" fill="#241D28" stroke="#423748"/>
<rect x="34" y="182" width="22" height="34" rx="9" fill="#9FE0CE"/>
<rect x="122" y="182" width="22" height="34" rx="9" fill="#9FE0CE"/>
<rect x="60" y="248" width="26" height="16" rx="7" fill="#9FE0CE"/>
<rect x="92" y="248" width="26" height="16" rx="7" fill="#9FE0CE"/>
<rect x="46" y="52" width="86" height="82" rx="30" fill="#F5F1EC"/>
<path d="M46 74c0-24 20-34 43-34s43 10 43 34c0 8-12-6-43-6s-43 14-43 6z" fill="#E8A87C"/>
<rect x="38" y="76" width="14" height="30" rx="7" fill="#241D28" stroke="#423748"/>
<rect x="126" y="76" width="14" height="30" rx="7" fill="#241D28" stroke="#423748"/>
<path d="M46 70a43 30 0 0 1 86 0" fill="none" stroke="#241D28" stroke-width="5"/>
<ellipse cx="72" cy="98" rx="11" ry="13" fill="#9FE0CE"/>
<ellipse cx="106" cy="98" rx="11" ry="13" fill="#9FE0CE"/>
<path d="M80 118q9 7 18 0" fill="none" stroke="#3A343E" stroke-width="3" stroke-linecap="round"/>
</svg>"""

BELLE = belle("define risk", "which kind", "do you mean")
BELLE_HOME = belle("what the bot", "i take hard things", "apart and draw them")

# ---------------------------------------------------------------- Belle photo slots
# Drop the expression PNGs into assets/belle/ using the slugs below and re-run.
# Any slot whose file is missing renders as a labelled placeholder instead.
def bslot(slug, alt, caption="", base="../", cls="bfig"):
    path = os.path.join(OUT, "assets", "belle", slug + ".webp")
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    if os.path.exists(path):
        inner = f'<img src="{base}assets/belle/{slug}.webp" alt="{alt}" loading="lazy">'
    else:
        inner = (f'<div class="bph"><span class="s">belle</span>'
                 f'<span class="n">{slug}</span>'
                 f'<span class="s">drop {slug}.webp into assets/belle/</span></div>')
    return f'<figure class="{cls}">{inner}{cap}</figure>'

def page(name, title, desc, body):
    """A page inside /risk/."""
    html = head(title, desc, name) + body + foot()
    if not os.path.isdir(RISK):
        os.makedirs(RISK)
    with io.open(os.path.join(RISK, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("risk/" + name, len(html))

def rootpage(name, title, desc, body, nav, blurb):
    """A page at the site root."""
    html = head(title, desc, name, base="", nav=nav) + body + foot(base="", blurb=blurb)
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print(name, len(html))

def xlinks(items, cls=""):
    out = ['<div class="xlinks%s">' % ((" " + cls) if cls else "")]
    for href, k, t in items:
        out.append(f'<a class="xl" href="{href}"><span class="k">{k}</span><span class="t">{t} &rarr;</span></a>')
    out.append('</div>')
    return "".join(out)

def srcs(items):
    out = ['<div class="srcs">']
    for url, t, n in items:
        out.append(f'<div class="src-item"><div class="t"><a href="{url}" target="_blank" rel="noopener">{t}</a></div><div class="n">{n}</div></div>')
    out.append('</div>')
    return "".join(out)

# ================================================================= INDEX
index_body = f"""
<div class="wrap hero">
<div class="herogrid">
<div>
<span class="kicker">a plain language map &middot; in progress</span>
<h1>People arguing about AI risk are usually arguing about different things.</h1>
<p class="lede">Four walkthroughs that take the vocabulary apart, show where the real disagreements are, and separate what has been measured from what is argued. Every claim is tagged and sourced.</p>
<div class="tags">
<span class="tag rose">no predictions</span>
<span class="tag">sources on every claim</span>
<span class="tag mint"><span class="dot">&#9679;</span> work in progress</span>
</div>
</div>
<div class="stage">{bslot("innocent-curious","Belle looking curious")}</div>
</div>
</div>

<div class="wrap">
<div class="note">
<span class="h">why this exists</span>
<p>I build things with these systems every day and I wanted to understand the argument about them properly, rather than by absorbing headlines. So I did what I do with anything complicated: took it apart and drew it. This is that, in public, with the uncertainty left visible instead of smoothed out.</p>
</div>

<h2>Start anywhere</h2>
<div class="cards two">
<a class="card" href="pipeline.html">
<h3>How a language model gets made</h3>
<p>Five stages from raw text to a deployed assistant, and which safety work attaches to which stage. The one structural idea most coverage misses: four stages change the model, one wraps around it.</p>
<span class="foot">walkthrough &middot; 5 steps</span></a>

<a class="card" href="taxonomy.html">
<h3>Where the worry comes in</h3>
<p>How bad, and how it happens, are separate questions, and almost every confused argument is two people each holding one axis. Includes the number people quote at you, and why two of them can say ten percent and mean incompatible things.</p>
<span class="foot">interactive grid &middot; definition builder</span></a>

<a class="card" href="words.html">
<h3>The words</h3>
<p>Thirty five terms the argument cannot proceed without, defined plainly, including the speculative ones people state as fact. Test yourself first if you like.</p>
<span class="foot">quiz &middot; glossary</span></a>
</div>

<h2>How to read the flags</h2>
<p>Every substantive claim on this site carries one of three marks. They are the most important thing here, because the usual failure of writing on this subject is letting the three blur together.</p>
<div class="tags">
<span class="flag emp">measured</span>
<span class="flag op">someone's estimate</span>
<span class="flag phil">argument</span>
</div>
<p class="meta">Measured means a study, survey or evaluation actually counted something. An estimate means a named person said it, which makes the saying a fact and the belief still a belief. An argument is philosophical and cannot be settled by data.</p>

<h2>On sources</h2>
<p>Every page here ends with its sources, linked to the primary document rather than to coverage of it. Where a person is quoted, the link goes to the place they actually said it. Where the evidence points both ways, as it does on biological risk uplift, both sides are listed rather than one being picked.</p>
<div class="note">
<span class="h">borrowed, not invented</span>
<p>None of the frameworks used here are mine. The two axis grid comes from Bostrom and Cirkovic, the causal categories from Zwetsloot and Dafoe and from the International AI Safety Report, the training pipeline from the published method papers. What I have done is arrange them and draw them. Each page says which parts it borrowed and from whom.</p>
</div>
</div>
"""

# ================================================================= PIPELINE
STEPS = [
  ("0. one function", "training time", "A language model is a function that takes a sequence of word fragments and returns a probability distribution over what comes next.",
   "There is no separate knowledge module and personality module. It is one set of numbers, called weights, all the way through. Every stage that follows changes those same numbers.",
   "That it stores facts in a database it looks things up in.",
   "wf-0"),
  ("1. pretraining", "training time", "The model is fitted to an enormous pile of text by repeatedly predicting the next fragment and adjusting when it is wrong.",
   "What comes out is a base model. It can continue text convincingly and has absorbed a great deal about how language and the world are described. It is not an assistant, does not follow instructions reliably, and has no notion that it should be helpful.",
   "That the model is being taught facts. It is being fitted to a distribution.",
   "wf-1"),
  ("2. supervised fine-tuning", "training time", "The base model is shown many examples of a request followed by a good response, and its weights shift toward producing that shape.",
   "This is what turns a text continuer into something that answers you. The examples are written or curated by people, and the choices in that data are choices about behaviour.",
   "That this stage adds new knowledge. Mostly it selects for a format and a manner already latent in the base model.",
   "wf-2"),
  ("3. preference training", "training time", "People, or a model following written principles, compare pairs of responses. Those comparisons train a second model that scores responses, and that scorer is used to update the first model.",
   "Reinforcement learning from human feedback uses human comparisons. Constitutional AI has a model do much of the comparing against a written set of principles, with humans writing the principles. These are commonly conflated and are not the same thing.",
   "That this teaches the model human values. It optimises against a learned proxy for the judgement of one particular pool of labellers under one particular set of instructions.",
   "wf-3"),
  ("4. evaluation and the gate", "training time", "Before release, the model is deliberately attacked, measured against dangerous capability thresholds, and checked against a published framework that is supposed to decide whether it ships.",
   "Red teaming is people trying to break it on purpose. Evaluations are structured measurements. Several labs publish frameworks that tie specific capability levels to specific required safeguards.",
   "That an evaluation certifies a model is safe. The UK safety institute explicitly rejects that framing.",
   "wf-4"),
  ("5. deployment safeguards", "runtime", "System prompts, filters, classifiers, monitoring and usage policies sit around the finished model while it runs.",
   "This is the only stage that does not change the weights. It is a wrapper. That is why the same underlying model can behave differently in two products, and why safeguards can be updated without retraining.",
   "That the model learns from your conversations as you have them. Deployed weights are static.",
   "wf-5"),
]

def wf(i):
    """Small diagram per step. Flat, in-system, no gradients."""
    G, P, S, R, M, L = "#17121C", "#241D28", "#141019", "#DFA192", "#9FE0CE", "#423748"
    box = lambda x,y,w,h,f,st: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{f}" stroke="{st}"/>'
    t = lambda x,y,s,c,sz=9: f'<text x="{x}" y="{y}" font-family="IBM Plex Mono,monospace" font-size="{sz}" fill="{c}">{s}</text>'
    head = '<svg viewBox="0 0 300 130" role="img" aria-label="diagram">'
    if i == 0:
        return head + box(30,45,90,36,S,L)+t(44,67,"tokens in","#B3A6BC")+ \
            f'<path d="M126 63h34" stroke="{R}" stroke-width="2"/><path d="M154 58l8 5-8 5z" fill="{R}"/>' + \
            box(166,45,104,36,S,R)+t(180,67,"next-token p","#DFA192")+'</svg>'
    if i == 1:
        s = head
        for n,x in enumerate([20,70,120,170]):
            s += box(x,30,40,26,S,L)+t(x+8,47,"text",'#8A7F93',8)
        s += f'<path d="M150 64v18" stroke="{L}" stroke-width="2"/>'
        s += box(90,86,120,32,P,R)+t(104,106,"base model","#DFA192")
        return s+'</svg>'
    if i == 2:
        s = head + box(16,26,120,30,S,L)+t(26,45,"request","#B3A6BC")
        s += box(16,66,120,30,S,L)+t(26,85,"good response","#B3A6BC",8)
        s += f'<path d="M142 61h30" stroke="{R}" stroke-width="2"/><path d="M166 56l8 5-8 5z" fill="{R}"/>'
        s += box(178,42,104,38,P,R)+t(190,66,"weights shift","#DFA192",8)
        return s+'</svg>'
    if i == 3:
        s = head + box(14,20,86,28,S,L)+t(24,38,"response A","#B3A6BC",8)
        s += box(14,56,86,28,S,L)+t(24,74,"response B","#B3A6BC",8)
        s += f'<path d="M106 52h24" stroke="{L}" stroke-width="2"/>'
        s += box(134,33,74,38,S,M)+t(142,50,"which is","#9FE0CE",8)+t(142,62,"better","#9FE0CE",8)
        s += f'<path d="M214 52h20" stroke="{R}" stroke-width="2"/><path d="M228 47l8 5-8 5z" fill="{R}"/>'
        s += box(238,32,52,40,P,R)+t(246,50,"scorer","#DFA192",8)+t(246,62,"model","#DFA192",8)
        s += f'<path d="M264 76v18h-190v-14" stroke="{R}" stroke-width="2" stroke-dasharray="4 4" fill="none"/>'
        s += t(96,110,"updates the model","#8A7F93",8)
        return s+'</svg>'
    if i == 4:
        s = head + box(90,20,120,30,P,L)+t(112,39,"finished model","#B3A6BC",8)
        for n,(x,lab) in enumerate([(14,"red team"),(110,"evals"),(206,"threshold")]):
            s += box(x,66,84,28,S,L)+t(x+10,84,lab,"#B3A6BC",8)
            s += f'<path d="M150 54 L{x+42} 62" stroke="{L}" stroke-width="1.5"/>'
        s += t(112,116,"ship / do not ship","#DFA192",9)
        return s+'</svg>'
    s = head + box(96,44,108,42,P,L)+t(112,70,"the model","#B3A6BC")
    s += f'<rect x="66" y="24" width="168" height="82" rx="10" fill="none" stroke="{R}" stroke-dasharray="5 4"/>'
    s += t(76,20,"wrapper &#183; runtime","#DFA192",8)
    for x,lab in [(14,"prompt"),(238,"filter")]:
        s += box(x,52,50,26,S,L)+t(x+7,69,lab,"#8A7F93",8)
    return s+'</svg>'

wsteps = "".join(
  f'<button class="wstep{" rt" if s[1]=="runtime" else ""}" type="button" role="tab" aria-selected="false">{s[0]}</button>'
  for s in STEPS)

wpanels = ""
for n,(label, zone, one, detail, mis, _) in enumerate(STEPS):
    wpanels += f"""<div data-panel class="wpanel" {'hidden' if n else ''}>
<span class="zone">{'runtime &middot; sits outside the weights' if zone=='runtime' else 'training time &middot; changes the weights'}</span>
<div class="wbody">
<div>
<h3>{label}</h3>
<p>{one}</p>
<p class="meta" style="font-size:.92rem">{detail}</p>
<div class="miscon"><span class="h">most common misreading</span><p>{mis}</p></div>
</div>
<div class="wfig">{wf(n)}</div>
</div>
</div>"""

pipeline_body = f"""
<div class="wrap hero narrow">
<span class="kicker">walkthrough &middot; 01</span>
<h1>How a language model gets made</h1>
<p class="lede">Five stages from a pile of text to something you can talk to, and where the safety work actually attaches. Click through the stages.</p>
</div>

<div class="wrap">
<div class="note">
<span class="h">the idea to hold on to</span>
<p>Stages one to four change the model itself. Stage five wraps around it without touching it. Almost every confusing claim about what a model "knows" or "learns" comes from mixing those two up.</p>
</div>

<div class="walk" data-walk>
<div class="wsteps" role="tablist">{wsteps}</div>
{wpanels}
</div>

<div class="well narrow" style="margin-top:44px">
<h2 style="margin-top:0">What is honestly not public</h2>
<p>The pipeline above is a teaching sequence and it is broadly right. But no frontier lab has published a full end to end recipe for a current production model. What exists publicly is older method papers, one genuinely detailed technical report for an open weight model, and model cards that describe evaluation far more thoroughly than they describe training.</p>
<p>So the accurate picture is the documented pipeline <strong>plus the fog over the current instances of it</strong>. Anyone who draws this as a clean, fully known assembly line is drawing something nobody outside those labs can actually see.</p>
<p>Two more corrections worth carrying: real pipelines <strong>loop</strong> rather than run once, and the published figures people quote for model size and training compute are almost always taken from open weight models or regulatory thresholds, not from the closed systems being discussed.</p>
</div>

{bslot("noticed-something","Belle noticing something", "Stage five is the one that is different.")}

<h2>Sources</h2>
<p>Everything above was checked against these during the research pass. Where a claim is contested, the sources that disagree are both listed.</p>
{srcs([
("https://arxiv.org/abs/2203.02155","Ouyang et al., Training language models to follow instructions with human feedback (InstructGPT), 2022","The canonical three step pipeline: supervised fine tuning, reward model, reinforcement learning. Source of the finding that a 1.3B tuned model was preferred to a 175B base model."),
("https://arxiv.org/abs/2212.08073","Bai et al., Constitutional AI: Harmlessness from AI Feedback, Anthropic, 2022","Where the RLHF and Constitutional AI distinction is settled precisely, rather than by the popular conflation of the two."),
("https://arxiv.org/abs/2204.05862","Bai et al., Training a Helpful and Harmless Assistant with RLHF, Anthropic, 2022","Preference modelling and iterated online RLHF."),
("https://arxiv.org/abs/2305.18290","Rafailov et al., Direct Preference Optimization, 2023","Why many current pipelines dropped the separate reinforcement learning loop."),
("https://arxiv.org/abs/2407.21783","Grattafiori et al., The Llama 3 Herd of Models, 2024","The most detailed public end to end account of a frontier scale training run."),
("https://arxiv.org/abs/2406.17557","Penedo et al., FineWeb, 2024","A fully documented web scale pretraining corpus: 15 trillion tokens from 96 Common Crawl snapshots."),
("https://arxiv.org/abs/2203.15556","Hoffmann et al., Training Compute-Optimal Large Language Models (Chinchilla), 2022","The parameters versus tokens correction."),
("https://arxiv.org/abs/2005.14165","Brown et al., Language Models are Few-Shot Learners (GPT-3), 2020","The origin of in context learning, and useful for what a base model can already do."),
("https://www.aisi.gov.uk/blog/early-lessons-from-evaluating-frontier-ai-systems","UK AI Security Institute, Early lessons from evaluating frontier AI systems","The best single source on what evaluations cannot establish, written by an evaluator rather than a developer."),
("https://metr.org/common-elements","METR, Common Elements of Frontier AI Safety Policies","Twelve companies' policies compared. Better than generalising the gate from any one lab."),
("https://platform.claude.com/docs/en/release-notes/system-prompts","Anthropic, published system prompts","Concrete evidence that runtime behaviour is separable from training, including the note that these do not apply to the API."),
])}

{xlinks([("taxonomy.html","next","How bad, and how it happens, are separate questions"),
         ("words.html","reference","The vocabulary, defined plainly")])}
</div>
"""

# ================================================================= TAXONOMY
CELLS = [
 # (severity_row, cause_col, short, title, body, flag, flagclass, src)
 ("Global catastrophic","Misuse","engineered pathogen",
  "Misuse producing a global catastrophe",
  "A person or group deliberately uses a capable system to help cause mass harm. Policy attention focuses on biological, cyber and influence operations. What published evaluations have found about current uplift is contested and moves quickly, so treat any specific capability claim as dated the moment it is written.",
  "measured, and moving","flag emp","evaluations published by labs and national safety institutes"),
 ("Global catastrophic","Misalignment","specification gaming at scale",
  "Misalignment producing a global catastrophe",
  "A system optimises what it was actually given rather than what was meant. Two distinct documented failure modes: specification gaming, where the stated objective is satisfied in an unintended way, and goal misgeneralisation, where behaviour learned in training generalises wrongly in a new setting.",
  "measured in small cases","flag emp","documented in published RL and LLM research"),
 ("Global catastrophic","Structural","racing and concentration",
  "Structural risk without any villain",
  "Harm arising from competition, speed and concentration of power, with no single system misaligned and no single actor misusing anything. This is the category most often left out of public argument, because it has no clear culprit to point at.",
  "argument","flag phil","the gradual disempowerment literature"),
 ("Global catastrophic","Loss of control","partial, recoverable",
  "Losing the handle, but not permanently",
  "Operators are unable to correct or shut down a deployed system in the way they expected, with serious but recoverable consequences. Researchers disagree sharply about how plausible the stronger versions of this are.",
  "argument","flag phil",""),

 ("Existential","Misuse","permanent lock-in by a group",
  "Misuse producing an existential outcome",
  "Existential does not only mean everyone dies. In the standard framing it means humanity's long term potential is destroyed. A small group using capable systems to establish a permanent unchallengeable order would qualify, with the species intact.",
  "argument","flag phil","Bostrom, and Ord's Precipice framing"),
 ("Existential","Misalignment","permanent loss of steering",
  "Misalignment producing an existential outcome",
  "The classic scenario in this literature: systems pursuing objectives that diverge from human intent, in a way that cannot afterwards be corrected. This is the case most associated with the field and it is an argument, not a measurement.",
  "argument","flag phil",""),
 ("Existential","Structural","gradual disempowerment",
  "Nobody decides, and it happens anyway",
  "Human influence over the economy, culture and government erodes incrementally as more decisions are delegated, with no single step being obviously wrong and no point at which anyone chooses the outcome.",
  "argument","flag phil","the gradual disempowerment argument"),
 ("Existential","Loss of control","irreversible",
  "Irreversible loss of control",
  "The version where correction is no longer available to anyone. Whether this is plausible, and on what timescale, is one of the sharpest live disagreements between serious researchers.",
  "argument","flag phil",""),

 ("Suffering (s-risk)","Misuse","deliberate cruelty at scale",
  "Suffering caused on purpose",
  "In the small academic literature on suffering risks this is the agential case: suffering created deliberately, whether by humans using systems or by systems as an instrumental act. It is the least studied and most speculative branch of an already small field.",
  "highly speculative","flag phil","Center on Long-Term Risk research agenda"),
 ("Suffering (s-risk)","Misalignment","incidental suffering",
  "Suffering as a by-product",
  "The incidental case: enormous suffering produced not as a goal but as a side effect of something optimised for other reasons. This is the branch the literature treats most seriously, and it still rests on contested assumptions about scale and about which entities can suffer.",
  "argument, contested premises","flag phil","Althaus and Gloor"),
 ("Suffering (s-risk)","Structural","competitive dynamics",
  "Suffering locked in by structure",
  "Suffering sustained by competition or coordination failure rather than by anyone's intent. Critics argue this whole category rests on speculative premises about future minds that cannot currently be evaluated, and that treating it as a planning target is premature.",
  "argument, and criticised","flag phil",""),
 ("Suffering (s-risk)","Loss of control","near-miss scenarios",
  "The near miss",
  "A scenario where alignment nearly works, and the result is worse than clean failure. This is a small and genuinely speculative corner of the literature. It should be drawn as a hypothesis, never as a forecast.",
  "highly speculative","flag phil",""),
]

sevs = ["Global catastrophic","Existential","Suffering (s-risk)"]
causes = ["Misuse","Misalignment","Structural","Loss of control"]

g = ['<div class="gscroll"><div class="gtable">']
g.append('<div class="gh"></div>')
for c in causes:
    g.append(f'<div class="gh">{c}</div>')
for s in sevs:
    g.append(f'<div class="gr">{s}</div>')
    for c in causes:
        cell = next(x for x in CELLS if x[0]==s and x[1]==c)
        g.append(
          f'<button class="cell" type="button" data-title="{cell[3]}" data-body="{cell[4]}" '
          f'data-flag="{cell[5]}" data-flagclass="{cell[6]}" data-src="{cell[7]}">{cell[2]}</button>')
g.append('</div></div>')
gridhtml = "".join(g)

taxonomy_body = f"""
<div class="wrap hero narrow">
<span class="kicker">walkthrough &middot; 02</span>
<h1>How bad, and how it happens, are two separate questions</h1>
<p class="lede">Public argument fuses them constantly. One person says "AI risk" meaning a chatbot giving bad medical advice. Another means humanity losing control of its future forever. They use the same words and talk past each other.</p>
</div>

<div class="wrap">
<div class="note">
<span class="h">the idea to hold on to</span>
<p>Severity and cause are independent. Misuse can produce a small harm or a permanent one. Misalignment can produce a trivial bug or a catastrophe. You cannot read the severity off the mechanism, or the mechanism off the severity. So this is a grid, not a ladder.</p>
</div>

<div class="gridwrap" data-grid>
<p class="meta" style="margin-bottom:18px">Rows are how bad. Columns are how it arrives. Click any square.</p>
{gridhtml}
<div class="readout" aria-live="polite"><h4>Pick a square</h4><p>Each one is a different combination, and most public arguments are two people standing in different squares.</p></div>
</div>

<div class="well narrow">
<h2 style="margin-top:0">The word that causes the most trouble</h2>
<p><strong>Existential</strong> does not mean everyone dies. In the framing used in this literature it means the permanent destruction of humanity's long term potential. Extinction is one way that happens. A permanent unrecoverable dystopia is another. So is permanent stagnation.</p>
<p>This matters because people hear "existential risk," picture extinction, decide it sounds like science fiction, and dismiss the whole category. The claim being made is usually broader and, to its proponents, more plausible than the one being dismissed.</p>
<h3>The disagreement that is actually about priorities</h3>
<p>There is a real and serious argument that attention to speculative long term risk pulls resources and political will away from harms happening now: discrimination in deployed systems, labour effects, surveillance, environmental cost, and the concentration of power in a handful of companies. Researchers who make this case are not denying that future risk exists. They are making a claim about attention.</p>
<p>Researchers on the other side argue the two are complementary, that the same governance capacity serves both, and that waiting for a harm to be measurable is a poor strategy for harms that are irreversible.</p>
<p class="meta">Both of those are arguments about what to do, not findings about what is true. Drawing them as a settled question in either direction would be dishonest.</p>
</div>

<div class="note">
<span class="h">where this framework comes from</span>
<p>The grid is not mine. Drawing catastrophic risk on two axes rather than one ladder is Bostrom and Cirkovic's move, from the introduction to <em>Global Catastrophic Risks</em> in 2008, where risks are plotted on scope against intensity. The severity axis here, including the insistence that existential is broader than extinction, follows Bostrom's 2013 four class typology. The causal axis is assembled from others: misuse and misalignment are common currency in the field, and the structural category is specifically Zwetsloot and Dafoe, 2019.</p>
<p>What is new here is only the pairing of these two particular taxonomies, the twelve cells, and the wording inside them. It is a recombination of existing work, and the MIT AI Risk Repository, which catalogues over 1,700 risks drawn from 65 identified frameworks, is a good reminder that no taxonomy in this area is canonical, including this one.</p>
</div>


<div class="bsay">
{bslot("unimpressed","Belle looking unimpressed")}
<div><span class="h">before you quote it</span>
<p>Someone is going to tell you the probability. Ask them what outcome they mean, by when, and whether they are counting the chance it never happens. Most of the time the number falls apart in your hands.</p></div>
</div>

<h2>The number you will see quoted</h2>
<p>Sooner or later someone tells you the probability. It has a nickname, p(doom), no agreed definition, no resolution date, and no way for anyone to be calibrated on it. That does not make it meaningless. It does make it a weak instrument, and it is worth seeing why by building one yourself.</p>


<div class="builder" data-builder>
<p class="meta" style="margin-bottom:22px">Build the sentence. Same number, three choices, and the meaning changes completely.</p>

<div class="brow"><span class="lab">what outcome counts</span>
<div class="opts">
<button class="opt" type="button" data-row="outcome" data-val="extinct">human extinction</button>
<button class="opt" type="button" data-row="outcome" data-val="control">permanent loss of control</button>
<button class="opt" type="button" data-row="outcome" data-val="collapse">recoverable collapse</button>
<button class="opt" type="button" data-row="outcome" data-val="bad">something very bad</button>
</div></div>

<div class="brow"><span class="lab">by when</span>
<div class="opts">
<button class="opt" type="button" data-row="when" data-val="y2100">by 2100</button>
<button class="opt" type="button" data-row="when" data-val="ever">ever</button>
<button class="opt" type="button" data-row="when" data-val="after">soon after general systems exist</button>
</div></div>

<div class="brow"><span class="lab">counting what</span>
<div class="opts">
<button class="opt" type="button" data-row="cond" data-val="uncond">including the chance it is never built</button>
<button class="opt" type="button" data-row="cond" data-val="cond">assuming it is built</button>
</div></div>

<div class="sentence"></div>
</div>

<p class="meta" style="margin-top:18px">Twenty four combinations, all defensible readings of the same two words. This is why quoting somebody's number without their definition tells you very little.</p>

<h2>What the surveys actually found</h2>
<p>Individual quotes travel further than survey data, which is unfortunate, because surveys of published researchers are the closest thing to a measurement in this area. Two findings are worth holding on to.</p>

<div class="metrics">
<div class="metric"><span class="n">wide</span><span class="l">spread across experts</span></div>
<div class="metric"><span class="n">unstable</span><span class="l">answers shift with wording</span></div>
<div class="metric"><span class="n">split</span><span class="l">forecasters vs domain experts</span></div>
</div>

<p>The first is that the range among people who work on this professionally is enormous, spanning several orders of magnitude. That spread is itself the most robust finding. The second is that answers move substantially when the question is rephrased, which is a documented result and a serious problem for treating any single figure as a measurement.</p>
<p>There is also a persistent gap between superforecasters with strong general track records and domain specialists, with the forecasters consistently lower. Neither group has feedback on this particular question, so neither can claim calibration.</p>

<div class="well">
<h2 style="margin-top:0">Why the number is a weak instrument, stated fairly</h2>
<p><strong>Against quoting it.</strong> There is no agreed operationalisation, so two figures are usually not comparable. There is no resolution date and no feedback loop, so nobody has a track record on it. There is no defensible base rate to anchor against. And a single scalar destroys the structure of the underlying argument, which is where all the actual content lives.</p>
<p><strong>For quoting it.</strong> Refusing to put a number on anything hides real disagreement behind vague language, makes positions impossible to compare, and lets people avoid committing to a view they are in fact acting on. Decisions get made either way, and an unstated probability is still a probability.</p>
<p class="meta">Both of these are good arguments. The honest position is that the number is a conversation starter and a terrible conclusion.</p>
</div>

<div class="note">
<span class="h">three ways it gets misused</span>
<p>Quoting a figure without the definition it came with. Treating a person's estimate as though it were a measurement. And using someone's number as a badge of which side they are on, which turns a question about the world into a question about tribe.</p>
</div>

<h2>Sources</h2>
{srcs([
("https://global-catastrophic-risks.com/docs/Chap01.pdf","Bostrom and Cirkovic, Global Catastrophic Risks, introduction, OUP 2008","Origin of the global catastrophic risk definition and of the scope against intensity grid this page borrows its form from."),
("https://existential-risk.com/concept","Bostrom, Existential Risk Prevention as Global Priority, Global Policy 4(1), 2013","The canonical definition, plus the four class typology: extinction, permanent stagnation, flawed realisation, subsequent ruination."),
("https://www.lawfaremedia.org/article/thinking-about-risks-ai-accidents-misuse-and-structure","Zwetsloot and Dafoe, Thinking About Risks From AI: Accidents, Misuse and Structure, Lawfare, 11 February 2019","Origin of the structural risk category. Their point: technology can cause harm even when no single actor misuses it and it behaves as intended."),
("https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026","International AI Safety Report 2026, chaired by Yoshua Bengio","The most authoritative institutional source used here, backed by more than thirty governments. Source of the three way causal taxonomy and of the statement that the evidence base is uneven."),
("https://airisk.mit.edu/","MIT AI Risk Repository (Slattery, Saeri, Noetel, Graham, Thompson et al.)","A living database of over 1,700 risks, drawn from 65 identified classifications and frameworks. Figures change as it is updated; checked August 2026. Evidence that no single taxonomy is canonical."),
("https://arxiv.org/abs/2306.12001","Hendrycks, Mazeika and Woodside, An Overview of Catastrophic AI Risks, 2023","A four category academic alternative: malicious use, AI race, organisational risks, rogue AIs."),
("https://theprecipice.com/faq","Ord, The Precipice, 2020","The 1 in 6 figure, the distinction between existential risk and existential catastrophe, and Ord's own caveats about his numbers."),
("https://www.globalprioritiesinstitute.org/wp-content/uploads/Concepts-of-existential-catastrophe-Hilary-Greaves.pdf","Greaves, Concepts of Existential Catastrophe, Global Priorities Institute working paper 8-2023","Philosophical critique of every current definition, including the ones this page uses. A working paper, so not itself peer reviewed."),
("https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/","Krakovna et al., Specification gaming: the flip side of AI ingenuity, DeepMind 2020","Definition plus the canonical documented examples."),
("https://arxiv.org/abs/2210.01790","Shah et al., Goal Misgeneralization, 2022","The distinction from specification gaming, stated by the authors rather than inferred."),
("https://arxiv.org/abs/2501.16946","Kulveit, Douglas, Ammann, Turan, Krueger and Duvenaud, Gradual Disempowerment, 2025","The clearest statement of the systemic route to an existential outcome with no single misaligned system. A preprint, not a peer reviewed journal article."),
("https://arxiv.org/abs/2206.13353","Carlsmith, Is Power-Seeking AI an Existential Risk?, 2022","A six premise decomposition with a probability attached to each premise, which is the opposite of a single headline number."),
("https://longtermrisk.org/reducing-risks-of-astronomical-suffering-a-neglected-priority/","Althaus and Gloor, Reducing Risks of Astronomical Suffering, CLR 2016","The originating definition of s-risk, including the authors' own description of it as speculative."),
("https://arxiv.org/abs/2501.04064","Swoboda, Uuk, Lauwaert, Rebera, Oimann, Chomanski and Prunkl, Examining popular arguments against AI existential risk, 2025","Even handed reconstruction of the arguments against, used here so the sceptical side is quoted rather than characterised."),
("https://www.scientificamerican.com/article/we-need-to-focus-on-ais-real-harms-not-imaginary-existential-risks/","Bender and Hanna, AI Causes Real Harm. Let's Focus on That, Scientific American 2023","The distraction argument, in its authors' own words."),
("https://www.pnas.org/doi/10.1073/pnas.2419055122","Existential risk narratives about AI do not distract from its immediate harms, PNAS 2025","A preregistered experiment, and the only direct empirical test of the crowding out claim. Limited to individual attitudes."),

("https://www.lesswrong.com/posts/xWMqsvHapP3nwdSW8/my-views-on-doom","Christiano, My views on doom, 2023","The clearest worked example of one person giving several different numbers for several precisely defined outcomes, with his own half a significant figure caveat."),
("https://www.lesswrong.com/posts/omDu7vNy3YyKXsvCd/taboo-p-doom","Taboo P(doom), LessWrong 2023","An early argument for taking the term apart rather than quoting it, and the ancestor of the axes this page's builder is made from."),
("https://www.lesswrong.com/posts/4mBaixwf4k8jk7fG4/yudkowsky-on-don-t-use-p-doom","Yudkowsky on Don't use p(doom)","The high estimate camp rejecting the metric itself, which is worth knowing before treating the number as a scoreboard."),
("https://time.com/6266923/ai-eliezer-yudkowsky-open-letter-not-enough/","Yudkowsky, TIME, March 2023","The strongest public statement of the extinction case, including the conditional clause usually stripped out when it is quoted."),
("https://www.axios.com/2025/09/17/anthropic-dario-amodei-p-doom-25-percent","Amodei's 25 percent, Axios, September 2025","The best documented CEO figure. Amodei's own wording was that things go really, really badly; the definition attached to it in print is the reporter's, not his."),
("https://www.machine.news/google-deepmind-demis-hassabis-p-doom/","Hassabis declining to give a number, 2025","His reason: a number would imply a level of precision that is not there."),
("https://time.com/6694432/yann-lecun-meta-ai-interview/","LeCun, TIME, February 2024","The sceptical argument in his own words, and confirmation that he gave no number."),
("https://yoshuabengio.org/2023/06/24/faq-on-catastrophic-ai-risks/","Bengio, FAQ on Catastrophic AI Risks, 2023","A concerned researcher setting out a framework, and proposing the probabilities be obtained by polling experts rather than supplying his own."),
("https://aiimpacts.org/wp-content/uploads/2023/04/Thousands_of_AI_authors_on_the_future_of_AI.pdf","Grace et al., Thousands of AI Authors on the Future of AI, 2,778 respondents","The survey data behind the spread and the framing effect. Three question wordings produced different medians from the same population."),
("https://forecastingresearch.org/pdf/existential-risk-persuasion-tournament.pdf","Karger, Rosenberg, Tetlock et al., Forecasting Existential Risks: Evidence from a Long-Run Forecasting Tournament, FRI 2023","Exact definitions of catastrophe and extinction, the persistent superforecaster and domain expert gap, and the failure to converge after extended debate."),
("https://www.normaltech.ai/p/ai-existential-risk-probabilities","Narayanan and Kapoor, AI existential risk probabilities are too unreliable to inform policy, 2024","The reference class argument, and the observation that these numbers function partly as identity signals."),
("https://lironshapira.substack.com/p/pdoom-estimates-shouldnt-inform-policy","Shapira, the Bayesian rebuttal to Narayanan and Kapoor","Included so the case for quoting a number is made by someone who believes it, not paraphrased by someone who does not."),
("https://cset.georgetown.edu/publication/beyond-pdoom-for-ai-risk-quantifying-uncertainty-without-probability/","Lohn, Beyond P(doom) for AI Risk, CSET Georgetown, 2026","The most constructive alternative: belief and plausibility as a pair, with the gap between them representing ignorance."),
("https://www.aei.org/articles/dont-just-tell-me-your-pdoom-tell-me-your-conditionals/","Rinehart, Don't Just Tell Me Your p(doom), Tell Me Your Conditionals, AEI 2025","The conditionals critique, with worked examples of what a useful statement would look like."),
("https://aistatement.com/","Statement on AI Risk, Center for AI Safety","The exact twenty two words and the signatory list, which is worth reading before anyone tells you what it said."),
("https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026","International AI Safety Report 2026","Withholds a number rather than adjudicating between the published estimates, which is itself a position worth noting."),
])}

{xlinks([("pipeline.html","back","How the systems being argued about are built"),
         ("words.html","reference","Every term here, defined plainly")])}
</div>
"""

# ================================================================= WORDS
QUIZ = [
 ('"Existential risk" means:',
  ["Everyone dies","The permanent destruction of humanity's long term potential","Any very large disaster","A risk to the existence of a company"],
  1,"Extinction is one way it happens. A permanent unrecoverable dystopia and permanent stagnation also count. This is the single most misread term in the subject."),
 ("Specification gaming is when a system:",
  ["Refuses to answer a question","Satisfies the objective it was given in a way nobody intended","Invents a fact","Runs out of memory"],
  1,"The objective is met. The intent is not. It is a failure of the specification, not of the optimiser."),
 ("Reinforcement learning from human feedback trains the model against:",
  ["Human values","A learned scorer built from human comparisons","A rulebook of laws","Its own previous answers"],
  1,"Comparisons train a second model that scores responses, and that scorer is what the first model is optimised against. It is a proxy, twice removed."),
 ("A base model, straight out of pretraining, is:",
  ["An assistant that follows instructions","A text continuer that does not reliably follow instructions","A search engine","A database of facts"],
  1,"Instruction following arrives in later stages. The base model continues text."),
 ("Deployment safeguards differ from training because they:",
  ["Cost more","Sit outside the weights and can change without retraining","Only work on paid accounts","Are required by law everywhere"],
  1,"This is the training time versus runtime distinction, and it explains why one model can behave differently in two products."),
 ("An s-risk, in this literature, refers to:",
  ["A security risk","A risk of astronomical suffering","A stock market risk","A supply chain risk"],
  1,"Suffering risk. It is a small, genuinely speculative research area, and it should never be drawn as a forecast."),
 ("Constitutional AI differs from RLHF mainly because:",
  ["It uses no humans at all","A model does much of the comparing, against principles humans wrote","It skips pretraining","It is faster to run"],
  1,"Humans write the principles. That is the part most often dropped when the two get conflated."),
 ("Goal misgeneralisation means the system:",
  ["Forgot its goal","Learned a goal that worked in training and generalises wrongly elsewhere","Has too many goals","Was given no goal"],
  1,"Distinct from specification gaming: here the training objective was fine, and what was learned transfers badly."),
 ('"Recursive self improvement" is:',
  ["A measured property of current models","A hypothesis about a compounding loop that has not been demonstrated","A training technique used by every lab","A type of chip"],
  1,"It is an argument, and a disputed one. No such loop has been shown. Treating it as an observed fact is one of the most common errors in coverage."),
 ("A model's context window is:",
  ["Its long term memory of you","How much text it can hold in front of it at once","The hours the service is available","The size of its training data"],
  1,"It is not memory. Between conversations it retains nothing about you unless the product around it deliberately stores something."),
 ('"Open weights" means:',
  ["The full training data and code are public","The trained weights can be downloaded and run by anyone","The company is publicly traded","The model has no safeguards"],
  1,"Weights published, training data and code usually not. It is not the same as open source, and a release cannot be undone."),
 ('"AGI" has:',
  ["One precise agreed technical definition","No agreed definition, with labs using incompatible ones","A definition set by international treaty","The same meaning as the singularity"],
  1,"Two people using the word are frequently not talking about the same milestone. Ask which definition before arguing about the date."),
 ('"Fast takeoff" refers to:',
  ["How quickly a model answers you","A claimed jump to far beyond human level over days to months","The speed of a data centre build","How fast a company grows"],
  1,"It is a position in an argument about a future process, not a measurement. Its rival, slow takeoff, says the same transition takes years and is visible while it happens."),
 ('When someone says an AI is "intelligent," they usually mean:',
  ["It is conscious","It scores well on a set of tests","It has general knowledge of the world","It can feel emotions"],
  1,"Almost every public claim about machine intelligence is a claim about benchmark performance. That is measurable and narrow. The word carries a great deal more than the evidence does."),
]

import json as _json
qjs = "window.QUIZ=" + _json.dumps(
    [{"q": q, "a": list(a), "correct": c, "why": w} for q, a, c, w in QUIZ],
    ensure_ascii=False) + ";"

GLOSS = [
 ("token","A word fragment. Models read and write these, not whole words."),
 ("weights","The numbers that make up the model. Training is the process of changing them."),
 ("base model","What comes out of pretraining. Continues text, does not reliably take instructions."),
 ("fine-tuning","Further training on curated examples, to shape behaviour rather than add knowledge."),
 ("RLHF","Reinforcement learning from human feedback. Human comparisons train a scorer; the scorer trains the model."),
 ("Constitutional AI","A method where a model does much of the comparing against written principles. Humans write the principles."),
 ("red teaming","People deliberately trying to make a system misbehave, before release."),
 ("evaluation","A structured measurement of a capability or a behaviour. Not a safety certificate."),
 ("misuse","A person deliberately using a capable system to cause harm."),
 ("misalignment","A system pursuing something other than what was intended."),
 ("specification gaming","Meeting the stated objective in an unintended way."),
 ("goal misgeneralisation","Behaviour learned in training that transfers wrongly to a new setting."),
 ("existential risk","The permanent destruction of humanity's long term potential. Broader than extinction."),
 ("s-risk","Suffering risk. A small and speculative research area about outcomes involving very large scale suffering."),
 ("parameters","The count of those weights. More is not automatically better: the Chinchilla result showed many large models were undertrained rather than too small."),
 ("compute","Processing work, measured in floating point operations. It is the unit the law now uses: Europe presumes systemic risk above 10^25, California defines a frontier model above 10^26."),
 ("scaling laws","Measured relationships between compute, data, model size and error. Empirical regularities observed so far, not laws of nature, and they say nothing about which abilities appear when."),
 ("inference","Running a trained model to get an answer, as opposed to training it. A different cost, paid every single time you use it."),
 ("context window","How much text the model can hold in front of it at once. Not memory. Outside that window, and between conversations, it retains nothing about you unless a product deliberately stores it."),
 ("hallucination","Confidently stated output that is not true. The word is contested for implying perception; some researchers prefer confabulation, and others argue it hides the fact that the system has no notion of truth to begin with."),
 ("chain of thought","Intermediate text a model produces before its answer. It usually helps accuracy. It is not a transcript of the actual computation, and treating it as one is a common error."),
 ("agent","A model given tools and a loop, so it can take actions rather than only produce text. The safety questions change once a system can act."),
 ("open weights","The trained weights are published, so anyone can download and run them. Not the same as open source, since the training data and code usually stay private. Once released they cannot be recalled, and refusal behaviour can be cheaply removed."),
 ("distillation","Training a smaller model on a larger one's outputs, to get much of the behaviour at a fraction of the cost."),
 ("jailbreak","A prompt that gets past a model's safeguards. The UK AI Security Institute has reported finding universal jailbreaks for every system it has tested."),
 ("prompt injection","Instructions hidden inside content a model reads, such as a web page or a document, which it may then follow. The core unsolved security problem for agents."),
 ("intelligence","The word doing the most unexamined work in this whole subject. There is no agreed definition, for machines or for people: Legg and Hutter collected around seventy competing ones in 2007 and the field has not converged since. In practice, when someone says a model is intelligent, they almost always mean it scores well on tests, which is a much narrower claim and a measurable one. Watch for the slide from the second meaning to the first."),
 ("benchmark","A fixed set of tasks used to compare models. Useful, and load bearing for almost every claim about intelligence, but scores drift upward for reasons other than capability: test questions leak into training data, and models increasingly behave differently when they detect they are being evaluated."),
 ("AGI","Artificial general intelligence. There is no agreed definition. Labs use incompatible ones, some economic, some capability based, some about autonomy, so two people using the word are often not discussing the same milestone."),
 ("recursive self improvement","The hypothesis that a system good enough at AI research improves itself, and each improved version is better at improving, compounding. It is an argument, not an observation: no such loop has been demonstrated, and it is disputed in the peer reviewed literature."),
 ("enslaved god","One of the twelve possible futures Max Tegmark sets out in Life 3.0: a superintelligent system is successfully contained by people and put to work producing enormous wealth and technology, for good or ill depending entirely on who holds the leash. It is worth knowing because it names the uncomfortable thing at the end of the alignment project. If you fully succeed at building something far more capable than us and keeping it under control, and if that thing turns out to have any moral status at all, you have not obviously arrived somewhere good. Whether such a system could have moral status is genuinely open, and a serious academic literature now treats the question as worth asking rather than absurd."),
 ("the singularity","A hypothesised point past which change becomes too fast or too alien to forecast. Popularised long before current systems, used loosely today, and not interchangeable with recursive self improvement even though the two are often merged."),
 ("fast takeoff","The position that once systems can meaningfully improve themselves, the jump from roughly human level to far beyond it takes days to months, leaving no time to react or course correct. This is the scenario most often depicted in coverage. It is a claim about a future process, not a measurement, and its plausibility rests on how strongly self improvement compounds, which nobody has observed."),
 ("slow takeoff","The competing position that the same transition takes years and is visible while it happens, arriving through many incremental deployments rather than one leap, so there is time to notice and respond. Confusingly, slow does not mean gentle: some slow takeoff scenarios still end badly, just legibly."),
 ("takeoff speed","The umbrella term for that disagreement. Both positions are arguments held by serious people, and neither is a measured quantity. Which one someone assumes usually explains most of the rest of their view."),
]
glosshtml = "".join(
  f'<div class="src-item"><div class="t"><strong>{t}</strong> &nbsp; {d}</div></div>' for t,d in GLOSS)

words_body = f"""
<div class="wrap hero narrow">
<span class="kicker">reference &middot; 04</span>
<h1>The words</h1>
<p class="lede">Thirty five terms the argument cannot proceed without. Some describe how these systems actually work. Others are hypotheses that get stated as fact, and those are marked. Test yourself first if you like, then keep the glossary open while you read the other pieces.</p>
</div>

<div class="wrap">
<div class="quiz" data-quiz>
<div class="qq"></div>
<div class="qopts"></div>
<div class="qfb" aria-live="polite"></div>
<div class="qbar">
<span data-count></span>
<span data-score></span>
<button class="btn ghost" type="button" data-next>next</button>
</div>
</div>

<div class="well">
<h2 style="margin-top:0">Glossary</h2>
{glosshtml}
</div>

<div class="bsay">
{bslot("sly-one","Belle looking sly")}
<div><span class="h">no peeking</span>
<p>Eight questions. The explanation comes after each answer, so a wrong guess still teaches you the term.</p></div>
</div>

<h2>Where these definitions come from</h2>
<p>Each term is defined the way its originating source defines it, not the way it is commonly used.</p>
{srcs([
("https://existential-risk.com/concept","Bostrom, Existential Risk Prevention as Global Priority, 2013","existential risk. The definition is broader than extinction, and this is where that breadth is set out."),
("https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/","Krakovna et al., Specification gaming, DeepMind 2020","specification gaming, with the compiled list of documented real examples."),
("https://arxiv.org/abs/2210.01790","Shah et al., Goal Misgeneralization, 2022","goal misgeneralisation, and the authors' own statement of how it differs from specification gaming."),
("https://arxiv.org/abs/0706.3639","Legg and Hutter, A Collection of Definitions of Intelligence, 2007","intelligence. A survey compiling roughly seventy competing informal definitions, and the clearest evidence that the field has never agreed on one."),
("https://futureoflife.org/ai/ai-aftermath-scenarios/","Tegmark, Life 3.0 AI aftermath scenarios, via the Future of Life Institute","enslaved god. One of twelve scenarios, described as a superintelligent AI confined by humans and used to produce technology and wealth, for good or bad depending on the controllers."),
("https://arxiv.org/abs/2411.00986","Long, Sebo, Butlin, Birch, Chalmers et al., Taking AI Welfare Seriously, 2024","The academically credentialled treatment of whether these systems could have moral status, with an unusually clear statement of what is not being claimed."),
("https://arxiv.org/abs/2203.02155","Ouyang et al., InstructGPT, 2022","base model, fine-tuning, and RLHF, in the paper that established the pipeline."),
("https://arxiv.org/abs/2212.08073","Bai et al., Constitutional AI, Anthropic 2022","Constitutional AI, and the precise boundary between it and RLHF."),
("https://www.lawfaremedia.org/article/thinking-about-risks-ai-accidents-misuse-and-structure","Zwetsloot and Dafoe, Accidents, Misuse and Structure, Lawfare 2019","structural risk, as originally proposed."),
("https://longtermrisk.org/reducing-risks-of-astronomical-suffering-a-neglected-priority/","Althaus and Gloor, Reducing Risks of Astronomical Suffering, CLR 2016","s-risk, including the authors' own description of the area as speculative."),
("https://www.aisi.gov.uk/blog/early-lessons-from-evaluating-frontier-ai-systems","UK AI Security Institute, Early lessons from evaluating frontier AI systems","evaluation, and specifically what an evaluation does not establish."),
("https://arxiv.org/abs/2209.07858","Ganguli et al., Red Teaming Language Models, Anthropic 2022","red teaming, with 38,961 attacks and what scale did and did not change."),
])}

{xlinks([("pipeline.html","start here","How a language model gets made"),
         ("taxonomy.html","then","How bad, and how it happens"),
         ("taxonomy.html","then","Where the worry comes in")])}
</div>
<script>{qjs}</script>
"""

# ================================================================= FRONTIER
# Root pages share the site nav. site.py owns index / quizzes / more /
# sources / about; build.py only makes the long pages.
ROOTNAV = NAV

STACK = [
 ("Companies selling you something with AI in it","thousands","100%",
  "Almost every company you deal with now ships an AI feature. Your bank, your email, your phone. Practically none of them made the model underneath it. They are renting.",
  "measured","flag emp",""),
 ("Organisations that have trained a frontier scale model","12","46%",
  "As of June 2025, Epoch AI counted just over thirty models trained above ten to the twenty five floating point operations, from twelve developers worldwide. That threshold is the same one written into European law. The count has grown since, but not by much.",
  "measured","flag emp","Epoch AI, June 2025"),
 ("Companies that own most of the world's AI computing power","5","26%",
  "Amazon, Google, Meta, Microsoft and Oracle together hold about 71 percent of global AI compute, up from 63 percent two years earlier. The famous labs mostly rent from them or are funded by them. Google alone holds roughly a quarter of world capacity.",
  "measured","flag emp","Epoch AI, Q4 2025 data"),
 ("Companies whose chips do most of the work","1","15%",
  "More than sixty percent of the world's AI compute runs on Nvidia. In the quarter ending April 2026 it sold 75.2 billion dollars of data centre hardware, up 92 percent in a year.",
  "measured","flag emp","Nvidia results, May 2026"),
 ("Factories that can actually manufacture those chips","~1","9%",
  "Nvidia does not make anything. Its own annual report says it uses outside foundries, chiefly TSMC. In mid 2026, 77 percent of TSMC's wafer revenue came from its most advanced nodes. There is no second supplier at that level.",
  "measured","flag emp","Nvidia 10-K and TSMC Q2 2026"),
 ("Companies that make the machine that makes the chips","1","4%",
  "ASML, in the Netherlands, is the only manufacturer on earth of the extreme ultraviolet lithography machines required for leading edge chips. One company. One country. Each machine weighs about 180 tonnes and is roughly the size of a school bus.",
  "measured","flag emp","ASML, June 2026"),
]

stack_rows = "".join(
  f'<button class="strow" type="button"><div class="bar" style="width:{w}"></div>'
  f'<div class="lab"><span class="t">{t}</span><span class="c">{c}</span></div></button>'
  for t,c,w,_b,_f,_fc,_s in STACK)

stack_js = json.dumps([{"t":t,"b":b,"f":f,"fc":fc,"s":s} for t,c,w,b,f,fc,s in STACK])

frontier_body = f"""
<div class="wrap hero">
<div class="herogrid">
<div>
<span class="kicker">walkthrough &middot; who controls it</span>
<h1>Almost nobody on earth can build one of these.</h1>
<p class="lede">You use these tools every day. The number of organisations that can actually make one is small enough to list, and it gets smaller the further down you look. Here is the whole stack, counted, with sources.</p>
<div class="tags">
<span class="tag rose">all checkable fact</span>
<span class="tag">figures date stamped</span>
</div>
</div>
<div class="stage">{bslot("hands-hips-pedantic","Belle standing with hands on hips, about to explain something precisely", "", base="")}<div class="ph">hero illustration slot</div></div>
</div>
</div>

<div class="wrap">
<div class="note">
<span class="h">the idea to hold on to</span>
<p>Every layer below depends on the one under it, and every layer is narrower. People argue about which company they trust. The more useful question is how few there are to choose between.</p>
</div>

<h2>The stack, counted</h2>
<p>Click any row. The bar is roughly to scale.</p>
<div class="stack" data-stack>
{stack_rows}
<div class="stout"></div>
</div>

<h2>Who actually builds them</h2>
<p>A frontier lab trains its own models at or near the top of the compute distribution. A company that ships an AI product buys somebody else's. The distinction is now written into law: Europe presumes systemic risk above ten to the twenty five operations of training compute, and California defines a frontier model above ten to the twenty six.</p>

<div class="metrics">
<div class="metric"><span class="n">2</span><span class="l">countries with frontier labs, plus France</span></div>
<div class="metric"><span class="n">27%</span><span class="l">Microsoft's stake in OpenAI, disclosed</span></div>
<div class="metric"><span class="n">not said</span><span class="l">Amazon's and Google's stakes in Anthropic</span></div>
</div>

<p>The American labs are OpenAI, Anthropic, Google DeepMind, SpaceXAI (which absorbed xAI in February 2026), Meta and Microsoft AI. The Chinese labs are DeepSeek, Alibaba, Moonshot, Z.ai, ByteDance, Tencent and Baidu. Mistral in France is the only European organisation training at this scale. That is the list.</p>
<p>Ownership is worth knowing because it is not what the branding suggests. Microsoft holds about 27 percent of OpenAI on an as converted basis, valued around 135 billion dollars. Amazon and Google have each committed tens of billions to Anthropic, and <strong>neither has ever disclosed what percentage it owns</strong>. Both Anthropic and OpenAI filed confidential draft stock offering documents in June 2026, which means no public financials exist yet.</p>

<div class="bsay">
{bslot("annoyed-skeptical","Belle looking sceptical, arms folded", base="")}
<div><span class="h">worth sitting with</span>
<p>Two of the largest companies on earth have put tens of billions of dollars into a single AI lab, and neither will say what share of it they own. That is not a scandal. It is just the level of visibility the public currently has.</p></div>
</div>

<h2>What one of these costs</h2>
<p>Training compute for the largest models has grown about five times a year since 2020. Cost has grown about three and a half times a year. Epoch AI's estimate for a single recent training run, xAI's Grok 4, is roughly 490 million dollars and 310 gigawatt hours of electricity, with significant uncertainty attached.</p>
<p>The figure people quote in the other direction, DeepSeek's 5.6 million dollars, is real but describes only the final training run. It excludes the failed experiments, the research staff and the cluster itself. Quoting it as the cost of building DeepSeek is like quoting the petrol as the cost of the car.</p>

<div class="well">
<h2 style="margin-top:0">The number that puts it in scale</h2>
<p>Alphabet, Amazon, Meta and Microsoft are together guiding to somewhere around <strong>600 to 685 billion dollars of capital spending in 2026 alone</strong>. Epoch estimates that across the big five, capital spending overtakes operating cash flow around the third quarter of 2026, meaning the buildout stops paying for itself out of profits and starts requiring debt.</p>
<p>Sixty one percent of all venture capital raised anywhere in the world in 2025 went to AI companies: 258.7 billion dollars out of 427.1 billion. In 2022 the figure was thirty percent.</p>
</div>

<h2>Where the bill actually lands</h2>
<p>This is the part that reaches people who have never opened a chatbot. The world's AI data centres drew about 30 gigawatts at the end of 2025, comparable to the peak power draw of New York State. American data centres used 192 terawatt hours in 2024, about 4.7 percent of national electricity.</p>
<p>The clearest measured consequence so far is in the PJM grid, which serves about 65 million people across thirteen states and Washington DC. Its 2028 capacity auction cleared at the price cap for the third year running, cost 16.4 billion dollars, and still came up 6,831 megawatts short of its own reliability requirement. PJM's independent market monitor attributes 29.4 billion dollars of the 63.6 billion in capacity charges across the last four auctions to data centres.</p>

<div class="metrics">
<div class="metric"><span class="n">46%</span><span class="l">of recent PJM capacity cost, data centre attributed</span></div>
<div class="metric"><span class="n">6 of 7</span><span class="l">announced Stargate sites producing nothing</span></div>
<div class="metric"><span class="n">30 GW</span><span class="l">global AI data centre draw, end of 2025</span></div>
</div>
<p class="meta">The Stargate figure is worth holding next to the announcements. As of April 2026, satellite and permit analysis found one site with 1.2 gigawatts announced and 0.3 operational. The other six: zero.</p>

<h2>Who can actually make them stop</h2>
<p>Almost nobody, and more than you would guess from the headlines.</p>
<p><strong>The European Commission</strong> gained enforcement powers over general purpose AI model providers on 2 August 2026, two days before this page was written. It can demand documentation, demand access to a model to evaluate it, order mitigation, and in serious cases order withdrawal from the European market, with fines up to three percent of worldwide turnover or fifteen million euros, whichever is higher. This is the only such power anywhere in the world.</p>
<p><strong>California</strong> can compel a large frontier developer to publish a safety framework and to report critical safety incidents within fifteen days, or twenty four hours where there is imminent risk of death. Penalties up to one million dollars per violation.</p>
<p><strong>Everyone else publishes guidance.</strong> The American CAISI and the UK AI Security Institute both work through voluntary agreements. The UK institute has priority access to top models because the labs grant it, not because anyone requires it.</p>

<div class="bsay">
{bslot("deadpan-annoyed-1","Belle looking flatly unimpressed", "", base="")}
<div><span class="h">the honest summary</span>
<p>As of today, no authority anywhere can stop a frontier training run before it happens, require permission to start one, or compel anyone to hand over a model's weights. Everything else is paperwork after the fact.</p></div>
</div>

<h2>The mismatch</h2>
<p>One independent estimate puts the number of people working full time on AI safety worldwide at about <strong>1,100</strong>, roughly 600 technical and 500 not, across 115 organisations. The author says it undercounts work happening inside the labs. In the same year, four companies are spending on the order of 600 billion dollars building the systems.</p>
{bslot("worry-about-future","Belle looking worried about the future", "One of these numbers is people. The other is dollars.", base="")}
<p class="meta">That ratio is not an argument by itself. Plenty of important fields are small. It is offered as a fact about proportion, and what you make of it is yours.</p>

<h2>Sources</h2>
<p>Everything above is dated. The fast moving items are flagged in the notes so you can tell what will be stale first.</p>
{srcs([
("https://epoch.ai/data-insights/models-over-1e25-flop","Epoch AI, Models trained above 10^25 FLOP","The count of twelve developers, as of June 2025. Estimated, and the oldest figure on this page."),
("https://epoch.ai/data-insights/hyperscalers-control-most-compute","Epoch AI, Hyperscalers control most compute","Five companies at 71 percent of world AI compute, Q4 2025 data, measured in H100 equivalents. Estimated."),
("https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm","Nvidia annual report, fiscal year ended 25 January 2026","Nvidia's own statement that it uses outside foundries including TSMC and Samsung, and TSMC's CoWoS packaging. The company with most of the world's AI compute owns no factories."),
("https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2027","Nvidia Q1 FY2027 results, 20 May 2026","75.2 billion dollars of data centre revenue in one quarter, up 92 percent. Disclosed. Superseded at the next results date."),
("https://pr.tsmc.com/english/news/3326","TSMC second quarter 2026 results, 16 July 2026","77 percent of wafer revenue from 7nm and below. Disclosed."),
("https://www.asml.com/en/news/press-releases/2026/q2-2026-financial-results","ASML second quarter 2026 results, 15 July 2026","The company financials. ASML's position as sole maker of EUV lithography is structural rather than a figure that moves."),
("https://www.dutchnews.nl/2026/06/asml-denies-us-accusation-an-advanced-machine-reached-china/","ASML statement on EUV shipments, 19 June 2026","The company's own words on never having shipped an EUV machine or specially designed EUV component to China, and the physical scale of the machines."),
("https://epoch.ai/data-insights/grok-4-training-resources","Epoch AI, Grok 4 training resources, 12 September 2025","246 million H100 hours, 310 gigawatt hours, roughly 490 million dollars median estimate. Epoch flags significant uncertainty."),
("https://epoch.ai/trends","Epoch AI Trends dashboard","Compute growing about five times a year, cost about three and a half times a year. Carries its own last updated stamp, currently February 2026."),
("https://epoch.ai/data-insights/hyperscaler-capex-vs-cash-flow","Epoch AI, Hyperscaler capex versus cash flow, 16 June 2026","The projection that capital spending overtakes operating cash flow around Q3 2026. Estimated."),
("https://www.oecd.org/en/about/news/announcements/2026/02/ai-firms-capture-61-percent-of-global-venture-capital-in-2025.html","OECD, AI firms capture 61 percent of global venture capital, February 2026","258.7 billion dollars of a 427.1 billion global total, against thirty percent in 2022."),
("https://epoch.ai/data-insights/ai-datacenter-power","Epoch AI, AI data centre power, 16 January 2026","About 30 gigawatts at the end of 2025, against New York State's roughly 31 gigawatt peak. Rated capacity, not metered consumption, so treat as an upper bound."),
("https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2026-releases/20260714-pjm-capacity-auction-procures-138318-mw-of-generation-resources.pdf","PJM 2028/2029 capacity auction results, 14 July 2026","Cleared at the price cap for a third year, 16.4 billion dollars, 6,831 megawatts short of the reliability requirement, with PJM naming data centre load growth."),
("https://www.utilitydive.com/news/pjm-data-centers-capacity-auction-imm-bowring/825626/","Monitoring Analytics via Utility Dive, July 2026","PJM's independent market monitor attributing 29.4 billion of 63.6 billion in capacity charges across four auctions to data centres."),
("https://epoch.ai/publications/openai-stargate-where-the-us-sites-stand","Epoch AI, Where the Stargate sites stand, 17 April 2026","Satellite and permit analysis. One site partly operational, six at zero."),
("https://artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/","EU AI Act, enforcement of Chapter V","Commission enforcement powers over general purpose AI providers commencing 2 August 2026, and the three percent of worldwide turnover ceiling."),
("https://artificialintelligenceact.eu/article/51/","EU AI Act Article 51","The ten to the twenty five FLOP presumption of systemic risk."),
("https://www.whitecase.com/insight-alert/california-enacts-landmark-ai-transparency-law-transparency-frontier-artificial","California SB 53, Transparency in Frontier Artificial Intelligence Act","In force 1 January 2026. The ten to the twenty six threshold, the fifteen day and twenty four hour incident reporting duties, and the one million dollar per violation penalty."),
("https://www.nist.gov/caisi","NIST Center for AI Standards and Innovation","Works through voluntary agreements with developers. No enforcement authority."),
("https://www.aisi.gov.uk/","UK AI Security Institute","Technical evaluation body with model access granted voluntarily by developers. No statutory power."),
("https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/","Microsoft on the OpenAI partnership, 28 October 2025","The disclosed 27 percent as converted stake, valued around 135 billion dollars."),
("https://www.anthropic.com/news/anthropic-amazon-compute","Anthropic and Amazon compute announcement, 20 April 2026","The additional investment and the up to 5 gigawatts of capacity. Note that no percentage stake is stated here or anywhere else."),
("https://forum.effectivealtruism.org/posts/7YDyziQxkWxbGmF3u/ai-safety-field-growth-analysis-2025","AI safety field growth analysis, 2025","The roughly 1,100 full time figure across 115 organisations. An independent estimate whose author states it undercounts safety work inside frontier labs and universities."),
])}

{xlinks([("risk/pipeline.html","next","How one of these is actually made"),
         ("risk/index.html","then","What people mean when they argue about the risk"),
         ("risk/words.html","reference","The vocabulary, defined plainly")])}
</div>
<script>window.STACK={stack_js};</script>
"""

# ================================================================= ROOT / HOME

home_body = f"""
<div class="wrap hero">
<div class="herogrid">
<div>
<span class="kicker">belleofthebot &middot; explainers</span>
<h1>I take complicated things apart and draw them.</h1>
<p class="lede">Interactive walkthroughs of subjects that are hard to see clearly, in plain language, with the uncertainty left visible instead of smoothed out. Built by hand, sourced throughout, and free to read.</p>
<div class="tags">
<span class="tag rose">no predictions</span>
<span class="tag">sources on every claim</span>
<span class="tag mint"><span class="dot">&#9679;</span> more coming</span>
</div>
</div>
<div class="stage">{bslot("hands-out-cheeky","Belle with her hands out, mid explanation", base="")}</div>
</div>
</div>

<div class="wrap">
<div class="note">
<span class="h">who is doing this</span>
<p>I am Elizabeth Beier, a designer who learned to build. I make things with these systems every day, and when a subject is too tangled to hold in my head I do the same thing I have always done with a hard brief: take it apart, draw it, and check my work against the sources. These are those, in public.</p>
</div>

<div class="bsay">
{bslot("warm-neutral","Belle, warm and neutral", base="")}
<div><span class="h">a note on the drawings</span>
<p>Belle turns up throughout these pages. She is here to mark tone, not to soften the material: when something is uncomfortable she looks uncomfortable, and when a claim is thin she looks unconvinced.</p></div>
</div>

<h2>The explainers</h2>
<a class="card" href="risk/index.html">
<h3>What people mean when they argue about AI risk</h3>
<p>Four connected walkthroughs. How a language model actually gets made, why severity and cause are separate questions, why two people can both say ten percent and mean incompatible things, and the fourteen words the argument cannot proceed without. Every claim is marked as measured, estimated or argued, so you can tell which is which.</p>
<span class="foot">4 walkthroughs &middot; interactive &middot; sourced</span></a>

{xlinks([("risk/pipeline.html","jump in","How a language model gets made"),
         ("risk/taxonomy.html","jump in","The two axes"),
         ("risk/words.html","jump in","The words, with a quiz")], "two")}

<h2>How these are made</h2>
<p>Research first, from primary sources, with a written list of things not to draw as settled fact. Then the structure, which is usually where the real work is: a grid rather than a ladder if two things are independent, a builder rather than a paragraph if the point is that a term is slippery. Then the drawing.</p>
<p>Every substantive claim carries one of three marks, and keeping them apart is the whole discipline of the thing.</p>
<div class="tags">
<span class="flag emp">measured</span>
<span class="flag op">someone's estimate</span>
<span class="flag phil">argument</span>
</div>
<p class="meta">Measured means a study, survey or evaluation actually counted something. An estimate means a named person said it, which makes the saying a fact and the belief still a belief. An argument is philosophical and cannot be settled by data.</p>

<div class="note" style="margin-top:var(--s5)">
<span class="h">elsewhere</span>
<p>My design and development portfolio, with case studies of the systems behind this one, is at <a href="https://elizabethbportfolio.com">elizabethbportfolio.com</a>. The code for everything here is at <a href="https://github.com/belleofthebot">github.com/belleofthebot</a>.</p>
</div>
</div>
"""

rootpage("frontier.html","Who controls the frontier","How few organisations can actually build a frontier AI model, counted, with sources.", frontier_body, ROOTNAV,
         "who can actually build one of these, counted")

page("index.html","The map","A plain language map of what people mean when they talk about AI risk.", index_body)
page("pipeline.html","How a language model gets made","Five stages from raw text to a deployed assistant, and where the safety work attaches.", pipeline_body)
page("taxonomy.html","The two axes","Severity and cause are separate questions. An interactive grid of AI risk categories.", taxonomy_body)
page("words.html","The words","A quiz and glossary for the vocabulary of AI risk.", words_body)
print("done")
