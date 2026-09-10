"""Discover and build standalone math solutions with PyInstaller."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOLUTIONS_DIR = ROOT / "solutions"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


@dataclass(frozen=True)
class Solution:
    name: str
    path: Path

    @property
    def entry_point(self) -> Path:
        return self.path / "main.py"


def discover_solutions() -> list[Solution]:
    """Return solution folders that contain a main.py entry point."""
    if not SOLUTIONS_DIR.exists():
        return []

    return [
        Solution(path.name, path)
        for path in sorted(SOLUTIONS_DIR.iterdir())
        if path.is_dir() and (path / "main.py").is_file()
    ]


def select_solutions(name: str | None, build_all: bool) -> list[Solution]:
    solutions = discover_solutions()
    if build_all:
        return solutions
    if not name:
        raise SystemExit("Choose a solution with --solution or use --all.")

    selected = [solution for solution in solutions if solution.name == name]
    if not selected:
        available = ", ".join(solution.name for solution in solutions) or "none"
        raise SystemExit(f"Unknown solution {name!r}. Available solutions: {available}")
    return selected


def build_solution(solution: Solution) -> None:
    output_dir = DIST_DIR / solution.name
    work_dir = BUILD_DIR / solution.name
    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        solution.name,
        "--distpath",
        str(output_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(work_dir),
        str(solution.entry_point),
    ]
    print(f"Building {solution.name}...")
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except FileNotFoundError as error:
        raise SystemExit(
            "PyInstaller is not installed. Run: "
            "python -m pip install -r requirements-build.txt"
        ) from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--solution", help="Name of one solution folder to build")
    selection.add_argument("--all", action="store_true", help="Build every discovered solution")
    parser.add_argument("--list", action="store_true", help="List discovered solutions and exit")
    parser.add_argument("--clean", action="store_true", help="Remove generated build and dist folders before building")
    args = parser.parse_args()

    solutions = discover_solutions()
    if args.list:
        for solution in solutions:
            print(solution.name)
        return 0

    if args.clean:
        shutil.rmtree(DIST_DIR, ignore_errors=True)
        shutil.rmtree(BUILD_DIR, ignore_errors=True)

    selected = select_solutions(args.solution, args.all)
    if not selected:
        raise SystemExit("No solutions were found under solutions/. Add a folder containing main.py.")
    for solution in selected:
        build_solution(solution)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())