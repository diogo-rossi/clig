import pytest
from resources import CapSys
from clig import ArgumentGroup, Arg, data, run, MutuallyExclusiveGroup

helpmsg = """
usage: foo [-h] [--age AGE | --height HEIGHT] teste name

positional arguments:
  teste

options:
  -h, --help       show this help message and exit

my group:
  this is my group

  name             help for name argument
  --age AGE        help for age argument
  --height HEIGHT  help for height argument"""


def foo(
    teste: str,
    name: Arg[
        str,
        data(
            group=(g := ArgumentGroup("my group", description="this is my group")),
            help="help for name argument",
        ),
    ],
    age: Arg[
        int, data(group=(m := MutuallyExclusiveGroup(argument_group=g)), help="help for age argument")
    ] = 32,
    height: Arg[float, data(group=m, help="help for height argument")] = 32.6,
):
    return locals()


def test_intg_06_groups(capsys: CapSys):
    with pytest.raises(SystemExit) as e:
        run(foo, ["--help"])
    assert e.value.code == 0
    assert helpmsg.strip() in capsys.readouterr().out
    assert run(foo, "jaspion opa --height 1.75".split()) == {
        "teste": "jaspion",
        "name": "opa",
        "age": 32,
        "height": 1.75,
    }
