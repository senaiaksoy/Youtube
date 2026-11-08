// Template library: world-agnostic motion API. Every tween lives on one paused GSAP timeline, so scenes stay seekable and deterministic.
// A world (assets/world/world.js) sets window.WORLD = { enter, small, stamp, bg(K), deco(K) }.
(function () {
  function start() {
    const W = window.WORLD || {}; const html = document.documentElement; const root = document.getElementById('root');
    const dur = parseFloat(root.dataset.duration); const tl = gsap.timeline({ paused: true });
    let a = (parseInt(html.dataset.seed || '1', 10) >>> 0) || 1;
    const rnd = () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const M = {
      rise: (s, t) => tl.fromTo(s, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power3.out' }, t),
      fade: (s, t) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.9, ease: 'sine.inOut' }, t),
      cut: (s, t) => { tl.set(s, { opacity: 0 }, 0); tl.set(s, { opacity: 1 }, t); },
      mask: (s, t) => tl.fromTo(s, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 -10% 0)', duration: 0.6, ease: 'power3.inOut' }, t),
      wipe: (s, t) => tl.fromTo(s, { clipPath: 'inset(-10% 100% -10% 0)' }, { clipPath: 'inset(-10% -2% -10% 0)', duration: 0.55, ease: 'power2.inOut' }, t),
      slam: (s, t) => tl.fromTo(s, { opacity: 0, scale: 1.16 }, { opacity: 1, scale: 1, duration: 0.24, ease: 'expo.out' }, t),
      blur: (s, t) => tl.fromTo(s, { opacity: 0, filter: 'blur(18px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.7, ease: 'power2.out' }, t),
      pop: (s, t) => tl.fromTo(s, { opacity: 0, scale: 0.86 }, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2.2)' }, t),
      type: (s, t) => tl.fromTo(s, { clipPath: 'inset(-10% 100% -10% 0)' }, { clipPath: 'inset(-10% -2% -10% 0)', duration: 0.8, ease: 'steps(16)' }, t),
      step: (s, t) => tl.fromTo(s, { opacity: 0, y: 34, rotation: rnd() * 5 - 2.5 }, { opacity: 1, y: 0, rotation: rnd() * 1.6 - 0.8, duration: 0.42, ease: 'steps(5)' }, t),
    };
    const K = {
      tl, dur, W, root, rnd, port: html.dataset.aspect === '9x16', bg: root.querySelector('.bg'), deco: root.querySelector('.deco'),
      big: (s, t) => M[W.enter || 'rise'](s, t),
      in: (s, t) => M[W.small || 'rise'](s, t),
      strike: (s, t) => tl.fromTo(s, { '--strike': '0%' }, { '--strike': '100%', duration: W.strikeDur ?? 0.55, ease: W.strikeEase || 'power2.inOut' }, t),
      stamp: (s, t) => M[W.stamp || 'slam'](s, t),
      bar: (s, t, v) => tl.fromTo(s, { scaleX: 0 }, { scaleX: v / 100, duration: W.barDur ?? 0.9, ease: W.barEase || 'power3.out' }, t),
      pushIn: (s) => tl.fromTo(s, { scale: 1 }, { scale: 1.04, duration: dur, ease: 'none' }, 0),
      done() {
        if (W.deco) W.deco(K);
        if (W.bg) W.bg(K);
        tl.to({}, { duration: 0.01 }, dur - 0.01);
        return tl;
      },
    };
    return K;
  }
  window.Kit = { start };
})();
