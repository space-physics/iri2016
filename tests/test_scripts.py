#!/usr/bin/env python
import pytest
import sys
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parents[1]
PY = sys.executable


def test_latitude():
    pytest.importorskip("matplotlib")
    subprocess.check_call([PY, "LatitudeProfile.py", "-148"], cwd=R)


def test_time():
    pytest.importorskip("matplotlib")
    subprocess.check_call([PY, "TimeProfile.py", "2012-01-01", "2012-01-02", "1.0", "65", "-148"], cwd=R)


def test_alt():
    pytest.importorskip("matplotlib")
    subprocess.check_call([PY, "AltitudeProfile.py", "2012-01-01", "65", "-148"], cwd=R)


if __name__ == "__main__":
    pytest.main([__file__])
