import os
from cpt.packager import ConanMultiPackager


def build_conf(multi_options, **kw):
    items = []
    for options in multi_options:
        builder = ConanMultiPackager()
        builder.add_common_builds(pure_c=False, shared_option_name=False)
        builder.update_build_if(lambda x: True, new_options=options)
        items.extend(builder.items)
    return items


def filter_conf(cfg, items):
    def f(build):
        if not cfg["build_static"] and build.options["libigl:static_library"]:
            return False
        if not cfg["build_libcxx"] and build.settings["compiler.libcxx"] == "libstdc++":
            return False
        if not cfg["build_libcxx11"] and build.settings["compiler.libcxx"] in ("libstdc++11", "libc++"):
            return False
        return True
    return filter(f, items)


if __name__ == "__main__":
    cfg = {
        "build_static": False,
        "build_libcxx11": False,
        "build_libcxx": False,
    }

    env = os.environ
    if env.get("PACKAGE_BUILD_STATIC_LIB") == "1":
        cfg["build_static"] = True
        cfg["build_libcxx11"] = env.get("PACKAGE_BUILD_LIBCXX11_ABI") == "1"
        cfg["build_libcxx"] = env.get("PACKAGE_BUILD_LIBCXX_ABI") == "1"

    options = [
        {"libigl:static_library": False},
        {"libigl:static_library": True},
    ]
    builder = ConanMultiPackager()
    builder.items = filter_conf(
        cfg,
        items=build_conf(multi_options=options,
                         pure_c=False,
                         shared_options_name=False))
    builder.run()
