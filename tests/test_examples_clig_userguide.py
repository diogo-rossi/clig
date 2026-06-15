import pytest
import clig
from resources import CapSys


def test_example01():

    def printperson(name, title="Mister"):
        return f"{title} {name}"

    assert clig.run(printperson, ["John"]) == "Mister John"
    assert clig.run(printperson, ["Maria", "--title", "Miss"]) == "Miss Maria"
    assert clig.run(printperson, ["Isaac", "--title", "Sir"]) == "Sir Isaac"


example02help = """usage: greetings [-h] [--greet GREET] name

Description of the command: A greeting prompt!

positional arguments:
  name           The name to greet

options:
  -h, --help     show this help message and exit
  --greet GREET  The greeting used. Defaults to "Hello"."""


def test_example02(capsys: CapSys):

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
