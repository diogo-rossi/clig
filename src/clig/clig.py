##############################################################################################################
# %%          IMPORTS
##############################################################################################################

from __future__ import annotations

import inspect
import re
import sys
from argparse import ArgumentParser, FileType, HelpFormatter, Action, BooleanOptionalAction, Namespace
from argparse import HelpFormatter, RawTextHelpFormatter, _SubParsersAction  # [_ArgumentParserT]
from argparse import _ArgumentGroup, _MutuallyExclusiveGroup
from dataclasses import KW_ONLY, Field, dataclass, field
from inspect import Parameter
from inspect import _ParameterKind
from types import UnionType
from collections import OrderedDict
from collections.abc import Sequence
from typing import get_args, get_origin, Union, Annotated
from typing import Any, Callable, Iterable, Literal, Mapping, Self, TypedDict, Unpack, overload
from enum import Enum, StrEnum
from importlib.metadata import PackageNotFoundError
from importlib.metadata import distributions as pkg_distributions
from importlib.metadata import version as pkg_metadata_version

Kind = _ParameterKind
Arg = Annotated

EMPTY = Parameter.empty

##############################################################################################################
# %%          DOCSTRINGS TEMPLATES
##############################################################################################################

DESCRIPTION_DOCSTRING = """{{description}}"""

DESCRIPTION_EPILOG_DOCSTRING = """
    {{description}}    

    {{epilog}}
"""

NUMPY_DOCSTRING_WITH_EPILOG = """
    {{description}}

    {{epilog}}

    Parameters
    ----------
    {{parameter_name}} : {{parameter_type}}
        {{parameter_description}}
"""

NUMPY_DOCSTRING_WITH_EPILOG_NOTYPES = """
    {{description}}

    {{epilog}}

    Parameters
    ----------
    {{parameter_name}}
        {{parameter_description}}
"""

SPHINX_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""

SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
"""

GOOGLE_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""

GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}}: {{parameter_description}}
"""

GOOGLE_DOCSTRING_NOTYPES = """
{{description}}

Args:
    {{parameter_name}}: {{parameter_description}}
"""

CLIG_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}
    {{parameter_description}}
"""


NUMPY_DOCSTRING = """
    {{description}}

    Parameters
    ----------
    {{parameter_name}} : {{parameter_type}}
        {{parameter_description}}
"""

SPHINX_DOCSTRING = """
{{description}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""

GOOGLE_DOCSTRING = """
{{description}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""

CLIG_DOCSTRING = """
{{description}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}
    {{parameter_description}}
"""

CLIG_DOCSTRING_SHORT = """
{{description}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}: {{parameter_description}}
"""

# TODO: add 'no type' variants

DOCSTRING_TEMPLATES = [
    NUMPY_DOCSTRING_WITH_EPILOG,
    SPHINX_DOCSTRING_WITH_EPILOG,
    GOOGLE_DOCSTRING_WITH_EPILOG,
    CLIG_DOCSTRING_WITH_EPILOG,
    NUMPY_DOCSTRING_WITH_EPILOG_NOTYPES,
    SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES,
    GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES,
    GOOGLE_DOCSTRING_NOTYPES,
    NUMPY_DOCSTRING,
    SPHINX_DOCSTRING,
    GOOGLE_DOCSTRING,
    CLIG_DOCSTRING,
    CLIG_DOCSTRING_SHORT,
    DESCRIPTION_DOCSTRING,
    DESCRIPTION_EPILOG_DOCSTRING,
]

SUBPARSERS_DEST = "subcommand_"


class DocStr(StrEnum):
    DESCRIPTION_DOCSTRING = DESCRIPTION_DOCSTRING
    DESCRIPTION_EPILOG_DOCSTRING = DESCRIPTION_EPILOG_DOCSTRING
    NUMPY_DOCSTRING_WITH_EPILOG = NUMPY_DOCSTRING_WITH_EPILOG
    NUMPY_DOCSTRING_WITH_EPILOG_NOTYPES = NUMPY_DOCSTRING_WITH_EPILOG_NOTYPES
    SPHINX_DOCSTRING_WITH_EPILOG = SPHINX_DOCSTRING_WITH_EPILOG
    SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES = SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES
    GOOGLE_DOCSTRING_WITH_EPILOG = GOOGLE_DOCSTRING_WITH_EPILOG
    GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES = GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES
    CLIG_DOCSTRING_WITH_EPILOG = CLIG_DOCSTRING_WITH_EPILOG
    NUMPY_DOCSTRING = NUMPY_DOCSTRING
    SPHINX_DOCSTRING = SPHINX_DOCSTRING
    GOOGLE_DOCSTRING = GOOGLE_DOCSTRING
    CLIG_DOCSTRING = CLIG_DOCSTRING
    CLIG_DOCSTRING_SHORT = CLIG_DOCSTRING_SHORT
    GOOGLE_DOCSTRING_NOTYPES = GOOGLE_DOCSTRING_NOTYPES


##############################################################################################################
# %%          MAIN CLASS
##############################################################################################################


@dataclass
class Command:
    """The base class to create commands from functions."""

    func: Callable[..., Any] | None = None
    """The function that will be turned into a command."""

    # Arguments for `ArgumentParser` object, see: https://docs.python.org/3/library/argparse.html#argumentparser-objects

    prog: str | None = None
    """The name of the program (default: generated from the function name).   
    https://docs.python.org/3/library/argparse.html#prog
    """

    usage: str | None = None
    """The string describing the program usage (default: generated from arguments added to parser).   
    https://docs.python.org/3/library/argparse.html#usage
    """

    description: str | None = None
    """Text to display before the argument help (by default, collected from the docstring when possible).   
    https://docs.python.org/3/library/argparse.html#description
    """

    epilog: str | None = None
    """Text to display after the argument help (by default, collected from the docstring when possible).   
    https://docs.python.org/3/library/argparse.html#epilog
    """

    parents: Sequence[ArgumentParser] = field(default_factory=list)
    """A list of `ArgumentParser` objects whose arguments should also be included.   
    https://docs.python.org/3/library/argparse.html#parents
    """

    formatter_class: type[HelpFormatter] = RawTextHelpFormatter
    """A class for customizing the help output (by default, `argparse.RawTextHelpFormatter`).   
    https://docs.python.org/3/library/argparse.html#formatter-class
    """

    prefix_chars: str = "-"
    """The set of characters that prefix optional arguments (default: `"-"`).   
    https://docs.python.org/3/library/argparse.html#prefix-chars
    """

    fromfile_prefix_chars: str | None = None
    """The set of characters that prefix files from which additional arguments should be read (default: `None`).   
    https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars
    """

    argument_default: Any = None
    """ The global default value for arguments (default: `None`).   
    https://docs.python.org/3/library/argparse.html#argument-default
    """

    conflict_handler: str = "error"
    """The strategy for resolving conflicting optionals (usually unnecessary).   
    https://docs.python.org/3/library/argparse.html#conflict-handler
    """

    add_help: bool = True
    """Add a `-h/--help` option to the parser (default: `True`).   
    https://docs.python.org/3/library/argparse.html#add-help
    """

    allow_abbrev: bool = True
    """Allows long options to be abbreviated if the abbreviation is unambiguous (default: `True`).   
    https://docs.python.org/3/library/argparse.html#allow-abbrev
    """

    exit_on_error: bool = True
    """Determines whether or not ArgumentParser exits with error info when an error occurs. (default: `True`).   
    https://docs.python.org/3/library/argparse.html#exit-on-error
    """

    # Arguments for `add_subparsers()` method, see: https://docs.python.org/3/library/argparse.html#subcommands
    _: KW_ONLY

    subcommands_title: str = "subcommands"
    """Title for the sub-parser group in help output; by default `"subcommands"` if description is provided,
    otherwise uses title for positional arguments."""

    subcommands_description: str | None = None
    """Description for the sub-parser group in help output, by default `None`."""

    subcommands_prog: str | None = None
    """Usage information that will be displayed with subcommand help, by default the name of the program and
    any positional arguments before the subparser argument."""

    subcommands_required: bool = False
    """Whether or not a subcommand must be provided, by default `False` (added in 3.7).   
    https://docs.python.org/3/library/argparse.html#required
    """

    subcommands_help: str | None = None
    """Help for sub-parser group in help output, by default `None`.   
    https://docs.python.org/3/library/argparse.html#help
    """

    subcommands_metavar: str | None = None
    """String presenting available subcommands in help; by default it is `None` and presents subcommands
    in form `{cmd1, cmd2, ..}`.   
    https://docs.python.org/3/library/argparse.html#metavar
    """

    # Arguments for `add_parser()` method, see: https://docs.python.org/3/library/argparse.html#subcommands

    name: str | None = None
    """Name of the subcommand, taken by the `add_parser()` method."""

    help: str | None = None
    """A help message for the subparser command."""

    aliases: Sequence[str] = field(init=False, default_factory=list)
    """Sequence that allows multiple strings to refer to the same subparser"""

    # Extra arguments of this library

    docstring_template: str | DocStr | None = None
    """The template used to parse parameter descriptions from the function's docstring.
    When `None`, clig auto-detects the format by trying all known templates in order
    (NumPy, Sphinx, Google, clig-style). Set this explicitly to skip auto-detection and
    enforce a specific format. Use a `DocStr` enum member or any of the
    `NUMPY_DOCSTRING`, `SPHINX_DOCSTRING`, `GOOGLE_DOCSTRING`, `CLIG_DOCSTRING`
    module-level constants (and their variants).
    """

    default_bool: bool = False
    """The default value assumed for `bool`-annotated parameters when deciding the
    argparse action. When `False` (the default), a `bool` parameter with no default
    generates a `store_true` action (flag absent → `False`, flag present → `True`).
    When `True`, the action becomes `store_false` (flag absent → `True`, flag present →
    `False`). This setting is overridden per-argument when the parameter already has an
    explicit default value.
    """

    make_flags: bool | None = None
    """Whether to turn all positional-like parameters into optional flags (i.e. add a
    `--name` prefix). When `None` (the default), clig decides per-argument: parameters
    that have a default value are automatically promoted to flags; those without remain
    positional. Set to `True` to force every argument to be a flag, or `False` to keep
    every argument positional regardless of defaults. Per-argument `make_flag` metadata
    takes precedence over this setting.
    """

    make_shorts: bool | None = None
    """Whether to automatically generate a short flag (e.g. `-n`) alongside every long
    flag (e.g. `--name`). When `None` (the default) or `False`, only the long flag is
    used. When `True`, clig derives the shortest non-conflicting single-character option
    from the argument name and prepends it to the flag list. Short flags are also added
    to the help (`-h`) and version (`-v`) options when this is enabled.
    """

    metavarmodifier: str | Sequence[str] | Callable[[str], str] | None = None
    """A modifier applied to the displayed metavar of *all* arguments (both positional
    and optional) in the help output. A plain `str` replaces the metavar with that
    string; a `Sequence[str]` is used as a fixed tuple of metavar tokens (for multi-value
    arguments); a callable receives the argument name and must return the desired
    metavar string. `None` leaves the metavar at its argparse default. Acts as a
    fallback for both `posmetavarmodifier` and `optmetavarmodifier` when those are
    `None`.
    """

    posmetavarmodifier: str | Sequence[str] | Callable[[str], str] | None = None
    """A modifier applied to the metavar of *positional* arguments only. Follows the
    same rules as `metavarmodifier` (str, sequence, or callable). When set, takes
    precedence over `metavarmodifier` for positional arguments; when `None`, falls back
    to `metavarmodifier`.
    """

    optmetavarmodifier: str | Sequence[str] | Callable[[str], str] | None = None
    """A modifier applied to the metavar of *optional* (flagged) arguments only. Follows
    the same rules as `metavarmodifier` (str, sequence, or callable). When set, takes
    precedence over `metavarmodifier` for optional arguments; when `None`, falls back to
    `metavarmodifier`.
    """

    helpmodifier: Callable[[str], str] | None = None
    """A callable applied to the help string of *all* arguments before it is passed to
    argparse. Receives the current help string (may be an empty string if no help was
    found) and must return the final string to display. Useful for appending default
    values, wrapping text, or adding ANSI colours uniformly. Acts as a fallback for both
    `poshelpmodifier` and `opthelpmodifier` when those are `None`.
    """

    poshelpmodifier: Callable[[str], str] | None = None
    """A callable applied to the help string of *positional* arguments only. Follows the
    same contract as `helpmodifier`. When set, takes precedence over `helpmodifier` for
    positional arguments; when `None`, falls back to `helpmodifier`.
    """

    opthelpmodifier: Callable[[str], str] | None = None
    """A callable applied to the help string of *optional* (flagged) arguments only.
    Follows the same contract as `helpmodifier`. When set, takes precedence over
    `helpmodifier` for optional arguments; when `None`, falls back to `helpmodifier`.
    """

    help_flags: Sequence[str] = field(default_factory=tuple)
    """The flag strings that trigger the help action (default: `("-h", "--help")`).
    When this is non-empty *or* `help_msg` is set, the built-in argparse help is
    disabled (`add_help=False`) and a custom help argument is registered instead using
    these flags and `help_msg`. Pass an empty sequence together with `help_msg` to keep
    the default `-h`/`--help` flags while customising only the message.
    """

    help_msg: str | None = None
    """The help text shown for the help option itself (the line that describes `-h,
    --help` in the usage output). Defaults to `"show this help message and exit"` when
    `help_flags` is provided or this field is set. Setting either `help_flags` or
    `help_msg` disables the standard argparse help mechanism so that the custom flags and
    message are used instead.
    """

    version: bool | str = False
    """Whether to add version information to the command. Defaults to `False`.
    If `True`, tries to find the version from the function's package.
    If it is a string, use the string as the version information."""

    versionmodifier: Callable[[str], str] | None = None
    """A callable applied to the version string before it is passed to argparse's
    `version` action. Receives the resolved version string (whether auto-detected from
    the package metadata or supplied directly via `version`) and must return the final
    string to display when `--version` is invoked. Useful for adding a program name
    prefix, ANSI colours, or extra build metadata (e.g. `lambda v: f"my_tool {v}"`).
    `None` leaves the version string unchanged. Has no effect when `version` is `False`.
    """

    # Extra arguments of this library not initialized

    parent: Command | None = field(init=False, default=None)
    parser: ArgumentParser | None = field(init=False, default=None)

    def __post_init__(self):

        self.parameters: Mapping[str, Parameter] = {}
        """A dict with `name: Parameter`, where `Parameter` comes from stdlib `inspect`
        ref: https://docs.python.org/3/library/inspect.html#inspect.Parameter"""

        if self.func:
            self.name = self.name or self.func.__name__.replace("_", "-")
            self.parameters = inspect.signature(self.func).parameters

        self.docstring_data: _DocstringData | None = self._get_data_from_docstring()
        self.argument_data: list[_ArgumentData] = self.__generate_argument_data_list()
        if self.docstring_data:
            self.description = self.description or self.docstring_data.description
            self.epilog = self.epilog or self.docstring_data.epilog

        self.sub_commands: OrderedDict[str, Command] = OrderedDict()
        self.sub_commands_group: _SubParsersAction | None = None
        self.longstartflags: str = f"{self.prefix_chars}" * 2

        self._argument_groups: list[ArgumentGroup] = []
        self._mutually_exclusive_groups: list[MutuallyExclusiveGroup] = []

        if self.help_flags or self.help_msg:
            self.add_help = False

        self.opthelpmodifier = self.opthelpmodifier or self.helpmodifier
        self.poshelpmodifier = self.poshelpmodifier or self.helpmodifier
        self.optmetavarmodifier = self.optmetavarmodifier or self.metavarmodifier
        self.posmetavarmodifier = self.posmetavarmodifier or self.metavarmodifier

        self.help_flags = self.help_flags or (("-h", "--help") if self.add_help or self.help_msg else ())
        self.version_flags = (
            ("-v", "--version")
            if self.version and self.make_shorts
            else ("--version",) if self.version else ()
        )

    ##########################################################################################################
    # %:          PUBLIC METHODS
    ##########################################################################################################

    @overload
    def subcommand[**P, T](self, func: Callable[P, T]) -> Callable[P, T]: ...

    @overload
    def subcommand[**P, T](
        self, **kwargs: Unpack[CompleteCommandArguments]
    ) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

    def subcommand[**P, T](
        self,
        func: Callable[P, T] | None = None,
        **kwargs: Unpack[CompleteCommandArguments],
    ) -> Callable[P, T] | Callable[[Callable[P, T]], Callable[P, T]]:
        """Add a subcommand and return the input function unchanged. Suitable to use as decorator."""
        if func is not None:
            self.new_subcommand(func)
            return func

        def wrap(func):
            self.new_subcommand(func, **kwargs)
            return func

        return wrap

    def add_subcommand(
        self, func: Callable[..., Any], *args, **kwargs: Unpack[CompleteCommandArguments]
    ) -> Self:
        """Add a subcommand and return the caller object. Suitable to add multiple subcommands in a row."""
        self.new_subcommand(func, *args, **kwargs)
        return self

    def end_subcommand(
        self, func: Callable[..., Any], *args, **kwargs: Unpack[CompleteCommandArguments]
    ) -> Command:
        """Add a subcommand and return the parent `Command` instance of the caller object.
        If `parent` attribute is `None`, raise `ValueError`."""
        if self.parent is None:
            raise ValueError(
                "\n\nMethod `end_subcommand()` can not be called by `Command` instances without parent.\n\n"
            )
        self.new_subcommand(func, *args, **kwargs)
        return self.parent

    def new_subcommand(
        self,
        func: Callable[..., Any],
        name: str | None = None,
        help: str | None = None,
        aliases: Sequence[str] | None = None,
        *args,
        **kwargs: Unpack[CommandArguments],
    ) -> Command:
        """Add a subcommand and return the new created subcommand (a new `Command` instance)"""
        # TODO: add `deprecated` included in v3.13
        count = 0
        parent_parser = self.parent
        while parent_parser:
            count += 1
            parent_parser = parent_parser.parent
        cmd: Command = Command(func, *args, **kwargs)
        cmd.name = name or func.__name__
        if not hasattr(self, "subparsers_dest"):
            self.subparsers_dest: str = ""
        self.subparsers_dest = ",".join(
            [self.subparsers_dest[1 : -1 * (count + 1)], cmd.name] if self.subparsers_dest else [cmd.name]
        )
        self.subparsers_dest = "{" + self.subparsers_dest + "}" + " " * count
        cmd.aliases = aliases or []
        help = help or (cmd.description.strip().split("\n")[0] if cmd.description else None)  # one line
        cmd.help = help
        cmd.parent = self
        cmd.__sanitize_argument_data_names()
        self.sub_commands.update({cmd.name: cmd})
        return cmd

    def print_help(self):
        if self.parser is None:
            self._add_parsers()
        assert self.parser is not None
        self.parser.print_help()

    def run(self, args: Sequence[str] | None = None) -> Any:
        # TODO: `Context` object
        # TODO: treat variatic argument as parse_know
        # TODO: treat "positional only"?
        if args == None:
            args = sys.argv[1:]
        if self.parser is None:
            self._add_parsers()
        assert self.parser is not None
        namespace: Namespace
        rest: list[str] = []
        starargs: list[str] = []
        starkwargs: dict[str, str] = {}
        if any([argdata.kind in [Kind.VAR_POSITIONAL, Kind.VAR_KEYWORD] for argdata in self.argument_data]):
            namespace, rest = self.parser.parse_known_args(args)
            starargs, starkwargs = self._get_unknown_args(rest)
        else:
            namespace: Namespace = self.parser.parse_args(args)
        # TODO Enum decoverter
        for arg in self.argument_data:
            annotation = arg.typeannotation
            if get_origin(annotation) in [Union, UnionType]:
                annotation = [t for t in get_args(annotation) if t is not type(None)][0]
            if isinstance(annotation, type) and issubclass(annotation, Enum):
                setattr(namespace, arg.name, annotation[getattr(namespace, arg.name)])
            if get_origin(annotation) is Literal:
                types = get_args(annotation)
                for t in types:
                    choice_type = type(t)
                    if issubclass(choice_type, Enum):
                        try:
                            setattr(namespace, arg.name, choice_type[getattr(namespace, arg.name)])
                        except:
                            continue
            if (
                get_origin(annotation) is tuple
                or (isinstance(annotation, type) and issubclass(annotation, tuple))
            ) and (
                arg.kwargs.get("default") is EMPTY
                or arg.kwargs.get("default") != getattr(namespace, arg.name)
            ):
                try:
                    setattr(namespace, arg.name, tuple(getattr(namespace, arg.name)))
                except TypeError:
                    setattr(namespace, arg.name, (getattr(namespace, arg.name)))
        subcommand_name = (
            getattr(namespace, self.subparsers_dest) if hasattr(self, "subparsers_dest") else None
        )
        if self.parent is None:
            self.context = Context(namespace=namespace, command=self)
        else:
            self.context = self.parent.context
        result = None
        if self.func:
            result = self.func(
                *self._get_pos_parameters(namespace, starargs),
                **self._get_kw_parameters(namespace, starkwargs),
            )
        if subcommand_name is not None:
            args = args[args.index(subcommand_name) + 1 :]
            return self.sub_commands[subcommand_name].run(args)
        return result

    ##########################################################################################################
    # %:          PRIVATE METHODS
    ##########################################################################################################

    def __repr__(self, indent: int = 0) -> str:
        return (
            f"{''.ljust(indent)}{'Sub' if self.parent is not None else ''}Command("
            + "".join(
                [
                    f"{"\n".ljust(indent+5)}{name} = {getattr(self,name)}"
                    for name in ["func", "name", "description"]
                ]
            )
            + "".join([f"\n{self.sub_commands[s].__repr__(indent=indent+4)}" for s in self.sub_commands])
            + f"{"\n".ljust(indent+1)})"
        )

    def __generate_argument_data_list(self) -> list[_ArgumentData]:
        argument_data: list[_ArgumentData] = []
        for par in self.parameters:
            data: _ArgumentData = _get_argument_data_from_parameter(self.parameters[par])
            data.help = self.docstring_data.helps.get(data.name, None) if self.docstring_data else None
            argument_data.append(data)
        return argument_data

    def __sanitize_argument_data_names(self) -> None:
        if self.parent:
            names: list[str] = [arg.name for arg in self.parent.argument_data]
            strip_names: list[str] = [n.strip() for n in names]
            for arg in self.argument_data:
                if arg.name.strip() in strip_names:
                    arg.name = names[strip_names.index(arg.name.strip())] + " "

    def _get_pos_parameters(self, namespace: Namespace, starargs: list[str]) -> list[Any]:
        args = []
        for argdata in self.argument_data:
            if argdata.kind not in [
                Kind.POSITIONAL_OR_KEYWORD,
                Kind.POSITIONAL_ONLY,
            ]:
                break
            if _is_context_annotation(argdata.typeannotation):
                args.append(self.context)
            else:
                args.append(_getattr_with_spaces(namespace, argdata.name))
        t = str
        for argdata in self.argument_data:
            if argdata.kind in [Kind.VAR_POSITIONAL]:
                t = argdata.typeannotation if callable(argdata.typeannotation) else str
                break
        args.extend([t(v) for v in starargs])
        return args

    def _get_kw_parameters(self, namespace: Namespace, starkwargs: dict[str, Any]) -> OrderedDict:
        kwargs = OrderedDict(
            {
                argdata.name.strip(): _getattr_with_spaces(namespace, argdata.name)
                for argdata in self.argument_data
                if argdata.kind in [Kind.KEYWORD_ONLY]
                and not (_is_context_annotation(argdata.typeannotation))
            }
        )
        t = str
        for argdata in self.argument_data:
            if isinstance(argdata.typeannotation, type) and issubclass(argdata.typeannotation, Context):
                if argdata.kind in [Kind.KEYWORD_ONLY]:
                    kwargs.update({argdata.name: self.context})
            if argdata.kind in [Kind.VAR_KEYWORD]:
                t = argdata.typeannotation if callable(argdata.typeannotation) else str
                break
        kwargs.update(
            {k: [t(item) for item in v] if isinstance(v, list) else t(v) for k, v in starkwargs.items()}
        )
        return kwargs

    def _get_unknown_args(self, args: list[str]) -> tuple[list[str], dict[str, Any]]:
        pos = []
        i = 0
        while i < len(args) and not args[i].startswith("-"):
            pos.append(args[i])
            i += 1
        opts = {}
        current_key = None
        current_values = []
        while i < len(args):
            token = args[i]
            if token.startswith(self.prefix_chars):
                if current_key is not None:
                    if len(current_values) == 1:
                        opts[current_key] = current_values[0]
                    else:
                        opts[current_key] = current_values
                current_key = token.lstrip(self.prefix_chars)
                current_values = []
            else:
                current_values.append(token)
            i += 1
        if current_key is not None:
            if len(current_values) == 1:
                opts[current_key] = current_values[0]
            else:
                opts[current_key] = current_values
        return pos, opts

    def _get_data_from_docstring(self) -> _DocstringData | None:
        if self.docstring_template:
            return self._collect_docstring_data_using_template(self.docstring_template)
        for template in DOCSTRING_TEMPLATES:
            data: _DocstringData | None = self._collect_docstring_data_using_template(template)
            if data:
                return data
        docstring = _normalize_docstring(self.func.__doc__)
        if docstring:
            return _DocstringData(description=docstring, epilog=None)
        return None

    def _collect_docstring_data_using_template(self, template: str | None = None) -> _DocstringData | None:
        docstring = _normalize_docstring(self.func.__doc__)
        if not docstring:
            return None
        separator: str = "################################" * 30
        template = template or self.docstring_template
        parameter_number = len(
            [
                par
                for par in self.parameters
                if self.parameters[par].kind not in [Kind.VAR_KEYWORD, Kind.VAR_POSITIONAL]
            ]
        )
        # escape for regex match, but not "{" and "}"
        template = re.escape(_normalize_docstring(template) + "\n").replace(r"\{", "{").replace(r"\}", "}")
        place_holders: dict[str, list[int]] = {
            "description": [],
            "epilog": [],
            "parameter_name": [],
            "parameter_type": [],
            "parameter_description": [],
        }
        detected_place_holders: list[str] = re.findall(r"{{.*?}}", template)
        order_counter = 0
        for word in detected_place_holders:
            word = word.removeprefix("{{").removesuffix("}}")
            if word in place_holders:
                place_holders[word].append(order_counter)
                order_counter += 1
        parameter_section_init_index: int = 0
        for i, line in enumerate(template.splitlines()):
            if any([f"{{{{{key}}}}}" in line for key in place_holders if key.startswith("parameter")]):
                parameter_section_init_index = i
                break
        parameter_section_length = sum(
            [template.count(f"{{{{{key}}}}}") for key in place_holders if key.startswith("parameter")]
        )
        if parameter_number > 0 and not parameter_section_length:
            return None
        if parameter_section_length:
            parameter_section = "\n".join(template.splitlines()[parameter_section_init_index:])
            for _ in range(parameter_number - 1):
                template += f"{parameter_section}\n"
        else:
            docstring = docstring.rstrip() + f"\n{separator}"
            template = template.rstrip() + f"\n{re.escape(separator)}\n"
        for place_holder in place_holders:
            template = template.replace(f"{{{{{place_holder}}}}}", "(?! )(.*?)")
        docstring += "\n"
        template += "(?!\\s)(.*?)"
        match = re.match(template, docstring, re.DOTALL)
        if match:
            matches: tuple[str, ...] = match.groups()
            description = matches[place_holders["description"][0]] if place_holders["description"] else None
            epilog = matches[place_holders["epilog"][0]] if place_holders["epilog"] else None
            docstring_data = _DocstringData(description=description, epilog=epilog)
            for i in range(parameter_number):
                docstring_data.helps[
                    matches[place_holders["parameter_name"][0] + parameter_section_length * i]
                ] = _normalize_docstring(
                    matches[place_holders["parameter_description"][0] + parameter_section_length * i].strip()
                )
            return docstring_data
        return None

    def __make_argflagged(self, name: str) -> str:
        return f"{self.longstartflags}{name.replace("_","-")}"

    def __has_long_start_flag(self, flags: Sequence[str]) -> bool:
        return any([flag.startswith(f"{self.longstartflags}") for flag in flags])

    def __has_short_start_flag(self, flags: Sequence[str]) -> bool:
        return any([flag.startswith(self.prefix_chars) and flag[1] != self.prefix_chars for flag in flags])

    def __does_not_have_long_start_flag(self, flags: Sequence[str]) -> bool:
        return not self.__has_long_start_flag(flags)

    def __does_not_have_short_start_flag(self, flags: Sequence[str]) -> bool:
        return not self.__has_short_start_flag(flags)

    def _generate_args_for_add_argument(
        self, argdata: _ArgumentData
    ) -> tuple[tuple[str, ...], _CompleteKeywordArguments]:
        """Helper function to get data from the proxy object and creates (args, kwargs) to `add_argument()`
        Ref: https://docs.python.org/3/library/argparse.html#the-add-argument-method
        """
        # TODO: check variadic args and kwargs
        kwargs: _CompleteKeywordArguments = {
            "dest": argdata.name,
            "help": argdata.kwargs.get("help", argdata.help),
            "default": argdata.kwargs.get("default", argdata.default),
        }
        default_bool = kwargs["default"] if kwargs["default"] is not EMPTY else self.default_bool
        action, nargs, argtype, choices = "store", None, str, None
        kwargs["action"] = argdata.kwargs.get("action") or action
        if argdata.typeannotation is not None:
            action, nargs, argtype, choices = _get_data_from_typeannotation(
                argdata.typeannotation, default_bool, argdata.default, kwargs["action"]
            )
        kwargs["action"] = argdata.kwargs.get("action") or action
        if kwargs["action"] in ["store", "append", "extend"]:
            kwargs["type"] = argdata.kwargs.get("type") or argtype
            kwargs["nargs"] = argdata.kwargs.get("nargs") or nargs
            kwargs["choices"] = argdata.kwargs.get("choices") or choices
        argdata.make_flag = (
            all(
                [
                    argdata.make_flag is None,
                    self.__does_not_have_long_start_flag(argdata.flags),
                    argdata.default is not EMPTY,
                    # kwargs.get("nargs") not in ["*", "?"],
                ]
            )
            or kwargs["action"] in ["store_true", "store_false"]
            or argdata.make_flag
        )
        argflagged: str | None = None
        if (
            argdata.make_flag
            or all(
                [
                    argdata.make_flag is None,
                    argdata.flags,
                    self.__does_not_have_long_start_flag(argdata.flags),
                ]
            )
            or (kwargs["action"] in ["help", "version"] and len(argdata.flags) == 0)
        ):
            argflagged = self.__make_argflagged(argdata.name)
        if argflagged:
            argdata.flags.append(argflagged)
        if kwargs["default"] is EMPTY:
            kwargs["default"] = None
            if argdata.flags:
                if kwargs["action"] in ["help"]:
                    pass
                else:
                    kwargs["required"] = argdata.kwargs.get("required") or True
                    if kwargs["action"] in ["store_true", "store_false"]:
                        kwargs["action"] = BooleanOptionalAction

        if kwargs["action"] in ["version"] and "required" in kwargs:
            kwargs.pop("required")

        # given in `argdata.kwargs` has preference over inferred
        for key in ["metavar", "const", "version"]:
            try:
                kwargs[key] = argdata.kwargs.pop(key)  # type: ignore
            except KeyError:
                pass
        if (
            self.make_shorts
            and self.__has_long_start_flag(argdata.flags)
            and self.__does_not_have_short_start_flag(argdata.flags)
            or (kwargs["action"] in ["help"] and len(argdata.flags) == 0)
        ):
            argdata.flags = [self._make_short_option(argdata.name)] + argdata.flags

        if (
            kwargs["action"] not in ["store_true", "store_false", "help", "version"]
            and "metavar" not in kwargs
        ):
            if self.optmetavarmodifier is not None and len(argdata.flags) > 0:
                kwargs["metavar"] = self._set_arg_metavar(self.optmetavarmodifier, argdata)
            if self.posmetavarmodifier is not None and len(argdata.flags) == 0:
                kwargs["metavar"] = self._set_arg_metavar(self.posmetavarmodifier, argdata)

        if len(argdata.flags) > 0 and any([self.opthelpmodifier, argdata.helpmodifier]):
            helpmodifier = argdata.helpmodifier or self.opthelpmodifier
            assert helpmodifier is not None
            kwargs["help"] = helpmodifier(str(kwargs.get("help", "")))
        if len(argdata.flags) == 0 and any([self.poshelpmodifier, argdata.helpmodifier]):
            helpmodifier = argdata.helpmodifier or self.poshelpmodifier
            assert helpmodifier is not None
            kwargs["help"] = helpmodifier(str(kwargs.get("help", "")))

        return tuple(argdata.flags), kwargs

    def _make_short_option(self, name: str) -> str:
        past_options = (
            list(self.help_flags)
            + list(self.version_flags)
            + [option for argument in self.arguments for option in argument.option_strings]
        )
        for n in range(1, len(name) + 1):
            short_option = f"{self.prefix_chars}{name[:n]}"
            if short_option not in past_options:
                return short_option
            if short_option.upper() not in past_options:
                return short_option.upper()
            short_option = f"{self.prefix_chars}{''.join(p[:n] for p in name.split("_"))}"
            if short_option not in past_options:
                return short_option
        return short_option

    def _set_arg_metavar(
        self, modifier: str | Sequence[str] | Callable[[str], str], argdata: _ArgumentData
    ) -> str | tuple[str, ...] | None:
        if modifier is not None:
            if callable(modifier):
                return modifier(argdata.name)
            if isinstance(modifier, str):
                return modifier
            if isinstance(modifier, Sequence):
                return tuple(modifier)
        return modifier

    def _add_parsers(self) -> None:
        if self.parent is None:
            self.parser = ArgumentParser(
                prog=self.prog or self.name if self.func else None,
                usage=self.usage,
                description=self.description,
                epilog=self.epilog,
                parents=self.parents,
                formatter_class=self.formatter_class,
                prefix_chars=self.prefix_chars,
                fromfile_prefix_chars=self.fromfile_prefix_chars,
                argument_default=self.argument_default,
                conflict_handler=self.conflict_handler,
                add_help=self.add_help,
                allow_abbrev=self.allow_abbrev,
                exit_on_error=self.exit_on_error,
            )
        else:
            if self.parent.parser is None:
                self.parent._add_parsers()
                return
            assert self.parent.sub_commands_group and self.name
            self.parser = self.parent.sub_commands_group.add_parser(
                name=self.name,
                help=self.help,
                aliases=self.aliases,
                prog=self.prog,
                usage=self.usage,
                description=self.description,
                epilog=self.epilog,
                parents=self.parents,
                formatter_class=self.formatter_class,
                prefix_chars=self.prefix_chars,
                fromfile_prefix_chars=self.fromfile_prefix_chars,
                argument_default=self.argument_default,
                conflict_handler=self.conflict_handler,
                add_help=self.add_help,
                allow_abbrev=self.allow_abbrev,
                exit_on_error=self.exit_on_error,
            )
        self.arguments: list[Action] = []
        assert self.parser is not None
        if (self.help_flags or self.help_msg) and not self.add_help:
            self.help_msg = self.help_msg or "show this help message and exit"
            self.parser.add_argument(*self.help_flags, action="help", help=self.help_msg)
        if self.version and self.func is not None:
            if not isinstance(self.version, str):
                self.version = _get_pkg_version(self.func)
            self.version = self.versionmodifier(self.version) if self.versionmodifier else self.version
            self.parser.add_argument(*self.version_flags, action="version", version=self.version)
        for argdata in self.argument_data:
            argdata.make_flag = self._set_argumentdata_makeflag(argdata)
            if argdata.kind in [Kind.VAR_KEYWORD, Kind.VAR_POSITIONAL]:
                continue
            if _is_context_annotation(argdata.typeannotation):
                continue
            flags, kwargs = self._generate_args_for_add_argument(argdata)
            handler = self.parser
            if argdata.group is not None:
                group = argdata.group
                if isinstance(group, ArgumentGroup):
                    handler = self._add_argument_group_to_parser(arggroup=group)
                if isinstance(group, MutuallyExclusiveGroup):
                    if "required" in kwargs:
                        kwargs.pop("required")
                    if group.argument_group is not None:
                        handler = self._add_argument_group_to_parser(arggroup=group.argument_group)
                    if group not in self._mutually_exclusive_groups:
                        self._mutually_exclusive_groups.append(group)
                        group._argparse_mutually_exclusive_group = handler.add_mutually_exclusive_group(
                            required=group.required
                        )
                    handler = group._argparse_mutually_exclusive_group

            self.arguments.append(handler.add_argument(*flags, **kwargs))  # type: ignore

        if self.sub_commands and not self.sub_commands_group:
            # ref: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
            self.sub_commands_group = self.parser.add_subparsers(
                title=self.subcommands_title,
                description=self.subcommands_description,
                prog=self.subcommands_prog,  # I corrected this, see https://github.com/python/typeshed/issues/13162
                required=self.subcommands_required,
                help=self.subcommands_help,
                metavar=self.subcommands_metavar,
                dest=self.subparsers_dest,
            )

        for cmd in self.sub_commands:
            self.sub_commands[cmd]._add_parsers()

    def _set_argumentdata_makeflag(self, argdata: _ArgumentData) -> bool | None:
        if argdata.kind in [Kind.VAR_KEYWORD, Kind.KEYWORD_ONLY]:
            return True
        if argdata.make_flag is not None:
            return argdata.make_flag
        if self.make_flags is not None:
            return self.make_flags
        return None

    def _add_argument_group_to_parser(self, arggroup: ArgumentGroup) -> _ArgumentGroup:
        assert self.parser is not None
        if arggroup not in self._argument_groups:
            self._argument_groups.append(arggroup)
            arggroup._argparse_argument_group = self.parser.add_argument_group(
                title=arggroup.title,
                description=arggroup.description,
                argument_default=arggroup.argument_default,
                conflict_handler=arggroup.conflict_handler,
            )
        return arggroup._argparse_argument_group

    @property
    def is_main_command(self) -> bool:
        return self.parent is None


##############################################################################################################
# %%          PRIVATE CLASSES: Typed dict
##############################################################################################################


class _ArgumentMetaDataDictionary(TypedDict, total=False):
    """Dictionary with some parameters passed to the original `add_argument()` method.
    These are expected to be in the argument metadata annotation.
    Namely: `action`, `nargs`, `const`, `choices`, `required`, `help`, `metavar`, `version`.
    The parameter `version` is not documented, but is on some stub.
    The parameters `name_or_flags`, `default`, `type`, `dest` are not passed in this dictionary.
    Ref: https://docs.python.org/3/library/argparse.html#the-add-argument-method
    """

    action: (
        str
        | Literal[
            "store",
            "store_const",
            "store_true",
            "store_false",
            "append",
            "append_const",
            "count",
            "help",
            "version",
            "extend",
        ]
        | type[Action]
    )
    """The basic type of action to be taken when this argument is encountered at the command line.
    
        `ArgumentParser` objects associate command-line arguments with actions. These actions can do just about
        anything with the command-line arguments associated with them, though most actions simply add an attribute
        to the object returned by `parse_args()`. The `action` keyword argument specifies how the command-line
        arguments should be handled. The supplied actions are

        - `"store"`:
            This just stores the argument's value. This is the default action. For example::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo')
                >>> parser.parse_args('--foo 1'.split())
                Namespace(foo='1')

        - `"store_const"`:
            This stores the value specified by the const keyword argument; note that the const keyword argument
            defaults to `None`. The `store_const` action is most commonly used with optional arguments that
            specify some sort of flag. For example::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', action='store_const', const=42)
                >>> parser.parse_args(['--foo'])
                Namespace(foo=42)

        - `"store_true"` and `"store_false"`:
            These are special cases of `"store_const"` used for storing the
            values `True` and `False` respectively. In addition, they create default values of `False` and True
            respectively. For example::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', action='store_true')
                >>> parser.add_argument('--bar', action='store_false')
                >>> parser.add_argument('--baz', action='store_false')
                >>> parser.parse_args('--foo --bar'.split())
                Namespace(foo=True, bar=False, baz=True)

        - `"append"`:
            This stores a list, and appends each argument value to the list. It is useful to allow an option to
            be specified multiple times. If the default value is non-empty, the default elements will be present
            in the parsed value for the option, with any values from the command line appended after those default
            values. Example usage::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', action='append')
                >>> parser.parse_args('--foo 1 --foo 2'.split())
                Namespace(foo=['1', '2'])

        - `"append_const"`:
            This stores a list, and appends the value specified by the `const` keyword argument to the list;
            note that the `const` keyword argument defaults to `None`. The `"append_const"` action is typically
            useful when multiple arguments need to store constants to the same list. For example::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
                >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
                >>> parser.parse_args('--str --int'.split())
                Namespace(types=[<class 'str'>, <class 'int'>])

        - `"count"`:
            This counts the number of times a keyword argument occurs. For example, this is useful for
            increasing verbosity levels::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--verbose', '-v', action='count', default=0)
                >>> parser.parse_args(['-vvv'])
                Namespace(verbose=3)

            Note, the default will be `None` unless explicitly set to 0.

        - `"help"`:
            This prints a complete help message for all the options in the current parser and then exits. By
            default a help action is automatically added to the parser. See `ArgumentParser` for details of how
            the output is created.

            **Note**:
                This may be used to change the default help action, also passing `add_help=False` to the parser constructor.

        - `"version"`:
            This expects a `version=` keyword argument in the `add_argument()` call, and prints version
            information and exits when invoked::

                >>> import argparse
                >>> parser = argparse.ArgumentParser(prog='PROG')
                >>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
                >>> parser.parse_args(['--version'])
                PROG 2.0

        - `"extend"`:
            This stores a list, and extends each argument value to the list. Example usage::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument("--foo", action="extend", nargs="+", type=str)
                >>> parser.parse_args(["--foo", "f1", "--foo", "f2", "f3", "f4"])
                Namespace(foo=['f1', 'f2', 'f3', 'f4'])

            You may also specify an arbitrary action by passing an Action subclass or other object that implements
            the same interface. The `BooleanOptionalAction` is available in `argparse` and adds support for
            boolean actions such as `--foo` and `--no-foo`::

                >>> import argparse
                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', action=argparse.BooleanOptionalAction)
                >>> parser.parse_args(['--no-foo'])
                Namespace(foo=False)

            The recommended way to create a custom action is to extend Action, overriding the `__call__` method and
            optionally the `__init__` and `format_usage` methods. An example of a custom action::

                >>> class FooAction(argparse.Action):
                ...    def __init__(self, option_strings, dest, nargs=None, **kwargs):
                ...        if nargs is not None:
                ...            raise ValueError("nargs not allowed")
                ...        super().__init__(option_strings, dest, **kwargs)
                ...    def __call__(self, parser, namespace, values, option_string=None):
                ...        print('%r %r %r' % (namespace, values, option_string))
                ...        setattr(namespace, self.dest, values)
                ...
                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', action=FooAction)
                >>> parser.add_argument('bar', action=FooAction)
                >>> args = parser.parse_args('1 --foo 2'.split())
                Namespace(bar=None, foo=None) '1' None
                Namespace(bar='1', foo=None) '2' '--foo'
                >>> args
                Namespace(bar='1', foo='2')

            For more details, see `Action`.
    """

    nargs: int | str | None
    """The number of command-line arguments that should be consumed.

        `ArgumentParser` objects usually associate a single command-line argument with a single action to be taken.
        The `nargs` keyword argument associates a different number of command-line arguments with a single action.
        See also "Specifying ambiguous arguments". The supported values are:
        
        - `N` (an integer):
            `N` arguments from the command line will be gathered together into a list. For example::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', nargs=2)
                >>> parser.add_argument('bar', nargs=1)
                >>> parser.parse_args('c --foo a b'.split())
                Namespace(bar=['c'], foo=['a', 'b'])

            Note that `nargs=1` produces a list of one item. This is different from the default, in which the item
            is produced by itself.

        - `"?"`:
            One argument will be consumed from the command line if possible, and produced as a single item. If
            no command-line argument is present, the value from `default` will be produced. Note that for optional
            arguments, there is an additional case - the option string is present but not followed by a
            command-line argument. In this case the value from `const` will be produced. Some examples to
            illustrate this::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
                >>> parser.add_argument('bar', nargs='?', default='d')
                >>> parser.parse_args(['XX', '--foo', 'YY'])
                Namespace(bar='XX', foo='YY')
                >>> parser.parse_args(['XX', '--foo'])
                Namespace(bar='XX', foo='c')
                >>> parser.parse_args([])
                Namespace(bar='d', foo='d')

            One of the more common uses of `nargs="?"` is to allow optional input and output files::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
                >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
                >>> parser.parse_args(['input.txt', 'output.txt'])
                Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
                        outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
                >>> parser.parse_args([])
                Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
                        outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)

        - `"*"`:
            All command-line arguments present are gathered into a list. Note that it generally doesn't make
            much sense to have more than one positional argument with `nargs="*"`, but multiple optional arguments
            with `nargs="*"` is possible. For example::

                >>> parser = argparse.ArgumentParser()
                >>> parser.add_argument('--foo', nargs='*')
                >>> parser.add_argument('--bar', nargs='*')
                >>> parser.add_argument('baz', nargs='*')
                >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
                Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y']

        - `"+"`:
            Just like `"*"`, all command-line args present are gathered into a list. Additionally, an error
            message will be generated if there wasn't at least one command-line argument present. For example::

                >>> parser = argparse.ArgumentParser(prog='PROG')
                >>> parser.add_argument('foo', nargs='+')
                >>> parser.parse_args(['a', 'b'])
                Namespace(foo=['a', 'b'])
                >>> parser.parse_args([])
                usage: PROG [-h] foo [foo ...]
                PROG: error: the following arguments are required: foo
    """

    const: Any
    """A constant value required by some `action` and `nargs` selections.

        The const argument of `add_argument()` is used to hold constant values that are not read from the command
        line but are required for the various ArgumentParser actions. The two most common uses of it are:

        1. When `add_argument()` is called with `action='store_const'` or `action='append_const'`. These
           actions add the const value to one of the attributes of the object returned by `parse_args()`. See
           the action description for examples. If const is not provided to `add_argument()`, it will receive a
           default value of `None`.

        2. When `add_argument()` is called with option strings (like `-f` or `--foo`) and `nargs='?'`. This
           creates an optional argument that can be followed by zero or one command-line arguments. When
           parsing the command line, if the option string is encountered with no command-line argument
           following it, the value of const will be assumed to be `None` instead. See the `nargs` description
           for examples.

        Changed in Python version 3.11: `const=None` by default, including when `action='append_const'` or
        `action='store_const'`.    
    """

    choices: Iterable | None
    """A sequence of the allowable values for the argument.

        Some command-line arguments should be selected from a restricted set of values. These can be handled by
        passing a sequence object as the choices keyword argument to `add_argument()`. When the command line is
        parsed, argument values will be checked, and an error message will be displayed if the argument was not one
        of the acceptable values::

            >>> parser = argparse.ArgumentParser(prog='game.py')
            >>> parser.add_argument('move', choices=['rock', 'paper', 'scissors'])
            >>> parser.parse_args(['rock'])
            Namespace(move='rock')
            >>> parser.parse_args(['fire'])
            usage: game.py [-h] {rock,paper,scissors}
            game.py: error: argument move: invalid choice: 'fire' (choose from 'rock',
            'paper', 'scissors')

        Note that inclusion in the choices sequence is checked after any `type` conversions have been performed, so
        the type of the objects in the choices sequence should match the `type` specified::

            >>> parser = argparse.ArgumentParser(prog='doors.py')
            >>> parser.add_argument('door', type=int, choices=range(1, 4))
            >>> print(parser.parse_args(['3']))
            Namespace(door=3)
            >>> parser.parse_args(['4'])
            usage: doors.py [-h] {1,2,3}
            doors.py: error: argument door: invalid choice: 4 (choose from 1, 2, 3)

        Any sequence can be passed as the choices value, so `list` objects, `tuple` objects, and custom sequences
        are all supported.

        Use of `enum.Enum` is not recommended because it is difficult to control its appearance in usage, help, and
        error messages.

        Formatted choices override the default `metavar` which is normally derived from `dest`. This is usually what
        you want because the user never sees the dest parameter. If this display isn't desirable (perhaps because
        there are many choices), just specify an explicit `metavar`.
    """

    required: bool | None
    """Whether or not the command-line option may be omitted (optionals only).

        In general, the `argparse` module assumes that flags like `-f` and `--bar` indicate optional arguments,
        which can always be omitted at the command line. To make an option required, `True` can be specified for the
        `required=` keyword argument to `add_argument()`::

            >>> parser = argparse.ArgumentParser()
            >>> parser.add_argument('--foo', required=True)
            >>> parser.parse_args(['--foo', 'BAR'])
            Namespace(foo='BAR')
            >>> parser.parse_args([])
            usage: [-h] --foo FOO
            : error: the following arguments are required: --foo

        As the example shows, if an option is marked as `required`, `parse_args()` will report an error if that
        option is not present at the command line.

        > [!NOTE]
        > Required options are generally considered bad form because users expect options to be optional, and
        > thus they should be avoided when possible.
    """

    help: str | None
    """A brief description of what the argument does.

        The `help` value is a string containing a brief description of the argument. When a user requests help
        (usually by using `-h` or `--help` at the command line), these `help` descriptions will be displayed with
        each argument::

            >>> parser = argparse.ArgumentParser(prog='frobble')
            >>> parser.add_argument('--foo', action='store_true', help='foo the bars before frobbling')
            >>> parser.add_argument('bar', nargs='+', help='one of the bars to be frobbled')
            >>> parser.parse_args(['-h'])
            usage: frobble [-h] [--foo] bar [bar ...]

            positional arguments:
            bar     one of the bars to be frobbled

            options:
                -h, --help  show this help message and exit
                --foo   foo the bars before frobbling

        The help strings can include various format specifiers to avoid repetition of things like the program name
        or the argument `default`. The available specifiers include the program name, `%(prog)s` and most keyword
        arguments to `add_argument()`, e.g. `%(default)s`, `%(type)s`, etc.::

            >>> parser = argparse.ArgumentParser(prog='frobble')
            >>> parser.add_argument('bar', nargs='?', type=int, default=42,
            ...                 help='the bar to %(prog)s (default: %(default)s)')
            >>> parser.print_help()
            usage: frobble [-h] [bar]

            positional arguments:
            bar     the bar to frobble (default: 42)

            options:
                -h, --help  show this help message and exit

        As the help string supports %-formatting, if you want a literal % to appear in the help string, you must
        escape it as `%%`.

        `argparse` supports silencing the help entry for certain options, by setting the `help` value to
        `argparse.SUPPRESS`::

            >>> parser = argparse.ArgumentParser(prog='frobble')
            >>> parser.add_argument('--foo', help=argparse.SUPPRESS)
            >>> parser.print_help()
            usage: frobble [-h]

            options:
                -h, --help  show this help message and exit
    """

    metavar: str | tuple[str, ...] | None
    """A name for the argument in usage messages.

        When `ArgumentParser` generates help messages, it needs some way to refer to each expected argument. By
        default, ArgumentParser objects use the `dest` value as the "name" of each object. By default, for
        positional argument actions, the `dest` value is used directly, and for optional argument actions, the
        `dest` value is uppercased. So, a single positional argument with `dest='bar'` will be referred to as `bar`.
        A single optional argument `--foo` that should be followed by a single command-line argument will be
        referred to as `FOO`. An example::

            >>> parser = argparse.ArgumentParser()
            >>> parser.add_argument('--foo')
            >>> parser.add_argument('bar')
            >>> parser.parse_args('X --foo Y'.split())
            Namespace(bar='X', foo='Y')
            >>> parser.print_help()
            usage:  [-h] [--foo FOO] bar

            positional arguments:
            bar

            options:
                -h, --help  show this help message and exit
                --foo FOO

        An alternative name can be specified with `metavar`::

            >>> parser = argparse.ArgumentParser()
            >>> parser.add_argument('--foo', metavar='YYYY')
            >>> parser.add_argument('bar', metavar='XXXX')
            >>> parser.parse_args('X --foo Y'.split())
            Namespace(bar='X', foo='Y')
            >>> parser.print_help()
            usage:  [-h] [--foo YYYY] XXXX

            positional arguments:
            XXXX

            options:
                -h, --help  show this help message and exit
                --foo YYYY

        Note that `metavar` only changes the displayed name - the name of the attribute on the `parse_args()` object
        is still determined by the `dest` value.

        Different values of `nargs` may cause the metavar to be used multiple times. Providing a tuple to `metavar`
        specifies a different display for each of the arguments::

            >>> parser = argparse.ArgumentParser(prog='PROG')
            >>> parser.add_argument('-x', nargs=2)
            >>> parser.add_argument('--foo', nargs=2, metavar=('bar', 'baz'))
            >>> parser.print_help()
            usage: PROG [-h] [-x X X] [--foo bar baz]

            options:
                -h, --help     show this help message and exit
                -x X X
                --foo bar baz
    """

    version: str | None
    """Expected keyword argument in the `add_argument()` call when `action='version'`."""


class KeywordArguments(_ArgumentMetaDataDictionary, total=False):
    """Dictionary inheriting parameters passed to the original `add_argument()` method,
    including `default` and `type`. These are suppose to be passed to the `add_argument()` method, after
    including `dest` and `name_or_flags`.
    Ref: https://docs.python.org/3/library/argparse.html#the-add-argument-method
    """

    default: Any
    type: type | Callable[[str], Any] | None


class _CompleteKeywordArguments(KeywordArguments, total=False):
    """Dictionary with all parameters passed to the original `add_argument()` method,
    including `dest` . These are suppose to be passed to the `add_argument()` method after
    including `name_or_flags`, which is positional (not a keyword argument).
    Ref: https://docs.python.org/3/library/argparse.html#the-add-argument-method
    """

    dest: str


##############################################################################################################
# %%          PRIVATE CLASSES: data classes
##############################################################################################################


@dataclass
class _DocstringData:
    """A dataclass with data recovered from docstring"""

    description: str | None
    epilog: str | None
    helps: dict[str, str] = field(default_factory=dict)


@dataclass
class _ArgumentData:
    """A proxy dataclass to store info that came from `inspect.Parameter` objects
    Ref: https://docs.python.org/3/library/inspect.html#inspect.Parameter

    Parameters
    ----------
    - `name` (`str`): Name of the parameter.
    - `typeannotation` (`Callable[[str], Any] | str | FileType | None`, optional): Defaults to `None`.
        Typeannotation of type. When `Annotated`, is the "origin"
    - `kind` (`Kind`, optional): Defaults to `Kind.POSITIONAL_OR_KEYWORD`. See reference.
    - `default` (`Any`, optional): Defaults to `Parameter.empty`. See reference.
    - `flags` (`list[str]`, optional): Defaults to `field(default_factory=list)`. List of flags.
    - `kwargs` (`KeywordArguments`, optional): Defaults to `field(default_factory=KeywordArguments)`.
        Dictionary inheriting parameters passed to the original add_argument() method, including default
        and type. These are suppose to be passed to the add_argument() method, after including dest and
        name_or_flags. Ref: https://docs.python.org/3/library/argparse.html#the-add-argument-method
    - `make_flag` (`bool | None`, optional): Defaults to `None`. Whether to force make flags.
    - `group` (`ArgumentGroup | MutuallyExclusiveGroup | None`, optional): Defaults to `None`.
        Group which the argument belongs
    - `parser` (`Any`, optional): Defaults to `None`. Not used in `clig` (maybe in `dataparsers`?)
    - `help` (`str | None`, optional): Defaults to `None`. Help string
    - `help_modifier` (`Callable[[str], str] | None`, optional): Defaults to `None`. Argument help modifier.
    """

    name: str
    typeannotation: Callable[[str], Any] | str | FileType | None = None
    kind: Kind = Kind.POSITIONAL_OR_KEYWORD
    default: Any = Parameter.empty
    flags: list[str] = field(default_factory=list)
    kwargs: KeywordArguments = field(default_factory=KeywordArguments)
    make_flag: bool | None = None
    group: ArgumentGroup | MutuallyExclusiveGroup | None = None
    parser: Any = None
    help: str | None = None
    helpmodifier: Callable[[str], str] | None | None = None


##############################################################################################################
# %%          PUBLIC CLASSES: Command arguments
##############################################################################################################


class CommandArguments(TypedDict, total=False):

    # Arguments for `ArgumentParser` object, see: https://docs.python.org/3/library/argparse.html#argumentparser-objects

    prog: str | None
    """The name of the program (default: generated from the function name).   
    https://docs.python.org/3/library/argparse.html#prog
    """

    usage: str | None
    """The string describing the program usage (default: generated from arguments added to parser).   
    https://docs.python.org/3/library/argparse.html#usage
    """

    description: str | None
    """Text to display before the argument help (by default, collected from the docstring when possible).   
    https://docs.python.org/3/library/argparse.html#description
    """

    epilog: str | None
    """Text to display after the argument help (by default, collected from the docstring when possible).   
    https://docs.python.org/3/library/argparse.html#epilog
    """

    parents: Sequence[ArgumentParser]
    """A list of `ArgumentParser` objects whose arguments should also be included.   
    https://docs.python.org/3/library/argparse.html#parents
    """

    formatter_class: type[HelpFormatter]
    """A class for customizing the help output (by default, `argparse.RawTextHelpFormatter`).   
    https://docs.python.org/3/library/argparse.html#formatter-class
    """

    prefix_chars: str
    """The set of characters that prefix optional arguments (default: `"-"`).   
    https://docs.python.org/3/library/argparse.html#prefix-chars
    """

    fromfile_prefix_chars: str | None
    """The set of characters that prefix files from which additional arguments should be read (default: `None`).   
    https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars
    """

    argument_default: Any
    """ The global default value for arguments (default: `None`).   
    https://docs.python.org/3/library/argparse.html#argument-default
    """

    conflict_handler: str
    """The strategy for resolving conflicting optionals (usually unnecessary).   
    https://docs.python.org/3/library/argparse.html#conflict-handler
    """

    add_help: bool
    """Add a `-h/--help` option to the parser (default: `True`).   
    https://docs.python.org/3/library/argparse.html#add-help
    """

    allow_abbrev: bool
    """Allows long options to be abbreviated if the abbreviation is unambiguous (default: `True`).   
    https://docs.python.org/3/library/argparse.html#allow-abbrev
    """

    exit_on_error: bool
    """Determines whether or not ArgumentParser exits with error info when an error occurs. (default: `True`).   
    https://docs.python.org/3/library/argparse.html#exit-on-error
    """

    # Arguments for `add_subparsers()` method, see: https://docs.python.org/3/library/argparse.html#subcommands

    subcommands_title: str
    """Title for the sub-parser group in help output; by default `"subcommands"` if description is provided,
    otherwise uses title for positional arguments."""

    subcommands_description: str | None
    """Description for the sub-parser group in help output, by default `None`."""

    subcommands_prog: str | None
    """Usage information that will be displayed with subcommand help, by default the name of the program and
    any positional arguments before the subparser argument."""

    subcommands_required: bool
    """Whether or not a subcommand must be provided, by default `False` (added in 3.7).   
    https://docs.python.org/3/library/argparse.html#required
    """

    subcommands_help: str | None
    """Help for sub-parser group in help output, by default `None`.   
    https://docs.python.org/3/library/argparse.html#help
    """

    subcommands_metavar: str | None
    """String presenting available subcommands in help; by default it is `None` and presents subcommands
    in form `{cmd1, cmd2, ..}`.   
    https://docs.python.org/3/library/argparse.html#metavar
    """

    # Extra arguments of this library

    docstring_template: str | DocStr | None
    """The template used to parse parameter descriptions from the function's docstring.
    When `None`, clig auto-detects the format by trying all known templates in order
    (NumPy, Sphinx, Google, clig-style). Set this explicitly to skip auto-detection and
    enforce a specific format. Use a `DocStr` enum member or any of the
    `NUMPY_DOCSTRING`, `SPHINX_DOCSTRING`, `GOOGLE_DOCSTRING`, `CLIG_DOCSTRING`
    module-level constants (and their variants).
    """

    default_bool: bool
    """The default value assumed for `bool`-annotated parameters when deciding the
    argparse action. When `False` (the default), a `bool` parameter with no default
    generates a `store_true` action (flag absent → `False`, flag present → `True`).
    When `True`, the action becomes `store_false` (flag absent → `True`, flag present →
    `False`). This setting is overridden per-argument when the parameter already has an
    explicit default value.
    """

    make_flags: bool | None
    """Whether to turn all positional-like parameters into optional flags (i.e. add a
    `--name` prefix). When `None` (the default), clig decides per-argument: parameters
    that have a default value are automatically promoted to flags; those without remain
    positional. Set to `True` to force every argument to be a flag, or `False` to keep
    every argument positional regardless of defaults. Per-argument `make_flag` metadata
    takes precedence over this setting.
    """

    make_shorts: bool | None
    """Whether to automatically generate a short flag (e.g. `-n`) alongside every long
    flag (e.g. `--name`). When `None` (the default) or `False`, only the long flag is
    used. When `True`, clig derives the shortest non-conflicting single-character option
    from the argument name and prepends it to the flag list. Short flags are also added
    to the help (`-h`) and version (`-v`) options when this is enabled.
    """

    metavarmodifier: str | Sequence[str] | Callable[[str], str] | None
    """A modifier applied to the displayed metavar of *all* arguments (both positional
    and optional) in the help output. A plain `str` replaces the metavar with that
    string; a `Sequence[str]` is used as a fixed tuple of metavar tokens (for multi-value
    arguments); a callable receives the argument name and must return the desired
    metavar string. `None` leaves the metavar at its argparse default. Acts as a
    fallback for both `posmetavarmodifier` and `optmetavarmodifier` when those are
    `None`.
    """

    posmetavarmodifier: str | Sequence[str] | Callable[[str], str] | None
    """A modifier applied to the metavar of *positional* arguments only. Follows the
    same rules as `metavarmodifier` (str, sequence, or callable). When set, takes
    precedence over `metavarmodifier` for positional arguments; when `None`, falls back
    to `metavarmodifier`.
    """

    optmetavarmodifier: str | Sequence[str] | Callable[[str], str] | None
    """A modifier applied to the metavar of *optional* (flagged) arguments only. Follows
    the same rules as `metavarmodifier` (str, sequence, or callable). When set, takes
    precedence over `metavarmodifier` for optional arguments; when `None`, falls back to
    `metavarmodifier`.
    """

    helpmodifier: Callable[[str], str] | None
    """A callable applied to the help string of *all* arguments before it is passed to
    argparse. Receives the current help string (may be an empty string if no help was
    found) and must return the final string to display. Useful for appending default
    values, wrapping text, or adding ANSI colours uniformly. Acts as a fallback for both
    `poshelpmodifier` and `opthelpmodifier` when those are `None`.
    """

    poshelpmodifier: Callable[[str], str] | None
    """A callable applied to the help string of *positional* arguments only. Follows the
    same contract as `helpmodifier`. When set, takes precedence over `helpmodifier` for
    positional arguments; when `None`, falls back to `helpmodifier`.
    """

    opthelpmodifier: Callable[[str], str] | None
    """A callable applied to the help string of *optional* (flagged) arguments only.
    Follows the same contract as `helpmodifier`. When set, takes precedence over
    `helpmodifier` for optional arguments; when `None`, falls back to `helpmodifier`.
    """

    help_flags: Sequence[str]
    """The flag strings that trigger the help action (default: `("-h", "--help")`).
    When this is non-empty *or* `help_msg` is set, the built-in argparse help is
    disabled (`add_help=False`) and a custom help argument is registered instead using
    these flags and `help_msg`. Pass an empty sequence together with `help_msg` to keep
    the default `-h`/`--help` flags while customising only the message.
    """

    help_msg: str | None
    """The help text shown for the help option itself (the line that describes `-h,
    --help` in the usage output). Defaults to `"show this help message and exit"` when
    `help_flags` is provided or this field is set. Setting either `help_flags` or
    `help_msg` disables the standard argparse help mechanism so that the custom flags and
    message are used instead.
    """

    version: bool | str
    """Whether to add version information to the command. Defaults to `False`.
    If `True`, tries to find the version from the function's package.
    If it is a string, use the string as the version information."""

    versionmodifier: Callable[[str], str] | None
    """A callable applied to the version string before it is passed to argparse's
    `version` action. Receives the resolved version string (whether auto-detected from
    the package metadata or supplied directly via `version`) and must return the final
    string to display when `--version` is invoked. Useful for adding a program name
    prefix, ANSI colours, or extra build metadata (e.g. `lambda v: f"my_tool {v}"`).
    `None` leaves the version string unchanged. Has no effect when `version` is `False`.
    """


class CompleteCommandArguments(CommandArguments, total=False):

    # Arguments for `add_parser()` method, see: https://docs.python.org/3/library/argparse.html#subcommands

    name: str | None
    """Name of the subcommand, taken by the `add_parser()` method."""

    help: str | None
    """A help message for the subparser command."""


##############################################################################################################
# %%          PUBLIC CLASSES: API uses
##############################################################################################################


@dataclass
class Context[T]:
    namespace: T
    command: Command


@dataclass
class ArgumentGroup:
    """Ref: https://docs.python.org/3/library/argparse.html#argument-groups"""

    title: str | None = None
    description: str | None = None
    _: KW_ONLY
    argument_default: Any = None
    conflict_handler: str = "error"

    def __post_init__(self):
        self._argparse_argument_group: _ArgumentGroup


@dataclass
class MutuallyExclusiveGroup:
    """Ref: https://docs.python.org/3/library/argparse.html#mutual-exclusion"""

    required: bool = False
    _: KW_ONLY
    argument_group: ArgumentGroup | None = None
    title: str | None = None
    description: str | None = None
    argument_default: Any = None
    conflict_handler: str | None = None

    def __post_init__(self):
        self._argparse_mutually_exclusive_group: _MutuallyExclusiveGroup
        self.__any_argument_group_parameter = any(
            [
                par is not None
                for par in [
                    self.title,
                    self.description,
                    self.argument_default,
                    self.conflict_handler,
                ]
            ]
        )
        if self.argument_group is not None and self.__any_argument_group_parameter:
            raise ValueError("Parameters `argument_group` not allowed with `title`, `description`, etc...")
        if self.__any_argument_group_parameter:
            self.argument_group = ArgumentGroup(
                title=self.title,
                description=self.description,
                argument_default=self.argument_default,
                conflict_handler=self.conflict_handler or "error",
            )


@dataclass
class ArgumentMetaData:
    flags: list[str] = field(default_factory=list)
    make_flag: bool | None = None
    group: ArgumentGroup | MutuallyExclusiveGroup | None = None
    helpmodifier: Callable[[str], str] | None | None = None
    dictionary: KeywordArguments = field(default_factory=KeywordArguments)


##############################################################################################################
# %%          PRIVATE FUNCTIONS
##############################################################################################################


@overload
def _get_pkg_version(func: Callable[..., Any]) -> str: ...


@overload
def _get_pkg_version(func: Callable[..., Any], return_pkg_name: bool = False) -> tuple[str, str, bool]: ...


def _get_pkg_version(func: Callable[..., Any], return_pkg_name: bool = False) -> str | tuple[str, str, bool]:
    """`return_pkg_name` is used of testing"""
    pkg_version: str = "0.0.0"
    check_distributions: bool = True

    module_name = func.__module__
    module_obj = sys.modules[module_name]

    if hasattr(module_obj, "__version__") and not return_pkg_name:
        pkg_version = module_obj.__version__
        check_distributions = False

    pkg_name = module_obj.__package__
    if pkg_name and check_distributions:
        try:
            pkg_version = pkg_metadata_version(pkg_name)
            check_distributions = False
        except PackageNotFoundError:
            pass

    if check_distributions:
        module_name = module_name.split(".")[0]
        for dist in pkg_distributions():
            if any(file.parts[0] == module_name for file in (dist.files or [])):
                pkg_name, pkg_version = dist.name, dist.version
                break

    if return_pkg_name and pkg_name is not None:
        return pkg_name, pkg_version, check_distributions

    return pkg_version


def _is_context_annotation(annotation: Any) -> bool:
    if isinstance(annotation, type):
        return issubclass(annotation, Context)
    annotation = get_origin(annotation)
    if isinstance(annotation, type):
        return issubclass(annotation, Context)
    return False


def _getattr_with_spaces(namespace: Namespace, name: str) -> Any:
    """Like `getattr` but try to get attributes with spaces appended to the names"""
    # Try exact match first
    if hasattr(namespace, name):
        return getattr(namespace, name)

    # Otherwise, keep appending spaces until found
    padded = name
    while True:
        padded += " "
        if hasattr(namespace, padded):
            return getattr(namespace, padded)


def _normalize_docstring(docstring: str | None) -> str:
    """https://peps.python.org/pep-0257/#handling-docstring-indentation

    This functions maybe do the same as `inspect.cleandoc`.
    However, this one accepts `None`.
    """
    if not docstring:
        return ""
    lines: list[str] = docstring.expandtabs(tabsize=4).splitlines()
    indentation: int = min([len(line) - len(line.lstrip()) for line in lines[1:] if line.lstrip()], default=0)
    lines: list[str] = [lines[0].strip()] + [
        line.removeprefix(" " * indentation).rstrip() for line in lines[1:]
    ]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


def _get_argument_data_from_parameter(parameter: Parameter) -> _ArgumentData:
    """Helper function to get data from a `inspect.Parameter` object and generetes a proxy object
    Ref: https://docs.python.org/3/library/inspect.html#inspect.Parameter
    """
    argdata: _ArgumentData = _ArgumentData(name=parameter.name, kind=parameter.kind)
    argdata.default = parameter.default
    if parameter.annotation is not EMPTY:
        annotation = parameter.annotation
        if type(annotation) == str:
            annotation = eval(annotation)
        argdata.typeannotation = annotation
        if hasattr(annotation, "__metadata__"):
            argdata.typeannotation = annotation.__origin__
            metadatas = annotation.__metadata__
            for metadata in metadatas:
                if isinstance(metadata, ArgumentMetaData):
                    argdata.flags = metadata.flags.copy()
                    argdata.make_flag = metadata.make_flag
                    argdata.group = metadata.group
                    argdata.helpmodifier = metadata.helpmodifier
                    argdata.kwargs = metadata.dictionary.copy()
                    break
    if parameter.annotation is EMPTY and parameter.default is not EMPTY:
        argdata.typeannotation = type(parameter.default)
    return argdata


def _get_data_from_typeannotation(
    annotation: Any,
    default_bool: bool = False,
    default: Any = None,
    action: str | type[Action] = "store",
) -> tuple[str | type[Action], str | int | None, type | Callable[[str], Any] | None, Sequence[Any] | None]:
    """Return `action`, `nargs`, `argtype`, `choices`"""
    nargs = None
    argtype = annotation if callable(annotation) else str
    choices = None
    origin = get_origin(annotation)
    if origin:
        types = get_args(annotation)
        if origin in [Union, UnionType]:
            types = [t for t in get_args(annotation) if t is not type(None)]
            argtype = __create_union_converter(types)
            inner_origin = get_origin(types[0])
            if inner_origin is tuple:
                inner_types = get_args(types[0])
                nargs = len(inner_types) if Ellipsis not in inner_types else "*"
                nargs = "+" if (nargs == "*" and default is EMPTY) else nargs
            if inner_origin in [list, Sequence]:
                argtype = get_args(types[0])[0]
                nargs = "*"
                nargs = "+" if (nargs == "*" and default is EMPTY) else nargs
        elif origin is tuple:
            nargs = len(types) if Ellipsis not in types else "*"
            argtype = types[0]
            nargs = "+" if (nargs == "*" and default is EMPTY) else nargs
        elif origin in [list, Sequence]:
            nargs = "*" if action != "append" else None
            argtype = types[0]
            nargs = "+" if (nargs == "*" and default is EMPTY) else nargs
        elif origin is Literal:
            choices = [t.name if isinstance(t, Enum) else t for t in types]
            argtype = None  # create_literal_converter(types)
    if annotation == bool:
        action = "store_false" if default_bool else "store_true"
        argtype = None
    if isinstance(argtype, type) and issubclass(argtype, Enum):
        choices = list(getattr(argtype, "__members__").keys())
        argtype = None

    return action, nargs, argtype, choices


def __create_union_converter(types):

    try:
        if len(types) == 1 and issubclass(types[0], Enum):
            return types[0]
    except TypeError:
        if len(types) == 1 and isinstance(types[0], type):
            return types[0]

    def converter(value: str) -> Any:
        for t in types:
            try:
                if isinstance(t, type) and issubclass(t, Enum):
                    return t[value]
                # Attempt conversion
                while get_origin(t) is not None:
                    t = get_args(t)[0]
                converted_value = t(value)
                # Check string representation matches
                return converted_value
                # if str(converted_value) == value:
            except (ValueError, TypeError):
                continue  # Ignore and try the next type
        raise ValueError("ERROR in conversion")

    return converter


def __raise_caret_error(message: str):
    """Raise a caret-style RuntimeError pointing to the caller line."""
    # Get caller frame info
    stack = inspect.stack()
    frame = stack[2] if len(stack) > 2 else stack[1]
    filename = frame.filename
    lineno = frame.lineno
    assert frame.code_context is not None
    line = frame.code_context[0].rstrip("\n")
    col_start = frame.index or 0  # approximate, might be None

    # Create caret underline
    caret_line = " " * col_start + "^" * len(line.strip())

    # Format and print error with caret and message
    sys.stderr.write(f'  File "{filename}", line {lineno}\n')
    sys.stderr.write(f"    {line}\n")
    sys.stderr.write(f"    {caret_line}\n")
    sys.stderr.write(f"{type(RuntimeError()).__name__}: {message}\n")
    sys.exit(1)


##############################################################################################################
# %%          UNUSED FUNCTIONS
##############################################################################################################


def __create_literal_converter(types):
    def converter(s):
        for value in types:
            if isinstance(value, Enum) and s == getattr(value, "name"):
                return getattr(value, "name")
            if str(value) == s:
                return value
        raise ValueError("ERRO")

    return converter


def __count_leading_spaces(string: str):
    return len(string) - len(string.lstrip())


def __arg(
    *flags: str,
    make_flag: bool | None = None,
    group: ArgumentGroup | MutuallyExclusiveGroup | None = None,
    subparser: Field[Any] | None = None,
    **kwargs: Unpack[KeywordArguments],
) -> Any:
    """"""
    return field(
        default=kwargs.pop("default", None),
        metadata={
            "obj": ArgumentMetaData(
                flags=list(flags),
                make_flag=make_flag,
                group=group,
                dictionary=kwargs,
            ),
            "subparser": subparser,
        },
    )


def __get_metadata_from_field(field: Field[Any]) -> _ArgumentData:
    if type(field.type) == str:
        field.type = eval(field.type)
    data: _ArgumentData = _ArgumentData(name=field.name, typeannotation=field.type)
    if field.default is not field.default_factory:
        data.default = field.default
    if field.metadata:
        data.parser = field.metadata.get("subparser", None)
        metadata: ArgumentMetaData = field.metadata.get("obj", None)
        data.flags = metadata.flags
        data.make_flag = metadata.make_flag
        data.group = metadata.group
        data.kwargs = metadata.dictionary
    return data


##############################################################################################################
# %%          PUBLIC FUNCTIONS
##############################################################################################################

_main_command: Command | None = None


def command(func: Callable | None = None, *args, **kwargs: Unpack[CompleteCommandArguments]):
    global _main_command
    if _main_command is not None:
        __raise_caret_error(
            "The main command is already defined. Please use `clig.command()` function only once"
        )

    def wrap(func: Callable):
        global _main_command
        _main_command = Command(func, *args, **kwargs)
        return func

    # See if we're being called as @subcommand or @subcommand().
    if func is None:
        # We're called with parens.
        return wrap

    # We're called as @subcommand without parens.
    return wrap(func)


def subcommand(
    func: Callable | None = None,
    parent: Command | Callable | str | None = None,
    *args,
    **kwargs: Unpack[CompleteCommandArguments],
):
    if _main_command is None:
        __raise_caret_error(
            "The main command is not defined. Please use `clig.subcommand()` function only after `clig.command()`"
        )
        raise

    if parent is None:
        parent = _main_command

    if inspect.isfunction(parent):
        parent = __get_command_in_command_chain_by_name(
            _main_command, __get_subcommand_name(_main_command, parent)
        )

    if isinstance(parent, str):
        parent = __get_command_in_command_chain_by_name(_main_command, parent)

    assert isinstance(parent, Command), "\n\n\nThe `parent` argument must be a `Command`\n\n"

    def wrap(func: Callable):
        parent.add_subcommand(func, *args, **kwargs)
        return func

    # See if we're being called as @subcommand or @subcommand().
    if func is None:
        # We're called with parens.
        return wrap

    # We're called as @subcommand without parens.
    return wrap(func)


def __get_subcommand_name(cmd: Command, func: Callable) -> str | None:
    subcmds = cmd.sub_commands
    for name in subcmds:
        if subcmds[name].func == func:
            return name
    for name in subcmds:
        res = __get_subcommand_name(subcmds[name], func)
        if res:
            return res


def __get_command_in_command_chain_by_name(cmd: Command, name: str | None) -> Command | None:
    if name is None:
        return name
    subcmds = cmd.sub_commands
    res = subcmds.get(name)
    if res is None:
        for n in subcmds:
            res = __get_command_in_command_chain_by_name(subcmds[n], name)
            if res:
                return res
    return res


def data(
    *flags: str,
    make_flag: bool | None = None,
    group: ArgumentGroup | MutuallyExclusiveGroup | None = None,
    helpmodifier: Callable[[str], str] | None | None = None,
    **kwargs: Unpack[KeywordArguments],
) -> ArgumentMetaData:
    return ArgumentMetaData(
        flags=list(flags),
        make_flag=make_flag,
        group=group,
        helpmodifier=helpmodifier,
        dictionary=kwargs,
    )


def run(
    func: Callable[..., Any] | None = None,
    args: Sequence[str] | None = None,
    **kwargs: Unpack[CompleteCommandArguments],
) -> Any:
    if func is None:
        if _main_command is not None:
            return _main_command.run(args)
        __raise_caret_error("The main command is not defined. Please pass a function to `clig.run()`")
    return Command(func, **kwargs).run(args)
