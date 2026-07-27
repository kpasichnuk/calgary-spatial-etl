from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from pathlib import Path
import csv

import geopandas as gpd

from src.config import DATASETS
from src.transform import ID_FIELDS, KEEP_FIELDS, TARGET_CRS, processed_output_path


REPORT_PATH = Path("outputs/qa/qa_report.csv")


class QualityGateError(RuntimeError):
    """Raised when one or more processed layers fail blocking QA checks."""


@dataclass(frozen=True)
class QAResult:
    dataset: str
    input_path: str
    row_count: int
    missing_field_count: int
    null_geometry_count: int
    empty_geometry_count: int
    invalid_geometry_count: int
    null_id_count: int
    duplicate_id_count: int
    crs: str
    expected_crs: str
    passed: bool
    checked_at_utc: str
    error: str = ""


def inspect_layer(
    dataset_name: str,
    input_path: str | Path,
    expected_fields: list[str],
    id_field: str | None,
    expected_crs: str = TARGET_CRS,
) -> QAResult:
    path = Path(input_path)
    checked_at = datetime.now(timezone.utc).isoformat()

    try:
        if not path.exists():
            raise FileNotFoundError(f"Missing processed file: {path}")

        gdf = gpd.read_file(path)
        missing_fields = [
            field for field in [*expected_fields, gdf.geometry.name]
            if field not in gdf.columns
        ]
        null_geometry_count = int(gdf.geometry.isna().sum())
        empty_geometry_count = int(gdf.geometry.is_empty.sum())
        invalid_geometry_count = int((~gdf.geometry.is_valid).sum())
        null_id_count = int(gdf[id_field].isna().sum()) if id_field in gdf.columns else 0
        duplicate_id_count = (
            int(gdf[id_field].dropna().duplicated().sum())
            if id_field in gdf.columns
            else 0
        )
        crs = str(gdf.crs) if gdf.crs is not None else ""
        error = ""
        if id_field and id_field not in gdf.columns:
            error = f"Missing ID field: {id_field}"

        passed = not any(
            [
                len(gdf) == 0,
                missing_fields,
                null_geometry_count,
                empty_geometry_count,
                invalid_geometry_count,
                null_id_count,
                duplicate_id_count,
                crs != expected_crs,
                error,
            ]
        )

        return QAResult(
            dataset=dataset_name,
            input_path=str(path),
            row_count=len(gdf),
            missing_field_count=len(missing_fields),
            null_geometry_count=null_geometry_count,
            empty_geometry_count=empty_geometry_count,
            invalid_geometry_count=invalid_geometry_count,
            null_id_count=null_id_count,
            duplicate_id_count=duplicate_id_count,
            crs=crs,
            expected_crs=expected_crs,
            passed=passed,
            checked_at_utc=checked_at,
            error=error,
        )
    except (FileNotFoundError, KeyError, OSError, ValueError) as exc:
        return QAResult(
            dataset=dataset_name,
            input_path=str(path),
            row_count=0,
            missing_field_count=len(expected_fields) + 1,
            null_geometry_count=0,
            empty_geometry_count=0,
            invalid_geometry_count=0,
            null_id_count=0,
            duplicate_id_count=0,
            crs="",
            expected_crs=expected_crs,
            passed=False,
            checked_at_utc=checked_at,
            error=str(exc),
        )


def write_report(results: list[QAResult], report_path: str | Path = REPORT_PATH) -> None:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(result) for result in results]

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[field.name for field in fields(QAResult)],
        )
        writer.writeheader()
        writer.writerows(rows)


def run_qa(report_path: str | Path = REPORT_PATH) -> list[QAResult]:
    results = []
    for dataset_name, config in DATASETS.items():
        result = inspect_layer(
            dataset_name=dataset_name,
            input_path=processed_output_path(config["output"]),
            expected_fields=KEEP_FIELDS[dataset_name],
            id_field=ID_FIELDS[dataset_name],
        )
        results.append(result)
        print(
            f"{dataset_name}: rows={result.row_count} "
            f"invalid={result.invalid_geometry_count} "
            f"duplicates={result.duplicate_id_count} passed={result.passed}"
        )

    write_report(results, report_path)
    failures = [result.dataset for result in results if not result.passed]
    if failures:
        raise QualityGateError(f"QA failed for: {', '.join(failures)}")

    print(f"QA passed. Wrote report -> {report_path}")
    return results


if __name__ == "__main__":
    run_qa()
