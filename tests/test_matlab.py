#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import shutil

R = Path(__file__).parent


@pytest.mark.skipif(not shutil.which('matlab'), reason='matlab not found')
def test_matlab_api():
    subprocess.check_call(['matlab', '-nojvm', '-r',
                           'r=runtests(); exit(any([r.Failed]))'],
                          cwd=R, timeout=60)


@pytest.mark.skipif(not shutil.which('octave'), reason='octave not found')
def test_octave_api():
    subprocess.check_call(['octave', '-q', '--eval="exit(test_iri2016)"'],
                          cwd=R, timeout=60)


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
