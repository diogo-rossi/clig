from resources import CapSys
import clig
import pytest

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
