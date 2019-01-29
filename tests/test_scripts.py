#!/usr/bin/env python
import pytest
import subprocess


def test_latitude():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRI16latitudeProfile', '-148'])


def test_time():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRI16timeProfile', '2012-01-01', '2012-01-02', '1.0', '65', '-148'])


def test_alt():
    pytest.importorskip('matplotlib')
    subprocess.check_call(['IRI16altitudeProfile', '2012-01-01', '65', '-148'])


if __name__ == '__main__':
    pytest.main(['-xv', __file__])
