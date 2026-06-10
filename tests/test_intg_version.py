import clig
import pytest
from resources import CapSys


def test_version_with_string(capsys: CapSys):
    def main_command() -> int:
        return 0

    with pytest.raises(SystemExit) as e:
        clig.run(main_command, ["--version"], version="1.2.3")

    assert main_command() == 0
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert "1.2.3" in output


def test_version_with_version_msg(capsys: CapSys):
    def main_command() -> int:
        return 1

    with pytest.raises(SystemExit) as e:
        clig.run(main_command, ["--help"], version="1.2.3", version_msg="This is my version.")

    assert main_command() == 1
    assert e.value.code == 0
    output = capsys.readouterr().out
    assert "This is my version." in output
