from cpt.packager import ConanMultiPackager

def build_conf(multi_options, **kw):
    items = []
    for options in multi_options:
        builder = ConanMultiPackager()
        builder.add_common_builds(pure_c=False, shared_option_name=False)
        builder.update_build_if(lambda x: True, new_options=options)
        items.extend(builder.items)
    return items


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.items = build_conf(multi_options=[{"libigl:static_library": False}, {"libigl:static_library": True}],
                               pure_c=False,
                               shared_options_name=False)
    builder.run()
