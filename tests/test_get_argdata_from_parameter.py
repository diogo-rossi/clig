import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../src"))
from clig import get_argdata_from_parameter, ArgumentData, Kind


def test_metadata_without_annotation():
    def foo(a):
        pass

    parameter = inspect.signature(foo).parameters["a"]
    argmetadata = get_argdata_from_parameter(parameter)
    assert argmetadata == ArgumentData(name="a", kind=Kind.POSITIONAL_OR_KEYWORD)
