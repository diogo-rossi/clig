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
2. It has some flexibility over the use of docstrings.
3. It uses `argparse` under the hood, with concepts of `argparse`. So you don't
   need to learn anything new (if you already know the _stdlib_ module
   `argparse`).

## List of packages

A lot of packages out there solves the same problem as `clig`, i.e., generates a
CLI. But they have basically 2 different approaches.

## Download the module

You can just download the `clig`'s module to use in some restrict environment,
place it in your path and import it.

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
