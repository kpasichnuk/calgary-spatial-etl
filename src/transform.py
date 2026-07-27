from pathlib import Path
from datetime import datetime, timezone
import csv
import re

import geopandas as gpd

from src.config import DATASETS


# Use one target CRS for all layers so spatial operations are consistent.
TARGET_CRS = "EPSG:3347"

# Optional field subsets by dataset (use normalized names).
# Edit these lists as you learn the exact source schema.
KEEP_FIELDS = {
    "communities": [
        "comm_code",
        "name",
        "class",
        "class_code",
        "sector",
    ],
    "roads": [
        "segment_id",
        "full_name",
        "street_type",
        "class_code",
        "one_way",
        "built_status",
    ],
    "transit_stops": [
        "teleride_number",
        "stop_name",
        "status",
        "globalid",
    ],
    "land_use_districts": [
        "lu_code",
        "label",
        "description",
        "major",
    ],
}

# If an ID field exists, cast it to string to avoid downstream join/type issues.
ID_FIELDS = {
    "communities": "comm_code",
    "roads": "segment_id",
    "transit_stops": "globalid",
    "land_use_districts": None,
}

LOG_PATH = Path("outputs/logs/transform_log.csv")


def normalize_col_name(name: str) -> str:
    # Convert to lowercase snake_case for predictable coding/SQL.
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name


def normalize_columns(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf.columns = [normalize_col_name(c) for c in gdf.columns]
    return gdf


def processed_output_path(raw_output_path: str) -> Path:
    # Convert data/raw/<file> to data/processed/<file>.
    return Path(raw_output_path.replace("data/raw/", "data/processed/"))


def keep_required_fields(
    gdf: gpd.GeoDataFrame, keep_fields: list[str]
 ) -> tuple[gpd.GeoDataFrame, list[str]]:
    gdf = gdf.copy()
    missing = []

    # Ensure expected fields exist; create null fields if missing.
    for field in keep_fields:
        if field not in gdf.columns:
            gdf[field] = None
            missing.append(field)

    return gdf[keep_fields + ["geometry"]], missing


def cast_id_to_string(gdf: gpd.GeoDataFrame, id_field: str | None) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    if id_field and id_field in gdf.columns:
        gdf[id_field] = gdf[id_field].astype("string")
    return gdf


def repair_geom(geom):
    # Try make_valid first; fallback to buffer(0) for compatibility.
    try:
        from shapely import make_valid

        return make_valid(geom)
    except Exception:
        try:
            return geom.buffer(0)
        except Exception:
            return None


def clean_geometry(gdf: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, int, int]:
    gdf = gdf.copy()

    # Remove null and empty geometries before validation.
    gdf = gdf[gdf.geometry.notnull()]
    gdf = gdf[~gdf.geometry.is_empty]

    invalid_before = int((~gdf.is_valid).sum())

    if invalid_before > 0:
        mask = ~gdf.is_valid
        gdf.loc[mask, "geometry"] = gdf.loc[mask, "geometry"].apply(repair_geom)

    # Drop anything still invalid/null/empty after repair attempts.
    gdf = gdf[gdf.geometry.notnull()]
    gdf = gdf[~gdf.geometry.is_empty]
    gdf = gdf[gdf.is_valid]

    invalid_after = int((~gdf.is_valid).sum())
    return gdf, invalid_before, invalid_after


def ensure_crs_and_reproject(gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
    gdf = gdf.copy()

    # Calgary GeoJSON is typically EPSG:4326. Set only when missing.
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")

    return gdf.to_crs(target_crs)


def append_transform_log(rows: list[dict]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_PATH.exists()

    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dataset",
                "input_path",
                "output_path",
                "rows_in",
                "rows_out",
                "missing_fields",
                "invalid_before",
                "invalid_after",
                "crs_out",
                "processed_at_utc",
                "status",
                "error",
            ],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)


def process_dataset(dataset_name: str, cfg: dict) -> dict:
    input_path = cfg["output"]
    output_path = processed_output_path(input_path)

    row = {
        "dataset": dataset_name,
        "input_path": input_path,
        "output_path": str(output_path),
        "rows_in": 0,
        "rows_out": 0,
        "missing_fields": "",
        "invalid_before": 0,
        "invalid_after": 0,
        "crs_out": TARGET_CRS,
        "processed_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "error": "",
    }

    try:
        if not Path(input_path).exists():
            raise FileNotFoundError(f"Missing raw file: {input_path}")

        gdf = gpd.read_file(input_path)
        row["rows_in"] = len(gdf)

        gdf = normalize_columns(gdf)

        keep_fields = KEEP_FIELDS.get(dataset_name, [])
        keep_fields = [f for f in keep_fields if f != "geometry"]
        if keep_fields:
            gdf, missing = keep_required_fields(gdf, keep_fields)
            row["missing_fields"] = ",".join(missing)

        id_field = ID_FIELDS.get(dataset_name)
        gdf = cast_id_to_string(gdf, id_field)

        gdf, invalid_before, invalid_after = clean_geometry(gdf)
        row["invalid_before"] = invalid_before
        row["invalid_after"] = invalid_after

        gdf = ensure_crs_and_reproject(gdf, TARGET_CRS)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        gdf.to_file(output_path, driver="GeoJSON")
        row["rows_out"] = len(gdf)

        print(
            f"{dataset_name}: rows_in={row['rows_in']} rows_out={row['rows_out']} "
            f"invalid_before={invalid_before} invalid_after={invalid_after} "
            f"crs={TARGET_CRS} -> {output_path}"
        )

    except Exception as exc:
        row["status"] = "error"
        row["error"] = str(exc)
        print(f"{dataset_name}: ERROR -> {exc}")

    return row


def run_transform() -> None:
    # Run the same transform pipeline for each configured dataset.
    log_rows = []
    for dataset_name, cfg in DATASETS.items():
        log_rows.append(process_dataset(dataset_name, cfg))

    append_transform_log(log_rows)
    print(f"Wrote log -> {LOG_PATH}")


if __name__ == "__main__":
    # Allow direct execution: python -m src.transform
    run_transform()