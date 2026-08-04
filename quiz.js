/* belleofthebot · quizzes
   One topic, three levels. Pass at 80 percent and you move up: level 2, level 3,
   then on to the next topic. Below 80 and you go back to the cards for that
   topic, filtered, so the next attempt is not a guess. */
(function () {
  'use strict';

  var root = document.querySelector('[data-quizgame]');
  if (!root || !window.QUIZDATA) return;

  var D = window.QUIZDATA;              // { topics:[{key,name,levels:{1:[],2:[],3:[]}}] }
  var PASS = 0.8;

  var pick = root.querySelector('.qpick');
  var play = root.querySelector('.qplay');
  var done = root.querySelector('.qdone');

  var topic = null, level = 1, qs = [], at = 0, score = 0, locked = false;

  function topicByKey(k) {
    for (var i = 0; i < D.topics.length; i++) if (D.topics[i].key === k) return D.topics[i];
    return null;
  }
  function nextTopic(k) {
    for (var i = 0; i < D.topics.length; i++) if (D.topics[i].key === k)
      return D.topics[(i + 1) % D.topics.length];
    return D.topics[0];
  }

  /* ---------- start ---------- */
  function start(tkey, lv) {
    topic = topicByKey(tkey);
    if (!topic) return;
    level = Math.min(3, Math.max(1, lv || 1));
    qs = (topic.levels[level] || []).slice();
    if (!qs.length) { level = 1; qs = topic.levels[1].slice(); }
    at = 0; score = 0;
    pick.hidden = true; done.hidden = true; play.hidden = false;
    play.className = 'qplay c-' + topic.key;
    play.querySelector('.qtopic').textContent = topic.name;
    play.querySelector('.qlevel').textContent = 'level ' + level;
    history.replaceState(null, '', '?topic=' + topic.key + '&level=' + level);
    draw();
  }

  function draw() {
    locked = false;
    var q = qs[at];
    play.querySelector('.qq').textContent = q.q;
    var box = play.querySelector('.qopts');
    box.innerHTML = '';
    q.a.forEach(function (txt, n) {
      var b = document.createElement('button');
      b.className = 'qopt'; b.type = 'button'; b.textContent = txt;
      b.addEventListener('click', function () { answer(n, q); });
      box.appendChild(b);
    });
    play.querySelector('.qfb').textContent = '';
    play.querySelector('[data-next]').disabled = true;
    play.querySelector('[data-next]').textContent =
      at === qs.length - 1 ? 'see result' : 'next';
    play.querySelector('[data-count]').textContent = (at + 1) + ' of ' + qs.length;
    play.querySelector('[data-score]').textContent = score + ' correct';
    var pct = Math.round((at / qs.length) * 100);
    play.querySelector('.qfill').style.width = pct + '%';
  }

  function answer(n, q) {
    if (locked) return;
    locked = true;
    if (n === q.correct) score++;
    var opts = play.querySelectorAll('.qopt');
    Array.prototype.forEach.call(opts, function (x, m) {
      if (m === q.correct) x.classList.add('right');
      else if (m === n) x.classList.add('wrong');
      x.disabled = true;
    });
    play.querySelector('.qfb').textContent = q.why;
    play.querySelector('[data-score]').textContent = score + ' correct';
    play.querySelector('[data-next]').disabled = false;
  }

  play.querySelector('[data-next]').addEventListener('click', function () {
    if (at < qs.length - 1) { at++; draw(); return; }
    finish();
  });

  /* ---------- result ---------- */
  function band(ratio) {
    if (ratio === 1)      return D.bands.perfect;
    if (ratio >= PASS)    return D.bands.pass;
    if (ratio >= 0.5)     return D.bands.mid;
    return D.bands.low;
  }

  function finish() {
    var ratio = score / qs.length;
    var b = band(ratio);
    var passed = ratio >= PASS;
    play.hidden = true; done.hidden = false;
    done.className = 'qdone c-' + topic.key;

    done.querySelector('.rscore').textContent = score + ' out of ' + qs.length;
    done.querySelector('.rline').textContent =
      b.line.replace('{topic}', topic.name).replace('{short}', topic.short || topic.name)
            .replace('{n}', score).replace('{t}', qs.length);
    var img = done.querySelector('.rbelle img');
    if (img) {
      img.src = (window.BELLEIMG && window.BELLEIMG[b.belle]) ||
                ('assets/belle/' + b.belle + '.webp');
      img.alt = '';
    }

    var nextBtn = done.querySelector('[data-onward]');
    var nt;
    if (passed && level < 3) {
      nextBtn.textContent = 'level ' + (level + 1);
      nextBtn.onclick = function () { start(topic.key, level + 1); };
      done.querySelector('.rwhat').textContent =
        'You passed. Level ' + (level + 1) + ' is waiting.';
    } else if (passed) {
      nt = nextTopic(topic.key);
      nextBtn.textContent = 'start ' + nt.name;
      nextBtn.onclick = function () { start(nt.key, 1); };
      done.querySelector('.rwhat').textContent =
        'That is all three levels of ' + topic.name + '. On to ' + nt.name + '.';
    } else {
      nextBtn.textContent = 'read the ' + topic.name + ' cards';
      nextBtn.onclick = function () { location.href = 'index.html?cat=' + topic.key; };
      done.querySelector('.rwhat').textContent =
        'Under eighty percent. Have a read, then come straight back.';
    }

    done.querySelector('[data-restart]').onclick = function () { start(topic.key, level); };
    done.querySelector('[data-pickagain]').onclick = function () {
      done.hidden = true; pick.hidden = false;
      history.replaceState(null, '', location.pathname);
    };

    /* share */
    var txt = 'I got ' + score + '/' + qs.length + ' on the ' + topic.name +
              ' quiz, level ' + level + ', at belleofthebot.com';
    var sb = done.querySelector('[data-share]');
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

  /* ---------- pick screen ---------- */
  Array.prototype.forEach.call(root.querySelectorAll('[data-start]'), function (b) {
    b.addEventListener('click', function () {
      start(b.dataset.start, +b.dataset.level || 1);
    });
  });

  (function fromUrl() {
    var p = new URLSearchParams(location.search);
    var t = p.get('topic');
    if (t && topicByKey(t)) start(t, +p.get('level') || 1);
  })();
})();
