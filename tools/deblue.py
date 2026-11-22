#!/usr/bin/env python3
"""Remove a blue/purple light cast from a photo: blue-tinted pixels are re-tinted with the photo's own warm skin
tone (keeping their brightness); bright low-colour pixels (headband) become neutral white.  deblue.py in out"""
import sys
import numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert("RGBA")).astype(np.float32)
rgb, a = im[..., :3], im[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
lum = 0.30 * R + 0.59 * G + 0.11 * B
warm = (a > 200) & (R > B + 30) & (lum > 50) & (lum < 200)
ratio = np.median(rgb[warm] / lum[warm][:, None], axis=0)          # skin colour per unit brightness
skin = lum[..., None] * ratio
grey = np.repeat(lum[..., None], 3, -1) * np.array([1.02, 1.0, 0.97])
t = np.clip((B / np.maximum(R, 1) - 0.72) / 0.35, 0, 1)            # how blue-cast the pixel is
sat = (rgb.max(-1) - rgb.min(-1)) / np.maximum(rgb.max(-1), 1)
gr = G / np.maximum(R, 1)
neutral = np.clip((lum - 85) / 35, 0, 1) * np.clip((gr - 0.82) / 0.08, 0, 1)   # headband / whites (G close to R; skin has G well under R)
from scipy import ndimage
lab, n = ndimage.label((neutral > 0.3) & (a > 110))
if n:
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1)); keep = [i + 1 for i, z in enumerate(sizes) if z >= 0.15 * sizes.max()]
    neutral = neutral * np.isin(lab, keep)                                   # the headband only, not cheek glare
target = skin * (1 - neutral[..., None]) + grey * neutral[..., None]
out = rgb * (1 - t[..., None]) + target * t[..., None]
out = out * (1 - neutral[..., None] * (1 - t[..., None])) + grey * (neutral[..., None] * (1 - t[..., None]))
Image.fromarray(np.dstack([np.clip(out, 0, 255), a]).astype(np.uint8), "RGBA").save(sys.argv[2])
print(sys.argv[2], "skin ratio", ratio.round(3))
