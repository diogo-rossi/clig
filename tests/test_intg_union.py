import clig
import pytest
from enum import Enum
from resources import CapSys


class CPU(Enum):
    intel = 1
    amd = 2


def test_union_enum(capsys: CapSys):

    def foo(a: CPU | None):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(foo, ["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert "{intel,amd}" in output

    assert clig.run(foo, ["intel"]) == {"a": CPU(1)}
