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
    
    
def test_top_scripts():
    """ uses tempdir so as to show directory-agnostic module behavior (essential!)"""
    scripts = ['AltitudeProfile.py','TimeProfile.py','LatitudeProfile.py']
    with tempfile.TemporaryDirectory() as d:
        print('running script from directory',d)
        
        for s in scripts:
            shutil.copy(root/s, d)
            print('testing',s)
            subprocess.check_call(['python',s,'-q'], cwd=d)


if __name__ == '__main__':
    np.testing.run_module_suite()
