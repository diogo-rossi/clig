# Advanced features

## Arguments for `clig.run()` function

### Arguments of the original `parse_args()` method

[`parse_args()`](https://docs.python.org/3/library/argparse.html#the-parse-args-method)
method

### Calling `clig.run()` without a function

## Arguments for `clig.Command()` constructor

### Arguments of the original `ArgumentParser()` method

[`ArgumentParser()`](https://docs.python.org/3/library/argparse.html#argumentparser-objects)
method

### Calling `clig.Command()` without a function

## Helps

### Docstring templates

### Helps in arguments

### Helps in subcommands

### Append and prepend to helps

## Flags creations

### Long flags creation

### Short flag creation

### Force flag in argument 

## Subcommands


```python
>>> from clig import Command
... 
>>> @Command
... def main(name: str, age: int, height: float):
...     """The main command
...     This is my main command
...     Args:
...         name: The name of the person
...         age: The age of the person
...         height: The height of the person
...     """
...     print(locals())
... 
>>> def second():
...     """A function witout arguments
...     This functions runs without arguments
...     """
...     print(locals())
... 
>>> subcmd = main.new_subcommand(second)
... 
>>> main.print_help()
usage: main [-h] name age height {second} ...

The main command

positional arguments:
name        The name of the person
age         The age of the person
height      The height of the person

options:
-h, --help  show this help message and exit

subcommands:
{second}
second    A function witout arguments

This functions runs without arguments

This is my main command

```
### Context




```python
# context-example01.py
import clig

@clig.command
def first(foo: str, bar: int):
    print(f"Arguments in the top level command: {locals()}")

@clig.subcommand
def second(ctx: clig.Context, ham: float):
    print("Running now the second command . . .")
    print(f"The 'foo' argument from the previous command was: foo = {ctx.namespace.foo}")

clig.run()
```


```bash
> python context-example01.py bazinga 32 second 22.5

    Arguments in the top level command: {'foo': 'bazinga', 'bar': 32}
    Running now the second command . . .
    The 'foo' argument from the previous command was: foo = bazinga
    
```

```python
# context-example02.py
from typing import Protocol
from clig import Command, Context

class MyProtocol(Protocol):
    foo: str
    bar: int

def first(foo: str, bar: int):
    print(locals())

def second(ctx: Context[MyProtocol], ham: float):
    foo_value: str = ctx.namespace.foo  # --> recognized by type checkers / intellisense
    print("foo value = " + foo_value)

Command(first).add_subcommand(second).run()
```


```bash
> python context-example02.py shazan 23 second 74.9

    {'foo': 'shazan', 'bar': 23}
    foo value = shazan
    >>> from clig import Command, Context
... 
>>> def main(foo: str, bar: int):
...     print(f"Running main with: {locals()}")
... 
>>> def sub1(ctx: Context, ham: float):
...     print(f"Top level command name = {ctx.command.name}")
... 
>>> def sub2(ctx: Context, baz: bool):
...     print("Subcommand functions:")
...     for cmd in ctx.command.sub_commands:
...         print(f"{cmd}: {ctx.command.sub_commands[cmd].func}")
... 
>>> command = Command(main).add_subcommand(sub1).add_subcommand(sub2)
>>> command.run(["hello", "23", "sub1", "32.5"])
Running main with: {'foo': 'hello', 'bar': 23}
Top level command name = main
>>> command.run(["hello", "23", "sub2", "--baz"])
Running main with: {'foo': 'hello', 'bar': 23}
Subcommand functions:
sub1: <function sub1 at 0x000002A802A2DD00>
sub2: <function sub2 at 0x000002A802BA8540>

```
### Method decorator with argument

### Function decorator with argument
