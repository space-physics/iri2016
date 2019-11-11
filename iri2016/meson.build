project('iri2016', 'fortran',
  default_options : ['default_library=static', 'buildtype=release'])

fc = meson.get_compiler('fortran')
oldargs = fc.first_supported_argument(['/nowarn', '-nowarn', '-w'])

subdir('src')

driver = executable('iri2016_driver', 'src/iri2016_driver.f90',
  link_with: iri2016)

testexe = executable('testiri2016', 'src/test.f90',
  link_with: iri2016)

test('IRI2016', testexe,
  timeout: 15,
  workdir: meson.source_root())