# Advanced features

The Command Line Interface created with `clig` can be customized in some ways
already provided by the
[argparse](https://docs.python.org/3/library/argparse.html) module. Besides,
other additional parameters can be used to add extra customization.
## Arguments for `clig.run()` function

The first parameter of the `clig.run()` function is normally the function turned
into the command.

The second positional parameter of the function could be the
[list of strings to pass to the commad inside the code](https://docs.python.org/3/library/argparse.html#args)
(which is defaulted to `sys.argv`).

However, other parameters can be passed as keyword arguments. They are the
parameters of the original
[`ArgumentParser()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)
constructor and some new extra parameters.

### Arguments of the original `parse_args()` method

[`parse_args()`](https://docs.python.org/3/library/argparse.html#the-parse-args-method)
method

### Calling `clig.run()` without a function
```python
# context-example01.py
import clig

def modi(s: str) -> str:
    return s.lower()

def main(foo: str, bar: int):
    return locals()

clig.run(main, metavarmod=modi)
```
```
> python context-example01.py -h

usage: main [-h] foo bar

positional arguments:
  foo
  bar

options:
  -h, --help  show this help message and exit
```
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
>>> def main(name: str, age: int, height: float):
...     """The main command
... 
...     This is my main command
... 
...     Args:
...         name: The name of the person
...         age: The age of the person
...         height: The height of the person
...     """
...     print(locals())
... 
>>> def second():
...     """A function witout arguments
... 
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
# context-example02.py
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
```
> python context-example02.py bazinga 32 second 22.5

Arguments in the top level command: {'foo': 'bazinga', 'bar': 32}
Running now the second command . . .
The 'foo' argument from the previous command was: foo = bazinga
```
```python
# context-example03.py
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
```
> python context-example03.py shazan 23 second 74.9

{'foo': 'shazan', 'bar': 23}
foo value = shazan
```
```python
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
sub1: <function sub1 at 0x000001C150569120>
sub2: <function sub2 at 0x000001C1505693A0>
```
### Method decorator with argument
### Function decorator with argument
## An solved issue with [`argparse`](https://docs.python.org/3/library/argparse.html) subparsers

There is a know `argparse` behavior that happens when you have subparsers with
same argument names, which may be seen as an issue.

Normally, all arguments are gathered in one
[`Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace):
```python
>>> from argparse import ArgumentParser
... 
>>> parser = ArgumentParser()
>>> parser.add_argument("--foo")
>>> subcommand = parser.add_subparsers()
>>> subcommand = subcommand.add_parser("subcommand")
>>> subcommand.add_argument("--bar")
>>> parser.parse_args(["--foo", "span", "subcommand", "--bar", "cheese"])
Namespace(foo='span', bar='cheese')
```
The issue is generated when you have subparsers with same argument names.  
Imagine you have the following subcommand structure:

```
parser
├─── argument "--name"
└─── subparser
     └───  argument "--name"
```

That would be built in `argparse` with:
```python
>>> from argparse import ArgumentParser
... 
>>> parser = ArgumentParser()
>>> parser.add_argument("--name")
>>> subcommand = parser.add_subparsers()
>>> subcommand = subcommand.add_parser("subcommand")
>>> subcommand.add_argument("--name")
```
Parsing the argument individually to each parser works ok:
```python
>>> parser.parse_args(["--name", "jean"])
Namespace(name='jean')
>>> parser.parse_args(["subcommand", "--name", "rose"])
Namespace(name='rose')
```
But using the whole command line gets an unexpected behavior → Only the last
argument value passed is stored:
```python
>>> parser.parse_args(["--name", "monica", "subcommand", "--name", "joe"])
Namespace(name='joe')
```
`clig` solves that issue before passing argument to the functions:
```python
>>> import clig
... 
>>> def main(name: str = ""):
...     print(locals())
... 
>>> def subcommand(name: str = ""):
...     print(locals())
... 
>>> cmd = clig.Command(main).add_subcommand(subcommand)
>>> cmd.run(["--name", "monica", "subcommand", "--name", "joe"])
{'name': 'monica'}
{'name': 'joe'}
```
The solution applied by `clig` is changing the argument names at runtime: Blank
spaces (`" "`) are appended to them, which are stripped when passing argument to
the functions. That can be inspected with the [`Context`](#context) object
approach:
```python
>>> import clig
... 
>>> def main(name: str = ""):
...     print(locals())
... 
>>> def subcommand(ctx: clig.Context, name: str = ""):
...     args = locals().copy()
...     args.pop("ctx")
...     print(args)
...     print(ctx.namespace)
... 
>>> cmd = clig.Command(main).add_subcommand(subcommand)
>>> cmd.run(["--name", "monica", "subcommand", "--name", "joe"])
{'name': 'monica'}
{'name': 'joe'}
Namespace(name='monica', **{'{subcommand}': 'subcommand', 'name ': 'joe'})
```
You don't need to know that internal solution in most cases. But, in cases when
you are using subparsers that access `Context` object with the whole `namespace`
attribute, then you may want to know how the
[`Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace)
object will look.
