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
