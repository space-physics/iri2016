project('iri2016', 'fortran',
  default_options : ['default_library=static', 'buildtype=release'])

fc = meson.get_compiler('fortran')

if fc.get_id() == 'intel'
  oldargs = '-nowarn'
elif fc.get_id() == 'intel-cl'
  oldargs = '/nowarn'
else
  oldargs = '-w'
endif

subdir('iri2016/src')

driver = executable('iri2016_driver', 'iri2016/src/iri2016_driver.F90',
  link_with: iri2016,
  fortran_args: '-DBIN_DIR='+ '"' + meson.build_root() + '"')

testexe = executable('testiri2016', 'iri2016/src/test.f90',
  link_with: iri2016)

test('IRI2016', testexe,
  timeout: 15)