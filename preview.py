# -*- coding: utf-8 -*-
"""Builds one self-contained HTML file that carries the whole site.

For previewing away from a checkout: every page becomes a section, the nav
switches between them instead of navigating, and css, js and images are
inlined so the file works with no server and no network except webfonts.
"""
import base64, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = [("index.html", "explore"), ("quizzes.html", "quizzes"),
         ("more.html", "more"), ("about.html", "about"), ("sources.html", "sources")]

def read(p):
    with io.open(os.path.join(HERE, p), encoding="utf-8") as f:
        return f.read()

PREVIEW_H = 420      # the art is 700px on the real site; a preview does not need it

def datauri(rel):
    """Inline an image, downscaled. Every byte here is base64 in one html file,
    and the whole point is a file small enough to send."""
    path = os.path.join(HERE, rel)
    if not os.path.exists(path):
        return None
    raw = open(path, "rb").read()
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw))
        if im.height > PREVIEW_H:
            w = round(im.width * PREVIEW_H / im.height)
            im = im.resize((w, PREVIEW_H), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=72, method=6)
            if buf.tell() < len(raw):
                raw = buf.getvalue()
    except Exception:
        pass
    return "data:image/webp;base64," + base64.b64encode(raw).decode("ascii")

# every image the pages and the quiz bands can ask for
imgs = set(re.findall(r'assets/belle/[A-Za-z0-9_\-]+\.webp', "".join(read(p) for p, _ in PAGES)))
imgs |= set("assets/belle/%s.webp" % n for n in
            ("delighted", "happy-proud", "warm-curious", "aw-shucks"))
URIS = {}
for rel in sorted(imgs):
    u = datauri(rel)
    if u:
        URIS[rel] = u

# the modal and the quiz build their image paths in javascript, so hand the
# whole expression set over as a map rather than trying to rewrite strings
BELLEDIR = os.path.join(HERE, "assets", "belle")
wanted = set(re.findall(r'"belle2?":\s*"([a-z0-9\-]+)"', "".join(read(p) for p, _ in PAGES)))
wanted |= set(re.findall(r'"belle":\s*"([a-z0-9\-]+)"', read("quizzes.html")))
wanted |= {"delighted", "happy-proud", "warm-curious", "aw-shucks"}   # quiz result bands
BYSLUG = {}
if os.path.isdir(BELLEDIR):
    for f in sorted(os.listdir(BELLEDIR)):
        if f.endswith(".webp") and f[:-5] in wanted:
            BYSLUG[f[:-5]] = datauri(os.path.join("assets", "belle", f))
print("inlined %d images, %d expressions" % (len(URIS), len(BYSLUG)))

def inline_imgs(s):
    for rel, uri in URIS.items():
        s = s.replace('"' + rel + '"', '"' + uri + '"')
    return s

sections, scripts = [], []
for name, label in PAGES:
    h = read(name)
    body = h[h.index("<main"):h.index("</main>") + 7]
    # page-local data blocks travel with the page
    for m in re.finditer(r'<script>(.*?)</script>', body, re.S):
        scripts.append(m.group(1))
    body = re.sub(r'<script>.*?</script>', '', body, flags=re.S)
    for m in re.finditer(r'<script>(.*?)</script>', h[h.index("</main>"):], re.S):
        scripts.append(m.group(1))
    sections.append('<div class="pv-page" data-page="%s"%s>%s</div>'
                    % (name, "" if name == "index.html" else " hidden", body))

# the modal travels inside the explore section already, so nothing extra here
modal = ""

nav = "".join('<button class="link" type="button" data-pv="%s"%s>%s</button>'
              % (n, ' aria-current="page"' if n == "index.html" else "", l)
              for n, l in PAGES)

css = read("belle.css")
js = read("explore.js") + "\n" + read("quiz.js")
js = js.replace("location.href = 'index.html?cat=' + topic.key;",
                "window.__go('index.html', 'cat=' + topic.key);")

# the preset reader becomes a global so the router can drive the filters
PRESET_OLD = """  (function preset() {
    var p = new URLSearchParams(location.search);"""
PRESET_NEW = """  window.__filter = function (qs) {
    picked = { cat: null, flag: null };
    Array.prototype.forEach.call(pills, function (o) { o.classList.remove('on'); });
    var p = new URLSearchParams(qs || location.search);"""
assert PRESET_OLD in js
js = js.replace(PRESET_OLD, PRESET_NEW).replace("""    apply();
  })();""", """    apply();
  };
  window.__filter();""", 1)

doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>belleofthebot_ &middot; preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;700&display=swap">
<style>
%(css)s
.pv-page[hidden]{display:none}
.nav-in button.link{background:none;border:0;font:inherit;cursor:pointer}
.pv-note{font-family:var(--mono);font-size:.72rem;color:var(--faint);
  text-align:center;padding:.55rem 1rem;border-bottom:1px solid var(--edge)}
</style>
</head>
<body>
<div class="pv-note">preview build &middot; one file, no server &middot; the real site is five pages</div>
<header class="nav"><div class="nav-in">
<a class="mark" href="#" data-pv="index.html">belleof<span class="sg">thebot</span><span class="cur">_</span></a>
<span class="nav-sp"></span>
%(nav)s
</div></header>
%(sections)s
%(modal)s
<footer><div class="wrap">
<span>every claim marked &middot; every source named</span>
<span>built by elizabeth beier &middot; <a href="https://instagram.com/belleofthebot">@belleofthebot</a></span>
</div></footer>
<script>
/* history is not writable from a file or a sandboxed frame, so make it a no-op
   rather than let the pages throw on their first filter click */
(function () {
  var rs = history.replaceState.bind(history);
  history.replaceState = function () { try { rs.apply(history, arguments); } catch (e) {} };
})();
</script>
<script>window.BELLEIMG=%(belle)s;</script>
<script>%(data)s</script>
<script>
window.__go = function (page, q) {
  Array.prototype.forEach.call(document.querySelectorAll('.pv-page'), function (s) {
    s.hidden = s.dataset.page !== page;
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-pv]'), function (b) {
    if (b.dataset.pv === page) b.setAttribute('aria-current', 'page');
    else b.removeAttribute('aria-current');
  });
  window.scrollTo(0, 0);
  if (q && window.__filter) window.__filter(q);
};
document.addEventListener('click', function (e) {
  var b = e.target.closest('[data-pv]');
  if (b) { e.preventDefault(); window.__go(b.dataset.pv); }
  var a = e.target.closest('a[href]');
  if (!a || b) return;
  var h = a.getAttribute('href');
  if (!h || h.charAt(0) === '#' || h.indexOf('http') === 0) return;
  var page = h.split('?')[0], q = h.split('?')[1] || '';
  if (document.querySelector('.pv-page[data-page="' + page + '"]')) {
    e.preventDefault();
    window.__go(page, q);
  }
});
</script>
<script>%(js)s</script>
</body></html>
""" % {"css": css, "nav": nav, "sections": "\n".join(sections),
       "modal": modal, "data": "\n".join(scripts), "js": js,
       "belle": json.dumps(BYSLUG)}

doc = inline_imgs(doc)
name = os.environ.get("PREVIEW", "preview.html")
with io.open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
    f.write(doc)
print(name, len(doc))
