from pathlib import Path
from enum import StrEnum
import clig


class Color(StrEnum):
    red = "red"
    blue = "blue"
    yellow = "yellow"


def main_int(a: int | Path):
    return locals()


def main_path(a: Path | int):
    return locals()


def test_intg_03_convert_int():
    assert clig.run(main_int, ["1"]) == {"a": 1}
    assert clig.run(main_int, ["32"]) == {"a": 32}
    assert clig.run(main_int, ["somedir"]) == {"a": Path("somedir")}


def test_intg_03_convert_path():
    assert clig.run(main_path, ["1"]) == {"a": Path("1")}
    assert clig.run(main_path, ["32"]) == {"a": Path("32")}
