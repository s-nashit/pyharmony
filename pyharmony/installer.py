import subprocess
from typing import List, Set, Tuple

def run_command(cmd: List[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)

def get_installed_packages(python_exec: str) -> Set[str]:
    cmd = [python_exec, "-m", "pip", "list", "--format=freeze"]
    result = run_command(cmd, check=True)
    installed = set()

    for line in result.stdout.splitlines():
        if "==" in line:
            pkg = line.split("==")[0].strip().lower()
            installed.add(pkg)

    return installed

def install_packages(python_exec: str, packages: List[str], dry_run: bool = False) -> None:
    if not packages:
        print("No missing packages to install.")
        return

    cmd = [python_exec, "-m", "pip", "install"] + packages
    print("Install command:", " ".join(cmd))

    if dry_run:
        print("Dry run enabled. No packages were installed.")
        return

    subprocess.run(cmd, check=True)

def pip_check(python_exec: str) -> Tuple[int, str]:
    cmd = [python_exec, "-m", "pip", "check"]
    result = run_command(cmd, check=False)
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode, output

def pip_freeze(python_exec: str) -> str:
    cmd = [python_exec, "-m", "pip", "freeze"]
    result = run_command(cmd, check=True)
    return result.stdout
