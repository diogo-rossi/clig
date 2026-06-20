from resources import CapSys
import clig
import pytest

output_prog08 = """
Arguments in the top level command: {'foo': 'bazinga', 'bar': 32}

Running now the second command . . .
The 'foo' argument from the previous command was: foo = bazinga
""".strip()


def test_prog08(capsys: CapSys):
    @clig.command
    def first(foo: str, bar: int):
        print(f"Arguments in the top level command: {locals()}")

    @clig.subcommand
    def second(ctx: clig.Context, ham: float):
        print()
        print("Running now the second command . . .")
        print(f"The 'foo' argument from the previous command was: foo = {ctx.namespace.foo}")

    clig.run(args="bazinga 32 second 22.5".split())
    output = capsys.readouterr().out
    assert output_prog08 in output
