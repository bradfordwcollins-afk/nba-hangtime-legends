#!/usr/bin/env python3
"""Replace one in-game head frame with a photo, colour-matched to the player's other frames and drawn with his
existing head palette.  Usage: replace_head_frame.py <LIB.IMG> <frame# 1-16> <photo.png> x0,y0,x1,y1 cx,cy,rx,ry
   [--flip] [--out preview.png]   (box = head crop; ellipse = keep-mask in photo coords, cuts the neck)"""
import sys, statistics, argparse
sys.path.insert(0, __import__("os").path.dirname(__file__)); import imglib
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument("lib"); ap.add_argument("frame", type=int); ap.add_argument("photo")
ap.add_argument("box"); ap.add_argument("ellipse"); ap.add_argument("--flip", action="store_true"); ap.add_argument("--out")
ap.add_argument("--refs", default="3,5,8,14"); ap.add_argument("--height", type=int, default=0)
a = ap.parse_args()
b, ii, pp = imglib.read_lib(a.lib); k = a.frame - 1
pal = pp[ii[k]["pal"] - imglib.PAL_BASE]["colors"]
src = Image.open(a.photo).convert("RGBA")
x0, y0, x1, y1 = (int(v) for v in a.box.split(",")); cx, cy, rx, ry = (float(v) for v in a.ellipse.split(","))
px = src.load()
for y in range(src.height):
    for x in range(src.width):
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1: px[x, y] = (0, 0, 0, 0)
head = src.crop((x0, y0, x1, y1))
if a.flip: head = head.transpose(Image.FLIP_LEFT_RIGHT)
# colour match (per channel mean / spread) to the reference frames
ref = []
for r in (int(v) - 1 for v in a.refs.split(",")):
    im = ii[r]; p2 = pp[im["pal"] - imglib.PAL_BASE]["colors"]
    ref += [p2[c] for c in imglib.pixels(b, im) if c]
hp = head.load(); sp = [hp[x, y][:3] for y in range(head.height) for x in range(head.width) if hp[x, y][3] > 110]
st = [(statistics.mean(c[j] for c in ref), statistics.pstdev(c[j] for c in ref), statistics.mean(c[j] for c in sp), statistics.pstdev(c[j] for c in sp)) for j in range(3)]
for y in range(head.height):
    for x in range(head.width):
        c = hp[x, y]
        if c[3]: hp[x, y] = tuple(max(0, min(255, round(g[0] + (c[j] - g[2]) * g[1] / max(1, g[3])))) for j, g in enumerate(st)) + (c[3],)
H = a.height or ii[k]["h"]; W = max(8, round(head.width * H / head.height))
sm = head.resize((W, H), Image.LANCZOS)
out = []
for y in range(H):
    for x in range(W):
        c = sm.getpixel((x, y))
        if c[3] <= 110: out.append(0); continue
        out.append(min(range(1, len(pal)), key=lambda i: sum((c[j] - pal[i][j]) ** 2 * (2, 3, 1)[j] for j in range(3))))
rows = [y for y in range(H) if any(out[y * W:(y + 1) * W])]; cols = [x for x in range(W) if any(out[y * W + x] for y in range(H))]
ty0, ty1, tx0, tx1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
w, h = tx1 - tx0, ty1 - ty0; npx = [out[y * W + x] for y in range(ty0, ty1) for x in range(tx0, tx1)]
# neck point: same relative spot as the old frame
old = ii[k]; ax = round(old["anix"] * w / old["w"]); ay = h - (old["h"] - old["aniy"])
imglib.write_lib(a.lib, b, ii, pp, {k: (w, h, ax, ay, npx)})
if a.out:
    b2, i2, p2 = imglib.read_lib(a.lib)
    S = 5; img = Image.new("RGB", (len(i2) * 32 * S // 2, 46 * S), (36, 36, 44))
    for n, im in enumerate(i2):
        r = imglib.render(b2, im, p2, S // 2 + 1); img.paste(r, (n * 32 * S // 2, 4), r)
    img.save(a.out)
print("frame", a.frame, "->", w, "x", h, "anim", ax, ay)
