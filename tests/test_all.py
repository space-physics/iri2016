#!/usr/bin/env python
import numpy as np
from pathlib import Path
import pyiri2016
import tempfile
import shutil
import subprocess

root = Path(__file__).parents[1]

def test_main1():

    iri = pyiri2016.IRI('1980-03-21T12', 130., 0., 0.)

    np.testing.assert_allclose((iri['ne'].item(), iri.NmF2, iri.hmF2),
                    (267285184512.0, 2580958937088.0, 438.78643798828125))

    print('assert passed')
    
    
def test_other_directory():
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(root/'AltitudeProfile.py', d)
        print('running script from directory',d)
        subprocess.check_call(['python','AltitudeProfile.py','-q'],cwd=d)


if __name__ == '__main__':
    np.testing.run_module_suite()
