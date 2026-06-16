import pytest
from resources import CapSys


from clig import Command


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
    """A function with string"""
    return locals()


def third(other: int):
    """A function with int"""
    return locals()


default_help = """
usage: main [-h] name age height {third,second} ...

The main command

positional arguments:
  name            The name of the person
  age             The age of the person
  height          The height of the person

options:
  -h, --help      show this help message and exit

subcommands:
  {third,second}
    third         A function with int
    second        A function with string

This is my main command"""

help_with_subcommands_title = """
usage: main [-h] name age height {third,second} ...

The main command

positional arguments:
  name            The name of the person
  age             The age of the person
  height          The height of the person

options:
  -h, --help      show this help message and exit

:=== SUBCOMMANDS SECTION TITLE ===:
  {third,second}
    third         A function with int
    second        A function with string

This is my main command"""

help_with_subcommands_help = """
usage: main [-h] name age height {third,second} ...

The main command

positional arguments:
  name            The name of the person
  age             The age of the person
  height          The height of the person

options:
  -h, --help      show this help message and exit

subcommands:
  {third,second}  Help string of the subcommands. By default, it is empty.
    third         A function with int
    second        A function with string

This is my main command
"""

help_with_subcommands_description = """
usage: main [-h] name age height {third,second} ...

The main command

positional arguments:
  name            The name of the person
  age             The age of the person
  height          The height of the person

options:
  -h, --help      show this help message and exit

subcommands:
  Description string of the subcommands. When used, adds the EMPTY line below.

  {third,second}
    third         A function with int
    second        A function with string

This is my main command"""

help_with_subcommands_metavar = """
usage: main [-h] name age height {new-metavar} ...

The main command

positional arguments:
  name           The name of the person
  age            The age of the person
  height         The height of the person

options:
  -h, --help     show this help message and exit

subcommands:
  {new-metavar}
    third        A function with int
    second       A function with string

This is my main command"""

help_with_all_subcommands_options = """
usage: main [-h] name age height {new-metavar} ...

The main command

positional arguments:
  name           The name of the person
  age            The age of the person
  height         The height of the person

options:
  -h, --help     show this help message and exit

:=== SUBCOMMANDS SECTION TITLE ===:
  Description string of the subcommands. When used, adds the EMPTY line below.

  {new-metavar}  Help string of the subcommands. By default, it is empty.
    third        A function with int
    second       A function with string

This is my main command"""

ST = ":=== SUBCOMMANDS SECTION TITLE ==="
SH = "Help string of the subcommands. By default, it is empty."
SD = "Description string of the subcommands. When used, adds the EMPTY line below."
SM = "{new-metavar}"


def test_intg_05_subcommands_options_default(capsys: CapSys):
    cmd = Command(main)
    cmd.add_subcommand(third).add_subcommand(second)
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert default_help.strip() in output


def test_intg_05_subcommands_options_title(capsys: CapSys):
    cmd = Command(main, subcommands_title=ST)
    cmd.add_subcommand(third).add_subcommand(second)
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help_with_subcommands_title.strip() in output


def test_intg_05_subcommands_options_help(capsys: CapSys):
    cmd = Command(main, subcommands_help=SH)
    cmd.add_subcommand(third).add_subcommand(second)
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help_with_subcommands_help.strip() in output


def test_intg_05_subcommands_options_description(capsys: CapSys):
    cmd = Command(main, subcommands_description=SD)
    cmd.add_subcommand(third).add_subcommand(second)
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help_with_subcommands_description.strip() in output


def test_intg_05_subcommands_options_metavar(capsys: CapSys):
    cmd = Command(main, subcommands_metavar=SM)
    cmd.add_subcommand(third).add_subcommand(second)
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help_with_subcommands_metavar.strip() in output


def test_intg_05_subcommands_options_all_options(capsys: CapSys):
    cmd = Command(
        main, subcommands_title=ST, subcommands_help=SH, subcommands_description=SD, subcommands_metavar=SM
    )
    cmd.add_subcommand(third).add_subcommand(second)
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help_with_all_subcommands_options.strip() in output


def test_intg_05_subcommands_returns():
    cmd = Command(main)
    cmd.add_subcommand(third).add_subcommand(second)
    assert cmd.run(["jesus", "33", "1.80"]) == {"name": "jesus", "age": 33, "height": 1.80}
    assert cmd.run(["jesus", "33", "1.80", "second"]) == {}
    assert cmd.run(["jesus", "33", "1.80", "third", "24"]) == {"other": 24}
