# pyharmony/parser.py

import ast
import json
from pathlib import Path
from typing import Set

def extract_imports_from_source(source: str) -> Set[str]:
    imports = set()
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                # Skip relative imports like from . import x
                if node.module:
                    imports.add(node.module.split(".")[0])
    except SyntaxError:
        # ignore syntax errors for now
        pass
    return imports

def extract_imports_from_file(file_path: Path) -> Set[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return extract_imports_from_source(f.read())
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        return set()

def extract_imports_from_notebook(file_path: Path) -> Set[str]:
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
        cells = nb.get("cells", [])
        for cell in cells:
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            imports.update(extract_imports_from_source(source))
    except Exception as e:
        print(f"Skipping notebook {file_path}: {e}")
    return imports