window.WORLD = { enter: 'blur', small: 'rise', stamp: 'blur',
  bg(K) {
    if (!K.bg) return;
    K.tl.fromTo(K.bg, { backgroundPosition: '0px 0px, 0px 0px, 0px 0px, 0px 0px' }, { backgroundPosition: '48px 24px, 48px 24px, 48px 24px, 48px 24px', duration: K.dur, ease: 'none' }, 0);
    K.tl.fromTo(K.deco, { '--scan': '-30%' }, { '--scan': '110%', duration: K.dur, ease: 'none' }, 0);
  } };
