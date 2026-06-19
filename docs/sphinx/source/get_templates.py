import clig.clig

source_file = clig.clig.__file__

LIST_OF_TEMPLATES = [
    "DESCRIPTION_DOCSTRING",
    "DESCRIPTION_EPILOG_DOCSTRING",
    "SPHINX_DOCSTRING",
    "NUMPY_DOCSTRING",
    "GOOGLE_DOCSTRING",
    "CLIG_DOCSTRING",
    "SPHINX_DOCSTRING_WITH_EPILOG",
    "NUMPY_DOCSTRING_WITH_EPILOG",
    "GOOGLE_DOCSTRING_WITH_EPILOG",
    "CLIG_DOCSTRING_WITH_EPILOG",
    "SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES",
    "NUMPY_DOCSTRING_WITH_EPILOG_NOTYPES",
    "GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES",
    "GOOGLE_DOCSTRING_NOTYPES",
    "CLIG_DOCSTRING_SHORT",
]


def extrac_text(text: str, initial_string: str, final_string: str):
    start_index = text.find(initial_string)
    final_index = text.find(final_string, start_index + len(initial_string))
    final_index += len(final_string)
    return text[start_index:final_index]


def extract_docstring_template(text: str, docname: str):
    return extrac_text(text, f'{docname} = """', '"""')


def write_templates():
    with open(source_file, "r", encoding="utf-8") as file:
        text = file.read()
    with open("docstrings_templates.md", "w", encoding="utf-8") as file:
        file.write("# Docstrings templates\n")
        file.write("\nBuilt-in docstring templates to use in inferring function/argument information.\n")

        for template in LIST_OF_TEMPLATES:
            file.write(
                f"## {template.replace("_"," ").lower().replace("docstring","").strip().capitalize()}\n"
            )
            file.write("\n```python\n")
            file.write(extract_docstring_template(text, template))
            file.write("\n```\n\n")
