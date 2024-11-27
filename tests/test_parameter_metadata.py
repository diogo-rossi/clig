import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../src"))
import clig


def test_metadata_without_annotation():
    def foo(a):
        pass

    parameter = inspect.signature(foo).parameters["a"]
    argmetadata = clig.get_argdata_from_parameter(parameter)
    assert argmetadata == clig.ArgumentData(name="a", kind=inspect._ParameterKind.POSITIONAL_OR_KEYWORD)
