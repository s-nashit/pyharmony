from pathlib import Path
from typing import Iterable, List

def unique_sorted(items: Iterable[str]) -> List[str]:
    return sorted(set(items))

def is_hidden_path(path: Path) -> bool:
    return any(part.startswith(".") and part not in {".", ".."} for part in path.parts)

def print_header(title: str):
    line = "=" * len(title)
    print(f"\n{title}\n{line}")
