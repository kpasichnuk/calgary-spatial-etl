# Project 1 Module 7: Orchestration and Testing Reference

## Purpose

This reference teaches the connected workflow and verification concepts behind [Module 7 orchestration and testing practice](../starters/project1_module_7_orchestration_testing_practice.ipynb) and `src/main.py`.

## 1. Orchestration Versus Stage Logic

Stage modules implement Extract, Transform, QA/QC, and Load. The orchestrator calls them in the correct dependency order.

```text
Extract -> Transform -> QA/QC -> Load
```

Orchestration should not duplicate each stage's internal logic. It coordinates boundaries, options, timing, and failure propagation.

## 2. Complete Operational Order

The broader operating sequence is:

```text
understand the contract
    -> activate and verify the environment
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

Environment, Git, PostGIS setup, and tests support ETL. Extract, Transform, QA/QC, and Load are the primary data pipeline stages.

## 3. Main Entry Point

Run the full pipeline:

```bash
python -m src.main
```

The module entry-point guard parses command-line arguments and passes them to `run_pipeline`.

Using `python -m` resolves the module in project context and supports package imports such as `from src.extract import run_extract`.

## 4. Skip Options

Reuse an intentionally preserved raw snapshot:

```bash
python -m src.main --skip-extract
```

Stop after QA without publishing to PostGIS:

```bash
python -m src.main --skip-extract --skip-load
```

Skip options express a deliberate operating mode. They should not conceal a failed prerequisite.

## 5. Stage Timing

`timed_stage` records elapsed wall-clock time using a performance counter.

Timing can reveal:

- network extraction slowdown
- unexpectedly expensive transformation
- database loading regression
- stage-to-stage performance differences

Timing proves duration, not correctness. It must be combined with stage evidence.

## 6. Failure Propagation

An uncaught stage exception stops the orchestrator. This is appropriate when continuing would violate a downstream precondition.

Examples:

- failed Extract means a fresh complete snapshot is unavailable
- failed QA means Load must not publish
- failed Load means the run is not operationally complete

The first broken guarantee owns the initial diagnosis.

## 7. Stale Artifact Risk

A file existing on disk does not prove it belongs to the current run.

Transform records per-dataset errors and may leave an older processed file in place. Operators must inspect current logs and statuses rather than inferring success from file presence.

A stronger future design could remove stale outputs before processing or make Transform raise when any configured dataset fails.

## 8. Verification Levels

### Unit test

Checks a small behavior with controlled inputs, such as duplicate-ID rejection.

### Integration test

Checks connected components, such as GeoPandas, SQLAlchemy, and live PostGIS rollback.

### Smoke test

Exercises the smallest representative path across major boundaries.

### Operational verification

Runs current real sources and confirms actual generated artifacts and database state.

### Static analysis

Checks code properties without running the complete system, such as syntax or type diagnostics.

No one level replaces all others.

## 9. Happy and Failure Paths

Happy-path tests prove accepted input can succeed. Failure-path tests prove defects are rejected safely.

For a data pipeline, failure safety is essential because a partial or silently corrupted publication can be worse than a visible stopped run.

Examples:

- valid QA layer passes
- duplicate ID fails
- missing file returns an actionable result
- repeated Load does not duplicate
- forced database failure rolls back

## 10. Skipped Tests

The PostGIS integration tests are opt-in:

```bash
RUN_POSTGIS_TESTS=1 python -m unittest discover -s tests -v
```

Without the environment variable, the tests are reported as skipped. A skipped result means the behavior remains unverified in that test run.

Report passed, failed, skipped, and errored tests separately.

## 11. Evidence by Stage

| Stage | Evidence |
|---|---|
| Environment | selected interpreter and successful imports |
| Git | branch, working tree, staged diff, commit history |
| PostGIS | service status, database connection, extensions |
| Extract | current raw files and provenance log |
| Transform | current processed files and transform log |
| QA/QC | passing report and successful stage exit |
| Load | committed transaction, counts, SRID, indexes |
| Tests | explicit pass/fail/skip/error results |

A console message alone is weaker than reconciled artifacts and state.

## 12. Complete Versus Operational

**Complete** means the implementation, tests, setup definitions, and documentation satisfy the defined project scope.

**Operational** means current runtime evidence passes in the available environment.

A complete project can be temporarily nonoperational because an API or Docker is unavailable. A one-time successful run does not prove the implementation is complete or maintainable.

## 13. Boundary-First Troubleshooting

Use this statement:

> The first broken guarantee is at the ___ boundary, shown by ___ evidence, so I will inspect ___ before changing downstream stages.

Examples:

- missing import -> environment boundary
- HTTP 503 -> Extract boundary
- unexpected row loss -> Transform boundary
- wrong CRS in QA -> Transform-to-QA boundary
- connection refused -> PostGIS setup boundary
- row mismatch -> Load boundary
- skipped database tests -> integration-verification boundary

This prevents random downstream edits.

## 14. Safe Operator Runbook

1. Activate `calgary-etl` and confirm the interpreter.
2. Inspect Git status and branch.
3. Start and inspect PostGIS.
4. Initialize the database when needed.
5. Run the correct pipeline command.
6. Stop at the first failed stage.
7. Inspect logs and reports for the current run.
8. Reconcile PostGIS counts, SRID, and indexes.
9. Run unit and integration tests.
10. Review source changes before committing.

## 15. Test Isolation

Tests should avoid modifying production-like project artifacts.

Useful isolation techniques include:

- temporary directories
- in-memory GeoDataFrames
- fake HTTP responses
- isolated database schemas
- deterministic fixtures
- teardown cleanup

Isolation makes reruns predictable and reduces accidental side effects.

## Common Misconceptions

- Orchestration should reimplement stage logic. It should coordinate it.
- Skip flags are fixes for failed stages. They are deliberate operating choices.
- Existing artifacts prove current success. They may be stale.
- Unit tests prove the live database works. Integration evidence is still needed.
- A live run makes regression tests unnecessary. Both provide different evidence.
- Complete and operational mean the same thing. They answer different questions.

## Review Checklist

You should be able to explain:

- stage implementation versus orchestration
- correct stage order and preconditions
- each `src.main` command form
- timing versus correctness evidence
- test levels and skipped tests
- stale artifact risk
- complete versus operational status
- boundary-first troubleshooting
- the evidence needed for a verified run

## Companion Resources

- [Module 7 orchestration and testing practice](../starters/project1_module_7_orchestration_testing_practice.ipynb)
- [Project 1 ETL walkthrough](../walkthroughs/project1_etl_walkthrough.ipynb)
- [Big-picture assessment](../assessments/project1_big_picture_assessment.ipynb)
