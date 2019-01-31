#!/usr/bin/env python
import setuptools  # noqa: F401
from pkg_resources import parse_version
from pathlib import Path
# from numpy.distutils.core import Extension, setup
import os
import subprocess

"""
Because of bad bugs in IRI2016 itself, present even in plain Fortran usage, we can't safely use F2py, bad data can result.

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

R = Path(__file__).parent
BINDIR = R / 'build'
SRCDIR = R / 'src'

cmakever = subprocess.check_output(['cmake', '--version'], universal_newlines=True)
cmakever = parse_version(cmakever.split()[2])
if cmakever < parse_version('3.13'):
    raise RuntimeError(
        'CMake >= 3.13 needed to build IRI2016.'
        'Please see https://cmake.org/download or https://github.com/scivision/cmake-utils/blob/master/cmake_setup.sh')

# %% workaround, CMake >= 3.13
if os.name == 'nt':
    subprocess.check_call(['cmake', '-G', 'MinGW Makefiles',
                           '-DCMAKE_SH="CMAKE_SH-NOTFOUND', '-S', str(SRCDIR), '-B', str(BINDIR)])
else:
    subprocess.check_call(['cmake', '-S', str(SRCDIR), '-B', str(BINDIR)])


subprocess.check_call(['cmake', '--build', str(BINDIR), '-j'])
