# example6.py
from typing import Literal
from enum import Enum
import clig

class Color(Enum):
    red = 1
    blue = 2
    yellow = 3

def main(color: Color):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)