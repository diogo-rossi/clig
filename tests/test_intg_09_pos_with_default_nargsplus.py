import pytest
from argparse import ArgumentParser
from resources import CapSys
from clig import Arg, data, run

error_msg = """
usage: main [-h] name [name ...]
main: error: the following arguments are required: name
""".strip()


def main(name: Arg[list[str], data(default="diogo")]):
    return locals()


parser = ArgumentParser()
parser.add_argument("name", default="diogo", nargs="+")


def test_intg_09_pos_with_default(capsys: CapSys):
    with pytest.raises(SystemExit) as e:
        run(main, [])
    assert e.value.code == 2
    output = capsys.readouterr().err
    assert error_msg in output
    assert run(main, ["rocky", "sandy"]) == {"name": ["rocky", "sandy"]}
    assert run(main, ["rocky", "sandy"]) == vars(parser.parse_args(["rocky", "sandy"]))
