/* belleofthebot · quizzes
   Five subjects, three levels each, plus a bonus round on the actors.

   The rules, in one place:
     · Pass is 80 percent.
     · A level is locked until the level below it has been passed.
     · A wrong answer always shows which one was right, and why.
     · Failing offers the same level again, immediately.
     · Passing level three offers the next subject.
     · Passing everything gets you Belle, extremely pleased.

   Progress is kept in localStorage where that works, and in memory where it
   does not, so the file still behaves when opened straight off a disk. */
(function () {
  'use strict';

  var root = document.querySelector('[data-quizgame]');
  if (!root || !window.QUIZDATA) return;

  var D = window.QUIZDATA;
  var PASS = 0.8;
  var KEY = 'botquiz.v1';

  /* ---------- progress ---------- */
  var mem = {};
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return mem; }
  }
  function save(p) {
    mem = p;
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
  }
  var done = load();                       // { "risk:2": true, ... }

  function passed(topicKey, level) { return !!done[topicKey + ':' + level]; }
  function unlocked(topicKey, level) {
    return level === 1 || passed(topicKey, level - 1);
  }
  function topicComplete(k) { return passed(k, 1) && passed(k, 2) && passed(k, 3); }
  function allComplete() {
    for (var i = 0; i < D.topics.length; i++)
      if (!topicComplete(D.topics[i].key)) return false;
    return true;
  }

  /* ---------- elements ---------- */
  var pick = root.querySelector('.qpick');
  var play = root.querySelector('.qplay');
  var over = root.querySelector('.qdone');
  var prize = root.querySelector('.qprize');

  var topic = null, level = 1, qs = [], at = 0, score = 0, locked = false, bonus = false;

  function topicByKey(k) {
    if (k === 'whosaid') return D.bonus;
    for (var i = 0; i < D.topics.length; i++) if (D.topics[i].key === k) return D.topics[i];
    return null;
  }
  function nextUnfinished(fromKey) {
    var n = D.topics.length, start = 0;
    for (var i = 0; i < n; i++) if (D.topics[i].key === fromKey) start = i + 1;
    for (var j = 0; j < n; j++) {
      var t = D.topics[(start + j) % n];
      if (!topicComplete(t.key)) return t;
    }
    return null;
  }

  /* ---------- the pick screen ---------- */
  function paintPick() {
    Array.prototype.forEach.call(pick.querySelectorAll('[data-start]'), function (b) {
      var k = b.dataset.start, lv = +b.dataset.level;
      var ok = unlocked(k, lv), won = passed(k, lv);
      b.disabled = !ok;
      b.classList.toggle('locked', !ok);
      b.classList.toggle('won', won);
      b.title = ok ? '' : 'Pass level ' + (lv - 1) + ' first';
      var mark = b.querySelector('.tick');
      if (mark) mark.hidden = !won;
    });
    var b = pick.querySelector('[data-bonus]');
    if (b) b.hidden = false;
    var note = pick.querySelector('[data-allnote]');
    if (note) note.hidden = !allComplete();
  }

  /* ---------- running a round ---------- */
  function start(tkey, lv) {
    topic = topicByKey(tkey);
    if (!topic) return;
    bonus = tkey === 'whosaid';
    level = bonus ? 0 : Math.min(3, Math.max(1, lv || 1));
    if (!bonus && !unlocked(tkey, level)) return;

    qs = (bonus ? topic.questions : topic.levels[level] || []).slice();
    if (!qs.length) return;
    at = 0; score = 0;

    pick.hidden = true; over.hidden = true; if (prize) prize.hidden = true;
    play.hidden = false;
    play.className = 'qplay c-' + (bonus ? 'actors' : topic.key);
    play.querySelector('.qtopic').textContent = topic.name;
    play.querySelector('.qlevel').textContent = bonus ? 'bonus round' : 'level ' + level;
    try {
      history.replaceState(null, '', bonus ? '?topic=whosaid'
                                           : '?topic=' + topic.key + '&level=' + level);
    } catch (e) {}
    draw();
  }

  function draw() {
    locked = false;
    var q = qs[at];
    play.querySelector('.qq').innerHTML = q.q;
    var box = play.querySelector('.qopts');
    box.innerHTML = '';
    q.a.forEach(function (txt, n) {
      var b = document.createElement('button');
      b.className = 'qopt'; b.type = 'button'; b.innerHTML = txt;
      b.addEventListener('click', function () { answer(n, q); });
      box.appendChild(b);
    });
    var fb = play.querySelector('.qfb');
    fb.innerHTML = ''; fb.hidden = true;
    var nx = play.querySelector('[data-next]');
    nx.disabled = true;
    nx.textContent = at === qs.length - 1 ? 'see result' : 'next';
    play.querySelector('[data-count]').textContent = (at + 1) + ' of ' + qs.length;
    play.querySelector('[data-score]').textContent = score + ' correct';
    play.querySelector('.qfill').style.width = Math.round((at / qs.length) * 100) + '%';
  }

  function answer(n, q) {
    if (locked) return;
    locked = true;
    var right = n === q.correct;
    if (right) score++;
    var opts = play.querySelectorAll('.qopt');
    Array.prototype.forEach.call(opts, function (x, m) {
      if (m === q.correct) x.classList.add('right');
      else if (m === n) x.classList.add('wrong');
      x.disabled = true;
    });
    /* a wrong answer always names the right one, not just the reasoning */
    var fb = play.querySelector('.qfb');
    fb.innerHTML = (right ? '<b class="fb-yes">Correct.</b> '
                          : '<b class="fb-no">Not quite.</b> The answer is <b>' +
                            q.a[q.correct] + '</b>. ') + q.why;
    fb.hidden = false;
    play.querySelector('[data-score]').textContent = score + ' correct';
    play.querySelector('[data-next]').disabled = false;
  }

  play.querySelector('[data-next]').addEventListener('click', function () {
    if (at < qs.length - 1) { at++; draw(); return; }
    finish();
  });

  /* ---------- the result ---------- */
  function band(ratio) {
    if (ratio === 1)   return D.bands.perfect;
    if (ratio >= PASS) return D.bands.pass;
    if (ratio >= 0.5)  return D.bands.mid;
    return D.bands.low;
  }

  function belleSrc(slug) {
    return (window.BELLEIMG && window.BELLEIMG[slug]) || ('assets/belle/' + slug + '.webp');
  }

  function showPrize() {
    if (!prize) return;
    play.hidden = true; over.hidden = true; prize.hidden = false;
    var p = D.prize;
    var img = prize.querySelector('img');
    if (img) {
      img.onerror = function () { this.onerror = null; this.src = belleSrc(p.fallback); };
      img.src = belleSrc(p.belle);
    }
    prize.querySelector('.pline').innerHTML = p.line;
    prize.querySelector('.psub').innerHTML = p.sub;
  }

  function finish() {
    var ratio = score / qs.length;
    var b = band(ratio);
    var won = ratio >= PASS;

    if (won && !bonus) {
      done[topic.key + ':' + level] = true;
      save(done);
    }

    play.hidden = true; over.hidden = false;
    over.className = 'qdone c-' + (bonus ? 'actors' : topic.key);
    over.querySelector('.rscore').textContent = score + ' out of ' + qs.length;
    over.querySelector('.rline').innerHTML =
      b.line.replace('{short}', topic.short || topic.name).replace('{topic}', topic.name);
    var img = over.querySelector('.rbelle img');
    if (img) { img.src = belleSrc(b.belle); img.alt = ''; }

    var onward = over.querySelector('[data-onward]');
    var again = over.querySelector('[data-restart]');
    var what = over.querySelector('.rwhat');
    again.textContent = won ? 'take it again' : 'try this level again';
    again.onclick = function () { start(bonus ? 'whosaid' : topic.key, level); };

    if (bonus) {
      onward.textContent = 'back to the quizzes';
      onward.onclick = toPick;
      what.textContent = won ? 'A bonus round, so nothing is unlocked. Purely for the pleasure of it.'
                             : 'No harm done. These are quotations, not principles.';
    } else if (won && level < 3) {
      onward.textContent = 'level ' + (level + 1) + ' is unlocked';
      onward.onclick = function () { start(topic.key, level + 1); };
      what.textContent = 'You passed. Level ' + (level + 1) + ' is open now.';
    } else if (won && allComplete()) {
      onward.textContent = 'claim your prize';
      onward.onclick = showPrize;
      what.textContent = 'That is every level of every subject. There is something waiting.';
    } else if (won) {
      var nt = nextUnfinished(topic.key);
      if (nt) {
        onward.textContent = 'start ' + nt.name;
        onward.onclick = function () { start(nt.key, 1); };
        what.textContent = 'That is all three levels of ' + topic.name + '. On to ' + nt.name + '.';
      } else {
        onward.textContent = 'back to the quizzes';
        onward.onclick = toPick;
        what.textContent = 'That is all three levels of ' + topic.name + '.';
      }
    } else {
      onward.textContent = 'read the ' + topic.name + ' cards';
      onward.onclick = function () {
        if (window.__go) window.__go('index.html', 'cat=' + topic.key);
        else location.href = 'index.html?cat=' + topic.key;
      };
      what.textContent = 'Under eighty percent, so this level stays where it is. ' +
                         'Have a read, or go straight round again.';
    }

    /* share */
    var txt = 'I got ' + score + '/' + qs.length + ' on the ' + topic.name +
              (bonus ? ' bonus round' : ' quiz, level ' + level) + ' at belleofthebot.com';
    var sb = over.querySelector('[data-share]');
    sb.onclick = function () {
      if (navigator.share) {
        navigator.share({ text: txt, url: location.href }).catch(function () {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(txt + ' ' + location.href).then(function () {
          sb.textContent = 'copied';
          setTimeout(function () { sb.textContent = 'share result'; }, 1800);
        });
      }
    };
  }

  function toPick() {
    over.hidden = true; play.hidden = true;
    if (prize) prize.hidden = true;
    pick.hidden = false;
    paintPick();
    try { history.replaceState(null, '', location.pathname); } catch (e) {}
  }

  over.querySelector('[data-pickagain]').onclick = toPick;
  if (prize) {
    var pb = prize.querySelector('[data-pickagain]');
    if (pb) pb.onclick = toPick;
  }

  /* ---------- wiring ---------- */
  Array.prototype.forEach.call(root.querySelectorAll('[data-start]'), function (b) {
    b.addEventListener('click', function () {
      start(b.dataset.start, +b.dataset.level || 1);
    });
  });
  var bonusBtn = root.querySelector('[data-bonus]');
  if (bonusBtn) bonusBtn.addEventListener('click', function () { start('whosaid', 0); });

  var reset = root.querySelector('[data-reset]');
  if (reset) reset.addEventListener('click', function () {
    done = {}; save(done); paintPick();
    reset.textContent = 'progress cleared';
    setTimeout(function () { reset.textContent = 'clear my progress'; }, 1800);
  });

  paintPick();

  (function fromUrl() {
    var p = new URLSearchParams(location.search);
    var t = p.get('topic');
    if (t && topicByKey(t)) start(t, +p.get('level') || 1);
  })();
})();
