# User guide

`clig` is a single module, written in pure python, that wraps around the
_stdlib_ module `argparse` (using the _stdlib_ module `inspect`) to generate
command line interfaces through simple functions.

## Basic usage

Create or import some function and call `clig.run()` with it:



```python
# example1.py
import clig

def noundata(name, title="Mister"):
    print(f"Title: {title}")
    print(f"Name: {name}")

clig.run(noundata)
```

In general, the function arguments that have a "default" value are turned into
optional _flagged_ (`--`) command line arguments, while the "non default" will
be positional arguments.



```
> python example1.py -h

    usage: noundata [-h] [--title TITLE] name
    
    positional arguments:
      name
    
    options:
      -h, --help     show this help message and exit
      --title TITLE
    
```
The script can then be used in the same way as used with `argparse`:



```
> python example1.py John 

    Title: Mister
    Name: John
    
```

```
> python example1.py Maria --title Miss

    Title: Miss
    Name: Maria
    
```
## Helps

Arguments and command Helps are taken from the docstring when possible:



```python
# example2.py
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


```
> python example2.py --help

    usage: greetings [-h] [--greet GREET] name
    
    Description of the command: A greeting prompt!
    
    positional arguments:
      name           The name to greet
    
    options:
      -h, --help     show this help message and exit
      --greet GREET  The greeting used. Defaults to "Hello".
    
```
There is an internal list of docstring templates from which you can choose if
the inferred docstring is not correct. It is also possible to specify your own
custom docstring template.


## Argument inference

Based on [type annotations](https://docs.python.org/3/library/typing.html), some
arguments can be inferred from the function signature to pass to the
`argparse.ArgumentParser.add_argument()` method:



```python
# example3.py
import clig

def recordperson(name: str, age: int, height: float):
    print(locals())

clig.run(recordperson)
```

The types in the annotation may be passed to
`argparse.ArgumentParser.add_argument()` method as `type` keyword argument:



```
> python example3.py John 37 1.70

    {'name': 'John', 'age': 37, 'height': 1.7}
    
```
And the type conversions are performed as usual



```
> python example3.py Mr John Doe

    usage: recordperson [-h] name age height
    recordperson: error: argument age: invalid int value: 'John'
    
```
### Booleans

Booleans are transformed in arguments with `action` of kind `"store_true"` or
`"store_false"` (depending on the default value).



```python
# example4.py
import clig

def recordperson(name: str, age: int, title="Mister", graduate: bool = False):
    print(locals())

clig.run(recordperson)
```


```
> python example4.py -h

    usage: recordperson [-h] [--title TITLE] [--graduate] name age
    
    positional arguments:
      name
      age
    
    options:
      -h, --help     show this help message and exit
      --title TITLE
      --graduate
    
```

```
> python example4.py Leo 36 --title "Doctor" --graduate

    {'name': 'Leo', 'age': 36, 'title': 'Doctor', 'graduate': True}
    
```
If no default is given to the boolean, a `required=True` keyword argument is
passed to `add_argument()` method in the flag boolean option and a
`BooleanOptionalAction` (already available in `argparse`) is passed as `action`
keyword argument, adding support for a boolean complement action in the form
`--no-option`:



```python
# example5.py
import clig

def recordperson(name: str, age: int, graduate: bool):
    print(locals())

clig.run(recordperson)
```


```
> python example5.py -h

    usage: recordperson [-h] --graduate | --no-graduate name age
    
    positional arguments:
      name
      age
    
    options:
      -h, --help            show this help message and exit
      --graduate, --no-graduate
    
```

```
> python example5.py Ana 23

    usage: recordperson [-h] --graduate | --no-graduate name age
    recordperson: error: the following arguments are required: --graduate/--no-graduate
    
```
### Tuples, Sequences and Lists: `nargs`

If the type is a `tuple` of specified length `N`, the argument automatically
uses `nargs=N`. If the type is a generic `Sequence`, a `list` or a `tuple` of
_any_ length (i.e., `tuple[<type>, ...]`), it uses `nargs="*"`.



```python
# example6.py
from typing import Sequence
import clig


def main(name: tuple[str, str], ages: list[int]):
    print(locals())


clig.run(main)
```


```
> python example6.py -h

    usage: main [-h] name name [ages ...]
    
    positional arguments:
      name
      ages
    
    options:
      -h, --help  show this help message and exit
    
```

```
> python example6.py John Mary 2 78 35

    {'name': ['John', 'Mary'], 'ages': [2, 78, 35]}
    
```
### Literals and Enums: `choices`

If the type is a `Literal` or a `Enum` the argument automatically uses
`choices`.



```python
# example7.py
from typing import Literal
import clig

def main(name: str, move: Literal["rock", "paper", "scissors"]):
    print(locals())

clig.run(main)
```


```
> python example7.py -h

    usage: main [-h] name {rock,paper,scissors}
    
    positional arguments:
      name
      {rock,paper,scissors}
    
    options:
      -h, --help            show this help message and exit
    
```
As is expected in `argparse`, an error message will be displayed if the argument
was not one of the acceptable values:


```
> python example7.py John knife

    usage: main [-h] name {rock,paper,scissors}
    main: error: argument move: invalid choice: 'knife' (choose from rock, paper, scissors)
    
```

```
> python example7.py Mary paper

    {'name': 'Mary', 'move': 'paper'}
    
```
Enums should be passed by name



```python
# example8.py
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


```
> python example8.py -h

    usage: main [-h] {red,blue,yellow} {minimun,mean,maximum}
    
    positional arguments:
      {red,blue,yellow}
      {minimun,mean,maximum}
    
    options:
      -h, --help            show this help message and exit
    
```

```
> python example8.py red mean

    {'color': <Color.red: 1>, 'statistic': <Statistic.mean: 'mean'>}
    
```

```
> python example8.py green

    usage: main [-h] {red,blue,yellow} {minimun,mean,maximum}
    main: error: argument color: invalid choice: 'green' (choose from red, blue, yellow)
    
```
You can even mix `Enum` and `Literal`



```python
# example9.py
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


```
> python example9.py red

    {'color': <Color.red: 1>}
    
```

```
> python example9.py green

    {'color': 'green'}
    
```
## Argument specification


## Subcommands

