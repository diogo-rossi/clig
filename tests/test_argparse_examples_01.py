import clig
import argparse
import pathlib
import pytest
from resources import CapSys

# First example of https://docs.python.org/3/library/argparse.html

parser = argparse.ArgumentParser(
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


def test_first_example_parsed_args(capsys: CapSys):
    def ProgramName(filename, count=None, verbose=False):
        return locals()

    assert clig.run(ProgramName, args) == parsed_args
    assert clig.run(ProgramName, args, make_shorts=True) == parsed_args_shorts

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
