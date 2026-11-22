#!/usr/bin/env python3
"""Rebuild a player's head library in the photos' own colours.
natural_heads.py <orig.IMG> <out.IMG> <crops.txt> <skinref frames e.g. 3,4,5,14>
crops.txt lines: photo frame# x0,y0,x1,y1 cx,cy,rx,ry flip|-
Photo frames are drawn straight from the (de-blued) photos; the other frames keep their drawing but their colours
are moved to the photos' skin tone; then one new palette is built for all frames.  Prints the skin colour stats
(old head skin, new head skin) used to rebuild the body palette."""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, __import__("os").path.dirname(__file__)); import imglib
src, dst, crops, refs = sys.argv[1:5]
b, ii, pp = imglib.read_lib(src)
pal0 = pp[0]
def isband(c):
    mx, mn = max(c[:3]), min(c[:3]); return mx > 95 and (mx - mn) / mx < 0.22
def lum(c): return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]
frames = {}          # k -> (w, h, ax, ay, rgba float array)
for line in open(crops):
    if not line.strip(): continue
    f, fr, box, el, fl = line.split(); k = int(fr) - 1
    im = Image.open(f).convert("RGBA"); a = np.asarray(im).copy()
    cx, cy, rx, ry = map(float, el.split(",")); yy, xx = np.mgrid[:a.shape[0], :a.shape[1]]
    a[((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 > 1] = 0
    head = Image.fromarray(a).crop(tuple(map(int, box.split(","))))
    if fl == "flip": head = head.transpose(Image.FLIP_LEFT_RIGHT)
    H = ii[k]["h"]; W = max(8, round(head.width * H / head.height))
    # premultiplied resize so transparent pixels don't bleed black into the edge
    ha = np.asarray(head).astype(np.float32); al = ha[..., 3:4] / 255
    pm = Image.fromarray(np.clip(np.dstack([ha[..., :3] * al, ha[..., 3]]), 0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    s = np.asarray(pm).astype(np.float32); al = s[..., 3:4] / 255
    rgb = np.where(al > 0.05, s[..., :3] / np.maximum(al, 0.05), 0)
    op = s[..., 3] > 110
    rows = np.nonzero(op.any(1))[0]; cols = np.nonzero(op.any(0))[0]
    y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    rgb = rgb[y0:y1, x0:x1]; op = op[y0:y1, x0:x1]; w, h = x1 - x0, y1 - y0
    old = ii[k]; ax = round(old["anix"] * w / old["w"]); ay = h - (old["h"] - old["aniy"])
    frames[k] = (w, h, ax, ay, rgb, op)
# skin stats: photos vs the old head
def skinpx(rgbs):
    return np.array([c for c in rgbs if not isband(c) and lum(c) > 55])
new_skin = skinpx([tuple(c) for k, (w, h, ax, ay, rgb, op) in frames.items() for c in rgb[op]])
oldc = pal0["colors"]
old_skin = skinpx([oldc[c] for r in map(int, refs.split(",")) for c in imglib.pixels(b, ii[r - 1]) if c])
def ratio(px): return np.median(px / np.maximum(np.array([lum(c) for c in px]), 1)[:, None], 0)
newpx = np.array([c for k, (w, h, ax, ay, rgb, op) in frames.items() for c in rgb[op] if not isband(c)])
oldpx = np.array([oldc[c] for r in map(int, refs.split(",")) for c in imglib.pixels(b, ii[r - 1]) if c and not isband(oldc[c])], float)
nl = np.array([lum(c) for c in newpx]); ol = np.array([lum(c) for c in oldpx])
rs = ratio(new_skin); ks = 0.88 * np.median([lum(c) for c in new_skin]) / np.median([lum(c) for c in old_skin])
def hairness(c): return min(1, max(0, (c[1] / max(c[0], 1) - 0.62) / 0.15))
nh, oh = newpx[nl < 40], np.array([c for c in oldpx if hairness(c) > 0.5])
rh = ratio(nh) if len(nh) else rs; kh = (np.median([lum(c) for c in nh]) / np.median([lum(c) for c in oh])) if len(nh) and len(oh) else 1
def moved(c):
    if isband(c): return np.array(c, float)
    L = lum(c); t = 1 - hairness(c)
    return np.clip(rh * L * kh * (1 - t) + rs * L * ks * t, 0, 255)
for k, im in enumerate(ii):
    if k in frames: continue
    px = imglib.pixels(b, im); w, h = im["w"], im["h"]
    rgb = np.array([moved(oldc[c]) if c else (0, 0, 0) for c in px], float).reshape(h, w, 3)
    op = (np.array(px) != 0).reshape(h, w)
    frames[k] = (w, h, im["anix"], im["aniy"], rgb, op)
# one palette for everything (index 0 = transparent), 15-bit
allpx = np.concatenate([rgb[op] for (w, h, ax, ay, rgb, op) in frames.values()]).astype(np.uint8)
n = pal0["n"] - 1
q = Image.fromarray(allpx.reshape(1, -1, 3)).quantize(n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
qp = np.array(q.getpalette()[:3 * n], float).reshape(-1, 3)
words = [pal0["words"][0]] + [imglib.to15(c) for c in qp]
cols = np.array([imglib.c15(wd) for wd in words[1:]], float)
wt = np.array([2, 3, 1], float)
new = {}
for k, (w, h, ax, ay, rgb, op) in frames.items():
    d = (((rgb.reshape(-1, 1, 3) - cols[None]) ** 2) * wt).sum(-1)
    idx = d.argmin(1) + 1
    idx[~op.reshape(-1)] = 0
    new[k] = (w, h, ax, ay, [int(v) for v in idx])
pp[0]["words"] = words
imglib.write_lib(dst, b, ii, pp, new)
print(json.dumps(dict(old_skin=old_skin.mean(0).round(1).tolist(), new_skin=new_skin.mean(0).round(1).tolist(),
                      old_lum=float(np.median([lum(c) for c in old_skin])), new_lum=float(np.median([lum(c) for c in new_skin])))))
