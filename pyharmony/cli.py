import typer
from typing import Set

from pyharmony.scanner import find_python_files, find_notebook_files
from pyharmony.parser import extract_imports_from_file, extract_imports_from_notebook
from pyharmony.stdlib import is_stdlib
from pyharmony.localmods import find_local_modules
from pyharmony.mapper import map_imports
from pyharmony.config import load_import_map
from pyharmony.env import ensure_venv, get_venv_python, activation_hint
from pyharmony.installer import get_installed_packages, install_packages, pip_check
from pyharmony.freeze import write_requirements
from pyharmony.utils import unique_sorted

app = typer.Typer(
    help="PyHarmony - Detect imports, install missing packages in a virtual environment, and manage dependencies."
)

def collect_imports(root: str = ".", include_notebooks: bool = False) -> Set[str]:
    imports = set()

    for file in find_python_files(root):
        imports.update(extract_imports_from_file(file))

    if include_notebooks:
        for nb in find_notebook_files(root):
            imports.update(extract_imports_from_notebook(nb))

    return imports

def filter_third_party(imports: Set[str], root: str = ".") -> list[str]:
    local_modules = find_local_modules(root)

    filtered = [
        m for m in imports
        if not is_stdlib(m) and m not in local_modules
    ]

    return unique_sorted(filtered)

@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to project root"),
    notebooks: bool = typer.Option(False, "--notebooks", help="Include Jupyter notebooks (.ipynb)"),
    map_file: str = typer.Option(None, "--map-file", help="Custom import map JSON file"),
):
    """
    Scan a project and display detected third-party imports and mapped packages.
    """
    import_map = load_import_map(map_file)
    imports = collect_imports(path, include_notebooks=notebooks)
    third_party = filter_third_party(imports, path)
    packages = map_imports(third_party, import_map)

    typer.echo("\nDetected third-party imports:")
    for m in third_party:
        typer.echo(f" - {m}")

    typer.echo("\nMapped packages:")
    for p in packages:
        typer.echo(f" - {p}")

@app.command()
def install(
    path: str = typer.Argument(".", help="Path to project root"),
    notebooks: bool = typer.Option(False, "--notebooks", help="Include Jupyter notebooks (.ipynb)"),
    map_file: str = typer.Option(None, "--map-file", help="Custom import map JSON file"),
    venv_name: str = typer.Option(".venv", "--venv-name", help="Virtual environment folder name"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show install command but do not install"),
    no_freeze: bool = typer.Option(False, "--no-freeze", help="Do not write requirements.txt"),
):
    """
    Create/use a virtual environment, detect missing packages, install them, run pip check, and write requirements.txt.
    """
    import_map = load_import_map(map_file)
    imports = collect_imports(path, include_notebooks=notebooks)
    third_party = filter_third_party(imports, path)
    packages = map_imports(third_party, import_map)

    venv_path = ensure_venv(path, venv_name)
    py_exec = get_venv_python(venv_path)

    typer.echo(f"\nUsing Python: {py_exec}")

    installed = get_installed_packages(py_exec)
    missing = [p for p in packages if p.lower() not in installed]

    typer.echo("\nMissing packages:")
    if missing:
        for p in missing:
            typer.echo(f" - {p}")
    else:
        typer.echo(" - None")

    install_packages(py_exec, missing, dry_run=dry_run)

    if not dry_run:
        code, output = pip_check(py_exec)
        if code == 0:
            typer.echo("\nDependency check: OK")
        else:
            typer.echo("\nDependency issues found:")
            typer.echo(output)

        if not no_freeze:
            write_requirements(py_exec, path)

    typer.echo(f"\nTo activate the environment:\n{activation_hint(venv_path)}")

@app.command()
def doctor(
    path: str = typer.Argument(".", help="Path to project root"),
    venv_name: str = typer.Option(".venv", "--venv-name", help="Virtual environment folder name"),
):
    """
    Run pip check inside the project's virtual environment to detect broken dependencies.
    """
    venv_path = ensure_venv(path, venv_name)
    py_exec = get_venv_python(venv_path)

    code, output = pip_check(py_exec)
    if code == 0:
        typer.echo("No broken dependencies found.")
    else:
        typer.echo("Dependency issues found:")
        typer.echo(output)

@app.command()
def freeze(
    path: str = typer.Argument(".", help="Path to project root"),
    venv_name: str = typer.Option(".venv", "--venv-name", help="Virtual environment folder name"),
    filename: str = typer.Option("requirements.txt", "--filename", help="Output filename"),
):
    """
    Write pip freeze output from the project's virtual environment to requirements.txt (or custom filename).
    """
    venv_path = ensure_venv(path, venv_name)
    py_exec = get_venv_python(venv_path)
    write_requirements(py_exec, path, filename=filename)

@app.command()
def explain(
    path: str = typer.Argument(".", help="Path to project root"),
    notebooks: bool = typer.Option(False, "--notebooks", help="Include Jupyter notebooks (.ipynb)"),
    map_file: str = typer.Option(None, "--map-file", help="Custom import map JSON file"),
):
    """
    Show import -> classification -> package mapping (useful for debugging / teaching).
    """
    import_map = load_import_map(map_file)
    imports = collect_imports(path, include_notebooks=notebooks)
    local_modules = find_local_modules(path)

    typer.echo("\nImport analysis:")
    for m in unique_sorted(imports):
        if is_stdlib(m):
            kind = "stdlib"
            pkg = "-"
        elif m in local_modules:
            kind = "local"
            pkg = "-"
        else:
            kind = "third-party"
            pkg = import_map.get(m, m)

        typer.echo(f" - {m:20} | {kind:10} | {pkg}")

if __name__ == "__main__":
    app()
