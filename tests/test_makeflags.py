import pytest
from resources import CapSys
from clig.clig import Arg, data, Command


def test_make_flag_on_argument_automatically():
    def main(foobar: Arg[str, data("-f")]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foobar"]
    assert cmd.run(["-f", "test"]) == dict(foobar="test")
    assert cmd.run(["--foobar", "testing"]) == dict(foobar="testing")


def test_donot_make_flag_on_argument_automatically():
    def main(foobar: Arg[str, data("-f", "--foo")]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo"]
    assert cmd.run(["-f", "test"]) == dict(foobar="test")
    assert cmd.run(["--foo", "testing"]) == dict(foobar="testing")


def test_force_make_flag_on_argument_automatically():
    def main(foobar: Arg[str, data("-f", "--foo", make_flag=True)]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo", "--foobar"]
    assert cmd.run(["-f", "test"]) == dict(foobar="test")
    assert cmd.run(["--foo", "testing"]) == dict(foobar="testing")
    assert cmd.run(["--foobar", "testingagain"]) == dict(foobar="testingagain")


def test_force_make_flag_on_argument_automatically_in_command():
    def main(foobar: Arg[str, data("-f", "--foo")]):
        return locals()

    cmd = Command(main, make_flags=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo", "--foobar"]
    assert cmd.run(["--foobar", "test"]) == dict(foobar="test")


def test_force_donot_make_flag_on_argument():
    def main(foobar: Arg[str, data("-f", make_flag=False)]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f"]
    assert cmd.run(["-f", "test"]) == dict(foobar="test")


def test_force_donot_make_flag_in_command():
    def main(foobar: Arg[str, data("-f")]):
        return locals()

    cmd = Command(main, make_flags=False)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f"]
    assert cmd.run(["-f", "test"]) == dict(foobar="test")


def test_conflict_force_make_flags_true_on_argument():
    def main(foobar: Arg[str, data("-f", "--foo", make_flag=True)], bazham: Arg[str, data("-b")]):
        return locals()

    cmd = Command(main, make_flags=False)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo", "--foobar"]
    assert cmd.arguments[1].option_strings == ["-b"]
    assert cmd.run(["-f", "test", "-b", "baz"]) == dict(foobar="test", bazham="baz")


def test_conflict_force_make_flags_true_on_command():
    def main(foobar: Arg[str, data("-f", "--foo", make_flag=False)], bazham: Arg[str, data("-b", "--baz")]):
        return locals()

    cmd = Command(main, make_flags=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo"]
    assert cmd.arguments[1].option_strings == ["-b", "--baz", "--bazham"]
    assert cmd.run(["-f", "test", "-b", "baz"]) == dict(foobar="test", bazham="baz")


def test_force_make_flags_on_command_argument_not_annotated(capsys: CapSys):
    def main(foobar: str, bazham: int = 42):
        return locals()

    cmd = Command(main, make_flags=False)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == []
    assert cmd.arguments[1].option_strings == []

    with pytest.raises(SystemExit) as e:
        cmd.run(["dio"])

    assert e.value.code == 2
    assert "the following arguments are required: bazham" in capsys.readouterr().err
    assert cmd.run(["test", "35"]) == dict(foobar="test", bazham=35)


def test_force_make_shorts_on_command():
    def main(foobar: str = "dio", bazham: int = 42):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["--foobar"]
    assert cmd.arguments[1].option_strings == ["--bazham"]

    cmd = Command(main, make_shorts=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foobar"]
    assert cmd.arguments[1].option_strings == ["-b", "--bazham"]
    assert cmd.run(["-f", "test", "-b", "66"]) == dict(foobar="test", bazham=66)


def test_force_make_shorts_conflict(capsys: CapSys):
    def main(foo: str = "dio", foobar: int = 42):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["--foo"]
    assert cmd.arguments[1].option_strings == ["--foobar"]
    assert cmd.run(["--foo", "test", "--foobar", "66"]) == dict(foo="test", foobar=66)

    cmd = Command(main, make_shorts=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo"]
    assert cmd.arguments[1].option_strings == ["-F", "--foobar"]
    assert cmd.run(["-f", "test", "-F", "67"]) == dict(foo="test", foobar=67)


def test_force_make_shorts_conflicting_on_command():
    def main(foobar: str = "dio", foo_ham: int = 42, foo_hat: int = 42):
        return locals()

    cmd = Command(main, make_shorts=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foobar"]
    assert cmd.arguments[1].option_strings == ["-F", "--foo-ham"]
    assert cmd.arguments[2].option_strings == ["-fh", "--foo-hat"]
    assert cmd.run(["-f", "test", "-F", "66"]) == dict(foobar="test", foo_ham=66, foo_hat=42)

    def second(name: str = "name", namefile: str = "file", namefolder: str = "folder"):
        return locals()

    cmd = Command(second, make_shorts=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-n", "--name"]
    assert cmd.arguments[1].option_strings == ["-N", "--namefile"]
    assert cmd.arguments[2].option_strings == ["-na", "--namefolder"]

    assert cmd.run([]) == dict(name="name", namefile="file", namefolder="folder")
    assert cmd.run(["-n", "paul", "-N", "test"]) == dict(name="paul", namefile="test", namefolder="folder")

    def third(
        name: str = "name", name_file: str = "file", name_folder: str = "folder", name_files: str = "folder"
    ):
        return locals()

    cmd = Command(third, make_shorts=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-n", "--name"]
    assert cmd.arguments[1].option_strings == ["-N", "--name-file"]
    assert cmd.arguments[2].option_strings == ["-nf", "--name-folder"]
    assert cmd.arguments[3].option_strings == ["-na", "--name-files"]

    assert cmd.run([]) == dict(name="name", name_file="file", name_folder="folder", name_files="folder")


def test_force_make_shorts_until_total():
    def main(foo: str = "dio", fo: int = 42, fos: int = 42, fox: int = 42, fob: int = 77):
        return locals()

    cmd = Command(main, make_shorts=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo"]
    assert cmd.arguments[1].option_strings == ["-F", "--fo"]
    assert cmd.arguments[2].option_strings == ["-fo", "--fos"]
    assert cmd.arguments[3].option_strings == ["-FO", "--fox"]
    assert cmd.arguments[4].option_strings == ["-fob", "--fob"]
    assert cmd.run("-f diogo -F 1 -fo 2 -FO 3 -fob 4".split()) == {
        "foo": "diogo",
        "fo": 1,
        "fos": 2,
        "fox": 3,
        "fob": 4,
    }
