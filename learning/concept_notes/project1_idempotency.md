# Idempotency

## Core Idea

An operation is idempotent when repeating it with the same intended input leaves the system in the same intended final state rather than accumulating unintended changes.

Conceptually:

```text
apply(input) once  -> intended state
apply(input) again -> same intended state
```

The repeated operation may still perform work. Idempotency describes the resulting state, not whether the second execution does nothing.

## Project Example: Full-Table Replacement

This project's Load stage writes complete approved snapshots using replacement semantics.

Suppose the incoming roads layer has 19,385 rows:

```text
first load  -> roads table has 19,385 rows
second load -> roads table still has 19,385 rows
```

The second full load replaces the table from the same complete input instead of appending another 19,385 rows.

That is the project's main idempotency guarantee.

## Replace Versus Append

### Replace

```text
existing rows are replaced by the complete incoming snapshot
```

Repeating the same full snapshot produces the same table contents, assuming deterministic serialization and a successful transaction.

### Append

```text
incoming rows are added to existing rows
```

Repeating a complete snapshot append can duplicate every row:

```text
first append  -> 19,385 rows
second append -> 38,770 rows
```

Append can be correct for event streams or genuinely new batches, but it is not idempotent for repeated full snapshots unless additional keys and conflict rules prevent duplication.

### Upsert

An upsert inserts new keys and updates existing keys. It can support idempotent repeated inputs when stable identifiers, conflict behavior, and deletion handling are carefully defined.

The current project does not implement upsert loading.

## Idempotency in Other Project Operations

Some setup operations are also designed for safe repetition:

- `mkdir(parents=True, exist_ok=True)` tolerates existing directories.
- `CREATE DATABASE` logic in `sql/init.sql` avoids recreating an existing database.
- `CREATE EXTENSION IF NOT EXISTS` safely ensures PostGIS extensions exist.
- repeated table replacement refreshes current data without duplicate accumulation.

Not every operation is idempotent. Extract and Transform logs currently append rows, so rerunning stages intentionally adds new operational history.

## Idempotency Versus Determinism

These concepts differ:

- **Determinism:** the same input produces the same output.
- **Idempotency:** applying an operation repeatedly leaves the same intended final state.

An operation can be idempotent while recording a new timestamp on every run. The database table may end in the same state even though logs differ.

## Idempotency Versus Transactions

Idempotency and transactions solve different problems.

- **Idempotency:** protects safe repetition from unintended accumulation.
- **Transaction atomicity:** protects a single run from leaving a partial committed state.

Replacement does not guarantee that four tables update together. The shared database transaction provides that all-or-nothing behavior.

A robust Load stage needs both:

```text
repeat successful run -> no duplicate accumulation
failed run             -> no partial publication
```

## Idempotency Versus Reproducibility

- **Idempotency** asks whether repeating an operation leaves the intended state.
- **Reproducibility** asks whether the process and environment can be recreated to obtain the expected result.

A live API can change between runs. Two successful full loads can each be idempotent relative to their own input snapshots while producing different tables because the source data changed.

## How the Project Tests It

The PostGIS integration test loads the same controlled layer twice using replacement semantics and verifies that the final row count does not double.

This provides executable evidence for repeated full-load behavior. It does not prove that every external source run returns identical data.

## Failure Cases to Watch

Idempotency can be broken by:

- switching a full snapshot load from replace to append
- unstable or missing keys in an upsert design
- side effects outside the controlled transaction
- partial writes followed by unsafe retry logic
- duplicated external notifications or exports
- nonrepeatable transformations that accumulate changes

Each side effect must be considered separately. An idempotent database write does not automatically make the entire pipeline idempotent.

## Plain-Language Definition

> Idempotency means a safe rerun refreshes the intended state without unintentionally duplicating or accumulating data.

## Related Resources

- [Module 6 Load and PostGIS reference](../reference/project1_module_6_load_postgis_reference.md)
- [Module 6 Load and PostGIS practice](../practice/project1_module_6_load_postgis_practice.ipynb)
- [Module 7 orchestration and testing reference](../reference/project1_module_7_orchestration_testing_reference.md)
