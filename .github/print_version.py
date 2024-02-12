import pkg_resources  # part of setuptools

version = pkg_resources.require("yinstruments")[0].version
print(version)
