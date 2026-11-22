"""Index of every head in the game: label -> (lib, [16 image indices]), and which roster names use it."""
import re, glob, os
import imglib
SRC = '/home/claude/nba-hangtime-rebuild/BACKUP/XCODE101L'
def build():
    heads = {}
    for f in glob.glob(SRC + '/*.axx'):
        lab = None
        for line in open(f, errors='replace'):
            m = re.match(r'^(\w+_h)\s*$', line.rstrip())
            if m: lab = m.group(1); continue
            m = re.match(r'^\s+HDMAC\s+(\w+)', line)
            if m and lab: heads.setdefault(lab, m.group(1))
            lab = None
    users = {}
    for f in glob.glob(SRC + '/PLYRAT*.axx'):
        prev = ''
        for line in open(f, errors='replace'):
            m = re.search(r';\s*([A-Z][A-Za-z .\'\-()]+?)\s*$', line)
            if 'LWWWWWW' in line and m: prev = m.group(1).strip()
            m2 = re.search(r'(\w+_h)\s*(;.*)?$', line)
            if line.strip().startswith('.long') and m2 and prev:
                users.setdefault(m2.group(1), set()).add(re.sub(r'\s*\(dead slot\)', '', prev, flags=re.I))
    where = {}; libs = {}
    for f in sorted(glob.glob(SRC + '/IMG/*.IMG')) + sorted(glob.glob(SRC + '/../ART100/*.IMG')):
        try: b, ii, pp = imglib.read_lib(f)
        except Exception: continue
        libs[f] = (b, ii, pp)
        for k, im in enumerate(ii): where.setdefault(im['name'].upper(), (f, k))
    out = {}
    for lab, first in heads.items():
        f, k = where[first.upper()]; b, ii, pp = libs[f]
        pre = re.sub(r'0?1$', '', first.upper()); cand = {}
        for j, im in enumerate(ii):
            m = re.match(re.escape(pre) + r'_?0?(\d+)$', im['name'].upper())
            if m: cand[int(m.group(1))] = j
        frames = [cand.get(n, k + n - 1) for n in range(1, 17)]
        out[lab] = dict(lib=f, frames=frames, users=sorted(u for u in users.get(lab, ()) if u.upper() != 'CAN SHATTER'))
    return out, libs
