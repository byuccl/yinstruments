"""Check that the version in setup.py is greater than the latest version on PyPI."""

import ast
import sys
import urllib.request
import json
from packaging import version


def get_pypi_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return version.parse(data["info"]["version"])


def get_setup_version(setup_path):
    with open(setup_path) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "setup":
            for keyword in node.keywords:
                if keyword.arg == "version":
                    return version.parse(ast.literal_eval(keyword.value))
    raise RuntimeError(f"Could not find version in {setup_path}")


if __name__ == "__main__":
    setup_path = sys.argv[1] if len(sys.argv) > 1 else "../setup.py"

    pypi_ver = get_pypi_version("yinstruments")
    current_ver = get_setup_version(setup_path)

    print(f"PyPI version:    {pypi_ver}")
    print(f"Current version: {current_ver}")

    if current_ver <= pypi_ver:
        print("FAIL: Current version must be greater than the PyPI version.")
        sys.exit(1)

    print("OK: Version check passed.")
