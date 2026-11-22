#!/usr/bin/env python3
"""Clean a head's white headband (fill notches/holes, smooth the edge, even white shading) and optionally shave
the head (hair on the scalp side of the band -> shaded skin).
fix_band_bald.py in.IMG out.IMG band_idx(e.g. 1-5) [--bald skin_idx_lo-hi hair_idx_lo-hi]"""
import sys, random
import numpy as np
from scipy import ndimage
sys.path.insert(0, __import__("os").path.dirname(__file__)); import imglib
def rng(s): a, b = map(int, s.split("-")); return list(range(a, b + 1))
src, dst, bandr = sys.argv[1:4]
BAND = rng(bandr); bald = "--bald" in sys.argv
if bald: SKIN = rng(sys.argv[sys.argv.index("--bald") + 1]); HAIRC = rng(sys.argv[sys.argv.index("--bald") + 2])
DIR = {1: (0, -1), 2: (0, -1), 3: (0, -1), 4: (0, -1), 5: (0, -1), 6: (-1, -1), 7: (0, -1), 8: (1, -1), 9: (0, -1),
       10: (0, -1), 11: None, 12: (-1, -1), 13: (-1, 1), 14: (0, -1), 15: (0, -1), 16: (-1, 0)}
b, ii, pp = imglib.read_lib(src); pal = pp[0]["colors"]
lum = lambda c: 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]
whites = sorted(BAND, key=lambda i: -lum(pal[i]))[:4]          # 4 clean shades, brightest first
for a in sys.argv:
    if a.startswith("--dirs="):
        for part in a[7:].split(";"):
            f, v = part.split(":"); DIR[int(f)] = tuple(int(t) for t in v.split(","))
BACKV = {1, 2}
rnd = random.Random(3); new = {}
for k, im in enumerate(ii):
    w, h = im["w"], im["h"]; px = np.array(imglib.pixels(b, im)).reshape(h, w); op = px != 0
    band = np.isin(px, BAND)
    if band.sum() > 6:
        m = ndimage.binary_closing(band, structure=np.ones((3, 3)), iterations=1) | band
        m = ndimage.binary_fill_holes(m) & op
        # 3x3 majority smoothing of the edge
        s = ndimage.uniform_filter(m.astype(float), 3)
        m = ((s > 0.5) | (m & (s > 0.4))) & op
        lab, n = ndimage.label(m)
        if n > 1:
            sz = ndimage.sum(m, lab, range(1, n + 1)); m = np.isin(lab, [i + 1 for i, z in enumerate(sz) if z >= 0.2 * sz.max()])
        # shading: by the smoothed original brightness, the band's lower edge one shade darker
        L = np.array([[lum(pal[c]) if band[y, x] else np.nan for x, c in enumerate(row)] for y, row in enumerate(px)])
        Lf = np.where(np.isnan(L), 0, L); Wt = (~np.isnan(L)).astype(float)
        sm = ndimage.uniform_filter(Lf, 3) / np.maximum(ndimage.uniform_filter(Wt, 3), 1e-6)
        sm[np.isnan(sm) | (ndimage.uniform_filter(Wt, 3) == 0)] = 230
        shade = np.digitize(sm, [215, 232, 244])        # 0 darkest .. 3 brightest
        out_idx = np.array(whites[::-1])[shade]
        lower = m & ~np.roll(m, -1, 0)                   # bottom edge pixels of the band
        out_idx = np.where(lower, whites[3], out_idx)
        px = np.where(m, out_idx, px)
        band = m
    if bald:
        lab, n = ndimage.label(op & ~band)
        by, bx = np.nonzero(band); bc = np.array([bx.mean(), by.mean()]) if len(bx) else np.array([w / 2, h / 2])
        scalp = np.zeros_like(op); d = DIR[k + 1]
        for c in range(1, n + 1):
            mm = lab == c; cy, cx = np.nonzero(mm)
            if d is None or (np.array([cx.mean(), cy.mean()]) - bc) @ np.array(d, float) > 0: scalp |= mm
        # hair on the other side of the band too (back views): dark hair colours touching the band region
        hairc = np.isin(px, HAIRC) & op & ~band
        lab2, n2 = ndimage.label(hairc | scalp)
        touch = set(np.unique(lab2[ndimage.binary_dilation(band, iterations=1) & (hairc | scalp)])) - {0}
        if k + 1 in BACKV: scalp |= np.isin(lab2, list(touch)) & hairc
        else: scalp |= ndimage.binary_dilation(scalp, iterations=1) & hairc & op   # leftover hair specks at the scalp edge
        if k + 1 == 11: scalp = op.copy()
        if scalp.any():
            # dome shading from the skin colours of this palette
            face = op & ~band & ~scalp & np.isin(px, SKIN)
            fl = np.array([lum(pal[c]) for c in px[face]]) if face.any() else np.array([lum(pal[c]) for c in SKIN])
            lo, hi = np.percentile(fl, 20), np.percentile(fl, 92)
            dist = ndimage.distance_transform_edt(op)
            t = np.clip(dist / max(1, dist[scalp].max()), 0, 1) ** 0.6
            yy, xx = np.mgrid[:h, :w]
            cy, cx = np.nonzero(scalp); hx, hy = cx.mean() - 0.15 * w, cy.min() + 0.3 * (cy.max() - cy.min())
            spec = np.exp(-(((xx - hx) / (0.18 * w)) ** 2 + ((yy - hy) / (0.14 * h)) ** 2))
            target = lo + (hi - lo) * (0.75 * t + 0.35 * spec)
            sk = sorted(SKIN, key=lambda i: lum(pal[i])); sl = np.array([lum(pal[i]) for i in sk])
            for y, x in zip(*np.nonzero(scalp)):
                v = target[y, x] + rnd.uniform(-5, 5)
                px[y, x] = sk[int(np.abs(sl - v).argmin())]
    new[k] = (w, h, im["anix"], im["aniy"], [int(v) for v in px.reshape(-1)])
imglib.write_lib(dst, b, ii, pp, new)
