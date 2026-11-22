#!/usr/bin/env python3
"""Paint short dark hair on a head library: the head is split by its headband, and the part on the scalp side
(direction per frame) becomes textured hair.  add_hair.py in.IMG out.IMG band_indices(1-11)"""
import sys, random
import numpy as np
from scipy import ndimage
sys.path.insert(0, __import__("os").path.dirname(__file__)); import imglib
src, dst = sys.argv[1:3]
band_idx = set(range(1, 12))
DIR = {1: (0, -1), 2: (0, -1), 3: (0, -1), 4: (0, -1), 5: (0, -1), 6: (-1, -1), 7: (0, -1), 8: (1, -1), 9: (0, -1),
       10: (0, -1), 11: None, 12: (-1, -1), 13: (-1, 1), 14: (0, -1), 15: (0, -1), 16: (-1, 0)}
BACK = {1: (9, None), 7: (8, None), 6: (8, None), 2: (7, 0.5)}   # back views: hair also on the far side of the band, (depth px, max x share)
b, ii, pp = imglib.read_lib(src)
words = list(pp[0]["words"])
HAIR = len(words); words.append(imglib.to15((26, 19, 17)))        # new near-black hair colour
LIGHT = [59, 60, 62]                                                # existing dark browns for the twists' texture
rnd = random.Random(7)
new = {}
for k, im in enumerate(ii):
    w, h = im["w"], im["h"]; px = np.array(imglib.pixels(b, im)).reshape(h, w)
    op = px != 0; band = np.isin(px, list(band_idx))
    lab, n = ndimage.label(op & ~band)
    by, bx = np.nonzero(band); bc = np.array([bx.mean(), by.mean()]) if len(bx) else np.array([w / 2, h / 2])
    hair = np.zeros_like(op)
    d = DIR[k + 1]
    for c in range(1, n + 1):
        m = lab == c; cy, cx = np.nonzero(m)
        if d is None or (np.array([cx.mean(), cy.mean()]) - bc) @ np.array(d, float) > 0: hair |= m
    if k + 1 in BACK and len(by):
        depth, xmax = BACK[k + 1]
        rest = op & ~band & ~hair
        dist = ndimage.distance_transform_edt(~band)
        yy, xx = np.mgrid[:h, :w]
        lim = depth * (1 - 0.35 * ((xx - w / 2) / (w / 2)) ** 2)        # nape hairline: deeper in the middle
        m = rest & (dist <= lim)
        edge = rest & (dist > lim) & (dist <= lim + 1.5) & ((xx + yy) % 2 == 0)
        m |= edge
        if xmax: m &= xx < xmax * w
        hair |= m
    out = px.copy()
    for y, x in zip(*np.nonzero(hair)):
        r = rnd.random()
        out[y, x] = LIGHT[(x + 2 * y) % 3] if (r < 0.22 and (x + y) % 2) else HAIR
    new[k] = (w, h, im["anix"], im["aniy"], [int(v) for v in out.reshape(-1)])
pp[0]["words"] = words
imglib.write_lib(dst, b, ii, pp, new)
print("hair colour index", HAIR, "palette size", len(words))
