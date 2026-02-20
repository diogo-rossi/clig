from clig.clig import _get_pkg_version


import git
import PIL.Image
import yaml
import pytest


def test_get_git_version():
    pkg, ver, deep_search = _get_pkg_version(func=git.refresh, return_pkg_name=True)
    assert deep_search == True
    assert pkg == "GitPython"
    assert ver == git.__version__


def test_get_pil_version():
    pkg, ver, deep_search = _get_pkg_version(func=PIL.Image.open, return_pkg_name=True)
    assert deep_search == True
    assert pkg == "pillow"
    assert ver == PIL.Image.__version__


def test_get_yaml_version():
    pkg, ver, deep_search = _get_pkg_version(func=yaml.add_constructor, return_pkg_name=True)
    assert deep_search == True
    assert pkg == "PyYAML"
    assert ver == yaml.__version__


def test_get_pytestl_version():
    pkg, ver, deep_search = _get_pkg_version(func=pytest.approx, return_pkg_name=True)
    assert deep_search == True
    assert pkg == "pytest"
    assert ver == pytest.__version__
