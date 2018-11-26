#!/usr/bin/env python
import setuptools  # noqa: F401
from pathlib import Path
# from numpy.distutils.core import Extension, setup
import os
import subprocess

"""
if os.name == 'nt':
    sfn = Path(__file__).parent / 'setup.cfg'
    stxt = sfn.read_text()
    if '[build_ext]' not in stxt:
        with sfn.open('a') as f:
            f.write("[build_ext]\ncompiler = mingw32")


src = [  # 'iriwebg.for',
    'irisub.for', 'irifun.for',
    'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for']

F = Path('src')
src = [str(F/s) for s in src]

ext = Extension(name='iri16', sources=src,
                f2py_options=['only:', 'iri_sub', ':'],  # ['skip:', 'dfridr', ':'],
                extra_f77_compile_args=['-w'])
"""

R = Path('iri2016') / 'data'
iridata = list(map(str,
                   (list((R/'ccir').glob('*.asc')) +
                    list((R/'igrf').glob('*.dat')) +
                       list((R/'index').glob('*.dat')) +
                       list((R/'mcsat').glob('*.dat')) +
                       list((R/'ursi').glob('*.asc')))
                   ))

iridata = list(map(str, iridata))  # even for Numpy 1.14 due to numpy.distutils

setuptools.setup(
    # ext_modules=[ext],
    data_files=iridata,
)

# %% workaround
if os.name == 'nt':
    subprocess.check_call(['cmake', '-G', 'MinGW Makefiles',
                           '-DCMAKE_SH="CMAKE_SH-NOTFOUND', '../src'],
                          cwd='bin',
                          universal_newlines=True)
else:
    subprocess.check_call(['cmake', '../src'], cwd='bin',
                          universal_newlines=True)


subprocess.check_call(['cmake', '--build', '.'], cwd='bin',
                      universal_newlines=True)
