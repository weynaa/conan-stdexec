from conan import ConanFile
from conan.tools.build.cppstd import check_min_cppstd
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy, rmdir
from conan.tools.scm import Git

import os

class StdexecPackage(ConanFile):
    name = "stdexec"
    description = "Experimental Reference implementation of P2300 std::execution"
    author = "Michał Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach"
    topics = ("WG21", "concurrency")
    homepage = "https://github.com/NVIDIA/stdexec"
    url = "https://github.com/NVIDIA/stdexec"
    license = "Apache 2.0"

    settings = "os", "arch", "compiler", "build_type"

    generators = "CMakeToolchain"

    options = {
        "header_only": [False, True],
    }

    default_options = {
        "header_only": True,
    }

    def validate(self):
        check_min_cppstd(self, "20")

    def layout(self):
        cmake_layout(self)

    def source(self):
        git = Git(self)
        git.clone(url=self.conan_data["sources"][self.version]["url"], target=".")
        git.checkout(commit=self.conan_data["sources"][self.version]["commit"])

    def build(self):
        build_tests = not self.conf.get("tools.build:skip_test", default=False)

        cmake = CMake(self)
        cmake.configure(variables={
            "STDEXEC_BUILD_TESTS": build_tests,
            "STDEXEC_BUILD_EXAMPLES": build_tests,
        })
        cmake.build()
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
        copy(self, "license*", self.source_folder, os.path.join(self.package_folder, "licenses"))

        rmdir(self, os.path.join(self.package_folder,"lib","cmake"))
        if (self.options.header_only):
            rmdir(self, os.path.join(self.package_folder,"lib"))

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
        if (not self.options.header_only):
            self.cpp_info.components["system_context"].set_property(
                "cmake_target_name", "STDEXEC::system_context")
            self.cpp_info.components["system_context"].libs = [
                "system_context"]
            self.cpp_info.components["system_context"].requires = ["stdexec"]
