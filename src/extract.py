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