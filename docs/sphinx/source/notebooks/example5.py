# example5.py
from typing import Literal
import clig

def main(name: str, move: Literal["rock", "paper", "scissors"]):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)