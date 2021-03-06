import os
import subprocess
from conans import ConanFile, CMake, tools
from contextlib import contextmanager

@contextmanager
def chdir(d):
    curr = os.getcwd()
    os.chdir(d)
    yield
    os.chdir(curr)


class LibiglConan(ConanFile):
    name = "libigl"
    version = "0.1"
    license = "MPL2"

    author = "dvd <dvd+conan@gnx.it>"
    url = "https://gitlab.com/dvd0101/conan-libigl"
    commit_id = "3cb4894eaf8ea4610467189ca292be349425d44b"

    homepage = "https://libigl.github.io/"
    description = """libigl is a simple C++ geometry processing library.

We have a wide functionality including construction of sparse discrete
differential geometry operators and finite-elements matrices such as the
cotangent Laplacian and diagonalized mass matrix, simple facet and edge-based
topology data structures, mesh-viewing utilities for OpenGL and GLSL, and many
core functions for matrix manipulation which make Eigen feel a lot more like
MATLAB."""
    topics = ("geometry", "matrices", "algorithms")

    settings = "os", "compiler", "build_type", "arch"
    options = {"static_library": [True, False]}
    default_options = {"static_library": False}

    generators = "cmake"

    requires = ("eigen/3.3.7@d3d/testing",)

    exports = "fix_static_build.patch", "fix_cmake_install.patch"

    def source(self):
        git = tools.Git(folder="libigl")
        git.clone("https://github.com/libigl/libigl.git")
        git.checkout(self.commit_id)
        print("using commit:", git.get_commit())

        # this fix enable the static build on 32bit target where sizeof(size_t)
        # != sizeof(unsigned int)
        # The bug is in the explicit instantiation of some template functions
        # that does not perfectly match their declarations (but this is
        # a no issue on a 64bit platform because the two types are the same ).
        # self._fix_static_build()

        # this fix the install procedure; cmake is instructed to install only
        # the headers file ending with `.h` while there are some with the
        # `.hpp` extension
        # self._fix_cmake_install()

        # self._patch_cmake_project()

    def _fix_static_build(self):
        patch = open("fix_static_build.patch", mode="rb")
        with chdir("libigl"):
            subprocess.run(args=["patch", "-p1"],
                           input=patch.read())

    def _fix_cmake_install(self):
        patch = open("fix_cmake_install.patch", mode="rb")
        with chdir("libigl"):
            subprocess.run(args=["patch", "-p1"],
                           input=patch.read())

    def _patch_cmake_project(self):
        with chdir("libigl"):
            tools.replace_in_file("CMakeLists.txt",
                                  "project(libigl)",
                                  """project(libigl)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
# libIGL must find the Eigen3 library imported by conan
# otherwise it downloads a own copy from internet
find_package(Eigen3 REQUIRED) """)

    def _configure_cmake(self):
        cmake = CMake(self)

        if self.develop:
            cmake.verbose = True

        if self.options.static_library:
            cmake.definitions["LIBIGL_USE_STATIC_LIBRARY"] = "ON"
        else:
            cmake.definitions["LIBIGL_USE_STATIC_LIBRARY"] = "OFF"

        # All these dependencies are needed to build the examples or the tests
        cmake.definitions["LIBIGL_BUILD_TUTORIALS"] = "OFF"
        cmake.definitions["LIBIGL_BUILD_TESTS"] = "OFF"
        cmake.definitions["LIBIGL_BUILD_PYTHON"] = "OFF"

        cmake.definitions["LIBIGL_WITH_CGAL"] = "OFF"
        cmake.definitions["LIBIGL_WITH_COMISO"] = "OFF"
        cmake.definitions["LIBIGL_WITH_CORK"] = "OFF"
        cmake.definitions["LIBIGL_WITH_EMBREE"] = "OFF"
        cmake.definitions["LIBIGL_WITH_MATLAB"] = "OFF"
        cmake.definitions["LIBIGL_WITH_MOSEK"] = "OFF"
        cmake.definitions["LIBIGL_WITH_OPENGL"] = "OFF"
        cmake.definitions["LIBIGL_WITH_OPENGL_GLFW"] = "OFF"
        cmake.definitions["LIBIGL_WITH_OPENGL_GLFW_IMGUI"] = "OFF"
        cmake.definitions["LIBIGL_WITH_PNG"] = "OFF"
        cmake.definitions["LIBIGL_WITH_TETGEN"] = "OFF"
        cmake.definitions["LIBIGL_WITH_TRIANGLE"] = "OFF"
        cmake.definitions["LIBIGL_WITH_XML"] = "OFF"
        cmake.definitions["LIBIGL_WITH_PYTHON"] = "OFF"

        cmake.configure(source_folder="libigl")
        return cmake

    def build(self):
        make = self._configure_cmake()
        make.build()

    def package(self):
        make = self._configure_cmake()
        make.install()

    def package_info(self):
        self.cpp_info.cppflags = ["-pthread"]

        if self.options.static_library:
            self.cpp_info.libdirs = ["lib"]
            self.cpp_info.libs = ["libigl.a"]
            self.cpp_info.cppflags += ["-DIGL_STATIC_LIBRARY"]
