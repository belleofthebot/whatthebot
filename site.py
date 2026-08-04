# -*- coding: utf-8 -*-
"""Generates belleofthebot.com.

Four paths, matching the Instagram categories, built from the SAME specs the
carousels use. One source of truth: edit social/carousels.py and both the feed
and the site change together.

  index.html        the four paths, how to read the flags, where I stand
  actors.html       AI actors
  behavior.html     AI behavior
  components.html   AI components
  risk.html         AI risk

Each path page: a card per term, a quiz built from those same terms, and links
to the long form pieces where one exists.
"""
import os, io, json, sys, re

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "social"))
import carousels as C

CATS = C.CATS
ORDER = ["components", "behavior", "actors", "risk"]

BLURB = {
 "components": "The parts, and the words for them. What a model is made of, what it can hold, and what the vocabulary actually means.",
 "behavior":   "What these systems really do. The documented behaviours, including the alarming ones, with the experimental setup attached.",
 "actors":     "Who builds this, who owns it, who can stop it, and what the people at the centre of the argument actually said.",
 "risk":       "What could go wrong, how bad it could get, and which parts are measured against which parts are argued.",
}
LEAD = {
 "components": "warm-neutral", "behavior": "annoyed-skeptical",
 "actors": "noticed-something", "risk": "worry-about-future",
}
DEEP = {
 "actors":     [("frontier.html", "Who controls the frontier",
                 "The whole stack counted, from thousands of companies down to the one that makes the machine that makes the chips.")],
 "components": [("risk/pipeline.html", "How a language model gets made",
                 "Five stages from raw text to a deployed assistant, and which safety work attaches to which stage."),
                ("risk/words.html", "The full glossary",
                 "Thirty five terms defined plainly, with a fourteen question quiz covering all four paths at once.")],
 "risk":       [("risk/taxonomy.html", "Where the worry comes in",
                 "How bad and how it happens are separate questions. A grid you can click through, plus the number people quote at you.")],
 "behavior":   [],
}

def strip(t):
    t = t.replace("<br>", " ")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)) \
        .replace("&rsquo;", "’").replace("&ldquo;", "“").replace("&rdquo;", "”") \
        .replace("&middot;", "·").replace("&amp;", "&").strip()

FLAGNAME = {"emp": "measured", "op": "someone&rsquo;s estimate",
            "arg": "argument", "def": "definition"}
FLAGCLS = {"emp": "emp", "op": "op", "arg": "phil", "def": "def"}

NAV = [("index.html", "home")] + [(c + ".html", CATS[c]) for c in ORDER]

def head(title, desc, current, cat=None):
    links = "".join(
        '<a class="link" href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else '', t)
        for h, t in NAV)
    body_cls = f' class="c-{cat}"' if cat else ""
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
<body{body_cls}>
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
<span>plain language walkthroughs of things that are hard to see clearly</span>
<span>built by elizabeth beier &middot; every claim marked &middot; every source named</span>
</div></footer>
<script src="belle.js"></script>
</body></html>
"""

def page(name, title, desc, body, cat=None):
    html = head(title, desc, name, cat) + body + FOOT
    io.open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
    print(name, len(html))

def belle_img(slug, cls="bfig"):
    p = os.path.join(OUT, "assets", "belle", slug + ".webp")
    if os.path.exists(p):
        return f'<figure class="{cls}"><img src="assets/belle/{slug}.webp" alt="" loading="lazy"></figure>'
    return f'<figure class="{cls}"><div class="bph"><span class="n">{slug}</span></div></figure>'

# ---------------------------------------------------------------- term cards
def cards_for(cat):
    items = [(k, v) for k, v in C.SPECS.items() if v["cat"] == cat]
    out = ['<div class="tcards">']
    for k, sp in items:
        pts = "".join(
            f'<li><b>{strip(t)}</b> {strip(b)}</li>' for _i, t, b in sp["three"])
        out.append(f'''<details class="tcard" name="t-{cat}">
<summary>
  <span class="tname">{strip(sp["term"])}</span>
  <span class="thook">{sp["hook"]}</span>
  <span class="topen">read</span>
</summary>
<div class="tbody">
  <p class="tanswer">{sp["reveal"]}</p>
  <p class="meta">{strip(sp["revsub"])}</p>
  <ul class="tpts">{pts}</ul>
  <p>{sp["why"]} {strip(sp["whysub"])}</p>
  <div class="tfoot">
    <span class="flag {FLAGCLS[sp["flag"]]}">{FLAGNAME[sp["flag"]]}</span>
    <span class="src">{sp["src"]}</span>
  </div>
</div>
</details>''')
    out.append('</div>')
    return "".join(out)

def quiz_for(cat):
    items = [(k, v) for k, v in C.SPECS.items() if v["cat"] == cat]
    qs = []
    for k, sp in items:
        raw = list(sp["opts"])
        correct = raw[1]
        target = sum(ord(c) for c in k) % 4
        rest = [o for i, o in enumerate(raw) if i != 1]
        shown = rest[:target] + [correct] + rest[target:]
        qs.append({"q": strip(sp["q"]), "a": [strip(o) for o in shown],
                   "correct": target, "why": strip(sp["revsub"])})
    return qs

def path_page(cat):
    deep = DEEP[cat]
    deep_html = ""
    if deep:
        rows = "".join(
            f'<a class="xl" href="{h}"><span class="k">go deeper</span>'
            f'<span class="t">{t} &rarr;</span><span class="d">{d}</span></a>' for h, t, d in deep)
        deep_html = f'<h2>The long version</h2><div class="xlinks">{rows}</div>'
    qjs = json.dumps(quiz_for(cat))
    n = len([1 for v in C.SPECS.values() if v["cat"] == cat])
    body = f"""
<div class="wrap hero">
<div class="herogrid">
<div>
<span class="kicker">one of four paths</span>
<h1>{CATS[cat]}</h1>
<p class="lede">{BLURB[cat]}</p>
<div class="tags"><span class="tag rose">{n} terms</span><span class="tag">quiz below</span></div>
</div>
<div class="stage">{belle_img(LEAD[cat], "bfig plain")}</div>
</div>
</div>

<div class="wrap">
<h2>The terms</h2>
<p>Open any one. Each gives the plain answer, three things worth knowing, and how the claim is filed.</p>
{cards_for(cat)}

<h2>Test yourself</h2>
<p>Same questions as the posts. The explanation comes after each answer, so a wrong guess still teaches you the term.</p>
<div class="quizwrap" data-quiz>
  <h3 class="qq"></h3>
  <div class="qopts"></div>
  <p class="qfb"></p>
  <div class="qbar"><span data-count class="meta"></span><span data-score class="meta"></span>
    <button class="btn" type="button" data-next>next</button></div>
</div>

{deep_html}

<div class="xlinks" style="margin-top:var(--s5)">
{"".join(f'<a class="xl" href="{c}.html"><span class="k">next path</span><span class="t">{CATS[c]} &rarr;</span></a>' for c in ORDER if c != cat)}
</div>
</div>
<script>window.QUIZ={qjs};</script>
"""
    page(cat + ".html", CATS[cat], strip(BLURB[cat]), body, cat)

# ---------------------------------------------------------------- home
def home():
    paths = "".join(f'''<a class="path p-{c}" href="{c}.html">
<span class="pn">{CATS[c]}</span>
<span class="pd">{BLURB[c]}</span>
<span class="pc">{len([1 for v in C.SPECS.values() if v["cat"]==c])} terms &middot; quiz</span>
</a>''' for c in ORDER)
    body = f"""
<div class="wrap hero">
<div class="herogrid">
<div>
<span class="kicker">belleofthebot &middot; ai, explained plainly</span>
<h1>Four paths through the thing everyone is arguing about.</h1>
<p class="lede">What these systems are made of, what they actually do, who builds them, and what could go wrong. Plain language, every claim marked, every source named.</p>
<div class="tags">
<span class="tag rose">{len(C.SPECS)} terms</span>
<span class="tag">four quizzes</span>
<span class="tag mint"><span class="dot">&#9679;</span> more coming</span>
</div>
</div>
<div class="stage">{belle_img("hands-out-cheeky", "bfig plain")}</div>
</div>
</div>

<div class="wrap">
<div class="paths">{paths}</div>

<h2>How to read the flags</h2>
<p>Every claim here carries one of four marks. They are the most important thing on the site, because the usual failure of writing about AI is letting these blur together.</p>
<div class="flagkey">
<div class="fk"><span class="flag emp">measured</span><span>A study, survey or evaluation actually counted something.</span></div>
<div class="fk"><span class="flag op">someone&rsquo;s estimate</span><span>A named person said it. That makes the saying a fact and the belief still a belief.</span></div>
<div class="fk"><span class="flag phil">argument</span><span>Reasoned, not counted. It cannot be settled by data alone.</span></div>
<div class="fk"><span class="flag def">definition</span><span>What a word means in this literature. Not a finding, not a forecast.</span></div>
</div>

<div class="well">
<h2 style="margin-top:0">Where I stand</h2>
<p>I am not neutral about this, and I would rather say so than pretend.</p>
<p>I think these systems are already here and worth understanding properly, by ordinary people, not only by the people building them. I also think the risks are real and worth acting on. Not because catastrophe is certain, but because some of the possible outcomes cannot be undone, and the time to think about those is before rather than after.</p>
<p>That position does not change how I handle evidence, and it is why the marks above exist. <strong>A stated view and honest sourcing are not in tension.</strong> If anything the opposite: when you can see where I stand, you can also see every place I decline to overclaim in my own favour. So when something on this site is only an argument, I say so, including when it is an argument I find persuasive.</p>
<p class="meta">Where researchers genuinely disagree, I quote both sides in their own words rather than characterising the one I like less.</p>
</div>

<div class="bsay">
{belle_img("warm-neutral")}
<div><span class="h">who is doing this</span>
<p>I am Elizabeth Beier, a designer who learned to build. I make things with these systems every day, and when a subject is too tangled to hold in my head I do what I have always done with a hard brief: take it apart, draw it, and check my work against the sources.</p></div>
</div>

<div class="note" style="margin-top:var(--s5)">
<span class="h">elsewhere</span>
<p>The same material, one term at a time, at <a href="https://instagram.com/belleofthebot">@belleofthebot</a>. My design and development portfolio is at <a href="https://elizabethbportfolio.com">elizabethbportfolio.com</a>, and the code for this site is at <a href="https://github.com/belleofthebot">github.com/belleofthebot</a>.</p>
</div>
</div>
"""
    page("index.html", "AI, explained plainly",
         "Four paths through AI: components, behaviour, actors and risk. Plain language, every claim marked, every source named.", body)

if __name__ == "__main__":
    home()
    for c in ORDER:
        path_page(c)
    print(f"{len(C.SPECS)} terms across {len(ORDER)} paths")
