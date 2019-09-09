#!/usr/bin/env python3
import subprocess
import shutil
import os
from pathlib import Path

R = Path(__file__).resolve().parents[1]

CMAKE = shutil.which("cmake")
if not CMAKE:
    raise ImportError("CMake not found")


def build(srcdir: Path = R, builddir: Path = R / "build"):
    try:
        build_meson(srcdir, builddir)
    except Exception:
        build_cmake(srcdir, builddir)


def build_meson(srcdir: Path, builddir: Path):

    subprocess.check_call(["meson", "setup", str(builddir), str(srcdir)])
    subprocess.check_call(["ninja", "-C", str(builddir)])


def build_cmake(srcdir: Path, builddir: Path):

    tail = [" -S ", str(srcdir), " -B ", str(builddir)]

    if os.name == "nt":
        ccmd = [CMAKE, "-G", "MinGW Makefiles", "-DCMAKE_SH='CMAKE_SH-NOTFOUND'"] + tail
    else:
        ccmd = [CMAKE] + tail

    subprocess.check_call(ccmd)
    subprocess.check_call([CMAKE, "--build", str(builddir), "--parallel"])


if __name__ == "__main__":
    exe = build()
