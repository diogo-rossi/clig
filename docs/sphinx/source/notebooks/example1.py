# example1.py

import clig


def greetage(name: str, age: int, greet="Hello", askback: bool = False):
    print(f"{greet} {name}! I am {age} yeats old.")
    if askback:
        print("How old are you?")


clig.run(greetage)
