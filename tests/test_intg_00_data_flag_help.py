from enum import Enum
from resources import CapSys
import clig


class Color(Enum):
    red = 1
    blue = 2
    yellow = 3


def main(color: clig.Arg[Color, clig.data("-c", help="new color")] = Color.blue):
    """Summary of main function

    Main function that demonstrates the use of clig.Arg with an Enum type and custom help message.

    Parameters
    ----------
    - `color` (`Color`):
        My color argument that accepts values from the `Color` enum. It has a default value of `Color.blue`
        and can be specified using the `-c` flag in the command line.
    """
    print(f"Passed arguments to function: {locals()}")
    return locals()


def test_intg_00_data_flag_help(capsys: CapSys):
    cmd = clig.Command(main)
    cmd.print_help()
    output = capsys.readouterr().out
    assert "new color" in output
    assert "-c" in output
    assert clig.run(main, "-c red".split()) == {"color": Color(1)}
