from typing import Any
import json

with open("userguide.ipynb", "r", encoding="utf-8") as file:
    text = file.read()

cells: list[dict[str, Any]] = json.loads(text)["cells"]

for cell in cells:
    if cell.get("cell_type") == "code":
        source: list[str] | None = cell.get("source")
        if source and source[0].startswith("# example"):
            filename = source[0].lstrip("# ").strip()
            with open(filename, "w", encoding="utf-8") as file:
                file.write("".join(source))
