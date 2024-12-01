import inspect
from pathlib import Path
import sys

sys.path.insert(0, str((Path(__file__).parent / "../src").resolve()))
from clig import get_argdata_from_parameter, ArgumentData, Kind


def test_metadata_without_annotation():
    def foo(a):
        pass

    parameter = inspect.signature(foo).parameters["a"]
    argmetadata = get_argdata_from_parameter(parameter)
    assert argmetadata == ArgumentData(name="a", kind=Kind.POSITIONAL_OR_KEYWORD)
