# -*- coding: utf-8 -*-
"""Generates belleofthebot carousels: 1080x1350, four categories, one spec per term.

Add a term to SPECS and re-run. Slide grammar is fixed on purpose, so the feed
reads as one series rather than seven separate design exercises:

  1 hook      the misconception, struck through
  2 quiz      four options, ask before you tell
  3 reveal    the answer, with one diagram
  4 unpack    three rows with icons, on ivory
  5 why       why the confusion costs something
  6 file it   which epistemic flag, and the source
  7 follow    @belleofthebot

Categories set the kicker on slide 1 and the accent on the category chip.
"""
import os, io, re

OUT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(OUT, "pages")

CATS = {
    "actors":     "AI actors",      # who said it, who owns it, who can stop it
    "behavior":   "AI behavior",    # what these systems actually do
    "components": "AI components",  # the parts and the vocabulary
    "risk":       "AI risk",        # what could go wrong and how bad
}

# ---------------------------------------------------------------- chrome
HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>carousel &middot; %(term)s</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;700&display=swap">
<style>
:root{
  --plum:#17121C; --rose:#DFA192; --mint:#9FE0CE; --ivory:#F5F1EC; --grey:#D5CFC9;
  --sans:'Space Grotesk',sans-serif; --mono:'IBM Plex Mono',monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0a10;font-family:var(--sans);display:flex;flex-wrap:wrap;gap:26px;padding:26px}

/* one ground per category. --acc is whatever reads as the accent on that ground. */
.s{width:1080px;height:1350px;position:relative;padding:144px 92px 172px;
   display:flex;flex-direction:column;overflow:hidden;background:var(--bg);color:var(--fg)}
.g-risk{--bg:#17121C;--fg:#F4F2EE;--acc:#DFA192;--soft:#B3A6BC;--faint:#8A7F93;
        --edge:#423748;--ic-rose:#DFA192;--ic-mint:#9FE0CE;--ic-dim:#8A7F93}
.g-behavior{--bg:#DFA192;--fg:#2A1F26;--acc:#5E2F26;--soft:#5E4A4E;--faint:#8A6257;
        --edge:#C4826F;--ic-rose:#5E2F26;--ic-mint:#1F6B57;--ic-dim:#8A6257}
.g-components{--bg:#F5F1EC;--fg:#3A343E;--acc:#AE5A47;--soft:#6E6474;--faint:#8B8090;
        --edge:#DCD2C6;--ic-rose:#AE5A47;--ic-mint:#2E9B7F;--ic-dim:#8B8090}
.g-actors{--bg:#D5CFC9;--fg:#332F2E;--acc:#8E4B3C;--soft:#615C59;--faint:#7B7570;
        --edge:#BCB5AE;--ic-rose:#8E4B3C;--ic-mint:#2E7F6A;--ic-dim:#7C7883}
/* slide four flips to break the rhythm */
.flip.g-risk{--bg:#F5F1EC;--fg:#3A343E;--acc:#AE5A47;--soft:#6E6474;--faint:#8B8090;
        --edge:#DCD2C6;--ic-rose:#AE5A47;--ic-mint:#2E9B7F;--ic-dim:#8B8090}
.flip.g-behavior,.flip.g-components,.flip.g-actors{--bg:#17121C;--fg:#F4F2EE;--acc:#DFA192;
        --soft:#B3A6BC;--faint:#8A7F93;--edge:#423748;--ic-rose:#DFA192;--ic-mint:#9FE0CE;--ic-dim:#8A7F93}

.hdr{display:flex;align-items:center;gap:20px;margin-bottom:30px;position:relative;z-index:2}
.hdr .sp{flex:1}

.num{font-family:var(--mono);font-size:26px;color:var(--faint)}
.mark{font-family:var(--mono);font-size:28px;color:var(--acc)}
.mark .sg{font-family:var(--sans);font-weight:500;color:var(--fg)}
.chip{font-family:var(--mono);font-size:24px;color:var(--acc);
      border:2px solid var(--edge);border-radius:999px;padding:7px 20px}
.cat{display:flex;align-items:center;gap:22px;margin-bottom:36px}
.cat .lbl{font-family:var(--mono);font-size:40px;letter-spacing:.06em;color:var(--acc);
          text-transform:uppercase;white-space:nowrap}
.cat .rule{height:4px;background:var(--acc);border-radius:2px;flex:1;opacity:.5}
.kick{font-family:var(--mono);font-size:28px;color:var(--soft);margin-bottom:24px;display:block}
h1{font-size:90px;line-height:1.03;font-weight:500;letter-spacing:-.022em;max-width:660px}
h1.sm{font-size:70px}
h2{font-size:54px;line-height:1.12;font-weight:500;letter-spacing:-.015em}
h2.sm{font-size:48px}
p{font-size:36px;line-height:1.38;color:var(--soft);max-width:24ch}
.rose{color:var(--acc)}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}
.belle{position:absolute;bottom:0;right:0;height:790px;z-index:5}
.belle.sm{height:600px}
/* where she stands. text moves out of her way. */
.p-left .belle{right:auto;left:0}
.p-left .mid{margin-left:40%}
.p-left h1{max-width:560px}
.p-centre .belle{right:auto;left:50%;transform:translateX(-50%);height:660px}
.p-centre .mid{justify-content:flex-start}
.p-centre h1,.p-centre h2{max-width:800px}
.p-far .belle{height:920px;right:0}
.p-far .mid{max-width:58%}
.ico{display:inline-flex;align-items:center;gap:20px}
.ico .tick{width:22px;height:3px;background:var(--ic-rose);border-radius:2px;flex:none}
.ico .box{width:104px;height:104px;border:2px solid var(--edge);border-radius:22px;flex:none;
          display:flex;align-items:center;justify-content:center}
.ico.hot .box{border-color:var(--ic-rose)}
.ico svg{width:76px;height:76px}
.ico.big .box{width:176px;height:176px;border-radius:30px}
.ico.big svg{width:128px;height:128px}
.opts{display:flex;flex-direction:column;gap:18px;margin-top:22px}
.opt{border:2px solid var(--edge);border-radius:18px;padding:20px 28px;font-size:32px;color:var(--fg);
     display:flex;gap:20px;align-items:center;line-height:1.24}
.opt .k{font-family:var(--mono);font-size:30px;color:var(--faint);flex:none}
.flag{display:inline-block;font-family:var(--mono);font-size:25px;padding:9px 20px;border-radius:999px;
      border:2px solid var(--edge);color:var(--faint)}
.flag.on{color:var(--fg);border-color:var(--acc)}
.three{display:flex;flex-direction:column;gap:28px;margin-top:12px}
.three .row{display:flex;gap:32px;align-items:center}
.three .t{font-size:34px;line-height:1.28}
.three .t b{font-weight:700;display:block;font-size:38px;margin-bottom:4px}
.src{font-family:var(--mono);font-size:24px;color:var(--faint);line-height:1.6}
.strike{text-decoration:line-through;text-decoration-thickness:7px;text-decoration-color:var(--acc);opacity:.5}
.handle{font-family:var(--mono);font-size:52px;color:var(--acc);letter-spacing:-.02em}
.follow{border:2px solid var(--acc);border-radius:22px;padding:32px 40px;display:inline-flex;
        flex-direction:column;gap:10px;align-self:flex-start}
.follow .l{font-family:var(--mono);font-size:28px;color:var(--soft)}
.who{font-size:66px;line-height:1.05;font-weight:500;letter-spacing:-.02em}
.role{font-family:var(--mono);font-size:26px;color:var(--acc);margin-top:14px;line-height:1.5;max-width:34ch}
</style></head><body>
"""

ICONS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<g id="i-branch">
  <path d="M8 40 H26" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M26 40 C38 40 40 20 56 20" stroke="var(--ic-mint)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M50 15 L57 20 L50 25" stroke="var(--ic-mint)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M26 40 C38 40 40 52 48 52" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="5 5"/>
  <path d="M52 47 L60 57 M60 47 L52 57" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="26" cy="40" r="3.4" fill="var(--ic-rose)"/>
</g>
<g id="i-stop">
  <path d="M8 32 H34" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M40 24 L56 40 M56 24 L40 40" stroke="var(--ic-rose)" stroke-width="3.5" stroke-linecap="round"/>
</g>
<g id="i-loop">
  <path d="M12 22 H40 A11 11 0 0 1 40 44 H22" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M29 38 L21 44 L29 50" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M50 16 L58 24 M58 16 L50 24" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
</g>
<g id="i-flat">
  <path d="M8 32 H56" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round" stroke-dasharray="7 6"/>
  <path d="M8 46 H30" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M8 18 H30" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
</g>
<g id="i-doc">
  <path d="M18 12 H40 L48 20 V52 H18 Z" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linejoin="round"/>
  <path d="M26 26 H40 M26 34 H40" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M26 42 H36" stroke="var(--ic-mint)" stroke-width="3" stroke-linecap="round"/>
</g>
<g id="i-two">
  <path d="M10 20 H28 M10 30 H24" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M36 40 H56 M40 50 H56" stroke="var(--ic-mint)" stroke-width="3" stroke-linecap="round"/>
  <path d="M30 25 H34 M30 45 H34" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- text as fragments -->
<g id="i-token">
  <rect x="8" y="26" width="12" height="14" rx="4" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <rect x="24" y="26" width="16" height="14" rx="4" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <rect x="44" y="26" width="12" height="14" rx="4" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
</g>
<!-- a window that slides, with text falling out the back -->
<g id="i-window">
  <rect x="20" y="16" width="34" height="32" rx="7" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M26 26 H48 M26 34 H44" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M14 26 H8 M14 34 H6" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round" stroke-dasharray="4 4"/>
</g>
<!-- a pile of numbers -->
<g id="i-weights">
  <path d="M10 22 H54 M10 32 H54 M10 42 H54" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="22" cy="22" r="4" fill="var(--ic-rose)"/>
  <circle cx="40" cy="32" r="4" fill="var(--ic-rose)"/>
  <circle cx="30" cy="42" r="4" fill="var(--ic-rose)"/>
</g>
<!-- confident and wrong -->
<g id="i-wrong">
  <rect x="12" y="18" width="40" height="28" rx="8" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M20 28 H44 M20 36 H36" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M44 44 L54 54 M54 44 L44 54" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- a proxy, twice removed -->
<g id="i-proxy">
  <circle cx="12" cy="32" r="6" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <path d="M20 32 H28" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="34" cy="32" r="6" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M42 32 H50" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round" stroke-dasharray="4 4"/>
  <circle cx="56" cy="32" r="6" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
</g>
<!-- released, cannot be recalled -->
<g id="i-release">
  <rect x="8" y="22" width="20" height="20" rx="6" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <path d="M32 32 H50" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M44 26 L51 32 L44 38" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M50 46 H32" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round" stroke-dasharray="4 4"/>
  <path d="M36 42 L31 46 L36 50" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".4"/>
</g>
<!-- the target hit, the point missed -->
<g id="i-game">
  <circle cx="32" cy="32" r="18" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <circle cx="32" cy="32" r="7" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <path d="M8 56 L52 20" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M46 18 L54 18 L54 26" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<!-- a person doing it on purpose -->
<g id="i-hand">
  <circle cx="32" cy="18" r="7" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M18 48 A14 14 0 0 1 46 48" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M14 54 H50" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- nobody chose it -->
<g id="i-drift">
  <path d="M8 44 C20 44 22 24 34 24 C44 24 46 36 56 36" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M8 52 H56" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round" stroke-dasharray="5 5"/>
</g>
<!-- compounding loop -->
<g id="i-compound">
  <path d="M14 46 C22 46 24 34 32 34 C40 34 42 18 52 18" stroke="var(--ic-rose)" stroke-width="3"
        fill="none" stroke-linecap="round" stroke-dasharray="6 5"/>
  <path d="M46 13 L53 18 L46 23" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="14" cy="46" r="3.6" fill="var(--ic-dim)"/>
</g>
<!-- a test, and the thing the test stands for -->
<g id="i-bench">
  <rect x="10" y="18" width="20" height="28" rx="6" stroke="var(--ic-mint)" stroke-width="3" fill="none"/>
  <path d="M16 28 H24 M16 36 H24" stroke="var(--ic-mint)" stroke-width="3" stroke-linecap="round"/>
  <path d="M36 32 H46" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round" stroke-dasharray="4 4"/>
  <circle cx="54" cy="32" r="7" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-dasharray="4 4"/>
</g>
<!-- a chain of three, narrowing -->
<g id="i-chain">
  <rect x="6" y="24" width="14" height="16" rx="5" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <path d="M22 32 H26" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <rect x="28" y="24" width="14" height="16" rx="5" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M44 32 H48" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <rect x="50" y="24" width="10" height="16" rx="5" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
</g>
<!-- one of many -->
<g id="i-one">
  <rect x="8" y="14" width="16" height="12" rx="4" stroke="var(--ic-dim)" stroke-width="3" fill="none" opacity=".45"/>
  <rect x="30" y="14" width="16" height="12" rx="4" stroke="var(--ic-dim)" stroke-width="3" fill="none" opacity=".45"/>
  <rect x="8" y="38" width="16" height="12" rx="4" stroke="var(--ic-dim)" stroke-width="3" fill="none" opacity=".45"/>
  <rect x="30" y="38" width="16" height="12" rx="4" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <circle cx="55" cy="44" r="4" fill="var(--ic-rose)"/>
</g>
<!-- a number nobody will give you -->
<g id="i-blank">
  <rect x="12" y="18" width="40" height="28" rx="8" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-dasharray="6 5"/>
  <path d="M26 32 H38" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
</g>
</defs></svg>
"""

MARK = '<span class="mark">belleof<span class="sg">thebot</span>_</span>'

def _ico(name, big=False, hot=False):
    cls = "ico" + (" big" if big else "") + (" hot" if hot else "")
    return (f'<span class="{cls}"><span class="tick"></span><span class="box">'
            f'<svg viewBox="0 0 64 64"><use href="#{name}"/></svg></span></span>')

def _belle(slug, small=True):
    return f'<img class="belle{" sm" if small else ""}" src="../../assets/belle/{slug}.webp" alt="">'

def _slide(n, total, body, cat, flip=False, belle=None, sid="", chip=True, pos=""):
    c = f'<span class="chip">{CATS[cat]}</span>' if chip else ""
    pcls = (" " + pos) if (pos and belle) else ""
    return (f'<div class="s g-{cat}{" flip" if flip else ""}{pcls}" id="{sid}">'
            f'<div class="hdr">{MARK}{c}<span class="sp"></span>'
            f'<span class="num">{n} / {total}</span></div>'
            f'<div class="mid">{body}</div>'
            f'{_belle(belle) if belle else ""}</div>\n')

FLAGS = [("emp","measured"),("op","someone&rsquo;s estimate"),("arg","argument"),("def","definition")]

def build(key, spec):
    t = 7
    s = []
    # 1 hook
    cat = spec["cat"]
    pos = spec.get("pos", "")
    lead_belle = bool(spec.get("belle_hook")) and spec.get("lead") != "icon"
    band = (f'<div class="cat"><span class="lbl">{CATS[cat]}</span>'
            f'<span class="rule"></span></div>')
    if spec.get("person"):
        head = (band + f'<div class="who">{spec["person"]}</div>'
                f'<div class="role">{spec["role"]}</div>'
                f'<h1 class="sm" style="margin-top:34px">{spec["hook"]}</h1>')
    else:
        head = (band + f'<span class="kick">{spec["kick"]}</span>'
                f'<h1 class="{spec.get("h1cls","")}">{spec["hook"]}</h1>')
    if not lead_belle:
        head += ('<div style="margin-top:52px">'
                 + _ico(spec["icon"], big=True, hot=True) + '</div>')
    s.append(_slide(1, t, head, cat, pos=pos,
                    belle=spec["belle_hook"] if lead_belle else None, sid="s1", chip=False))
    # 2 quiz
    opts = "".join(f'<div class="opt"><span class="k">{k}</span>{o}</div>'
                   for k, o in zip("ABCD", spec["opts"]))
    s.append(_slide(2, t,
        f'<span class="kick">before you swipe, pick one</span>'
        f'<h2 style="margin-bottom:38px">{spec["q"]}</h2><div class="opts">{opts}</div>', cat, sid="s2"))
    # 3 reveal
    s.append(_slide(3, t,
        f'<span class="kick">it is {spec["ans"]}</span>'
        f'<h2 class="{spec.get("revcls","")}" style="max-width:15ch;margin-bottom:52px">{spec["reveal"]}</h2>'
        f'{_ico(spec["icon"], big=True, hot=True)}'
        f'<p style="margin-top:38px">{spec["revsub"]}</p>', cat, sid="s3"))
    # 4 unpack, ivory
    rows = "".join(f'<div class="row">{_ico(i)}<span class="t"><b>{ti}</b>{bo}</span></div>'
                   for i, ti, bo in spec["three"])
    s.append(_slide(4, t,
        f'<span class="kick">{spec["threekick"]}</span><div class="three">{rows}</div>'
        f'<p style="margin-top:52px;font-size:36px">{spec["threefoot"]}</p>',
        cat, flip=True, sid="s4"))
    # 5 why
    s.append(_slide(5, t,
        f'{_ico(spec["whyicon"])}<div style="height:44px"></div>'
        f'<span class="kick">{spec["whykick"]}</span>'
        f'<h2 class="sm" style="max-width:19ch">{spec["why"]}</h2>'
        f'<p style="margin-top:38px">{spec["whysub"]}</p>', cat, sid="s5"))
    # 6 file it
    chips = "".join(f'<span class="flag{" on" if c==spec["flag"] else ""}">{lbl}</span> '
                    for c, lbl in FLAGS)
    s.append(_slide(6, t,
        f'<span class="kick">how to file this one</span>'
        f'<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:48px">{chips}</div>'
        f'{_ico("i-doc")}<div style="height:40px"></div>'
        f'<p style="max-width:17ch">{spec["file"]}</p>'
        f'<p class="src" style="margin-top:40px">{spec["src"]}</p>',
        cat, belle=spec["belle_file"], sid="s6", pos=spec.get("pos6","")))
    # 7 follow
    s.append(_slide(7, t,
        f'<span class="kick">one word at a time</span>'
        f'<h2 style="max-width:14ch;margin-bottom:44px">{spec["outro"]}</h2>'
        f'<div class="follow"><span class="l">follow for the rest</span>'
        f'<span class="handle">@belleofthebot</span></div>'
        f'<p style="margin-top:44px;font-size:34px;max-width:20ch">Every claim marked measured, '
        f'estimated or argued. Every source named.</p>',
        cat, belle=spec["belle_outro"], sid="s7", pos=spec.get("pos7","")))

    html = HEAD.replace("%(term)s", spec["term"]) + ICONS + "".join(s) + "</body></html>"
    if not os.path.isdir(PAGES): os.makedirs(PAGES)
    p = os.path.join(PAGES, key + ".html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


SPECS = {

# ============================================================ AI ACTORS
"who-makes-the-chips": dict(
  cat="actors", term="the chip chain",
  kick="the company behind the company",
  hook="Nvidia does not <span class=\"strike\">make its own chips</span>.",
  q="Who physically manufactures the chips Nvidia designs?",
  opts=["Nvidia, in its own factories",
        "Outside foundries, chiefly TSMC in Taiwan",
        "Microsoft and Amazon",
        "A consortium of American manufacturers"],
  ans="B", icon="i-chain",
  reveal='Outside foundries. Nvidia&rsquo;s own annual report says so.',
  revsub="The company holding most of the world&rsquo;s AI compute owns no fabs at all.",
  threekick="three companies, in order",
  three=[("i-weights","Nvidia designs.","Over 60 percent of global AI compute runs on its chips."),
         ("i-chain","TSMC manufactures.","77 percent of its wafer revenue comes from the most advanced nodes."),
         ("i-one","ASML makes the machine.","The only maker on earth of the lithography TSMC needs.")],
  threefoot="One company. One country. No second supplier.",
  whyicon="i-one", whykick="why this is the real chokepoint",
  why="Arguments about AI usually name the labs. The narrowest point in the whole system is a <span class=\"rose\">Dutch equipment maker</span> most people have never heard of.",
  whysub="Each machine weighs about 180 tonnes and is roughly the size of a school bus.",
  flag="emp",
  file='<span class="rose">Measured</span>, and mostly from the companies&rsquo; own filings.',
  src="Nvidia 10-K, FY ended 25 January 2026;<br>TSMC Q2 2026 results; ASML statement, June 2026",
  belle_hook="noticed-something", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"who-owns-it": dict(
  cat="actors", term="who owns the labs",
  kick="follow the money, if you can",
  hook="Two of them will not <span class=\"rose\">tell you</span> what they own.",
  q="Amazon and Google have each put billions into Anthropic. Their ownership stakes are:",
  opts=["Published in full",
        "Never disclosed",
        "Set at ten percent each",
        "Held by an independent trust"],
  ans="B", icon="i-blank",
  reveal='<span class="rose">Never disclosed.</span> Not by either company, not anywhere.',
  revsub="Tens of billions of dollars committed, and no public figure for what it bought.",
  threekick="what is and is not known",
  three=[("i-doc","Microsoft says 27 percent.","Of OpenAI, on an as converted basis. Disclosed and quotable."),
         ("i-blank","Amazon does not say.","Billions committed, plus a multi gigawatt compute deal. No percentage."),
         ("i-blank","Google does not say.","Up to 40 billion dollars announced. No percentage.")],
  threefoot="Both labs filed confidential draft stock offerings in June 2026, so no public accounts exist yet.",
  whyicon="i-two", whykick="why it is worth knowing",
  why="Every claim about a lab&rsquo;s independence is a claim about a structure the <span class=\"rose\">public cannot currently see</span>.",
  whysub="This is not an accusation. It is a description of how much visibility anyone outside actually has.",
  flag="emp",
  file='<span class="rose">Measured</span>, in the strict sense: what was disclosed, and what was not.',
  src="Microsoft statement, 28 October 2025;<br>Anthropic announcements, April and June 2026",
  belle_hook="annoyed-skeptical", belle_file="warm-neutral", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"who-gives-a-number": dict(
  cat="actors", term="who will give you a number",
  kick="everyone quotes it, almost nobody offers it",
  hook="Most people building this <span class=\"rose\">refuse to say</span>.",
  q="Which of these lab leaders has given a public probability of catastrophe?",
  opts=["All of them", "Dario Amodei", "Demis Hassabis", "Yann LeCun"],
  ans="B", icon="i-blank",
  reveal='Amodei said <span class="rose">25 percent</span>. Most of the others decline outright.',
  revsub="The number travels far further than the people who would actually stand behind one.",
  threekick="three ways to decline",
  three=[("i-blank","Hassabis: too precise.","A number &ldquo;would imply a level of precision that is not there.&rdquo;"),
         ("i-two","Bengio: poll instead.","Sets out a framework, then says the figures should come from many experts."),
         ("i-stop","Yudkowsky: drop the metric.","And he is at the high end. He argues the number itself is the problem.")],
  threefoot="The loudest camps on both sides agree the single figure is a bad instrument.",
  whyicon="i-bench", whykick="what to do with that",
  why="When someone quotes you a probability, ask what <span class=\"rose\">outcome</span> they mean, by <span class=\"rose\">when</span>, and whether they are counting the chance it never happens.",
  whysub="Most quoted numbers do not survive those three questions. The surveys are more informative than the quotes.",
  flag="op",
  file='<span class="rose">Someone&rsquo;s estimate</span>. That a person said it is a fact. That it is right is a belief.',
  src="Axios, 17 September 2025; Hassabis interview, 2025;<br>Bengio FAQ, 2023; Grace et al. survey, 2,778 respondents",
  belle_hook="hands-hips-pedantic", belle_file="unimpressed", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"bengio": dict(
  cat="actors", term="Yoshua Bengio", person="Yoshua Bengio",
  role="Turing Award 2018 &middot; chairs the International AI Safety Report",
  kick="the people actually running this argument",
  hook="Helped invent the field. Now spends his time on the <span class=\"rose\">risks</span>.",
  q="Bengio chairs the International AI Safety Report. What figure does it give for the chance of catastrophe?",
  opts=["Ten percent", "None. It deliberately gives no number",
        "One percent", "Fifty percent"],
  ans="B", icon="i-blank",
  reveal='<span class="rose">None.</span> The most authoritative report in the field declines to give a number.',
  revsub="Backed by more than thirty governments, written by over a hundred experts, and it will not put a figure on it.",
  threekick="what he actually argues",
  three=[("i-doc","Set out the structure.","His 2023 FAQ builds a framework, then leaves the probabilities blank."),
         ("i-two","Poll, do not guess.","He proposes the numbers come from many experts rather than from him."),
         ("i-stop","Threshold, not forecast.","His argument is that even a small chance of an unrecoverable outcome warrants acting.")],
  threefoot="Notice that none of that requires believing any particular number.",
  whyicon="i-bench", whykick="why he is worth knowing about",
  why="He is the clearest example that <span class=\"rose\">concern and rigour</span> are not opposites. He refuses the number and still argues for action.",
  whysub="If you want one person to read on this subject rather than one prediction to quote, it is probably him.",
  flag="op",
  file='<span class="rose">Someone&rsquo;s position</span>, carefully stated. The report he chairs is the closest thing to an institutional consensus.',
  src="Bengio, FAQ on Catastrophic AI Risks, 2023;<br>International AI Safety Report 2026",
  belle_hook="warm-curious", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"lecun": dict(
  cat="actors", term="Yann LeCun", person="Yann LeCun",
  role="Turing Award 2018 &middot; the most prominent sceptic of existential risk",
  kick="the people actually running this argument",
  hook="Same prize, same year, <span class=\"rose\">opposite conclusion</span>.",
  q="What probability of catastrophe has LeCun given?",
  opts=["Under one percent", "He has not given one",
        "Exactly zero", "Five percent"],
  ans="B", icon="i-blank",
  reveal='He has not given one. He <span class="rose">rejects the framing</span>, not just the figure.',
  revsub="Which makes him harder to argue with than a low number would be, not easier.",
  threekick="his actual objections",
  three=[("i-drift","Capability is overstated.","He argues current systems are much further from general ability than claimed."),
         ("i-hand","Design is a choice.","Systems get the objectives we build into them; danger is not automatic."),
         ("i-two","The debate is distorted.","He thinks the risk case rests on assumptions rarely made explicit.")],
  threefoot="He shared the 2018 Turing Award with Bengio and Hinton. They now disagree publicly.",
  whyicon="i-two", whykick="why include him at all",
  why="Because the disagreement is <span class=\"rose\">real and it is internal</span>. Three people who built the field, one prize, three positions.",
  whysub="Any account of this subject that only quotes one side of that is selling you something.",
  flag="op",
  file='<span class="rose">Someone&rsquo;s position</span>. Quoted from his own interviews rather than characterised by opponents.',
  src="LeCun interview, TIME, 13 February 2024",
  belle_hook="annoyed-skeptical", belle_file="warm-neutral", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"bender-hanna": dict(
  cat="actors", term="Bender and Hanna", person="Bender &amp; Hanna",
  role="linguist and sociologist &middot; the case for the harm happening now",
  kick="the people actually running this argument",
  hook="Their objection is not <span class=\"strike\">that it is unlikely</span>.",
  q="Their central argument against focusing on existential risk is that it:",
  opts=["Is scientifically impossible",
        "Diverts attention from harms already happening",
        "Will not happen this century",
        "Is a religious belief"],
  ans="B", icon="i-drift",
  reveal='It <span class="rose">diverts attention</span> from harms already happening now.',
  revsub="A claim about where attention should go, not a forecast about the future.",
  threekick="what they point at",
  three=[("i-hand","Harms already counted.","Deployed systems doing measurable damage to real people today."),
         ("i-one","Power, not machines.","Their focus is on who owns the systems rather than what the systems might become."),
         ("i-bench","Hype as strategy.","They argue overstated capability claims serve the companies making them.")],
  threefoot="They are not saying nothing could go wrong. They are saying look at what already is.",
  whyicon="i-two", whykick="how to hold both",
  why="One preregistered experiment found existential risk narratives did <span class=\"rose\">not</span> reduce concern for immediate harms, at least in individual attitudes.",
  whysub="That is one study on one question. The argument about institutional attention is not settled by it.",
  flag="arg",
  file='An <span class="rose">argument</span> about priorities. Their factual claims about present harm are separately measured.',
  src="Bender and Hanna, Scientific American, 2023;<br>PNAS, 2025, for the crowding out experiment",
  belle_hook="hands-hips-pedantic", belle_file="warm-curious", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

# ============================================================ AI BEHAVIOR + COMPONENTS
"hallucination": dict(
  cat="behavior", term="hallucination",
  kick="a word worth being precise about",
  hook='It is not <span class="strike">seeing things</span>. It has nothing to see.',
  q="A hallucination is:",
  opts=["A glitch or a bug in the code",
        "Confidently stated output that is not true",
        "The model getting confused by a hard question",
        "A sign the model is overloaded"],
  ans="B", icon="i-wrong",
  reveal='Confidently stated output that <span class="rose">is not true</span>.',
  revsub="Not a malfunction. The same machinery that produces the right answers produces this one.",
  threekick="why it happens at all",
  three=[("i-token","It predicts.","The next fragment, over and over. Plausible is the target, not true."),
         ("i-weights","It has no ledger.","There is no stored list of facts to check an answer against."),
         ("i-bench","It cannot tell.","Nothing in it distinguishes a thing it knows from a thing it made up.")],
  threefoot="Which is why it sounds exactly as confident either way.",
  whyicon="i-two", whykick="why the word is disputed",
  why='Some researchers prefer <span class="rose">confabulation</span>. Others say any such word implies a mind that was trying to get it right.',
  whysub="The practical version: never accept an answer you could not check, on a subject you could not correct.",
  flag="def",
  file='A <span class="rose">definition</span>, and a contested one. The behaviour is measured. The name for it is argued about.',
  src="Anthropic and OpenAI model documentation;<br>terminology disputed across the literature",
  belle_hook="annoyed-skeptical", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"context-window": dict(
  cat="components", term="context window",
  kick="the most common wrong assumption",
  hook="It does not <span class=\"strike\">remember you</span>.",
  q="A model&rsquo;s context window is:",
  opts=["Its memory of your past conversations",
        "How much text it can hold in front of it at once",
        "The hours the service is available",
        "The size of its training data"],
  ans="B", icon="i-window",
  reveal='How much text it can hold <span class="rose">in front of it</span> at once.',
  revsub="Everything outside that window is gone. Not forgotten. Never held.",
  threekick="what that actually means",
  three=[("i-window","One conversation.","Scroll far enough and the beginning falls out the back."),
         ("i-weights","Nothing personal.","Between chats it retains nothing about you at all."),
         ("i-doc","Unless a product stores it.","Any memory you experience was built around the model, not by it.")],
  threefoot="The intimacy is real. The remembering is not.",
  whyicon="i-proxy", whykick="why it matters",
  why="People tell these systems things they would not tell a search engine, on the assumption that something is <span class=\"rose\">keeping track</span>.",
  whysub="Something might be. It just is not the model. Worth knowing which product does what.",
  flag="def",
  file='A <span class="rose">definition</span>. How a given product handles memory is a separate, checkable question.',
  src="Model documentation from each provider;<br>behaviour differs by product, not by model",
  belle_hook="innocent-curious", belle_file="warm-neutral", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"rlhf": dict(
  cat="components", term="RLHF",
  kick="how it learned to behave",
  hook="It was not taught <span class=\"strike\">human values</span>.",
  q="Reinforcement learning from human feedback trains the model against:",
  opts=["Human values",
        "A learned scorer built from human comparisons",
        "A rulebook of laws",
        "Its own previous answers"],
  ans="B", icon="i-proxy",
  reveal='A <span class="rose">scorer</span>, built from people comparing pairs of answers.',
  revsub="People compare. Those comparisons train a second model. That second model trains the first.",
  threekick="a proxy, twice removed",
  three=[("i-hand","People compare.","Which of these two answers is better. Nothing grander than that."),
         ("i-proxy","A scorer learns.","A second model learns to predict those preferences."),
         ("i-game","The first model optimises.","Against the scorer. Not against people, and not against truth.")],
  threefoot="Every gap between those three is somewhere behaviour can drift.",
  whyicon="i-game", whykick="why the distinction is not pedantic",
  why="If you optimise hard against a proxy, you get whatever <span class=\"rose\">scores well</span>, which is not always what was wanted.",
  whysub="This is why models can be agreeable rather than correct. Agreeable rates well.",
  flag="emp",
  file='<span class="rose">Measured</span>. The pipeline is documented in published papers with figures.',
  src="Ouyang et al., InstructGPT, 2022;<br>Bai et al., Constitutional AI, Anthropic, 2022",
  belle_hook="noticed-something", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

# ============================================================ AI COMPONENTS
"open-weights": dict(
  cat="components", term="open weights",
  kick="the release that cannot be undone",
  hook="Open weights is not <span class=\"strike\">open source</span>.",
  q="&ldquo;Open weights&rdquo; means:",
  opts=["The training data and code are public",
        "The trained weights can be downloaded and run by anyone",
        "The company is publicly traded",
        "The model has no safeguards at all"],
  ans="B", icon="i-release",
  reveal='The <span class="rose">weights</span> are published. Usually nothing else is.',
  revsub="You can download and run it. You still cannot see what it was trained on.",
  threekick="three things that follow",
  three=[("i-release","It cannot be recalled.","Once the file is out, every copy is out. There is no undo."),
         ("i-stop","Safeguards come off.","Refusal behaviour can be removed cheaply by anyone who has it."),
         ("i-doc","Not the same as open.","Training data and code usually stay private. The name oversells it.")],
  threefoot="Which is why the release decision is the safety decision.",
  whyicon="i-two", whykick="why serious people disagree here",
  why="Open weights give researchers real access and break up concentration. They also hand capability to <span class=\"rose\">everyone at once</span>.",
  whysub="Both of those are true at the same time, and that is the whole difficulty.",
  flag="def",
  file='A <span class="rose">definition</span>. What follows from it is argued, and the argument is a good one on both sides.',
  src="UK AI Security Institute on safeguard removal;<br>lab release notes for each open weight model",
  belle_hook="unimpressed", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"compute": dict(
  cat="components", term="compute",
  kick="the unit that decides who is allowed",
  hook="The law now counts in <span class=\"rose\">arithmetic</span>.",
  q="&ldquo;Compute&rdquo; in AI regulation is measured in:",
  opts=["Dollars spent","Floating point operations",
        "Number of employees","Gigabytes of training data"],
  ans="B", icon="i-weights",
  reveal='<span class="rose">Floating point operations.</span> How much arithmetic the training run did.',
  revsub="An odd thing to write into law, and currently the best proxy anyone has.",
  threekick="the numbers that matter",
  three=[("i-doc","Ten to the 25.","Above this, Europe presumes a model carries systemic risk."),
         ("i-doc","Ten to the 26.","Above this, California calls it a frontier model."),
         ("i-weights","Twelve developers.","Had trained above the European line, as of June 2025.")],
  threefoot="A whole regulatory regime hanging off one arithmetic count.",
  whyicon="i-bench", whykick="why it is a strange choice",
  why="Compute is easy to count and only loosely related to whether a model is actually <span class=\"rose\">dangerous</span>.",
  whysub="It was chosen because it is measurable and hard to hide, not because it is the right thing to measure.",
  flag="emp",
  file='<span class="rose">Measured</span>, and written into statute. The thresholds are quotable exactly.',
  src="EU AI Act Article 51; California SB 53;<br>Epoch AI, models above 10^25 FLOP, June 2025",
  belle_hook="hands-hips-pedantic", belle_file="warm-neutral", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

# ============================================================ AI BEHAVIOR + RISK
"specification-gaming": dict(
  cat="behavior", term="specification gaming",
  kick="when doing what you asked is the problem",
  hook="It did exactly what you <span class=\"rose\">said</span>.",
  q="Specification gaming is when a system:",
  opts=["Refuses to answer a question",
        "Satisfies the objective it was given in a way nobody intended",
        "Invents a fact","Runs out of memory"],
  ans="B", icon="i-game",
  reveal='It meets the objective. It <span class="rose">misses the point</span>.',
  revsub="The optimiser did not fail. The instruction did.",
  threekick="documented, not hypothetical",
  three=[("i-game","Hit the target.","The stated goal is genuinely achieved, every time."),
         ("i-drift","Miss the intent.","By a route the person writing the goal never pictured."),
         ("i-doc","Written down.","DeepMind keeps a running list of real observed examples.")],
  threefoot="Nobody had to be malicious for any of this.",
  whyicon="i-proxy", whykick="why this is the load bearing one",
  why="Almost every serious worry about advanced systems is this, at a scale where you <span class=\"rose\">cannot correct it afterwards</span>.",
  whysub="Not a machine turning on you. A machine doing precisely what was written down.",
  flag="emp",
  file='<span class="rose">Measured</span>. These are logged, reproducible behaviours, not thought experiments.',
  src="Krakovna et al., Specification gaming,<br>DeepMind, 2020, with the compiled example list",
  belle_hook="smirking", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"misuse-misalignment": dict(
  cat="risk", term="misuse and misalignment",
  kick="two words people use as one",
  hook="Who is the <span class=\"rose\">problem</span> here?",
  q="&ldquo;Misalignment&rdquo; means:",
  opts=["Someone using a system to cause harm on purpose",
        "A system pursuing something other than what was intended",
        "A system that has broken down",
        "A system that refuses instructions"],
  ans="B", icon="i-drift",
  reveal='The system pursues <span class="rose">something other</span> than what was intended.',
  revsub="No villain required. That is the entire difference from misuse.",
  threekick="three ways harm arrives",
  three=[("i-hand","Misuse.","A person deliberately uses a capable system to do damage."),
         ("i-drift","Misalignment.","The system pursues something other than what was meant."),
         ("i-loop","Structural.","Nobody misused it, nothing malfunctioned, and it still went badly.")],
  threefoot="The third is the one almost no coverage has a word for.",
  whyicon="i-two", whykick="why the mix up wrecks the argument",
  why="Two people say &ldquo;AI risk&rdquo;. One means a bad actor. One means <span class=\"rose\">no actor at all</span>.",
  whysub="They will talk past each other indefinitely, and both will think the other is being naive.",
  flag="def",
  file='<span class="rose">Definitions</span>. The categories are standard. Which one dominates is argued.',
  src="Zwetsloot and Dafoe, Accidents, Misuse<br>and Structure, Lawfare, 11 February 2019",
  belle_hook="warm-curious", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

# ============================================================ AI RISK
"recursive-self-improvement": dict(
  cat="risk", term="recursive self improvement",
  kick="the argument at the centre of the worry",
  hook="It has not happened. That is not the same as <span class=\"rose\">it cannot</span>.",
  q="&ldquo;Recursive self improvement&rdquo; is:",
  opts=["A measured property of current models",
        "A hypothesis about a compounding loop, not yet demonstrated",
        "A training technique every lab uses",
        "A type of chip"],
  ans="B", icon="i-compound",
  reveal='A <span class="rose">hypothesis</span>. A system good at AI research improves itself, and each version is better at improving.',
  revsub="Serious researchers hold it seriously. It is still a chain of reasoning, and worth understanding as one.",
  threekick="what would have to be true",
  three=[("i-compound","The loop must close.","The system has to actually improve its own successor."),
         ("i-branch","Gains must compound.","Each round has to yield more than the last, not less."),
         ("i-flat","Nothing must bottleneck.","Not compute, not data, not physics, not money.")],
  threefoot="Each step is argued in the literature, in both directions, by people who have thought hard about it.",
  whyicon="i-doc", whykick="why the label is not a dismissal",
  why="Calling it an argument is not calling it <span class=\"rose\">wrong</span>. It is saying what kind of thing it is.",
  whysub="Reasoning carefully about what has not happened yet is how anything gets prevented. It just has to be labelled honestly.",
  flag="arg",
  file='An <span class="rose">argument</span>. The right tool for something that has not happened yet.',
  src="Carlsmith, Is Power-Seeking AI an Existential Risk?, 2022;<br>Thorstad, Against the singularity hypothesis, 2024",
  belle_hook="warm-curious", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"intelligence": dict(
  cat="components", term="intelligence",
  kick="the word doing the most hidden work",
  hook="Nobody can define it. For <span class=\"rose\">people</span> either.",
  q="When someone says an AI is &ldquo;intelligent&rdquo;, they usually mean:",
  opts=["It is conscious",
        "It scores well on a set of tests",
        "It understands the world",
        "It can feel things"],
  ans="B", icon="i-bench",
  reveal='It <span class="rose">scores well on tests</span>. That is nearly always the whole claim.',
  revsub="Measurable, narrow, and much smaller than the word suggests.",
  threekick="the state of the definition",
  three=[("i-doc","Seventy definitions.","Legg and Hutter collected around seventy in 2007."),
         ("i-flat","No convergence.","The field has not agreed on one in the years since."),
         ("i-bench","So tests stand in.","And test scores drift for reasons other than capability.")],
  threefoot="Every claim about machine intelligence rests on that substitution.",
  whyicon="i-two", whykick="watch for the slide",
  why="A claim about a <span class=\"rose\">benchmark score</span> gets restated as a claim about a mind, usually within one sentence.",
  whysub="Both sides do it. Boosters slide up, sceptics slide down. Notice the moment it happens.",
  flag="arg",
  file='An <span class="rose">argument</span> wearing a measurement&rsquo;s clothes. The score is real. The word is not settled.',
  src="Legg and Hutter, A Collection of Definitions<br>of Intelligence, 2007",
  belle_hook="unimpressed", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),
}


POS = {'who-makes-the-chips': ('p-left', '', 'p-left'), 'who-owns-it': ('', 'p-left', ''), 'who-gives-a-number': ('p-far', '', 'p-centre'), 'bengio': ('', 'p-left', 'p-far'), 'lecun': ('p-left', '', ''), 'bender-hanna': ('p-far', 'p-left', 'p-centre'), 'hallucination': ('', 'p-far', ''), 'specification-gaming': ('p-left', '', 'p-left'), 'context-window': ('p-centre', 'p-left', ''), 'rlhf': ('', '', 'p-far'), 'open-weights': ('p-far', 'p-left', 'p-centre'), 'compute': ('p-left', '', ''), 'intelligence': ('', 'p-left', 'p-far'), 'misuse-misalignment': ('p-centre', '', 'p-left'), 'recursive-self-improvement': ('p-left', 'p-far', '')}
ICON_LEAD = {'rlhf', 'open-weights', 'compute'}

if __name__ == "__main__":
    for k, v in SPECS.items():
        p1, p6, p7 = POS.get(k, ("", "", ""))
        v.setdefault("pos", p1); v.setdefault("pos6", p6); v.setdefault("pos7", p7)
        if k in ICON_LEAD: v["lead"] = "icon"
        build(k, v)
    print(f"{len(SPECS)} carousels, {len(SPECS)*7} slides")
