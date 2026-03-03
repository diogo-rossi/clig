# %%          IMPORTS AND SETTINGS
############# IMPORTS AND SETTINGS ###########################################################################

import importlib
import inspect
import os
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict

import git
from pyprj import nbmd
from pyprj.markdown_utils import get_markdown_sections
from pyprj.pyproject import author_name, pkg_name, pkg_version, pyproject
from sphinx.application import Sphinx

import clig


class PyDomainInfo(TypedDict):
    module: str
    fullname: str


COLUMNS: int = 100
try:
    COLUMNS = os.get_terminal_size().columns
except OSError:
    pass
SEP: str = COLUMNS * "-"

THIS_DIR: Path = Path(__file__).parent.resolve()
os.chdir(THIS_DIR)

notebooks_dirpath: Path = Path("./notebooks")

nbmd.nbmd(notebooks_dirpath, dont_run_notebooks_before=False)

INITIAL_README: str = """# `clig` - CLI Generator

A single module, pure python, **Command Line Interface Generator**.

OBS: currently under development.

"""


index_sections: list[str] = get_markdown_sections(Path("index.md"))
userguide_sections: list[str] = get_markdown_sections(notebooks_dirpath / "userguide.md")


readme: str = (
    (INITIAL_README + index_sections[2] + "".join(userguide_sections))
    .replace(
        "./advancedfeatures.md",
        "https://github.com/diogo-rossi/clig/blob/main/docs/sphinx/source/notebooks/advancedfeatures.md",
    )
    .replace("", "")
)


with open(pyproject.dirpath / "README.md", "w", encoding="utf-8") as file:
    file.write(readme)


git_repo = git.Repo(".", search_parent_directories=True)
code_url = f"https://github.com/diogo-rossi/clig/blob/main/"


# %%          SPHINX DATA
############# SPHINX DATA ####################################################################################

project = pkg_name
copyright = f"{datetime.now().year}, {author_name}"
author = author_name
release = pkg_version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinxnotes.comboroles",
    "sphinx.ext.linkcode",
]

templates_path = ["_templates"]
exclude_patterns = []

maximum_signature_line_length = 70
napoleon_google_docstring = True
napoleon_numpy_docstring = False
default_role = "code"

myst_heading_anchors = 4
myst_enable_extensions = [
    "dollarmath",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#math-shortcuts
    "amsmath",
    "html_image",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images
    "colon_fence",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

html_theme = "furo"
html_title = f'<p style="text-align: center"><b>{pkg_name}</b></p>'
html_css_files = ["css/custom.css"]
html_logo = "../../logo.png"


def linkcode_resolve(domain: Literal["py", "c", "cpp", "javascript"], info: PyDomainInfo):
    if domain != "py":
        print("---------------- here")
        return None
    if not info["module"]:
        print("---------------- there")
        return None

    mod = importlib.import_module(info["module"])
    if "." in info["fullname"]:
        objname, attrname = info["fullname"].split(".")
        obj = getattr(mod, objname)
        try:
            # object is a method of a class
            obj = getattr(obj, attrname)
        except AttributeError:
            # object is an attribute of a class
            print("---------------- other")
            return None
    else:
        obj = getattr(mod, info["fullname"])

    try:
        file = inspect.getsourcefile(obj)
        lines = inspect.getsourcelines(obj)
    except TypeError:
        # e.g. object is a typing.Union
        print("---------------- otherother")
        return None
    if file is None:
        print("---------------- otherotherother")
        return None
    file = Path(file).resolve().relative_to(git_repo.working_dir)
    # if file.parts[0] != "clig":
    # e.g. object is a typing.NewType
    # print(f"---------------- {file}")
    # return None
    start, end = lines[1], lines[1] + len(lines[0]) - 1

    # return "https://github.com/diogo-rossi/clig"  # f"{code_url}/{file}#L{start}-L{end}"
    return f"{code_url}/{file}#L{start}-L{end}"


def convert_admonitions_to_myst(app, filename, lines: list[str]):
    _GITHUB_ADMONITIONS = {
        "> [!NOTE]": "note",
        "> [!TIP]": "tip",
        "> [!IMPORTANT]": "important",
        "> [!WARNING]": "warning",
        "> [!CAUTION]": "caution",
    }

    # loop through lines, replace github admonitions
    for i, orig_line in enumerate(lines):
        orig_line_splits = orig_line.split("\n")
        replacing = False
        for j, line in enumerate(orig_line_splits):
            # look for admonition key
            for admonition_key in _GITHUB_ADMONITIONS:
                if admonition_key in line:
                    line = line.replace(admonition_key, "```{" + _GITHUB_ADMONITIONS[admonition_key] + "}\n")
                    # start replacing quotes in subsequent lines
                    replacing = True
                    break
            else:
                # replace indent to match directive
                if replacing and "> " in line:
                    line = line.replace("> ", "  ")
                elif replacing:
                    # missing "> ", so stop replacing and terminate directive
                    line = f"\n```\n{line}"
                    replacing = False
            # swap line back in splits
            orig_line_splits[j] = line
        # swap line back in original
        lines[i] = "\n".join(orig_line_splits)


def setup(app: Sphinx):
    print(SEP)
    print("> Converting admonitions to MyST format")
    app.connect("source-read", convert_admonitions_to_myst)
    print("> Adding custom CSS file")
    app.add_css_file("custom.css")
    print(SEP)
