# -*- coding: utf-8 -*-
"""Generates belleofthebot.com.

Built from the SAME specs as the Instagram carousels, so the feed and the site
can never drift apart. Edit social/carousels.py and rebuild.

  index.html     Belle's introduction, filter pills, the card grid, the modal
  quizzes.html   one quiz per subject, three levels, pass at 80 percent
  more.html      the long form pieces
  sources.html   every source on the site, in one place
  about.html     about Belle, about Elizabeth, how to share

Quiz levels are derived, not hand written, so they deepen on their own as terms
are added:

  level 1  the first four terms of a subject, definition questions. A gentle start.
  level 2  every definition question in the subject.
  level 3  classify each claim: measurement, theory, definition, or someone's
           position. This is the skill the whole site is actually teaching.
"""
import os, io, json, sys, re

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "social"))
import carousels as C

# subject order, and the colour each one wears
SUBJECTS = ["components", "concepts", "behavior", "actors", "risk"]
SUBNAME  = {"components": "components", "concepts": "concepts", "behavior": "behaviors",
            "actors": "actors", "risk": "risks"}
SUBBLURB = {
 "components": "The parts these systems are made of, and how they are built and tested.",
 "concepts":   "The abstract ideas everyone argues about before anybody defines them.",
 "behavior":   "What these systems actually do, including the alarming bits, with the setup attached.",
 "actors":     "Who builds this, who owns it, who can stop it, and what they actually said.",
 "risk":       "What could go wrong, how bad it could get, and how much of it is measured.",
}

# How the cards look in the grid. "belle" gives every tile the carousel cover,
# character and all. "diagram" swaps the character for the icon language. "plain"
# is the text-only tile. Set TILES in the environment to switch.
TILES = os.environ.get("TILES", "mix")

# In mix, Belle takes the biggest and most abstract ideas, where a face does
# more work than a diagram, and the diagrams carry everything concrete.
BELLE_TERMS = {
    # Belle takes roughly half the grid: the abstract ideas, the people, and the
    # cards where a face carries the tone better than a drawing. Chosen for range
    # as well as fit, so the grid is not a wall of alarm.
    "alphago", "consciousness", "bengio", "hassabis", "red-teaming",
    "taboo-your-words", "amodei", "p-doom", "agi", "superintelligence",
    "exponential-growth", "existential-risk", "s-risk",
    "recursive-self-improvement", "misuse-misalignment", "intelligence",
    "altman", "hinton", "scheming", "ai-psychosis", "data-center",
    "gender-shades", "fei-fei-li", "gebru", "toner", "murati",
    "daniela-amodei", "crawford", "koller", "lucy-guo",
    "shoggoth", "off-switch", "alignment-faking", "mechahitler",
    "permanent-disempowerment", "optimization", "drones", "grown-not-built",
    "yang", "miri", "hendrycks", "openai", "anthropic", "google-deepmind",
    "deepseek", "xai", "rogue-ai", "enslaved-god", "race-to-agi", "automation",
    "apollo", "bio-threshold", "neural-network", "ai-2027",
    "power-concentration", "sydney", "environment", "persuasion",
    "ubi", "abundance", "bitter-lesson", "moravec", "goodharts-law",
    "interpretability", "differential-development", "grokking",
    "sycophancy", "emergent-abilities", "moravec", "jailbreak",
}

# The second expression, shown on hover. Idle face, then the reaction: the point
# is that the grid rewards looking at it. Falls back to a scale if the art is
# missing.
HOVER = {
 # idle face, then the reaction. The grid should reward looking at it.
 "who-makes-the-chips": "close-up-goading", "who-owns-it": "deadpan-annoyed-1",
 "who-gives-a-number": "hands-out-cheeky",  "bengio": "saying-unpleasant-truth-1",
 "lecun": "unimpressed",                    "bender-hanna": "smirking",
 "hallucination": "startled",               "specification-gaming": "sly-one",
 "blackmail": "yikes",                      "evaluation-awareness": "secret-close-smile",
 "context-window": "surprised-worried",     "rlhf": "dead-pan-1",
 "open-weights": "yikes",                   "compute": "bright-neutral",
 "red-teaming": "smirking",                 "agi": "unimpressed",
 "misuse-misalignment": "saying-unpleasant-truth-1",
 "recursive-self-improvement": "worry-about-future",
 "intelligence": "grumpy-eyes-closed",      "p-doom": "hands-out-cheeky",
 "s-risk": "shock-worry",                   "job-loss": "glum",
 "existential-risk": "yikes",               "consciousness": "noticed-something",
 "superintelligence": "shock-worry",        "exponential-growth": "shocked",
 "alphago": "happy-proud",                  "hinton": "glum",
 "altman": "deadpan-annoyed-1",             "amodei": "hands-hips-pedantic",
 "hassabis": "secret-close-smile",          "scheming": "sly-one",
 "ai-psychosis": "saying-unpleasant-truth-1",
 "data-center": "surprised-worried",        "taboo-your-words": "hands-hips-pedantic",
 "gender-shades": "noticed-something",       "fei-fei-li": "happy-proud",
 "gebru": "hands-hips-pedantic",           "toner": "annoyed-skeptical",
 "murati": "shock-worry",                  "daniela-amodei": "warm-curious",
 "crawford": "saying-unpleasant-truth-1",  "koller": "delighted",
 "lucy-guo": "smirking",                    "shoggoth": "shocked",
 "off-switch": "shock-worry",               "alignment-faking": "secret-close-smile",
 "mechahitler": "yikes",                    "permanent-disempowerment": "worry-about-future",
 "optimization": "unimpressed",             "drones": "shock-worry",
 "grown-not-built": "noticed-something",    "yang": "hands-hips-pedantic",
 "miri": "glum",                            "hendrycks": "hands-hips-pedantic",
 "openai": "deadpan-annoyed-1",             "anthropic": "innocent-curious",
 "google-deepmind": "warm-neutral",         "deepseek": "shocked",
 "xai": "yikes",                            "rogue-ai": "sly-one",
 "enslaved-god": "shock-worry",             "race-to-agi": "deadpan-annoyed-1",
 "automation": "glum",                      "apollo": "smirking",                     "bio-threshold": "shock-worry",
 "neural-network": "unimpressed",           "ai-2027": "shock-worry",
 "power-concentration": "yikes",            "sydney": "shocked",
 "environment": "glum",                     "persuasion": "sly-one",
 "ubi": "hands-out-cheeky",                 "abundance": "delighted",
 "bitter-lesson": "grumpy-eyes-closed",     "moravec": "smirking",
 "goodharts-law": "unimpressed",            "interpretability": "innocent-curious",
 "differential-development": "warm-neutral","grokking": "happy-proud",
 "sycophancy": "secret-close-smile",        "emergent-abilities": "startled",
 "jailbreak": "sly-one",                    "learning": "glum",
 "companions": "surprised-worried",         "value-lock-in": "shock-worry",
}

# the four kinds of claim
TYPES = [("emp", "measurement"), ("arg", "theory"),
         ("def", "definition"), ("op", "someone&rsquo;s position")]
TYPENAME = dict(TYPES)
TYPEDESC = {
 "emp": "A study, survey or evaluation actually counted something.",
 "arg": "Reasoned rather than counted. It cannot be settled by data alone.",
 "def": "What a word means in this literature. Not a finding, not a forecast.",
 "op":  "A named person said it. That makes the saying a fact and the belief still a belief.",
}

MORE = [
 ("frontier.html", "Who controls the frontier", "actors",
  "The whole stack counted, from thousands of companies down to the single firm that makes the machine that makes the chips."),
 ("risk/pipeline.html", "How a language model gets made", "components",
  "Five stages from raw text to a deployed assistant, and which safety work attaches to which stage."),
 ("risk/taxonomy.html", "Where the worry comes in", "risk",
  "How bad and how it happens are separate questions. A grid you can click through, plus the number people quote at you."),
 ("risk/words.html", "The full glossary", "concepts",
  "Thirty five terms defined plainly, with a quiz that covers every subject at once."),
]

def strip(t):
    t = t.replace("<br>", " ")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)) \
        .replace("&rsquo;", "’").replace("&ldquo;", "“").replace("&rdquo;", "”") \
        .replace("&middot;", "·").replace("&amp;", "&").strip()

NAV = [("index.html", "explore"), ("quizzes.html", "quizzes"),
       ("more.html", "more"), ("about.html", "about")]

def head(title, desc, current):
    links = "".join(
        '<a class="link" href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else '', t)
        for h, t in NAV)
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;700&display=swap">
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
<span>every claim marked &middot; every source named</span>
<span>built by elizabeth beier &middot; <a href="https://instagram.com/belleofthebot">@belleofthebot</a></span>
</div></footer>
"""

def page(name, title, desc, body, scripts=()):
    js = "".join(f'<script src="{s}"></script>' for s in scripts)
    html = head(title, desc, name) + body + FOOT + js + "</body></html>"
    io.open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
    print(name, len(html))

def belle_img(slug, cls="bfig"):
    p = os.path.join(OUT, "assets", "belle", slug + ".webp")
    if os.path.exists(p):
        return f'<figure class="{cls}"><img src="assets/belle/{slug}.webp" alt="" loading="lazy"></figure>'
    return f'<figure class="{cls}"><div class="bph"><span class="n">{slug}</span></div></figure>'

def terms_in(cat):
    return [(k, v) for k, v in C.SPECS.items() if v["cat"] == cat]

def has_belle(slug):
    return bool(slug) and os.path.exists(
        os.path.join(OUT, "assets", "belle", slug + ".webp"))

def photo_for(key):
    """A cut out portrait for the people cards, if one has been added.

    Drop a background-free png or webp at assets/people/<key>.webp and the tile
    and the card both switch to it. Until then the card wears Belle, so nothing
    breaks while the art is being gathered. Each one needs a credit line in the
    spec's photosrc field, because these are other people's photographs."""
    for ext in (".webp", ".png"):
        if os.path.exists(os.path.join(OUT, "assets", "people", key + ext)):
            return "assets/people/" + key + ext
    return ""

def grounds():
    """Lift the category grounds straight out of the carousel stylesheet, so the
    site and the feed cannot end up different colours. Renamed tg- for the web."""
    out = []
    for m in re.finditer(r"^\.g-(\w+)\{([^}]+)\}", C.HEAD, re.M):
        out.append(".tg-%s{%s}" % (m.group(1), " ".join(m.group(2).split())))
    return "<style>\n" + "\n".join(out) + "\n</style>"

def hook_size(hook):
    """No ellipsis. The hook is short by design, so when one runs long the type
    steps down rather than the sentence being cut off mid thought."""
    n = len(strip(hook))
    for limit, cls in ((40, "h-xl"), (58, "h-l"), (84, "h-m")):
        if n <= limit:
            return cls
    return "h-s"

def anchor_for(key):
    """Belle should not sit in the same corner on every tile."""
    return ["b-left", "b-mid", "b-right"][sum(ord(c) for c in key) % 3]

def tile(k, sp, cat):
    """One card in the grid. Three looks, same data."""
    common = (f'tabindex="0" role="button" data-key="{k}" data-cat="{cat}" '
              f'data-flag="{sp["flag"]}" aria-label="Open {strip(sp["term"])}"')
    flag = f'<span class="flag f-{sp["flag"]}">{TYPENAME[sp["flag"]]}</span>'

    wants_belle = TILES == "belle" or (TILES == "mix" and k in BELLE_TERMS)
    if TILES == "plain" or (wants_belle and not has_belle(sp.get("belle_hook"))):
        return f'''<article class="etile c-{cat}" {common}>
  <span class="et-sub">AI {SUBNAME[cat]}</span>
  <h3 class="et-term">{strip(sp["term"])}</h3>
  <p class="et-hook">{sp["hook"]}</p>
  {flag}
</article>'''

    photo = photo_for(k)
    if photo:
        art = (f'<figure class="et-photo"><img src="{photo}" alt="{strip(sp["term"])}"'
               f' loading="lazy"></figure>')
        anchor = anchor_for(k)
    elif not wants_belle:
        art = f'''<svg class="et-icon" viewBox="0 0 64 64" aria-hidden="true"><use href="#{sp["icon"]}"/></svg>'''
        anchor = "b-icon"
    else:
        idle = sp["belle_hook"]
        react = HOVER.get(k)
        second = (f'<img class="et-react" src="assets/belle/{react}.webp" alt="" loading="lazy">'
                  if has_belle(react) else "")
        art = (f'<figure class="et-belle"><img class="et-idle" src="assets/belle/{idle}.webp"'
               f' alt="" loading="lazy">{second}</figure>')
        anchor = anchor_for(k)

    return f'''<article class="etile cover tg-{cat} c-{cat} {anchor}" {common}>
  <div class="et-top"><span class="et-name">{strip(sp["term"])}</span>{flag}</div>
  <h3 class="et-hook {hook_size(sp["hook"])}">{sp["hook"]}</h3>
  {art}
  <span class="et-open">open <span aria-hidden="true">&rarr;</span></span>
</article>'''

# ---------------------------------------------------------------- card data
def card_data():
    d = {}
    for k, sp in C.SPECS.items():
        d[k] = {
            "key": k, "cat": sp["cat"], "catname": "AI " + SUBNAME[sp["cat"]],
            "term": strip(sp["term"]), "kick": strip(sp["kick"]), "hook": sp["hook"],
            "reveal": sp["reveal"], "revsub": strip(sp["revsub"]),
            "threekick": strip(sp["threekick"]),
            "three": [[i, strip(t), strip(b)] for i, t, b in sp["three"]],
            "threefoot": strip(sp["threefoot"]),
            "whykick": strip(sp["whykick"]), "why": sp["why"], "whysub": strip(sp["whysub"]),
            "flag": sp["flag"], "flagname": TYPENAME[sp["flag"]],
            "file": sp["file"], "src": sp["src"],
            "icon": sp["icon"],
            "unknown": sp["unknown"],
            "belle": sp["belle_hook"] if has_belle(sp.get("belle_hook")) else "",
            "photo": photo_for(k), "photosrc": sp.get("photosrc", ""),
            "belle2": HOVER.get(k, "") if has_belle(HOVER.get(k)) else "",
        }
        d[k].update(question(k, sp))
    return d

def question(k, sp):
    """The carousel's own multiple choice, with the answer moved off B."""
    raw = list(sp["opts"]); correct = raw[1]
    target = sum(ord(c) for c in k) % 4
    rest = [o for i, o in enumerate(raw) if i != 1]
    shown = rest[:target] + [correct] + rest[target:]
    return {"q": strip(sp["q"]), "opts": [strip(o) for o in shown],
            "ans": target, "ansy": strip(sp["revsub"])}

# ---------------------------------------------------------------- quizzes
def defn_questions(cat):
    out = []
    for k, sp in terms_in(cat):
        raw = list(sp["opts"]); correct = raw[1]
        target = sum(ord(c) for c in k) % 4
        rest = [o for i, o in enumerate(raw) if i != 1]
        shown = rest[:target] + [correct] + rest[target:]
        out.append({"q": strip(sp["q"]), "a": [strip(o) for o in shown],
                    "correct": target, "why": strip(sp["revsub"])})
    return out

def flag_questions(cat):
    """Level three. Classify the claim, which is the site's actual lesson."""
    labels = [strip(TYPENAME[t]) for t, _ in TYPES]
    out = []
    for k, sp in terms_in(cat):
        right = labels.index(strip(TYPENAME[sp["flag"]]))
        target = (sum(ord(c) for c in k) + 2) % 4
        rest = [l for i, l in enumerate(labels) if i != right]
        shown = rest[:target] + [labels[right]] + rest[target:]
        out.append({
            "q": "How is this filed? “" + strip(sp["reveal"]) + "”",
            "a": shown, "correct": target,
            "why": strip(sp["file"])})
    return out

def who_said_it():
    """A bonus round for the actors page: verified quotations, attributed.

    Every line here was checked against a primary or clearly named source during
    research. If a quotation cannot be verified to a retrievable source it does
    not go in, however famous it is."""
    Q = [
     ("&ldquo;I left so that I could talk about the dangers of AI without considering "
      "how this impacts Google.&rdquo;", "Geoffrey Hinton",
      ["Sam Altman", "Yann LeCun", "Elon Musk"],
      "Posted on X on 1 May 2023, the day his departure was reported. He added that Google had acted very responsibly."),
     ("&ldquo;If this technology goes wrong, it can go quite wrong.&rdquo;", "Sam Altman",
      ["Demis Hassabis", "Dario Amodei", "Geoffrey Hinton"],
      "To a US Senate subcommittee, 16 May 2023, in his first congressional testimony."),
     ("&ldquo;I don&rsquo;t have a p(doom) number because I think it would imply a level of "
      "precision that is not there.&rdquo;", "Demis Hassabis",
      ["Yoshua Bengio", "Dario Amodei", "Timnit Gebru"],
      "On the Lex Fridman podcast, July 2025. He also called the risk definitely non zero."),
     ("&ldquo;Mitigating the risk of extinction from AI should be a global priority alongside "
      "other societal-scale risks such as pandemics and nuclear war.&rdquo;",
      "the Center for AI Safety",
      ["the United Nations", "the European Commission", "the Future of Life Institute"],
      "Twenty two words, published 30 May 2023, signed by Hinton, Bengio, Hassabis, Altman and Amodei among others."),
     ("&ldquo;AI is neither artificial nor intelligent.&rdquo;", "Kate Crawford",
      ["Emily Bender", "Timnit Gebru", "Joy Buolamwini"],
      "The opening argument of Atlas of AI, 2021. Her point is that it is made of minerals, energy and labour."),
     ("&ldquo;Self-governance cannot reliably withstand the pressure of profit incentives.&rdquo;",
      "Helen Toner",
      ["Timnit Gebru", "Max Tegmark", "Stuart Russell"],
      "With Tasha McCauley in The Economist, May 2024, six months after they were removed from OpenAI&rsquo;s board."),
     ("&ldquo;General methods that leverage computation are ultimately the most effective, "
      "and by a large margin.&rdquo;", "Richard Sutton",
      ["Ilya Sutskever", "Geoffrey Hinton", "Andrej Karpathy"],
      "The Bitter Lesson, March 2019. In 2025 he argued that today&rsquo;s language models are not an example of it."),
     ("&ldquo;Generative AI systems are grown more than they are built.&rdquo;", "Dario Amodei",
      ["Demis Hassabis", "Sam Altman", "Fei-Fei Li"],
      "The Urgency of Interpretability, April 2025. He compares it to growing a plant."),
     ("A language model is &ldquo;a stochastic parrot&rdquo;, stitching together forms "
      "without reference to meaning.", "Bender, Gebru, McMillan-Major and Mitchell",
      ["Gary Marcus", "Yann LeCun", "Judea Pearl"],
      "On the Dangers of Stochastic Parrots, 2021. Two of the four authors had left Google by the time it was published."),
     ("A kill switch requirement &ldquo;will devastate the open-source community.&rdquo;",
      "Fei-Fei Li",
      ["Yann LeCun", "Andrew Ng", "Elon Musk"],
      "Opposing California&rsquo;s SB 1047 in August 2024. She also said she is not anti AI governance."),
     ("&ldquo;The substantial disparities in the accuracy of classifying darker females... "
      "require urgent attention.&rdquo;", "Buolamwini and Gebru",
      ["the Federal Trade Commission", "Microsoft Research", "the ACLU"],
      "Gender Shades, 2018. Error rates ran to 34.7 percent for darker skinned women against 0.3 for lighter skinned men."),
     ("&ldquo;We want to help make AI systems safer from day one.&rdquo;", "Daniela Amodei",
      ["Mira Murati", "Lila Ibrahim", "Helen Toner"],
      "In a Stripe interview, July 2023. She is Anthropic&rsquo;s co-founder and president."),
    ]
    out = []
    for i, (quote, right, wrong, why) in enumerate(Q):
        target = (i * 3 + 1) % 4
        shown = wrong[:target] + [right] + wrong[target:]
        out.append({"q": "Who said it? " + quote, "a": shown, "correct": target, "why": why})
    return out

def quiz_data():
    topics = []
    for cat in SUBJECTS:
        d = defn_questions(cat)
        topics.append({
            "key": cat, "name": "AI " + SUBNAME[cat], "short": SUBNAME[cat],
            # Three rounds of 8 to 12, drawn from different terms so the levels
            # are genuinely different rather than the same set twice.
            "levels": {"1": d[:10], "2": d[10:22] or d[:10],
                       "3": flag_questions(cat)[:12]},
        })
    return {"topics": topics, "bonus": {
        "key": "whosaid", "name": "who said it", "short": "who said it",
        "questions": who_said_it()},
     "bands": {
        "perfect": {"belle": "delighted",
                    "line": "Every single one. You must be superintelligent."},
        "pass":    {"belle": "happy-proud",
                    "line": "Comfortably past. That is the {short} vocabulary in hand."},
        "mid":     {"belle": "warm-curious",
                    "line": "Most of the way there. A read of the {short} cards and another go should do it."},
        "low":     {"belle": "aw-shucks",
                    "line": "Do not worry, you will get this. Almost nobody starts here knowing it."},
     },
     "prize": {"belle": "tearfully-proud", "fallback": "delighted",
               "line": "You have passed every level of every subject on this site.",
               "sub": "There is no badge. There is me, extremely pleased, and the fact that you can now "
                      "read almost any article about AI and tell which parts are measured, which are "
                      "argued, and which are somebody&rsquo;s guess wearing a number. That was the "
                      "entire point. Go and be insufferable about it."}}

# ---------------------------------------------------------------- index
def index():
    cards = card_data()
    # round robin across subjects, so the unfiltered grid reads as five colours
    # rather than five blocks. Filtering still hands you one clean subject.
    queues = [[(k, sp, cat) for k, sp in terms_in(cat)] for cat in SUBJECTS]
    tiles = []
    while any(queues):
        for q in queues:
            if q:
                tiles.append(tile(*q.pop(0)))

    subpills = "".join(
        f'<button class="pill p-{c}" data-kind="cat" data-val="{c}" type="button">'
        f'AI {SUBNAME[c]} <span class="pn">{len(terms_in(c))}</span></button>' for c in SUBJECTS)
    typepills = "".join(
        f'<button class="pill t-{t}" data-kind="flag" data-val="{t}" type="button">{n}</button>'
        for t, n in TYPES)

    extra = grounds() + C.ICONS

    body = f"""{extra}
<div class="wrap intro">
<div class="introgrid">
{belle_img("friendly-wave" if os.path.exists(os.path.join(OUT,"assets","belle","friendly-wave.webp")) else "warm-neutral", "bfig plain big")}
<div>
<span class="kicker">hello, I am Belle</span>
<h1>Everyone is arguing about AI. Almost nobody agrees what the words mean.</h1>
<p class="lede">So I took them apart. Every card below is one idea, in plain language, with the source it came from and a mark saying what kind of claim it is. Pick a subject, or pick a kind of claim, and start anywhere.</p>
<p class="lede">Nothing here predicts the future. It just tells you what is actually known, what is somebody&rsquo;s view, and how to tell the difference.</p>
<div class="tags">
<span class="tag rose">{len(C.SPECS)} cards</span>
<span class="tag">every source named</span>
<a class="tag mint" href="quizzes.html"><span class="dot">&#9679;</span> or take a quiz</a>
</div>
</div>
</div>
</div>

<div class="wrap" data-explore>
<div class="filters">
  <div class="frow">
    <span class="flab">subject</span>
    <div class="pills">{subpills}</div>
  </div>
  <div class="frow">
    <span class="flab">kind of claim</span>
    <div class="pills">{typepills}</div>
  </div>
  <div class="frow fbar">
    <span class="meta" data-count></span>
    <button class="btn ghost sm" type="button" data-clear>clear filters</button>
  </div>
</div>

<div class="egrid{"" if TILES == "plain" else " covers"}">{"".join(tiles)}</div>
<p class="eempty meta" hidden>Nothing matches both filters. Try clearing one.</p>
</div>

<div class="modal" data-modal hidden>
  <div class="mscrim"></div>
  <div class="mcard" role="dialog" aria-modal="true" aria-label="card">
    <div class="mhead">
      <span class="mcat"></span>
      <span class="mterm"></span>
      <button class="mclose" type="button" data-close aria-label="close">&times;</button>
    </div>
    <div class="mbody"></div>
    <div class="mfoot">
      <button class="btn ghost sm" type="button" data-prev>back</button>
      <div class="mdots"></div>
      <button class="btn sm" type="button" data-next>next</button>
    </div>
  </div>
</div>

<script>window.CARDS={json.dumps(cards)};</script>
"""
    page("index.html", "AI, explained plainly",
         "Every AI term that matters, in plain language, marked by what kind of claim it is and sourced.",
         body, ("explore.js",))

# ---------------------------------------------------------------- quizzes
def quizzes():
    qd = quiz_data()
    rows = ""
    for cat in SUBJECTS:
        lv = ""
        for n in (1, 2, 3):
            cls = "btn sm" if n == 1 else "btn ghost sm"
            lv += (f'<button class="{cls}" type="button" data-start="{cat}" data-level="{n}">'
                   f'level {n}<span class="tick" hidden>&#10003;</span></button>')
        rows += f'''<div class="qrow c-{cat}">
<div class="qr-name"><span class="qr-sub">AI {SUBNAME[cat]}</span>
<span class="meta">{len(terms_in(cat))} terms</span></div>
<div class="qr-lvls">{lv}</div></div>'''

    body = f"""
<div class="wrap hero narrow">
<span class="kicker">quizzes</span>
<h1>Find out what you actually know.</h1>
<p class="lede">Five subjects, three levels each, between eight and twelve questions a round. Level one is a gentle start, level two covers the rest of the subject, and level three asks you to classify the claims yourself, which is the real skill.</p>
<p class="lede">Score eighty percent and the next level unlocks. Score less and you can go straight round again. Every wrong answer tells you which one was right, and why.</p>
</div>

<div class="wrap" data-quizgame>
  <div class="qpick">{rows}
    <div class="qbonus">
      <div class="qr-name"><span class="qr-sub">who said it</span>
      <span class="meta">bonus round &middot; always open</span></div>
      <div class="qr-lvls"><button class="btn sm" type="button" data-bonus>start</button></div>
    </div>
    <p class="meta" style="margin-top:var(--s4)">Progress is kept in this browser and nowhere else. <button class="linkbtn" type="button" data-reset>clear my progress</button></p>
    <p class="meta prizehint" data-allnote hidden>Every level is passed. Finish any round to claim what Belle owes you.</p>
  </div>

  <div class="qplay" hidden>
    <div class="qtop"><span class="qtopic"></span><span class="qlevel meta"></span></div>
    <div class="qprog"><span class="qfill"></span></div>
    <h2 class="qq"></h2>
    <div class="qopts"></div>
    <p class="qfb" hidden></p>
    <div class="qbar">
      <span data-count class="meta"></span>
      <span data-score class="meta"></span>
      <button class="btn" type="button" data-next>next</button>
    </div>
  </div>

  <div class="qdone" hidden>
    <div class="rgrid">
      <div class="rbelle"><img src="assets/belle/happy-proud.webp" alt=""></div>
      <div>
        <span class="rscore"></span>
        <h2 class="rline"></h2>
        <p class="rwhat"></p>
        <div class="ractions">
          <button class="btn" type="button" data-onward></button>
          <button class="btn ghost" type="button" data-restart>take it again</button>
          <button class="btn ghost" type="button" data-share>share result</button>
          <button class="btn ghost" type="button" data-pickagain>all quizzes</button>
        </div>
      </div>
    </div>
  </div>

  <div class="qprize" hidden>
    <div class="rgrid">
      <div class="rbelle big"><img src="assets/belle/delighted.webp" alt=""></div>
      <div>
        <span class="rscore">the whole thing</span>
        <h2 class="pline"></h2>
        <p class="psub"></p>
        <div class="ractions">
          <button class="btn ghost" type="button" data-pickagain>back to the quizzes</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>window.QUIZDATA={json.dumps(qd)};</script>
"""
    page("quizzes.html", "Quizzes",
         "Five subjects, three levels each. Pass at eighty percent and the next level unlocks.",
         body, ("quiz.js",))

# ---------------------------------------------------------------- more
def more():
    rows = "".join(
        f'<a class="xl c-{c}" href="{h}"><span class="k">AI {SUBNAME[c]}</span>'
        f'<span class="t">{t} &rarr;</span><span class="d">{d}</span></a>'
        for h, t, c, d in MORE)
    body = f"""
<div class="wrap hero narrow">
<span class="kicker">more</span>
<h1>The longer versions.</h1>
<p class="lede">The cards are deliberately short. When a subject needs more room than that, it gets its own piece. Each one is built the same way: plain language, every claim marked, every source named.</p>
</div>
<div class="wrap">
<div class="xlinks">{rows}</div>

<h2>Where the sources live</h2>
<p>Every claim on this site is traceable. The cards name their source, the long pieces carry full linked bibliographies, and everything is gathered in one place.</p>
<div class="xlinks">
<a class="xl" href="sources.html"><span class="k">reference</span><span class="t">All sources &rarr;</span>
<span class="d">Every source behind every card, grouped by subject, plus the bibliographies from the long pieces.</span></a>
</div>
</div>
"""
    page("more.html", "More", "Longer pieces, and where every source lives.", body)

# ---------------------------------------------------------------- sources
def sources():
    blocks = ""
    for cat in SUBJECTS:
        items = "".join(
            f'<div class="src-item"><div class="t"><strong>{strip(sp["term"])}</strong> '
            f'<span class="flag f-{sp["flag"]}">{TYPENAME[sp["flag"]]}</span></div>'
            f'<div class="n">{sp["src"]}</div></div>' for k, sp in terms_in(cat))
        blocks += f'<h2 class="c-{cat}"><span class="subdot"></span>AI {SUBNAME[cat]}</h2><div class="srcs">{items}</div>'
    longs = "".join(f'<a class="xl" href="{h}"><span class="k">full bibliography</span>'
                    f'<span class="t">{t} &rarr;</span></a>' for h, t, c, d in MORE)
    body = f"""
<div class="wrap hero narrow">
<span class="kicker">sources</span>
<h1>Everything here is checkable.</h1>
<p class="lede">That is the whole point of the site, so here is the list. Where a claim is contested, the sources that disagree are both named rather than one being quietly dropped.</p>
</div>
<div class="wrap">
{blocks}
<h2>Full bibliographies</h2>
<p>The long pieces carry their sources as linked lists, with a note on what each one is good for and which figures go stale fastest.</p>
<div class="xlinks">{longs}</div>
</div>
"""
    page("sources.html", "Sources", "Every source behind every card on the site.", body)

# ---------------------------------------------------------------- about
def about():
    body = f"""
<div class="wrap hero">
<div class="herogrid">
<div>
<span class="kicker">about</span>
<h1>Who is doing this, and why.</h1>
<p class="lede">A short answer to both, and a request: if any of it is wrong, tell me, and I will fix it and say that I did.</p>
</div>
<div class="stage">{belle_img("warm-curious", "bfig plain")}</div>
</div>
</div>

<div class="wrap">
<h2>About Belle</h2>
<p>Belle is the robot who does the explaining. She is drawn, not generated, and she is here to carry tone rather than decorate: when something is uncomfortable she looks uncomfortable, and when a claim is thin she looks unconvinced.</p>
<p>She is a robot explaining artificial intelligence, which is a joke, but a useful one. She is also not pretending to be neutral, and neither am I.</p>

<h2>About me</h2>
<p>I am Elizabeth Beier, a designer who learned to build. I make things with these systems every day, and when a subject is too tangled to hold in my head I do what I have always done with a hard brief: take it apart, draw it, and check my work against the sources.</p>
<p>I am not a researcher. I have not trained a model. What I can do is read the primary sources carefully, notice when a number has travelled a long way from what the paper actually said, and draw the difference clearly.</p>

<div class="well">
<h2 style="margin-top:0">Where I stand</h2>
<p>I am not neutral about this, and I would rather say so than pretend.</p>
<p>I think these systems are already here and worth understanding properly, by ordinary people, not only by the people building them. I also think the risks are real and worth acting on. Not because catastrophe is certain, but because some of the possible outcomes cannot be undone, and the time to think about those is before rather than after.</p>
<p>That position does not change how I handle evidence, and it is exactly why the marks exist. <strong>A stated view and honest sourcing are not in tension.</strong> If anything the opposite: when you can see where I stand, you can also see every place I decline to overclaim in my own favour. So when something here is only a theory, I say so, including when it is a theory I find persuasive.</p>
<p class="meta">Where researchers genuinely disagree, I quote both sides in their own words rather than characterising the one I like less.</p>
</div>

<h2>How the marks work</h2>
<p>Every card carries one of four. Letting these blur together is the usual failure of writing about AI, and keeping them apart is most of what this site is for.</p>
<div class="flagkey">
{"".join(f'<div class="fk"><span class="flag f-{t}">{n}</span><span>{TYPEDESC[t]}</span></div>' for t, n in TYPES)}
</div>

<h2>How much of this is settled</h2>
<p>Not much of it. That is not modesty, it is the actual state of the subject, and it is why every card here carries a panel headed <strong>what we do not know</strong> one step before the end.</p>
<p>An analogy I was given by a reader who works in the field, and have not been able to improve on: physics has a cutting edge of unresolved questions wrapped around a very large body of settled understanding. This does not. It has a small area of understanding surrounded by questions we do not yet have the language to formulate. If scholars in the sixteen hundreds had set out to build a card deck explaining physics, that is roughly where this is &mdash; and saying sixteen hundreds physics may be generous.</p>
<p>So the cards are not a summary of what is known. They are a vocabulary for a conversation that is going to happen whether or not the vocabulary is ready, assembled so that you can at least tell which parts are measured, which are argued, and which are nobody&rsquo;s to claim yet.</p>
<p class="meta">If a card&rsquo;s unknowns panel understates the confusion, that is a bug, and I would like to hear about it.</p>

<h2>How to share this</h2>
<p>Please do, and no permission needed. The most useful thing you can do is send one card to somebody who is arguing about a word they have not defined.</p>
<div class="xlinks">
<a class="xl" href="index.html"><span class="k">send a card</span><span class="t">Explore the cards &rarr;</span>
<span class="d">Open any card, then share the link. It opens on the same card.</span></a>
<a class="xl" href="quizzes.html"><span class="k">or a challenge</span><span class="t">Send someone a quiz &rarr;</span>
<span class="d">Results are shareable. Level three is harder than it looks.</span></a>
<a class="xl" href="https://instagram.com/belleofthebot"><span class="k">or follow along</span>
<span class="t">@belleofthebot &rarr;</span><span class="d">The same material, one term at a time.</span></a>
</div>

<h2>Corrections</h2>
<p>If something here is wrong, out of date, or quotes a figure further than its source supports, I want to know. Several numbers on this site were corrected before publication for exactly that reason, and the fastest way to lose the point of the whole thing would be to get precious about it.</p>
<p>Sources for everything are on the <a href="sources.html">sources page</a>.</p>
</div>
"""
    page("about.html", "About", "About Belle, about Elizabeth Beier, and how the marks work.", body)

if __name__ == "__main__":
    index(); quizzes(); more(); sources(); about()
    print(f"{len(C.SPECS)} cards across {len(SUBJECTS)} subjects")
