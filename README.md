# Calgary Spatial ETL

A Python and PostGIS pipeline that extracts Calgary open-data layers, standardizes their schemas and spatial properties, applies a blocking QA gate, and loads validated layers into PostGIS.

> Contains information licensed under the Open Government Licence – City of Calgary.

See [References and Attribution](REFERENCES.md) for the source datasets, licence terms, geospatial standards, and software documentation used by this project.

## Pipeline

1. **Extract** downloads configured GeoJSON sources and records provenance in `outputs/logs/extract_log.csv`.
2. **Transform** normalizes fields, IDs, geometry, and CRS, then writes `EPSG:3347` GeoJSON files to `data/processed/`.
3. **QA** checks schema, row presence, IDs, CRS, and geometry quality, then writes `outputs/qa/qa_report.csv`.
4. **Load** writes only QA-approved layers to PostGIS in one transaction and verifies row counts, SRID, and spatial indexes.

## Spatial Analysis Extension

Project 1 now includes a structured [spatial analysis extension](analysis/README.md) that uses QA-approved communities and transit stops to study mapped stop density by community.

The extension develops spatial intuition alongside Python and PostGIS skills: question framing, units and scale, CRS and measurement, spatial joins, normalization, validation, interpretation, and responsible communication. Its initial result is a screening comparison, not a claim about transit accessibility, equity, demand, or service quality.

The analysis curriculum begins after the core ETL modules and includes references, clean practice notebooks, 25-point module tests, concept notes, and an implementation/testing boundary for the eventual reproducible case study.

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
- `learning/starters/`: clean, version-controlled practice notebook originals
- `learning/working/`: ignored local copies used while completing exercises
- `learning/attempts/`: completed notebooks preserved for review or portfolio evidence
- `learning/assessments/`: retrieval-practice assessment
- `learning/reference/`: line-by-line explanations
- `learning/guides/`: project and library guides

Start with the [Project 1 learning resource index](learning/README.md), or use the core sequence directly:

- [Project study guide](learning/guides/project1_study_guide.md)
- [ETL walkthrough](learning/walkthroughs/project1_etl_walkthrough.ipynb)
- [Big-picture project guide](learning/guides/project1_big_picture_guide.md)
- [Big-picture assessment](learning/assessments/project1_big_picture_assessment.ipynb)

## Portfolio Roadmap

The [portfolio planning index](planning/README.md) records the longer-term path from this ETL project to a separate spatial API, web GIS application, and deeper analysis case study.

Projects 2 and 3 are intentionally not created yet. The plan defines readiness gates and explains why each future project should remain an independent repository. When Project 2 begins, a portfolio-level VS Code multi-root workspace can group the sibling repositories without merging their Git histories, environments, or deployments.
