cmake_minimum_required(VERSION 3.1)
project(iri2016 Fortran)
enable_testing()

if(CMAKE_BUILD_TYPE STREQUAL Debug)
  add_compile_options(-g -O0)
else()
  add_compile_options(-O3)
endif()

if(${CMAKE_Fortran_COMPILER_ID} STREQUAL GNU)
  list(APPEND FFLAGS -mtune=native -ffpe-trap=invalid,zero,overflow)
  # -fdefault-real-8 -fno-align-commons)
elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Intel)

elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL PGI)

elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Flang)
  list(APPEND FFLAGS -Mallocatable=03)
  list(APPEND FLIBS -static-flang-libs)
endif()

add_library(iri2016 irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for)
target_compile_options(iri2016 PRIVATE ${FFLAGS})
target_link_libraries(iri2016 PRIVATE ${FLIBS})
# ---
add_executable(iri2016_driver iri2016_driver.f90)
target_link_libraries(iri2016_driver PRIVATE iri2016 ${FLIBS})
target_compile_options(iri2016_driver PRIVATE ${FFLAGS})

add_executable(testiri2016 test.f90)
target_link_libraries(testiri2016 PRIVATE iri2016 ${FLIBS})
target_compile_options(testiri2016 PRIVATE ${FFLAGS})
add_test(NAME IRI2016 COMMAND testiri2016 
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../iri2016)

