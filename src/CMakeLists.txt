cmake_minimum_required(VERSION 3.1)
project(iri2016 Fortran)
enable_testing()

include(../cmake/compilers.cmake)

add_library(iri2016 irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for)
target_compile_options(iri2016 PRIVATE ${FFLAGS} -w)
# ---
add_executable(iri2016_driver iri2016_driver.F90)
target_link_libraries(iri2016_driver PRIVATE iri2016 ${FLIBS})
target_compile_options(iri2016_driver PRIVATE ${FFLAGS})
set_target_properties(iri2016_driver PROPERTIES 
                      COMPILE_DEFINITIONS BIN_DIR='${CMAKE_CURRENT_BINARY_DIR}')

add_executable(testiri2016 test.f90)
target_link_libraries(testiri2016 PRIVATE iri2016 ${FLIBS})
target_compile_options(testiri2016 PRIVATE ${FFLAGS})
add_test(NAME IRI2016 COMMAND testiri2016 
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../iri2016)

