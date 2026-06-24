from resources import CapSys
import clig
from clig import Command
import pytest


def test_prog01():

    def main(name: str, age: int, height: float):
        return locals()

    cmd = Command(main)
    assert cmd.run(["Carmem Miranda", "42", "1.85"]) == {"name": "Carmem Miranda", "age": 42, "height": 1.85}


helpmsg_prog02 = """
usage: prog [-h] name age {subfunction1,subfunction2} ...

positional arguments:
  name
  age
  {subfunction1,subfunction2}

options:
  -h, --help            show this help message and exit
""".strip()

helpmsg_prog02_sub = """
usage: prog name age subfunction2 [-h] father mother {subsubfunction} ...

positional arguments:
  father
  mother
  {subsubfunction}

options:
  -h, --help        show this help message and exit
""".strip()


def test_prog02(capsys: CapSys):
    from clig import Command

    def prog(name: str, age: int):
        return locals()

    def subfunction1(height: float):
        return locals()

    def subfunction2(father: str, mother: str):
        return locals()

    def subsubfunction(city: str, state: str):
        return locals()

    # defines the main object
    cmd = Command(prog)

    # adds a subcommand to the main object
    cmd.add_subcommand(subfunction1)

    # adds and returns a new created subcommand object
    sub = cmd.new_subcommand(subfunction2)

    # adds a subcommand to the subcommand object
    sub.add_subcommand(subsubfunction)

    # main command help
    cmd.print_help()
    output = capsys.readouterr().out
    assert helpmsg_prog02 in output

    sub.print_help()
    output = capsys.readouterr().out
    assert helpmsg_prog02_sub in output

    assert cmd.run("jack 23".split()) == {"name": "jack", "age": 23}
    assert cmd.run("jack 23 subfunction2 michael suzan subsubfunction santos SP".split()) == {
        "city": "santos",
        "state": "SP",
    }


helpmsg_prog06 = """
usage: main [-h] [--verbose] {foo,bar} ...

Description for the main command

positional arguments:
  {foo,bar}
    foo       Help for foo sub command
    bar       Help for bar sub command

options:
  -h, --help  show this help message and exit
  --verbose
""".strip()


def test_prog06(capsys: CapSys):
    from clig import command, subcommand, run

    @command
    def main(verbose: bool = False):
        """Description for the main command"""
        return locals()

    @subcommand
    def foo(a, b):
        """Help for foo sub command"""
        return locals()

    @subcommand
    def bar(c, d):
        """Help for bar sub command"""
        return locals()

    with pytest.raises(SystemExit) as e:
        run(args=["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog06 in output
    assert run(args=[]) == {"verbose": False}
    assert run(args=["foo", "hello", "world"]) == {"a": "hello", "b": "world"}
    assert run(args=["bar", "world", "hello"]) == {"c": "world", "d": "hello"}


helpmsg_prog07 = """
usage: prog [-h] [--name NAME] [--age AGE] {subfunction} ...

positional arguments:
  {subfunction}

options:
  -h, --help     show this help message and exit
  --name NAME
  --age AGE
""".strip()

helpmsg_prog07subfunction = """
usage: prog subfunction [-h] height {internalsubfunction} ...

positional arguments:
  height
  {internalsubfunction}

options:
  -h, --help            show this help message and exit
""".strip()


def test_prog07(capsys: CapSys):
    from clig import command, subcommand, run

    @command
    def prog(name: str = "mario", age: int = 40):
        return locals()

    @subcommand
    def subfunction(height: float):
        return locals()

    @subcommand(parent=subfunction)
    def internalsubfunction(city: str, state: str):
        return locals()

    with pytest.raises(SystemExit) as e:
        run(args=["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog07 in output

    with pytest.raises(SystemExit) as e:
        run(args=["subfunction", "-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog07subfunction in output

    assert run(args=[]) == {"name": "mario", "age": 40}
    assert run(args=["subfunction", "1.8"]) == {"height": 1.80}
    assert run(args="subfunction 2.5 internalsubfunction rio RJ".split()) == {"city": "rio", "state": "RJ"}


output_prog08 = """
Arguments in the top level command: {'foo': 'bazinga', 'bar': 32}

Running now the second command . . .
The 'foo' argument from the previous command was: foo = bazinga
""".strip()


def test_prog08(capsys: CapSys):
    @clig.command
    def first(foo: str, bar: int):
        print(f"Arguments in the top level command: {locals()}")

    @clig.subcommand
    def second(ctx: clig.Context, ham: float):
        print()
        print("Running now the second command . . .")
        print(f"The 'foo' argument from the previous command was: foo = {ctx.namespace.foo}")

    clig.run(args="bazinga 32 second 22.5".split())
    output = capsys.readouterr().out
    assert output_prog08 in output
