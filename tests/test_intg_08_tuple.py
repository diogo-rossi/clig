import clig
from argparse import ArgumentParser


def main(name: tuple[str, str], ages: tuple[int, int] | None = None, height: float | None = 32):
    return locals()


parser = ArgumentParser()
parser.add_argument("name", nargs=2, type=str)
parser.add_argument("--ages", nargs=2, type=int, default=None)
parser.add_argument("--height", type=float, default=32)


def test_intg_08_tuple():

    args = "diogo bia --ages 45 56 --height 32365".split()
    assert clig.run(main, args) == {"name": ("diogo", "bia"), "ages": (45, 56), "height": 32365}
    assert vars(parser.parse_args(args)) == {"name": ["diogo", "bia"], "ages": [45, 56], "height": 32365}

    args = "jon mary --ages 23 24".split()
    assert clig.run(main, args) == {"name": ("jon", "mary"), "ages": (23, 24), "height": 32}
    assert vars(parser.parse_args(args)) == {"name": ["jon", "mary"], "ages": [23, 24], "height": 32}
