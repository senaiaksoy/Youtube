window.WORLD = { enter: 'slam', small: 'rise', stamp: 'slam', strikeDur: 0.22, strikeEase: 'expo.out', barDur: 0.4, barEase: 'expo.out',
  bg(K) { if (K.deco) K.tl.fromTo(K.deco, { '--slide': '60%' }, { '--slide': '0%', duration: 0.5, ease: 'expo.out' }, 0); } };
