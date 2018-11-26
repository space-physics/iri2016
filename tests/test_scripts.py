#!/usr/bin/env python
import pytest
import subprocess


def test_latitude():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRI16latitudeProfile', '-148'])


def test_time():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRI16timeProfile', '65', '-148'])


def test_alt():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRI16altitudeProfile', '65', '-148'])


if __name__ == '__main__':
    pytest.main(['-xv', __file__])
