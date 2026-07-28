#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRACTICE_DIR = PROJECT_ROOT / "learning" / "practice"
ATTEMPTS_DIR = PROJECT_ROOT / "learning" / "attempts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create clean, disposable attempts from practice notebooks."
    )
    parser.add_argument(
        "module",
        help="Module number to reset, such as 0, or 'all' for every module.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing attempt notebook.",
    )
    return parser.parse_args()


def find_practice_notebooks(module: str) -> list[Path]:
    if module == "all":
        paths = sorted(PRACTICE_DIR.glob("project1_module_*_practice.ipynb"))
    elif module.isdigit():
        paths = sorted(
            PRACTICE_DIR.glob(f"project1_module_{int(module)}_*_practice.ipynb")
        )
    else:
        raise ValueError("Module must be a number or 'all'.")

    if not paths:
        raise FileNotFoundError(f"No practice notebook found for module {module}.")
    if module != "all" and len(paths) > 1:
        raise RuntimeError(f"More than one practice notebook matched module {module}.")
    return paths


def attempt_path(practice_path: Path) -> Path:
    name = practice_path.name.replace("_practice.ipynb", "_attempt.ipynb")
    return ATTEMPTS_DIR / name


def clear_execution_state(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
    path.write_text(
        json.dumps(notebook, indent=1, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def reset_notebooks(module: str, force: bool) -> list[Path]:
    practice_paths = find_practice_notebooks(module)
    destinations = [attempt_path(path) for path in practice_paths]
    existing = [path for path in destinations if path.exists()]

    if existing and not force:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(
            f"Attempt already exists: {names}. Use --force to replace it."
        )

    ATTEMPTS_DIR.mkdir(parents=True, exist_ok=True)
    for practice_path, destination in zip(practice_paths, destinations):
        shutil.copy2(practice_path, destination)
        clear_execution_state(destination)
    return destinations


def main() -> None:
    args = parse_args()
    try:
        destinations = reset_notebooks(args.module.lower(), args.force)
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as error:
        raise SystemExit(f"ERROR: {error}") from error

    for destination in destinations:
        print(f"Created {destination.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()