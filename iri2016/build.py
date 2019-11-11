"""
A generic, clean way to build C/C++/Fortran code "build on run"

Michael Hirsch, Ph.D.
https://www.scivision.dev
"""
import shutil
from pathlib import Path
import subprocess
import os
import typing
import sys
import pkg_resources
import argparse
import logging

R = Path(__file__).resolve().parent
SRCDIR = R
BINDIR = SRCDIR / "build"


def build(build_sys: str, src_dir: Path = SRCDIR, bin_dir: Path = BINDIR):
    """
    attempts build with Meson or CMake
    """
    if build_sys == "meson":
        meson_setup(src_dir, bin_dir)
    elif build_sys == "cmake":
        if not check_cmake_version("3.13"):
            raise ValueError("Need at least CMake 3.13")
        cmake_setup(src_dir, bin_dir)
    else:
        raise ValueError("Unknown build system {}".format(build_sys))


def cmake_setup(src_dir: Path, bin_dir: Path):
    """
    attempt to build using CMake >= 3
    """
    cmake_exe = shutil.which("cmake")
    if not cmake_exe:
        raise FileNotFoundError("CMake not available")
    cfgfn = bin_dir / "CMakeCache.txt"
    if cfgfn.is_file():
        cfgfn.unlink()

    wopts = ["-G", "MinGW Makefiles", '-DCMAKE_SH="CMAKE_SH-NOTFOUND'] if os.name == "nt" else []

    subprocess.run([cmake_exe, "-S", str(src_dir), "-B", str(bin_dir)] + wopts)

    subprocess.run([cmake_exe, "--build", str(bin_dir), "--parallel"])


def meson_setup(src_dir: Path, bin_dir: Path):
    """
    attempt to build with Meson + Ninja
    """
    args: typing.List[str] = []
    meson_exe = shutil.which("meson")

    if not meson_exe:
        raise FileNotFoundError("Meson not available")

    if (bin_dir / "build.ninja").is_file():
        args += ["--wipe"]

    cmd = [meson_exe, "setup", str(bin_dir), str(src_dir)] + args
    logging.debug(cmd)
    subprocess.run(cmd)

    subprocess.run([meson_exe, "test", "-C", str(bin_dir)])


def check_cmake_version(min_version: str) -> bool:
    cmake = shutil.which("cmake")
    if not cmake:
        return False

    cmake_version = subprocess.check_output([cmake, "--version"], universal_newlines=True).split()[2]

    pmin = pkg_resources.parse_version(min_version)
    pcmake = pkg_resources.parse_version(cmake_version)

    return pcmake >= pmin


def get_libpath(bin_dir: Path, stem: str) -> Path:
    if sys.platform in ("win32", "cygwin"):
        dllfn = bin_dir / ("lib" + stem + ".dll")
    elif sys.platform == "linux":
        dllfn = bin_dir / ("lib" + stem + ".so")
    elif sys.platform == "darwin":
        dllfn = bin_dir / ("lib" + stem + ".dylib")

    if not dllfn.is_file():
        dllfn = None

    return dllfn


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("buildsys", choices=["meson", "cmake"])
    P = p.parse_args()

    build(P.buildsys)
