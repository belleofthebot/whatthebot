/* belleofthebot · explore
   Pill filters over a card grid, and a modal that flips through a card the way
   the carousels do. No dependencies. Degrades to a plain readable grid if JS
   never runs, because every card's content is already in the DOM. */
(function () {
  'use strict';

  var root = document.querySelector('[data-explore]');
  if (!root || !window.CARDS) return;

  var grid   = root.querySelector('.egrid');
  var count  = root.querySelector('[data-count]');
  var pills  = root.querySelectorAll('.pill');
  var empty  = root.querySelector('.eempty');
  var picked = { cat: null, flag: null };

  /* ---------- filtering ---------- */
  function apply() {
    var shown = 0;
    Array.prototype.forEach.call(grid.children, function (el) {
      var okc = !picked.cat  || el.dataset.cat  === picked.cat;
      var okf = !picked.flag || el.dataset.flag === picked.flag;
      var ok = okc && okf;
      el.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown + (shown === 1 ? ' card' : ' cards');
    if (empty) empty.hidden = shown !== 0;
    var q = [];
    if (picked.cat)  q.push('cat=' + picked.cat);
    if (picked.flag) q.push('flag=' + picked.flag);
    history.replaceState(null, '', q.length ? '?' + q.join('&') : location.pathname);
  }

  Array.prototype.forEach.call(pills, function (p) {
    p.addEventListener('click', function () {
      var kind = p.dataset.kind, val = p.dataset.val;
      picked[kind] = (picked[kind] === val) ? null : val;
      Array.prototype.forEach.call(pills, function (o) {
        if (o.dataset.kind === kind) o.classList.toggle('on', o.dataset.val === picked[kind]);
      });
      apply();
    });
  });

  root.querySelector('[data-clear]').addEventListener('click', function () {
    picked = { cat: null, flag: null };
    Array.prototype.forEach.call(pills, function (o) { o.classList.remove('on'); });
    apply();
  });

  /* preselect from the url, so a quiz can send someone straight to a topic */
  (function preset() {
    var p = new URLSearchParams(location.search);
    ['cat', 'flag'].forEach(function (k) {
      var v = p.get(k);
      if (!v) return;
      picked[k] = v;
      Array.prototype.forEach.call(pills, function (o) {
        if (o.dataset.kind === k && o.dataset.val === v) o.classList.add('on');
      });
    });
    apply();
  })();

  /* ---------- the modal ---------- */
  var modal = document.querySelector('[data-modal]');
  var mBody = modal.querySelector('.mbody');
  var mDots = modal.querySelector('.mdots');
  var mCat  = modal.querySelector('.mcat');
  var order = [], at = 0, panel = 0, panels = [];

  function visibleKeys() {
    return Array.prototype.filter.call(grid.children, function (el) { return !el.hidden; })
      .map(function (el) { return el.dataset.key; });
  }

  var answered = {};                    // key -> chosen option, so a flip back remembers

  /* image source, indirected so the single file preview can inline the art */
  function belleSrc(s) {
    return (window.BELLEIMG && window.BELLEIMG[s]) || ('assets/belle/' + s + '.webp');
  }

  function belleTag(slug, cls) {
    return slug ? '<figure class="' + cls + '"><img src="' + belleSrc(slug) +
                  '" alt="" loading="lazy"></figure>' : '';
  }

  function build(card, key) {
    var pts = card.three.map(function (t) {
      return '<li><svg class="mpi" viewBox="0 0 64 64" aria-hidden="true"><use href="#' +
             t[0] + '"/></svg><div><b>' + t[1] + '</b> ' + t[2] + '</div></li>';
    }).join('');

    var opts = card.opts.map(function (o, i) {
      return '<button class="mopt" type="button" data-opt="' + i + '">' + o + '</button>';
    }).join('');

    var icon = '<svg class="mfig" viewBox="0 0 64 64" aria-hidden="true"><use href="#' +
               card.icon + '"/></svg>';

    var panels = [
      /* 1 · the cover, so Belle is the first thing you see */
      '<span class="mkick">' + card.kick + '</span><h2 class="mhook">' + card.hook + '</h2>' +
        belleTag(card.belle, 'mbelle'),

      /* 2 · the question, before the answer */
      '<span class="mkick">before you read on</span><h3 class="mq">' + card.q + '</h3>' +
        '<div class="mopts" data-quiz="' + key + '">' + opts + '</div>' +
        '<p class="mfb" hidden></p>',

      /* 3 · the plain answer */
      '<span class="mkick">the plain answer</span><h3 class="mans">' + card.reveal + '</h3>' +
        '<p>' + card.revsub + '</p>' + icon,

      /* 4 · three points, each with its own drawing */
      '<span class="mkick">' + card.threekick + '</span><ul class="mpts">' + pts + '</ul>' +
        '<p class="meta">' + card.threefoot + '</p>',

      /* 5 · why it matters */
      '<span class="mkick">' + card.whykick + '</span><p class="mwhy">' + card.why + '</p>' +
        '<p>' + card.whysub + '</p>',

      /* 6 · what nobody knows, which on this subject is most of it */
      '<span class="mkick">what we do not know</span>' +
        '<p class="mobj">' + card.unknown + '</p>' +
        '<svg class="mfig" viewBox="0 0 64 64" aria-hidden="true"><use href="#i-blank"/></svg>',

      /* 7 · how it is filed, the source, and Belle again on the way out */
      '<span class="mkick">how this claim is filed</span>' +
        '<p class="mfile">' + card.file + '</p>' +
        '<div class="mflag"><span class="flag f-' + card.flag + '">' + card.flagname + '</span></div>' +
        '<p class="src">' + card.src + '</p>' +
        belleTag(card.belle2 || card.belle, 'mbelle small')
    ];

    return panels;
  }

  /* the question panel is the only live one: bind it after every paint */
  function wireQuiz(card) {
    var box = mBody.querySelector('[data-quiz]');
    if (!box) return;
    var key = box.dataset.quiz;
    var fb = mBody.querySelector('.mfb');
    var btns = box.querySelectorAll('.mopt');

    function settle(n) {
      Array.prototype.forEach.call(btns, function (b, i) {
        b.classList.toggle('right', i === card.ans);
        b.classList.toggle('wrong', i === n && n !== card.ans);
        b.disabled = true;
      });
      fb.textContent = card.ansy;
      fb.hidden = false;
    }
    if (answered[key] !== undefined) { settle(answered[key]); return; }
    Array.prototype.forEach.call(btns, function (b, i) {
      b.addEventListener('click', function () { answered[key] = i; settle(i); });
    });
  }

  function paint() {
    mBody.innerHTML = panels[panel];
    mBody.scrollTop = 0;
    if (panel === 1) wireQuiz(current);
    mDots.innerHTML = panels.map(function (_, i) {
      return '<button class="mdot' + (i === panel ? ' on' : '') + '" data-go="' + i +
             '" aria-label="panel ' + (i + 1) + '"></button>';
    }).join('');
    Array.prototype.forEach.call(mDots.children, function (d) {
      d.addEventListener('click', function () { panel = +d.dataset.go; paint(); });
    });
    modal.querySelector('[data-prev]').disabled = panel === 0;
    var nx = modal.querySelector('[data-next]');
    nx.textContent = panel === panels.length - 1 ? 'next card' : 'next';
  }

  function open(key) {
    order = visibleKeys();
    at = order.indexOf(key);
    load(key);
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    modal.querySelector('[data-close]').focus();
  }

  var current = null;

  function load(key) {
    var card = window.CARDS[key];
    current = card;
    panels = build(card, key);
    panel = 0;
    mCat.textContent = card.catname;
    mCat.className = 'mcat';
    /* the card wears its subject's ground, the way the carousel does */
    modal.querySelector('.mcard').className = 'mcard tg-' + card.cat;
    modal.querySelector('.mterm').textContent = card.term;
    paint();
  }

  function close() {
    modal.hidden = true;
    document.body.style.overflow = '';
  }

  Array.prototype.forEach.call(grid.children, function (el) {
    el.addEventListener('click', function () { open(el.dataset.key); });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(el.dataset.key); }
    });
  });

  modal.querySelector('[data-close]').addEventListener('click', close);
  modal.querySelector('.mscrim').addEventListener('click', close);
  modal.querySelector('[data-prev]').addEventListener('click', function () {
    if (panel > 0) { panel--; paint(); }
  });
  modal.querySelector('[data-next]').addEventListener('click', function () {
    if (panel < panels.length - 1) { panel++; paint(); return; }
    at = (at + 1) % order.length;
    load(order[at]);
  });

  document.addEventListener('keydown', function (e) {
    if (modal.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') modal.querySelector('[data-next]').click();
    if (e.key === 'ArrowLeft' && panel > 0) { panel--; paint(); }
  });
})();
