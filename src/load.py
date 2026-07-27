from dataclasses import dataclass
from pathlib import Path
import os
import re

import geopandas as gpd
from sqlalchemy import Engine, create_engine, text

from src.config import DATASETS
from src.qa import run_qa
from src.transform import processed_output_path


DEFAULT_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5433/calgary_gis"
)
DEFAULT_SCHEMA = "public"
_IDENTIFIER_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")


@dataclass(frozen=True)
class LoadResult:
    dataset: str
    table_name: str
    source_rows: int
    loaded_rows: int
    srid: int
    spatial_index_present: bool


def validate_identifier(value: str, kind: str) -> str:
    if not _IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(f"Invalid {kind}: {value!r}")
    return value


def database_url_from_environment() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def load_layer(
    connection,
    dataset_name: str,
    input_path: str | Path,
    schema: str = DEFAULT_SCHEMA,
) -> LoadResult:
    table_name = validate_identifier(dataset_name, "table name")
    schema_name = validate_identifier(schema, "schema name")
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Missing QA-approved file: {path}")

    gdf = gpd.read_file(path)
    if gdf.crs is None:
        raise ValueError(f"{dataset_name}: cannot load data without a CRS")

    gdf.to_postgis(
        name=table_name,
        con=connection,
        schema=schema_name,
        if_exists="replace",
        index=False,
    )

    loaded_rows = connection.execute(
        text(f'SELECT COUNT(*) FROM "{schema_name}"."{table_name}"')
    ).scalar_one()
    srid = connection.execute(
        text(
            f'SELECT ST_SRID(geometry) FROM "{schema_name}"."{table_name}" '
            "WHERE geometry IS NOT NULL LIMIT 1"
        )
    ).scalar_one_or_none()
    spatial_index_present = bool(
        connection.execute(
            text(
                "SELECT EXISTS ("
                "SELECT 1 FROM pg_indexes "
                "WHERE schemaname = :schema AND tablename = :table "
                "AND indexdef ILIKE '%USING gist%geometry%'"
                ")"
            ),
            {"schema": schema_name, "table": table_name},
        ).scalar_one()
    )

    result = LoadResult(
        dataset=dataset_name,
        table_name=table_name,
        source_rows=len(gdf),
        loaded_rows=int(loaded_rows),
        srid=int(srid or 0),
        spatial_index_present=spatial_index_present,
    )
    if result.loaded_rows != result.source_rows:
        raise RuntimeError(
            f"{dataset_name}: loaded {result.loaded_rows} of {result.source_rows} rows"
        )
    if result.srid <= 0:
        raise RuntimeError(f"{dataset_name}: loaded geometry has no valid SRID")
    if not result.spatial_index_present:
        raise RuntimeError(f"{dataset_name}: spatial index was not created")

    return result


def run_load(
    database_url: str | None = None,
    schema: str = DEFAULT_SCHEMA,
    engine: Engine | None = None,
    require_qa: bool = True,
) -> list[LoadResult]:
    if require_qa:
        run_qa()

    active_engine = engine or create_engine(
        database_url or database_url_from_environment(),
        pool_pre_ping=True,
    )
    owns_engine = engine is None

    try:
        results = []
        with active_engine.begin() as connection:
            for dataset_name, config in DATASETS.items():
                result = load_layer(
                    connection=connection,
                    dataset_name=dataset_name,
                    input_path=processed_output_path(config["output"]),
                    schema=schema,
                )
                results.append(result)
                print(
                    f"{dataset_name}: loaded={result.loaded_rows} "
                    f"srid={result.srid} spatial_index={result.spatial_index_present}"
                )
        return results
    finally:
        if owns_engine:
            active_engine.dispose()


if __name__ == "__main__":
    run_load()
