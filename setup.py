
from glob import glob
from numpy.distutils.core import Extension, setup
from os.path import join


name = 'pyiri2016'
sourcePath = 'source'
f77CompileArgs = ['-w']

iriSource1 = ['iriwebg.pyf', 'iriwebg.for', 'irisub.for', 'irifun.for', \
    'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for']
sources1 = []
for src in iriSource1:
    sources1.append(join(sourcePath, src))

ext1 = Extension(name='iriweb', sources=sources1, f2py_options=['--quiet'], \
    extra_f77_compile_args=f77CompileArgs)


ccirData = glob(join(join('data', 'ccir'), '*.asc'))
igrfData = glob(join(join('data', 'igrf'), '*.dat'))
indexData = glob(join(join('data', 'index'), '*.dat'))
mcsatData = glob(join(join('data', 'mcsat'), '*.dat'))
ursiData = glob(join(join('data', 'ursi'), '*.asc'))


iriDataFiles = [(join(name, join('data', 'ccir')), ccirData), \
    (join(name, join('data', 'igrf')), igrfData), \
    (join(name, join('data', 'index')), indexData), \
    (join(name, join('data', 'mcsat')), mcsatData), \
    (join(name, join('data', 'ursi')), ursiData) \
    ]

if __name__ == '__main__':

    setup(name=name, \
        version='1.0.0', \
        author='Ronald Ilma', \
        author_email='rri5@cornell.edu', \
        description='IRI2016 Apps', \
        packages=[name], \
        ext_package=name, \
        ext_modules=[ ext1 ], \
        data_files=iriDataFiles, \
        )