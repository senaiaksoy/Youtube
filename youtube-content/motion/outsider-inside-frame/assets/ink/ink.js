/* Outsider Inside — black-ink diagram lines: boxes, connectors, arrows, hatched bars (rough.js 4.6.6, MIT).
   INK ONLY (#1B2230): the red pen stays Dr. Aksoy's real strokes (assets/pen) — never draw red with this.
   Deterministic: every shape gets a seed derived from <html data-ink-seed> (written by tools/pen.mjs from the
   video's seed) + its call order, so a re-render is identical and the next video's lines differ.
   Seek-safe: shapes are built once at load; the draw-on is a GSAP tween of stroke-dashoffset on the paused timeline.

   const ink = oiInk.layer('#root');               // one full-frame <svg> in the scene's own px (W×H of the aspect)
   const b = ink.box(x, y, w, h);                  // wobbly rectangle (2 strokes, like a felt pen going round twice)
   const r = ink.boxAround('#node1', 18);          // box around an element (its CSS box + padding)
   const a = ink.arrow([[x1,y1],[x2,y2]], {bend: 30}); // curved connector + 2-stroke arrowhead
   const h = ink.hatch(x, y, w, h);                // outlined bar filled with hachure (bar charts)
   const e = ink.ellipse(cx, cy, w, h);            // wobbly circle / ellipse (e.g. around the end-screen subscribe slot)
   ink.draw(tl, b, 1.2, 0.6);                      // draws the shape's paths one after another from t=1.2 over 0.6 s
*/
(function () {
  const INK = '#1B2230';
  const root = document.documentElement;
  const seed0 = Number(root.dataset.inkSeed || 1);
  let calls = 0;
  const base = (o = {}) => Object.assign({ seed: (seed0 * 131 + (++calls) * 17) % 2147483646 + 1, roughness: 1.15, bowing: 1.1,
    stroke: INK, strokeWidth: 3.4, fill: undefined }, o);
  const box = (el, rootEl) => { let x = 0, y = 0, n = el; while (n && n !== rootEl) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; }
    return { x, y, w: el.offsetWidth, h: el.offsetHeight }; };
  window.oiInk = {
    layer(rootSel) {
      const rootEl = document.querySelector(rootSel);
      const W = rootEl.offsetWidth, H = rootEl.offsetHeight;
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'ink-layer'); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      svg.setAttribute('width', W); svg.setAttribute('height', H);
      svg.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;mix-blend-mode:multiply;overflow:visible';
      rootEl.appendChild(svg);
      const rc = rough.svg(svg);
      const add = (g) => { g.querySelectorAll('path').forEach((p) => { p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round'); });
        svg.appendChild(g); return g; };
      const api = {
        svg, W, H,
        box: (x, y, w, h, o) => add(rc.rectangle(x, y, w, h, base(o))),
        boxAround: (sel, pad = 16, o) => { const b = box(document.querySelector(sel), rootEl);
          return api.box(b.x - pad, b.y - pad, b.w + 2 * pad, b.h + 2 * pad, o); },
        rectOf: (sel) => box(document.querySelector(sel), rootEl),
        line: (x1, y1, x2, y2, o) => add(rc.line(x1, y1, x2, y2, base(o))),
        ellipse: (cx, cy, w, h, o) => add(rc.ellipse(cx, cy, w, h, base(o))),
        arrow: (pts, o = {}) => {
          const [p0, p1] = [pts[0], pts[pts.length - 1]];
          const bend = o.bend || 0; const mx = (p0[0] + p1[0]) / 2, my = (p0[1] + p1[1]) / 2;
          const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1;
          const mid = [mx - dy / L * bend, my + dx / L * bend];
          const g = add(pts.length > 2 || bend ? rc.curve(pts.length > 2 ? pts : [p0, mid, p1], base(o)) : rc.line(p0[0], p0[1], p1[0], p1[1], base(o)));
          const q = pts.length > 2 ? pts[pts.length - 2] : (bend ? mid : p0);
          const a = Math.atan2(p1[1] - q[1], p1[0] - q[0]), s = o.head || 26;
          const h1 = [p1[0] - s * Math.cos(a - 0.45), p1[1] - s * Math.sin(a - 0.45)], h2 = [p1[0] - s * Math.cos(a + 0.45), p1[1] - s * Math.sin(a + 0.45)];
          const head = rc.linearPath([h1, p1, h2], base(Object.assign({}, o, { roughness: 0.8 })));
          head.querySelectorAll('path').forEach((p) => g.appendChild(p));
          return g;
        },
        hatch: (x, y, w, h, o = {}) => add(rc.rectangle(x, y, w, h, base(Object.assign({ fill: INK, fillStyle: 'hachure', hachureGap: 13,
          hachureAngle: -41, fillWeight: 2.2 }, o)))),
        draw(tl, g, t, dur, ease = 'none') {
          const paths = [...g.querySelectorAll('path')];
          // rough.js puts the hachure fill first: draw the outline first, then the fill
          const sw = (p) => Number(p.getAttribute('stroke-width') || 0);
          paths.sort((a, b) => sw(b) - sw(a));   // outline (heavier) before hachure (lighter); stable otherwise
          const lens = paths.map((p) => p.getTotalLength() + 2); const tot = lens.reduce((a, b) => a + b, 0) || 1;
          let c = t;
          paths.forEach((p, i) => { p.style.strokeDasharray = `${lens[i]} ${lens[i]}`; const d = dur * lens[i] / tot;
            tl.fromTo(p, { strokeDashoffset: lens[i] }, { strokeDashoffset: 0, duration: d, ease }, c); c += d; });
          return c;
        },
      };
      return api;
    },
  };
})();
