cmake_minimum_required(VERSION 3.1)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(iri2016 Fortran)
enable_testing()

add_subdirectory(src)

add_executable(iri2016_driver src/iri2016_driver.f90)
target_link_libraries(iri2016_driver PRIVATE iri2016)

add_executable(testiri2016 src/test.f90)
target_link_libraries(testiri2016 PRIVATE iri2016)
add_test(NAME IRI2016 COMMAND testiri2016
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set_tests_properties(IRI2016 PROPERTIES TIMEOUT 15)
