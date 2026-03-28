from pathlib import Path
from typing import Set
from pyharmony.scanner import should_skip

def find_local_modules(root: str = ".") -> Set[str]:
    """
    Detect local modules/packages so we don't try to pip-install them.
    """
    root_path = Path(root)
    local_modules = set()

    # Python files => module names
    for py_file in root_path.rglob("*.py"):
        if should_skip(py_file):
            continue
        local_modules.add(py_file.stem)

    # Packages => folder containing __init__.py
    for init_file in root_path.rglob("__init__.py"):
        if should_skip(init_file):
            continue
        local_modules.add(init_file.parent.name)

    return local_modules
