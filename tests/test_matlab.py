#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import shutil

R = Path(__file__).parent

OCTAVE = shutil.which("octave-cli")
MATLAB = shutil.which("matlab")


@pytest.mark.skipif(not MATLAB, reason="matlab not found")
def test_matlab_api():
    subprocess.check_call([MATLAB, "-batch", "test_iri2016"], cwd=R, timeout=60)


@pytest.mark.skipif(not OCTAVE, reason="octave not found")
def test_octave_api():
    subprocess.check_call([OCTAVE, "test_iri2016.m"], cwd=R, timeout=60)


if __name__ == "__main__":
    pytest.main([__file__])
