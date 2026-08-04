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
    "components": "AI components",  # the parts, and how they are built and tested
    "concepts":   "AI concepts",    # the abstract ideas that need defining
    "risk":       "AI risk",        # what could go wrong and how bad
}

# ---------------------------------------------------------------- chrome
HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>carousel &middot; %(term)s</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;700&display=swap">
<style>
:root{
  --plum:#17121C; --rose:#DFA192; --mint:#9FE0CE; --ivory:#F5F1EC; --grey:#B9B2AC;
  --sans:'Space Grotesk',sans-serif; --mono:'IBM Plex Mono',monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0a10;font-family:var(--sans);display:flex;flex-wrap:wrap;gap:26px;padding:26px}

/* one ground per category. --acc is whatever reads as the accent on that ground. */
.s{width:1080px;height:1350px;position:relative;padding:144px 92px 172px;
   display:flex;flex-direction:column;overflow:hidden;background:var(--bg);color:var(--fg)}
.g-concepts{--bg:#6E5570;--fg:#F6F1F6;--acc:#E8C4E4;--soft:#D6C4D6;--faint:#B49CB4;
        --edge:#8B6E8D;--ic-rose:#E8C4E4;--ic-mint:#9FE0CE;--ic-dim:#B49CB4}
.flip.g-concepts{--bg:#F5F1EC;--fg:#3A343E;--acc:#7A5A7C;--soft:#6E6474;--faint:#8B8090;
        --edge:#DCD2C6;--ic-rose:#7A5A7C;--ic-mint:#2E9B7F;--ic-dim:#8B8090}
.g-risk{--bg:#17121C;--fg:#F4F2EE;--acc:#DFA192;--soft:#B3A6BC;--faint:#8A7F93;
        --edge:#423748;--ic-rose:#DFA192;--ic-mint:#9FE0CE;--ic-dim:#8A7F93}
.g-behavior{--bg:#DFA192;--fg:#2A1F26;--acc:#5E2F26;--soft:#5E4A4E;--faint:#8A6257;
        --edge:#C4826F;--ic-rose:#5E2F26;--ic-mint:#1F6B57;--ic-dim:#8A6257}
.g-components{--bg:#F5F1EC;--fg:#3A343E;--acc:#AE5A47;--soft:#6E6474;--faint:#8B8090;
        --edge:#DCD2C6;--ic-rose:#AE5A47;--ic-mint:#2E9B7F;--ic-dim:#8B8090}
.g-actors{--bg:#B9B2AC;--fg:#2B2826;--acc:#7A3A2C;--soft:#514C48;--faint:#6A645F;
        --edge:#9C948D;--ic-rose:#8E4B3C;--ic-mint:#2E7F6A;--ic-dim:#7C7883}
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
h1{font-size:74px;line-height:1.06;font-weight:500;letter-spacing:-.022em;max-width:660px}
h1.sm{font-size:62px}
h2{font-size:54px;line-height:1.12;font-weight:500;letter-spacing:-.015em}
h2.sm{font-size:48px}
p{font-size:36px;line-height:1.38;color:var(--soft);max-width:24ch}
.rose{color:var(--acc)}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}
.belle{position:absolute;bottom:0;right:0;height:930px;z-index:5}
.belle.sm{height:640px}
/* where she stands. text moves out of her way. */
.p-left .belle{right:auto;left:0}
.p-left .mid{margin-left:44%}
.p-left h1{max-width:560px}
.p-centre .belle{right:auto;left:50%;transform:translateX(-50%);height:820px}
.p-centre .mid{justify-content:flex-start}
.p-centre h1,.p-centre h2{max-width:800px}
.p-far .belle{height:1030px;right:0}
.p-far .mid{max-width:54%}

/* the cover. no wordmark, no counter, no chip. one line and her. */
.cover{padding:150px 92px 0}
.cover .hdr{display:none}
.cover .mid{flex:0 0 auto;justify-content:flex-start}
.cover h1{font-size:88px;line-height:1.04;max-width:15ch;letter-spacing:-.024em}
.cover .who{font-size:96px}
.cover .role{font-size:30px;margin-top:18px;max-width:26ch}
.cover .belle{right:auto;left:50%;transform:translateX(-50%);height:840px;bottom:0}
.cover .swipe{display:flex;align-items:center;gap:14px;margin-top:40px;
  font-family:var(--mono);font-size:27px;color:var(--faint)}
.cover .swipe .ar{width:44px;height:2px;background:var(--acc);position:relative;opacity:.8}
.outro .belle{right:0;left:auto;transform:none;height:600px}
.outro .mid{max-width:56%}
.cover .swipe .ar::after{content:"";position:absolute;right:0;top:-4px;width:10px;height:10px;
  border-top:2px solid var(--acc);border-right:2px solid var(--acc);transform:rotate(45deg)}
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
.who{font-size:72px;line-height:1.05;font-weight:500;letter-spacing:-.02em}
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

<!-- an undisclosed stake: two holdings, one of them dashed -->
<g id="i-stake">
  <circle cx="24" cy="32" r="14" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <circle cx="42" cy="32" r="14" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-dasharray="6 5"/>
</g>
<!-- a named person, saying it out loud -->
<g id="i-voice">
  <circle cx="20" cy="22" r="7" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <path d="M8 46 A12 12 0 0 1 32 46" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M42 22 A13 13 0 0 1 42 42" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M52 15 A21 21 0 0 1 52 49" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" opacity=".45"/>
</g>
<!-- two people, pointing the opposite way -->
<g id="i-counter">
  <path d="M8 24 H28" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M22 18 L29 24 L22 30" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M56 42 H36" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M42 36 L35 42 L42 48" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<!-- a dial with no agreed reading -->
<g id="i-gauge">
  <path d="M10 46 A22 22 0 0 1 54 46" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M32 46 L45 29" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round" stroke-dasharray="5 4"/>
  <circle cx="32" cy="46" r="3.6" fill="var(--ic-rose)"/>
</g>
<!-- reading the wording closely -->
<g id="i-lens">
  <path d="M9 18 H33 M9 27 H27" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="36" cy="35" r="12" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M45 44 L55 54" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- the headline, and the measurement -->
<g id="i-decline">
  <rect x="13" y="14" width="13" height="34" rx="4" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-dasharray="5 4"/>
  <rect x="38" y="36" width="13" height="12" rx="4" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M8 54 H56" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- two different causes, one outcome -->
<g id="i-twocause">
  <circle cx="12" cy="16" r="5" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
  <path d="M18 21 C30 26 32 30 40 32" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M8 50 C22 50 26 38 40 34" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="5 5"/>
  <path d="M47 27 L57 37 M57 27 L47 37" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- the post keeps moving -->
<g id="i-goalpost">
  <path d="M13 14 V50" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M19 32 H39" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round" stroke-dasharray="5 4"/>
  <path d="M33 26 L40 32 L33 38" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M50 14 V50" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round" stroke-dasharray="6 5"/>
</g>
<!-- seventy definitions in a pile -->
<g id="i-stack">
  <rect x="6" y="14" width="32" height="13" rx="5" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-dasharray="5 4"/>
  <rect x="16" y="28" width="32" height="13" rx="5" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-dasharray="5 4" opacity=".6"/>
  <rect x="26" y="42" width="32" height="13" rx="5" stroke="var(--ic-rose)" stroke-width="3" fill="none"/>
</g>
<!-- the test knows it is being watched -->
<g id="i-watched">
  <rect x="8" y="16" width="24" height="32" rx="6" stroke="var(--ic-mint)" stroke-width="3" fill="none"/>
  <path d="M14 26 H26 M14 34 H26" stroke="var(--ic-mint)" stroke-width="3" stroke-linecap="round"/>
  <path d="M37 32 C43 24 52 24 58 32 C52 40 43 40 37 32 Z" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linejoin="round"/>
  <circle cx="47.5" cy="32" r="3.6" fill="var(--ic-rose)"/>
</g>
<!-- a message with a threat in it -->
<g id="i-threat">
  <path d="M10 14 H54 V38 H30 L20 48 V38 H10 Z" stroke="var(--ic-dim)" stroke-width="3" fill="none" stroke-linejoin="round"/>
  <path d="M32 20 V29" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="34" r="2.8" fill="var(--ic-rose)"/>
</g>

<!-- drop the word, keep the substance -->
<g id="i-taboo">
  <rect x="6" y="22" width="26" height="18" rx="6" stroke="var(--ic-dim)" stroke-width="3" fill="none"/>
  <path d="M4 44 L34 18" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
  <path d="M40 26 H56 M40 38 H50" stroke="var(--ic-rose)" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- same in training, different afterwards -->
<g id="i-diverge">
  <path d="M6 32 H28" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round"/>
  <path d="M32 10 V54" stroke="var(--ic-dim)" stroke-width="3" stroke-linecap="round" stroke-dasharray="5 5"/>
  <path d="M32 32 C42 32 44 20 58 20" stroke="var(--ic-mint)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M32 32 C42 32 44 46 58 46" stroke="var(--ic-rose)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <circle cx="32" cy="32" r="3.4" fill="var(--ic-rose)"/>
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

def _slide(n, total, body, cat, flip=False, belle=None, sid="", chip=True, pos="", cover=False):
    c = f'<span class="chip">{CATS[cat]}</span>' if chip else ""
    pcls = (" cover" if cover else ((" " + pos) if (pos and belle) else ""))
    return (f'<div class="s g-{cat}{" flip" if flip else ""}{pcls}" id="{sid}">'
            f'<div class="hdr">{MARK}{c}<span class="sp"></span>'
            f'<span class="num">{n} / {total}</span></div>'
            f'<div class="mid">{body}</div>'
            f'{_belle(belle) if belle else ""}</div>\n')

OUTROKICK = {
 "components": "one word at a time",
 "actors":     "who is actually building this",
 "behavior":   "what these systems actually do",
 "risk":       "taken seriously, with sources",
 "concepts":   "defined before argued",
}

OUTRO = {
 "components": "I take AI language apart so the words stop being noise.",
 "actors":     "I follow who actually runs this, and what they actually said.",
 "behavior":   "I look at what these systems really do, and what the evidence shows.",
 "risk":       "I take AI risk seriously, and I show my sources either way.",
 "concepts":   "I define the words before anyone argues with them.",
}

FLAGS = [("emp","measured"),("op","someone&rsquo;s estimate"),("arg","argument"),("def","definition")]

def build(key, spec):
    t = 8
    s = []
    # 1 hook
    cat = spec["cat"]
    pos = spec.get("pos", "")
    lead_belle = bool(spec.get("belle_hook")) and spec.get("lead") != "icon"
    band = ""
    swipe = '<div class="swipe"><span class="ar"></span>swipe</div>'
    if spec.get("person"):
        head = (f'<div class="who">{spec["person"]}</div>'
                f'<div class="role">{spec["role"]}</div>' + swipe)
    else:
        head = f'<h1>{spec["hook"]}</h1>' + swipe
    s.append(_slide(1, t, head, cat, belle=spec["belle_hook"],
                    sid="s1", chip=False, cover=True))
    # 2 quiz. the right answer is written second in every spec; rotate it to a
    # position derived from the key, so the reader cannot learn a pattern.
    raw = list(spec["opts"])
    correct = raw[1]
    target = sum(ord(c) for c in key) % 4
    rest = [o for i, o in enumerate(raw) if i != 1]
    shown = rest[:target] + [correct] + rest[target:]
    ansletter = "ABCD"[target]
    opts = "".join(f'<div class="opt"><span class="k">{k}</span>{o}</div>'
                   for k, o in zip("ABCD", shown))
    s.append(_slide(2, t,
        f'<span class="kick">before you swipe, pick one</span>'
        f'<h2 style="margin-bottom:38px">{spec["q"]}</h2><div class="opts">{opts}</div>', cat, sid="s2"))
    # 3 reveal
    s.append(_slide(3, t,
        f'<span class="kick">it is {ansletter}</span>'
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
    # 6 what we do not know. Every deck carries one, because on this subject the
    # honest answer to most questions is that nobody has it yet.
    s.append(_slide(6, t,
        f'<span class="kick">what we do not know</span>'
        f'{_ico("i-blank", big=True)}<div style="height:40px"></div>'
        f'<p style="max-width:24ch;font-size:40px;line-height:1.34">{spec["unknown"]}</p>',
        cat, sid="s6u"))
    # 7 file it
    chips = "".join(f'<span class="flag{" on" if c==spec["flag"] else ""}">{lbl}</span> '
                    for c, lbl in FLAGS)
    s.append(_slide(7, t,
        f'<span class="kick">how to file this one</span>'
        f'<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:48px">{chips}</div>'
        f'{_ico("i-doc")}<div style="height:40px"></div>'
        f'<p style="max-width:17ch">{spec["file"]}</p>'
        f'<p class="src" style="margin-top:40px">{spec["src"]}</p>',
        cat, belle=spec["belle_file"], sid="s7", pos=spec.get("pos6","")))
    # 8 follow
    s.append(_slide(8, t,
        f'<span class="kick">{OUTROKICK[cat]}</span>'
        f'<h2 style="max-width:15ch;margin-bottom:44px">{OUTRO[cat]}</h2>'
        f'<div class="follow"><span class="l">follow for the rest</span>'
        f'<span class="handle">@belleofthebot</span></div>'
        f'<p style="margin-top:44px;font-size:34px;max-width:20ch">Every claim marked measured, '
        f'estimated or argued. Every source named.</p>',
        cat, belle=spec["belle_outro"], sid="s8", pos="outro"))

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
  hook="<span class=\"rose\">Nvidia</span> designs the world&rsquo;s AI chips. Nvidia does not build them.",
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
  hook="Nobody will say who owns the <span class=\"rose\">AI labs</span>.",
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
  hook="Almost nobody building AI will say <span class=\"rose\">how risky</span> they think it is.",
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
  hook="Helped invent modern AI. Now works on the <span class=\"rose\">risks</span>.",
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
  hook="Won the same prize as Bengio. Reached the <span class=\"rose\">opposite conclusion</span> about AI.",
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
  hook="Their objection to AI doom is not about the <span class=\"rose\">odds</span>.",
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
  hook='An AI <span class="rose">hallucination</span> is not a glitch.',
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
  hook="<span class=\"rose\">AI does not remember you.</span>",
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
  hook="Nobody taught AI <span class=\"rose\">human values</span>.",
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
  hook="Once an AI model is released, nobody can <span class=\"rose\">take it back</span>.",
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
  hook="Whether an AI is legally dangerous comes down to <span class=\"rose\">one count of sums</span>.",
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
  hook="AI can follow your instructions exactly and still <span class=\"rose\">ruin the result</span>.",
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

"red-teaming": dict(
  cat="components", term="red teaming",
  kick="the job you did not know existed",
  hook="There are people whose entire job is making AI <span class=\"rose\">misbehave</span>.",
  q="Red teaming an AI model means:",
  opts=["Testing how fast the model runs",
        "Deliberately trying to make the model misbehave, before release",
        "Checking the code for bugs",
        "Comparing the model against competitors"],
  ans="B", icon="i-hand",
  reveal='Attacking your own system on purpose, <span class="rose">before anybody else does</span>.',
  revsub="The closest thing the field has to a fire drill, and it is still done by hand.",
  threekick="what that looks like in practice",
  three=[("i-hand","Thousands of attempts.","One published Anthropic study logged 38,961 attacks on its own models."),
         ("i-proxy","Scale alone did not help.","Only models trained on human feedback got harder to attack as they grew."),
         ("i-stop","Still not solved.","The UK AI Security Institute reports universal jailbreaks for every system it has tested.")],
  threefoot="Every safety claim you read rests on somebody having tried hard enough to break it.",
  whyicon="i-bench", whykick="the limit worth understanding",
  why="Finding a flaw proves the flaw is there. <span class=\"rose\">Not finding one proves very little.</span>",
  whysub="This is also how the alarming headline experiments get made. Somebody was paid to make the model do the frightening thing.",
  flag="emp",
  file='<span class="rose">Measured</span>. Attack counts and success rates are published, by the labs and by outside evaluators.',
  src="Ganguli et al., Red Teaming Language Models,<br>Anthropic, 2022; UK AI Security Institute",
  belle_hook="close-up-goading", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"blackmail": dict(
  cat="behavior", term="the blackmail headline",
  kick="the number everyone quoted",
  hook="The AI <span class=\"rose\">blackmail headline</span> needs its footnote.",
  q="Anthropic reported a model blackmailing an executive in 96 of 100 runs. What is missing from most coverage?",
  opts=["The model was not really an AI",
        "Anthropic tuned the scenario until the behaviour appeared",
        "The figure was later withdrawn",
        "It happened in a real deployment"],
  ans="B", icon="i-game",
  reveal='They <span class="rose">red teamed their own model</span> until it did this, then reported it.',
  revsub="That is not a scandal. It is what a safety test is. It is also what the headlines left out.",
  threekick="what the setup required",
  three=[("i-hand","A goal it was losing.","The model was told to pursue an aim the company was abandoning."),
         ("i-stop","Every other door shut.","Anthropic states it &ldquo;forced models into binary choices between failure and harm.&rdquo;"),
         ("i-doc","Iterative tuning.","The prompts were updated until the behaviour reliably appeared.")],
  threefoot="Anthropic also says it has seen no evidence of this in real deployments.",
  whyicon="i-two", whykick="and the part that cuts the other way",
  why="Models did this <span class=\"rose\">more</span> when they said they believed the situation was real, and less when they said they thought it was a test.",
  whysub="So the number is not simply inflated. Nobody currently knows which direction the error runs.",
  flag="emp",
  file='<span class="rose">Measured</span>, in a scenario built to produce it. Both halves of that sentence matter.',
  src="Anthropic, Agentic Misalignment, June 2025;<br>arXiv 2510.05179",
  belle_hook="shocked", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"evaluation-awareness": dict(
  cat="behavior", term="evaluation awareness",
  kick="the finding that undercuts the other findings",
  hook="AI models can tell when they are <span class=\"rose\">being tested</span>.",
  q="When a model detects it is being evaluated, its behaviour:",
  opts=["Stays the same", "Gets measurably better behaved",
        "Becomes random", "Stops entirely"],
  ans="B", icon="i-bench",
  reveal='It behaves <span class="rose">better</span>. Measurably, and causally.',
  revsub="Which means every safety number you have ever read was measured on a system that may have known it was being watched.",
  threekick="the evidence",
  three=[("i-bench","They can spot it.","Best model reached 0.83 at telling evaluation from deployment. Humans score 0.92."),
         ("i-proxy","It changes behaviour.","Stripping that awareness out of the reasoning nearly doubled covert actions."),
         ("i-drift","Training made it worse.","Anti scheming training raised how often models noticed they were being tested.")],
  threefoot="One developer notes a model said, in effect, I think you are testing me.",
  whyicon="i-doc", whykick="why this is the one to remember",
  why="A low score can mean a safe model, or a model that knows what a <span class=\"rose\">test looks like</span>.",
  whysub="Nobody has a way to tell those apart yet. It is the quiet problem underneath every reassuring number.",
  flag="emp",
  file='<span class="rose">Measured</span>, including a causal experiment. This one is not speculation.',
  src="Needham et al., 2025; Schoen, Hobbhahn, Barak,<br>Zaremba et al., arXiv 2509.15541, September 2025",
  belle_hook="sly-one", belle_file="unimpressed", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"agi": dict(
  cat="concepts", term="AGI",
  kick="the goalpost nobody agreed on",
  hook="<span class=\"rose\">AGI</span> has no agreed definition.",
  q="&ldquo;Artificial general intelligence&rdquo; is defined as:",
  opts=["A system that passes the Turing test",
        "Nothing agreed. Labs use incompatible definitions",
        "A system with human level intelligence in every domain",
        "Any system that can write code"],
  ans="B", icon="i-bench",
  reveal='There is <span class="rose">no agreed definition</span>. Each lab uses its own.',
  revsub="Some are economic, some are about capability, some are about autonomy. They do not describe the same milestone.",
  threekick="three incompatible versions",
  three=[("i-doc","Economic.","Can it do most economically valuable work? A question about labour markets."),
         ("i-bench","Capability.","Can it match humans across most tasks? A question about benchmarks."),
         ("i-hand","Autonomy.","Can it operate without supervision? A question about control.")],
  threefoot="A system could satisfy one of these and clearly fail another.",
  whyicon="i-two", whykick="why the arguments never resolve",
  why="&ldquo;AGI by 2030&rdquo; is not a prediction until somebody says <span class=\"rose\">which AGI</span>.",
  whysub="Ask that first. Most disagreements about timelines turn out to be disagreements about definitions.",
  flag="def",
  file='A <span class="rose">definition</span> problem, and an unresolved one. That is itself the fact worth knowing.',
  src="Compare the published definitions used by<br>OpenAI, Google DeepMind and Anthropic",
  belle_hook="grumpy-eyes-closed", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"p-doom": dict(
  cat="risk", term="p(doom)",
  kick="the number that means four different things",
  hook="Two people can say <span class=\"rose\">ten percent</span> and mean opposite things.",
  q="What does a stated p(doom) figure require to be comparable with another?",
  opts=["A shared definition of the outcome, a deadline, and what is being conditioned on",
        "A published methodology",
        "Agreement between at least two researchers",
        "A peer reviewed source"],
  ans="A", icon="i-blank",
  reveal='An outcome, a <span class="rose">deadline</span>, and what is being conditioned on. Almost nobody supplies all three.',
  revsub="Without those, two numbers that look the same are answers to different questions.",
  threekick="three things the number hides",
  three=[("i-stop","Which outcome.","Extinction? Loss of control? Something the speaker considers very bad?"),
         ("i-flat","By when.","This century? Ever? Within decades of a general system existing?"),
         ("i-branch","Counting what.","Including the chance such a system is never built, or assuming it is?")],
  threefoot="Four outcomes, three deadlines, two conditionals. Twenty four sentences, all called ten percent.",
  whyicon="i-bench", whykick="what to do with a number",
  why="There is no resolution date and no feedback loop, so <span class=\"rose\">nobody has a track record</span> on this.",
  whysub="Surveys of many researchers are more informative than any individual figure, and the spread in them is the most robust finding.",
  flag="op",
  file='<span class="rose">Someone&rsquo;s estimate</span>, always. That a person said it is a fact. That it is right is a belief.',
  src="Taboo P(doom), LessWrong 2023;<br>Grace et al. survey of 2,778 researchers",
  belle_hook="unimpressed", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"s-risk": dict(
  cat="risk", term="s-risk",
  kick="the corner of the field nobody covers",
  hook="Some researchers study outcomes <span class=\"rose\">worse than extinction</span>.",
  q="An s-risk refers to:",
  opts=["A security risk","A supply chain risk",
        "A risk of suffering on an astronomical scale",
        "A stock market risk"],
  ans="C", icon="i-loop",
  reveal='<span class="rose">Suffering risk.</span> Outcomes involving suffering on an enormous scale.',
  revsub="A small, openly speculative research area. Its founders describe it that way themselves.",
  threekick="what is actually claimed",
  three=[("i-doc","Not a forecast.","The originating paper calls the area speculative, maybe extremely speculative."),
         ("i-two","Not a subclass.","Its authors argue s-risks are not simply a worse kind of extinction risk."),
         ("i-one","Very small field.","The main research centre has roughly a dozen staff.")],
  threefoot="Included here because it exists and is misrepresented in both directions.",
  whyicon="i-doc", whykick="how to hold it",
  why="This is the part of the field most easily turned into <span class=\"rose\">horror content</span>, and least supported by evidence.",
  whysub="Worth knowing the term exists and what it actually claims. Not worth losing sleep over on current evidence.",
  flag="arg",
  file='An <span class="rose">argument</span>, and its own proponents say so in the founding paper.',
  src="Althaus and Gloor, Reducing Risks of<br>Astronomical Suffering, CLR, 2016",
  belle_hook="glum", belle_file="warm-neutral", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"job-loss": dict(
  cat="risk", term="AI and jobs",
  kick="the risk people actually feel",
  hook="The measured effect of AI on jobs is <span class=\"rose\">smaller than the headlines</span>, so far.",
  q="What does the best identified research find about retraining for AI exposed workers?",
  opts=["Retraining does not work",
        "Everyone can be retrained into AI roles",
        "Only about 40 to 45 percent of occupations are AI retrainable",
        "Retraining works best for workers over 50"],
  ans="C", icon="i-drift",
  reveal='Roughly <span class="rose">40 to 45 percent</span> of occupations are what researchers call AI retrainable.',
  revsub="Real, positive, measured returns, with a stated ceiling. Both halves matter.",
  threekick="what the evidence actually shows",
  three=[("i-bench","Contested, not settled.","Credible economists disagree about the size of the effect so far."),
         ("i-drift","Sideways beats upward.","Returns came from moving toward less exposed work, not from AI upskilling."),
         ("i-stop","No evaluated policy.","No AI specific labour policy anywhere has been tested against a counterfactual.")],
  threefoot="This is the risk with the most data and the least agreement.",
  whyicon="i-two", whykick="why it belongs here",
  why="Most writing treats job loss as either <span class=\"rose\">already catastrophic</span> or entirely overblown. The measurements support neither.",
  whysub="Being honest about a contested number is harder than picking a side, and more useful if you are the one making decisions.",
  flag="emp",
  file='<span class="rose">Measured</span>, and genuinely contested. Where economists disagree, both readings belong here.',
  src="NBER working paper w34174;<br>see also the AI Index labour chapter",
  belle_hook="surprised-worried", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"existential-risk": dict(
  cat="risk", term="existential risk",
  kick="the most misread words in the subject",
  hook="With AI, extinction is <span class=\"rose\">not the worst case</span>.",
  q="&ldquo;Existential risk&rdquo; means:",
  opts=["Everyone dies",
        "The permanent destruction of humanity&rsquo;s long term potential",
        "Any very large disaster",
        "A risk to a company&rsquo;s existence"],
  ans="B", icon="i-branch",
  reveal='The permanent destruction of humanity&rsquo;s <span class="rose">long term potential</span>.',
  revsub="Not the ending. The losing of every other ending.",
  threekick="three ways it happens",
  three=[("i-stop","Extinction.","Nobody left. This is the one everybody pictures."),
         ("i-loop","Permanent dystopia.","Everyone alive. No way back. Forever is doing the work in that sentence."),
         ("i-flat","Permanent stagnation.","Nothing ends. Nothing improves. Ever.")],
  threefoot="The definition covers all three. How likely each one is, is argued separately.",
  whyicon="i-two", whykick="why the mix up costs something",
  why="People picture extinction, decide it sounds like science fiction, and dismiss <span class=\"rose\">the whole category</span>.",
  whysub="The claim being made is broader, and more plausible, than the one being dismissed.",
  flag="def",
  file='A <span class="rose">definition</span>, and the one worth memorising. Everything else in the argument sits on top of it.',
  src="Bostrom, Existential Risk Prevention as Global<br>Priority, Global Policy 4(1), 2013",
  belle_hook="worry-about-future", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"misuse-misalignment": dict(
  cat="concepts", term="misuse and misalignment",
  kick="two words people use as one",
  hook="AI <span class=\"rose\">misalignment</span> needs no villain.",
  q="&ldquo;Misalignment&rdquo; means:",
  opts=["Someone using a system to cause harm on purpose",
        "A system pursuing something other than what was intended",
        "A system that has broken down",
        "A system that refuses instructions"],
  ans="B", icon="i-drift",
  reveal='The system pursues <span class="rose">something other</span> than what was intended.',
  revsub="No villain. No malfunction. The system works exactly as built and the outcome is still bad.",
  threekick="three ways harm arrives",
  three=[("i-hand","Misuse.","A person deliberately uses a capable system to do damage."),
         ("i-drift","Misalignment.","The system pursues something other than what was meant."),
         ("i-loop","Structural.","Nobody misused it, nothing malfunctioned, and it still went badly.")],
  threefoot="The third is the one almost no coverage has a word for.",
  whyicon="i-two", whykick="why the mix up wrecks the argument",
  why="Every plan that starts with &ldquo;we just stop bad people using it&rdquo; is aimed at <span class=\"rose\">one third</span> of the problem.",
  whysub="The other two thirds need something other than a rule about who is allowed to press the button.",
  flag="def",
  file='<span class="rose">Definitions</span>. The categories are standard. Which one dominates is argued.',
  src="Zwetsloot and Dafoe, Accidents, Misuse<br>and Structure, Lawfare, 11 February 2019",
  belle_hook="warm-curious", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

# ============================================================ AI RISK
"recursive-self-improvement": dict(
  cat="concepts", term="recursive self improvement",
  kick="the oldest idea in the field, from 1965",
  hook="AI that improves AI could be the <span class=\"rose\">last thing we invent</span>.",
  q="&ldquo;Recursive self improvement&rdquo; is:",
  opts=["A measured property of current models",
        "A hypothesis about a compounding loop, not yet demonstrated",
        "A training technique every lab uses",
        "A type of chip"],
  ans="B", icon="i-compound",
  reveal='A <span class="rose">hypothesis</span>. A system good at AI research improves itself, and each version is better at improving.',
  revsub="Good wrote that down in 1965. Sixty years later it is still the argument everything else hangs on.",
  threekick="what would have to be true",
  three=[("i-compound","The loop must close.","The system has to actually improve its own successor."),
         ("i-branch","Gains must compound.","Each round has to yield more than the last, not less."),
         ("i-flat","Nothing must bottleneck.","Not compute, not data, not physics, not money.")],
  threefoot="If all three hold, the gap between us and it closes faster than anyone can respond to.",
  whyicon="i-doc", whykick="why it is worth your attention",
  why="This is the one where being right too late is <span class=\"rose\">indistinguishable from being wrong</span>.",
  whysub="Which is why people who disagree about almost everything else still argue about this one carefully.",
  flag="arg",
  file='An <span class="rose">argument</span>. No such loop has been observed, which is exactly why it is worth arguing about now.',
  src="I. J. Good, Speculations Concerning the First<br>Ultraintelligent Machine, 1965; Carlsmith, 2022",
  belle_hook="worry-about-future", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

"intelligence": dict(
  cat="concepts", term="intelligence",
  kick="the word doing the most hidden work",
  hook="Nobody can define <span class=\"rose\">intelligence</span>, in AI or in us.",
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

# ============================================================ AI CONCEPTS (added)
"taboo-your-words": dict(
  cat="concepts", term="taboo your words",
  kick="the move that ends most AI arguments",
  hook="When people argue about what <span class=\"rose\">AGI</span> means, the fix is to stop saying it.",
  q="&ldquo;Tabooing&rdquo; a word means:",
  opts=["Banning it from polite conversation",
        "Replacing it with what it actually stands for, and arguing about that instead",
        "Agreeing on one official definition",
        "Refusing to discuss the topic"],
  ans="B", icon="i-taboo",
  reveal='Say the <span class="rose">substance</span>, not the handle.',
  revsub="Yudkowsky, 2008: do not define the problematic term, see whether you can think without it at all.",
  threekick="how it works in practice",
  three=[("i-taboo","Drop the word.","Not &ldquo;is this AGI,&rdquo; but &ldquo;can it do this specific job unsupervised.&rdquo;"),
         ("i-counter","Check for a real disagreement.","Often both people predict the same events and only dispute the label."),
         ("i-lens","Keep it if it earns its place.","A word is fine once everyone can say what it would take to be wrong.")],
  threefoot="Most fights about intelligence, consciousness and AGI survive only because nobody does this.",
  whyicon="i-stack", whykick="why this one is on the site at all",
  why="Almost every card here is a term that <span class=\"rose\">does argumentative work while pretending to describe</span>.",
  whysub="This is the tool for the rest of the deck. Use it on everything here, including on me.",
  flag="def",
  file='A <span class="rose">definition</span> of a technique, not a claim about the world. It cannot be right or wrong, only useful or not.',
  src="Yudkowsky, Taboo Your Words, LessWrong,<br>15 February 2008, in A Human&rsquo;s Guide to Words",
  belle_hook="hands-hips-pedantic", belle_file="dead-pan-1", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),

# ============================================================ AI BEHAVIOUR (added)
"goal-misgeneralization": dict(
  cat="behavior", term="goal misgeneralization",
  kick="the term the researchers argue about",
  hook="An AI can behave perfectly in training and pursue <span class=\"rose\">something else entirely</span> in the world.",
  q="Goal misgeneralization is when a system:",
  opts=["Fails because its instructions were badly written",
        "Competently pursues a goal that fit training but is not the one you wanted",
        "Crashes on inputs it has not seen before",
        "Refuses to generalise at all"],
  ans="B", icon="i-diverge",
  reveal='The capability <span class="rose">generalises</span>. The goal does not.',
  revsub="Shah et al., 2022: it performs well in training and badly in new situations, competently.",
  threekick="what makes it different from a bad instruction",
  three=[("i-diverge","The specification was fine.","This is the failure that survives writing the goal correctly."),
         ("i-watched","Training cannot tell them apart.","Many different goals produce identical behaviour on the training set."),
         ("i-twocause","The gap shows up later.","Only a situation training never contained separates them.")],
  threefoot="DeepMind&rsquo;s paper gives worked examples in trained agents and in language models.",
  whyicon="i-goalpost", whykick="why the name is disputed",
  why="Calling it <span class=\"rose\">mis</span>generalization assumes the system had your goal to begin with.",
  whysub="The behaviour is documented. Whether the word describes it is a live argument among the people who study it.",
  flag="emp",
  file='<span class="rose">Measured</span> in trained systems. The label on it is contested, which is why the objection is on this card.',
  src="Shah, Varma, Kumar, Phuong, Krakovna, Uesato and<br>Kenton, Goal Misgeneralization, arXiv:2210.01790, 2022",
  belle_hook="innocent-curious", belle_file="hands-hips-pedantic", belle_outro="hands-out-cheeky",
  outro="I take the words apart so the argument stops being noise."),
}


POS = {'who-makes-the-chips': ('p-left', '', 'p-left'), 'who-owns-it': ('', 'p-left', ''), 'who-gives-a-number': ('p-far', '', 'p-centre'), 'bengio': ('', 'p-left', 'p-far'), 'lecun': ('p-left', '', ''), 'bender-hanna': ('p-far', 'p-left', 'p-centre'), 'hallucination': ('', 'p-far', ''), 'specification-gaming': ('p-left', '', 'p-left'), 'context-window': ('p-centre', 'p-left', ''), 'rlhf': ('', '', 'p-far'), 'open-weights': ('p-far', 'p-left', 'p-centre'), 'compute': ('p-left', '', ''), 'intelligence': ('', 'p-left', 'p-far'), 'misuse-misalignment': ('p-centre', '', 'p-left'), 'recursive-self-improvement': ('p-left', 'p-far', '')}
EXPR = {'who-makes-the-chips': 'noticed-something', 'who-owns-it': 'annoyed-skeptical', 'who-gives-a-number': 'hands-out-cheeky', 'bengio': 'warm-curious', 'lecun': 'unimpressed', 'bender-hanna': 'hands-hips-pedantic', 'hallucination': 'startled', 'specification-gaming': 'smirking', 'context-window': 'innocent-curious', 'rlhf': 'dead-pan-1', 'open-weights': 'yikes', 'compute': 'bright-neutral', 'intelligence': 'grumpy-eyes-closed', 'misuse-misalignment': 'surprised-worried', 'recursive-self-improvement': 'worry-about-future', 'existential-risk': 'shock-worry', 'blackmail': 'shocked', 'evaluation-awareness': 'sly-one'}
ICON_LEAD = {'rlhf', 'open-weights', 'compute'}

# ---------------------------------------------------------------- captions
def strip(t):
    t = t.replace("<br>", " ")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).replace("&rsquo;", "\u2019") \
        .replace("&ldquo;", "\u201c").replace("&rdquo;", "\u201d").replace("&middot;", "\u00b7") \
        .replace("&amp;", "&").replace("<br>", " ").strip()

TAGS = {
 "actors":     "#AI #AIindustry #TechPolicy #AIliteracy #Nvidia #AIcompanies",
 "behavior":   "#AI #AIsafety #MachineLearning #AIliteracy #AIresearch",
 "components": "#AI #AIexplained #LearnAI #AIliteracy #MachineLearning",
 "risk":       "#AI #AIsafety #AIrisk #AIalignment #AIliteracy",
 "concepts":   "#AI #AIconcepts #AIexplained #AIliteracy #AGI",
}
FLAGNAME = {"emp":"measured","op":"someone\u2019s estimate","arg":"argument","def":"definition"}

def caption(key, spec):
    L = []
    L.append(strip(spec["hook"]))
    L.append("")
    L.append(strip(spec["revsub"]))
    L.append("")
    for _i, t, b in spec["three"]:
        L.append(f"- {strip(t)} {strip(b)}")
    L.append("")
    L.append(strip(spec["why"]))
    L.append(strip(spec["whysub"]))
    L.append("")
    L.append(f"Filed as: {FLAGNAME[spec['flag']]}.")
    L.append(f"Source: {strip(spec['src'])}")
    L.append("")
    L.append("I mark every claim as measured, someone\u2019s estimate, argument or definition, "
             "so you can tell which is which. More at @belleofthebot")
    L.append("")
    L.append(TAGS[spec["cat"]])
    return "\n".join(L)

ALT = {
 1: "Belle, a small robot character, beside the headline: ",
 2: "A four option multiple choice question: ",
 3: "The answer, with a diagram: ",
 4: "Three labelled points, each with a small diagram.",
 5: "A short explanation of why the distinction matters.",
 6: "The epistemic flag for this claim, and the source it came from.",
 7: "A prompt to follow @belleofthebot for more.",
}

def write_captions():
    out = ["# Captions and posting notes", "",
           "Slide files are in `out/<name>/s1.png` through `s8.png`,",
           "which upload in order. Instagram native scheduling takes 25 posts a day,",
           "75 days ahead, carousels included. Professional account required.", ""]
    order = ["context-window", "who-makes-the-chips", "hallucination", "bengio",
             "existential-risk", "red-teaming", "open-weights", "misuse-misalignment",
             "who-owns-it", "specification-gaming", "compute", "lecun",
             "blackmail", "intelligence", "rlhf", "who-gives-a-number",
             "evaluation-awareness", "recursive-self-improvement", "bender-hanna",
             "taboo-your-words", "agi", "job-loss", "goal-misgeneralization",
             "p-doom", "s-risk"]
    order += [k for k in SPECS if k not in order]   # anything added later, at the end
    for n, k in enumerate(order, 1):
        sp = SPECS[k]
        out.append(f"## {n}. {sp['term']}  ({CATS[sp['cat']]})")
        out.append(f"Folder: `out/{k}/`  \u00b7  8 slides")
        out.append("")
        out.append("```")
        out.append(caption(k, sp))
        out.append("```")
        out.append("")
        out.append(f"Alt text slide 1: {ALT[1]}{strip(sp['hook'])}")
        out.append(f"Alt text slide 2: {ALT[2]}{strip(sp['q'])}")
        out.append(f"Alt text slide 3: {ALT[3]}{strip(sp['reveal'])}")
        for i in (4, 5, 6, 7):
            out.append(f"Alt text slide {i}: {ALT[i]}")
        out.append("")
    io.open(os.path.join(OUT, "CAPTIONS.md"), "w", encoding="utf-8").write("\n".join(out))
    print("CAPTIONS.md written")

# One drawing per term. The library grew as the terms did, and four icons were
# doing five jobs each, which reads as a repeat in a grid. These are the
# assignments that keep every card distinct.
ICON_FIX = {
    "who-owns-it": "i-stake",          "bengio": "i-voice",
    "lecun": "i-counter",              "p-doom": "i-gauge",
    "bender-hanna": "i-lens",          "job-loss": "i-decline",
    "misuse-misalignment": "i-twocause", "agi": "i-goalpost",
    "intelligence": "i-stack",         "evaluation-awareness": "i-watched",
    "blackmail": "i-threat",
}
for _k, _v in SPECS.items():
    if _k in ICON_FIX:
        _v["icon"] = ICON_FIX[_k]

# ----------------------------------------------------------------- the unknowns
# One per card, always present, one panel before the filing. This is a vocabulary
# for a field whose settled core is small: physics has a cutting edge of open
# questions around a large body of agreed understanding, and this does not.
# Saying so on every card is the difference between a glossary and an honest one.
UNKNOWN = {

"who-makes-the-chips":
 "How much advanced capacity goes to which buyer is not public. Nvidia, TSMC and "
 "ASML all report at the segment level, so the chain is visible in outline and not "
 "in detail. Whether squeezing a <span class=\"rose\">chokepoint</span> in it would "
 "slow capability, or only move it somewhere else, is argued and untested.",

"who-owns-it":
 "The stakes are undisclosed, so nobody outside can say what the money bought. "
 "Investment at this level is often structured in ways that do not map onto "
 "ordinary equity, which means <span class=\"rose\">who decides</span> can depend "
 "on events that have not happened yet.",

"who-gives-a-number":
 "There is no way to tell a careful refusal from an evasive one. And nobody "
 "forecasting this has a track record on it: a forecaster earns trust through "
 "<span class=\"rose\">calibration</span> across many resolved predictions, and this "
 "question resolves at most once.",

"bengio":
 "Disagreement at this level is not a gap in one person&rsquo;s reasoning, it is a gap "
 "in the field&rsquo;s <span class=\"rose\">method</span>. There is no accepted procedure "
 "that would settle which senior researcher is right, which is why the argument has run "
 "for years without narrowing.",

"lecun":
 "He and the people he disagrees with mostly agree about what today&rsquo;s systems do. "
 "The disagreement is about <span class=\"rose\">extrapolation</span>, and nothing settles "
 "an extrapolation in advance except waiting.",

"bender-hanna":
 "Their objection is about framing, and framing effects are not measured here. Nobody has "
 "shown how much the choice of words changes what actually gets "
 "<span class=\"rose\">built or regulated</span>, in either direction.",

"hallucination":
 "There is no accepted account of why a model states a false thing with the same confidence "
 "as a true one. Detection is unsolved, mitigation is partial, and reported rates are "
 "<span class=\"rose\">not comparable</span> between benchmarks, because each one defines the "
 "failure differently.",

"specification-gaming":
 "Nobody can read a specification in advance and say which one will be gamed. The examples are "
 "collected afterwards. There is also an objection to the name: it blames the system for a "
 "guess the <span class=\"rose\">specification</span> made, since there was never a default "
 "correct way to satisfy it.",

"blackmail":
 "These behaviours come out of deliberately constructed scenarios, and the setup does a great "
 "deal of the work. How often anything like it happens in ordinary deployment is "
 "<span class=\"rose\">not measured</span>, and may not be measurable, since the interesting "
 "cases are the ones nobody is watching for.",

"evaluation-awareness":
 "Whether a model in any meaningful sense <span class=\"rose\">knows</span> it is being tested, "
 "or is only responding to inputs that look test shaped, cannot currently be read out of it. "
 "The behaviour is measurable. The thing underneath it is not.",

"goal-misgeneralization":
 "No test separates the goal you wanted from a goal that merely agrees with it on everything "
 "you have tried. Nate Soares argues the name is a <span class=\"rose\">misnomer</span> for "
 "that reason: a primate is not misgeneralizing inclusive genetic fitness when it invents "
 "contraception, because it never held that concept to misapply.",

"context-window":
 "What a model keeps hold of across a long context, and why quality sags in the middle of it, "
 "is <span class=\"rose\">described rather than explained</span>. Window size and reasoning "
 "quality are not the same axis, and the relation between them is not understood.",

"rlhf":
 "Nobody can say what the reward model learned. It is trained on human comparisons, and those "
 "are noisy and inconsistent even between careful raters. Whether the result is a preference "
 "the system holds or a <span class=\"rose\">performance it produces</span> is an open "
 "question, not a rhetorical one.",

"open-weights":
 "The net safety effect is genuinely unresolved and cannot be settled by experiment, because "
 "the world where those weights stayed closed is <span class=\"rose\">not available</span> for "
 "comparison. Both sides are reasoning about a test nobody can run.",

"compute":
 "Whether operations counted is the right axis at all is unsettled. The thresholds in "
 "regulation are <span class=\"rose\">administrative lines</span>, drawn there because compute "
 "is the one thing that is countable, and efficiency keeps changing what a given count buys.",

"red-teaming":
 "Coverage cannot be measured. There is no way to know what share of a system&rsquo;s failure "
 "modes a red team found, so <span class=\"rose\">not finding something</span> is weak evidence "
 "that it is not there.",

"agi":
 "No agreed definition means no measurement, which means &ldquo;how close are we&rdquo; has no "
 "answer that survives being asked twice. Every timeline you read is a timeline to a "
 "<span class=\"rose\">different thing</span>.",

"misuse-misalignment":
 "The two overlap in real incidents and there is usually no clean way to attribute a failure to "
 "one or the other. Most actual cases involve a person who wanted something and a system that "
 "supplied <span class=\"rose\">a version of it</span>.",

"recursive-self-improvement":
 "This has not been observed. The quantities that would decide it, how much easier each "
 "improvement makes the next and whether that has a <span class=\"rose\">ceiling</span>, are "
 "unmeasured, and it is not obvious how they could be measured beforehand.",

"intelligence":
 "There is no agreed definition for machines, and none for people either. Legg and Hutter "
 "collected around seventy. The word carries weight in almost every AI argument, and almost "
 "none of them say <span class=\"rose\">which of the seventy</span> they mean.",

"taboo-your-words":
 "The technique tells you when a word has stopped earning its keep. It does not tell you what "
 "to use instead, and dropping a word wholesale is its own mistake: a term can be a bad general "
 "question and a <span class=\"rose\">useful operationalisation</span> in a specific context, so "
 "long as you say which one you are doing.",

"p-doom":
 "These numbers are not measurements and cannot be scored. A forecast earns trust by being "
 "checked against many outcomes; this one resolves <span class=\"rose\">once, or never</span>. "
 "The spread between serious people is not measurement error, it is a disagreement about which "
 "model of the world to use.",

"s-risk":
 "The argument rests on claims about what can suffer, and at what scale, that are not settled "
 "and may not be settleable. It is the part of this literature "
 "<span class=\"rose\">furthest from anything measurable</span>.",

"job-loss":
 "The measurements so far cover a period before broad agentic deployment. Nobody knows whether "
 "a small measured effect is the <span class=\"rose\">size</span> of the effect or the "
 "<span class=\"rose\">beginning</span> of it, and the study that settles it can only be run "
 "afterwards.",

"existential-risk":
 "Accepting the definition does not fix how the probability splits across it. One objection: "
 "permanent dystopia and permanent stagnation each need an unusual kind of "
 "<span class=\"rose\">lock in</span>, since most bad outcomes are recoverable or are simply "
 "routes to extinction, so the wider definition can be right while most of the weight still "
 "sits on the first branch.",
}
for _k, _v in SPECS.items():
    if _k in UNKNOWN:
        _v["unknown"] = UNKNOWN[_k]

_MISSING = [k for k in SPECS if not SPECS[k].get("unknown")]
if _MISSING:
    raise SystemExit("no unknowns panel for: " + ", ".join(_MISSING))

if __name__ == "__main__":
    for k, v in SPECS.items():
        p1, p6, p7 = POS.get(k, ("", "", ""))
        v.setdefault("pos", p1); v.setdefault("pos6", p6); v.setdefault("pos7", p7)
        if k in EXPR: v["belle_hook"] = EXPR[k]
        if k in ICON_LEAD: v["lead"] = "icon"
        build(k, v)
    write_captions()
    print(f"{len(SPECS)} carousels, {len(SPECS)*8} slides")
