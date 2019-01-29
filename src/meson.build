project('iri2016', 'fortran', default_options : ['default_library=static'])


iri2016= library('iri2016', 'irisub.for', 'irifun.for', 'iritec.for', 'iridreg.for', 'igrf.for', 'cira.for', 'iriflip.for',
  fortran_args: '-w')

driver = executable('iri2016_driver', 'iri2016_driver.F90',
  link_with: iri2016,
  fortran_args: '-DBIN_DIR='+ '"' + meson.build_root() + '"')
  
testexe = executable('testiri2016', 'test.f90',
  link_with: iri2016)
 
test('IRI2016', testexe)
