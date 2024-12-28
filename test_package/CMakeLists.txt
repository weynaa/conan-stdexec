cmake_minimum_required(VERSION 3.21)
project(PackageTest CXX)
find_package(STDEXEC REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example PRIVATE STDEXEC::stdexec STDEXEC::system_context)
