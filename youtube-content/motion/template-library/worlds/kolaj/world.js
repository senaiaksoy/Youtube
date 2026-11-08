// Stepped time: every move lands on a low frame rate; the scraps boil on 2-frame holds driven by the seeded generator.
window.WORLD = { enter: 'step', small: 'step', stamp: 'step', strikeEase: 'steps(6)', strikeDur: 0.5, barEase: 'steps(7)', barDur: 0.7,
  deco(K) {
    if (!K.deco) return;
    const cs = getComputedStyle(document.documentElement); const cols = [cs.getPropertyValue('--accent'), cs.getPropertyValue('--accent2'), '#FBF7EE'];
    const shapes = ['polygon(0 12%,100% 0,92% 100%,6% 88%)', 'polygon(8% 0,100% 16%,84% 100%,0 80%)', 'polygon(0 0,86% 8%,100% 92%,14% 100%)'];
    for (let i = 0; i < 3; i++) {
      const el = document.createElement('i'); const w = 240 + K.rnd() * 300;
      el.style.cssText = `--c:${cols[i]};width:${w}px;height:${w * (0.5 + K.rnd() * 0.4)}px;right:${-60 + K.rnd() * 240}px;top:${i * 34 - 8 + K.rnd() * 12}%;clip-path:${shapes[i]};opacity:.9`;
      K.deco.appendChild(el);
      for (let t = 0; t < K.dur; t += 0.5) K.tl.set(el, { rotation: K.rnd() * 3 - 1.5 + i * 7, x: K.rnd() * 5 - 2.5, y: K.rnd() * 5 - 2.5 }, t);
    }
  } };
