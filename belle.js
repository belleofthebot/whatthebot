/* belleofthebot_ · shared interaction
   No dependencies. Every widget degrades to readable static content without JS. */

(function () {
  'use strict';

  /* ---------- 1. Severity x causation grid ---------- */
  var grid = document.querySelector('[data-grid]');
  if (grid) {
    var readout = grid.querySelector('.readout');
    var cells = grid.querySelectorAll('.cell');
    function showCell(btn) {
      cells.forEach(function (c) { c.classList.toggle('on', c === btn); });
      readout.innerHTML =
        '<h4>' + btn.dataset.title + '</h4>' +
        '<p>' + btn.dataset.body + '</p>' +
        '<span class="flag ' + btn.dataset.flagclass + '">' + btn.dataset.flag + '</span>' +
        (btn.dataset.src ? ' <span class="src meta">' + btn.dataset.src + '</span>' : '');
      readout.setAttribute('aria-live', 'polite');
    }
    cells.forEach(function (c) {
      c.addEventListener('click', function () { showCell(c); });
    });
  }

  /* ---------- 2. p(doom) definition builder ---------- */
  var builder = document.querySelector('[data-builder]');
  if (builder) {
    var pick = { outcome: null, when: null, cond: null };
    var out = builder.querySelector('.sentence');

    var TEXT = {
      outcome: {
        extinct: 'every human being is dead',
        control: 'humanity has permanently lost control of its own future, whether or not people are still alive',
        collapse: 'civilisation has collapsed but humanity survives and could recover',
        bad: 'something the speaker considers very bad has happened'
      },
      when: {
        y2100: 'by the year 2100',
        ever: 'at any point, with no deadline',
        after: 'within a few decades of the first genuinely general system being built'
      },
      cond: {
        uncond: 'counting the possibility that such a system is never built',
        cond: 'assuming such a system does get built'
      }
    };

    function render() {
      if (!pick.outcome || !pick.when || !pick.cond) {
        out.innerHTML = '<span class="meta">Pick one from each row.</span>';
        return;
      }
      out.innerHTML =
        'Your 10% means: there is a one in ten chance that <b>' + TEXT.outcome[pick.outcome] + '</b>, ' +
        '<b>' + TEXT.when[pick.when] + '</b>, ' + TEXT.cond[pick.cond] + '.';
    }

    builder.querySelectorAll('.opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var row = b.dataset.row;
        pick[row] = b.dataset.val;
        builder.querySelectorAll('.opt[data-row="' + row + '"]').forEach(function (o) {
          o.classList.toggle('on', o === b);
        });
        render();
      });
    });
    render();
  }

  /* ---------- 3. Stepped walkthrough ---------- */
  var walk = document.querySelector('[data-walk]');
  if (walk) {
    var steps = walk.querySelectorAll('.wstep');
    var panels = walk.querySelectorAll('[data-panel]');
    function go(i) {
      steps.forEach(function (s, n) { s.classList.toggle('on', n === i); s.setAttribute('aria-selected', n === i); });
      panels.forEach(function (p, n) { p.hidden = n !== i; });
    }
    steps.forEach(function (s, i) { s.addEventListener('click', function () { go(i); }); });
    go(0);
  }

  /* ---------- 4. Vocabulary quiz ---------- */
  var quiz = document.querySelector('[data-quiz]');
  if (quiz && window.QUIZ) {
    var i = 0, score = 0, locked = false;
    var qEl = quiz.querySelector('.qq');
    var oEl = quiz.querySelector('.qopts');
    var fEl = quiz.querySelector('.qfb');
    var bEl = quiz.querySelector('.qbar');
    var nEl = quiz.querySelector('[data-next]');

    function draw() {
      locked = false;
      var q = window.QUIZ[i];
      qEl.textContent = q.q;
      oEl.innerHTML = '';
      q.a.forEach(function (txt, n) {
        var b = document.createElement('button');
        b.className = 'qopt';
        b.type = 'button';
        b.textContent = txt;
        b.addEventListener('click', function () {
          if (locked) return;
          locked = true;
          var right = n === q.correct;
          if (right) score++;
          oEl.querySelectorAll('.qopt').forEach(function (x, m) {
            if (m === q.correct) x.classList.add('right');
            else if (m === n) x.classList.add('wrong');
          });
          fEl.textContent = q.why;
          bEl.querySelector('[data-score]').textContent = score + ' correct';
          nEl.disabled = false;
        });
        oEl.appendChild(b);
      });
      fEl.textContent = '';
      nEl.disabled = true;
      nEl.textContent = i === window.QUIZ.length - 1 ? 'see result' : 'next';
      bEl.querySelector('[data-count]').textContent = (i + 1) + ' of ' + window.QUIZ.length;
      bEl.querySelector('[data-score]').textContent = score + ' correct';
    }

    nEl.addEventListener('click', function () {
      if (i < window.QUIZ.length - 1) { i++; draw(); }
      else {
        qEl.textContent = 'You got ' + score + ' of ' + window.QUIZ.length + '.';
        oEl.innerHTML = '';
        fEl.textContent = score === window.QUIZ.length
          ? 'That is the whole vocabulary. The pieces will read faster now.'
          : 'The terms you missed are defined in the glossary below, with sources.';
        nEl.textContent = 'start again';
        nEl.disabled = false;
        nEl.onclick = function () { i = 0; score = 0; nEl.onclick = null; draw(); };
      }
    });
    draw();
  }
})();
