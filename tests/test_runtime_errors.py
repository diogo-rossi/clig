import pytest
import clig


def test_subcommand_decorator_without_main_command():

    with pytest.raises(RuntimeError) as e:

        @clig.subcommand
        def main(): ...

    assert "The main command is not defined. " in e.value.args[0]
    assert "Please use `clig.subcommand()` function only after `clig.command()`" in e.value.args[0]


def test_command_decorator_twice():

    with pytest.raises(RuntimeError) as e:

        @clig.command
        def main(): ...

        @clig.command
        def cmd(): ...

    assert "The main command is already defined with the function '" in e.value.args[0]
    assert "Please, use `clig.command()` function only once." in e.value.args[0]


def test_run_without_command():

    with pytest.raises(RuntimeError) as e:
        clig.run()

    assert "The main command is not defined. Please pass a function to `clig.run()`." in e.value.args[0]


def test_end_subcommand_error():

    def main():
        return 0

    def sub():
        return 1

    cmd = clig.Command(main)
    with pytest.raises(ValueError) as e:
        cmd.end_subcommand(sub)

    assert main() == 0
    assert sub() == 1
    assert (
        "Method `end_subcommand()` can not be called by `Command` instances without parent."
        in e.value.args[0]
    )
