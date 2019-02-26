# conan-libigl

A conan package for [libigl](https://libigl.github.io/).

## Options

- `static_library` (default: **False**)
- `commit_id` (default: **""**)

### static_library

libigl can be compiled as a static library to reduce the compile times of your projects,
this option controls such behavior.

### commit_id

This option exists only for the **git** version of this package, and it
controls which commit is used to build the package; the default is the
**current HEAD**.
