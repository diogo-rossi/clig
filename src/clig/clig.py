from __future__ import annotations

import inspect
import re
from argparse import ArgumentParser, FileType, HelpFormatter
from dataclasses import KW_ONLY, Field, dataclass, field
from inspect import Parameter
from inspect import _ParameterKind as ParameterKind
from types import MappingProxyType, UnionType
from collections.abc import Sequence
from typing import get_args, get_origin, Union
from typing import Any, Callable, Iterable, Literal, Mapping, Self, TypedDict, Unpack, overload
from enum import StrEnum

EMPTY = Parameter.empty

DESCRIPTION_DOCSTRING = """
    {{description}}
"""

NUMPY_DOCSTRING = """
    {{description}}

    {{epilog}}

    Parameters
    ----------
    {{parameter_name}} : {{parameter_type}}
        {{parameter_description}}
"""

SPHINX_DOCSTRING = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""

GOOGLE_DOCSTRING = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""

CLIG_DOCSTRING = """
{{description}}

{{epilog}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}
    {{parameter_description}}
"""

DOCSTRING_TEMPLATES = [
    DESCRIPTION_DOCSTRING,
    NUMPY_DOCSTRING,
    SPHINX_DOCSTRING,
    GOOGLE_DOCSTRING,
    CLIG_DOCSTRING,
]

SUBPARSERS_DEST = "subparser_name"


class DocStr(StrEnum):
    NUMPY_DOCSTRING = NUMPY_DOCSTRING
    SPHINX_DOCSTRING = SPHINX_DOCSTRING
    GOOGLE_DOCSTRING = GOOGLE_DOCSTRING
    CLIG_DOCSTRING = CLIG_DOCSTRING


@dataclass
class Command:
    func: Callable[..., Any] | None = None
    prog: str | None = None
    usage: str | None = None
    description: str | None = None
    epilog: str | None = None
    parents: Sequence[ArgumentParser] = field(default_factory=list)
    formatter_class: type[HelpFormatter] = HelpFormatter
    prefix_chars: str = "-"
    fromfile_prefix_chars: str | None = None
    argument_default: Any = None
    conflict_handler: str = "error"
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True
    _: KW_ONLY
    subcommands_title: str = "subcommands"
    subcommands_description: str | None = None
    subcommands_prog: str | None = None
    subcommands_required: bool = False
    subcommands_help: str | None = None
    subcommands_metavar: str | None = None
    docstring_template: str | DocStr | None = None

    def __post_init__(self):
        self.parameters: Mapping[str, Parameter] = {}
        if self.func:
            self.parameters = inspect.signature(self.func).parameters
        self.argument_data: list[ArgumentData] = self.get_argument_data()
        self.parent: Command | None = None
        self.sub_commands: list[Command] = []
        self.startflags: str = f"{self.prefix_chars}" * 2

    @overload
    def command[**P, T](self, func: Callable[P, T]) -> Callable[P, T]: ...

    @overload
    def command[**P, T](self, **kwargs) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

    def command[**P, T](
        self,
        func: Callable[P, T] | None = None,
        **kwargs,
    ) -> Callable[P, T] | Callable[[Callable[P, T]], Callable[P, T]]:  # fmt: skip
        if func is not None:
            self.new_command(func)
            return func

        def wrap(func):
            self.new_command(func, **kwargs)
            return func

        return wrap

    def add_command(self, func: Callable[..., Any], *args, **kwargs) -> Self:
        self.new_command(func, *args, **kwargs)
        return self

    def new_command(self, func: Callable[..., Any], *args, **kwargs) -> Command:
        count = -1
        parent_parser = self.parent
        while parent_parser:
            count += 1
            parent_parser = parent_parser.parent
        self.subparsers_dest = f"{SUBPARSERS_DEST}{'_' if count >= 0 else ""}{count if count >= 0 else ''}"
        cmd: Command = Command(func, *args, **kwargs)
        self.sub_commands.append(cmd)
        cmd.parent = self
        return cmd

    def get_argument_data(self) -> list[ArgumentData]:
        argument_data: list[ArgumentData] = []

        docstring_data: DocstringData | None = self.get_inferred_docstring_data()

        helps: dict[str, str] = {}
        if docstring_data:
            helps: dict[str, str] = docstring_data.helps
            self.description = docstring_data.description
            self.epilog = docstring_data.epilog

        for par in self.parameters:
            data = get_argdata_from_parameter(self.parameters[par])
            data.help = helps.get(data.name)
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
        separator: str = "################################"
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
            docstring = docstring.rstrip() + separator
            template = template.rstrip() + separator
        for place_holder in place_holders:
            template = template.replace(f"{{{{{place_holder}}}}}", "(.*?)")
        docstring += "\n"
        template += "(.*)"
        match = re.match(template, docstring, re.DOTALL)
        if match:
            matches: tuple[str, ...] = match.groups()
            description = matches[place_holders["description"][0]] if place_holders["description"] else None
            epilog = matches[place_holders["epilog"][0]] if place_holders["epilog"] else None
            docstring_data = DocstringData(description=description, epilog=epilog)
            for i in range(parameter_number):
                docstring_data.helps[
                    matches[place_holders["parameter_name"][0] + parameter_section_length * i]
                ] = matches[place_holders["parameter_description"][0] + parameter_section_length * i].strip()
            return docstring_data
        return None

    def make_argflagged(self, name: str) -> str:
        return f"{self.startflags}{name}"

    def inferarg(self, argdata: ArgumentData) -> tuple[tuple[str, ...], CompleteKeywordArguments]:
        kwargs: CompleteKeywordArguments = {"dest": argdata.name}
        kwargs["help"] = argdata.kwargs.get("help", argdata.help)
        action, nargs, argtype, choices = "store", None, str, None
        if argdata.type is not None:
            action, nargs, argtype, choices = get_data_from_argtype(argdata.type)
        kwargs["default"] = argdata.kwargs.get("default", argdata.default)
        kwargs["action"] = argdata.kwargs.get("action") or action
        kwargs["type"] = argdata.kwargs.get("type") or argtype
        if kwargs["action"] in ["store", "append"]:
            kwargs["nargs"] = argdata.kwargs.get("nargs") or nargs
            kwargs["choices"] = argdata.kwargs.get("choices") or choices
        argdata.make_flag = (
            all(
                [
                    argdata.make_flag is None,
                    kwargs["default"] is not EMPTY,
                    kwargs.get("nargs") not in ["*", "?"],
                ]
            )
            or argdata.make_flag
        )
        argflagged: str | None = None
        if argdata.make_flag or all(
            [
                argdata.make_flag is None,
                argdata.flags,
                not any([flag.startswith(f"{self.startflags}") for flag in argdata.flags]),
            ]
        ):
            argflagged = self.make_argflagged(argdata.name)
        if argflagged:
            argdata.flags.append(argflagged)
        if kwargs["default"] is EMPTY:
            kwargs["default"] = None
            if argdata.flags:
                kwargs["required"] = argdata.kwargs.get("required") or True

        # given in `argdata.kwargs` has preference over inferred
        for key in ["metavar", "const", "version"]:
            try:
                kwargs[key] = argdata.kwargs.pop(key)  # type: ignore
            except KeyError:
                pass
        return tuple(argdata.flags), kwargs

    def add_parsers(self) -> None:
        """"""
        ...

    def run(self, args: Sequence[str] | None = None) -> None:
        if not self.is_main_command:
            return

    @property
    def is_main_command(self) -> bool:
        return self.parent is None


class Application:
    main: Callable[..., Any] | None = None
    prog: str = ""
    prefix_chars: str = "-"

    def __post_init__(self):
        self.parser = ArgumentParser()

    def command[**P, T](self, func: Callable[P, T]) -> Callable[P, T]:
        return func

    def add_command(self, func: Callable[..., Any]) -> Self:
        return self

    def new_command(self, func: Callable[..., Any]) -> Command:
        return Command()


class ArgumentMetaDataDictionary(TypedDict, total=False):
    action: str
    nargs: int | str | None
    const: Any
    choices: Iterable | None
    required: bool | None
    help: str | None
    metavar: str | tuple[str, ...] | None
    version: str | None


class KeywordArguments(ArgumentMetaDataDictionary, total=False):
    default: Any
    type: type | None


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
    type: Callable[[str], Any] | str | FileType | None = None
    kind: ParameterKind = ParameterKind.POSITIONAL_OR_KEYWORD
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
    data: ArgumentData = ArgumentData(name=field.name, type=field.type)
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
        if callable(annotation):
            data.type = annotation
        if hasattr(annotation, "__metadata__"):
            data.type = annotation.__origin__
            metadata: ArgumentMetaData = annotation.__metadata__
            if isinstance(metadata, ArgumentMetaData):
                data.flags = metadata.flags
                data.make_flag = metadata.make_flag
                data.argument_group = metadata.argument_group
                data.mutually_exclusive_group = metadata.mutually_exclusive_group
                data.kwargs = metadata.dictionary
    if parameter.annotation is EMPTY and parameter.default is not EMPTY:
        data.type = type(parameter.default)
    return data


def get_data_from_argtype(
    argtype: Any,
    default_bool: bool = False,
) -> tuple[str, str | int | None, type | None, Sequence[Any] | None]:
    """Return `action`, `nargs`, `argtype`, `choices`"""
    action = "store"
    nargs = None
    typ = str
    choices = None
    origin = get_origin(argtype)
    if origin:
        args = get_args(argtype)
        if origin is tuple:
            nargs = len(args) if Ellipsis not in args else "*"
            typ = args[0]
        if origin in [list, Sequence, Union, UnionType]:
            typ = [a for a in args if a is not type(None)][0]
            nargs = "*"
        if origin is Literal:
            choices = args
    else:
        typ = argtype
        if typ == bool:
            action = "store_false" if default_bool else "store_true"

    return action, nargs, typ, choices
