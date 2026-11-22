#!/usr/bin/env python3
"""Uniform clean white headbands: smooth edges (curve fit on level bands, morphological on tilted ones),
one bright fill, light top edge, soft shadow line at the bottom, stray whites -> skin.
clean_band.py in.IMG out.IMG [level frames e.g. 1,2,3,4,5,9,13,14,15]"""
import sys, numpy as np
from scipy import ndimage
sys.path.insert(0, __import__("os").path.dirname(__file__)); import imglib
src, dst = sys.argv[1:3]
LEVEL = {int(v) for v in (sys.argv[3] if len(sys.argv) > 3 else "1,2,3,4,5,9,13,14,15").split(",")}
b, ii, pp = imglib.read_lib(src); pal = np.array(pp[0]["colors"], float)
L = pal @ [.3, .59, .11]; sat = (pal.max(1) - pal.min(1)) / np.maximum(pal.max(1), 1)
whiteish = (L > 135) & (sat < 0.22); whiteish[0] = False
W4 = sorted(np.nonzero(whiteish)[0], key=lambda i: -L[i])[:4]       # brightest .. darker
TOP, FILL, LOW, SHADOW = W4[0], W4[1], W4[2], W4[3]
new = {}
for k, im in enumerate(ii):
    w, h = im["w"], im["h"]; px = np.array(imglib.pixels(b, im)).reshape(h, w); op = px != 0
    cand = whiteish[px] & op
    lab, n = ndimage.label(cand)
    if not n: continue
    sz = ndimage.sum(cand, lab, range(1, n + 1)); band = lab == (np.argmax(sz) + 1)
    if band.sum() < 10: continue
    if k + 1 in LEVEL:
        cols = [x for x in range(w) if band[:, x].any()]
        top = np.array([np.nonzero(band[:, x])[0].min() for x in cols]); bot = np.array([np.nonzero(band[:, x])[0].max() for x in cols])
        th = np.median(bot - top)
        pt = np.polyfit(cols, top, 2); m = np.zeros_like(band)
        for x in range(min(cols), max(cols) + 1):
            t = int(round(np.polyval(pt, x))); bo = int(round(np.polyval(pt, x) + th))
            m[max(0, t):min(h, bo + 1), x] = True
        band = m & op
    else:
        m = ndimage.binary_closing(band, iterations=1) | band
        m = ndimage.binary_fill_holes(m)
        m = ndimage.binary_opening(m, structure=np.ones((2, 2))) | (band & ndimage.binary_erosion(m))
        s = ndimage.uniform_filter(m.astype(float), 3); band = ((s > 0.5) | (m & (s > 0.34))) & op
    out = px.copy()
    stray = (cand | whiteish[px]) & op & ~band
    for y, x in zip(*np.nonzero(stray)):
        nb = [v for v in px[max(0, y - 2):y + 3, max(0, x - 2):x + 3].reshape(-1) if v and not whiteish[v]]
        if nb: out[y, x] = max(set(nb), key=nb.count)
    out[band] = FILL
    up = band & ~np.roll(band, 1, 0); dn = band & ~np.roll(band, -1, 0)
    out[up] = TOP; out[dn] = SHADOW
    out[dn & np.roll(up, 0, 0)] = LOW
    edge = band & ~ndimage.binary_erosion(band) & ~up & ~dn
    out[edge] = LOW
    new[k] = (w, h, im["anix"], im["aniy"], [int(v) for v in out.reshape(-1)])
imglib.write_lib(dst, b, ii, pp, new)
print("cleaned", sorted(k + 1 for k in new))
