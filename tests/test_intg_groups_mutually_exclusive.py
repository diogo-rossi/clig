import pytest
from resources import CapSys
from clig import Command, Arg, data, MutuallyExclusiveGroup


def test_groups_mutually_exclusive_noRequired(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=False)

    def main(foo: Arg[str, data(group=g)] = "test", bar: Arg[int, data(group=g)] = 0):
        return locals()

    with pytest.raises(SystemExit) as e:
        Command(main).run("--foo rocky --bar 42".split())

    assert e.value.code == 2  # argparse exits with code 2 for argument errors
    output = capsys.readouterr().err
    assert "argument --bar: not allowed with argument --foo" in output
    assert Command(main).run([]) == {"foo": "test", "bar": 0}
    assert Command(main).run("--foo rocky".split()) == {"foo": "rocky", "bar": 0}
    assert Command(main).run("--bar 32".split()) == {"foo": "test", "bar": 32}


def test_groups_mutually_exclusive_required(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=True)

    def main(foo: Arg[str, data(group=g)] = "test", bar: Arg[int, data(group=g)] = 0):
        return locals()

    with pytest.raises(SystemExit) as e:
        Command(main).run([])

    assert e.value.code == 2  # argparse exits with code 2 for argument errors
    output = capsys.readouterr().err
    assert "one of the arguments --foo --bar is required" in output
    assert Command(main).run("--foo rocky".split()) == {"foo": "rocky", "bar": 0}
    assert Command(main).run("--bar 32".split()) == {"foo": "test", "bar": 32}
