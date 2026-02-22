from clig import Command, Arg, data


def foobar(myarg: str):
    """Summary

    Parameters
    ----------
    - `myarg` (`str`):
        Help for myarg.
    """
    return locals()


def modarglevel(myarg: Arg[str, data(helpmodifier=lambda s: f"{s} This is modified at argument level.")]):
    """Summary

    Parameters
    ----------
    - `myarg` (`str`):
        Help for myarg.
    """
    return locals()


def modarglevel_with_help(
    myarg: Arg[
        str, data(helpmodifier=lambda s: f"{s} This is modified at argument level.", help="other help")
    ],
):
    """Summary

    Parameters
    ----------
    - `myarg` (`str`):
        Help for myarg.
    """
    return locals()


def test_nohelpmodifier():
    cmd = Command(foobar)
    cmd.run(["anyvalue"])
    assert cmd.arguments[0].help == "Help for myarg."


def test_helpmodifier():
    cmd = Command(foobar, helpmodifier=lambda s: f"{s} Modified by command.")
    cmd.run(["anyvalue"])
    assert cmd.arguments[0].help == "Help for myarg. Modified by command."


def test_poshelpmodifier():
    cmd = Command(
        foobar,
        helpmodifier=lambda s: f"{s} Modified by command.",
        poshelpmodifier=lambda s: f"{s} Modified by command for pos parameters.",
    )
    cmd.run(["anyvalue"])
    assert cmd.arguments[0].help == "Help for myarg. Modified by command for pos parameters."


def test_arglevelhelpmodifier():
    cmd = Command(
        modarglevel,
        helpmodifier=lambda s: f"{s} Modified by command.",
        poshelpmodifier=lambda s: f"{s} Modified by command for pos parameters.",
    )
    cmd.run(["anyvalue"])
    assert cmd.arguments[0].help == "Help for myarg. This is modified at argument level."


def test_arglevelhelpmodifier_with_help():
    cmd = Command(
        modarglevel_with_help,
        helpmodifier=lambda s: f"{s} Modified by command.",
        poshelpmodifier=lambda s: f"{s} Modified by command for pos parameters.",
    )
    cmd.run(["anyvalue"])
    assert cmd.arguments[0].help == "other help This is modified at argument level."
