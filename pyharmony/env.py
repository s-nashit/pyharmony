# pyharmony/env.py

import os
import venv
from pathlib import Path

def ensure_venv(root: str = ".", venv_name: str = ".venv") -> Path:
    venv_path = Path(root) / venv_name
    if not venv_path.exists():
        print(f"Creating virtual environment at {venv_path} ...")
        venv.create(venv_path, with_pip=True)
    return venv_path

def get_venv_python(venv_path: Path) -> str:
    if os.name == "nt":
        return str(venv_path / "Scripts" / "python.exe")
    return str(venv_path / "bin" / "python")

def activation_hint(venv_path: Path) -> str:
    if os.name == "nt":
        return str(venv_path / "Scripts" / "activate")
    return f"source {venv_path / 'bin' / 'activate'}"