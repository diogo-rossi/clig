from typing import Literal
from enum import Enum
import clig


class Color(Enum):
    red = 1
    blue = 2
    yellow = 3


def main(color: Literal[Color.red, "azul", "preto"]):
    print(f"Passed arguments to function: {locals()}")
    return locals()


def test_intg_01_Literal_Enum_Color():
    assert clig.run(main, ["red"]) == {"color": Color(1)}
