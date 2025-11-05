##############################################################################################################
# %%          Add `<root>/src` to sys.path
##############################################################################################################

import sys
from pathlib import Path

path = Path(__file__).parent
sys.path.insert(0, str((path).resolve()))
sys.path.insert(0, str((path / "../../src").resolve()))

##############################################################################################################
# %%          Resources
##############################################################################################################
import pytest
from typing import Protocol


class OutErr(Protocol):
    out: str
    err: str


class CapSys(Protocol):
    def readouterr(self) -> OutErr: ...


##############################################################################################################
# %%          Testing
##############################################################################################################


from clig import Command, Arg, data, run


def test_list_withDefault_turnsIntoNargsStar():
    def main(names: Arg[list[str], data(default="rocky")] = []):
        return locals()

    assert Command(main).run(["--names", "tony", "neo"]) == {"names": ["tony", "neo"]}
    assert Command(main).run([]) == {"names": "rocky"}


def test_tuple_withDefault_turnsIntoNargsStar():
    def main(names: Arg[tuple[str, ...], data(default=("rocky",))] = ()):
        return locals()

    assert Command(main).run(["--names", "tony", "neo"]) == {"names": ("tony", "neo")}
    assert Command(main).run([]) == {"names": ("rocky",)}


def test_list_defaultOnData_noDefaultOnFunction_turnsIntoNargsPlus(capsys: CapSys):
    def main(names: Arg[list[str], data(default="rocky")]):
        return locals()

    assert Command(main).run(["tony", "neo"]) == {"names": ["tony", "neo"]}

    with pytest.raises(SystemExit) as e:
        Command(main).run([])

    assert e.value.code == 2  # argparse exits with code 2 for argument errors
    output = capsys.readouterr().err
    assert "the following arguments are required: names" in output


def test_tuple_defaultOnData_noDefaultOnFunction_turnsIntoNargsN(capsys: CapSys):
    def main(names: Arg[tuple[str, str], data(default="rocky")]):
        return locals()

    assert Command(main).run(["tony", "neo"]) == {"names": ("tony", "neo")}

    with pytest.raises(SystemExit) as e:
        Command(main).run([])

    assert e.value.code == 2  # argparse exits with code 2 for argument errors
    output = capsys.readouterr().err

    assert "the following arguments are required: name" in output


def test_union_tuple_none_withDefaultNone():
    def foo(ages: tuple[int, int] | None = None):
        return locals()

    assert Command(foo).run(["--ages", "36", "64"]) == {"ages": (36, 64)}
    assert Command(foo).run([]) == {"ages": None}


def test_union_list_none_withDefaultNone():
    def foo(ages: list[int] | None = None):
        return locals()

    assert Command(foo).run(["--ages", "36", "64", "42"]) == {"ages": [36, 64, 42]}
    assert Command(foo).run([]) == {"ages": None}
