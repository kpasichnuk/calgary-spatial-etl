from argparse import ArgumentParser
from time import perf_counter

from src.extract import run_extract
from src.load import run_load
from src.qa import run_qa
from src.transform import run_transform


def timed_stage(name: str, function) -> float:
    started = perf_counter()
    function()
    elapsed = perf_counter() - started
    print(f"{name} completed in {elapsed:.2f}s")
    return elapsed


def run_pipeline(skip_extract: bool = False, skip_load: bool = False) -> dict[str, float]:
    timings = {}
    if not skip_extract:
        timings["extract"] = timed_stage("Extract", run_extract)

    timings["transform"] = timed_stage("Transform", run_transform)
    timings["qa"] = timed_stage("QA", run_qa)

    if not skip_load:
        timings["load"] = timed_stage("Load", run_load)

    print(f"Pipeline completed: {timings}")
    return timings


def parse_args():
    parser = ArgumentParser(description="Run the Calgary spatial ETL pipeline.")
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Reuse existing raw files instead of downloading new snapshots.",
    )
    parser.add_argument(
        "--skip-load",
        action="store_true",
        help="Stop after QA without writing to PostGIS.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run_pipeline(skip_extract=arguments.skip_extract, skip_load=arguments.skip_load)
