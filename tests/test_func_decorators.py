import pytest
from resources import CapSys
from clig import command, subcommand, run


def test_command_without_args(capsys: CapSys):

    @command
    def mycmd(a: int, b: str):
        return locals()

    assert run(args=["34", "maria"]) == {"a": 34, "b": "maria"}


def test_command_and_subcommand_without_args(capsys: CapSys):

    @command
    def mycmd(a: int, b: str):
        return locals()

    @subcommand
    def mySubCmd(c: float, d: bool):
        return locals()

    assert run(args=["34", "maria"]) == {"a": 34, "b": "maria"}
    assert run(args=["666", "jack", "mySubCmd", "1.70", "--d"]) == {"c": 1.70, "d": True}


def test_command_with_args(capsys: CapSys):

    @command(make_shorts=True, make_flags=True, version="version 1.0.1")
    def mycmd(a: int, b: str):
        return locals()

    assert run(args=["-a", "34", "-b", "maria"]) == {"a": 34, "b": "maria"}

    with pytest.raises(SystemExit) as e:
        run(args=["-v"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert "version 1.0.1" in output


def test_command_and_subcommand_with_args(capsys: CapSys):

    @command(make_flags=True)
    def mycmd(a: int, b: str):
        return locals()

    @subcommand(make_flags=True, make_shorts=True)
    def mySubCmd(c: float, d: bool):
        return locals()

    assert run(args=["--a", "344", "--b", "mariana"]) == {"a": 344, "b": "mariana"}
    assert run(args="--a 666 --b joana mySubCmd -c 1.53 -d".split()) == {"c": 1.53, "d": True}

    # with pytest.raises(SystemExit) as e:
    #     run(args="--a 666 --b joana mySubCmd -c 1.53 -d".split())

    # assert e.value.code == 2
    # output = capsys.readouterr().err
    # assert "XX" in output
