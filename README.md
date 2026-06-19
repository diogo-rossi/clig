<img height="150px" src="docs/logo.png"/>

# `clig` - CLI Generator

[![PyPI - Version](https://img.shields.io/pypi/v/clig.svg)](https://pypi.org/project/clig)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clig.svg)](https://pypi.org/project/clig)

A single module, pure python, **Command Line Interface Generator**.

## Installation

Install with `pip`:

```PowerShell
pip install clig
```

Or just
[download the module](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/comparisons.md#download-the-module)

# User guide

`clig` is a single module, written in pure python, that wraps around the
_stdlib_ module [`argparse`](https://docs.python.org/3/library/argparse.html) to
generate command line interfaces through simple functions.

If you know how to use
[`argparse`](https://docs.python.org/3/library/argparse.html), you may want to
use `clig`.

## Basic usage

Create or import some function and call `clig.run()` with it:

```python
# example01.py
import clig

def printperson(name, title="Mister"):
    print(f"{title} {name}")

clig.run(printperson)
```

In general, the function arguments that have a "default" value are turned into
optional _flagged_ (`--`) command line arguments, while the "non default" will
be positional arguments.

```none
> python example01.py -h

usage: printperson [-h] [--title TITLE] name

positional arguments:
  name

options:
  -h, --help     show this help message and exit
  --title TITLE
```

The script can then be used in the same way as used with
[`argparse`](https://docs.python.org/3/library/argparse.html):

```none
> python example01.py John

Mister John
```

```none
> python example01.py Maria --title Miss

Miss Maria
```

You can also pass arguments in code (like with the original
[`parse_args()`](https://docs.python.org/3/library/argparse.html#the-parse-args-method)
method)

```python
>>> import clig
>>> def printperson(name, title="Mister"):
...     print(f"{title} {name}")
...
>>> clig.run(printperson, ["Isaac", "--title", "Sir"])
Sir Isaac
```

The `clig.run()` function also accepts
[other arguments to customize the interface](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md#parameters-for-cligrun-function)

## Helps

Arguments and command Helps are taken from the docstring when possible:

```python
# example02.py
import clig

def greetings(name, greet="Hello"):
    """Description of the command: A greeting prompt!

    Args:
        name: The name to greet
        greet: The greeting used. Defaults to "Hello".
    """
    print(f"Greetings: {greet} {name}!")

clig.run(greetings)
```

```none
> python example02.py --help

usage: greetings [-h] [--greet GREET] name

Description of the command: A greeting prompt!

positional arguments:
  name           The name to greet

options:
  -h, --help     show this help message and exit
  --greet GREET  The greeting used. Defaults to "Hello".
```

There is an [internal list of docstring templates](../docstrings_templates.md)
from which you can choose if the inferred docstring is not correct. It is also
possible to specify your own
[custom docstring template](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md#docstring-templates).

## Argument inference

Based on [type annotations](https://docs.python.org/3/library/typing.html), some
arguments can be inferred from the function signature to pass data to the
original
[`add_argument()`](https://docs.python.org/3/library/argparse.html#the-add-argument-method)
method:

```python
# example03.py
import clig

def recordperson(name: str, age: int, height: float):
    print(locals())

clig.run(recordperson)
```

The types in the annotation may be used in the
[`add_argument()`](https://docs.python.org/3/library/argparse.html#the-add-argument-method)
method as [`type`](https://docs.python.org/3/library/argparse.html#type) keyword
argument, when possible:

```none
> python example03.py John 37 1.73

{'name': 'John', 'age': 37, 'height': 1.73}
```

And the type conversions are performed as usual

```none
> python example03.py Mr John Doe

usage: recordperson [-h] name age height
recordperson: error: argument age: invalid int value: 'John'
```

### Booleans

Booleans are transformed into arguments with
[`action`](https://docs.python.org/3/library/argparse.html#action) of kind
`"store_true"` or `"store_false"` (depending on the default value).

```python
# example04.py
import clig

def recordperson(name: str, employee: bool = False):
    print(locals())

clig.run(recordperson)
```

```none
> python example04.py -h

usage: recordperson [-h] [--employee] name

positional arguments:
  name

options:
  -h, --help  show this help message and exit
  --employee
```

```none
> python example04.py --employee Leo

{'name': 'Leo', 'employee': True}
```

```none
> python example04.py Ana

{'name': 'Ana', 'employee': False}
```

#### Required booleans

If no default is given to the boolean, a
[`required=True`](https://docs.python.org/3/library/argparse.html#required)
keyword argument is used in the
[`add_argument()`](https://docs.python.org/3/library/argparse.html#the-add-argument-method)
method and a
[`BooleanOptionalAction`](https://docs.python.org/3/library/argparse.html#argparse.BooleanOptionalAction)
is used as [`action`](https://docs.python.org/3/library/argparse.html#action)
keyword argument, adding support for a boolean complement action in the form
`--no-option`:

```python
# example05.py
import clig

def recordperson(name: str, employee: bool):
    print(locals())

clig.run(recordperson)
```

```none
> python example05.py -h

usage: recordperson [-h] --employee | --no-employee name

positional arguments:
  name

options:
  -h, --help            show this help message and exit
  --employee, --no-employee
```

```none
> python example05.py Ana

usage: recordperson [-h] --employee | --no-employee name
recordperson: error: the following arguments are required: --employee/--no-employee
```

### Tuples, Lists and Sequences: [`nargs`](https://docs.python.org/3/library/argparse.html#nargs)

The original [`nargs`](https://docs.python.org/3/library/argparse.html#nargs)
keyword argument associates a different number of command-line arguments with a
single action. This is inferrend in types using `tuple`, `list` and `Sequence`.

#### Tuples

If the type is a `tuple` of specified length `N`, the argument automatically
uses `nargs=N`.

```python
# example06.py
import clig

def main(name: tuple[str, str]):
    print(locals())

clig.run(main)
```

```none
> python example06.py -h

usage: main [-h] name name

positional arguments:
  name

options:
  -h, --help  show this help message and exit
```

```none
> python example06.py rocky yoco

{'name': ('rocky', 'yoco')}
```

```none
> python example06.py rocky

usage: main [-h] name name
main: error: the following arguments are required: name
```

The argument can be positional (required, as above) or optional (with a
default).

```python
# example07.py
import clig

def main(name: tuple[str, str, str] = ("john", "mary", "jean")):
    print(locals())

clig.run(main)
```

```none
> python example07.py

{'name': ('john', 'mary', 'jean')}
```

```none
> python example07.py --name yoco

usage: main [-h] [--name NAME NAME NAME]
main: error: argument --name: expected 3 arguments
```

```none
> python example07.py --name yoco rocky sand

{'name': ('yoco', 'rocky', 'sand')}
```

#### List, Sequences and Tuples of any length

If the type is a generic `Sequence`, a `list` or a `tuple` of _any_ length
(i.e., `tuple[<type>, ...]`), it uses
[`nargs="+"`](https://docs.python.org/3/library/argparse.html#nargs) if it is
required (non default value) or
[`nargs="*"`](https://docs.python.org/3/library/argparse.html#nargs) if it is
not required (has a default value).

```python
# example08.py
import clig

def main(names: list[str]):
    print(locals())

clig.run(main)
```

In this example, we have `names` using
[`nargs="+"`](https://docs.python.org/3/library/argparse.html#nargs)

```none
> python example08.py -h

usage: main [-h] names [names ...]

positional arguments:
  names

options:
  -h, --help  show this help message and exit
```

```none
> python example08.py chester philip

{'names': ['chester', 'philip']}
```

```none
> python example08.py

usage: main [-h] names [names ...]
main: error: the following arguments are required: names
```

In the next example, we have `names` as optional argument, using
[`nargs="*"`](https://docs.python.org/3/library/argparse.html#nargs)

```python
# example09.py
import clig

def main(names: list[str] | None = None):
    print(locals())

clig.run(main)
```

```none
> python example09.py -h

usage: main [-h] [--names [NAMES ...]]

options:
  -h, --help           show this help message and exit
  --names [NAMES ...]
```

```none
> python example09.py --names katy buba

{'names': ['katy', 'buba']}
```

```none
> python example09.py

{'names': None}
```

### Literals and Enums: [`choices`](https://docs.python.org/3/library/argparse.html#choices)

If the type is a
[`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal) or a
[`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum) the argument
automatically uses
[`choices`](https://docs.python.org/3/library/argparse.html#choices).

```python
# example10.py
from typing import Literal
import clig

def main(name: str, move: Literal["rock", "paper", "scissors"]):
    print(locals())

clig.run(main)
```

```none
> python example10.py -h

usage: main [-h] name {rock,paper,scissors}

positional arguments:
  name
  {rock,paper,scissors}

options:
  -h, --help            show this help message and exit
```

As is expected in [`argparse`](https://docs.python.org/3/library/argparse.html),
an error message will be displayed if the argument was not one of the acceptable
values:

```none
> python example10.py John knife

usage: main [-h] name {rock,paper,scissors}
main: error: argument move: invalid choice: 'knife' (choose from rock, paper, scissors)
```

```none
> python example10.py Mary paper

{'name': 'Mary', 'move': 'paper'}
```

#### Passing Enums

In the command line, `Enum` should be passed by name, regardless of if it is a
number Enum or ar string Enum

```python
# example11.py
from enum import Enum, StrEnum
import clig

class Color(Enum):
    red = 1
    blue = 2
    yellow = 3

class Statistic(StrEnum):
    minimun = "minimun"
    mean = "mean"
    maximum = "maximum"

def main(color: Color, statistic: Statistic):
    print(locals())

clig.run(main)
```

```none
> python example11.py -h

usage: main [-h] {red,blue,yellow} {minimun,mean,maximum}

positional arguments:
  {red,blue,yellow}
  {minimun,mean,maximum}

options:
  -h, --help            show this help message and exit
```

It is correctly passed to the function

```none
> python example11.py red mean

{'color': <Color.red: 1>, 'statistic': <Statistic.mean: 'mean'>}
```

```none
> python example11.py green

usage: main [-h] {red,blue,yellow} {minimun,mean,maximum}
main: error: argument color: invalid choice: 'green' (choose from red, blue, yellow)
```

#### Literal with Enum

You can even mix `Enum` and `Literal`, following the
[`Literal` specification](https://typing.python.org/en/latest/spec/literal.html#legal-parameters-for-literal-at-type-check-time)

```python
# example12.py
from typing import Literal
from enum import Enum
import clig

class Color(Enum):
    red = 1
    blue = 2
    yellow = 3

def main(color: Literal[Color.red, "green", "black"]):
    print(locals())

clig.run(main)
```

```none
> python example12.py red

{'color': <Color.red: 1>}
```

```none
> python example12.py green

{'color': 'green'}
```

### Variadic arguments (`*args` and `**kwargs`): [Partial parsing](https://docs.python.org/3/library/argparse.html#partial-parsing)

When the function has variadic arguments in the form `*args` or `**kwargs`, the
[parse_known_args()](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_known_args)
method will be used internally to gather unspecified arguments:

```python
>>> import clig
>>> def variadics(foo: str, *args, **kwargs):
...     print(locals())
...
>>> clig.run(variadics, "bar badger BAR spam --name adam --title mister".split())
{'foo': 'bar', 'args': ('badger', 'BAR', 'spam'), 'kwargs': {'name': 'adam', 'title': 'mister'}}
```

#### `*args`

For
[arbitrary arguments in the form `*args`](https://docs.python.org/3/tutorial/controlflow.html?utm_source=chatgpt.com#arbitrary-argument-lists),
the unspecified arguments will be wrapped up in a tuple of strings, by default.
If there is a type annotation, the conversion is made in the whole tuple:

```python
>>> import clig
>>> def variadicstyped(number: float, *integers: int):
...     print(locals())
...
>>> clig.run(variadicstyped, ["36.7", "1", "2", "3", "4", "5"])
{'number': 36.7, 'integers': (1, 2, 3, 4, 5)}
```

#### `**kwargs`

For
[arbitrary keyword arguments in the form `**kwargs`](https://docs.python.org/3/tutorial/controlflow.html?utm_source=chatgpt.com#keyword-arguments),
the unspecified arguments will be wrapped up in a dictionary of strings by
default. The keys of the dictionary are the names used with the option delimiter
in the command line (usually `-` or `--`). If there are more than one value for
each option, they are gathered in a list:

```python
# example13.py
import clig

def foobar(name: str, **kwargs):
    print(locals())

clig.run(foobar)
```

```none
> python example13.py joseph --nickname joe --uncles jack jean adam

{'name': 'joseph', 'kwargs': {'nickname': 'joe', 'uncles': ['jack', 'jean', 'adam']}}
```

If there is a type annotation, the conversion is made in all elements of the
dictionary

```python
# example14.py
import clig

def foobartyped(name: str, **intergers: int):
    print(locals())

clig.run(foobartyped)
```

```none
> python example14.py joseph --age 23 --numbers 25 27 30

{'name': 'joseph', 'intergers': {'age': 23, 'numbers': [25, 27, 30]}}
```

```none
> python example14.py joseph --age 23 --numbers jack jean adam

ValueError: invalid literal for int() with base 10: 'jack'
```

#### Error when passing _flagged_ arguments to `*args`

The flag delimiters (usually `-` or `--`,
[which can be changed](https://docs.python.org/3/library/argparse.html#prefix-chars))
are always interpreted as prefix for keyword arguments, raising the correct
error when not allowed:

```python
# example15.py
import clig

def bazham(name: str, *uncles: str):
    print(locals())

clig.run(bazham)
```

```none
> python example15.py joseph jack john

{'name': 'joseph', 'uncles': ('jack', 'john')}
```

```none
> python example15.py joseph --uncles jack john

TypeError: bazham() got an unexpected keyword argument 'uncles'
```

## Argument specification

In some complex cases supported by
[`argparse`](https://docs.python.org/3/library/argparse.html), the arguments may
not be completely inferred by `clig.run()` on the function signature.

In theses cases, you can directly specificy the arguments parameters using the
[`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated)
typing (or its `clig`'s alias `Arg`) with its "metadata" created with the
`data()` function.

The `data()` function accepts all possible arguments of the original
[`add_argument()`](https://docs.python.org/3/library/argparse.html#the-add-argument-method)
method:

### name or flags

The
[`name_or_flags`](https://docs.python.org/3/library/argparse.html#name-or-flags)
parameter can be used to define additional flags for the arguments, like `-f` or
`--foo`:

```python
# example16.py
from clig import Arg, data, run

def main(foobar: Arg[str, data("-f", "--foo")] = "baz"):
    print(locals())

run(main)
```

```none
> python example16.py -h

usage: main [-h] [-f FOOBAR]

options:
  -h, --help            show this help message and exit
  -f FOOBAR, --foo FOOBAR
```

[`name or flags`](https://docs.python.org/3/library/argparse.html#name-or-flags)
can also be used to turn a positional argument (without default) into a
[`required`](https://docs.python.org/3/library/argparse.html#required) flagged
argument (a _required option_):

```python
# example17.py
from clig import Arg, data, run

def main(foo: Arg[str, data("-f")]):
    print(locals())

run(main)
```

```none
> python example17.py -h

usage: main [-h] -f FOO

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
```

```none
> python example17.py

usage: main [-h] -f FOO
main: error: the following arguments are required: -f/--foo
```

> [!NOTE]  
> As you can see above, `clig` tries to create a _long flag_ (`--`) for the
> argument when only _short flags_ (`-`) are defined, but not when long flags
> are _already_ defined. However,
> [this behavior can be disabled](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md#using-make_flags).

Some options for the
[`name or flags`](https://docs.python.org/3/library/argparse.html#name-or-flags)
parameter
[can also be set in the `run()` function](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md#automatic-argument-flags).

### nargs

Other cases of [`nargs`](https://docs.python.org/3/library/argparse.html#nargs)
can be specified in the `data()` function.

The next example uses an optional argument with
[`nargs="?"`](https://docs.python.org/3/library/argparse.html#nargs) and
[`const`](https://docs.python.org/3/library/argparse.html#const), which brings 3
different behaviors for the optional argument:

- value passed
- value not passed (sets default value)
- option passed without value (sets const value):

```python
>>> from clig import Arg, data, run
...
>>> def main(foo: Arg[str, data(nargs="?", const="c")] = "d"):
...     print(locals())
...
>>> run(main, ["--foo", "YY"])
{'foo': 'YY'}
>>> run(main, [])
{'foo': 'd'}
>>> run(main, ["--foo"])
{'foo': 'c'}
```

The next example makes optional a positional argument (not flagged), by using
[`nargs="?"`](https://docs.python.org/3/library/argparse.html#nargs) and
[`default`](https://docs.python.org/3/library/argparse.html#default) (which
would default to `None`):

```python
>>> from clig import Arg, data, run
>>> def main(foo: Arg[str, data(nargs="?", default="d")]):
...     print(locals())
...
>>> run(main, ["YY"])
{'foo': 'YY'}
>>> run(main, [])
{'foo': 'd'}
```

### action

Other options for the
[`action`](https://docs.python.org/3/library/argparse.html#action) parameter can
also be used in the `data()` function:

```python
>>> from clig import Arg, data, run
>>> def append(foo: Arg[list[str], data(action="append")] = ["0"]):
...     print(locals())
...
>>> def append_const(bar: Arg[list[int], data(action="append_const", const=42)] = [42]):
...     print(locals())
...
>>> def extend(baz: Arg[list[float], data(action="extend")] = [0]):
...     print(locals())
...
>>> def count(ham: Arg[int, data(action="count")] = 0):
...     print(locals())
...
>>> run(append, "--foo 1 --foo 2".split())
{'foo': ['0', '1', '2']}
...
>>> run(append_const, "--bar --bar --bar --bar".split())
{'bar': [42, 42, 42, 42, 42]}
...
>>> run(extend, "--baz 25 --baz 50 65 75".split())
{'baz': [0, 25.0, 50.0, 65.0, 75.0]}
...
>>> run(count, "--ham --ham --ham".split())
{'ham': 3}
```

### metavar

The parameter
[`metavar`](https://docs.python.org/3/library/argparse.html#metavar) is used to
set alternative names in help messages to refer to arguments. By default, they
would be referend as just the argument name, if positional, and the argument
name uppercased, if optional.

```python
# example18.py
from clig import Arg, data, run

def main(ham: Arg[str, data(metavar="YYY")], foo: Arg[str, data("-f", metavar="<foobar>")]):
    print(locals())

run(main)
```

```none
> python example18.py -h

usage: main [-h] -f <foobar> YYY

positional arguments:
  YYY

options:
  -h, --help            show this help message and exit
  -f <foobar>, --foo <foobar>
```

Some options for the
[`metavar`](https://docs.python.org/3/library/argparse.html#metavar) argument
[can also be set in the `run()` function](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md#metavar-modifiers).

### help

It is more convenient to specify [helps for arguments in the docstring](#helps).

However, you can define helps using the `data()` function in the same way as in
the original method
[`add_argument()`](https://docs.python.org/3/library/argparse.html#the-add-argument-method).
Helps passed in the `data()` function takes precedence.

```python
# example19.py
from clig import Arg, data, run

def mycommand(number: Arg[int, data(help="a different help for the number")]):
    """Description of the command

    Args:
        number: a number to compute
    """
    pass

run(mycommand)
```

```none
> python example19.py -h

usage: mycommand [-h] number

Description of the command

positional arguments:
  number      a different help for the number

options:
  -h, --help  show this help message and exit
```

Some options for the
[`help`](https://docs.python.org/3/library/argparse.html#help) argument
[can also be set in the `run()` function](https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md#help-modifiers).

## Argument groups

The
[`argparse`](https://docs.python.org/3/library/argparse.html#module-argparse)
module has the features of
[argument groups](https://docs.python.org/3/library/argparse.html#argument-groups)
and
[mutually exclusive argument groups](https://docs.python.org/3/library/argparse.html#mutual-exclusion).
These features can be used in `clig` with 2 additional classes: `ArgumentGroup`
and `MutuallyExclusiveGroup`.

The object created with these classes can be used in the `group` parameter of
the `data()` function.

Each class accepts all the parameters of the original methods
[`add_argument_group()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument_group)
and
[`add_mutually_exclusive_group()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group).

```python
# example20.py
from clig import Arg, data, run, ArgumentGroup

g = ArgumentGroup(title="Group of arguments", description="This is my group of arguments")

def main(foo: Arg[str, data(group=g)], bar: Arg[int, data(group=g)] = 42):
    print(locals())

run(main)
```

```none
> python example20.py -h

usage: main [-h] [--bar BAR] foo

options:
  -h, --help  show this help message and exit

Group of arguments:
  This is my group of arguments

  foo
  --bar BAR
```

Remember that mutually exclusive arguments
[must be optional](https://github.com/python/cpython/blob/7168553c00767689376c8dbf5933a01af87da3a4/Lib/argparse.py#L1805)
(either by using a flag in the `data` function, or by setting a deafult value):

```python
# example21.py
from clig import Arg, data, run, MutuallyExclusiveGroup

g = MutuallyExclusiveGroup()

def main(foo: Arg[str, data("-f", group=g)], bar: Arg[int, data(group=g)] = 42):
    print(locals())

run(main)
```

```none
> python example21.py --foo rocky --bar 23

usage: main [-h] [-f FOO | --bar BAR]
main: error: argument --bar: not allowed with argument -f/--foo
```

### Required mutually exclusive group

A `required` argument is accepted by the `MutuallyExclusiveGroup` in the same
way it is done with the original method
[`add_mutually_exclusive_group()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group)
(to indicate that at least one of the mutually exclusive arguments is required):

```python
# example22.py
from clig import Arg, data, run, MutuallyExclusiveGroup

g = MutuallyExclusiveGroup(required=True)

def main(foo: Arg[str, data(group=g)] = "baz", bar: Arg[int, data(group=g)] = 42):
    print(locals())

run(main)
```

```none
> python example22.py -h

usage: main [-h] (--foo FOO | --bar BAR)

options:
  -h, --help  show this help message and exit
  --foo FOO
  --bar BAR
```

```none
> python example22.py

usage: main [-h] (--foo FOO | --bar BAR)
main: error: one of the arguments --foo --bar is required
```

### Mutually exclusive group added to an argument group

The `MutuallyExclusiveGroup` constructor class also accepts an additional
`argument_group` parameter, because
[a mutually exclusive group can be added to an argument group](https://github.com/python/cpython/blob/920286d6b296f9971fc79e14ec22966f8f7a7b90/Doc/library/argparse.rst?plain=1#L2028-L2029).

```python
# example23.py
from clig import Arg, data, run, ArgumentGroup, MutuallyExclusiveGroup

ag = ArgumentGroup(title="Group of arguments", description="This is my group")
meg = MutuallyExclusiveGroup(argument_group=ag)

def main(
    foo: Arg[str, data(group=meg)] = "baz",
    bar: Arg[int, data(group=meg)] = 42,
):
    print(locals())

run(main)
```

```none
> python example23.py -h

usage: main [-h] [--foo FOO | --bar BAR]

options:
  -h, --help  show this help message and exit

Group of arguments:
  This is my group

  --foo FOO
  --bar BAR
```

However, you can define just the `MutuallyExclusiveGroup` object passing the
parameters of `ArgumentGroup` to the constructor of the former class, which
supports them:

```python
# example24.py
from clig import Arg, data, run, MutuallyExclusiveGroup

g = MutuallyExclusiveGroup(
    title="Group of arguments",
    description="This is my exclusive group of arguments",
)

def main(
    foo: Arg[str, data("-f", group=g)],
    bar: Arg[int, data("-b", group=g)],
):
    print(locals())

run(main)
```

```none
> python example24.py -h

usage: main [-h] [-f FOO | -b BAR]

options:
  -h, --help         show this help message and exit

Group of arguments:
  This is my exclusive group of arguments

  -f FOO, --foo FOO
  -b BAR, --bar BAR
```

### Using the walrus operator (`:=`)

You can do argument group definition all in one single line (in the function
declaration) by using the
[walrus operator](https://docs.python.org/3/reference/expressions.html#assignment-expressions)
(`:=`):

```python
# example25.py
from clig import Arg, data, run, MutuallyExclusiveGroup

def main(
    foo: Arg[str, data(group=(g := MutuallyExclusiveGroup(title="My group")))] = "baz",
    bar: Arg[int, data(group=g)] = 42,
):
    print(locals())

run(main)
```

```none
> python example25.py -h

usage: main [-h] [--foo FOO | --bar BAR]

options:
  -h, --help  show this help message and exit

My group:
  --foo FOO
  --bar BAR
```
