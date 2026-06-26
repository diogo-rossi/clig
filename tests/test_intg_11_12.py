from clig import Arg, data, run


def test_test_intg_11():
    def main(foo: Arg[list[int], data(action="append_const", const=666)] = [0]):
        return locals()

    assert run(main, "--foo --foo".split()) == {"foo": [0, 666, 666]}


def test_test_intg_12():
    def main(foo: Arg[list[int], data(action="extend")] = [0]):
        return locals()

    assert run(main, "--foo 23 --foo 45 89".split()) == {"foo": [0, 23, 45, 89]}
