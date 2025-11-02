##############################################################################################################
# %%                              IMPORTS
##############################################################################################################

from __future__ import annotations

import inspect
import re
import sys
from argparse import ArgumentParser, FileType, HelpFormatter, Action, BooleanOptionalAction
from argparse import HelpFormatter, RawTextHelpFormatter, _SubParsersAction  # [_ArgumentParserT]
from dataclasses import KW_ONLY, Field, dataclass, field
from inspect import Parameter
from inspect import _ParameterKind
from types import MappingProxyType, UnionType
from collections import OrderedDict
from collections.abc import Sequence
from typing import get_args, get_origin, Union, Annotated
from typing import Any, Callable, Iterable, Literal, Mapping, Self, TypedDict, Unpack, overload
from enum import Enum, StrEnum

Kind = _ParameterKind
Arg = Annotated

EMPTY = Parameter.empty

##############################################################################################################
# %%                              DOCSTRINGS TEMPLATES
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

# TODO: add 'no type' variants

DOCSTRING_TEMPLATES = [
    DESCRIPTION_DOCSTRING,
    DESCRIPTION_EPILOG_DOCSTRING,
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
    GOOGLE_DOCSTRING_NOTYPES = GOOGLE_DOCSTRING_NOTYPES


##############################################################################################################
# %%                              MAIN CLASS
##############################################################################################################


@dataclass
class Command:
    func: Callable[..., Any] | None = None
    # Arguments for `ArgumentParser` object, see: https://docs.python.org/3/library/argparse.html#argumentparser-objects
    prog: str | None = None
    usage: str | None = None
    description: str | None = None
    epilog: str | None = None
    parents: Sequence[ArgumentParser] = field(default_factory=list)
    formatter_class: type[HelpFormatter] = RawTextHelpFormatter
    prefix_chars: str = "-"
    fromfile_prefix_chars: str | None = None
    argument_default: Any = None
    conflict_handler: str = "error"
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True
    # Arguments for Sub-commands, see: https://docs.python.org/3/library/argparse.html#sub-commands
    _: KW_ONLY
    subcommands_title: str = "subcommands"
    subcommands_description: str | None = None
    subcommands_prog: str | None = None
    subcommands_required: bool = False
    subcommands_help: str | None = None
    subcommands_metavar: str | None = None
    # Extra arguments of this library
    docstring_template: str | DocStr | None = None
    default_bool: bool = False
    name: str | None = None
    help: str | None = None
    aliases: Sequence[str] = field(init=False, default_factory=list)
    parent: Command | None = field(init=False, default=None)
    parser: ArgumentParser | None = field(init=False, default=None)
    # TODO: `make_flags` option general
    # TODO: `make_shorts` option
    # TODO: `make_longs` option
    # TODO: set `func` before init

    def __post_init__(self):

        self.parameters: Mapping[str, Parameter] = {}
        """A dict with `name: Parameter`, where `Parameter` comes from stdlib `inspect`
        ref: https://docs.python.org/3/library/inspect.html#inspect.Parameter"""

        if self.func:
            self.name = self.name or self.func.__name__
            self.parameters = inspect.signature(self.func).parameters

        self.docstring_data: DocstringData | None = self.get_inferred_docstring_data()
        self.argument_data: list[ArgumentData] = self.get_argument_data()
        if self.docstring_data:
            self.description = self.description or self.docstring_data.description
            self.epilog = self.description or self.docstring_data.epilog

        self.sub_commands: OrderedDict[str, Command] = OrderedDict()
        self.sub_commands_group: _SubParsersAction | None = None
        self.longstartflags: str = f"{self.prefix_chars}" * 2

    ##########################################################################################################
    # %:                              PUBLIC METHODS
    ##########################################################################################################

    @overload
    def subcommand[**P, T](self, func: Callable[P, T]) -> Callable[P, T]: ...

    @overload
    def subcommand[**P, T](self, **kwargs) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

    def subcommand[**P, T](
        self,
        func: Callable[P, T] | None = None,
        **kwargs,
    ) -> Callable[P, T] | Callable[[Callable[P, T]], Callable[P, T]]:  # fmt: skip
        """Use for decorator"""
        if func is not None:
            self.new_subcommand(func)
            return func

        def wrap(func):
            self.new_subcommand(func, **kwargs)
            return func

        return wrap

    def add_subcommand(self, func: Callable[..., Any], *args, **kwargs) -> Self:
        """Used for multiple additions in line"""
        self.new_subcommand(func, *args, **kwargs)
        return self

    def new_subcommand(
        self,
        func: Callable[..., Any],
        name: str | None = None,
        help: str | None = None,
        aliases: Sequence[str] | None = None,
        *args,
        **kwargs,
    ) -> Command:
        """Internal method"""
        # TODO: add `deprecated` included in v3.13
        count = 1
        parent_parser = self.parent
        while parent_parser:
            count += 1
            parent_parser = parent_parser.parent
        self.subparsers_dest = f"{SUBPARSERS_DEST}{count}"
        cmd: Command = Command(func, *args, **kwargs)
        cmd.name = name or func.__name__
        cmd.aliases = aliases or []
        cmd.help = help
        cmd.parent = self
        self.sub_commands.update({cmd.name: cmd})
        return cmd

    def run(self, args: Sequence[str] | None = None) -> Any:
        # TODO: `Context` object
        # TODO: treat variatic argument as parse_know
        # TODO: treat "positional only"?
        if args == None:
            args = sys.argv[1:]
        if self.parser is None:
            self.add_parsers()
        assert self.parser is not None
        namespace = self.parser.parse_args(args)
        # TODO Enum decoverter
        for arg in self.argument_data:
            if isinstance(arg.typeannotation, type) and issubclass(arg.typeannotation, Enum):
                current = getattr(namespace, arg.name)
                setattr(namespace, arg.name, arg.typeannotation.__members__.get(current, current))
        if hasattr(self, "subparsers_dest"):
            subcommand_name = getattr(namespace, self.subparsers_dest)
            if subcommand_name is not None:
                args = " ".join(args).split(subcommand_name)
                namespace = self.parser.parse_args(args[0].split())
            delattr(namespace, self.subparsers_dest)
            if self.func:
                result = self.func(**vars(namespace))
            if subcommand_name is not None:
                return self.sub_commands[subcommand_name].run(args[1].split())
            return result
        else:
            if self.func:
                return self.func(**vars(namespace))

    ##########################################################################################################
    # %:                              PRIVATE METHODS
    ##########################################################################################################

    def get_argument_data(self) -> list[ArgumentData]:
        argument_data: list[ArgumentData] = []
        for par in self.parameters:
            data: ArgumentData = get_argdata_from_parameter(self.parameters[par])
            data.help = self.docstring_data.helps.get(data.name, None) if self.docstring_data else None
            argument_data.append(data)
        return argument_data

    def get_inferred_docstring_data(self) -> DocstringData | None:
        if self.docstring_template:
            return self.get_docstring_data(self.docstring_template)
        for template in DOCSTRING_TEMPLATES:
            data: DocstringData | None = self.get_docstring_data(template)
            if data:
                return data
        return None

    def get_docstring_data(self, template: str | None = None) -> DocstringData | None:
        separator: str = "################################" * 30
        template = template or self.docstring_template
        parameter_number = len(self.parameters)
        docstring = normalize_docstring(self.func.__doc__)
        # escape for regex match, but not "{" and "}"
        template = re.escape(normalize_docstring(template) + "\n").replace(r"\{", "{").replace(r"\}", "}")
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
            docstring_data = DocstringData(description=description, epilog=epilog)
            for i in range(parameter_number):
                docstring_data.helps[
                    matches[place_holders["parameter_name"][0] + parameter_section_length * i]
                ] = normalize_docstring(
                    matches[place_holders["parameter_description"][0] + parameter_section_length * i].strip()
                )
            return docstring_data
        return None

    def make_argflagged(self, name: str) -> str:
        return f"{self.longstartflags}{name.replace("_","-")}"

    def doesnothavelongstartflag(self, flags: Sequence[str]) -> bool:
        return not any([flag.startswith(f"{self.longstartflags}") for flag in flags])

    def inferarg(self, argdata: ArgumentData) -> tuple[tuple[str, ...], CompleteKeywordArguments]:
        # TODO: check variadic args and kwargs
        kwargs: CompleteKeywordArguments = {"dest": argdata.name}
        kwargs["help"] = argdata.kwargs.get("help", argdata.help)
        kwargs["default"] = argdata.kwargs.get("default", argdata.default)
        default_bool = kwargs["default"] if kwargs["default"] is not EMPTY else self.default_bool
        action, nargs, argtype, choices = "store", None, str, None
        if argdata.typeannotation is not None:
            action, nargs, argtype, choices = get_data_from_typeannotation(
                argdata.typeannotation, default_bool
            )
        kwargs["action"] = argdata.kwargs.get("action") or action
        if kwargs["action"] in ["store", "append"]:
            kwargs["type"] = argdata.kwargs.get("type") or argtype
            kwargs["nargs"] = argdata.kwargs.get("nargs") or nargs
            kwargs["choices"] = argdata.kwargs.get("choices") or choices
        argdata.make_flag = (
            all(
                [
                    argdata.make_flag is None,
                    self.doesnothavelongstartflag(argdata.flags),
                    kwargs["default"] is not EMPTY,
                    kwargs.get("nargs") not in ["*", "?"],
                ]
            )
            or kwargs["action"] in ["store_true", "store_false"]
            or argdata.make_flag
        )
        argflagged: str | None = None
        if argdata.make_flag or all(
            [
                argdata.make_flag is None,
                argdata.flags,
                self.doesnothavelongstartflag(argdata.flags),
            ]
        ):
            argflagged = self.make_argflagged(argdata.name)
        if argflagged:
            argdata.flags.append(argflagged)
        if kwargs["default"] is EMPTY:
            kwargs["default"] = None
            if argdata.flags:
                kwargs["required"] = argdata.kwargs.get("required") or True
                if kwargs["action"] in ["store_true", "store_false"]:
                    kwargs["action"] = BooleanOptionalAction

        # given in `argdata.kwargs` has preference over inferred
        for key in ["metavar", "const", "version"]:
            try:
                kwargs[key] = argdata.kwargs.pop(key)  # type: ignore
            except KeyError:
                pass
        return tuple(argdata.flags), kwargs

    def add_parsers(self) -> None:
        if self.parent is None:
            self.parser = ArgumentParser(
                prog=self.prog or self.func.__name__ if self.func else None,
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
        for argument_data in self.argument_data:
            flags, kwargs = self.inferarg(argument_data)
            self.arguments.append(self.parser.add_argument(*flags, **kwargs))  # type:ignore

        assert self.parser is not None
        if self.sub_commands and not self.sub_commands_group:
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
            self.sub_commands[cmd].add_parsers()

    @property
    def is_main_command(self) -> bool:
        return self.parent is None

    # endregion


##############################################################################################################
# %%                              AUX CLASSES
##############################################################################################################


class ArgumentMetaDataDictionary(TypedDict, total=False):
    action: str | Literal[ "store", "store_const", "store_true", "store_false", "append", "append_const", "count", "help", "version", "extend", ] | type[Action]  # fmt: skip
    nargs: int | str | None
    const: Any
    choices: Iterable | None
    required: bool | None
    help: str | None
    metavar: str | tuple[str, ...] | None
    version: str | None


class KeywordArguments(ArgumentMetaDataDictionary, total=False):
    default: Any
    type: type | Callable[[str], Any] | None


class CompleteKeywordArguments(KeywordArguments, total=False):
    dest: str


@dataclass
class ArgumentGroup:
    title: str | None = None


@dataclass
class MutuallyExclusiveGroup:
    required: bool = False


@dataclass
class ArgumentMetaData:
    flags: list[str] = field(default_factory=list)
    make_flag: bool | None = None
    argument_group: ArgumentGroup | None = None
    mutually_exclusive_group: MutuallyExclusiveGroup | None = None
    dictionary: KeywordArguments = field(default_factory=KeywordArguments)


@dataclass
class ArgumentData:
    name: str
    typeannotation: Callable[[str], Any] | str | FileType | None = None
    kind: Kind = Kind.POSITIONAL_OR_KEYWORD
    default: Any = Parameter.empty
    flags: list[str] = field(default_factory=list)
    kwargs: KeywordArguments = field(default_factory=KeywordArguments)
    make_flag: bool | None = None
    argument_group: ArgumentGroup | None = None
    mutually_exclusive_group: MutuallyExclusiveGroup | None = None
    parser: Any = None
    help: str | None = None


@dataclass
class DocstringData:
    description: str | None
    epilog: str | None
    helps: dict[str, str] = field(default_factory=dict)


##############################################################################################################
# %%                              FUNCTIONS
##############################################################################################################


def count_leading_spaces(string: str):
    return len(string) - len(string.lstrip())


def normalize_docstring(docstring: str | None) -> str:
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


def data(
    *flags: str,
    make_flag: bool | None = None,
    group: ArgumentGroup | None = None,
    mutually_exclusive_group: MutuallyExclusiveGroup | None = None,
    **kwargs: Unpack[KeywordArguments],
) -> ArgumentMetaData:
    return ArgumentMetaData(
        flags=list(flags),
        make_flag=make_flag,
        argument_group=group,
        mutually_exclusive_group=mutually_exclusive_group,
        dictionary=kwargs,
    )


def arg(
    *flags: str,
    make_flag: bool | None = None,
    group: ArgumentGroup | None = None,
    mutually_exclusive_group: MutuallyExclusiveGroup | None = None,
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
                argument_group=group,
                mutually_exclusive_group=mutually_exclusive_group,
                dictionary=kwargs,
            ),
            "subparser": subparser,
        },
    )


def get_metadata_from_field(field: Field[Any]) -> ArgumentData:
    if type(field.type) == str:
        field.type = eval(field.type)
    data: ArgumentData = ArgumentData(name=field.name, typeannotation=field.type)
    if field.default is not field.default_factory:
        data.default = field.default
    if field.metadata:
        data.parser = field.metadata.get("subparser", None)
        metadata: ArgumentMetaData = field.metadata.get("obj", None)
        data.flags = metadata.flags
        data.make_flag = metadata.make_flag
        data.argument_group = metadata.argument_group
        data.mutually_exclusive_group = metadata.mutually_exclusive_group
        data.kwargs = metadata.dictionary
    return data


def get_argdata_from_parameter(parameter: Parameter) -> ArgumentData:
    data: ArgumentData = ArgumentData(name=parameter.name, kind=parameter.kind)
    data.default = parameter.default
    if parameter.annotation is not EMPTY:
        annotation = parameter.annotation
        if type(annotation) == str:
            annotation = eval(annotation)
        data.typeannotation = annotation
        if hasattr(annotation, "__metadata__"):
            data.typeannotation = annotation.__origin__
            metadatas = annotation.__metadata__
            for metadata in metadatas:
                if isinstance(metadata, ArgumentMetaData):
                    data.flags = metadata.flags
                    data.make_flag = metadata.make_flag
                    data.argument_group = metadata.argument_group
                    data.mutually_exclusive_group = metadata.mutually_exclusive_group
                    data.kwargs = metadata.dictionary
                    break
    if parameter.annotation is EMPTY and parameter.default is not EMPTY:
        data.typeannotation = type(parameter.default)
    return data


def get_data_from_typeannotation(
    annotation: Any,
    default_bool: bool = False,
) -> tuple[str, str | int | None, type | Callable[[str], Any] | None, Sequence[Any] | None]:
    """Return `action`, `nargs`, `argtype`, `choices`"""
    action = "store"
    nargs = None
    argtype = annotation if callable(annotation) else str
    choices = None
    origin = get_origin(annotation)
    if origin:
        types = get_args(annotation)
        if origin in [Union, UnionType]:
            types = [t for t in get_args(annotation) if t is not type(None)]
            argtype = create_union_converter(types)
        if origin is tuple:
            nargs = len(types) if Ellipsis not in types else "*"
            argtype = types[0]
        if origin in [list, Sequence]:
            nargs = "*"
            argtype = types[0]
        if origin is Literal:
            choices = [t.name if isinstance(t, Enum) else t for t in types]
            argtype = create_literal_converter(types)
    if annotation == bool:
        action = "store_false" if default_bool else "store_true"
        argtype = None
    if isinstance(argtype, type) and issubclass(argtype, Enum):
        choices = list(getattr(argtype, "__members__").keys())
        argtype = None

    return action, nargs, argtype, choices


def run(func: Callable[..., Any], args: Sequence[str] | None = None, **kwargs):
    Command(func, **kwargs).run(args)


def create_literal_converter(types):
    def converter(s):
        for value in types:
            if isinstance(value, Enum) and s == getattr(value, "name"):
                return getattr(value, "name")
            if str(value) == s:
                return value
        raise ValueError("ERRO")

    return converter


def create_union_converter(types):
    if len(types) == 1 and issubclass(types[0], Enum):
        return types[0]

    def converter(value: str) -> Any:
        for t in types:
            try:
                if issubclass(t, Enum):
                    return t[value]
                # Attempt conversion
                converted_value = t(value)
                # Check string representation matches
                if str(converted_value) == value:
                    return converted_value
            except (ValueError, TypeError):
                continue  # Ignore and try the next type
        raise ValueError("ERRO")

    return converter
