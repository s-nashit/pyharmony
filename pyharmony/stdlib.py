import sys

try:
    STDLIB = set(sys.stdlib_module_names)  # Python 3.10+
except AttributeError:
    STDLIB = {
        "os", "sys", "math", "json", "re", "time", "datetime", "random",
        "collections", "itertools", "functools", "pathlib", "subprocess",
        "typing", "statistics", "csv", "sqlite3", "logging", "argparse",
        "unittest", "http", "urllib", "email", "hashlib", "threading",
        "multiprocessing", "shutil", "glob", "tempfile", "inspect",
        "dataclasses", "abc", "enum", "traceback"
    }

def is_stdlib(module_name: str) -> bool:
    return module_name in STDLIB
