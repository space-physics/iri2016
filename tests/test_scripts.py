#!/usr/bin/env python
import pytest
import subprocess
from pathlib import Path

root = Path(__file__).parents[1]


def test_latitude():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRIlatitudeProfile', '-148', '-q'])


def test_time():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRItimeProfile', '65', '-148', '-q'])


def test_alt():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRIaltitudeProfile', '65', '-148', '-q'])


if __name__ == '__main__':
    pytest.main(['-x', __file__])
