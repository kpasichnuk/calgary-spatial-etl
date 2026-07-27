# Calgary Spatial ETL: Big-Picture Project Guide

## 1. Project Summary

This project is a reproducible spatial ETL pipeline for four City of Calgary open-data layers:

- communities
- roads
- transit stops
- land-use districts

The pipeline downloads source GeoJSON, preserves raw snapshots, standardizes the data, enforces spatial and attribute quality rules, and loads approved layers into PostGIS. It also records operational logs and QA results so a run can be inspected afterward.

The production sequence is:

1. Set up the Python environment.
2. Set up Git and review the repository state.
3. Start and initialize PostGIS.
4. Extract source data.
5. Transform raw data.
6. run QA/QC as a blocking gate.
7. Load approved data into PostGIS.
8. Verify the database and generated artifacts.
9. Run automated tests.
10. Review and commit intentional source changes.

The central rule is that each stage has a clear input, output, and responsibility. Later stages should not silently repair failures that belong to earlier stages.

### Current Verification Status

As of July 27, 2026, the project is **complete and operational for its defined local project scope**. A fresh run using the current Calgary sources completed Extract, Transform, QA, and Load successfully. The full automated suite also passed, including the live PostGIS replacement and transaction-rollback tests.

| Layer | Extracted/transformed/loaded rows | QA | PostGIS SRID | GIST geometry index |
|---|---:|---|---:|---|
| communities | 313 | passed | 3347 | present |
| roads | 19,385 | passed | 3347 | present |
| transit stops | 7,748 | passed | 3347 | present |
| land-use districts | 10,351 | passed | 3347 | present |

The land-use source contained 43 invalid geometries in this run. Transform repaired them, and QA independently confirmed zero invalid geometries remained.

This is not the same as a production deployment guarantee. Current boundaries include:

- a public GitHub remote is configured, but there is no CI pipeline, scheduler, alerting service, or production hosting
- reliance on live Calgary API availability and a working local Docker service
- local development credentials in the default Docker configuration; nonlocal credentials must come from secure environment configuration
- full-snapshot table replacement rather than incremental loading or upsert history
- no generalized extraction retry, pagination, rate-limit, or schema-drift framework
- Transform records individual dataset errors; operators must review stage status and avoid relying on stale processed files after a failed dataset transformation

## 2. What the Project Produces

| Stage | Main input | Main output | Why it exists |
|---|---|---|---|
| Environment | `environment.yml` | `calgary-etl` Conda environment | Reproduces the Python and GIS toolchain |
| Git | Working tree | Versioned source history | Tracks intentional changes and supports recovery |
| Database setup | `docker-compose.yml`, `sql/init.sql` | Local PostGIS database | Provides the spatial database destination |
| Extract | Dataset URLs in `src/config.py` | `data/raw/*.geojson`, extract log | Captures source snapshots and provenance |
| Transform | Raw GeoJSON | `data/processed/*.geojson`, transform log | Produces consistent, analysis-ready layers |
| QA/QC | Processed GeoJSON | `outputs/qa/qa_report.csv` | Prevents unacceptable data from loading |
| Load | QA-approved GeoJSON | PostGIS tables | Publishes queryable spatial data transactionally |
| Tests | Test fixtures and PostGIS | Pass/fail results | Checks important behavior repeatedly |

Generated data, logs, reports, caches, local settings, and secrets are intentionally excluded from Git. Source code, tests, SQL, environment definitions, documentation, and learning material belong in Git.

## 3. Repository Map

| Location | Responsibility |
|---|---|
| `src/config.py` | Dataset names, source URLs, and raw output paths |
| `src/extract.py` | Source download and provenance logging |
| `src/transform.py` | Schema, ID, geometry, and CRS standardization |
| `src/qa.py` | Blocking quality checks and QA reporting |
| `src/load.py` | Transactional PostGIS loading and verification |
| `src/main.py` | Correct stage order and command-line options |
| `tests/` | Deterministic QA tests and opt-in PostGIS integration tests |
| `sql/init.sql` | Database creation and PostGIS extension setup |
| `data/raw/` | Immutable inputs for a particular run |
| `data/processed/` | Standardized outputs ready for QA |
| `outputs/logs/` | Extract and Transform run records |
| `outputs/qa/` | Machine-readable QA results |
| `learning/` | Guides, walkthroughs, assessments, and practice notebooks |

## 4. Correct Start-to-Finish Order

### Step 1: Understand the Data Contract

Before running or changing the pipeline, identify:

- which datasets are expected
- where each source comes from
- which attributes are retained
- which field acts as an identifier
- which CRS all processed layers must use
- which quality failures must block publication
- which PostGIS schema and tables are expected

This project configures four datasets and standardizes them to `EPSG:3347`, a projected CRS suitable for Canada-wide mapping and metric spatial work.

Important concepts:

- **Data contract:** the expected shape and meaning of data at a stage boundary.
- **Schema:** field names, field types, geometry column, and related constraints.
- **Provenance:** where data came from, when it was retrieved, and what was written.
- **CRS:** the coordinate reference system that gives coordinates their spatial meaning.
- **Idempotency:** repeating an operation produces the intended current state rather than duplicate accumulation.

### Step 2: Create the Python Environment

From the repository root:

```bash
conda env create -f environment.yml
conda activate calgary-etl
```

If the environment already exists, activate it and update it when the dependency definition changes:

```bash
conda env update -f environment.yml --prune
```

Purpose:

- isolate project dependencies from system Python
- install compatible compiled GIS libraries through Conda Forge
- make setup repeatable on another machine
- give VS Code and Jupyter a known interpreter

Important concepts:

- **Interpreter:** the Python executable that runs the project.
- **Environment isolation:** each project controls its own package versions.
- **Dependency declaration:** `environment.yml` describes the required runtime instead of relying on one machine's accidental state.
- **Compiled geospatial stack:** GeoPandas depends on libraries such as Shapely, PROJ, Fiona, and database drivers that must work together.
- **Reproducibility:** another developer can recreate the toolchain from a tracked definition.

Confirm the active environment and key imports before diagnosing pipeline logic:

```bash
which python
python --version
python -c "import geopandas, shapely, sqlalchemy, geoalchemy2, psycopg2; print('imports ok')"
```

### Step 3: Establish the Git Workflow

Git should be initialized before development so every intentional source change has history. In this repository, Git is already initialized on `main`.

Start every work session with:

```bash
git status
git log -1 --oneline
git remote -v
```

Purpose:

- know the branch and current baseline
- detect unsaved versus saved repository changes
- keep generated outputs and credentials out of history
- create reviewable snapshots at meaningful milestones
- support comparison, rollback, collaboration, and GitHub publication

Important concepts:

- **Working tree:** saved files as they currently exist.
- **Staging area:** the exact proposed content for the next commit.
- **Commit:** a named, immutable project snapshot with parent history.
- **Branch:** a movable reference to a sequence of commits.
- **Remote:** a named connection to another Git repository, commonly GitHub.
- **`.gitignore`:** patterns for untracked files Git should not offer for staging.
- **Tracked versus generated:** source definitions belong in history; reproducible outputs usually do not.

A disciplined change cycle is:

```bash
git status
git diff
# run the relevant tests
git add <intentional-files>
git diff --cached
git commit -m "Describe the completed change"
git push
```

Do not commit `.env`, passwords, access tokens, raw downloads, processed outputs, logs, QA reports, caches, or local editor state. `.gitignore` does not remove a file that was already tracked.

### Step 4: Start and Initialize PostGIS

Start the containerized database:

```bash
docker compose up -d
docker compose ps
```

Initialize the project database and spatial extensions:

```bash
docker compose exec -T postgis psql -U postgres -d postgres < sql/init.sql
```

Purpose:

- provide PostgreSQL without requiring a machine-wide manual installation
- enable PostGIS spatial types, functions, and indexes
- create the `calgary_gis` database consistently
- keep database infrastructure separate from Python application logic

Important concepts:

- **Container:** an isolated service created from a versioned image.
- **Image versus container:** the image is the template; the container is the running instance.
- **Port mapping:** host port `5433` forwards to PostgreSQL port `5432` inside the container.
- **Volume:** persistent database storage that survives container recreation.
- **Extension:** PostGIS adds spatial capabilities to PostgreSQL.
- **Connection URL:** identifies the driver, credentials, host, port, and database.

The project supports a `DATABASE_URL` environment variable. Credentials belong in environment configuration, never committed source files.

### Step 5: Extract

Run only Extract:

```bash
python -m src.extract
```

Purpose:

- download each configured Calgary GeoJSON source
- fail on unsuccessful HTTP responses
- write stable raw filenames
- preserve a raw snapshot for repeatable downstream work
- record source URL, retrieval time, HTTP status, and byte count

Important concepts:

- **HTTP request and response:** the client requests a URL and validates the server response.
- **Timeout:** prevents a request from waiting forever.
- **Status validation:** unsuccessful HTTP status codes must become visible failures.
- **Raw-data immutability:** transformations should create new outputs instead of rewriting evidence of what was received.
- **Stable paths:** predictable filenames allow later stages to find inputs.
- **Provenance logging:** a run record makes source retrieval auditable.
- **Configuration-driven iteration:** all datasets follow one process defined by shared configuration.

Extract depends on the external Calgary service and network. A failure here is not automatically a Transform failure. Check the URL, status, network, and partial files before proceeding.

### Step 6: Transform

Run only Transform:

```bash
python -m src.transform
```

Purpose:

- read raw GeoJSON into GeoDataFrames
- normalize column names to predictable SQL-friendly names
- retain the intended attributes and active geometry
- create expected nullable fields when a source field is absent and report that fact
- normalize identifier types
- remove unusable geometries and attempt repairs
- reproject every layer to `EPSG:3347`
- write processed GeoJSON and a transform log

Important concepts:

- **GeoDataFrame:** a table with an active geometry column and CRS metadata.
- **Vector geometry:** points, lines, and polygons represent different spatial phenomena.
- **Attribute normalization:** predictable lowercase snake-case names reduce downstream ambiguity.
- **Field selection:** retaining only required fields makes the output contract explicit.
- **Data type normalization:** IDs are labels, not quantities, even when they contain digits.
- **Null geometry:** no geometry value exists.
- **Empty geometry:** a geometry object exists but contains no coordinates.
- **Invalid geometry:** coordinates violate geometry validity rules, such as a self-intersecting polygon.
- **Geometry repair:** attempt a controlled repair, then remove features that still cannot satisfy the contract.
- **Assigning versus transforming a CRS:** assigning declares what existing coordinates mean; transforming calculates coordinates in another CRS.
- **Projected CRS:** supports meaningful metric distance and area operations better than longitude/latitude.
- **Copy semantics:** transformations should avoid unintentionally mutating caller-owned data.

The transform log should be reviewed for row loss, missing fields, repaired geometries, final CRS, and any per-dataset error. A stage printing an error is not equivalent to a successful pipeline, even if other datasets continue processing.

### Step 7: QA/QC Quality Gate

Run QA independently:

```bash
python -m src.qa
```

Purpose:

- independently inspect processed outputs
- verify every expected file exists
- require at least one row
- require the expected fields and geometry column
- reject null, empty, or invalid geometries
- reject null or duplicate configured IDs
- require the target CRS
- write one QA report
- stop the pipeline when any layer fails

Important concepts:

- **QA versus QC:** QA defines and improves the process that prevents defects; QC inspects outputs for actual defects. This stage contains practical elements of both.
- **Quality gate:** a blocking decision between preparation and publication.
- **Independent validation:** QA reopens outputs rather than trusting Transform's claims.
- **Completeness:** required files, fields, IDs, and rows are present.
- **Validity:** geometry and CRS satisfy technical rules.
- **Uniqueness:** identifiers do not ambiguously describe multiple features.
- **Actionable reporting:** failures include counts and messages that guide diagnosis.
- **Deterministic check:** the same input and rule produce the same pass/fail result.

QA should not silently repair data. Repair belongs in Transform; QA confirms whether Transform produced acceptable results.

### Step 8: Load

Run only Load:

```bash
python -m src.load
```

Purpose:

- rerun QA by default before database access
- load every approved processed layer into PostGIS
- replace each target table so reruns do not append duplicates
- perform the set of loads in one transaction
- verify source and database row counts match
- verify loaded geometry has an SRID
- verify a GIST spatial index exists

Important concepts:

- **Database schema:** a namespace containing related tables; production defaults to `public`.
- **Spatial table:** attributes plus a database geometry column with spatial metadata.
- **Transaction:** all table changes commit together or roll back together on failure.
- **Atomicity:** users do not receive a knowingly partial multi-layer publication.
- **Replace semantics:** rerunning refreshes current tables instead of duplicating rows.
- **SRID:** the numeric database identifier for a spatial reference system.
- **GIST index:** accelerates spatial filtering and relationship queries.
- **Post-load reconciliation:** compare expected and actual database state rather than assuming a write succeeded.
- **Identifier validation:** table and schema names are constrained before being used in SQL identifiers.

The load is successful only when the transaction commits and every layer passes row-count, SRID, and index verification.

### Step 9: Run the Orchestrated Pipeline

Run everything in production order:

```bash
python -m src.main
```

Reuse current raw snapshots but rerun all downstream stages:

```bash
python -m src.main --skip-extract
```

Validate through QA without publishing to PostGIS:

```bash
python -m src.main --skip-extract --skip-load
```

Purpose:

- give operators one correct entry point
- prevent accidental stage reordering
- expose deliberate skip options
- record elapsed time for each completed stage

The dependency chain is:

```text
Calgary API
    -> raw GeoJSON
    -> processed GeoJSON in EPSG:3347
    -> blocking QA report
    -> transactional PostGIS tables
```

Git and environment setup support the pipeline but are not data-processing stages. Tests verify the pipeline but do not replace operating it with real data.

### Step 10: Test and Verify

Run deterministic tests:

```bash
python -m unittest discover -s tests -v
```

Run all tests, including live PostGIS integration checks:

```bash
RUN_POSTGIS_TESTS=1 python -m unittest discover -s tests -v
```

Purpose:

- prove known-good QA inputs pass
- prove duplicate IDs fail
- prove missing files produce actionable failures
- prove repeat loads replace rather than duplicate
- prove a failed database transaction rolls back table creation

Important concepts:

- **Unit test:** isolates a small behavior with controlled inputs.
- **Integration test:** verifies components working together, such as GeoPandas, SQLAlchemy, and PostGIS.
- **Fixture:** controlled test data or setup.
- **Assertion:** an expected result that determines pass or fail.
- **Isolation:** integration tests use a separate schema and clean it up.
- **Regression protection:** previously verified behavior is checked after future changes.
- **Happy path and failure path:** both successful operation and safe failure matter.

Operational verification should also inspect:

- Extract and Transform logs
- the QA report
- processed file counts and CRS
- PostGIS table row counts
- geometry SRIDs
- spatial indexes
- command exit status

### Step 11: Review and Commit

After documentation, code, or test changes:

1. Run the narrowest relevant test.
2. Run broader tests when shared behavior changed.
3. Inspect `git status` and `git diff`.
4. Stage only intentional source changes.
5. Inspect `git diff --cached`.
6. Scan for secrets and generated data.
7. Commit one coherent completed change.
8. Push only after confirming the remote and branch.

Do not commit merely because the pipeline generated new output files. Commit changes to the definitions that make the system reproducible.

## 5. How the Stages Depend on One Another

| If this fails | Do not continue to | Investigate first |
|---|---|---|
| Environment | Any Python stage | Interpreter and dependency installation |
| Git review | Editing or committing | Branch, dirty files, ignored files, and secrets |
| PostGIS setup | Load or integration tests | Container, port, database, extensions, URL |
| Extract | Transform with a new snapshot | HTTP response, URL, network, raw files, extract log |
| Transform | QA or Load | schema, geometry, CRS, row loss, transform log |
| QA | Load | each failed metric and the responsible Transform rule |
| Load | Publication complete | transaction error, row reconciliation, SRID, index |
| Tests | Commit as verified | whether the failure is related to the intended change |

This ordering protects the meaning of the data. For example, loading first and checking later could publish invalid layers. Repairing data during QA would hide whether Transform is reliable. Editing raw files would destroy provenance.

## 6. Completion Criteria

The implementation is complete when all of the following are true:

- the environment can be recreated from `environment.yml`
- all four sources can be extracted to stable raw paths
- all four raw layers transform to the expected schema and `EPSG:3347`
- the QA gate passes valid processed layers and blocks invalid ones
- all four layers load in one PostGIS transaction
- loaded counts match source counts
- loaded geometry has a valid SRID
- each table has a GIST geometry index
- repeat loading does not duplicate data
- forced transaction failure rolls back
- automated tests pass
- setup, execution, and learning documentation exist
- secrets and generated artifacts remain outside Git history

External source availability, Docker availability, and credentials are runtime prerequisites, not properties the repository can permanently guarantee. Completion should therefore be reconfirmed with tests and a current pipeline run.

## 7. Practical Mental Model

Use this question at every boundary:

> What am I accepting, what guarantee am I adding, and what evidence proves it?

| Boundary | Accepted input | Guarantee added | Evidence |
|---|---|---|---|
| Extract output | Remote API response | Stable raw snapshot with provenance | Raw files and extract log |
| Transform output | Raw source structure | Standard schema, geometry, IDs, and CRS | Processed files and transform log |
| QA output | Processed candidate | Explicit pass against blocking rules | QA report and successful exit |
| Load output | QA-approved layers | Atomic spatial database publication | Counts, SRID, indexes, committed transaction |
| Git commit | Reviewed working change | Recoverable, attributable project snapshot | Staged diff and commit history |

That model is the big picture: each step reduces uncertainty and leaves evidence for the next person or the next run.