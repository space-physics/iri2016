import importlib.resources
import shutil
import subprocess


def build(exe_name: str):

    if not importlib.resources.is_resource(__package__, exe_name):
        ctest = shutil.which("ctest")
        if not ctest:
            raise RuntimeError("could not find CMake")
        if not (shutil.which("ninja") or shutil.which("make")):
            raise RuntimeError("Ninja not found. Please do 'python -m pip install ninja'")
        with importlib.resources.path(__package__, "setup.cmake") as setup:
            ret = subprocess.run([ctest, "-S", str(setup), "-VV"])
            if ret.returncode != 0:
                raise RuntimeError(f"not able to build {exe_name}")
