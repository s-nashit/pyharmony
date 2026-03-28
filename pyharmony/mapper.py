# pyharmony/mapper.py

from typing import Iterable, List, Dict
from pyharmony.utils import unique_sorted

def map_import_to_package(module_name: str, import_map: Dict[str, str]) -> str:
    return import_map.get(module_name, module_name)

def map_imports(modules: Iterable[str], import_map: Dict[str, str]) -> List[str]:
    return unique_sorted(map_import_to_package(m, import_map) for m in modules)