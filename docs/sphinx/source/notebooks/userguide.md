# User guide

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

Argument and command Helps are taken from the docstring when possible:


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
## Argument inference

Based on [type annotations](https://docs.python.org/3/library/typing.html), some arguments can be inferred from the function
signature to pass to `argparse`:


```python
# example1.py

import clig


def greetage(name: str, age: int, greet="Hello", askback: bool = False):
    print(f"{greet} {name}! I am {age} yeats old.")
    if askback:
        print("How old are you?")


clig.run(greetage)
```

Booleans are transformed in arguments with `action` of kind `"store_true"` or
`"store_false"` (depending on the default value).



```
> python example1.py Leo 36 --greet "Good morning" --askback

    Good morning Leo! I am 36 yeats old.
    How old are you?
    
```
And the types in type annotation are also passed to `argparse`:


```
> python example1.py Fernanda Lima

    usage: greetage [-h] [--greet GREET] [--askback] name age
    greetage: error: argument age: invalid int value: 'Lima'
    
```
## Tuples, Sequences and Lists: `nargs`

If the type is a `tuple` of specified length `N`, the argument automatically
uses `nargs=N`. If the type is a generic `Sequence`, a `list` or a `tuple` of _any_ length
(i.e., `tuple[<type>, ...]`), it uses `nargs="*"`.



```python
# example2.py
from typing import Sequence
import clig

def main(
    foo: tuple[str, str],
    bar: list[int],
):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)
```


```
> python example2.py -h

    usage: main [-h] foo foo [bar ...]
    
    positional arguments:
      foo
      bar
    
    options:
      -h, --help  show this help message and exit
    
```

```
> python example2.py John Mary 2 78 35

    Passed arguments to function: {'foo': ['John', 'Mary'], 'bar': [2, 78, 35]}
    
```

```
> python example2.py John Mary 2 78 35 test

    usage: main [-h] foo foo [bar ...]
    main: error: argument bar: invalid int value: 'test'
    
```
## Literals and Enums: `choices`

If the type is a `Literal` or a `Enum` the argument automatically uses `choices`.


```python
# example3.py
from typing import Literal
import clig

def main(
    foo: tuple[str, str],
    bar: list[int],
    move: Literal["rock", "paper", "scissors"],
):
    print(f"Passed arguments to function: {locals()}")

clig.run(main)
```


```
> python example3.py John Mary 2 78 35 rock

    Passed arguments to function: {'foo': ['John', 'Mary'], 'bar': [2, 78, 35], 'move': 'rock'}
    
```

```
> python example3.py John Mary 2 78 35 test

    usage: main [-h] foo foo [bar ...] {rock,paper,scissors}
    main: error: argument move: invalid choice: 'test' (choose from 'rock', 'paper', 'scissors')
    
```