# example0.py

import clig


def greetings(name, greet="Hello"):
    """Description of the command: A greeting prompt!

    Args:
        name (s): The name to greet
        greet (str, optional): The greeting used. Defaults to "Hello".
    """
    print(f"Greetings: {greet} {name}!")


clig.run(greetings)
