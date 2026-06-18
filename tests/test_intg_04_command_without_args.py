import pytest
from resources import CapSys
from clig import Command

# %%          helps
############# helps ##########################################################################################

main_help = """
[-h] {foo,bar} ...

positional arguments:
  {foo,bar}
    foo       The foo command
    bar       The bar command

options:
  -h, --help  show this help message and exit""".strip()

foo_help = """
foo [-h] a b

The foo command

positional arguments:
  a           Help for a argument
  b           Help for b argument

options:
  -h, --help  show this help message and exit""".strip()

bar_help = """
bar [-h] c d

The bar command

positional arguments:
  c           Help for c argument
  d           Help for d argument

options:
  -h, --help  show this help message and exit""".strip()

# %%          commands
############# commands #######################################################################################

# The main command may not have a function, in cases it doesn't need arguments
cmd = Command()


@cmd.subcommand
def foo(a, b):
    """The foo command

    Args:
        a: Help for a argument
        b: Help for b argument
    """
    ...


@cmd.subcommand
def bar(c, d):
    """The bar command

    Args:
        c: Help for c argument
        d: Help for d argument
    """
    ...


# %%          without subcommands section
############# without subcommands section ####################################################################


def test_intg_04_command_without_args_main(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        cmd.run(["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert main_help in output


def test_intg_04_command_without_args_foo(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        cmd.run(["foo", "-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert foo_help in output


def test_intg_04_command_without_args_bar(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        cmd.run(["bar", "-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert bar_help in output


# %%          with subcommands section
############# with subcommands section #######################################################################

main_help_subsection = """
[-h] {fos,bas} ...

options:
  -h, --help  show this help message and exit

subcommands:
  {fos,bas}
    fos       The foo command
    bas       The bar command""".strip()

scmd = Command(subcommands_title="subcommands")


@scmd.subcommand
def fos(a, b):
    """The foo command

    Args:
        a: Help for a argument
        b: Help for b argument
    """
    ...


@scmd.subcommand
def bas(c, d):
    """The bar command

    Args:
        c: Help for c argument
        d: Help for d argument
    """
    ...


def test_intg_04_command_without_args_main_subcommands_section(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        scmd.run(["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert main_help_subsection in output
