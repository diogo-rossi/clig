import inspect
import re
from argparse import ArgumentParser
from dataclasses import dataclass, field
from inspect import Parameter, Signature, signature
from pprint import pprint
from typing import Any, Callable, Tuple, cast

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
- `{{parameter_name}}` (`{{parameter_name}}`):
    {{parameter_description}}
"""


@dataclass
class DocstringData:
    description: str
    epilog: str
    parameters: dict[str, str] = field(default_factory=dict)


def count_leading_spaces(string: str):
    return len(string) - len(string.lstrip())


def normalize_docstring(docstring: str | None) -> str:
    """https://peps.python.org/pep-0257/#handling-docstring-indentation"""
    if not docstring:
        return ""
    lines: list[str] = docstring.expandtabs(tabsize=4).splitlines()
    indentation: int = min([len(line) - len(line.lstrip()) for line in lines[1:] if line.lstrip()])
    lines: list[str] = [lines[0].strip()] + [
        line.removeprefix(" " * indentation).rstrip() for line in lines[1:]
    ]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


def get_docstring_data(
    parameter_number: int, docstring: str, template: str = NUMPY_DOCSTRING
) -> DocstringData | None:
    docstring = normalize_docstring(docstring)
    template = normalize_docstring(template)
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
    parameter_section = "\n".join(template.splitlines()[parameter_section_init_index:])
    for _ in range(parameter_number - 1):
        template += f"{parameter_section}\n"
    for place_holder in place_holders:
        template = template.replace(f"{{{{{place_holder}}}}}", "(.*?)")
    template += "(.*)"
    match = re.match(template, docstring, re.DOTALL)
    if match:
        matches: tuple[str, ...] = match.groups()
        docstring_data = DocstringData(
            matches[place_holders["description"][0]], matches[place_holders["epilog"][0]]
        )
        for i in range(parameter_number):
            docstring_data.parameters[
                matches[place_holders["parameter_name"][0] + parameter_section_length * i]
            ] = matches[
                place_holders["parameter_description"][0] + parameter_section_length * i
            ].strip()
        print(matches[-1])
        return docstring_data
    return None
