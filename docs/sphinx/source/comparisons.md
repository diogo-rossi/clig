# Comparisons and features

There is a [lot of packages out there](#list-of-packages) that solve the same
problem as `clig`.

The first one that I have tested which uses a similar approach and is very
popular was [`typer`](https://typer.tiangolo.com/). It is a very usefull, modern
and complete package, with a large comunity, but it lacked some features I
wanted for `clig`, specially related to docstrings.

Another very complete package that also solves `typer` problems is
[`cyclopts`](https://cyclopts.readthedocs.io/en/stable/). To be honest, I almost
gave up making this module after knowing `cyclopts`, because it is really a very
good package.

However, `clig` has some advantages that may be important in some scenarios:

1. It is a single module, with no dependencies, pure python. Actually, you can
   just [download it](#download-the-module), place in some folder and import in
   your script.
2. It has some flexibility on the use of
   [docstrings](./notebooks/advancedfeatures.md#docstring-templates) and
   generation of
   [argument flags](./notebooks/advancedfeatures.md#automatic-argument-flags).
3. It uses `argparse` under the hood, with the concepts of `argparse`. So you
   don't need to learn anything new (if you already know how to use the _stdlib_
   module `argparse`).

## List of packages

A lot of packages out there solves the same problem as `clig`, i.e., generates a
CLI. But they have basically 2 different approaches.

In the first approach, the API tries to create a proxy object that can be used
by functions subsequently. So, the interface is decoupled from the
implementation. This is the strategy taken by `argparse`/`optparse` in the
_stdlib_. Some packages that follows this strategy are listed below:

- [`argparse`](https://docs.python.org/3/library/argparse.html)
- [`optparse`](https://docs.python.org/3/library/optparse.html)
- [`clout`](https://clout.readthedocs.io/en/latest/index.html)
- [`simple-parsing`](https://pypi.org/project/simple-parsing/)
- [`dataparsers`](https://dataparsers.readthedocs.io/en/latest/)
- [`datargs`](https://pypi.org/project/datargs/)
- [`dargparser`](https://pypi.org/project/dargparser/)
- [`argparse-dataclasses`](https://pypi.org/project/argparse-dataclasses/)
- [`argparse-dataclass`](https://pypi.org/project/argparse-dataclass/)

In the second approach, the interface is coupled with the implementation. It is
useful when the implementation itself is already documented (with type
declaration and/or functions docstrings), so the interface generation doesn't
require additional re-work. This is the strategy taken by `clig`. Some other
packages that follows this strategy are listed below:

- [`click`](https://click.palletsprojects.com/en/stable/)
- [`typer`](https://typer.tiangolo.com/)
- [`cyclopts`](https://cyclopts.readthedocs.io/en/stable/)
- [`fire`](https://pypi.org/project/fire/)

## Download the module

Since `clig` is made of a single module, you can just download the `clig.py`
module to use in some restrict environment, place it in your path and import it.

- Download the module with `curl`

```PowerShell
curl -L -o clig.py https://raw.githubusercontent.com/diogo-rossi/clig/refs/heads/main/src/clig/clig.py
```

- Download the module with `wget`

```PowerShell
wget https://raw.githubusercontent.com/diogo-rossi/clig/refs/heads/main/src/clig/clig.py -O clig.py
```

- Download the module with PowerShell (Windows)

```PowerShell
iwr -uri "https://raw.githubusercontent.com/diogo-rossi/clig/refs/heads/main/src/clig/clig.py" -out "clig.py"
```
