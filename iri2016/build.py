"""
A generic, clean way to build C/C++/Fortran code from setup.py or manually

Michael Hirsch, Ph.D.
https://www.scivision.dev
"""
import shutil
from pathlib import Path
import subprocess
import os
import sys
import pkg_resources

R = Path(__file__).resolve().parents[1]
SRCDIR = R
BINDIR = SRCDIR / "build"


def build(build_sys: str, src_dir: Path = SRCDIR, bin_dir: Path = BINDIR):
    """
    attempts build with Meson or CMake
    """
    if build_sys == "meson":
        meson_setup(src_dir, bin_dir)
    elif build_sys == "cmake":
        if not check_cmake_version("3.13.0"):
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

    wopts = ["-G", "MinGW Makefiles", '-DCMAKE_SH="CMAKE_SH-NOTFOUND'] if os.name == "nt" else []

    subprocess.check_call([cmake_exe, "-S", str(src_dir), "-B", str(bin_dir)] + wopts)

    subprocess.check_call([cmake_exe, "--build", str(bin_dir), "--parallel"])


def meson_setup(src_dir: Path, bin_dir: Path):
    """
    attempt to build with Meson + Ninja
    """
    meson_exe = shutil.which("meson")

    if not meson_exe:
        raise FileNotFoundError("Meson not available")

    if not (bin_dir / "build.ninja").is_file():
        subprocess.check_call([meson_exe, "setup", str(bin_dir), str(src_dir)])

    subprocess.check_call([meson_exe, "test", "-C", str(bin_dir)])


def check_cmake_version(min_version: str) -> bool:
    cmake = shutil.which("cmake")
    if not cmake:
        return False

    cmake_version = subprocess.check_output([cmake, "--version"], universal_newlines=True).split()[2]

    pmin = pkg_resources.parse_version(min_version)
    pcmake = pkg_resources.parse_version(cmake_version)

    return pcmake >= pmin


if __name__ == "__main__":
    build(sys.argv[1])
