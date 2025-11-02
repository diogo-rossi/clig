# User guide

`clig` is a single module, written in pure python, that wraps around the _stdlib_
module `argparse` to generate command line interfaces using simple functions.

## Basic usage

Create or import some function and call `clig.run()` with it:



```python
# example.py
import clig

def greetings(name, greet="Hello"):
    print(f"Greetings: {greet} {name}!")

clig.run(greetings)
```

    

In general, the function arguments that have a "default" value are turned into
optional _flagged_ (`--`) command line arguments, while the "non default" will
be positional arguments.


```
> python example.py -h

    usage: greetings [-h] [--greet GREET] name
    
    positional arguments:
      name
    
    options:
      -h, --help     show this help message and exit
      --greet GREET
    
```
The script can then be used in the same way as used with `argparse`:



```
> python example.py John 

    Greetings: Hello John!
    
```

```
> python example.py Maria --greet Hi

    Greetings: Hi Maria!
    
```
## Helps

Arguments and command Helps are taken from the docstring when possible:


```python
# example0.py
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
> python example0.py -h

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
custom template.


## Argument inference

Based on [type annotations](https://docs.python.org/3/library/typing.html), some
arguments can be inferred from the function signature to pass to the
`argparse.ArgumentParser.add_argument()` method:



```python
# example1.py
import clig

def greetage(name: str, age: int):
    print(f"{name} is {age} years old")

clig.run(greetage)
```

    

The types in the annotation are passed to
`argparse.ArgumentParser.add_argument()` method as `type` keyword argument:



```
> python example1.py Harry 17

    Harry is 17 years old
    
```

```
> python example1.py Harry Potter

    usage: greetage [-h] name age
    greetage: error: argument age: invalid int value: 'Potter'
    
```
### Booleans

Booleans are transformed in arguments with `action` of kind `"store_true"` or
`"store_false"` (depending on the default value).



```python
# example2.py
import clig

def greetage(name: str, age: int, greet="Hello", askback: bool = False):
    print(f"{greet} {name}! I am {age} yeats old.")
    if askback:
        print("How old are you?")

clig.run(greetage)
```

    


```
> python example2.py Leo 36 --greet "Good morning" --askback

    Good morning Leo! I am 36 yeats old.
    How old are you?
    
```
If no default is given to the boolean, a `required=True` keyword argument is
passed to `add_argument()` method in the flag boolean option and a
`BooleanOptionalAction` already available in `argparse` is passed as `action`
keyword argument, adding support for a boolean complement action in the form
`--no-option`:



```python
# example3.py
import clig

def greetage(name: str, age: int, ask: bool):
    print(f"Hello {name}! I am {age} yeats old.")
    if ask:
        print("How old are you?")

clig.run(greetage)
```

    


```
> python example3.py -h

    usage: greetage [-h] --ask | --no-ask name age
    
    positional arguments:
      name
      age
    
    options:
      -h, --help       show this help message and exit
      --ask, --no-ask
    
```

```
> python example3.py Ana 23

    usage: greetage [-h] --ask | --no-ask name age
    greetage: error: the following arguments are required: --ask/--no-ask
    
```
### Tuples, Sequences and Lists: `nargs`

If the type is a `tuple` of specified length `N`, the argument automatically
uses `nargs=N`. If the type is a generic `Sequence`, a `list` or a `tuple` of _any_ length
(i.e., `tuple[<type>, ...]`), it uses `nargs="*"`.



```python
# example4.py
from typing import Sequence
import clig


def main(foo: tuple[str, str], bar: list[int]):
    print(f"Passed arguments to function: {locals()}")


clig.run(main)
```

    


```
> python example4.py -h

    usage: main [-h] foo foo [bar ...]
    
    positional arguments:
      foo
      bar
    
    options:
      -h, --help  show this help message and exit
    
```

```
> python example4.py John Mary 2 78 35

    Passed arguments to function: {'foo': ['John', 'Mary'], 'bar': [2, 78, 35]}
    
```
### Literals and Enums: `choices`

If the type is a `Literal` or a `Enum` the argument automatically uses `choices`.


```python
# example5.py
from typing import Literal
import clig

def main(name: str, move: Literal["rock", "paper", "scissors"]):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)
```

    


```
> python example5.py -h

    usage: main [-h] name {rock,paper,scissors}
    
    positional arguments:
      name
      {rock,paper,scissors}
    
    options:
      -h, --help            show this help message and exit
    
```

```
> python example5.py John rock

    Passed arguments to function: {'name': 'John', 'move': 'rock'}
    
```

```
> python example5.py Mary test

    usage: main [-h] name {rock,paper,scissors}
    main: error: argument move: invalid choice: 'test' (choose from 'rock', 'paper', 'scissors')
    
```
Enums should be passed by name


```python
# example6.py
from enum import Enum
import clig

class Color(Enum):
    red = 1
    blue = 2
    yellow = 3

def main(color: Color):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)
```

    


```
> python example6.py -h

    usage: main [-h] {red,blue,yellow}
    
    positional arguments:
      {red,blue,yellow}
    
    options:
      -h, --help         show this help message and exit
    
```

```
> python example6.py red

    usage: main [-h] {red,blue,yellow}
    main: error: argument color: invalid Color value: 'red'
    
```

```
> python example6.py green

    usage: main [-h] {red,blue,yellow}
    main: error: argument color: invalid Color value: 'green'
    
```