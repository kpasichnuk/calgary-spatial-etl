#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKING_DIRS = {
    "learning": PROJECT_ROOT / "learning" / "working",
    "analysis": PROJECT_ROOT / "analysis" / "working",
}
ATTEMPT_DIRS = {
    "learning": PROJECT_ROOT / "learning" / "attempts",
    "analysis": PROJECT_ROOT / "analysis" / "attempts",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preserve completed working notebooks as version-controlled attempts."
    )
    parser.add_argument(
        "module",
        help="Module number to save, such as 0, or 'all' for every module.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Save a module-test working copy instead of a practice working copy.",
    )
    parser.add_argument(
        "--analysis",
        action="store_true",
        help="Use the spatial-analysis curriculum instead of the core learning curriculum.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing preserved attempt.",
    )
    return parser.parse_args()


def find_working_notebooks(
    module: str,
    resource: str = "practice",
    curriculum: str = "learning",
) -> list[Path]:
    working_dir = WORKING_DIRS[curriculum]
    prefix = "project1_analysis_module" if curriculum == "analysis" else "project1_module"
    suffix = "_test_working.ipynb" if resource == "test" else "_working.ipynb"

    if module == "all":
        paths = sorted(working_dir.glob(f"{prefix}_*{suffix}"))
    elif module.isdigit():
        paths = sorted(working_dir.glob(f"{prefix}_{int(module)}_*{suffix}"))
    else:
        raise ValueError("Module must be a number or 'all'.")

    if resource == "practice":
        paths = [path for path in paths if not path.name.endswith("_test_working.ipynb")]

    if not paths:
        raise FileNotFoundError(
            f"No {curriculum} {resource} working notebook found for module {module}."
        )
    if module != "all" and len(paths) > 1:
        raise RuntimeError(
            f"More than one {curriculum} {resource} working notebook matched module {module}."
        )
    return paths


def attempt_path(working_path: Path, curriculum: str = "learning") -> Path:
    name = working_path.name.replace("_working.ipynb", "_attempt.ipynb")
    return ATTEMPT_DIRS[curriculum] / name


def save_attempts(
    module: str,
    force: bool,
    resource: str = "practice",
    curriculum: str = "learning",
) -> list[Path]:
    working_paths = find_working_notebooks(module, resource, curriculum)
    destinations = [attempt_path(path, curriculum) for path in working_paths]
    existing = [path for path in destinations if path.exists()]

    if existing and not force:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(
            f"Preserved attempt already exists: {names}. Use --force to replace it."
        )

    for working_path in working_paths:
        json.loads(working_path.read_text(encoding="utf-8"))

    ATTEMPT_DIRS[curriculum].mkdir(parents=True, exist_ok=True)
    for working_path, destination in zip(working_paths, destinations):
        shutil.copy2(working_path, destination)
    return destinations


def main() -> None:
    args = parse_args()
    resource = "test" if args.test else "practice"
    curriculum = "analysis" if args.analysis else "learning"
    try:
        destinations = save_attempts(
            args.module.lower(), args.force, resource, curriculum
        )
    except (
        FileExistsError,
        FileNotFoundError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        raise SystemExit(f"ERROR: {error}") from error

    for destination in destinations:
        print(f"Saved {destination.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
