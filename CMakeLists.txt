cmake_minimum_required(VERSION 3.1)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(iri2016 Fortran)
enable_testing()

include(cmake/compilers.cmake)

add_subdirectory(src)

add_executable(iri2016_driver src/iri2016_driver.F90)
target_link_libraries(iri2016_driver PRIVATE iri2016 ${FLIBS})
target_compile_options(iri2016_driver PRIVATE ${FFLAGS})
target_compile_definitions(iri2016_driver PRIVATE BIN_DIR='${CMAKE_CURRENT_BINARY_DIR}')

add_executable(testiri2016 src/test.f90)
target_link_libraries(testiri2016 PRIVATE iri2016 ${FLIBS})
target_compile_options(testiri2016 PRIVATE ${FFLAGS})
add_test(NAME IRI2016 COMMAND testiri2016)
