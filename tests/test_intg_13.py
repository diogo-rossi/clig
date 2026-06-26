import pytest
from resources import CapSys
from clig import Arg, data, run, MutuallyExclusiveGroup

help13_a1 = """
usage: main1 [-h] -f FOO

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
""".strip()

error13_a1 = """
usage: main1 [-h] -f FOO
main1: error: one of the arguments -f/--foo is required
""".strip()


def test_test_intg_13_a1(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=True)

    def main1(foo: Arg[str, data("-f", group=g)]):
        return locals()

    with pytest.raises(SystemExit) as e:
        run(main1, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help13_a1 in output

    with pytest.raises(SystemExit) as e:
        run(main1, [])

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert error13_a1 in output


help13_a2 = """
usage: main2 [-h] (-f FOO | -b BAR)

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
  -b BAR, --bar BAR
""".strip()

error13_a2 = """
usage: main2 [-h] (-f FOO | -b BAR)
main2: error: one of the arguments -f/--foo -b/--bar is required
""".strip()


def test_test_intg_13_a2(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=True)

    def main2(foo: Arg[str, data("-f", group=g)], bar: Arg[int, data("-b", group=g)]):
        return locals()


help13_a3 = """
usage: main3 [-h] (--foo FOO | --bar BAR)

options:
  -h, --help  show this help message and exit
  --foo FOO
  --bar BAR
""".strip()

error13_a3 = """
usage: main3 [-h] (--foo FOO | --bar BAR)
main3: error: one of the arguments --foo --bar is required
""".strip()


def test_test_intg_13_a3(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=True)

    def main3(foo: Arg[str, data(group=g)] = "aaa", bar: Arg[int, data(group=g)] = 42):
        return locals()


help13_b1 = """
usage: main1 [-h] [-f FOO]

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
""".strip()


def test_test_intg_13_b1(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=False)

    def main1(foo: Arg[str, data("-f", group=g)]):
        return locals()

    with pytest.raises(SystemExit) as e:
        run(main1, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help13_b1 in output

    assert run(main1, "--foo test".split()) == {"foo": "test"}
    assert run(main1, "-f testing".split()) == {"foo": "testing"}


help13_b2 = """
usage: main2 [-h] [-f FOO | -b BAR]

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
  -b BAR, --bar BAR
""".strip()

error13_b2 = """
usage: main2 [-h] [-f FOO | -b BAR]
main2: error: argument -b/--bar: not allowed with argument -f/--foo
""".strip()


def test_test_intg_13_b2(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=False)

    def main2(foo: Arg[str, data("-f", group=g)], bar: Arg[int, data("-b", group=g)]):
        return locals()

    with pytest.raises(SystemExit) as e:
        run(main2, ["--help"])

    assert e.value.code == 0
    output = capsys.readouterr().out
    assert help13_b2 in output

    with pytest.raises(SystemExit) as e:
        run(main2, ["-f", "test", "-b", "32"])

    assert e.value.code == 2
    output = capsys.readouterr().err
    assert error13_b2 in output


help13_b3 = """
usage: main3 [-h] [--foo FOO | --bar BAR]

options:
  -h, --help  show this help message and exit
  --foo FOO
  --bar BAR
""".strip()

error13_b3 = """
usage: main3 [-h] [--foo FOO | --bar BAR]
main3: error: argument --bar: not allowed with argument --foo
""".strip()


def test_test_intg_13_b3(capsys: CapSys):

    g = MutuallyExclusiveGroup(required=False)

    def main3(foo: Arg[str, data(group=g)] = "aaa", bar: Arg[int, data(group=g)] = 42):
        return locals()
