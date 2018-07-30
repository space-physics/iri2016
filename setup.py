#!/usr/bin/env python
import setuptools  # noqa: F401
from pathlib import Path
from numpy.distutils.core import Extension, setup

src = [  # 'iriwebg.for',
    'irisub.for', 'irifun.for',
    'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for']

F = Path('src')
src = [str(F/s) for s in src]

ext = Extension(name='iri16', sources=src,
                f2py_options=['--quiet', 'skip:', 'dfridr', ':'],
                extra_f77_compile_args=['-w'])


R = Path('iri2016') / 'data'
iridata = list(map(str,
                   (list((R/'ccir').glob('*.asc')) +
                    list((R/'igrf').glob('*.dat')) +
                       list((R/'index').glob('*.dat')) +
                       list((R/'mcsat').glob('*.dat')) +
                       list((R/'ursi').glob('*.asc')))
                   ))

iridata = list(map(str, iridata))  # even for Numpy 1.14 due to numpy.distutils

setup(ext_modules=[ext],
      data_files=iridata,
      )
