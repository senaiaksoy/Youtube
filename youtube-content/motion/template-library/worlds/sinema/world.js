window.WORLD = { enter: 'fade', small: 'fade', stamp: 'fade', strikeDur: 1.0, strikeEase: 'sine.inOut', barDur: 1.6, barEase: 'sine.inOut',
  deco(K) {
    if (!K.deco) return;
    const g = document.createElement('i'); K.deco.appendChild(g);
    for (let t = 0; t < K.dur; t += 1 / 12) K.tl.set(g, { x: Math.round(K.rnd() * 40 - 20), y: Math.round(K.rnd() * 40 - 20) }, t); // grain moves at 12 fps
    if (K.bg) K.tl.fromTo(K.bg, { '--lx': '-24%' }, { '--lx': '44%', duration: K.dur, ease: 'sine.inOut' }, 0);
  } };
