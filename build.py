# -*- coding: utf-8 -*-
"""Generates the riskmap site. Shared chrome in one place so every page matches."""
import os, io

OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [("index.html","the map"),("pipeline.html","how it is made"),
       ("taxonomy.html","the two axes"),("pdoom.html","the number"),
       ("words.html","the words")]

def head(title, desc, current):
    links = "".join(
        '<a class="link" href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h==current else '', t)
        for h,t in NAV)
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
<link rel="stylesheet" href="belle.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="nav-in">
<a class="mark" href="index.html">belleof<span class="sg">thebot</span><span class="cur">_</span></a>
<span class="nav-sp"></span>
{links}
</div></header>
<main id="main">
"""

FOOT = """</main>
<footer><div class="wrap">
<span>a plain language map of what people mean when they talk about AI risk</span>
<span>built by elizabeth beier &middot; sources on every claim</span>
</div></footer>
<script src="belle.js"></script>
</body></html>
"""

# ---------------------------------------------------------------- Belle stand-in
BELLE = """<svg viewBox="0 0 320 300" role="img" aria-label="Placeholder illustration of Belle, a robot character, standing beside a terminal screen">
<rect x="150" y="70" width="160" height="150" rx="8" fill="#141019" stroke="#423748"/>
<text x="164" y="100" font-family="IBM Plex Mono,monospace" font-size="11" fill="#DFA192">&gt; define risk</text>
<text x="164" y="122" font-family="IBM Plex Mono,monospace" font-size="11" fill="#B3A6BC">which kind</text>
<text x="164" y="140" font-family="IBM Plex Mono,monospace" font-size="11" fill="#B3A6BC">do you mean</text>
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

def page(name, title, desc, body):
    html = head(title, desc, name) + body + FOOT
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print(name, len(html))

def xlinks(items):
    out = ['<div class="xlinks">']
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
<div class="stage">{BELLE}<div class="ph">hero illustration placeholder &middot; replace with your Belle render</div></div>
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
<h3>The two axes</h3>
<p>How bad, and how it happens, are separate questions. Almost every confused argument is two people each holding one axis. This one is a grid you can click through.</p>
<span class="foot">interactive grid</span></a>

<a class="card" href="pdoom.html">
<h3>The number, and why it is a weak instrument</h3>
<p>Two people can both say ten percent and mean incompatible things. Build the sentence yourself and watch the number change meaning.</p>
<span class="foot">interactive &middot; definition builder</span></a>

<a class="card" href="words.html">
<h3>The words</h3>
<p>Fourteen terms the argument cannot proceed without, defined plainly. Test yourself first if you like.</p>
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

{xlinks([("taxonomy.html","next","How bad, and how it happens, are separate questions"),
         ("pdoom.html","related","Why a single probability hides the argument"),
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

{xlinks([("pdoom.html","next","Why one number cannot hold all of this"),
         ("pipeline.html","back","How the systems being argued about are built"),
         ("words.html","reference","Every term here, defined plainly")])}
</div>
"""

# ================================================================= P(DOOM)
pdoom_body = f"""
<div class="wrap hero narrow">
<span class="kicker">walkthrough &middot; 03</span>
<h1>Two people say ten percent and mean incompatible things</h1>
<p class="lede">"p(doom)" is informal shorthand for the probability of a catastrophic outcome from AI. It has no agreed definition, no resolution date, and no way for anyone to be calibrated on it. That does not make it meaningless. It does make it a weak instrument.</p>
</div>

<div class="wrap">

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

{xlinks([("taxonomy.html","back","What the number is trying to compress"),
         ("words.html","next","The vocabulary, defined plainly"),
         ("pipeline.html","related","How the systems in question are built")])}
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
]
glosshtml = "".join(
  f'<div class="src-item"><div class="t"><strong>{t}</strong> &nbsp; {d}</div></div>' for t,d in GLOSS)

words_body = f"""
<div class="wrap hero narrow">
<span class="kicker">reference &middot; 04</span>
<h1>The words</h1>
<p class="lede">Fourteen terms the argument cannot proceed without. Test yourself first if you like, then keep the glossary open while you read the other pieces.</p>
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

{xlinks([("pipeline.html","start here","How a language model gets made"),
         ("taxonomy.html","then","How bad, and how it happens"),
         ("pdoom.html","then","The number, and its limits")])}
</div>
<script>{qjs}</script>
"""

page("index.html","The map","A plain language map of what people mean when they talk about AI risk.", index_body)
page("pipeline.html","How a language model gets made","Five stages from raw text to a deployed assistant, and where the safety work attaches.", pipeline_body)
page("taxonomy.html","The two axes","Severity and cause are separate questions. An interactive grid of AI risk categories.", taxonomy_body)
page("pdoom.html","The number","Why two people can say ten percent and mean incompatible things.", pdoom_body)
page("words.html","The words","A quiz and glossary for the vocabulary of AI risk.", words_body)
print("done")
