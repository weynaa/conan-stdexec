cmake_minimum_required(VERSION 3.21)
project(PackageTest CXX)
find_package(STDEXEC REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example PRIVATE STDEXEC::stdexec)

if(TARGET STDEXEC::system_context)
    target_link_libraries(example PRIVATE STDEXEC::system_context)
else()
    target_compile_definitions(example PRIVATE STDEXEC_SYSTEM_CONTEXT_HEADER_ONLY)
endif()
