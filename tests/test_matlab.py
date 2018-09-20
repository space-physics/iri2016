#!/usr/bin/env python
from pathlib import Path
import tempfile
import subprocess
import pytest
import xarray
import xarray.tests

R = Path(__file__).parent
Rm = Path(__file__).resolve().parents[1]


def test_matlab_api():
    try:
        subprocess.check_call(['matlab', '-nojvm', '-r "exit"'])
    except Exception:
        pytest.skip('Matlab not available')
        
    subprocess.check_call(['matlab', '-nojvm', '-r "iri2016()"'], cwd=Rm)


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
