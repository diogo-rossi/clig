# example2.py
from typing import Sequence
import clig

def main(
    foo: tuple[str, str],
    bar: list[int],
):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)