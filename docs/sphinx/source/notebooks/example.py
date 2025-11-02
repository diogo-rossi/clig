# example.py

import clig


def greetings(name, greet="Hello"):
    print(f"Greetings: {greet} {name}!")


clig.run(greetings)
