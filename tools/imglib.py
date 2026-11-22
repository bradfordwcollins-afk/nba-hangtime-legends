"""Read / write Williams .IMG libraries (8-bit images + 15-bit palettes) as used for the heads."""
import struct
PAL_BASE = 3
def c15(w): return (((w >> 10) & 31) << 3 | ((w >> 10) & 31) >> 2, ((w >> 5) & 31) << 3 | ((w >> 5) & 31) >> 2, (w & 31) << 3 | (w & 31) >> 2)
def read_lib(path):
    b = open(path, "rb").read()
    nimg, npal, diro = struct.unpack_from("<HHI", b, 0)
    imgs = []
    for i in range(nimg):
        r = diro + i * 50
        name = b[r:r + 16].split(b"\0")[0].decode("latin-1")
        flags, ax, ay, w, h, pal, off = struct.unpack_from("<HhhHHHI", b, r + 16)
        imgs.append(dict(name=name, flags=flags, anix=ax, aniy=ay, w=w, h=h, pal=pal, off=off, rec=b[r:r + 50]))
    pals = []
    pd = diro + nimg * 50
    for i in range(npal - PAL_BASE):
        r = pd + i * 26
        name = b[r:r + 10].split(b"\0")[0].decode("latin-1")
        _, bits, n, off = struct.unpack_from("<BBHI", b, r + 10)
        words = struct.unpack_from(f"<{n}H", b, off)
        pals.append(dict(name=name, n=n, off=off, words=list(words), colors=[c15(w) for w in words]))
    return b, imgs, pals
def pixels(b, im):
    s = (im["w"] + 3) & ~3
    return [b[im["off"] + y * s + x] for y in range(im["h"]) for x in range(im["w"])]
def render(b, im, pals, scale=1):
    from PIL import Image
    pal = pals[im["pal"] - PAL_BASE]["colors"]
    out = Image.new("RGBA", (im["w"], im["h"]))
    px = pixels(b, im)
    out.putdata([(0, 0, 0, 0) if c == 0 else pal[c] + (255,) for c in px])
    return out.resize((im["w"] * scale, im["h"] * scale), Image.NEAREST) if scale > 1 else out

def to15(c):
    c = [max(0, min(255, int(round(v)))) for v in c[:3]]
    return ((c[0] >> 3) << 10) | ((c[1] >> 3) << 5) | (c[2] >> 3)

def write_lib(path, b, imgs, pals, new):
    """Rewrite the library: new = {index: (w, h, anix, aniy, pixels)} replaces those images; the rest is copied."""
    body = bytearray(b[:28])
    pal_offs = []
    for p in pals:
        pal_offs.append(len(body)); body += struct.pack(f"<{len(p['words'])}H", *p["words"])
    img_offs, dims = [], []
    for k, im in enumerate(imgs):
        if k in new: w, h, ax, ay, px = new[k]
        else: w, h, ax, ay, px = im["w"], im["h"], im["anix"], im["aniy"], pixels(b, im)
        s = (w + 3) & ~3; img_offs.append(len(body)); dims.append((w, h, ax, ay))
        for y in range(h): body += bytes(px[y * w:(y + 1) * w]) + bytes(s - w)
    diro = len(body)
    for im, off, (w, h, ax, ay) in zip(imgs, img_offs, dims):
        rec = bytearray(im["rec"]); struct.pack_into("<HhhHHHI", rec, 16, im["flags"], ax, ay, w, h, im["pal"], off); body += rec
    nimg, npal, odir = struct.unpack_from("<HHI", b, 0)
    for i, p in enumerate(pals):
        r = bytearray(b[odir + nimg * 50 + i * 26: odir + nimg * 50 + i * 26 + 26]); struct.pack_into("<HI", r, 12, len(p["words"]), pal_offs[i]); body += r
    struct.pack_into("<HHI", body, 0, nimg, npal, diro)
    open(path, "wb").write(body)
