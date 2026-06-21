import clig


def main(name: tuple[str, str], ages: tuple[int, int] | None = None, height: float | None = 32):
    return locals()


def test_intg_08_tuple():

    assert clig.run(main, "diogo bia --ages 45 56 --height 32365".split()) == {
        "name": ("diogo", "bia"),
        "ages": (45, 56),
        "height": 32365,
    }

    assert clig.run(main, "jon mary --ages 23 24".split()) == {
        "name": ("jon", "mary"),
        "ages": (23, 24),
        "height": 32,
    }
