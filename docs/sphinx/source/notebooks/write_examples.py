from typing import Any
import json

with open("userguide.ipynb", "r", encoding="utf-8") as file:
    text = file.read()

content: dict[str, Any] = json.loads(text)

cells: list[dict[str, Any]] = content["cells"]

example_number = -2
for i, cell in enumerate(cells):
    if cell.get("cell_type") == "code":
        source: list[str] | None = cell.get("source")
        if source and source[0].startswith("%%python"):
            example_number += 1
            source[1] = f'# example{example_number if example_number >= 0 else ""}.py\n'
            filename = source[1].lstrip("# ").strip()
            with open(filename, "w", encoding="utf-8") as file:
                file.write("import sys\nfrom pathlib import Path\npath = Path(__file__).parent\n")
                file.write('sys.path.insert(0, str((path / "../../../../src").resolve()))')
                file.write("".join(source[1:]))
        elif source and source[0].startswith("! python"):
            parts = source[0].split(".py")
            parts[0] = f'! python example{example_number if example_number >= 0 else ""}.py'
            source[0] = "".join(parts)
        if source:
            cell["source"] = source  # update source
            cells[i] = cell  # update cell

content["cells"] = cells  # update cells

with open("userguide.ipynb", "w", encoding="utf-8") as file:
    json.dump(content, file, indent=4)
