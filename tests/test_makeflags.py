import sys
from pathlib import Path

this_dir = Path(__file__).parent

sys.path.insert(0, str((this_dir).resolve()))
sys.path.insert(0, str((this_dir / "../src").resolve()))

from clig.clig import Arg, data, Command


def test_make_flag_on_argument_automatically():
    def main(foobar: Arg[str, data("-f")]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foobar"]


def test_donot_make_flag_on_argument_automatically():
    def main(foobar: Arg[str, data("-f", "--foo")]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo"]


def test_force_make_flag_on_argument_automatically():
    def main(foobar: Arg[str, data("-f", "--foo", make_flag=True)]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo", "--foobar"]


def test_force_make_flag_on_argument_automatically_in_command():
    def main(foobar: Arg[str, data("-f", "--foo")]):
        return locals()

    cmd = Command(main, make_flags=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo", "--foobar"]


def test_force_donot_make_flag_on_argument():
    def main(foobar: Arg[str, data("-f", make_flag=False)]):
        return locals()

    cmd = Command(main)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f"]


def test_force_donot_make_flag_in_command():
    def main(foobar: Arg[str, data("-f")]):
        return locals()

    cmd = Command(main, make_flags=False)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f"]


def test_conflict_force_make_flags_true_on_argument():
    def main(foobar: Arg[str, data("-f", "--foo", make_flag=True)], bazham: Arg[str, data("-b")]):
        return locals()

    cmd = Command(main, make_flags=False)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo", "--foobar"]
    assert cmd.arguments[1].option_strings == ["-b"]


def test_conflict_force_make_flags_true_on_command():
    def main(foobar: Arg[str, data("-f", "--foo", make_flag=False)], bazham: Arg[str, data("-b", "--baz")]):
        return locals()

    cmd = Command(main, make_flags=True)
    cmd._add_parsers()
    assert cmd.arguments[0].option_strings == ["-f", "--foo"]
    assert cmd.arguments[1].option_strings == ["-b", "--baz", "--bazham"]
