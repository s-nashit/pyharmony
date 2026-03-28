from pathlib import Path
from typing import List

EXCLUDE_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}

def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)

def find_python_files(root: str = ".") -> List[Path]:
    root_path = Path(root)
    files = []
    for p in root_path.rglob("*.py"):
        if should_skip(p):
            continue
        files.append(p)
    return files

def find_notebook_files(root: str = ".") -> List[Path]:
    root_path = Path(root)
    files = []
    for p in root_path.rglob("*.ipynb"):
        if should_skip(p):
            continue
        files.append(p)
    return files
