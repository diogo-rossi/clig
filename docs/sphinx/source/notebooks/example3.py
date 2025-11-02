# example3.py
from typing import Literal
import clig

def main(
    foo: tuple[str, str],
    bar: list[int],
    move: Literal["rock", "paper", "scissors"],
):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)