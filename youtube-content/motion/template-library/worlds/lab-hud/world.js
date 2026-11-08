window.WORLD = { enter: 'type', small: 'type', stamp: 'cut', strikeEase: 'steps(10)', barEase: 'steps(12)',
  bg(K) { if (K.deco) K.tl.fromTo(K.deco, { '--scan': '0%' }, { '--scan': '100%', duration: Math.min(K.dur, 9), ease: 'none', repeat: Math.max(0, Math.floor(K.dur / 9) - 1) }, 0); } };
