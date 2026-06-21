import pytest
from resources import CapSys
import clig

error_msg = """
usage: foo [-h] [--ages [AGES ...]]
foo: error: argument --ages: invalid int value: '2.70'
""".strip()


def foo(ages: list[int] | None = None):
    return locals()


def test_intg_10_list_int(capsys: CapSys):

    assert clig.run(foo, "--ages 12 45 8".split()) == {"ages": [12, 45, 8]}
    assert clig.run(foo, []) == {"ages": None}

    with pytest.raises(SystemExit) as e:
        clig.run(foo, "--ages 2.70 45 8".split())

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert error_msg in output
