# Subcommands

Instead of using the function {attr}`clig.run()`, you can create an object
instance of the type `Command`, passing your function to its constructor, and
call the `Command.run()` method.

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
[subcommands](https://docs.python.org/3/library/argparse.html#sub-commands). All
subcommands will also be instances of the same class `Command`. There are 4 main
methods available:

1. {attr}`Command.new_subcommand<clig.Command.new_subcommand()>`:

   Creates a subcommand and returns the new created `Command` instance.

2. {attr}`Command.add_subcommand<clig.Command.add_subcommand()>`:

   Creates the subcommand and returns the caller object. This is useful to add
   multiple subcommands in one single line.

3. {attr}`Command.end_subcommand<clig.Command.end_subcommand()>`:

   Creates the subcommand and returns the parent of the caller object. If the
   caller doesn't have a parent, an error will be raised. This is useful when
   finishing to add subcommands in the object on a single line.

4. {attr}`Command.subcommand<clig.Command.subcommand()>`:

   Creates the subcommand and returns the input function unchanged. This is a
   proper method to be used as a
   [function decorator](https://docs.python.org/3/glossary.html#term-decorator).

There are also
[2 module level functions](#subcommands-using-function-decorators):
{attr}`clig.command()` and {attr}`clig.subcommand()`. They also returns the
functions unchanged, and so may also be used as decorators.

The functions declared as commands execute sequentially, from a `Command` to its
subcommands.

The `Command()` constructor also accepts other arguments to customize the
interface, and also has other methods, like `print_help()`, analog to the
[original method](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.print_help)

## Subcommands using methods

The methods `new_subcommand` and `add_subcommand` can be used to add subcommands
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

options:
  -h, --help            show this help message and exit

subcommands:
  {subfunction1,subfunction2}
    subfunction1
    subfunction2
```

Subcommands are correctly handled with their
[subparsers](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers).

```python
>>> # subcommand help
>>> sub.print_help()
usage: prog name age subfunction2 [-h] father mother {subsubfunction} ...

positional arguments:
  father
  mother

options:
  -h, --help        show this help message and exit

subcommands:
  {subsubfunction}
    subsubfunction
```

Remember that the command functions execute sequentially, from a `Command` to
its subcommands.

```python
>>> # run the main comand with all subcommands
>>> cmd.run("jack 23 subfunction2 michael suzan subsubfunction santos SP".split())
{'name': 'jack', 'age': 23}
{'father': 'michael', 'mother': 'suzan'}
{'city': 'santos', 'state': 'SP'}
...
>>> # run the subcommand with its subcommand
>>> sub.run(["jean", "karen", "subsubfunction", "campos", "RJ"])
{'father': 'jean', 'mother': 'karen'}
{'city': 'campos', 'state': 'RJ'}
```

To access the attributes of a command inside the functions of its subcommands,
check out the feature of the [`Context`](./advancedfeatures.md#context) object.

### All CLI in one statement

Using the 3 methods `new_subcommand`, `add_subcommand` and `end_subcommand` you
can define the whole interface in one single statement (one line of code).

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

######################################################################
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

options:
  -h, --help            show this help message and exit
  --exec-path EXEC_PATH
  --work-tree WORK_TREE

subcommands:
  {status,commit,remote,submodule}
    status              Show the repository status
    commit              Record changes to the repository
    remote              Manage remote repositories
    submodule           Manages git submodules
```

Help for the `remote` subcomand:

```none
> python prog02.py remote -h

usage: git remote [-h] [--verbose] {add,rename,remove} ...

Manage remote repositories

options:
  -h, --help           show this help message and exit
  --verbose

subcommands:
  {add,rename,remove}
    add                Add a new remote
    rename             Rename an existing remote
    remove             Remove the remote reference
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

Remember: the command functions execute sequentially, from a `Command` to its
subcommands.

```none
> python prog02.py remote rename oldName newName

Command: git | Arguments: {'exec_path': WindowsPath('git'), 'work_tree': WindowsPath('C:/Users')}
Command: remote | Arguments: {'verbose': False}
Command: rename | Arguments: {'old': 'oldName', 'new': 'newName'}
```

## Subcommands using method decorators

You can define subcommands using the `subcommand()` method as decorator. To do
it, first, create a `Command` instance. The decorator only registries the
functions as commands (it doesn't change their definitions).

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

options:
  -h, --help  show this help message and exit
  --verbose

subcommands:
  {foo,bar}
    foo       Help for foo sub command
    bar       Help for bar sub command
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
>>> @Command
>>> def main():
...     pass
...
>>> print(type(main)) # now the main function is a `Command` instance
<class 'clig.clig.Command'>
```

### Adding subcommads with decorators

By using decorators without arguments, the functions are not modified but you
won't be able to define more than one level of subcommands,
[unless you pass an argument to the decorators](./advancedfeatures.md#method-decorator-with-arguments).

However, by knowing the fact that subcommads are registered in a
[`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
attribute `Command.subcommands`, it it is possible to use it directly, calling
the respective `subcommand` decorator.

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

# now use the attribute to add another level of subcommands

@cmd.subcommands["subfunction2"].subcommand
def subsubfunction(city: str, state: str):
    print(locals())

cmd.run()
```

```none
> python prog04.py -h

usage: prog [-h] [--name NAME] [--age AGE] {subfunction1,subfunction2} ...

options:
  -h, --help            show this help message and exit
  --name NAME
  --age AGE

subcommands:
  {subfunction1,subfunction2}
    subfunction1
    subfunction2
```

```none
> python prog04.py subfunction2 -h

usage: prog subfunction2 [-h] father mother {subsubfunction} ...

positional arguments:
  father
  mother

options:
  -h, --help        show this help message and exit

subcommands:
  {subsubfunction}
    subsubfunction
```

## Subcommands using function decorators

As it was noticed in the previous example, using decorators without arguments,
(which do not modify functions definitions) does not allow you to declare more
than one level of subcommands, without using the `subcommands` OrderedDict
attribute.

For these simple cases, it is more convenient to use the module level functions
`clig.command()` and `clig.subcommand()` as decorators, because they don't
require to define a `Command` object:

```python
# prog05.py
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
> python prog05.py -h

usage: main [-h] [--verbose] {foo,bar} ...

Description for the main command

options:
  -h, --help  show this help message and exit
  --verbose

subcommands:
  {foo,bar}
    foo       Help for foo sub command
    bar       Help for bar sub command
```

However, to define more than one level of subcommands using these function
decorators, you can also
[pass arguments to the functions](./advancedfeatures.md#method-decorator-with-arguments),
in a similar way as
[passing an argument to the methods decorators](./advancedfeatures.md#function-decorator-with-arguments),
as discussed in the [Advanced Features](./advancedfeatures.md).
