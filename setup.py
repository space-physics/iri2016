#!/usr/bin/env python
install_requires = ['python-dateutil','numpy','pathlib2']
tests_require = ['nose','coveralls']
name = 'pyiri2016'
# %%
from setuptools import find_packages
from numpy.distutils.core import Extension, setup
from glob import glob
from os.path import join


src = ['iriwebg.for', 'irisub.for', 'irifun.for',
              'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for']

src = [join('fortran', s) for s in src]

ext = Extension(name='iri2016', sources=src,
                 f2py_options=['--quiet','skip:','dfridr',':'],
                 extra_f77_compile_args=['-w'])


ccirData = glob(join(join('data', 'ccir'), '*.asc'))
igrfData = glob(join(join('data', 'igrf'), '*.dat'))
indexData = glob(join(join('data', 'index'), '*.dat'))
mcsatData = glob(join(join('data', 'mcsat'), '*.dat'))
ursiData = glob(join(join('data', 'ursi'), '*.asc'))


iriDataFiles = [(join(name, join('data', 'ccir')), ccirData),
                (join(name, join('data', 'igrf')), igrfData),
                (join(name, join('data', 'index')), indexData),
                (join(name, join('data', 'mcsat')), mcsatData),
                (join(name, join('data', 'ursi')), ursiData)
                ]

if __name__ == '__main__':

    setup(name=name,
          packages=find_packages(),
          version='1.3.1',
          author=['Michael Hirsch, Ph.D.','Ronald Ilma'],
          url = 'https://github.com/scivision/pyIRI2016',
          description='IRI2016 International Reference Ionosphere from Python',
          long_description=open('README.rst').read(),
          classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          'Programming Language :: Python :: 3',
          ],
        ext_modules = [ext],
        data_files = iriDataFiles,
        install_requires = install_requires,
        extras_require={'plot':['matplotlib','seaborn','scipy','timeutil','pyigrf12','cartopy','pyapex'],
                         'tests':tests_require,},
        tests_require = tests_require,
        python_requires='>=3.6',
        )
