window.WORLD = { enter: 'blur', small: 'blur', stamp: 'blur', barDur: 1.2, barEase: 'power2.out',
  deco(K) {
    if (!K.bg) return;
    for (let i = 0; i < 3; i++) K.bg.appendChild(document.createElement('i'));
    [...K.bg.children].forEach((el, i) => K.tl.fromTo(el, { x: 0, y: 0, scale: 1 }, { x: (i - 1) * 180 + 90, y: i % 2 ? -110 : 120, scale: 1.14, duration: K.dur, ease: 'sine.inOut' }, 0));
  } };
