# example1.py
import clig

def greetage(name: str, age: int):
    print(f"{name} is {age} years old")

clig.run(greetage)