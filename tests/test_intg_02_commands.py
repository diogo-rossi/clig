import pytest
from pathlib import Path
from resources import CapSys
from clig import Command, Arg, data

# %%          functions
############# functions ######################################################################################


def git(
    exec_path: Arg[Path, data("-e", metavar="<path>")] = Path("git"),
    work_tree: Arg[Path, data("-w", metavar="<path>")] = Path(".").resolve(),
):
    return locals()


def remote(verbose: Arg[bool, data("-v", help="To be verbose")] = False):
    return locals()


def add(name: str, url: str):
    return locals()


def rename(old: str, new: str):
    return locals()


def remove(name: str):
    return locals()


def submodule(quiet: bool):
    return locals()


def init(path: Path = Path(".").resolve()):
    return locals()


def update(init: bool, path: Path = Path(".").resolve()):
    return locals()


# %%          with subcommands section
############# with subcommands section #######################################################################

main_subsection = Command(git, subcommands_required=True, subcommands_title="subcommands")


sub1_subsection = (
    main_subsection.new_subcommand(remote, subcommands_required=True, help="")
    .add_subcommand(add)
    .add_subcommand(rename)
    .add_subcommand(remove)
)
sub2_subsection = (
    main_subsection.new_subcommand(submodule, help="").add_subcommand(init).add_subcommand(update)
)

helpmessage_subcommands_section = """
usage: git [-h] [-e <path>] [-w <path>] {remote,submodule} ...

options:
  -h, --help            show this help message and exit
  -e <path>, --exec-path <path>
  -w <path>, --work-tree <path>

subcommands:
  {remote,submodule}
    remote
    submodule"""

errormessage = "git: error: the following arguments are required: {remote,submodule}"


def test_intg_02_commands_error(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        main_subsection.run([])

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert errormessage in output


def test_intg_02_commands_helpmsg(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        main_subsection.run(["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmessage_subcommands_section.strip() in output.strip()


def test_intg_02_commands_remote():

    assert main_subsection.run("remote add origin github.com".split()) == {
        "name": "origin",
        "url": "github.com",
    }
    assert main_subsection.run("remote rename oldremote newremote".split()) == {
        "old": "oldremote",
        "new": "newremote",
    }
    assert main_subsection.run("remote remove remotetoremove".split()) == {"name": "remotetoremove"}


def test_intg_02_commands_submodule_init(capsys: CapSys):

    errormsg = "git submodule: error: the following arguments are required: --quiet/--no-quiet"

    with pytest.raises(SystemExit) as e:
        assert main_subsection.run("submodule init --path temppath".split())

    assert e.value.code == 2
    readouterr = capsys.readouterr()
    err = readouterr.err
    assert errormsg in err

    errormsg = "error: unrecognized arguments: temppath"

    with pytest.raises(SystemExit) as e:
        assert main_subsection.run("submodule --quiet init temppath".split())

    assert e.value.code == 2
    readouterr = capsys.readouterr()
    err = readouterr.err
    assert errormsg in err

    assert main_subsection.run("submodule --quiet init --path temppath".split()) == {"path": Path("temppath")}


def test_intg_02_commands_submodule_update(capsys: CapSys):
    args = "submodule --quiet update --init --path subdir".split()
    assert main_subsection.run(args) == {"init": True, "path": Path("subdir")}


# %%          without subcommands sections
############# without subcommands sections ###################################################################

helpmessage_subcommands_default = """
usage: git [-h] [-e <path>] [-w <path>] {remote,submodule} ...

positional arguments:
  {remote,submodule}
    remote
    submodule

options:
  -h, --help            show this help message and exit
  -e <path>, --exec-path <path>
  -w <path>, --work-tree <path>
"""

main_default = Command(git, subcommands_required=True)

sub1_default = (
    main_default.new_subcommand(remote, subcommands_required=True, help="")
    .add_subcommand(add)
    .add_subcommand(rename)
    .add_subcommand(remove)
)
sub2_default = main_default.new_subcommand(submodule, help="").add_subcommand(init).add_subcommand(update)


def test_intg_02_commands_helpmsg_default(capsys: CapSys):

    with pytest.raises(SystemExit) as e:
        main_default.run(["-h"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert helpmessage_subcommands_default.strip() in output.strip()
