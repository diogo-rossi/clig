import clig
import argparse
import pathlib
import pytest
from clig import Command, Arg, data
from resources import CapSys, deindent
from argparse import ArgumentParser
from argparse import Namespace


def test_first_example_parsed_args(capsys: CapSys):
    """First example of https://docs.python.org/3/library/argparse.html"""

    parser = ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("filename")  # positional argument
    parser.add_argument("-c", "--count")  # option that takes a value
    parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag
    args = ["myfile", "--count", "3", "--verbose"]
    args_shorts = ["myfile", "-c", "3", "-v"]
    parsed_args = vars(parser.parse_args(args))
    parsed_args_shorts = vars(parser.parse_args(args))

    def ProgramName(filename, count=None, verbose=False):
        return locals()

    assert clig.run(ProgramName, args) == parsed_args
    assert clig.run(ProgramName, args_shorts, make_shorts=True) == parsed_args_shorts

    with pytest.raises(SystemExit) as e1:
        clig.run(
            ProgramName,
            ["--help"],
            make_shorts=True,
            description="What the program does",
            epilog="Text at the bottom of help",
        )

    assert e1.value.code == 0
    output1 = capsys.readouterr().out.strip()

    with pytest.raises(SystemExit) as e2:
        parser.parse_args(["--help"])

    assert e2.value.code == 0
    output2 = capsys.readouterr().out.strip()

    assert output1 in output2


help_prog_example1 = """
usage: myprogram [-h]

options:
  -h, --help  show this help message and exit
""".strip()

help_prog_example2 = """
usage: myprogram [-h] [--foo FOO]

options:
  -h, --help  show this help message and exit
  --foo FOO   foo of the myprogram program
""".strip()


def test_prog_example(capsys: CapSys):
    """Example of https://docs.python.org/3/library/argparse.html#prog"""

    parser = argparse.ArgumentParser(prog="myprogram")
    parser.print_help()
    output = capsys.readouterr().out.strip()
    assert help_prog_example1 in output

    def main1(): ...

    cmd = Command(main1, prog="myprogram")
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert help_prog_example1 in output

    parser = argparse.ArgumentParser(prog="myprogram")
    parser.add_argument("--foo", help="foo of the %(prog)s program")
    parser.print_help()
    output = capsys.readouterr().out.strip()
    assert help_prog_example2 in output

    def main2(foo: Arg[str | None, data(help="foo of the %(prog)s program")] = None): ...

    # TODO: variation with docstring

    cmd = Command(main2, prog="myprogram")
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert help_prog_example2 in output


help_usage_example = """
usage: PROG [options]

positional arguments:
  bar          bar help

options:
  -h, --help   show this help message and exit
  --foo [FOO]  foo help
""".strip()


def test_usage_example(capsys: CapSys):
    """https://docs.python.org/3/library/argparse.html#usage"""
    parser = argparse.ArgumentParser(prog="PROG", usage="%(prog)s [options]")
    parser.add_argument("--foo", nargs="?", help="foo help")
    parser.add_argument("bar", nargs="+", help="bar help")
    parser.print_help()
    output = capsys.readouterr().out.strip()
    assert help_usage_example in output

    def main1(
        bar: Arg[str, data(nargs="+", help="bar help")],
        foo: Arg[str | None, data(nargs="?", help="foo help")] = None,
    ): ...

    cmd = Command(main1, prog="PROG", usage="%(prog)s [options]")
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert help_usage_example in output

    def main2(
        bar: Arg[list[str], data(help="bar help")],
        foo: Arg[str | None, data(nargs="?", help="foo help")] = None,
    ): ...

    # TODO: variation with docstring

    cmd = Command(main2, prog="PROG", usage="%(prog)s [options]")
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert help_usage_example in output


help_epilog_example = """
usage: argparse.py [-h]

A foo that bars

options:
  -h, --help  show this help message and exit

And that's how you'd foo a bar
""".strip()


def test_epilog_example(capsys: CapSys):
    """https://docs.python.org/3/library/argparse.html#epilog"""

    parser = argparse.ArgumentParser(
        prog="argparse.py", description="A foo that bars", epilog="And that's how you'd foo a bar"
    )
    parser.print_help()
    output = capsys.readouterr().out.strip()
    assert help_epilog_example in output

    def main1(): ...

    cmd = Command(
        main1, prog="argparse.py", description="A foo that bars", epilog="And that's how you'd foo a bar"
    )
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert help_epilog_example in output

    def main2():
        """A foo that bars

        And that's how you'd foo a bar
        """
        ...

    # TODO: variation with docstring
    cmd = Command(main2, prog="argparse.py", docstring_template=clig.DocStr.DESCRIPTION_EPILOG_DOCSTRING)
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert help_epilog_example in output


def test_argparse_subcommands_aliases(capsys: CapSys):
    """https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers"""
    helpmsg = """
    usage: subali [-h] {checkout,co} ...

    positional arguments:
      {checkout,co}

    options:
      -h, --help     show this help message and exit
    """

    parser = argparse.ArgumentParser(prog="subali")
    subparsers = parser.add_subparsers()
    checkout_ = subparsers.add_parser("checkout", aliases=["co"])
    checkout_.add_argument("foo")

    parser.print_help()
    output = capsys.readouterr().out.strip()
    assert deindent(helpmsg) == output
    assert parser.parse_args(["co", "bar"]) == Namespace(foo="bar")

    def subali(): ...
    def checkout(foo):
        return locals()

    cmd = Command(subali).add_subcommand(checkout, aliases=["co"])
    cmd.print_help()
    output = capsys.readouterr().out.strip()
    assert deindent(helpmsg) == output
    assert cmd.run(["co", "bar"]) == {"foo": "bar"}
