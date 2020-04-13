cmake_minimum_required(VERSION 3.13)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(iri2016
LANGUAGES Fortran
DESCRIPTION "IRI2016 command line driver"
HOMEPAGE_URL https://github.com/space-physics/iri2016)
enable_testing()

include(CheckFortranCompilerFlag)
check_fortran_compiler_flag(-w nowarn)

set(OLD_FLAGS)
if(nowarn)
  set(OLD_FLAGS "-w")
endif()

if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  string(APPEND CMAKE_Fortran_FLAGS " -std=legacy -static")
elseif(CMAKE_Fortran_COMPILER_ID STREQUAL Intel)
  string(APPEND CMAKE_Fortran_FLAGS " -static-intel")
endif()

add_subdirectory(src)

add_executable(iri2016_driver src/iri2016_driver.f90)
target_link_libraries(iri2016_driver iri2016)

add_executable(test_iri2016 src/test.f90)
target_link_libraries(test_iri2016 iri2016)
add_test(NAME IRI2016 COMMAND test_iri2016
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set_tests_properties(IRI2016 PROPERTIES TIMEOUT 15)
