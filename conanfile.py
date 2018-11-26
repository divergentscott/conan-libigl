import re
from conans import ConanFile, CMake, tools

COMMIT_ID = None

_package_version = COMMIT_ID if COMMIT_ID is not None else "git"
if COMMIT_ID and re.match(r"^v\d", _package_version):
    # COMMIT_ID is something like "v2.0.0"
    # I drop the 'v' so that the package name will be: libigl/2.0.0
    _package_version = COMMIT_ID[1:]

_package_options = {
    "static_library": [True, False],
}

_package_default_options = {
    "static_library": False,
}

if COMMIT_ID is None:
    _package_options.update({
        "commit_id": "ANY",
    })

    _package_default_options["commit_id"] = ""


class LibiglConan(ConanFile):
    name = "libigl"
    version = _package_version
    license = "MPL2"

    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"

    homepage = "https://libigl.github.io/"
    description = """libigl is a simple C++ geometry processing library.
                     We have a wide functionality including construction of sparse discrete differential
                     geometry operators and finite-elements matrices such as the cotangent Laplacian and
                     diagonalized mass matrix, simple facet and edge-based topology data structures,
                     mesh-viewing utilities for OpenGL and GLSL, and many core functions for matrix
                     manipulation which make Eigen feel a lot more like MATLAB."""
    topics = ("geometry", "matrices", "algorithms")

    settings = "os", "compiler", "build_type", "arch"
    options = _package_options
    default_options = _package_default_options

    # generators = "cmake"

    requires = ("eigen/3.3.5@conan/stable",)

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/libigl/libigl.git")

        cid = COMMIT_ID or self.options.commit_id
        if cid:
            git.checkout(COMMIT_ID)

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

        cmake.configure()
        return cmake

    def build(self):
        make = self._configure_cmake()
        make.build()

    def package(self):
        # self.copy("*.h", dst="include", src="include")
        # self.copy("*.cpp", dst="include", src="include")
        # self.copy("LICENSE*", dst="licenses")
        make = self._configure_cmake()
        make.install()

    def package_info(self):
        self.cpp_info.cppflags = ["-pthread"]
        if self.options.static_library:
            self.cpp_info.libs = ["libigl.a"]
            self.cpp_info.cppflags += ["-DIGL_STATIC_LIBRARY"]
