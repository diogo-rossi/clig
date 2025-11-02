import os

os.system("jupyter nbconvert notebooks/userguide.ipynb --to markdown --output userguide.md")

with open("notebooks/userguide.md", "r", encoding="utf-8") as file:
    text = file.read()

text = text.replace("```python\n! python", "```\n> python")

lines = text.split("\n")

on_snippet = False
snippet_started = False
for i, line in enumerate(lines):
    if line.strip().startswith("Couldn't find"):
        lines[i] = "<must_remove>"
    if line.startswith("%%python"):
        lines[i] = "<must_remove>"
    if line.startswith("```bash") or line.startswith("> python"):
        on_snippet = True
        continue
    if on_snippet:
        if line.startswith("```"):
            lines[i] = "<must_remove>"
            continue
        if not line.startswith("    "):
            if snippet_started:
                lines[i] = "```"
                on_snippet = False
                snippet_started = False
                continue
            else:
                snippet_started = True
                continue


text = "\n".join([line for line in lines if line != "<must_remove>"])
with open("notebooks/userguide.md", "w", encoding="utf-8") as file:
    file.write(text)

# with open("../../../src/clig/__init__.pyi", "w", encoding="utf-8") as file:
#     file.write(
#         '"""\n'
#         + text.replace('"""', '\\"\\"\\"')
#         .replace("```\n\n```", "```\n`\n```")
#         .replace("```\n\n\n```", "```\n`\n```")
#         + '"""\n'
#     )
