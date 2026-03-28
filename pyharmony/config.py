# pyharmony/config.py

from pathlib import Path
import json
from typing import Dict

DEFAULT_MAP_FILE = "import_map.json"

def load_import_map(custom_map_path: str | None = None) -> Dict[str, str]:
    """
    Load import -> package mapping.
    Priority:
    1. custom_map_path if provided
    2. import_map.json in current working directory
    3. bundled default mapping from repository root (same cwd assumption for starter)
    """
    candidates = []

    if custom_map_path:
        candidates.append(Path(custom_map_path))

    candidates.append(Path.cwd() / DEFAULT_MAP_FILE)

    for candidate in candidates:
        if candidate.exists():
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception as e:
                print(f"Warning: could not load map file {candidate}: {e}")

    # Fallback built-in defaults
    return {
        "cv2": "opencv-python",
        "PIL": "Pillow",
        "sklearn": "scikit-learn",
        "bs4": "beautifulsoup4",
        "yaml": "PyYAML",
        "Crypto": "pycryptodome",
        "dateutil": "python-dateutil",
        "fitz": "PyMuPDF",
        "lxml": "lxml",
        "sns": "seaborn",
        "np": "numpy",  # alias commonly used but import is usually 'numpy as np'
        "pd": "pandas"  # alias commonly used but import is usually 'pandas as pd'
    }