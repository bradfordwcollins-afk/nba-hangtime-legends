#!/usr/bin/env python3
"""Body (flesh) palette from a head: keeps the base body ramp's light->dark shape, takes the head's skin hue, and
moves its brightness by how much brighter/darker the new head's skin is than the old head's (the base ramp matched
the old head).  Used as a module: ramp(base_words, old_skin_rgbs, new_skin_rgbs) -> words"""
import numpy as np
import imglib
def lum(c): return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]
def skin(colors):
    out = []
    for c in colors:
        mx, mn = max(c), min(c)
        if lum(c) < 45 or mx == 0: continue
        if (mx - mn) / mx < 0.22: continue           # white / grey (headband, eyes, teeth)
        if c[1] < 0.12 * c[0]: continue              # pure red (headband)
        if c[1] / max(1, c[0]) > 0.8: continue       # greenish / grey (hair)
        out.append(c)
    return np.array(out, float)
def ramp(base, old, new, k_extra=1.0):
    r = np.median(new / np.array([lum(c) for c in new])[:, None], 0)
    k = k_extra * np.median([lum(c) for c in new]) / np.median([lum(c) for c in old])
    return [base[0]] + [imglib.to15(np.clip(r * lum(imglib.c15(w)) * k, 0, 255)) for w in base[1:]], r, k
