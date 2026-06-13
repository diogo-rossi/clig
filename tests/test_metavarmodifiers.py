import clig
from clig import Arg, data


def test_optmetavarmodifier1():
    def myfun(aba: str = "hello", gue: str = "world"):
        return locals()

    cmd = clig.Command(myfun, optmetavarmodifier=lambda s: f"<{s.lower()}>")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "<aba>"
    assert cmd.arguments[1].metavar == "<gue>"

    assert cmd.run("--aba hi --gue city".split()) == {"aba": "hi", "gue": "city"}
    assert cmd.run([]) == {"aba": "hello", "gue": "world"}


def test_optmetavarmodifier2():
    def myfun(path_prefix: str = "users", user_age: int = 0):
        return locals()

    cmd = clig.Command(myfun, optmetavarmodifier=lambda s: f"{s.replace("_","-")}")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "path-prefix"
    assert cmd.arguments[1].metavar == "user-age"

    cmd = clig.Command(myfun, optmetavarmodifier=lambda s: f"{s.upper()}")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "PATH_PREFIX"
    assert cmd.arguments[1].metavar == "USER_AGE"

    cmd = clig.Command(myfun, optmetavarmodifier=lambda s: f"<{s.replace('_','-')}>")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "<path-prefix>"
    assert cmd.arguments[1].metavar == "<user-age>"

    assert cmd.run("--path-prefix home --user-age 18".split()) == {"path_prefix": "home", "user_age": 18}


def test_posmetavarmodifier():
    def myfun(my_arg_test):
        return locals()

    cmd = clig.Command(myfun, posmetavarmodifier=lambda s: f"{s.capitalize()}")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "My_arg_test"

    cmd = clig.Command(myfun, posmetavarmodifier=lambda s: f"{s.replace("_","--").capitalize()}")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "My--arg--test"

    assert cmd.run(["argument"]) == {"my_arg_test": "argument"}


def test_metavarmodifier_example1():
    def myfun(bar, foo=None):
        return locals()

    cmd = clig.Command(myfun, posmetavarmodifier="XXXX", optmetavarmodifier="YYYY")
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == "XXXX"
    assert cmd.arguments[1].metavar == "YYYY"

    assert cmd.run(["25"]) == dict(bar="25", foo=None)
    assert cmd.run(["test", "--foo", "25"]) == dict(bar="test", foo="25")


def test_metavarmodifier_example2():
    def prog(
        x: Arg[str, data("-x", make_flag=False, nargs=2, metavar=None)], foo: tuple[str, str] | None = None
    ):
        return locals()

    cmd = clig.Command(prog, prog="PROG", optmetavarmodifier=("bar", "baz"))
    cmd._add_parsers()
    assert cmd.arguments[0].metavar == None
    assert cmd.arguments[1].metavar == ("bar", "baz")

    assert cmd.arguments[0].option_strings == ["-x"]
    assert cmd.arguments[1].option_strings == ["--foo"]

    assert cmd.run("-x 25 32".split()) == {"x": ["25", "32"], "foo": None}
    assert cmd.run("-x test name --foo zero mega".split()) == {"x": ["test", "name"], "foo": ("zero", "mega")}
