#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_dosbox_path() -> Path:
    system = platform.system()

    if system == "Darwin":
        paths = [
	    Path("/Applications/DOSBox.app/Contents/MacOS/dosbox"),
        ]
    elif system == "Windows":
        paths = [
	    Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")) / "DOSBox-0.74-3" / "DOSBox.exe",
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "DOSBox-0.74-3" / "DOSBox.exe",
        ]
    else:
        paths = [
            Path("/usr/bin/dosbox"),
            Path("/usr/local/bin/dosbox"),
            Path.home() / ".local/bin/dosbox",
        ]

    for path in paths:
        if path.exists():
            return path

    dosbox = shutil.which("dosbox")
    if dosbox:
        return Path(dosbox)

    return None


def make_rom():
    script_dir = Path(__file__).parent.resolve()
    img_dir = script_dir / "IMG"
    rom_dir = img_dir / "rom"

    irw_path = img_dir / "MISC.IRW"
    if not irw_path.exists():
        irw_path = img_dir / "misc.irw"
    if not irw_path.exists():
        print("Error: MISC.IRW not found, skipping ROM generation.")
        return

    print("Reading misc.irw...")
    irw_data = irw_path.read_bytes()

    HEADER_SIZE = 0x44
    if len(irw_data) <= HEADER_SIZE:
        print(f"Error: misc.irw is too small ({len(irw_data)} bytes)")
        return

    bin_data = irw_data[HEADER_SIZE:]
    (img_dir / "misc.bin").write_bytes(bin_data)
    print(f"Wrote misc.bin ({len(bin_data)} bytes)")

    extra = len(bin_data) % 4
    if extra:
        # pad (not truncate) so the last image keeps all of its bytes
        print(f"Note: misc.bin size ({len(bin_data)}) not multiple of 4, padding")
        bin_data = bin_data + b"\x00" * (4 - extra)

    print("Deinterleaving into 4 byte planes...")
    planes = [bytearray() for _ in range(4)]
    for i, b in enumerate(bin_data):
        planes[i % 4].append(b)

    rom_dir.mkdir(exist_ok=True)
    for old_rom in rom_dir.glob("*.u*"):
        old_rom.unlink()
        print(f"  Removed {old_rom.name}")

    ROM_SIZE = 0x100000
    ROM_FILES = [
        "l1.0_nba_hangtime_u_117_image_rom.u117",
        "l1.0_nba_hangtime_u_116_image_rom.u116",
        "l1.0_nba_hangtime_u_115_image_rom.u115",
        "l1.0_nba_hangtime_u_114_image_rom.u114",
    ]

    for i, (plane, filename) in enumerate(zip(planes, ROM_FILES)):
        needed = ROM_SIZE - len(plane)
        if needed > 0:
            plane.extend(b'\x00' * needed)
        (rom_dir / filename).write_bytes(bytes(plane))
        print(f"Wrote {filename} ({len(plane)} bytes)")


def fix_palette():
    script_dir = Path(__file__).parent.resolve()
    pal_path = script_dir / "IMGPAL8.ASM"
    if not pal_path.exists():
        pal_path = script_dir / "imgpal8.asm"
    if not pal_path.exists():
        print("Warning: IMGPAL8.ASM not found, skipping palette fix.")
        return

    print("Fixing palettes...")
    lines = pal_path.read_text().splitlines()

    keep = [l for i, l in enumerate(lines) if i < 7 or i >= 44]
    kept = keep[:len(keep) - 70]

    pal_path.unlink()
    (script_dir / "IMGPAL8.ASM").write_text("\n".join(kept))
    print("Wrote IMGPAL8.ASM")


# Program ROM .text is full: the image headers / palettes of these heads go to the spare "shit" section.
SPARE_HEADS = ["XBOG", "XPMA", "XSPU", "XSTE", "XKLA", "XKOR", "XTMA", "XANT", "XHOL"]


def move_to_spare():
    script_dir = Path(__file__).parent.resolve()
    import re
    for fname, pat in (("NEWHEADS.TBL", r"^(%s)\d\d:"), ("IMGPAL8.ASM", r"^(%s)_P:")):
        path = script_dir / fname
        if not path.exists():
            path = script_dir / fname.lower()
        lines = path.read_text().split("\n")
        out, inside = [], False
        rx = re.compile(pat % "|".join(SPARE_HEADS))
        for ln in lines:
            label = re.match(r"^\w+:", ln)
            if label and rx.match(ln) and not inside:
                out += ['\t.sect\t"shit"', "\t.even"]; inside = True
            elif label and inside and not rx.match(ln):
                out += ["\t.text"]; inside = False
            out.append(ln)
        if inside: out.append("\t.text")
        path.write_text("\n".join(out))
        print(f"Moved {', '.join(SPARE_HEADS)} to the spare section in {path.name}")


def patch_names3():
    """The big DREAM TEAM scoreboard name lives in the names3 library but uses the BST18Y big-font palette."""
    import re
    path = Path(__file__).parent.resolve() / "NAMES3.TBL"
    t = path.read_text()
    t = re.sub(r"(\n(?:DREAM|NOLA|MEMPH|BRKLN):\n(?:.*\n){3})\t\.long\s+BAST_Y_P", r"\1\t.long   BST18Y_P", t)
    path.write_text(t)
    print("Patched DREAM palette in NAMES3.TBL")


def main():
    script_dir = Path(__file__).parent.resolve()

    dosbox = get_dosbox_path()
    if not dosbox:
        print("Error: DOSBox not found.")
        sys.exit(1)

    conf = script_dir / "build.conf"
    if not conf.exists():
        print(f"Error: build.conf not found in {script_dir}")
        sys.exit(1)

    cmd = [
        str(dosbox),
        "-conf", str(conf),
	"-noconsole",
	"-fastlaunch",
        "-c", "buildgfx.bat"
    ]

    result = subprocess.run(cmd, cwd=str(script_dir))
    if result.returncode != 0:
        sys.exit(result.returncode)

    make_rom()
    fix_palette()
    move_to_spare()
    patch_names3()


if __name__ == "__main__":
    main()
