cmake_minimum_required(VERSION 3.13)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(iri2016
LANGUAGES Fortran
DESCRIPTION "IRI2016 command line driver"
HOMEPAGE_URL https://github.com/space-physics/iri2016)
enable_testing()

# --- compiler options

include(CheckFortranCompilerFlag)
include(CheckFortranSourceCompiles)
check_fortran_compiler_flag(-w nowarn)

set(OLD_FLAGS)
if(nowarn)
  set(OLD_FLAGS "-w")
endif()

if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  set(CMAKE_REQUIRED_FLAGS -static)
  check_fortran_source_compiles("end" static_ok SRC_EXT f90)

  string(APPEND CMAKE_Fortran_FLAGS " -std=legacy")
  if(static_ok)
    string(APPEND CMAKE_Fortran_FLAGS " -static")
  endif()

elseif(CMAKE_Fortran_COMPILER_ID STREQUAL Intel)
  set(CMAKE_REQUIRED_FLAGS -static-intel)
  check_fortran_source_compiles("end" static_ok SRC_EXT f90)
  if(static_ok)
    string(APPEND CMAKE_Fortran_FLAGS " -static-intel")
  endif()
endif()

# --- main program

add_subdirectory(src)

add_executable(iri2016_driver src/iri2016_driver.f90)
target_link_libraries(iri2016_driver iri2016)
set_target_properties(iri2016_driver PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(test_iri2016 src/test.f90)
target_link_libraries(test_iri2016 iri2016)
add_test(NAME IRI2016
  COMMAND $<TARGET_FILE:test_iri2016>
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set_tests_properties(IRI2016 PROPERTIES TIMEOUT 15)
