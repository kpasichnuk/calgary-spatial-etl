# Calgary Spatial ETL

A Python and PostGIS pipeline that extracts Calgary open-data layers, standardizes their schemas and spatial properties, applies a blocking QA gate, and loads validated layers into PostGIS.

## Pipeline

1. **Extract** downloads configured GeoJSON sources and records provenance in `outputs/logs/extract_log.csv`.
2. **Transform** normalizes fields, IDs, geometry, and CRS, then writes `EPSG:3347` GeoJSON files to `data/processed/`.
3. **QA** checks schema, row presence, IDs, CRS, and geometry quality, then writes `outputs/qa/qa_report.csv`.
4. **Load** writes only QA-approved layers to PostGIS in one transaction and verifies row counts, SRID, and spatial indexes.

## Setup

```bash
conda env create -f environment.yml
conda activate calgary-etl
docker compose up -d
docker compose exec -T postgis psql -U postgres -d postgres < sql/init.sql
```

The local PostGIS service is exposed on port `5433` to avoid conflicts with an existing PostgreSQL installation. Override the default connection without committing credentials:

```bash
export DATABASE_URL='postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE'
```

## Run

Run the complete pipeline:

```bash
python -m src.main
```

Reuse existing raw snapshots:

```bash
python -m src.main --skip-extract
```

Stop after QA:

```bash
python -m src.main --skip-extract --skip-load
```

## Test

Run deterministic tests:

```bash
python -m unittest discover -s tests -v
```

Include isolated PostGIS replacement and rollback tests:

```bash
RUN_POSTGIS_TESTS=1 python -m unittest discover -s tests -v
```

## Learning Resources

Learning material is kept beside the implementation so exercises remain grounded in verified behavior:

- `learning/walkthroughs/`: guided project walkthrough
- `learning/practice/`: progressive practice notebooks for setup, Extract, Transform, QA, and Load
- `learning/assessments/`: retrieval-practice assessment
- `learning/reference/`: line-by-line explanations
- `learning/guides/`: project and library guides
