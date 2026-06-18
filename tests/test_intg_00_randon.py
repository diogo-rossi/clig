from resources import CapSys
from clig import Command

helpmsg_default_section = """
usage: main [-h] name age height {second} ...

The main command

positional arguments:
  name        The name of the person
  age         The age of the person
  height      The height of the person
  {second}
    second    A function witout arguments

options:
  -h, --help  show this help message and exit

This is my main command""".strip()

helpmsg_subcommands_section = """
usage: main [-h] name age height {second} ...

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

This is my main command""".strip()


@Command
def main(name: str, age: int, height: float):
    """The main command

    This is my main command

    Args:
        name: The name of the person
        age: The age of the person
        height: The height of the person
    """
    return locals()


def second():
    """A function witout arguments

    This functions runs without arguments
    """
    return locals()


def test_intg_00_random(capsys: CapSys):
    main.new_subcommand(second)
    main.print_help()
    output = capsys.readouterr().out
    assert helpmsg_default_section in output
    assert main.run(["ghost", "10", "1.50"]) == {"name": "ghost", "age": 10, "height": 1.50}
    assert main.run(["ghost", "10", "1.50", "second"]) == {}


def test_intg_00_random_subcommands_section(capsys: CapSys):
    maincmd = Command(main.func, subcommands_title="subcommands")
    maincmd.new_subcommand(second)
    maincmd.print_help()
    output = capsys.readouterr().out
    assert helpmsg_subcommands_section in output
    assert maincmd.run(["ghost", "10", "1.50"]) == {"name": "ghost", "age": 10, "height": 1.50}
    assert maincmd.run(["ghost", "10", "1.50", "second"]) == {}
