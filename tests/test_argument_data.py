# cSpell: disable
import sys
from pathlib import Path

this_dir = Path(__file__).parent

sys.path.insert(0, str((this_dir).resolve()))
sys.path.insert(0, str((this_dir / "../src").resolve()))

from clig import Command, ArgumentData, normalize_docstring, EMPTY
import resource_functions as funcs


def test_argumentdata_simple():
    cmd = Command(funcs.posNoType_kwNoType)
    arg_1, arg_2 = cmd.argument_data
    assert arg_1 == ArgumentData("first")
    assert arg_2 == ArgumentData("second", type=str, default="test")


def test_argumentdata_with_types():
    cmd = Command(funcs.posNoType_poslWithType_kwWithType)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert arg_a == ArgumentData("a")
    assert arg_b == ArgumentData("b", type=float)
    assert arg_c == ArgumentData("c", type=int, default=123)


def test_argumentdata_with_types_and_helps():
    cmd = Command(funcs.posWithType_kwWithType_kwBoolWithType_cligDocMultiline)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert arg_a == ArgumentData("a", type=str, help="Dicta et optio dicta.")
    assert arg_b == ArgumentData("b", type=int, default=123, help="Dolorum voluptate voluptas nisi.")
    assert arg_c == ArgumentData(
        "c",
        type=bool,
        default=True,
        help=normalize_docstring(
            """Asperiores quisquam odit voluptates et eos incidunt. Maiores minima provident doloremque aut
            dolorem. Minus natus ab voluptatum totam in. Natus consectetur modi similique rerum excepturi
            delectus aut."""
        ),
    )


def test_argumentdata_with_types_and_metadata():
    cmd = Command(funcs.posWithMetadataWithFlags_posWithMetadata_kwBool)
    arga, argb, argc = cmd.argument_data
    assert arga == ArgumentData(
        name="a",
        default=EMPTY,
        type=str,
        help=None,
        make_flag=None,
        argument_group=None,
        mutually_exclusive_group=None,
        flags=["-f", "--first"],
        kwargs={"help": "The first argument"},
    )
    assert argb == ArgumentData("b", flags=[], type=int, kwargs={"action": "store_const", "const": 123})
    assert argc == ArgumentData(
        "c",
        flags=[],
        type=bool,
        default=True,
    )
