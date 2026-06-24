from resources import CapSys
import clig
from clig import Command, command, subcommand, run
import pytest


def test_prog01():
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#subcommands"""

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
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#subcommands-using-methods"""
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
    assert cmd.run("jane 46 subfunction1 1.50".split()) == {"height": 1.50}
    assert cmd.run("jack 23 subfunction2 michael suzan subsubfunction santos SP".split()) == {
        "city": "santos",
        "state": "SP",
    }


helpmsg_prog03 = """
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


def test_prog03(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#subcommands-using-method-decorators"""

    def main(verbose: bool = False):
        """Description for the main command"""
        return locals()

    # create the command object
    cmd = Command(main)

    @cmd.subcommand
    def foo(a, b):
        """Help for foo sub command"""
        return locals()

    @cmd.subcommand
    def bar(c, d):
        """Help for bar sub command"""
        return locals()

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog03 in output
    assert cmd.run(args=["--verbose"]) == {"verbose": True}
    assert cmd.run(args=["foo", "baz", "ham"]) == {"a": "baz", "b": "ham"}
    assert cmd.run(args=["bar", "jack", "chan"]) == {"c": "jack", "d": "chan"}


helpmsg_prog04_main = """
usage: prog [-h] [--name NAME] [--age AGE] {subfunction1,subfunction2} ...

positional arguments:
  {subfunction1,subfunction2}

options:
  -h, --help            show this help message and exit
  --name NAME
  --age AGE
""".strip()

helpmsg_prog04_subfunction2 = """
usage: prog subfunction2 [-h] father mother {subsubfunction} ...

positional arguments:
  father
  mother
  {subsubfunction}

options:
  -h, --help        show this help message and exit
""".strip()


def test_prog_04(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#adding-internal-level-of-subcommads-with-decorators"""

    def prog(name: str = "mario", age: int = 40):
        return locals()

    cmd = Command(prog)

    @cmd.subcommand
    def subfunction1(height: float):
        return locals()

    @cmd.subcommand
    def subfunction2(father: str, mother: str):
        return locals()

    @cmd.subcommands["subfunction2"].subcommand
    def subsubfunction(city: str, state: str):
        return locals()

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog04_main in output

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["subfunction2", "-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog04_subfunction2 in output

    assert cmd.run([]) == {"name": "mario", "age": 40}
    assert cmd.run(["subfunction1", "1.70"]) == {"height": 1.70}
    assert cmd.run(["subfunction2", "jose", "maria"]) == {"father": "jose", "mother": "maria"}
    assert cmd.run(["subfunction2", "jose", "maria", "subsubfunction", "limeira", "SP"]) == {
        "city": "limeira",
        "state": "SP",
    }


helpmsg_prog05_main = """
usage: prog [-h] [--name NAME] [--age AGE] {subfunction} ...

positional arguments:
  {subfunction}

options:
  -h, --help     show this help message and exit
  --name NAME
  --age AGE
""".strip()

helpmsg_prog05_subfunction = """
usage: prog subfunction [-h] height {internalsubfunction} ...

positional arguments:
  height
  {internalsubfunction}

options:
  -h, --help            show this help message and exit
""".strip()


def test_prog05(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#method-decorator-with-arguments"""

    def prog(name: str = "mario", age: int = 40):
        return locals()

    cmd = Command(prog)

    @cmd.subcommand
    def subfunction(height: float):
        return locals()

    @cmd.subcommand(parent=subfunction)
    def internalsubfunction(city: str, state: str):
        return locals()

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog05_main in output

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["subfunction", "-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog05_subfunction in output

    assert cmd.run([]) == {"name": "mario", "age": 40}
    assert cmd.run(["subfunction", "1.70"]) == {"height": 1.70}
    assert cmd.run(["subfunction", "1.70", "internalsubfunction", "limeira", "SP"]) == {
        "city": "limeira",
        "state": "SP",
    }


helpmsg_prog05_main_with_name_as_parent = """
usage: prog [-h] [--name NAME] [--age AGE] {subprog} ...

positional arguments:
  {subprog}

options:
  -h, --help   show this help message and exit
  --name NAME
  --age AGE
""".strip()

helpmsg_prog05_subfunction_with_name_as_parent = """
usage: prog subprog [-h] height {internalsubfunction} ...

positional arguments:
  height
  {internalsubfunction}

options:
  -h, --help            show this help message and exit
""".strip()


def test_prog05_with_name_as_parent(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#method-decorator-with-arguments"""

    def prog(name: str = "mario", age: int = 40):
        return locals()

    cmd = Command(prog)

    @cmd.subcommand(name="subprog")
    def subfunction(height: float):
        return locals()

    @cmd.subcommand(parent="subprog")
    def internalsubfunction(city: str, state: str):
        return locals()

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog05_main_with_name_as_parent in output

    with pytest.raises(SystemExit) as e:
        cmd.run(args=["subprog", "-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmsg_prog05_subfunction_with_name_as_parent in output

    assert cmd.run([]) == {"name": "mario", "age": 40}
    assert cmd.run(["subprog", "1.70"]) == {"height": 1.70}
    assert cmd.run(["subprog", "1.70", "internalsubfunction", "limeira", "SP"]) == {
        "city": "limeira",
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
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#subcommands-using-function-decorators"""

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
    """https://clig.readthedocs.io/en/latest/notebooks/subcommands.html#function-decorator-with-arguments"""

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
