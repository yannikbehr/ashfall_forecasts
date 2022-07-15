import pkg_resources


def get_data(filename):
    return pkg_resources.resource_filename(__name__, filename)