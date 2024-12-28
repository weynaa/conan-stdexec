from conan import ConanFile
from conan.tools.build.cppstd import check_min_cppstd
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Git

import os

class StdexecPackage(ConanFile):
    name = "stdexec"
    description = "Implementation of P2300 std::execution"
    author = "Michał Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach"
    topics = ("WG21", "concurrency")
    homepage = "https://github.com/NVIDIA/stdexec"
    url = "https://github.com/NVIDIA/stdexec"
    license = "Apache 2.0"

    settings = "os", "arch", "compiler", "build_type"

    generators = "CMakeToolchain"

    options = {
        "shared": [False, True],
    }

    default_options = {
        "shared": False
    }

    def validate(self):
        check_min_cppstd(self, "20")

    def layout(self):
        cmake_layout(self)

    def source(self):
        git = Git(self)
        git.clone(url=self.conan_data[self.version]["url"], target=".")
        git.checkout(commit=self.conan_data[self.version]["commit"])

    def build(self):
        tests = "OFF" if self.conf.get(
            "tools.build:skip_test", default=False) else "ON"

        cmake = CMake(self)
        cmake.configure(variables={
            "STDEXEC_BUILD_TESTS": tests,
            "STDEXEC_BUILD_EXAMPLES": tests,
        })
        cmake.build()
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_package", "STDEXEC")
        self.cpp_info.components["stdexec"].set_property(
            "cmake_target_name", "STDEXEC::stdexec")

        if (self.settings.compiler == "msvc"):
            self.cpp_info.components["stdexec"].cxxflags = [
                "/Zc:__cplusplus", "/Zc:preprocessor"]
        elif (self.settings.compiler == "gcc"):
            self.cpp_info.components["stdexec"].cxxflags = ["-fcoroutines",
                                                            "-fconcepts-diagnostics-depth=10"]

        self.cpp_info.components["system_context"].set_property(
            "cmake_target_name", "STDEXEC::system_context")
        self.cpp_info.components["system_context"].libs = ["system_context"]
        self.cpp_info.components["system_context"].requires = ["stdexec"]
