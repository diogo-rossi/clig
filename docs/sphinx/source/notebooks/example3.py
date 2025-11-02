# example3.py
import clig

def greetage(name: str, age: int, ask: bool):
    print(f"Hello {name}! I am {age} yeats old.")
    if ask:
        print("How old are you?")

clig.run(greetage)