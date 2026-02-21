import clig.clig as clig


def maincmd():
    pass


def foobar():
    """This is a show description.

    This is a very long description that should not appear in the short help of subcommand, because the short
    help only contains one single line of information.
    """
    pass


def test_help_subcommand():
    cmd = clig.Command(maincmd)
    subcmd = cmd.new_subcommand(foobar)
    assert subcmd.help == "This is a show description."
    assert subcmd.description == clig._normalize_docstring(foobar.__doc__)
