# Project 1 Module 3: Extract Reference

## File Purpose
This module performs the Extract stage of ETL:
1. Reads dataset metadata from configuration.
2. Downloads raw files from source URLs.
3. Saves files to stable paths.
4. Writes a provenance log for traceability.

## Current Source

```python
from pathlib import Path
from datetime import datetime, timezone
import csv
import requests

from src.config import DATASETS


LOG_PATH = Path("outputs/logs/extract_log.csv")


def ensure_parent_dir(file_path: str) -> None:
Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def append_log(rows: list[dict]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_PATH.exists()

    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dataset",
                "source_url",
                "output_path",
                "downloaded_at_utc",
                "http_status",
                "bytes_written",
            ],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)


def run_extract() -> None:
    log_rows = []

    for dataset_name, cfg in DATASETS.items():
        url = cfg["url"]
        output_path = cfg["output"]  # stable name defined in config.py
        ensure_parent_dir(output_path)

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        data_bytes = response.content
        Path(output_path).write_bytes(data_bytes)

        log_rows.append(
            {
                "dataset": dataset_name,
                "source_url": url,
                "output_path": output_path,
                "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
                "http_status": response.status_code,
                "bytes_written": len(data_bytes),
            }
        )

        print(f"Saved {dataset_name} -> {output_path} ({len(data_bytes)} bytes)")

    append_log(log_rows)
    print(f"Wrote log -> {LOG_PATH}")


if __name__ == "__main__":
    run_extract()
```

## Line-by-Line and Concept Breakdown

### Imports
`from pathlib import Path`
- Imports `Path`, an object-oriented path API.
- Better than manual string concatenation for file paths.

`from datetime import datetime, timezone`
- `datetime` gives current timestamps.
- `timezone.utc` ensures UTC-aware timestamps.

`import csv`
- Standard library module for CSV writing.

`import requests`
- Third-party HTTP client library for downloading datasets.

`from src.config import DATASETS`
- Imports the shared dataset configuration dictionary.
- Keeps source URLs and paths centralized in one place.

### Constant
`LOG_PATH = Path("outputs/logs/extract_log.csv")`
- Defines where extract metadata is logged.
- Uses `Path` so path operations are cross-platform.

### Function: ensure_parent_dir
`def ensure_parent_dir(file_path: str) -> None:`
- Type hint: input is a string path.
- Return hint `-> None`: function returns nothing.

`Path(file_path).parent.mkdir(parents=True, exist_ok=True)`
- Converts string to Path object.
- `.parent` gets parent directory.
- `.mkdir(parents=True, exist_ok=True)` creates directory tree safely.

Python concepts:
1. Type hints improve readability and tooling.
2. Idempotent directory creation avoids crashes on reruns.

### Function: append_log
`def append_log(rows: list[dict]) -> None:`
- Accepts a list of dictionaries.
- Each dict is one row of log data.

`LOG_PATH.parent.mkdir(...)`
- Ensures log folder exists.

`file_exists = LOG_PATH.exists()`
- Checks whether the CSV already exists to decide header behavior.

`with LOG_PATH.open("a", newline="", encoding="utf-8") as f:`
- Opens file in append mode (`"a"`).
- `with` ensures file is closed automatically.
- `newline=""` avoids blank lines in CSV on some platforms.
- UTF-8 encoding for safe text output.

`writer = csv.DictWriter(...)`
- Builds a writer that maps dictionary keys to CSV columns.
- `fieldnames` defines column order explicitly.

`if not file_exists: writer.writeheader()`
- Writes column names only the first time.

`writer.writerows(rows)`
- Appends all collected rows in one call.

Python concepts:
1. Context manager (`with`) for resource safety.
2. DictWriter for structured tabular output.
3. Boolean condition with `if not ...`.

### Function: run_extract
`def run_extract() -> None:`
- Orchestrates entire extract stage.

`log_rows = []`
- Initializes an empty list to collect log dictionaries.

`for dataset_name, cfg in DATASETS.items():`
- Iterates through configured datasets.
- `dataset_name` is the key (for example `communities`).
- `cfg` is nested dict with `url`, `output`, `format`.

`url = cfg["url"]`
- Reads source URL from config.

`output_path = cfg["output"]`
- Reads destination raw path from config.

`ensure_parent_dir(output_path)`
- Creates destination folder if needed.

`response = requests.get(url, timeout=60)`
- Downloads data from the endpoint.
- Timeout prevents hanging forever.

`response.raise_for_status()`
- Raises exception on HTTP error codes (4xx/5xx).
- This is a fail-fast reliability pattern.

`data_bytes = response.content`
- Reads response payload as raw bytes.

`Path(output_path).write_bytes(data_bytes)`
- Writes raw bytes to file exactly as received.

`log_rows.append({...})`
- Appends metadata dictionary for this dataset.
- Includes dataset name, URL, output path, UTC timestamp, HTTP status, and bytes written.

`datetime.now(timezone.utc).isoformat()`
- Creates ISO-8601 UTC timestamp for provenance.

`print(f"Saved ...")`
- Prints progress feedback to terminal.
- Uses f-string interpolation.

After loop:

`append_log(log_rows)`
- Writes all log entries to CSV.

`print(f"Wrote log -> {LOG_PATH}")`
- Prints final log location.

### Module Entry Point
`if __name__ == "__main__":`
- Runs `run_extract()` only when file is executed directly.
- Does not auto-run when imported from another module.

Python concept:
- Standard Python entry-point guard for reusable scripts.

## Key Python Concepts Used in This Script
1. Imports and modules.
2. Constants and naming conventions.
3. Functions with type hints.
4. Loops and dictionary access.
5. Exception-aware HTTP handling.
6. File I/O with context managers.
7. CSV serialization with DictWriter.
8. Date/time in timezone-aware UTC.
9. f-strings for readable logging.

## Why This Design Is Strong for Portfolio Work
1. Reproducible: config-driven sources and stable output names.
2. Traceable: logged timestamps, statuses, and byte sizes.
3. Robust: directory checks and HTTP error handling.
4. Scalable: adding datasets requires config changes, not logic rewrites.
