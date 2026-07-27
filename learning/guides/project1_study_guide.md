# Calgary Spatial ETL Study Guide

## How to Use This Guide

This guide helps you learn the project well enough to explain it, operate it, and diagnose failures. It is not a line-by-line code explanation.

Use this cycle for each section:

1. Read the overview once.
2. Close the guide and explain the stage aloud.
3. Write its input, responsibility, output, and evidence from memory.
4. Run the relevant command or practice notebook.
5. Answer the review questions without notes.
6. Revisit weak sections after one day and again after one week.

Use these companion resources in order:

1. [Project 1 study guide](project1_study_guide.md) to learn the concepts.
2. [Project 1 ETL walkthrough](../walkthroughs/project1_etl_walkthrough.ipynb) to observe the workflow.
3. The stage workbooks listed in the [Project 1 learning resource index](../README.md) to practice individual skills.
4. [Project 1 big-picture assessment](../assessments/project1_big_picture_assessment.ipynb) to test cumulative understanding.
5. [Project 1 big-picture guide](project1_big_picture_guide.md) as the detailed operational reference.

## The One-Sentence Project Explanation

The Calgary Spatial ETL project downloads four Calgary open-data layers, preserves their raw snapshots, standardizes their schemas and spatial properties, blocks unacceptable data with QA/QC, and transactionally publishes verified layers to PostGIS.

## The Complete Order

Memorize this sequence:

```text
Understand the contract
    -> create and activate the environment
    -> inspect Git state
    -> start and initialize PostGIS
    -> Extract
    -> Transform
    -> QA/QC
    -> Load
    -> post-load verification
    -> automated tests
    -> review and commit source changes
```

Environment, Git, database setup, tests, and documentation support the ETL process. The actual data-processing stages are Extract, Transform, QA/QC, and Load.

## The Core Mental Model

At every stage, ask four questions:

1. **Input:** What does this stage accept?
2. **Responsibility:** What uncertainty or defect does it address?
3. **Output:** What does it produce for the next stage?
4. **Evidence:** How can I prove it succeeded?

| Stage | Input | Responsibility | Output | Evidence |
|---|---|---|---|---|
| Extract | Calgary API responses | Capture source data and provenance | Raw GeoJSON | Raw files and extract log |
| Transform | Raw GeoJSON | Standardize schema, IDs, geometry, and CRS | Processed GeoJSON | Transform log and processed files |
| QA/QC | Processed GeoJSON | Independently enforce acceptance rules | Pass/fail report | QA report and successful exit |
| Load | QA-approved layers | Publish an atomic database snapshot | PostGIS tables | Counts, SRID, GIST indexes, commit |

## 1. Project Contract and Architecture

### What to Know

The project processes four datasets:

- communities
- roads
- transit stops
- land-use districts

The common processed CRS is `EPSG:3347`. Each dataset has a configured source URL, raw output path, selected fields, and optional identifier field.

The architecture separates responsibilities:

- `src/config.py` defines dataset configuration.
- `src/extract.py` retrieves source data.
- `src/transform.py` standardizes it.
- `src/qa.py` decides whether it is acceptable.
- `src/load.py` publishes approved data.
- `src/main.py` controls the correct order.
- `tests/` verifies important behavior.

### Key Terms

- **Data contract:** the required form and meaning of data at a boundary.
- **Schema:** fields, types, geometry, and related constraints.
- **Pipeline:** connected stages that move data toward a defined result.
- **Configuration:** values that describe behavior without duplicating processing logic.
- **Separation of concerns:** each module owns one clear responsibility.

### Check Your Understanding

1. Why does every processed layer use one target CRS?
2. Why should dataset URLs live in configuration rather than be repeated throughout the code?
3. What is the difference between a module and a pipeline stage?
4. What guarantee must exist before Load begins?

## 2. Python Environment and Dependencies

### Purpose

The environment makes the Python and geospatial toolchain reproducible and isolated from unrelated projects.

### Commands to Recognize

```bash
conda env create -f environment.yml
conda activate calgary-etl
conda env update -f environment.yml --prune
which python
python --version
```

### What to Know

- The **interpreter** is the Python executable running the code.
- A **Conda environment** isolates Python and installed packages.
- `environment.yml` declares the environment another developer should be able to recreate.
- An installed package proves only that it exists on the current machine.
- A declared dependency records that the project requires it.
- VS Code and Jupyter must use the intended `calgary-etl` interpreter or kernel.
- GIS packages depend on compiled libraries such as GEOS, PROJ, and GDAL-related components.
- Environment variables provide runtime configuration without hard-coding secrets.

### Important Libraries

| Library | Role |
|---|---|
| GeoPandas | Tabular and vector spatial data operations |
| Shapely | Geometry objects, validity, and repair |
| PyProj/PROJ | CRS definitions and coordinate transformations |
| Fiona | Vector file access used by the geospatial stack |
| Requests | HTTP extraction |
| SQLAlchemy | Database engines, connections, SQL, and transactions |
| GeoAlchemy2 | Spatial database integration |
| psycopg2 | PostgreSQL driver |

### Common Mistakes

- Installing a package into one environment while running another interpreter.
- Assuming a notebook kernel changed because a terminal environment changed.
- Committing passwords in source code or notebooks.
- Debugging pipeline logic before confirming imports and the interpreter.
- Updating packages manually without updating the dependency definition.

### Check Your Understanding

1. What is the difference between Python, an interpreter, an environment, and a package?
2. Why can `pip install` appear successful while an import still fails in a notebook?
3. Why is `environment.yml` tracked in Git while the environment directory is not?
4. Where should `DATABASE_URL` be supplied?

## 3. Git and Version Control

### Purpose

Git records intentional changes to the definitions that make the project reproducible. It does not replace backups for every generated artifact, and it cannot see unsaved editor changes.

### The Four States to Distinguish

1. **Editor buffer:** changes currently visible but possibly not saved.
2. **Working tree:** saved files on disk.
3. **Staging area:** the proposed contents of the next commit.
4. **Commit:** an immutable snapshot in repository history.

### Daily Workflow

```bash
git status
git diff
# make and test the change
git add <intentional-files>
git diff --cached
git commit -m "Describe the completed change"
git push
```

### What Belongs in Git

Track:

- source code
- tests
- SQL definitions
- environment and dependency definitions
- documentation and learning material
- nonsecret configuration examples

Ignore:

- raw and processed downloads
- generated logs and QA reports
- `.env` and credentials
- caches and virtual environments
- local editor settings
- notebook checkpoints

### Key Terms

- **Repository:** project files plus Git history.
- **Commit:** a reviewed snapshot.
- **Branch:** a movable name pointing to a line of commits.
- **Remote:** a named connection to another repository.
- **Pull request:** a review and collaboration workflow around proposed commits.
- **Merge conflict:** competing changes Git cannot combine automatically.
- **`.gitignore`:** rules for untracked files that should normally remain outside Git.

### Common Mistakes

- Using `git add .` without reviewing what it stages.
- Assuming `.gitignore` removes an already tracked file.
- Committing generated data or credentials.
- Force-pushing without understanding shared history.
- Resolving a conflict by discarding another person's work.
- Confusing an unsaved notebook edit with a Git modification.

### Check Your Understanding

1. What does `git diff --cached` show?
2. Why should you test before committing?
3. Why are raw GeoJSON files ignored while `src/config.py` is tracked?
4. What should you inspect before pushing?
5. What must happen if a real credential enters Git history?

## 4. Docker and PostGIS Setup

### Purpose

Docker provides a repeatable PostgreSQL/PostGIS service. PostGIS is the destination that stores and spatially indexes approved layers.

### Commands to Recognize

```bash
docker compose up -d
docker compose ps
docker compose exec -T postgis psql -U postgres -d postgres < sql/init.sql
```

### What to Know

- An **image** is the service template.
- A **container** is a running image instance.
- A **volume** preserves database data outside the disposable container layer.
- Host port `5433` maps to PostgreSQL port `5432` inside the container.
- `sql/init.sql` creates `calgary_gis` and enables PostGIS extensions.
- A database URL includes driver, credentials, host, port, and database.
- Local development credentials are not suitable production credentials.

### Common Mistakes

- Connecting to port `5432` when this project exposes `5433`.
- Starting Docker but not initializing the project database.
- Assuming container startup proves PostGIS extensions exist.
- Running database tests against the wrong database or schema.
- Storing a production password in `docker-compose.yml` or source code.

### Check Your Understanding

1. Why are both Docker Compose and `sql/init.sql` needed?
2. What persists when a container is recreated?
3. What does the port mapping mean?
4. Why is PostGIS more than ordinary PostgreSQL?

## 5. Extract

### Purpose

Extract retrieves source data without changing its meaning and records enough provenance to understand what was received.

### Project Behavior

- Reads dataset URLs and output paths from configuration.
- Sends HTTP requests with a timeout.
- raises an error for unsuccessful HTTP status codes.
- Writes stable files under `data/raw/`.
- Records URL, destination, UTC time, status, and byte count.

### Key Concepts

- **HTTP status:** indicates whether the server fulfilled the request.
- **Timeout:** limits how long the client waits.
- **Provenance:** source, retrieval time, destination, and other run evidence.
- **Raw immutability:** preserve what arrived; write transformations elsewhere.
- **Snapshot:** the source state captured by a particular run.
- **Schema drift:** an upstream source changes its fields or structure.
- **Pagination:** retrieving a large result through multiple pages.
- **Rate limit:** a source restricts request frequency.
- **Retry:** controlled repetition after a transient failure.

### Failure Reasoning

If Extract fails, inspect:

1. network availability
2. source URL
3. HTTP status and response
4. timeout behavior
5. whether all expected raw files belong to the same successful run
6. extract log contents

Do not continue as if a partial snapshot were complete.

### Common Mistakes

- Transforming the API response before preserving raw data.
- Ignoring HTTP failures and writing error pages as data.
- Omitting timeouts.
- Overwriting source evidence with processed content.
- Treating a previous raw file as proof that the latest Extract succeeded.

### Check Your Understanding

1. What does Extract guarantee, and what does it not guarantee?
2. Why record byte count if QA later checks rows?
3. Why is a stable raw path useful?
4. How could pagination create an inconsistent snapshot?
5. When should a retry occur, and when should it not?

## 6. Transform

### Purpose

Transform converts source-specific raw layers into a consistent spatial data contract suitable for independent QA.

### Project Behavior

- Reads raw GeoJSON as GeoDataFrames.
- Normalizes column names to lowercase snake case.
- Retains selected attributes and the active geometry.
- Adds expected nullable fields when source fields are absent and logs them.
- Casts configured identifiers to strings.
- removes null and empty geometries.
- Attempts to repair invalid geometry.
- Removes geometry that remains unusable.
- Reprojects layers to `EPSG:3347`.
- Writes processed GeoJSON and transformation evidence.

### GeoDataFrame Mental Model

A GeoDataFrame is both:

- a table of attribute columns
- a spatial object with one active geometry column and CRS metadata

The geometry and CRS are not ordinary descriptive fields. Dropping the active geometry turns the result into nonspatial tabular data. Misstating the CRS gives coordinates the wrong meaning.

### Geometry States

| State | Meaning |
|---|---|
| Null | No geometry value exists |
| Empty | A geometry object exists but has no coordinates |
| Invalid | Coordinates violate geometry validity rules |
| Valid | Geometry satisfies the relevant structural rules |

### CRS: The Critical Distinction

- `set_crs(...)` assigns meaning to existing coordinates without changing them.
- `to_crs(...)` calculates new coordinates in another CRS.

If longitude/latitude coordinates have missing metadata, first assign the known source CRS, then transform to `EPSG:3347`. Assigning `EPSG:3347` directly to longitude/latitude values would falsely relabel coordinates without converting them.

### Identifier Reasoning

Identifiers describe identity, not quantity. String storage helps preserve formatting and avoids implying that arithmetic is meaningful. A road segment ID such as `00123` should not become the number `123` if leading zeros matter.

### Determinism

A deterministic Transform produces the same output from the same input and rules. Avoid hidden time dependence, random behavior, inconsistent ordering, and mutation of caller-owned data unless those behaviors are explicit.

### Common Mistakes

- Using `+=` and unintentionally mutating a caller's list.
- Treating CRS as a column named `CRS`.
- Omitting geometry during field selection.
- Confusing `set_crs` with `to_crs`.
- Performing QA repair inside the acceptance stage.
- Ignoring unexpected row loss.
- Editing the raw source file.

### Check Your Understanding

1. Why should Transform copy a GeoDataFrame before changing it?
2. Why retain geometry explicitly during field selection?
3. What is the difference among null, empty, invalid, and missing geometry?
4. Why is `EPSG:3347` preferable to longitude/latitude for metric analysis?
5. Which evidence would reveal unexpected row loss?
6. What future tests would joins, aggregation, and deduplication require?

## 7. QA/QC

### Purpose

QA/QC independently decides whether processed data is acceptable for publication. It is a blocking gate, not another transformation step.

### Project Checks

- processed file exists
- expected fields and geometry exist
- layer contains rows
- no null geometry
- no empty geometry
- no invalid geometry
- configured ID has no nulls
- configured ID has no duplicates
- CRS equals `EPSG:3347`

### Quality Dimensions

- **Completeness:** required data is present.
- **Validity:** values and geometry satisfy technical rules.
- **Uniqueness:** records expected to be distinct are distinct.
- **Consistency:** related representations agree.
- **Accuracy:** data reflects reality closely enough for its use.
- **Freshness:** data is recent enough for its purpose.
- **Referential integrity:** related keys point to valid records.
- **Reconciliation:** counts or totals agree across boundaries.

Not every dimension is fully implemented in this project, but you should recognize where each would belong.

### QA Versus QC

- **QA** emphasizes the process and controls that prevent defects.
- **QC** emphasizes inspection of actual outputs for defects.
- A practical pipeline quality gate commonly includes both ideas.

### Severity

- **Failure:** blocks publication.
- **Warning:** allows publication under an agreed policy but requires attention.
- **Diagnostic:** provides context without deciding acceptance.

### Failure Reasoning

When QA fails:

1. Read the specific failed metric.
2. Identify the dataset and processed artifact.
3. Trace the defect to Extract, Transform, or the quality rule.
4. Correct the owning stage.
5. Regenerate downstream artifacts.
6. Rerun QA before Load.

### Common Mistakes

- Repairing data inside QA and hiding a Transform defect.
- Checking only that a file exists.
- Printing warnings without defining whether they block.
- Trusting Transform's log instead of reopening its output.
- Loading first and checking afterward.

### Check Your Understanding

1. Why must QA independently reopen processed files?
2. Which current rules block Load?
3. Why does a duplicate ID matter?
4. What is the difference between a warning and a failure?
5. Which quality dimensions would you add for frequently changing source data?

## 8. Load and PostGIS

### Purpose

Load publishes only QA-approved layers and proves the database reflects the intended snapshot.

### Project Behavior

- Runs QA by default before loading.
- Opens a SQLAlchemy database engine and transaction.
- Replaces each destination table.
- Loads all layers inside one transaction.
- Reconciles source and loaded row counts.
- Confirms geometry has an SRID.
- Confirms a GIST spatial index exists.
- Commits all changes together or rolls them all back.

### Key Concepts

- **Transaction:** a group of operations treated as one unit.
- **Atomicity:** either all intended table changes commit or none do.
- **Rollback:** reverse uncommitted changes after failure.
- **Idempotency:** a safe rerun produces the intended current state without duplicate accumulation.
- **Replace:** recreate the complete destination snapshot.
- **Append:** add rows to existing data.
- **Upsert:** insert new keys and update existing keys.
- **SRID:** the database identifier for the geometry reference system.
- **GIST index:** an index structure used to accelerate spatial queries.
- **Reconciliation:** compare expected source state with actual target state.

### Why Replace Works Here

This project loads complete snapshots rather than change events. Replacing tables means a repeat run refreshes the current snapshot instead of appending the same features again.

Append or upsert would require stronger rules for:

- stable keys
- duplicate handling
- update and deletion detection
- batch checkpoints
- partial retry
- historical versus current records
- constraints and conflict behavior

### Failure Reasoning

If layer three fails inside one transaction, changes from layers one and two should not remain committed. Investigate the failing layer, database error, schema compatibility, connection, and transaction result before rerunning.

### Common Mistakes

- Loading without a successful QA gate.
- Using append for full snapshots and creating duplicates.
- Treating `to_postgis` returning as complete verification.
- Committing each layer separately when atomic publication is required.
- Ignoring SRID or spatial-index state.
- Building SQL identifiers from unchecked input.

### Check Your Understanding

1. Why is one transaction safer than four unrelated commits?
2. Why do matching row counts matter but not prove everything?
3. What does the SRID prove?
4. What does a GIST index change, and what does it not change?
5. When would upsert be more appropriate than replace?

## 9. Orchestration

### Purpose

The orchestrator gives operators one correct entry point and prevents accidental stage reordering.

### Commands

```bash
python -m src.main
python -m src.main --skip-extract
python -m src.main --skip-extract --skip-load
```

### Choosing the Command

- Use the full command for a fresh source-to-database run.
- Use `--skip-extract` to deliberately reuse current raw snapshots.
- Add `--skip-load` when validating only through QA.
- Do not use skip options merely to bypass a failing prerequisite.

### Important Limitation

Transform records individual dataset errors. An older processed file might still exist after a later dataset transformation fails. Review stage status and logs so stale output is not mistaken for the current run.

### Check Your Understanding

1. Why is orchestration different from stage implementation?
2. When is `--skip-extract` legitimate?
3. Why can the existence of a processed file be insufficient evidence?
4. What stage timings could help diagnose?

## 10. Testing and Verification

### Purpose

Tests provide repeatable evidence about defined behavior. They do not prove every source, machine, or future run will succeed.

### Commands

```bash
python -m unittest discover -s tests -v
RUN_POSTGIS_TESTS=1 python -m unittest discover -s tests -v
```

### Test Levels

- **Unit test:** checks a small behavior with controlled inputs.
- **Integration test:** checks multiple components working together.
- **Smoke test:** exercises the smallest representative end-to-end path.
- **Operational verification:** confirms a current real run and its artifacts.
- **Static analysis:** checks code properties without operating the full system.

### Current Test Evidence

The project tests:

- a valid QA layer passes
- a duplicate identifier fails
- a missing file produces an actionable failure
- repeat database loading does not duplicate rows
- a forced transaction failure rolls back table creation

### What to Verify After a Real Run

- command exit status
- Extract and Transform logs
- QA report
- input and output row counts
- processed CRS and geometry validity
- database row counts
- SRIDs
- GIST indexes
- transaction completion

### Common Mistakes

- Treating skipped integration tests as passes.
- Testing only the happy path.
- Assuming a unit test proves the live API works.
- Assuming a live run replaces deterministic regression tests.
- Ignoring cleanup and test isolation.

### Check Your Understanding

1. Why are unit and integration tests both needed?
2. What does the rollback test prove?
3. Why should tests use controlled fixtures?
4. What evidence is required before saying the project is currently operational?

## 11. Troubleshooting by Boundary

Use the first failing boundary instead of making random downstream changes.

| Symptom | First investigation |
|---|---|
| Import fails | Active interpreter, environment, installed dependencies |
| Docker connection fails | Container status, port `5433`, database URL |
| HTTP 503 | Source service and response; do not blame Transform |
| Raw file missing | Extract status, URL, output path, log |
| Unexpected row loss | Transform log and geometry/filtering rules |
| Wrong CRS in QA | Source CRS assignment and reprojection in Transform |
| Duplicate IDs in QA | Source data, ID selection, Transform business rule |
| Load count mismatch | Transaction, source file, target table, write error |
| No GIST index | Loaded table definition and GeoPandas/PostGIS behavior |
| Integration tests skipped | `RUN_POSTGIS_TESTS` and PostGIS availability |
| Secret appears in Git | Stop staging/pushing; remove safely and rotate if exposed |

Use this diagnostic sentence:

> The first broken guarantee is at the ___ boundary, shown by ___ evidence, so I will inspect ___ before changing downstream stages.

## 12. High-Value Comparisons

Be able to explain each pair without notes:

| Comparison | Essential distinction |
|---|---|
| Environment vs interpreter | Package context versus executable running Python |
| Installed vs declared dependency | Current machine fact versus reproducible project requirement |
| Unsaved buffer vs working tree | Editor memory versus saved disk state Git can inspect |
| Working tree vs staging area | Current saved changes versus proposed next commit |
| Raw vs processed data | Source evidence versus standardized derivative |
| Attribute vs geometry | Descriptive value versus spatial shape/location |
| `set_crs` vs `to_crs` | Declare coordinate meaning versus calculate new coordinates |
| Null vs empty geometry | Missing value versus geometry with no coordinates |
| Invalid vs inaccurate geometry | Structural rule failure versus mismatch with reality |
| Transform vs QA | Repair/standardize versus independently accept/reject |
| QA vs QC | Process-oriented prevention versus output inspection |
| Replace vs append | Refresh snapshot versus accumulate rows |
| Replace vs upsert | Recreate table versus key-based insert/update |
| Commit vs database transaction | Versioned source snapshot versus atomic data operation |
| Unit vs integration test | Isolated behavior versus connected components |
| Complete vs operational | Implementation exists versus current runtime evidence passes |

## 13. Essential Commands From Memory

Try to write these before revealing the table.

| Goal | Command |
|---|---|
| Activate environment | `conda activate calgary-etl` |
| Inspect interpreter | `which python` |
| Start PostGIS | `docker compose up -d` |
| Check PostGIS service | `docker compose ps` |
| Initialize database | `docker compose exec -T postgis psql -U postgres -d postgres < sql/init.sql` |
| Run Extract | `python -m src.extract` |
| Run Transform | `python -m src.transform` |
| Run QA | `python -m src.qa` |
| Run Load | `python -m src.load` |
| Run full pipeline | `python -m src.main` |
| Run unit tests | `python -m unittest discover -s tests -v` |
| Include PostGIS tests | `RUN_POSTGIS_TESTS=1 python -m unittest discover -s tests -v` |
| Inspect Git state | `git status` |
| Inspect saved changes | `git diff` |
| Inspect staged changes | `git diff --cached` |
| Inspect latest commit | `git log -1 --oneline` |
| Inspect remotes | `git remote -v` |

## 14. Seven-Session Study Plan

Do not measure progress only by reading time. Each session should include recall, practice, and explanation.

### Session 1: Architecture, Environment, and Git

- Draw the complete sequence from memory.
- Explain the four-stage boundary model.
- Activate the environment and identify the interpreter.
- Practice working tree versus staging area in the Git workbook.
- Answer Sections 1-3 review questions.

### Session 2: PostGIS and Extract

- Explain image, container, volume, port, database, and extension.
- Start and inspect PostGIS.
- Trace one dataset from configuration to its raw output and log.
- Explain timeout, status validation, provenance, and raw immutability.
- Answer Sections 4-5 review questions.

### Session 3: Transform Foundations

- Complete the Transform practice notebook exercises on schema and IDs.
- Explain GeoDataFrame, active geometry, null, empty, and invalid geometry.
- Demonstrate `set_crs` versus `to_crs` using toy data.
- Answer the first half of Section 6 review questions.

### Session 4: Transform and QA/QC

- Trace geometry cleaning and reprojection.
- Explain why repair belongs in Transform.
- List every blocking QA rule from memory.
- Design one warning and one diagnostic that do not currently exist.
- Answer Sections 6-7 review questions.

### Session 5: Load and Transactions

- Explain replace, append, and upsert.
- Draw transaction commit and rollback outcomes.
- Explain row reconciliation, SRID, and GIST indexes.
- Review the integration tests and state what each proves.
- Answer Section 8 review questions.

### Session 6: Orchestration, Testing, and Troubleshooting

- Choose among the three `src.main` command forms for sample scenarios.
- Classify tests as unit, integration, smoke, or operational.
- Work through every troubleshooting row without notes.
- Explain why complete and operational are separate claims.
- Answer Sections 9-10 review questions.

### Session 7: Cumulative Retrieval

- Explain the full project aloud in five minutes.
- Recreate the stage table from memory.
- Write all essential commands without looking.
- Complete [project1_big_picture_assessment.ipynb](../assessments/project1_big_picture_assessment.ipynb).
- Make a remediation list from missed questions.

## 15. Flashcards

Cover the answers and retrieve them aloud.

1. **What is ETL?** Extract source data, Transform it into a defined contract, and Load approved results into a destination.
2. **What is the target CRS?** `EPSG:3347`.
3. **What is provenance?** Evidence of source, retrieval time, destination, and run details.
4. **Why preserve raw files?** Replay, audit, comparison, and protection of source evidence.
5. **What does `set_crs` do?** Assigns CRS meaning without changing coordinates.
6. **What does `to_crs` do?** Calculates coordinates in another CRS.
7. **Where does geometry repair belong?** Transform.
8. **What is QA's job?** Independently accept or reject processed output.
9. **Why does QA precede Load?** To prevent known-bad data from publication.
10. **What does transaction atomicity mean?** All intended changes commit together or all roll back.
11. **Why is replacement idempotent here?** Each run recreates the current complete snapshot rather than appending duplicates.
12. **What does SRID represent?** The database identifier for the spatial reference system.
13. **Why use a GIST index?** To accelerate spatial query filtering.
14. **What is reconciliation?** Comparing expected source state with actual destination state.
15. **What does `git diff --cached` show?** The proposed contents of the next commit.
16. **Can Git see unsaved editor changes?** No.
17. **Does `.gitignore` untrack committed files?** No.
18. **What does a unit test prove?** A defined isolated behavior for controlled inputs.
19. **What does an integration test prove?** Selected components work together in the tested environment.
20. **What is the first troubleshooting rule?** Find the earliest broken stage guarantee.

## 16. Final Mastery Checklist

You understand the project when you can do all of the following without relying on memorized code:

- state the project purpose and four datasets
- draw the correct setup and ETL order
- distinguish supporting setup from data-processing stages
- explain every stage using input, responsibility, output, and evidence
- recreate and verify the Python environment
- explain Git's editor, working tree, staging, commit, branch, and remote states
- start and initialize PostGIS
- explain source provenance and raw-data preservation
- explain GeoDataFrames, geometry states, ID typing, and CRS operations
- justify every blocking QA rule
- explain replace semantics, transactions, rollback, SRID, indexes, and reconciliation
- choose the correct pipeline command for a scenario
- distinguish unit, integration, smoke, and operational verification
- diagnose from the earliest failed boundary
- identify generated artifacts that should remain outside Git
- explain the current project limitations without understating its verified success

## Final Retrieval Prompt

Without opening another file, answer:

> What data does this project accept, what guarantee does each stage add, what evidence proves each guarantee, and what prevents unacceptable or partially loaded data from being published?

If your answer clearly covers the environment, Git, PostGIS, Extract, Transform, QA/QC, Load, verification, testing, and failure ownership, you understand the project as a system rather than as disconnected Python files.