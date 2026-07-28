# Atomic Transactions

## Core Idea

An operation is **atomic** when it is treated as one indivisible unit: either all of its changes succeed and become permanent, or none of them do.

In database work, atomicity is commonly summarized as:

```text
all changes commit
        or
all changes roll back
```

Atomicity prevents a failed operation from leaving a partially updated database.

## This Project's Load Transaction

The Load stage publishes all configured spatial layers inside one SQLAlchemy transaction:

```python
with active_engine.begin() as connection:
    for dataset_name, config in DATASETS.items():
        load_layer(...)
```

`active_engine.begin()` starts a transaction and supplies one database connection to each layer load.

Conceptually:

```text
begin transaction
    -> load communities
    -> load roads
    -> load transit stops
    -> load land-use districts
commit transaction
```

If the entire block finishes successfully, SQLAlchemy commits the transaction. The new database state becomes permanent and visible according to PostgreSQL's transaction rules.

## What Happens on Failure

If loading or reconciling any layer raises an exception, execution leaves the transaction block and SQLAlchemy rolls it back.

For example:

```text
begin transaction
    -> communities succeeds
    -> roads succeeds
    -> transit stops fails
    -> land-use districts never loads
rollback transaction
```

The successful changes made earlier in that same transaction are not committed. The database retains its previous committed state rather than publishing a mixture of old and new layers.

## Commit and Rollback

A **commit** makes the transaction's successful changes permanent.

A **rollback** abandons the transaction's uncommitted changes and restores the database to its prior committed state.

```text
successful transaction -> commit   -> keep all changes
failed transaction     -> rollback -> keep none of its changes
```

Rollback does not mean reversing arbitrary history after a transaction has already committed. It acts on the current uncommitted transaction.

## Why Batch Atomicity Matters

The four layers form one publication batch. Without a shared transaction, a failure could leave this state:

```text
communities       -> current run
roads             -> current run
transit_stops     -> previous run
land_use_districts -> previous run
```

Each table might be valid by itself, but the database would contain layers from different pipeline runs. Atomic batch publication prevents that partial state.

## How the Project Tests Rollback

The PostGIS integration test:

1. starts a database transaction
2. creates and loads a controlled spatial table
3. deliberately raises `RuntimeError("force rollback")`
4. verifies that the table does not exist afterward

The test provides executable evidence that table creation inside the failed transaction is rolled back.

It tests one controlled table rather than forcing failure midway through the full four-layer `run_load()` loop. The application structure places all four calls inside the same transaction boundary, while broader integration coverage could additionally test a forced mid-batch failure through `run_load()` itself.

## Atomicity Versus Idempotency

These concepts solve different problems:

- **Atomicity:** prevents one failed run from leaving partial committed changes.
- **Idempotency:** prevents safe repeated runs from unintentionally accumulating changes.

This project needs both:

```text
failed run         -> no partial publication
successful rerun   -> no duplicate accumulation
```

Full-table replacement supports idempotency for repeated approved snapshots. The shared transaction supports atomicity across the Load batch.

## Atomicity Versus Consistency

Atomicity does not by itself prove that committed data is correct or satisfies every rule.

- **Atomicity** controls whether a group of changes is committed together.
- **Consistency** concerns whether defined database and application rules hold before and after a transaction.

This project runs QA before Load and reconciles row counts, SRID, and spatial indexes during Load. Those checks support consistency; the transaction ensures their associated database changes are committed or rolled back together.

## Atomicity Versus Isolation

Concurrent transactions may run at the same time. **Isolation** controls how their intermediate and committed changes can affect one another.

Atomicity says:

```text
this transaction is all-or-nothing
```

Isolation says:

```text
how this transaction interacts with other concurrent transactions
```

They are separate database guarantees.

## Atomicity Versus Durability

After a transaction commits, **durability** means the database preserves the committed changes despite events such as process restarts or crashes, within the guarantees of its storage configuration.

Atomicity decides whether the batch commits as a whole. Durability concerns keeping it after that commit.

## ACID

Atomicity is the **A** in the common ACID transaction properties:

| Property | Core question |
|---|---|
| Atomicity | Do all changes commit together or all roll back? |
| Consistency | Does the transaction preserve defined rules? |
| Isolation | How do concurrent transactions interact? |
| Durability | Do committed changes persist? |

A transaction system uses these properties together to support reliable database changes.

## Transaction Boundaries Matter

Atomicity applies only to work controlled by the same transaction.

The Load transaction can roll back PostgreSQL changes made through its connection. It cannot automatically undo effects outside PostgreSQL, such as:

- downloaded files
- processed GeoJSON files
- appended CSV log rows
- emails or external notifications
- requests sent to another API
- changes committed through a separate database connection

Making a complete multi-system workflow atomic requires additional patterns, such as staged publication, compensating actions, an outbox, or coordinated transactions. This project claims database atomicity for its Load batch, not universal rollback across the entire ETL pipeline.

## Plain-Language Definition

> Atomic means all-or-nothing: either the complete database operation is committed, or the database keeps its previous committed state.

## Related Resources

- [Idempotency](project1_idempotency.md)
- [Data quality gates](project1_data_quality_gates.md)
- [Module 6 Load and PostGIS reference](../reference/project1_module_6_load_postgis_reference.md)
- [Module 6 Load and PostGIS practice](../starters/project1_module_6_load_postgis_practice.ipynb)
- [Module 7 orchestration and testing reference](../reference/project1_module_7_orchestration_testing_reference.md)
