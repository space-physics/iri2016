cmake_minimum_required(VERSION 2.8.12)
project( iri2016 Fortran )

add_compile_options(-mtune=native)

add_executable(testiri2016 iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for iritest.for)
