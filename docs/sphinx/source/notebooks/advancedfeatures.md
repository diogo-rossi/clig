# Advanced features


```python
... 
```
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
## Context




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
    Command(func=<function first at 0x00000201158BD940>, prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=<class 'argparse.RawTextHelpFormatter'>, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True, exit_on_error=True, subcommands_title='subcommands', subcommands_description=None, subcommands_prog=None, subcommands_required=False, subcommands_help=None, subcommands_metavar=None, name='first', help=None, aliases=[], docstring_template=None, default_bool=False, make_flags=None, make_shorts=None, parent=None, parser=ArgumentParser(prog='first', usage=None, description=None, formatter_class=<class 'argparse.RawTextHelpFormatter'>, conflict_handler='error', add_help=True))
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
sub1: <function sub1 at 0x000001A611DAB240>
sub2: <function sub2 at 0x000001A611DA9F80>

```
## Method decorator with argument

## Function decorator with argument
