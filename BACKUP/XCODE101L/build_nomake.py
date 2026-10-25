#!/usr/bin/env python3
"""Drop-in alternative to build.py that does not use gmake.

gmake stays loaded while it runs the assembler, and with the extra players the
big modules (SELECT2 and later) can hang for lack of DOS memory. This script
assembles every module one by one in a plain batch file, links, and runs
bigsrec - the same steps build.bat/gmake perform - then merges the ROMs.

Usage (after buildgfx.py):   python3 build_nomake.py
Check asm.log and link.log if something fails.
"""
import re, subprocess, sys
from pathlib import Path
from build import get_dosbox_path, merge_rom

here = Path(__file__).parent.resolve()
mk = (here / "MAKEFILE").read_text(encoding="latin-1")
objs = mk.split("O =", 1)[1].split("\n\n")[0]
objs = "\n".join(l for l in objs.splitlines() if not l.lstrip().startswith("#"))
mods = [m[:-4] for m in re.findall(r"([A-Z0-9_]+\.OBJ)", objs)]

lines = ["echo off", "del *.obj", "del *.out", "\\tools\\vidram on", "del asm.log"]
for m in mods:
    lines += [f"echo {m} >> asm.log", f"\\tools\\gspa {m}.axx {m}.obj -h -l -v10 >> asm.log"]
lines += ["\\tools\\gsplnk bb.cmd > link.log", "cd rom", "\\tools\\vidram off",
          "c:\\tools\\bigsrec <ff8.lrn > ..\\srec.log", "exit"]
(here / "BUILDNM.BAT").write_text("\r\n".join(lines) + "\r\n")

dosbox = get_dosbox_path()
if not dosbox:
    sys.exit("Error: DOSBox not found.")
r = subprocess.run([str(dosbox), "-conf", str(here / "build.conf"), "-noconsole",
                    "-fastlaunch", "-c", "BUILDNM.BAT"], cwd=str(here))
log = (here / "asm.log")
if log.exists():
    txt = log.read_text(errors="replace")
    bad = re.findall(r"(\d+) Errors", txt)
    print(f"Assembled {txt.count('No Errors')} of {len(mods)} modules cleanly.")
    if bad:
        print("Errors found - see asm.log")
merge_rom()
