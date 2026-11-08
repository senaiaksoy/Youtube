window.WORLD = { enter: 'mask', small: 'rise', stamp: 'cut', barEase: 'power2.inOut',
  bg(K) { if (K.deco) K.tl.fromTo(K.deco, { '--rule': 0 }, { '--rule': 1, duration: 0.7, ease: 'power3.inOut' }, 0); } };
