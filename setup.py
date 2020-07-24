#!/usr/bin/env python
import setuptools  # noqa: F401
from pathlib import Path

"""
Because of bad bugs in IRI2016 itself, present even in plain Fortran usage, we can't safely use F2py, bad data can result.

src = [  # 'iriwebg.for',
    'irisub.for', 'irifun.for',
    'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for']

F = Path('src')
src = [str(F/s) for s in src]

ext = Extension(name='iri16', sources=src,
                f2py_options=['only:', 'iri_sub', ':'],  # ['skip:', 'dfridr', ':'],
                extra_f77_compile_args=['-w'])
"""

R = Path("src/iri2016/data")
if not R.is_dir():
    raise FileNotFoundError(R)

iridata = list(
    map(
        str,
        (
            list((R / "ccir").glob("*.asc"))
            + list((R / "igrf").glob("*.dat"))
            + list((R / "index").glob("*.dat"))
            + list((R / "mcsat").glob("*.dat"))
            + list((R / "ursi").glob("*.asc"))
        ),
    )
)

if not iridata:
    raise FileNotFoundError(f"iri data not found in {R}")

iridata = list(map(str, iridata))  # even for Numpy 1.14 due to numpy.distutils

setuptools.setup(
    # ext_modules=[ext],
    data_files=iridata
)
