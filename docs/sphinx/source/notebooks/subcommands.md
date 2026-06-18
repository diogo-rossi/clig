# Subcommands

Instead of using the function [`clig.run()`](clig.run) described in the
[userguide](./userguide.md), you can create an object instance of the type
[`Command`](clig.Command), passing your function to its constructor, and call
the [`Command.run()`](clig.Command.run) method.

```python
# prog01.py
from clig import Command

def main(name:str, age: int, height: float):
    print(locals())

cmd = Command(main)
cmd.run()
```

```none
> python prog01.py "Carmem Miranda" 42 1.85

{'name': 'Carmem Miranda', 'age': 42, 'height': 1.85}
```

This makes it possible to use some methods to add
[subcommands](https://docs.python.org/3/library/argparse.html#subcommands). All
subcommands will also be instances of the same class [`Command`](clig.Command).
There are 4 main methods available:

1. [`Command.new_subcommand`](clig.Command.new_subcommand):

   Creates a subcommand and returns the new created [`Command`](clig.Command)
   instance.

2. [`Command.add_subcommand`](clig.Command.add_subcommand):

   Creates the subcommand and returns the caller object. This is useful to add
   multiple subcommands [in one single line](#all-cli-in-one-statement).

3. [`Command.end_subcommand`](clig.Command.end_subcommand):

   Creates the subcommand and returns the parent of the caller object. If the
   caller doesn't have a parent, an error will be raised. This is useful when
   finishing to add subcommands in the object on a single line.

4. [`Command.subcommand`](clig.Command.subcommand):

   Creates the subcommand and returns the input function unchanged. This is a
   proper method to be used as a
   [function decorator](https://docs.python.org/3/glossary.html#term-decorator).

There are also
[2 module level functions](#subcommands-using-function-decorators):
[`clig.command()`](clig.command) and [`clig.subcommand()`](clig.subcommand).
They also returns the functions unchanged, and so may also be used as
decorators.

All the functions declared as commands execute sequentially, from a
[`Command`](clig.Command) to its subcommands.

The [`Command`](clig.Command) constructor also accepts other arguments to
customize the interface, and also has other methods, like
[`print_help()`](clig.Command.print_help), analog to the
[original method](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.print_help).

## Subcommands using methods

The methods [`new_subcommand`](clig.Command.new_subcommand) and
[`add_subcommand`](clig.Command.add_subcommand) can be used to add subcommands
in an usual object oriented code.

Consider the case below, with 2 levels of subcommands:

```
prog
├─── subfunction1
└─── subfunction2
            └─── subsubfunction
```

You can create the main command object and add subcommands to it after:

```python
>>> from clig import Command
>>> def prog(name: str, age: int):
...     print(locals())
...
>>> def subfunction1(height: float):
...     print(locals())
...
>>> def subfunction2(father: str, mother: str):
...     print(locals())
...
>>> def subsubfunction(city: str, state: str):
...     print(locals())
...
>>> # defines the main object
>>> cmd = Command(prog)
...
>>> # adds a subcommand to the main object
>>> cmd.add_subcommand(subfunction1)
...
>>> # adds and returns a new created subcommand object
>>> sub = cmd.new_subcommand(subfunction2)
...
>>> # adds a subcommand to the subcommand object
>>> sub.add_subcommand(subsubfunction)
...
>>> # main command help
>>> cmd.print_help()
usage: prog [-h] name age {subfunction1,subfunction2} ...

positional arguments:
  name
  age
  {subfunction1,subfunction2}

options:
  -h, --help            show this help message and exit
```

> ![NOTE]  
> To separate the subcommands section from the "positional arguments" and give
> it another title, see the
> [parameters can be passed to the `Command` constructor](./advancedfeatures.md#parameters-of-the-original-argumentparseradd_subparsers-object).

Subcommands are correctly handled with their
[subparsers](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers).

```python
>>> # subcommand help
>>> sub.print_help()
usage: prog name age subfunction2 [-h] father mother {subsubfunction} ...

positional arguments:
  father
  mother
  {subsubfunction}

options:
  -h, --help        show this help message and exit
```

Remember that the command functions execute sequentially, from a
[`Command`](clig.Command) to its subcommands.

```python
>>> # run the main comand with all subcommands
>>> cmd.run("jack 23 subfunction2 michael suzan subsubfunction santos SP".split())
{'name': 'jack', 'age': 23}
{'father': 'michael', 'mother': 'suzan'}
{'city': 'santos', 'state': 'SP'}
...
>>> # run only the subcommand with its subcommand
>>> sub.run(["jean", "karen", "subsubfunction", "campos", "RJ"])
{'father': 'jean', 'mother': 'karen'}
{'city': 'campos', 'state': 'RJ'}
```

To access the attributes of a command inside the functions of its subcommands,
check out the feature of the [`Context`](#context) object.

### All CLI in one statement

By using the 3 methods [`new_subcommand`](clig.Command.new_subcommand),
[`add_subcommand`](clig.Command.add_subcommand) and
[`end_subcommand`](clig.Command.end_subcommand) you can define the whole
interface in one single statement (one line of code).

To give a clear example, consider the [Git](https://git-scm.com/) cli interface.
Some of its command's hierarchy is the following:

```
git
├─── status
├─── commit
├─── remote
│    ├─── add
│    ├─── rename
│    └─── remove
└─── submodule
     ├─── init
     └─── update
```

Then, the functions could be declared in the following structure, with the CLI
definition at the end:

```python
# prog02.py
from inspect import getframeinfo, currentframe
from pathlib import Path
from clig import Command

def git(exec_path: Path = Path("git"), work_tree: Path = Path("C:/Users")):
    """The git command line interface"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def status(branch: str):
    """Show the repository status"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def commit(message: str):
    """Record changes to the repository"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def remote(verbose: bool = False):
    """Manage remote repositories"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def add(name: str, url: str):
    """Add a new remote"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def rename(old: str, new: str):
    """Rename an existing remote"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def remove(name: str):
    """Remove the remote reference"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def submodule(quiet: bool):
    """Manages git submodules"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def init(path: Path = Path(".").resolve()):
    """Initialize the submodules recorded in the index"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

def update(init: bool, path: Path = Path(".").resolve()):
    """Update the registered submodules"""
    print(f"Command: {getframeinfo(currentframe()).function} | Arguments: {locals()}")

######################################################################################
# The whole interface is built in the code below
# It could also be placed in a separated file importing the functions

(
    Command(git)
    .add_subcommand(status)
    .add_subcommand(commit)
    .new_subcommand(remote)
        .add_subcommand(add)
        .add_subcommand(rename)
        .end_subcommand(remove)
    .new_subcommand(submodule)
        .add_subcommand(init)
        .end_subcommand(update)
    .run()
)

```

Help for the main command:

```none
> python prog02.py -h

usage: git [-h] [--exec-path EXEC_PATH] [--work-tree WORK_TREE]
           {status,commit,remote,submodule} ...

The git command line interface

positional arguments:
  {status,commit,remote,submodule}
    status              Show the repository status
    commit              Record changes to the repository
    remote              Manage remote repositories
    submodule           Manages git submodules

options:
  -h, --help            show this help message and exit
  --exec-path EXEC_PATH
  --work-tree WORK_TREE
```

Help for the `remote` subcomand:

```none
> python prog02.py remote -h

usage: git remote [-h] [--verbose] {add,rename,remove} ...

Manage remote repositories

positional arguments:
  {add,rename,remove}
    add                Add a new remote
    rename             Rename an existing remote
    remove             Remove the remote reference

options:
  -h, --help           show this help message and exit
  --verbose
```

Help for the `remote rename` subcommand:

```none
> python prog02.py remote rename -h

usage: git remote rename [-h] old new

Rename an existing remote

positional arguments:
  old
  new

options:
  -h, --help  show this help message and exit
```

Remember: the command functions execute sequentially, from a
[`Command`](clig.Command) to its subcommands.

```none
> python prog02.py remote rename oldName newName

Command: git | Arguments: {'exec_path': WindowsPath('git'), 'work_tree': WindowsPath('C:/Users')}
Command: remote | Arguments: {'verbose': False}
Command: rename | Arguments: {'old': 'oldName', 'new': 'newName'}
```

## Subcommands using method decorators

You can define subcommands using the
[`Command.subcommand()`](clig.Command.subcommand) method as a decorator. To do
it, first create a [`Command`](clig.Command) instance. The decorator only
registries the functions as commands (it doesn't change their definitions).

```python
# prog03.py
from clig import Command

def main(verbose: bool = False):
    """Description for the main command"""
    print(f"{locals()}")

# create the command object
cmd = Command(main)

@cmd.subcommand
def foo(a, b):
    """Help for foo sub command"""
    print(f"{locals()}")

@cmd.subcommand
def bar(c, d):
    """Help for bar sub command"""
    print(f"{locals()}")

cmd.run()
```

```none
> python prog03.py -h

usage: main [-h] [--verbose] {foo,bar} ...

Description for the main command

positional arguments:
  {foo,bar}
    foo       Help for foo sub command
    bar       Help for bar sub command

options:
  -h, --help  show this help message and exit
  --verbose
```

> [!NOTE]  
> The `cmd` object in the example above could also be created
> [without a function argument](./advancedfeatures.md#calling-cligcommand-without-a-function)
> (i.e., `cmd = Command()`)

### Using the `Command()` constructor as a decorator

You could also use de `Command()` constructor as a
[decorator](https://docs.python.org/3/glossary.html#term-decorator). However,
that would redefine the function name as a `Command` instance.

```python
>>> from clig import Command
>>> def main():
...     pass
...
>>> cmd = Command(main) # the `main` function is not affected with this
>>> print(type(main))
<class 'function'>
...
>>> # this will change the `main` function!
>>> @Command
>>> def main():
...     pass
...
>>> print(type(main)) # now the main function is a `Command` instance
<class 'clig.clig.Command'>
```

### Adding internal level of subcommads with decorators

By using the [`@Command.subcommand`](clig.Command.subcommand) decorator without
arguments, the functions are not modified but you won't be able to define more
than one level of subcommands,
[unless you pass an `parent` argument to the decorator](#method-decorator-with-arguments).

However, by knowing the fact that subcommads are registered in a
[`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
attribute defined as [`Command.subcommands`](clig.Command.subcommands), it it is
possible to use it directly, by knowing the subcommad
[`name`](clig.Command.name), calling the respective
[`subcommand`](clig.Command.subcommand) decorator.

```python
# prog04.py
from clig import Command

def prog(name: str = "mario", age: int = 40):
    print(locals())

# defines the main object and adds subcommands

cmd = Command(prog)

@cmd.subcommand
def subfunction1(height: float):
    print(locals())

@cmd.subcommand
def subfunction2(father: str, mother: str):
    print(locals())

# now use the attribute `subcommands` to add another level of subcommands

@cmd.subcommands["subfunction2"].subcommand
def subsubfunction(city: str, state: str):
    print(locals())

cmd.run()
```

```none
> python prog04.py -h

usage: prog [-h] [--name NAME] [--age AGE] {subfunction1,subfunction2} ...

positional arguments:
  {subfunction1,subfunction2}

options:
  -h, --help            show this help message and exit
  --name NAME
  --age AGE
```

```none
> python prog04.py subfunction2 -h

usage: prog subfunction2 [-h] father mother {subsubfunction} ...

positional arguments:
  father
  mother
  {subsubfunction}

options:
  -h, --help        show this help message and exit
```

### Method decorator with arguments

The [`@Command.subcommad`](clig.Command.subcommad) decorator accepts all
arguments that creates a new [`Command`](clig.Command) instance, check them
[on the their docs](./advancedfeatures.md#).

A particular argument used to create more levels of subcommands is the `parent`
argument, which accepts a subcommad name, or its function object.

```python
# prog05.py
from clig import Command

def prog(name: str = "mario", age: int = 40):
    print(locals())

# First, defines the main object and adds on subcommand

cmd = Command(prog)

@cmd.subcommand
def subfunction(height: float):
    print(locals())

# now use the parent argument, with the function object

@cmd.subcommand(parent=subfunction)
def internalsubfunction(city: str, state: str):
    print(locals())

cmd.run()
```

```none
> python prog05.py --help

usage: prog [-h] [--name NAME] [--age AGE] {subfunction} ...

positional arguments:
  {subfunction}

options:
  -h, --help     show this help message and exit
  --name NAME
  --age AGE
```

```none
> python prog05.py subfunction --help

usage: prog subfunction [-h] height {internalsubfunction} ...

positional arguments:
  height
  {internalsubfunction}

options:
  -h, --help            show this help message and exit
```

## Subcommands using function decorators

As it was noticed in the previous section, using decorators without the `parent`
argument does not allow you to declare more than one level of subcommands, when
you don't use the [`subcommands`](clig.Command.subcommands) attribute,
[calling methods from its elements](#adding-subcommads-with-decorators).

For these simple cases, it is more convenient to use the module level functions
[`clig.command()`](clig.command) and [`clig.subcommand()`](clig.subcommand) as
decorators, because they don't require to define a [`Command`](clig.Command)
object:

```python
# prog06.py
from clig import command, subcommand, run

@command
def main(verbose: bool = False):
    """Description for the main command"""
    print(locals())

@subcommand
def foo(a, b):
    """Help for foo sub command"""
    print(locals())

@subcommand
def bar(c, d):
    """Help for bar sub command"""
    print(locals())

run()
```

```none
> python prog06.py -h

usage: main [-h] [--verbose] {foo,bar} ...

Description for the main command

positional arguments:
  {foo,bar}
    foo       Help for foo sub command
    bar       Help for bar sub command

options:
  -h, --help  show this help message and exit
  --verbose
```

However, to define more than one level of subcommands using these function
decorators, you can also pass arguments to the functions, in a similar way as
[passing an argument to the methods decorators](#method-decorator-with-arguments).

### Function decorator with arguments

The [`@clig.subcommad`](clig.subcommad) function decorator accepts many
arguments that creates a new [`Command`](clig.Command) instance, check them
[on the their docs](./advancedfeatures.md).

A particular argument used to create more levels of subcommands is the `parent`
argument, which accepts a subcommad name, or its function object.

```python
# prog07.py
from clig import command, subcommand, run

# Here, you don't need to define the main object as in the previous example

@command
def prog(name: str = "mario", age: int = 40):
    print(locals())

@subcommand
def subfunction(height: float):
    print(locals())

# but you still can use the parent argument, with the function object

@subcommand(parent=subfunction)
def internalsubfunction(city: str, state: str):
    print(locals())

run()
```

```none
> python prog07.py -h

usage: prog [-h] [--name NAME] [--age AGE] {subfunction} ...

positional arguments:
  {subfunction}

options:
  -h, --help     show this help message and exit
  --name NAME
  --age AGE
```

```none
> python prog07.py subfunction -h

usage: prog subfunction [-h] height {internalsubfunction} ...

positional arguments:
  height
  {internalsubfunction}

options:
  -h, --help            show this help message and exit
```

## Context

As noted above, one command and its subcommads run sequentially. However, they
normally don't have access from each other's arguments.

To get this access and use function's argument in its subcommad's functions, you
can declare an argument having the type [`clig.Context`](clig.Context). This
argument will not be added to the interface, but it will contain the whole
parser
[`Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace).

```python
# prog08.py
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

```none
> python prog08.py bazinga 32 second 22.5

Arguments in the top level command: {'foo': 'bazinga', 'bar': 32}
Running now the second command . . .
The 'foo' argument from the previous command was: foo = bazinga
```

### Protocols

You can pass a
[`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) as
type argument to the annotated [`Context`](clig.Context) parameter, so it can be
recognized by intellisense or type checkers.

```python
# prog09.py
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

```none
> python prog09.py shazan 23 second 74.9

{'foo': 'shazan', 'bar': 23}
foo value = shazan
```

### The Attribute [`Context.command`](clig.Context.command)

Besides the `Namespace`, the [`Context`](clig.Context) object will also contain
the whole main [`Command`](clig.Command) object in the attribute
[`Context.command`](clig.Context.command). So, you can use this object and all
its attributes.

```python
>>> from clig import Command, Context
...
...
>>> def main(foo: str, bar: int):
...     print(f"Running main with: {locals()}")
...
...
>>> def sub1(ctx: Context, ham: float):
...     print(f"Top level command name = {ctx.command.name}")
...
...
>>> def sub2(ctx: Context, baz: bool):
...     print("Subcommand functions:")
...     for cmd in ctx.command.subcommands:
...         print(f"{cmd}: {ctx.command.subcommands[cmd].func}")
...
...
>>> command = Command(main).add_subcommand(sub1).add_subcommand(sub2)
>>> command.run(["hello", "23", "sub1", "32.5"])
Running main with: {'foo': 'hello', 'bar': 23}
Top level command name = main
>>> command.run(["hello", "23", "sub2", "--baz"])
Running main with: {'foo': 'hello', 'bar': 23}
Subcommand functions:
sub1: <function sub1 at 0x00000218DEC90CC0>
sub2: <function sub2 at 0x00000218DECBF240>
```

### An solved issue with [`argparse`](https://docs.python.org/3/library/argparse.html) subparsers

There is a known `argparse` behavior that happens when you have subparsers with
same argument names, which may be seen as an issue, as described below.

Normally, all arguments are gathered into one
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
...
>>> def main(name: str = ""):
...     print(locals())
...
...
>>> def subcommand(name: str = ""):
...     print(locals())
...
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
...
>>> def main(name: str = ""):
...     print(locals())
...
...
>>> def subcommand(ctx: clig.Context, name: str = ""):
...     args = locals().copy()
...     args.pop("ctx")
...     print(args)
...     print(ctx.namespace)
...
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
