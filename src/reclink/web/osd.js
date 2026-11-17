/* The simulated OSD on the RecLink main page: a pretend camera (already recording) feeds the same %tokens the
   firmware uses. A chip picks the layout; the clock ticks once a second until the pause button stops it.
   Under reduced motion it shows the first frame and does not tick. */
(function () {
  var s = document.querySelector('.rl-osd__screen'); if (!s) return;
  var T = JSON.parse(s.getAttribute('data-sets'));
  var box = s.querySelector('.rl-osd__lines');
  var chips = document.querySelectorAll('.rl-chip');
  var pause = document.querySelector('.rl-osd .loop-pause');
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var layout = 0, sim = 40, tick = null, paused = false, anim = false, raf = 0, GL = '#%/+=*0123456789ABCDEF';
  function values(t) {
    var m = function (n) { return Math.floor(n / 60) + ':' + ('0' + (n % 60)).slice(-2); };
    var rem = Math.max(0, 5640 - t), rm = Math.ceil(rem / 60);
    var v = { st: 'REC', et: m(t), bt: (87 - Math.floor(t / 54)) + '%', rs: '5.3K', fp: '60', ln: 'WIDE', md: 'VIDEO', pr: 'HLG', bd: '10b', ar: '16:9' };
    v.rt = rm >= 100 ? Math.floor(rm / 60) + 'h' : rm + 'm'; v.sd = v.rt;
    v.sg = (38.4 - 0.1 * Math.floor(t / 7)).toFixed(1) + 'G';
    v.cr = String(-62 + Math.round(3 * Math.sin(t / 3) + 2 * Math.sin(t / 1.7)));
    return v;
  }
  function expand(tp, v) {
    return tp.replace(/%([a-z]{2})/g, function (x, k) { return k in v ? v[k] : x; }).replace(/\s+$/, '').slice(0, 16);
  }
  function paint() {
    if (anim) return;
    var v = values(sim), tp = T[layout], out = [];
    for (var k = 0; k < 4; k++) out.push(expand(tp[k] || '', v));
    box.textContent = out.join('\n');
  }
  function mark(n) {
    for (var d = 0; d < chips.length; d++) {
      chips[d].classList.toggle('is-on', d === n);
      chips[d].setAttribute('aria-pressed', d === n ? 'true' : 'false');
    }
  }
  // a layout change decodes every column from random glyphs into its character, line by line
  function go(n) {
    clearInterval(raf); mark(n);
    var v = values(sim), tp = T[n], tgt = [], rev = [], dur = 0, k, i;
    for (k = 0; k < 4; k++) {
      tgt.push(expand(tp[k] || '', v)); rev.push([]);
      for (i = 0; i < 16; i++) { rev[k][i] = k * 70 + i * 20 + Math.random() * 90; if (rev[k][i] > dur) dur = rev[k][i]; }
    }
    layout = n;
    if (reduce) { paint(); return; }
    dur += 80; anim = true;
    var t0 = Date.now();
    function frame() {
      var e = Date.now() - t0;
      if (e >= dur) { clearInterval(raf); anim = false; paint(); return; }
      var rowsOut = [];
      for (k = 0; k < 4; k++) {
        var out = '';
        for (i = 0; i < 16; i++) {
          if (e >= rev[k][i]) { var ch = tgt[k].charAt(i); out += (ch === ' ' || !ch) ? ' ' : ch; }
          else out += '<i>' + GL.charAt(Math.floor(Math.random() * GL.length)) + '</i>';
        }
        rowsOut.push(out);
      }
      box.innerHTML = rowsOut.join('\n');
    }
    frame(); raf = setInterval(frame, 40);
  }
  function start() { stop(); if (reduce || paused) return; tick = setInterval(function () { sim = (sim + 1) % 600; paint(); }, 1000); }
  function stop() { if (tick) { clearInterval(tick); tick = null; } }
  for (var d = 0; d < chips.length; d++) chips[d].addEventListener('click', function () { go(+this.getAttribute('data-i')); });
  if (pause) {
    if (reduce) pause.hidden = true;
    pause.addEventListener('click', function () {
      paused = !paused;
      pause.setAttribute('aria-pressed', paused ? 'true' : 'false');
      pause.setAttribute('aria-label', pause.getAttribute(paused ? 'data-play' : 'data-pause'));
      pause.querySelector('path').setAttribute('d', paused ? 'M4 2l8 5-8 5z' : 'M3 2h3v10H3zM8 2h3v10H8z');
      paused ? stop() : start();
    });
  }
  document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
  paint(); start();
})();
