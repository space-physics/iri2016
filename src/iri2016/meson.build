project('iri2016', 'fortran',
  default_options : ['default_library=shared', 'buildtype=release', 'warning_level=0', 'fortran_std=legacy'])

fc = meson.get_compiler('fortran')

subdir('src')

driver = executable('iri2016_driver',
  sources: 'src/iri2016_driver.f90',
  link_with : iri_lib)

testexe = executable('test_iri2016',
  sources: 'src/test.f90',
  link_with: iri_lib)

test('IRI2016', testexe,
  timeout: 15,
  workdir: meson.source_root())
