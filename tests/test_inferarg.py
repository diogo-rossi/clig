import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../src"))
from clig import Command, ArgumentData, CompleteKeywordArguments


def test_inferarg_simple():
    def foo(first, second="test"):
        pass

    cmd = Command(foo)
    arg_1, arg_2 = cmd.argument_data
    assert arg_1 == ArgumentData("first")
    assert arg_2 == ArgumentData("second", type=str, default="test")

    assert cmd.inferfrom_argdata(arg_1) == (
        (),
        CompleteKeywordArguments(
            action="store", dest="first", type=str, default=None, nargs=None, choices=None, help=None
        ),
    )
    assert cmd.inferfrom_argdata(arg_2) == (
        ("--second",),
        CompleteKeywordArguments(
            action="store",
            dest="second",
            type=str,
            default="test",
            nargs=None,
            choices=None,
            help=None,
        ),
    )


def test_inferarg_with_types():
    def bar(a, b: float, c: int = 123):
        pass

    cmd = Command(bar)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert arg_a == ArgumentData("a")
    assert arg_b == ArgumentData("b", type=float)
    assert arg_c == ArgumentData("c", type=int, default=123)

    assert cmd.inferfrom_argdata(arg_a) == (
        (),
        CompleteKeywordArguments(
            action="store",
            dest="a",
            type=str,
            default=None,
            nargs=None,
            choices=None,
            help=None,
        ),
    )
    assert cmd.inferfrom_argdata(arg_b) == (
        (),
        CompleteKeywordArguments(
            action="store",
            dest="b",
            type=float,
            default=None,
            nargs=None,
            choices=None,
            help=None,
        ),
    )
    assert cmd.inferfrom_argdata(arg_c) == (
        ("--c",),
        CompleteKeywordArguments(
            action="store",
            dest="c",
            type=int,
            default=123,
            nargs=None,
            choices=None,
            help=None,
        ),
    )
