import pytest
from resources import CapSys
from clig import Arg, data, run
from argparse import ArgumentParser


def test_intg_07_nargs():
    def bar(name: str, size: Arg[float, data(nargs="?", const=456)]):
        return locals()

    assert run(bar, ["rocky"]) == {"name": "rocky", "size": None}
    assert run(bar, ["rocky", "1.5"]) == {"name": "rocky", "size": 1.5}


def test_pos_with_required(capsys: CapSys):
    with pytest.raises(TypeError) as e:
        parser = ArgumentParser()
        parser.add_argument("name")
        parser.add_argument("size", nargs="?", const=456, required=True)

    assert "'required' is an invalid argument for positionals" in e.value.args[0]

    def foo(name: str, size: Arg[float, data(nargs="?", const=456, required=True)]): ...

    with pytest.raises(TypeError) as e:
        run(foo, ["rocky"])

    assert "'required' is an invalid argument for positionals" in e.value.args[0]
