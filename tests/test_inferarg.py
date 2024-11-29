# cSpell: disable
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

    assert cmd.inferarg(arg_1) == (
        (),
        CompleteKeywordArguments(
            action="store", dest="first", type=str, default=None, nargs=None, choices=None, help=None
        ),
    )
    assert cmd.inferarg(arg_2) == (
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

    assert cmd.inferarg(arg_a) == (
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
    assert cmd.inferarg(arg_b) == (
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
    assert cmd.inferarg(arg_c) == (
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


def test_inferarg_with_types_and_helps():
    def foo(a: str, b: int = 123, c: bool = True):
        """Reprehenderit unde commodi doloremque rerum ducimus quam accusantium.

        Qui quidem quo eligendi officia ea quod ab tempore esse. Sapiente quasi est sint. Molestias et
        laudantium quidem laudantium animi voluptate asperiores illum. Adipisci tempora nesciunt dolores
        tempore consequatur amet. Aut ipsa ex.

        Parameters
        ----------
        - `a` (`str`):
            Dicta et optio dicta.

        - `b` (`int`, optional): Defaults to `123`.
            Dolorum voluptate voluptas nisi.

        - `c` (`bool`, optional): Defaults to `True`.
            Asperiores quisquam odit voluptates et eos incidunt. Maiores minima provident doloremque aut
            dolorem. Minus natus ab voluptatum totam in. Natus consectetur modi similique rerum excepturi
            delectus aut.

        """
        pass

    cmd = Command(foo)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert arg_a == ArgumentData("a", type=str, help="Dicta et optio dicta.")
    assert arg_b == ArgumentData("b", type=int, default=123, help="Dolorum voluptate voluptas nisi.")
    # TODO: multi line parameter description
    assert arg_c == ArgumentData(
        "c",
        type=bool,
        default=True,
        help="""Asperiores quisquam odit voluptates et eos incidunt. Maiores minima provident doloremque aut
            dolorem. Minus natus ab voluptatum totam in. Natus consectetur modi similique rerum excepturi
            delectus aut.""",
    )
