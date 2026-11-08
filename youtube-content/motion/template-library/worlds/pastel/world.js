window.WORLD = { enter: 'pop', small: 'rise', stamp: 'pop', barEase: 'back.out(1.4)',
  bg(K) { if (K.bg) K.tl.fromTo(K.bg, { '--dy': '-26px' }, { '--dy': '26px', duration: K.dur, ease: 'sine.inOut' }, 0); } };
