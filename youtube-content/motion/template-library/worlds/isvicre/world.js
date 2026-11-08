window.WORLD = { enter: 'cut', small: 'cut', stamp: 'cut', strikeDur: 0.18, strikeEase: 'none', barDur: 0.25, barEase: 'expo.out',
  bg(K) { if (K.deco) K.tl.fromTo(K.deco, { '--blk': '0%' }, { '--blk': '100%', duration: 0.3, ease: 'expo.out' }, 0); } };
