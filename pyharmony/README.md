# PyHarmony

**Resolve imports. Fix dependencies. Restore harmony.**

PyHarmony is an open-source CLI tool that scans a Python project, detects third-party imports, maps them to pip package names, creates a virtual environment, installs missing packages, checks for broken dependencies, and writes a `requirements.txt`.

> Ideal for scripts, quick prototypes, notebooks, training environments, and bootstrapping projects.

---

## ✨ Features

- Scan `.py` files (and optionally `.ipynb`) for imports
- Ignore Python standard library imports
- Detect local modules/packages so they are not installed from pip
- Map import names to pip package names (`cv2 -> opencv-python`, `bs4 -> beautifulsoup4`, etc.)
- Create/use a project-local `.venv`
- Install missing packages
- Run `pip check` to detect broken dependencies
- Generate `requirements.txt`
- Explain how imports were classified (stdlib / local / third-party)

---

## 🚀 Installation

Clone the repository and install in editable mode:

```bash
git clone [https://github.com/yourusername/pyharmony.git](https://github.com/s-nashit/pyharmony-cli)
cd pyharmony
pip install -e .
```
