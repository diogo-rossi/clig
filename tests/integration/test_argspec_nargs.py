import sys
from pathlib import Path

path = Path(__file__).parent
sys.path.insert(0, str((path).resolve()))
sys.path.insert(0, str((path / "../../src").resolve()))

from argparse import ArgumentParser
from clig import Command, Arg, data
from clig import clig


def test_nargs_questionMark_nonDefault():
    """Ref: https://docs.python.org/3/library/argparse.html#nargs"""

    # original behavior

    parser = ArgumentParser("foo")
    parser.add_argument(dest="name")
    parser.add_argument(dest="size", nargs="?", type=int)

    args = parser.parse_args(["rocky", "123"])  # positional passed
    assert {"name": args.name, "size": args.size} == {"name": "rocky", "size": 123}

    args = parser.parse_args(["rocky"])  # not passed, produce default = None
    assert {"name": args.name, "size": args.size} == {"name": "rocky", "size": None}

    # test of lib

    def foo(name: str, size: Arg[float, data(nargs="?")]):
        return locals()

    assert clig.run(foo, ["rocky", "123"]) == {"name": "rocky", "size": 123}  # positional passed
    assert clig.run(foo, ["rocky"]) == {"name": "rocky", "size": None}  # not passed, produce default = None


def test_nargs_questionMark_default():
    """Ref: https://docs.python.org/3/library/argparse.html#nargs"""

    # original behavior

    parser = ArgumentParser("foo")
    parser.add_argument(dest="name")
    parser.add_argument("--size", dest="size", const=456, default=789, nargs="?", type=int)

    args = parser.parse_args(["rocky", "--size", "123"])  # optional passed
    assert {"name": args.name, "size": args.size} == {"name": "rocky", "size": 123}

    args = parser.parse_args(["rocky", "--size"])  # pass no value produce const
    assert {"name": args.name, "size": args.size} == {"name": "rocky", "size": 456}

    args = parser.parse_args(["rocky"])  # not passed, produce default
    assert {"name": args.name, "size": args.size} == {"name": "rocky", "size": 789}

    # test of lib

    def bar(name: str, size: Arg[float, data(nargs="?", const=456)] = 789):
        return locals()

    assert clig.run(bar, ["rocky", "--size", "123"]) == {"name": "rocky", "size": 123}  # optional passed
    assert clig.run(bar, ["rocky", "--size"]) == {"name": "rocky", "size": 456}  # pass no value produce const
    assert clig.run(bar, ["rocky"]) == {"name": "rocky", "size": 789}  # not passed, produce default
