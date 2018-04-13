#!/usr/bin/env python
install_requires = ['python-dateutil','numpy','xarray']
tests_require = ['pytest','nose','coveralls']
name = 'pyiri2016'
# %%
from pathlib import Path
from setuptools import find_packages
from numpy.distutils.core import Extension, setup
# %%

src = [#'iriwebg.for',
       'irisub.for', 'irifun.for',
              'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for']

F = Path('fortran')
src = [str(F/s) for s in src]

ext = Extension(name='iri2016', sources=src,
                 f2py_options=['--quiet','skip:','dfridr',':'],
                 extra_f77_compile_args=['-w'])


R = Path(name) / 'data'
iridata = (list((R/'ccir').glob('*.asc')) + 
           list((R/'igrf').glob('*.dat')) +
           list((R/'index').glob('*.dat')) +
           list((R/'mcsat').glob('*.dat')) +
           list((R/'ursi').glob('*.asc')))

iridata = list(map(str,iridata)) # even for Numpy 1.14 due to numpy.distutils

if __name__ == '__main__':

    setup(name=name,
          packages=find_packages(),
          version='1.4.1',
          author=['Michael Hirsch, Ph.D.','Ronald Ilma'],
          url = 'https://github.com/scivision/pyIRI2016',
          description='IRI2016 International Reference Ionosphere from Python',
          long_description=open('README.rst').read(),
          classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          ],
        ext_modules = [ext],
        data_files = iridata,
        install_requires = install_requires,
        extras_require={'plot':['matplotlib','seaborn','scipy','timeutil','pyigrf12','cartopy','pyapex'],
                         'tests':tests_require,},
        tests_require = tests_require,
        python_requires='>=3.6',
        scripts=['AltitudeProfile.py','TimeProfile.py','LatitudeProfile.py'],
        include_package_data=True,
        )
