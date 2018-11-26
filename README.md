# conan-libigl

A conan package for [libigl](https://libigl.github.io/).

## Options

- `static_library` (default: **False**)

If the package version is the special one **git** this version is also supported:

- `commit_id` (default: **""**)

### static_library

libigl can be compiled as a static library to reduce the compile times of your projects,
this option controls such behavior.

### commit_id

This option controls which commit is used to produces the package, by default it is the **current HEAD**.