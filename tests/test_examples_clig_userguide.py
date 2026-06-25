import pytest
import clig
from resources import CapSys


def test_example01():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#basic-usage"""

    def printperson(name, title="Mister"):
        return f"{title} {name}"

    assert clig.run(printperson, ["John"]) == "Mister John"
    assert clig.run(printperson, ["Maria", "--title", "Miss"]) == "Miss Maria"
    assert clig.run(printperson, ["Isaac", "--title", "Sir"]) == "Sir Isaac"


example02help = """
usage: greetings [-h] [--greet GREET] name

Description of the command: A greeting prompt!

positional arguments:
  name           The name to greet

options:
  -h, --help     show this help message and exit
  --greet GREET  The greeting used. Defaults to "Hello".
  """.strip()


def test_example02(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#helps"""

    def greetings(name, greet="Hello"):
        """Description of the command: A greeting prompt!

        Args:
            name: The name to greet
            greet: The greeting used. Defaults to "Hello".
        """
        return f"Greetings: {greet} {name}!"

    with pytest.raises(SystemExit) as e:
        clig.run(greetings, ["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert example02help in output
    assert clig.run(greetings, ["Maria"]) == "Greetings: Hello Maria!"


example03error = """
usage: recordperson [-h] name age height
recordperson: error: argument age: invalid int value: 'John'
""".strip()


def test_example03(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#argument-inference"""

    def recordperson(name: str, age: int, height: float):
        return locals()

    assert clig.run(recordperson, "John 37 1.73".split()) == {"name": "John", "age": 37, "height": 1.73}

    with pytest.raises(SystemExit) as e:
        clig.run(recordperson, "Mr John Doe".split())

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert example03error in output


def test_example04(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#booleans"""

    def recordperson(name: str, employee: bool = False):
        return locals()

    assert clig.run(recordperson, "--employee Leo".split()) == {"name": "Leo", "employee": True}
    assert clig.run(recordperson, "Ana".split()) == {"name": "Ana", "employee": False}


example05error = """
usage: recordperson [-h] --employee | --no-employee name
recordperson: error: the following arguments are required: --employee/--no-employee
""".strip()


def test_example05(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#required-booleans"""

    def recordperson(name: str, employee: bool):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(recordperson, "Ana".split())

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert example05error in output
    assert clig.run(recordperson, "Ana --no-employee".split()) == {"name": "Ana", "employee": False}


example06help = """
usage: main [-h] name name

positional arguments:
  name

options:
  -h, --help  show this help message and exit
""".strip()

example06error = """
usage: main [-h] name name
main: error: the following arguments are required: name
""".strip()


def test_example06(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#tuples"""

    def main(name: tuple[str, str]):
        return locals()

    assert clig.run(main, ["rocky", "yoco"]) == {"name": ("rocky", "yoco")}

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["rocky"])

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert example06error in output

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert example06help in output


example07error = """
usage: main [-h] [--name NAME NAME NAME]
main: error: argument --name: expected 3 arguments
""".strip()


def test_example07(capsys: CapSys):
    def main(name: tuple[str, str, str] = ("john", "mary", "jean")):
        return locals()

    assert clig.run(main, []) == {"name": ("john", "mary", "jean")}
    assert clig.run(main, "--name yoco rocky sand".split()) == {"name": ("yoco", "rocky", "sand")}

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--name", "yoco"])

    assert e.value.code == 2
    output = capsys.readouterr().err.strip()
    assert example07error in output


example08help = """
usage: main [-h] names [names ...]

positional arguments:
  names

options:
  -h, --help  show this help message and exit
""".strip()

example08error = """
usage: main [-h] names [names ...]
main: error: the following arguments are required: names
""".strip()


def test_example08(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#list-sequences-and-tuples-of-any-length"""

    def main(names: list[str]):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert example08help in output

    with pytest.raises(SystemExit) as e:
        clig.run(main, [])

    assert e.value.code == 2
    output = capsys.readouterr().err.strip()
    assert example08error in output

    assert clig.run(main, ["chester", "philip"]) == {"names": ["chester", "philip"]}


example09help = """
usage: main [-h] [--names [NAMES ...]]

options:
  -h, --help           show this help message and exit
  --names [NAMES ...]
""".strip()


def test_example09(capsys: CapSys):

    def main(names: list[str] | None = None):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert example09help in output

    assert clig.run(main, ["--names", "katy", "buba"]) == {"names": ["katy", "buba"]}
    assert clig.run(main, []) == {"names": None}


example10help = """
usage: main [-h] name {rock,paper,scissors}

positional arguments:
  name
  {rock,paper,scissors}

options:
  -h, --help            show this help message and exit
""".strip()

example10error = """
usage: main [-h] name {rock,paper,scissors}
main: error: argument move: invalid choice: 'knife' (choose from rock, paper, scissors)
""".strip()


def test_example10(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#literals-and-enums-choices"""

    from typing import Literal

    def main(name: str, move: Literal["rock", "paper", "scissors"]):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert example10help in output

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["John", "knife"])

    assert e.value.code == 2
    output = capsys.readouterr().err.strip()
    assert example10error in output

    assert clig.run(main, ["Mary", "paper"]) == {"name": "Mary", "move": "paper"}


example11help = """
usage: main [-h] {red,blue,yellow} {minimun,mean,maximum}

positional arguments:
  {red,blue,yellow}
  {minimun,mean,maximum}

options:
  -h, --help            show this help message and exit
""".strip()

example11error = """
usage: main [-h] {red,blue,yellow} {minimun,mean,maximum}
main: error: argument color: invalid choice: 'green' (choose from red, blue, yellow)
""".strip()


def test_example11(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#passing-enums"""
    from enum import Enum, StrEnum

    class Color(Enum):
        red = 1
        blue = 2
        yellow = 3

    class Statistic(StrEnum):
        minimun = "minimun"
        mean = "mean"
        maximum = "maximum"

    def main(color: Color, statistic: Statistic):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert example11help in output

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["green"])

    assert e.value.code == 2
    output = capsys.readouterr().err.strip()
    assert example11error in output

    assert clig.run(main, ["red", "mean"]) == {"color": Color(1), "statistic": Statistic("mean")}


def test_example12():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#literal-with-enum"""
    from typing import Literal
    from enum import Enum

    class Color(Enum):
        red = 1
        blue = 2
        yellow = 3

    def main(color: Literal[Color.red, "green", "black"]):
        return locals()

    assert clig.run(main, ["red"]) == {"color": Color(1)}
    assert clig.run(main, ["green"]) == {"color": "green"}


def test_variadic_arguments():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#variadic-arguments-args-and-kwargs-partial-parsing"""

    def variadics(foo: str, *args, **kwargs):
        return locals()

    assert clig.run(variadics, "bar badger BAR spam --name adam --title mister".split()) == {
        "foo": "bar",
        "args": ("badger", "BAR", "spam"),
        "kwargs": {"name": "adam", "title": "mister"},
    }


def test_variadic_args():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#args"""

    def variadicstyped(number: float, *integers: int):
        return locals()

    assert clig.run(variadicstyped, ["36.7", "1", "2", "3", "4", "5"]) == {
        "number": 36.7,
        "integers": (1, 2, 3, 4, 5),
    }


def test_example13():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#kwargs"""

    def foobar(name: str, **kwargs):
        return locals()

    assert clig.run(foobar, "joseph --nickname joe --uncles jack jean adam".split()) == {
        "name": "joseph",
        "kwargs": {"nickname": "joe", "uncles": ["jack", "jean", "adam"]},
    }


def test_example14():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#kwargs"""

    def foobartyped(name: str, **intergers: int):
        return locals()

    assert clig.run(foobartyped, "joseph --age 23 --numbers 25 27 30".split()) == {
        "name": "joseph",
        "intergers": {"age": 23, "numbers": [25, 27, 30]},
    }

    with pytest.raises(ValueError) as e:
        clig.run(foobartyped, "joseph --age 23 --numbers jack jean adam".split())

    assert "invalid literal for int() with base 10: 'jack'" in e.value.args[0]


def test_example15():
    """https://clig.readthedocs.io/en/latest/notebooks/userguide.html#error-when-passing-flagged-arguments-to-args"""

    def bazham(name: str, *uncles: str):
        return locals()

    assert clig.run(bazham, "joseph jack john".split()) == {"name": "joseph", "uncles": ("jack", "john")}

    with pytest.raises(TypeError) as e:
        clig.run(bazham, "joseph --uncles jack john".split())

    assert "bazham() got an unexpected keyword argument 'uncles'" in e.value.args[0]
