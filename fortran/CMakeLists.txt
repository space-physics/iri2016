cmake_minimum_required(VERSION 2.8.12)
project( iri2016 Fortran )

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ..)

add_compile_options(-mtune=native -g -fbacktrace)

# not used for now
# add_executable(testiri2016 iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for iritest.for)

add_executable(baseIRI2016 irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for test.f90)
