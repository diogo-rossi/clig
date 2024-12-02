# cSpell: disable
import inspect
import sys
from pathlib import Path

this_dir = Path(__file__).parent

sys.path.insert(0, str((this_dir).resolve()))
sys.path.insert(0, str((this_dir / "../src").resolve()))

from clig import get_argdata_from_parameter, ArgumentData, Kind
import functions as fun


def test_parameter_without_annotation():
    parameter = inspect.signature(fun.posNoType).parameters["a"]
    argmetadata = get_argdata_from_parameter(parameter)
    assert argmetadata == ArgumentData(name="a", kind=Kind.POSITIONAL_OR_KEYWORD)


def test_get_argdata_from_parameter_posWithType_posBoolWithType_cligDoc():
    parameters = inspect.signature(fun.posWithType_posBoolWithType_cligDoc).parameters
    par_name, par_flag = parameters["name"], parameters["flag"]
    arg_data_par_name = get_argdata_from_parameter(par_name)
    arg_data_par_flag = get_argdata_from_parameter(par_flag)
    assert arg_data_par_name == ArgumentData(name="name", type=str)
    assert arg_data_par_flag == ArgumentData(name="flag", type=bool)
