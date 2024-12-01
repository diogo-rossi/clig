# cSpell: disable
import inspect
import sys
from pathlib import Path

this_dir = Path(__file__).parent

sys.path.insert(0, str((this_dir).resolve()))
sys.path.insert(0, str((this_dir / "../src").resolve()))

from clig import get_argdata_from_parameter, ArgumentData, Kind
import resource_functions as funcs


def test_metadata_without_annotation():
    parameter = inspect.signature(funcs.posNoType).parameters["a"]
    argmetadata = get_argdata_from_parameter(parameter)
    assert argmetadata == ArgumentData(name="a", kind=Kind.POSITIONAL_OR_KEYWORD)
