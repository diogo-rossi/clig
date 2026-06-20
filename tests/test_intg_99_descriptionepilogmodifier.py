from enum import Enum
from resources import CapSys
import clig
import pytest

helpmsg_append_description = """
usage: main [-h] a b c

Description of the function. Appended TEXT.

positional arguments:
  a           Description of a.
  b           Description of b.
  c           Description of c.

options:
  -h, --help  show this help message and exit

Epilog of the function.
""".strip()

helpmsg_append_epilog = """
usage: main [-h] a b c

Description of the function.

positional arguments:
  a           Description of a.
  b           Description of b.
  c           Description of c.

options:
  -h, --help  show this help message and exit

Epilog of the function. Appended TEXT.
""".strip()


def main(a, b, c) -> dict:
    """Description of the function.

    Epilog of the function.

    Parameters
    ----------
    - `a` (`int`):
        Description of a.

    - `b` (`str`):
        Description of b.

    - `c` (`float`):
        Description of c.

    Returns
    -------
    `dict`:
        The `locals()` dict.
    """
    return locals()


def test_intg_99_descriptionmodifier(capsys: CapSys):
    cmd = clig.Command(main, descriptionmodifier=lambda s: f"{s} Appended TEXT.")
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    assert helpmsg_append_description.strip() in capsys.readouterr().out
    assert cmd.run("25 name 1.8".split()) == {"a": "25", "b": "name", "c": "1.8"}


def test_intg_99_epilogmodifier(capsys: CapSys):
    cmd = clig.Command(main, epilogmodifier=lambda s: f"{s} Appended TEXT.")
    with pytest.raises(SystemExit) as e:
        cmd.run(["--help"])
    assert e.value.code == 0
    assert helpmsg_append_epilog.strip() in capsys.readouterr().out
