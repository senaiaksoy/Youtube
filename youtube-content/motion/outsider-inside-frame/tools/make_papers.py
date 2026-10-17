#!/usr/bin/env python3
"""Outsider Inside — paper kits from Dr. Aksoy's photographed papers (2026-10-17).

Colours, rule pitch ratios, rule weights and dash/dot patterns were MEASURED from his photos
(prescription pad, ruled notebook, spiral lab notebook, squared notebook). Printed text, logo,
contact details, handwriting and show-through writing are never copied: rules are redrawn from the
measurements. The only photographic pixels reused are the spiral binding (no text on it).

  python3 make_papers.py <spiral-photo.png> <out-dir>

Writes <out-dir>/<paper>/ground-16x9.png, ground-9x16.png (+ spiral strips) and papers.json
(geometry so scenes can sit text on the rules).
"""
import json, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2  # supersampling

def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def canvas(W, H, ground):
    im = Image.new('RGBA', (W*SS, H*SS), hexrgb(ground) + (255,)); return im, ImageDraw.Draw(im)

def rgba(h, a): return hexrgb(h) + (int(round(a*255)),)

def hline(d, x0, x1, y, w, col, pattern=None, rng=None):
    """pattern=None solid; ('dash', on, off) ; ('dot', dot, period)"""
    y0 = int(round((y - w/2)*SS)); y1 = int(round((y + w/2)*SS)) - 1
    if pattern is None:
        d.rectangle([x0*SS, y0, x1*SS, y1], fill=col); return
    kind, on, per = pattern[0], pattern[1], pattern[1] + pattern[2] if pattern[0] == 'dash' else pattern[2]
    x = x0
    while x < x1:
        o = on * (1 + (rng.uniform(-0.12, 0.12) if rng is not None else 0))
        d.rectangle([int(x*SS), y0, int(min(x+o, x1)*SS), y1], fill=col)
        x += per

def vline(d, x, y0, y1, w, col):
    d.rectangle([int(round((x-w/2)*SS)), y0*SS, int(round((x+w/2)*SS))-1, y1*SS], fill=col)

def rect(d, x0, y0, x1, y1, w, col):
    hline(d, x0, x1, y0, w, col); hline(d, x0, x1, y1, w, col); vline(d, x0, y0, y1, w, col); vline(d, x1, y0, y1, w, col)

def finish(im, W, H): return im.resize((W, H), Image.LANCZOS)

# ---------- measured specs (photo → frame) ----------
# reçete (A5 pad): pitch 10.0 mm, dash 0.9 mm / gap 1.2 mm, blue-violet print; white stock.
# çizgili defter: pitch ≈4.5 % of page width, fine dotted grey (dot period ≈0.45 mm), header box; cream stock
#   (measured against the white prescription pad in the same photo: R×1.02 G×0.98 B×0.92).
# spiral lab defteri: pitch ≈3.2 % of page width, thin solid grey, inset ruled box + 2 header cells,
#   steel-blue edge band; stock ≈4 % warmer than the squared paper in the same photo.
# kareli: 5 mm squares, dark grey-brown rules.
SPEC = {
  'recete':    {'ground': '#F5F4F0', 'rule': '#6F6CA4', 'alpha': .72, 'w': 2, 'pitch': 96,
                'pattern': ('dash', 9, 11), 'label': 'Ordonnance (prescription pad)'},
  'cizgili':   {'ground': '#F3EBD6', 'rule': '#857C6B', 'alpha': .85, 'w': 2, 'pitch': 84,
                'pattern': ('dot', 2.4, 6), 'label': 'Ruled notebook (cream, dotted rules, header box)'},
  'lab-spiral':{'ground': '#EFEBE1', 'rule': '#B3AB9B', 'alpha': 1, 'w': 2, 'pitch': 72,
                'band': '#8EA8C3', 'label': 'Spiral lab notebook (ruled box, blue edge, real binding)'},
  'kareli':    {'ground': '#F2F1EC', 'rule': '#7B705C', 'alpha': .30, 'w': 2, 'cell': 54,
                'label': 'Squared paper (5 mm grid)'},
}

def make_recete(W, H):
    s = SPEC['recete']; im, d = canvas(W, H, s['ground']); rng = np.random.default_rng(7)
    m = round(W*0.078); top = 300 if W > H else 420
    ys = list(range(top, H - 100, s['pitch']))
    for y in ys: hline(d, m, W - m, y, s['w'], rgba(s['rule'], s['alpha']), s['pattern'], rng)
    return finish(im, W, H), {'rules_y': ys, 'x0': m, 'x1': W - m, 'pitch': s['pitch']}

def make_cizgili(W, H):
    s = SPEC['cizgili']; im, d = canvas(W, H, s['ground']); col = rgba(s['rule'], s['alpha'])
    m = round(W*0.0625); bx = (m, 60, W - m, 150) if W > H else (m, 120, W - m, 220)
    rect(d, *bx, 2, col); div = round(bx[0] + (bx[2]-bx[0])*(0.78 if W > H else 0.58))  # portrait: wider right cell for labels; vline(d, div, bx[1], bx[3], 2, col)
    ys = list(range(bx[3] + 60, H - 20, s['pitch']))
    for y in ys: hline(d, m, W - m, y, s['w'], col, s['pattern'])
    return finish(im, W, H), {'rules_y': ys, 'x0': m, 'x1': W - m, 'pitch': s['pitch'],
                              'header_box': list(bx), 'header_divider_x': div}

def spiral_strip(photo, H, scale=1.2):
    """Real binding: single rings cut from the photo, x-aligned, cross-faded and tiled in a fixed
    shuffled order (rings are industrial and identical; lighting varies a little ring to ring)."""
    a = np.asarray(Image.open(photo).convert('RGB')).astype(float)
    gains = np.array([247/204, 245/184, 240/161])            # photo's squared-paper strip -> frame paper white
    X0, X1, P, F = 1018, 1130, 41, 6                          # crop columns, ring period, fade rows
    ref = a[700:700+P, X0:X1].mean(2)
    tiles = []
    for y in (700, 741, 782, 864, 905, 946):                  # clean rings, no text, no shadow
        best = (0, 1e9)
        for dx in range(-6, 7):                               # align horizontally (photo is slightly skewed)
            for dy in range(-4, 5):
                t = a[y+dy:y+dy+P, X0+dx:X1+dx].mean(2); e = np.abs(t - ref).mean()
                if e < best[1]: best = ((dx, dy), e)
        (dx, dy), _ = best
        tiles.append(a[y+dy:y+dy+P+F, X0+dx:X1+dx] * gains)
    # brightness-match tiles to the first
    m0 = tiles[0].mean(); tiles = [np.clip(t * (m0 / t.mean()), 0, 255) for t in tiles]
    order = [0, 3, 1, 4, 2, 5, 1, 3, 0, 5, 2, 4]
    hsrc = int(np.ceil(H / scale)) + P
    out = np.zeros((hsrc + P + F, X1 - X0, 3)); y = 0; i = 0
    while y < hsrc:
        t = tiles[order[i % len(order)]]; i += 1
        if y == 0: out[0:P+F] = t
        else:
            w = np.linspace(0, 1, F)[:, None, None]
            out[y:y+F] = out[y:y+F]*(1-w) + t[:F]*w; out[y+F:y+P+F] = t[F:]
        y += P
    # match the strip's page margin (left columns) to the generated ground colour
    pg = out[:hsrc, 2:10].reshape(-1, 3).mean(0); tgt = np.array(hexrgb(SPEC['lab-spiral']['ground']), float)
    out = np.clip(out * (tgt / pg), 0, 255)
    img = Image.fromarray(out[:hsrc].astype('uint8'))
    img = img.resize((round(img.width*scale), round(img.height*scale)), Image.LANCZOS).crop((0, 0, round((X1-X0)*scale), H))
    al = np.full((H, img.width), 255, 'uint8'); f = 16
    for x in range(f): al[:, x] = int(255 * x / f)
    o = img.convert('RGBA'); o.putalpha(Image.fromarray(al)); return o

def make_spiral(W, H, photo):
    s = SPEC['lab-spiral']; im, d = canvas(W, H, s['ground']); col = rgba(s['rule'], s['alpha'])
    band = 56 if W > H else 44
    d.rectangle([0, 0, band*SS, H*SS], fill=rgba(s['band'], 1))
    strip = spiral_strip(photo, H); sx = W - strip.width + 8
    x0, x1 = band + 54, sx - 30
    hb = (x0, 52, x1, 132) if W > H else (x0, 110, x1, 200)
    rect(d, *hb, 2, col); hdiv = round(x0 + (x1-x0)*(0.2 if W > H else 0.16)); vline(d, hdiv, hb[1], hb[3], 2, col)
    box = (x0, hb[3] + 28, x1, H - 40); rect(d, *box, 2, col)
    ys = list(range(box[1] + s['pitch'], box[3] - 24, s['pitch']))
    for y in ys: hline(d, x0, x1, y, s['w'], col)
    out = finish(im, W, H); out.alpha_composite(strip, (sx, 0))
    return out, {'rules_y': ys, 'x0': x0, 'x1': x1, 'pitch': s['pitch'], 'header_box': list(hb),
                 'header_divider_x': hdiv, 'ruled_box': list(box), 'band_w': band, 'spiral_x': sx}

def make_kareli(W, H):
    s = SPEC['kareli']; im, d = canvas(W, H, s['ground']); col = rgba(s['rule'], s['alpha']); c = s['cell']
    nx = (W - 2*40)//c; ny = (H - 2*20)//c
    gx0 = (W - nx*c)//2; gy0 = (H - ny*c)//2
    for i in range(nx + 1): vline(d, gx0 + i*c, gy0, gy0 + ny*c, s['w'], col)
    for j in range(ny + 1): hline(d, gx0, gx0 + nx*c, gy0 + j*c, s['w'], col)
    return finish(im, W, H), {'grid_x0': gx0, 'grid_y0': gy0, 'cell': c, 'cols': nx, 'rows': ny}

def main():
    photo, out = sys.argv[1], sys.argv[2]; meta = {}
    for name, fn in [('recete', make_recete), ('cizgili', make_cizgili), ('lab-spiral', None), ('kareli', make_kareli)]:
        os.makedirs(os.path.join(out, name), exist_ok=True); meta[name] = {'label': SPEC[name]['label'],
            'ground': SPEC[name]['ground'], 'rule': SPEC[name]['rule']}
        for tag, (W, H) in {'16x9': (1920, 1080), '9x16': (1080, 1920)}.items():
            img, g = (make_spiral(W, H, photo) if name == 'lab-spiral' else fn(W, H))
            img.convert('RGB').save(os.path.join(out, name, f'ground-{tag}.png'), optimize=True)
            meta[name][tag] = g
    json.dump(meta, open(os.path.join(out, 'papers.json'), 'w'), indent=1)
    print('ok', list(meta))

if __name__ == '__main__': main()
