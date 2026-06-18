# Advanced features

The Command Line Interface created with `clig` can be customized in some ways.
Some of these ways are already provided by the
[argparse](https://docs.python.org/3/library/argparse.html) module, but other
additional parameters can be used to add extra customization.

## Parameters for `clig.run()` function

The first parameter of the `clig.run()` function is typically a function that
will be turned into a command. The second positional parameter could be a
[list of strings to pass to the commad inside the code](https://docs.python.org/3/library/argparse.html#args)
(which is defaulted to `sys.argv`).

On top of that, other parameters can be passed as keyword arguments. They are
the parameters of the original
[`ArgumentParser()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)
constructor and some new extra parameters, as detailed below.

### Parameters of the original [`ArgumentParser()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) object

All of these parameters should be passed as keyword arguments to the
`clig.run()` function. Refer to the
[original `argparse` documentation](https://docs.python.org/3/library/argparse.html#argumentparser-objects)
for details. Some parameters has predefined values assumed by `clig` (which can
be modified), as detailed in the short descriptions below:

- `prog`: The name of the new created program command. The default value is the
  name of the input function, with hyphens `-` replacing underscores `_`:

```python
>>> import clig
...
>>> def my_program():
...     """Short description"""
...     pass
...
>>> clig.run(my_program, ["-h"])
usage: my-program [-h]

Short description

options:
  -h, --help  show this help message and exit
```

```python
>>> clig.run(my_program, ["-h"], prog="myNewProgram")
usage: myNewProgram [-h]

Short description

options:
  -h, --help  show this help message and exit
```

- `description`: A text to display before the arguments help. By default, `clig`
  tries to get this parameter as the first line of the function docstring,
  [which can be customized](#docstring-templates).

```python
>>> clig.run(my_program, ["-h"], description="The description of my program")
usage: my-program [-h]

The description of my program

options:
  -h, --help  show this help message and exit
```

- `epilog`: A text to display after the command help. By default, `clig` tries
  to get this parameter from the function docstring after its first line, but
  [this also can be customized](#docstring-templates).

```python
>>> clig.run(my_program, ["-h"], epilog="Text displayed after, with additional info.")
usage: my-program [-h]

Short description

options:
  -h, --help  show this help message and exit

Text displayed after, with additional info.
```

Other
[`ArgumentParser()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)
parameters behave the same as in the original object. For instance, you can
change the
[`add_help`](https://docs.python.org/3/library/argparse.html#add-help) parameter
to `False` (This parameter adds a `-h/--help` option to the command and the
default is `True`)

```python
>>> clig.run(my_program, ["-h"], add_help=False)
usage: my-program
my-program: error: unrecognized arguments: -h
```

### Extra parameters specific of the [`clig.run()`](clig.run) function

The `clig.run()` function has some extra parameters that help to customize the
interface.

#### Metavar modifiers

The parameter `metavarmodifier` lets you input a function that changes the
[`metavar`](https://docs.python.org/3/library/argparse.html#metavar) keyword
argument for all command arguments. The defined function can receive the
argument `name` (not uppercased) and must return a string,

```python
# ex01.py
import clig

def main(foo: str, bar: int = 32):
    return locals()

clig.run(main, metavarmodifier=lambda name: f"<<{name}>>")
```

```none
> python ex01.py -h

usage: main [-h] [--bar <<bar>>] <<foo>>

positional arguments:
  <<foo>>

options:
  -h, --help     show this help message and exit
  --bar <<bar>>
```

To specify different modifiers for positional and optional arguments, use
`posmetavarmodifier` and `optmetavarmodifier`, which takes precedence over
`metavarmodifier`.

```python
# ex02.py
import clig

def main(foo: str, bar: int = 32):
    return locals()

clig.run(main, optmetavarmodifier=lambda s: f"<<<{s}>>>")
```

```none
> python ex02.py -h

usage: main [-h] [--bar <<<bar>>>] foo

positional arguments:
  foo

options:
  -h, --help       show this help message and exit
  --bar <<<bar>>>
```

#### Help modifiers

Similarly to `metavarmodifier`, `helpmodifier` lets you define functions that
change the [`help`](https://docs.python.org/3/library/argparse.html#help)
keyword argument for all command arguments. The function should receive the
already set [`help`](https://docs.python.org/3/library/argparse.html#help)
argument and return a new string.

This can be useful to include
[format specifiers, already available in the original `help`](https://docs.python.org/3/library/argparse.html#help)
keyword argument.

To specify different modifiers for positional and optional arguments, you can
use `poshelpmodifier` and `opthelpmodifier` (which takes precedence over
`helpmodifier`).

```python
# ex03.py
import clig

def myprogram(foo: str, bar: int = 32):
    """Summary

    Args:
        foo: Description of foo.
        bar: Description of bar.
    """
    return locals()

posmodifier = lambda h: "The '%(dest)s' argument of '%(prog)s'. " + h
optmodifier = lambda h: "The '%(dest)s' argument of '%(prog)s'. " + h + " Defaults to %(default)s"

clig.run(myprogram, poshelpmodifier=posmodifier, opthelpmodifier=optmodifier)
```

```none
> python ex03.py -h

usage: myprogram [-h] [--bar BAR] foo

Summary

positional arguments:
  foo         The 'foo' argument of 'myprogram'. Description of foo.

options:
  -h, --help  show this help message and exit
  --bar BAR   The 'bar' argument of 'myprogram'. Description of bar. Defaults to 32
```

#### Help flags and messages

As you may know, `argparser`'s objects add an option by default, which simply
displays the command's help message (Normally
"`-h, --help show this help message and exit`") that can be disabled with
[`add_help=False`](https://docs.python.org/3/library/argparse.html#add-help).

Occasionally, you may not want to disable the help option, but simply change its
flags or message: that can be achieved by disabling the help option and adding a
new function argument with parameter
[`action="help"`](https://docs.python.org/3/library/argparse.html#action) in the
command line.

However, you may not want to add any new extra argument in the function to just
handle help messages, but still want to change them. For these cases, there are
two extra arguments, `help_flags` and `help_msg`, which do exactly that: Set
different help flags or different help message.

```python
# ex04.py
import clig

def main():
    pass

clig.run(main, help_flags=["-?", "--show-help"])
```

```none
> python ex04.py -?

usage: main [-?]

options:
  -?, --show-help  show this help message and exit
```

The parameter `help_msg` could be used as a simple way to change the help
message, maybe to a different language:

```python
# ex05.py
import clig

def main():
    pass

clig.run(main, help_msg="Diese Hilfe Meldung anzeigen und beenden")
```

```none
> python ex05.py -h

usage: main [-h]

options:
  -h, --help  Diese Hilfe Meldung anzeigen und beenden
```

#### Version

Normally, you can add a new function argument with parameter
[`action="version"`](https://docs.python.org/3/library/argparse.html#action) in
the command line, which expects a `version=` keyword argument in the
[`data()`](./userguide.md#argument-specification) call, prints version
information and exits when invoked.

However, you may not want to add any new extra argument in the function to just
handle version information, but still want to use that feature. For these cases,
there the extra arguments: `version`, `versionmodifier` and `version_msg`.

```python
# ex06.py
import clig

def my_program():
    pass

clig.run(my_program, version='%(prog)s 2.0')
```

```none
> python ex06.py -h

usage: my-program [-h] [--version]

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

```none
> python ex06.py --version

my-program 2.0
```

The `version` argument accepts a string like in the original
[argparse](https://docs.python.org/3/library/argparse.html#action) module (as
shown above) but also accepts a boolean. If `version=True`, `clig` tries to find
the version information from the function's package metadata.

```python
# ex07.py
import clig
import yaml

clig.run(yaml.add_constructor, version=True)
```

```none
> python ex07.py --version

6.0.3
```

Similarly to `metavarmodifier` and `helpmodifier`, `versionmodifier` lets you
define a function that change the version string. The function should receive
the version string and return a new string.

```python
# ex08.py
import clig
import yaml

clig.run(yaml.add_constructor, version=True, versionmodifier=lambda s: f"yaml-add-constructor v{s}")
```

```none
> python ex08.py --version

yaml-add-constructor v6.0.3
```

The option `versionhelp` lets you change the default help message for the
`--version` argument.

```python
# ex09.py
import clig

def main():
    pass

clig.run(main, version="1.2.3", versionhelp="Show the AWESOME information about version!")
```

```none
> python ex09.py --help

usage: main [-h] [--version]

options:
  -h, --help  show this help message and exit
  --version   Show the AWESOME information about version!
```

#### Automatic argument flags

As you may know, you can add extra _flags_ (options with prefix, normally `-` or
`--`) to arguments
[using the `data()` function in the argument annotation](./userguide.md#name-or-flags)
(on the function signature). However, you may want to add/change argument flags
automatically, without touching the function signature. For these cases, you can
use the booleans `make_flags` or `short_flags`.

##### Using `make_flags`

Setting `make_flags=True` creates flags even for required arguments

```python
# ex10.py
import clig

def main(foo: str, bar: int):
    pass

clig.run(main, make_flags=True)
```

```none
> python ex10.py -h

usage: main [-h] --foo FOO --bar BAR

options:
  -h, --help  show this help message and exit
  --foo FOO
  --bar BAR
```

For non-required arguments, `make_flags=False` turns them into required
arguments.

```python
# ex11.py
import clig

def main(foo: str = "baz", bar: int = 42):
    pass

clig.run(main, make_flags=False)
```

```none
> python ex11.py -h

usage: main [-h] foo bar

positional arguments:
  foo
  bar

options:
  -h, --help  show this help message and exit
```

For non-required arguments, `make_flags=True` creates the regular flags from the
argument names in the cases where they are not present in the data.

```python
# ex12.py
import clig

def main(
    foo: clig.Arg[str, clig.data("--foobar")] = "baz",
    bar: clig.Arg[int, clig.data("--barfoo")] = 42,
):
    pass

clig.run(main, make_flags=True) # forces creation of --foo and --bar
```

```none
> python ex12.py -h

usage: main [-h] [--foobar FOO] [--barfoo BAR]

options:
  -h, --help            show this help message and exit
  --foobar FOO, --foo FOO
  --barfoo BAR, --bar BAR
```

##### Using `make_shorts`

Setting `make_shorts=True` creates "short flags" only for the non-required
arguments.

```python
# ex13.py
import clig

def main(foo: str, bar: int = 42):
    pass

clig.run(main, make_shorts=True)
```

```none
> python ex13.py -h

usage: main [-h] [-b BAR] foo

positional arguments:
  foo

options:
  -h, --help         show this help message and exit
  -b BAR, --bar BAR
```

To force the creation of "short flags" for required arguments, pass both
`make_flags=True` and `make_shorts=True`:

```python
# ex14.py
import clig

def main(foo: str, bar: int = 42):
    pass

clig.run(main, make_shorts=True, make_flags=True)
```

```none
> python ex14.py -h

usage: main [-h] -f FOO [-b BAR]

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
  -b BAR, --bar BAR
```

The strategy to create "short flags" uses the following order:

- First lether of the argument name (the simplest case)
- First lether of the argument name UPPERCASED (when there are two names
  starting with same lether)
- First lether of the each argument name part if it has TWO_PARTS (separated by
  underscores)

If the rules above produce ambiguous flags, the strategy starts searching again
using first and second lethers. If ambiguity is found again, shearch for first,
second and third lethers, and so on.

```python
# ex15.py
import clig

def main(
    file: str = ".",
    filename: str = ".",
    filedir: str = ".",
    filepath: str = ".",
    file_name: str = ".",
    file_dir: str = ".",
    file_path: str = ".",
    folder: str = ".",
    foldername: str = ".",
    folderdir: str = ".",
    folderpath: str = ".",
    folder_name: str = ".",
    folder_dir: str = ".",
    folder_path: str = ".",
):
    pass

clig.run(main, make_shorts=True)
```

```none
> python ex15.py -h

usage: main [-h] [-f FILE] [-F FILENAME] [-fi FILEDIR] [-FI FILEPATH]
            [-fn FILE_NAME] [-fd FILE_DIR] [-fp FILE_PATH] [-fo FOLDER]
            [-FO FOLDERNAME] [-fol FOLDERDIR] [-FOL FOLDERPATH]
            [-fona FOLDER_NAME] [-fodi FOLDER_DIR] [-fopa FOLDER_PATH]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
  -F FILENAME, --filename FILENAME
  -fi FILEDIR, --filedir FILEDIR
  -FI FILEPATH, --filepath FILEPATH
  -fn FILE_NAME, --file-name FILE_NAME
  -fd FILE_DIR, --file-dir FILE_DIR
  -fp FILE_PATH, --file-path FILE_PATH
  -fo FOLDER, --folder FOLDER
  -FO FOLDERNAME, --foldername FOLDERNAME
  -fol FOLDERDIR, --folderdir FOLDERDIR
  -FOL FOLDERPATH, --folderpath FOLDERPATH
  -fona FOLDER_NAME, --folder-name FOLDER_NAME
  -fodi FOLDER_DIR, --folder-dir FOLDER_DIR
  -fopa FOLDER_PATH, --folder-path FOLDER_PATH
```

#### Docstring templates

- [ ] TODO

### Calling `clig.run()` without a function

It is possible to call the `clig.run()` without any arguments, even without the
function argument. To do this, a `Command` instance must have be created first,
using the
[`clig.command()` function as a function decorator](./subcommands.md#subcommands-using-function-decorators).

```python
# ex16.py
import clig

@clig.command
def main(foo: str, bar: int):
    pass

clig.run()
```

```none
> python ex16.py -h

usage: main [-h] foo bar

positional arguments:
  foo
  bar

options:
  -h, --help  show this help message and exit
```

## Parameters for `clig.Command()` constructor

The `clig.Command()` constructor accepts
[all arguments of the `clig.run()`](#parameters-for-cligrun-function) function.
It also accepts some other arguments related to subcommands.

The first parameter of the `clig.Command()` constructor is typically a function
that will be turned into a command. Additionally, other parameters can be
passed. They are the parameters of the original
[`ArgumentParser()` constructor](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser),
some parameters of the
[`ArgumentParser.add_subparsers()` method](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers)
(to control subcommands) and parameters of the
[`add_parser()`](https://github.com/python/cpython/blob/1ed98a6b5155dd239d35f3c9dd35477feded9e1c/Lib/argparse.py#L1246)
method, as detailed below.

The parameters of the original
[`ArgumentParser()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)
constructor can be passed in their original form (as _positional_ or _keyword_
arguments). Some default values follow the
[description in the previous section describing the `clig.run()` function](./advancedfeatures.md#parameters-of-the-original-argumentparser-object).

The parameters of the original
[`ArgumentParser.add_subparsers()` method](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers)
have to be passed only as _keyword_ arguments, with names prefixed with
`subcommands_` and has some default values, detailed in the following.

### Parameters of the original [`ArgumentParser.add_subparsers()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers) object

Except for some arguments (like [`action`]() and [`dest`]()), all parameter of
the [original `ArgumentParser.add_subparsers()` method]() can be specified in
the [`Command()` constructor](), for whose the names are prepended by
`subcommands_`. Some parameters has predefined values assumed by `clig` (which
can be modified), as detailed in the short descriptions below:

- `subcommands_title`: title for the sub-parser group in help output. By default
  it is `"subcommands"` if a description is provided, otherwise it uses the
  title for positional arguments, like the original behavior.

### Extra parameters specific of the [`clig.Command()`](clig.Command) constructor

The [`clig.Command()`](clig.Command) constructor has some extra parameters that
help to customize the interface and control subcommands.

- [ ] TODO

### Calling `clig.Command()` without a function

It is possible to call the `clig.Command()` without any arguments, even without
the function argument. This may be usefull when you want to create an object not
associated with any function, and add subcommands after:

```python
# ex17.py
from clig import Command

cmd = Command()

def foo():
    pass

def bar():
    pass

cmd.add_subcommand(foo).add_subcommand(bar).run()
```

```none
> python ex17.py -h

usage: ex17.py [-h] {foo,bar} ...

positional arguments:
  {foo,bar}

options:
  -h, --help  show this help message and exit
```
