from clig import Arg, data, run


def bar(name: str, size: Arg[float, data(nargs="?", const=456, required=True)]):
    return locals()


def test_intg_07_nargs():
    assert run(bar, ["rocky"]) == {"name": "rocky", "size": None}
    assert run(bar, ["rocky", "1.5"]) == {"name": "rocky", "size": 1.5}
