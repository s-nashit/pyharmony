from pathlib import Path
from pyharmony.installer import pip_freeze

def write_requirements(python_exec: str, root: str = ".", filename: str = "requirements.txt") -> Path:
    req_path = Path(root) / filename
    req_path.write_text(pip_freeze(python_exec), encoding="utf-8")
    print(f"Generated {req_path}")
    return req_path
