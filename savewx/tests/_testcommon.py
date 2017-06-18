import os


def open_resource(file, *args, **kwargs):
    return open(os.path.join(os.path.dirname(__file__), file), *args, **kwargs)
