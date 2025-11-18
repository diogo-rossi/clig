from pathlib import Path
import os

THISDIR: Path = Path(__file__).parent

os.chdir(THISDIR)


def convert_jupyter_notebook_to_markdown(notebook_name: str):
    os.system(f"jupyter nbconvert notebooks/{notebook_name}.ipynb --to markdown --output {notebook_name}.md")


def line_with_raised_error(line: str):
    return any([line.strip().startswith(error) for error in ["ValueError:", "TypeError:"]])


def format_exported_notebook_file(input_file_name: str, output_file_name: str | None = None):

    if output_file_name is None:
        output_file_name = input_file_name

    with open(f"notebooks/{input_file_name}.md", "r", encoding="utf-8") as file:
        text = file.read()

    # format shell cells
    text = text.replace("```python\n! python", "```\n> python")

    lines = text.split("\n")

    on_shell_snippet = False
    on_python_snippet = False
    on_python_snippet_output = False
    end_of_python_snippet_output = False
    on_python_snippet_decorator = False
    snippet_started = False
    in_error = False
    for i, line in enumerate(lines):

        if "Traceback (most recent call last):" in line:  # check if entered in error cells
            in_error = True
            lines[i] = "<must_remove>"
            continue

        if line_with_raised_error(line):  # check if exited error cells
            in_error = False

        if line.startswith("```python"):  # check if entered python snippet cell
            on_python_snippet = True
            continue

        if line.startswith("> python"):  # check if entered shell snippet cell
            on_shell_snippet = True
            continue

        if line.startswith("%%python"):  # The python snippet is a file snippet, not python snippet
            on_python_snippet = False
            lines[i] = "<must_remove>"

        if in_error:  # remove error cell
            lines[i] = "<must_remove>"
            continue

        if on_python_snippet:
            if line.startswith("```"):  # end of snippet containing python code. Need to continue for output
                lines[i] = "<must_remove>"  # remove this single line
                on_python_snippet = False  # end of snippet containing python code
                on_python_snippet_output = True  # the next is the output
                continue
            if line.startswith(" "):  # the line is indented, put '...'
                lines[i] = "... " + lines[i]
                continue
            if line.startswith("@"):  # the line contains a decorator, put '>>>' and start decorator block
                lines[i] = ">>> " + lines[i]
                on_python_snippet_decorator = True
                continue
            if on_python_snippet_decorator:  # the line is not indented but is in a decorator block, put '...'
                lines[i] = "... " + lines[i]
                on_python_snippet_decorator = False
                continue
            if len(line) == 0:  # the line is empty, put '...'
                lines[i] = "... " + lines[i]
                continue
            lines[i] = ">>> " + lines[i]  # the line is a common python command

        if on_python_snippet_output:
            if not line.startswith("    "):  # end or start of output snippet
                if end_of_python_snippet_output:  # end of output snippet
                    lines[i] = "```"  # finalize output snippet
                    on_python_snippet_output = False
                    end_of_python_snippet_output = False
                    continue
                else:
                    lines[i] = "<must_remove>"  # remove this single line
                    end_of_python_snippet_output = True  # the next indented will be the end of output snippet
                    continue
            lines[i] = lines[i].strip()

        if on_shell_snippet:
            if line.startswith("```"):  # end of notebook snippet containing single line with cli command
                lines[i] = "<must_remove>"  # remove this single line
                continue
            if not line.startswith("    "):  # end or start of output snippet
                if snippet_started:  # end of output snippet, because it already started
                    lines[i] = "```"  # finalize output snippet
                    on_shell_snippet = False
                    snippet_started = False
                    continue
                else:
                    snippet_started = True  # start of output snippet
                    continue
    # remove lines
    text = "\n".join([line for line in lines if line != "<must_remove>"]).replace("... \n...", "...")

    # merge snippets
    text = text.replace("\n```\n\n```python\n>>>", ">>>")

    with open(f"notebooks/{output_file_name}.md", "w", encoding="utf-8") as file:
        file.write(text)


convert_jupyter_notebook_to_markdown("userguide")

format_exported_notebook_file("userguide")
