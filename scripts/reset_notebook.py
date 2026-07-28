#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STARTER_DIRS = {
    "learning": PROJECT_ROOT / "learning" / "starters",
    "analysis": PROJECT_ROOT / "analysis" / "starters",
}
TEST_DIRS = {
    "learning": PROJECT_ROOT / "learning" / "module_tests",
    "analysis": PROJECT_ROOT / "analysis" / "module_tests",
}
WORKING_DIRS = {
    "learning": PROJECT_ROOT / "learning" / "working",
    "analysis": PROJECT_ROOT / "analysis" / "working",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create ignored working copies from clean notebook starters."
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
    parser.add_argument(
        "--test",
        action="store_true",
        help="Create a working copy from a module test instead of a practice starter.",
    )
    parser.add_argument(
        "--analysis",
        action="store_true",
        help="Use the spatial-analysis curriculum instead of the core learning curriculum.",
    )
    return parser.parse_args()


def find_source_notebooks(
    module: str,
    resource: str = "practice",
    curriculum: str = "learning",
) -> list[Path]:
    source_dir = TEST_DIRS[curriculum] if resource == "test" else STARTER_DIRS[curriculum]
    prefix = "project1_analysis_module" if curriculum == "analysis" else "project1_module"

    if module == "all":
        paths = sorted(source_dir.glob(f"{prefix}_*_{resource}.ipynb"))
    elif module.isdigit():
        paths = sorted(
            source_dir.glob(f"{prefix}_{int(module)}_*_{resource}.ipynb")
        )
    else:
        raise ValueError("Module must be a number or 'all'.")

    if not paths:
        raise FileNotFoundError(
            f"No {resource} notebook found for module {module}."
        )
    if module != "all" and len(paths) > 1:
        raise RuntimeError(
            f"More than one {resource} notebook matched module {module}."
        )
    return paths


def working_path(
    source_path: Path,
    resource: str = "practice",
    curriculum: str = "learning",
) -> Path:
    replacement = "_test_working.ipynb" if resource == "test" else "_working.ipynb"
    name = source_path.name.replace(f"_{resource}.ipynb", replacement)
    return WORKING_DIRS[curriculum] / name


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


def reset_notebooks(
    module: str,
    force: bool,
    resource: str = "practice",
    curriculum: str = "learning",
) -> list[Path]:
    source_paths = find_source_notebooks(module, resource, curriculum)
    destinations = [working_path(path, resource, curriculum) for path in source_paths]
    existing = [path for path in destinations if path.exists()]

    if existing and not force:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(
            f"Working copy already exists: {names}. Use --force to replace it."
        )

    WORKING_DIRS[curriculum].mkdir(parents=True, exist_ok=True)
    for source_path, destination in zip(source_paths, destinations):
        shutil.copy2(source_path, destination)
        clear_execution_state(destination)
    return destinations


def main() -> None:
    args = parse_args()
    resource = "test" if args.test else "practice"
    curriculum = "analysis" if args.analysis else "learning"
    try:
        destinations = reset_notebooks(
            args.module.lower(), args.force, resource, curriculum
        )
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as error:
        raise SystemExit(f"ERROR: {error}") from error

    for destination in destinations:
        print(f"Created {destination.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()