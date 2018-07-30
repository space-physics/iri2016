cmake_minimum_required(VERSION 3.7)
project(iri2016 Fortran)
enable_testing()

if(CMAKE_BUILD_TYPE STREQUAL Debug)
  add_compile_options(-g -O0)
else()
  add_compile_options(-O3)
endif()

if(${CMAKE_Fortran_COMPILER_ID} STREQUAL GNU)
  list(APPEND FFLAGS -mtune=native -ffpe-trap=invalid,zero,overflow -fbacktrace)
  # -fdefault-real-8 -fno-align-commons)
elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Intel)

elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL PGI)
  list(APPEND FFLAGS -Mallocatable=03)
elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Flang)
  list(APPEND FFLAGS -Mallocatable=03)
  link_libraries(-static-flang-libs)
endif()


# ---
add_executable(testiri2016 irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for test.f90)
add_test(NAME IRI2016 COMMAND testiri2016 WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../iri2016)

