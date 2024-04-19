import os
import theia


def package_dir():
    return os.path.dirname(theia.__file__) + "/"


def upload_dir(filename):
    return package_dir() + "web/uploads/" + filename
