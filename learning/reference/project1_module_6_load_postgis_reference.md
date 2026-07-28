# Project 1 Module 6: Load and PostGIS Reference

## Purpose

This reference teaches the database-loading concepts behind [Module 6 Load and PostGIS practice](../starters/project1_module_6_load_postgis_practice.ipynb) and `src/load.py`.

## 1. Load Stage Contract

Load accepts only QA-approved processed GeoJSON and publishes spatial tables to PostGIS.

Its success criteria are stronger than "the write method returned":

- every intended layer loads
- source and target row counts match
- loaded geometry has a valid SRID
- a GIST geometry index exists
- the transaction commits

## 2. Database URL and Environment

The connection URL identifies the SQLAlchemy dialect, driver, account, host, port, and database.

```text
postgresql+psycopg2://user:password@localhost:5433/calgary_gis
```

`DATABASE_URL` can override the local default. Do not print or commit nonpublic credentials.

## 3. SQLAlchemy Engine and Connection

An engine manages database connectivity. A connection performs SQL and writes within a specific context.

```python
from sqlalchemy import create_engine

engine = create_engine(database_url, pool_pre_ping=True)
```

`pool_pre_ping=True` checks pooled connections before reuse, reducing failures from stale connections.

Owned engines should be disposed when no longer needed.

## 4. Transactions and Atomicity

A transaction groups operations into one unit.

```python
with engine.begin() as connection:
    load_first_layer(connection)
    load_second_layer(connection)
```

If all operations succeed, the context commits. If an exception escapes, it rolls back.

Atomic publication means users do not receive a knowingly partial four-layer refresh.

## 5. Replace, Append, and Upsert

### Replace

Recreates the destination table from a complete snapshot. This project uses replace semantics.

### Append

Adds rows to existing data. Repeating a full snapshot append would create duplicates unless prevented by constraints and logic.

### Upsert

Inserts new keys and updates existing keys. It requires stable keys and defined conflict behavior.

A move from replace to upsert would also require deletion detection, batch recovery, and stronger key rules.

## 6. Idempotency

An idempotent rerun produces the intended current state without accumulating unintended duplicates.

Replacement is idempotent for this full-snapshot design because each successful run refreshes the destination from the complete approved input.

Idempotency does not mean every intermediate action is identical. It means the resulting intended state is stable across safe reruns.

## 7. GeoDataFrame to PostGIS

GeoPandas writes a GeoDataFrame with `to_postgis`.

The GeoDataFrame needs:

- an active geometry column
- CRS metadata
- database-compatible field values
- a valid connection

The database stores geometry with an SRID derived from the CRS.

## 8. SQL Identifier Validation

Schema and table names are SQL identifiers, not ordinary parameter values.

The project restricts identifiers to lowercase letters, digits, and underscores with a valid first character.

This prevents malformed names and reduces SQL-injection risk where identifiers must be interpolated into SQL text.

Bound parameters should still be used for ordinary values.

## 9. Row Reconciliation

After writing a table, Load queries its row count and compares it with the source GeoDataFrame.

Matching counts prove that the number of stored records agrees for this boundary. They do not prove:

- every value is correct
- every geometry is accurate
- no fields were altered unexpectedly

Reconciliation is one layer of evidence, not the entire quality argument.

## 10. SRID Verification

The SRID identifies the spatial reference system stored with geometry.

For this project, loaded geometry should report SRID `3347`.

A positive SRID proves the database recognizes a spatial reference. Verifying the expected exact SRID is stronger than checking only that it is nonzero.

## 11. GIST Spatial Index

A GIST index supports efficient spatial filtering and relationship queries.

Examples that benefit include:

- bounding-box searches
- intersection candidates
- nearby-feature filtering
- spatial joins

An index improves query access paths. It does not repair geometry, assign a CRS, or guarantee every query will use the index.

## 12. QA Before Database Access

`run_load` calls QA by default before creating or using the database engine.

This ordering prevents known-bad processed layers from entering a publication transaction and avoids unnecessary database work.

Bypassing QA should be limited to controlled integration tests that provide equivalent approved fixtures.

## 13. Rollback Behavior

If one layer fails inside the shared transaction, earlier uncommitted table changes should roll back.

The integration test deliberately raises an exception after creating a table and confirms the table does not remain.

This verifies failure safety, not only successful insertion.

## 14. Isolated Integration Testing

Database tests use a separate schema such as `etl_test`.

Isolation prevents tests from replacing production-like `public` tables. Setup creates the schema; teardown removes it and all contained objects.

The environment variable `RUN_POSTGIS_TESTS=1` makes live database dependencies explicit.

A skipped integration test is neither a pass nor a failure. It means that behavior was not exercised in that run.

## 15. Failure Diagnosis

### Connection failure

Inspect Docker status, port `5433`, database existence, credentials, and `DATABASE_URL`.

### Missing input

Return to Transform and QA. Do not create an empty database table to conceal a missing approved artifact.

### Row mismatch

Inspect the transaction, source count, target query, write warnings, and field/geometry compatibility.

### Missing SRID

Inspect GeoDataFrame CRS before Load and the destination geometry metadata.

### Missing spatial index

Inspect table indexes and the behavior of the installed GeoPandas/GeoAlchemy2/PostGIS stack.

## Common Misconceptions

- A successful write call proves publication. Post-load verification is still required.
- Append is a safe replacement for full snapshots. It can duplicate rows.
- A transaction prevents every possible data-quality defect. It protects atomic database state.
- Matching row counts prove all values are correct. They do not.
- A GIST index changes geometry accuracy. It affects query performance.

## Review Checklist

You should be able to explain:

- engine, connection, and transaction
- atomic commit and rollback
- replace, append, and upsert
- why replacement is idempotent here
- identifier validation
- row reconciliation
- SRID and GIST indexes
- isolated integration tests
- why QA precedes Load

## Companion Resources

- [Module 6 Load and PostGIS practice](../starters/project1_module_6_load_postgis_practice.ipynb)
- [Module 1 Environment/PostGIS reference](project1_module_1_environment_postgis_reference.md)
- [Module 5 QA/QC reference](project1_module_5_qa_qc_reference.md)
