from resources import CapSys
from clig import Command

helpmsg = """usage: main [-h] name age height {second} ...

The main command

positional arguments:
  name        The name of the person
  age         The age of the person
  height      The height of the person

options:
  -h, --help  show this help message and exit

subcommands:
  {second}
    second    A function witout arguments

This is my main command"""


@Command
def main(name: str, age: int, height: float):
    """The main command

    This is my main command

    Args:
        name: The name of the person
        age: The age of the person
        height: The height of the person
    """
    print(locals())


def second():
    """A function witout arguments

    This functions runs without arguments
    """
    print(locals())


subcmd = main.new_subcommand(second)


def test_intg_00_random(capsys: CapSys):
    main.print_help()
    output = capsys.readouterr().out
    assert helpmsg in output
