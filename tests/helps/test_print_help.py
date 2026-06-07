import clig
from resources import CapSys


def test_enum(capsys: CapSys):

    def main(a=1, b=2):
        """Documentation for main function"""
        return locals()

    cmd = clig.Command(main)
    cmd.print_help()
    output = capsys.readouterr().out
    assert "Documentation for main function" in output
    assert "--a" in output
    assert "--b" in output
