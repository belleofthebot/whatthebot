"""The site navigation, defined once.

Both generators import this, so the header cannot drift between the card pages
and the long-form pages. base is prefixed at render time because the risk pages
sit one directory down.
"""

NAV = [("index.html", "explore"), ("quizzes.html", "quizzes"),
       ("more.html", "more"), ("about.html", "about")]

# The long pages live under "more". They are all listed on more.html anyway, but
# a hover menu saves a hop. It opens on hover for a pointer and on focus for a
# keyboard, and "more" itself stays a real link, so a touch device that never
# fires hover still lands on the page that lists the same things.
SUBNAV = [("frontier.html",      "who controls the frontier"),
          ("risk/pipeline.html", "how a model gets made"),
          ("risk/taxonomy.html", "where the worry comes in"),
          ("risk/words.html",    "the full glossary"),
          ("sources.html",       "all sources"),
          ("suggest.html",       "suggest a correction")]

def navlinks(current, base=""):
    out = []
    for h, t in NAV:
        cur = ' aria-current="page"' if h == current else ''
        if h != "more.html":
            out.append('<a class="link" href="%s%s"%s>%s</a>' % (base, h, cur, t))
            continue
        sub = "".join('<a href="%s%s">%s</a>' % (base, sh, st) for sh, st in SUBNAV)
        out.append(
            '<span class="navsub">'
            '<a class="link" href="%s%s"%s aria-haspopup="true">%s</a>'
            '<span class="submenu">%s</span></span>' % (base, h, cur, t, sub))
    return "".join(out)
