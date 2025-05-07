#!/usr/bin/env python3
import subprocess
import os
import venv

VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"

def check_venv(path: str):
    if not os.path.isdir(path):
        print("VENV: Not found")
        print(f"Creating virtual environment in {path}…")
        venv.create(path, with_pip=True)
    else:
        print(f"VENV: OK")

def get_python_exec_venv(path: str) -> str:
    python_exec = "python.exe" if os.name == "nt" else "python"
    return os.path.join(path, "Scripts" if os.name == "nt" else "bin", python_exec)

def get_required_dependencies(path: str) -> list[str]:
    with open(path, "r") as f:
        pkgs = []
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pkg = line.split("==")[0].split(">=")[0].split("<=")[0]
            pkgs.append(pkg)
        return pkgs

def is_pkg_installed_venv(pkg: str, python_exec: str) -> bool:
    try:
        subprocess.check_output([
            python_exec, "-c",
            f"import importlib.metadata as m; m.version('{pkg}')"
        ], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_pkg_venv(pkgs: list[str], python_exec: str):
    missing = [p for p in pkgs if not is_pkg_installed_venv(p, python_exec)]
    if not missing:
        print("Dependencies: OK")
        return
    print(f"Installing missing dependencies...")
    subprocess.check_call([python_exec, "-m", "pip", "install", *missing])

def main():
    check_venv(VENV_DIR)
    python_exec = get_python_exec_venv(VENV_DIR)
    pkgs = get_required_dependencies(REQUIREMENTS_FILE)
    install_pkg_venv(pkgs, python_exec)

    subprocess.check_call([python_exec, "-m", "main"])


if __name__ == "__main__":
    main()