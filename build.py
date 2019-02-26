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
        if not cfg["build_static"] and not build.options["libigl:static_library"]:
            return True
        if cfg["build_static"] and build.options["libigl:static_library"]:
            return True
        return False
    return filter(f, items)


if __name__ == "__main__":
    env = os.environ
    cfg = {
        "build_static": env.get("PACKAGE_BUILD_STATIC_LIB") == "1",
    }

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
