# Function Side Effects

## Core Idea

A function side effect is an observable action that occurs in addition to producing its return value.

Side effects are not automatically mistakes. Many useful functions intentionally write files, update databases, send requests, print messages, or modify objects. The important questions are whether the side effect is expected, documented, and appropriate for the function's responsibility.

## Return Value Versus Side Effect

This function only calculates and returns a value:

```python
def add_numbers(first, second):
    return first + second
```

Calling it does not intentionally change anything outside the function:

```python
total = add_numbers(2, 3)
```

By contrast, this function writes a file:

```python
def save_status(path):
    path.write_text("complete")
```

Its filesystem change remains after the function finishes. That change is a side effect.

## Common Side Effects

A function has a side effect when it does something observable such as:

- modifying an input object
- changing a global variable
- writing, renaming, or deleting a file
- appending to a log
- changing a database
- sending an HTTP request
- printing to the terminal
- sending an email or notification
- starting or stopping an external service

A function can have more than one side effect and can also return a value.

## Input Mutation as a Side Effect

Consider a function that receives a list:

```python
def add_geometry(fields):
    fields.append("geometry")
```

The function returns `None`, but it changes the caller's list:

```python
required = ["name"]
add_geometry(required)

print(required)
# ["name", "geometry"]
```

The mutation is a side effect because code outside the function can observe the changed list.

This version avoids changing the input:

```python
def with_geometry(fields):
    return fields + ["geometry"]
```

The caller explicitly receives a new list:

```python
required = ["name"]
output = with_geometry(required)

print(required)  # ["name"]
print(output)    # ["name", "geometry"]
```

## Copying for Caller Safety

Several Transform helpers copy their GeoDataFrame input before changing it:

```python
def normalize_columns(gdf):
    gdf = gdf.copy()
    gdf.columns = [normalize_col_name(column) for column in gdf.columns]
    return gdf
```

The local `gdf` refers to the copy after `gdf.copy()`. Renaming its columns does not intentionally modify the caller's original GeoDataFrame.

This design makes the helper easier to reason about:

```text
input GeoDataFrame  -> remains unchanged
returned copy       -> contains normalized columns
```

A copy can reduce mutation side effects, although the function still performs computation and may raise exceptions.

## Intentional Project Side Effects

The ETL stage functions are useful specifically because they affect the world outside Python's local function scope.

### Extract

`run_extract()`:

- sends HTTP requests to City of Calgary endpoints
- creates parent directories
- writes raw GeoJSON files
- appends retrieval records to the extract log
- prints progress messages

### Transform

`run_transform()`:

- reads raw files
- creates processed-output directories
- writes processed GeoJSON files
- appends records to the transform log
- prints status messages

### QA/QC

`run_qa()` reads processed artifacts, writes a QA report, and may raise a blocking exception.

### Load

`run_load()` connects to PostgreSQL and replaces PostGIS tables inside a transaction. A successful commit changes durable database state.

These are intentional side effects defined by each stage's contract.

## Expected Versus Unexpected Side Effects

A side effect is **expected** when the function's name, documentation, contract, and calling context make it clear.

```text
append_log(...) -> expected to change a log file
run_load(...)   -> expected to change database tables
```

A side effect is **unexpected** when the caller reasonably expects no external change.

```text
normalize_columns(frame) -> surprising if it silently changes frame
```

Unexpected side effects can cause defects because another part of the program may still rely on the original object or external state.

The issue is predictability, not simply whether change occurs.

## Side Effects and Function Contracts

A useful function contract explains:

- accepted inputs
- returned output
- side effects
- failure behavior
- assumptions

For example, a contract for `append_log(rows)` could state:

```text
Input:       log row dictionaries
Return:      None
Side effect: creates the log directory and appends CSV rows
Failure:     may raise an I/O or permission exception
Assumption:  rows match the configured CSV fields
```

A `None` return value does not mean that a function did nothing. It often means the function's purpose is its side effect.

## Side Effects and Exceptions

A function can perform some side effects and then fail. This can leave partial external state.

For example, Extract writes each raw file as it downloads it. If a later dataset request fails, earlier files from that run may already exist. A Python exception does not automatically undo those writes.

Database transactions provide stronger control for database side effects:

```text
all Load changes succeed -> commit
one Load change fails     -> roll back the transaction
```

That rollback covers database work inside the transaction. It does not undo files or logs written outside it.

## Side Effects and Testing

Functions without external side effects are often easier to test because the test can compare inputs and returned outputs directly.

For functions with side effects, tests may need controlled resources such as:

- temporary directories for file writes
- mocked HTTP responses
- isolated database schemas
- captured terminal output
- copies of mutable input objects

A caller-safety test can verify that an input remains unchanged:

```python
original = frame.copy()
result = normalize_columns(frame)

assert frame.equals(original)
assert result is not frame
```

Tests should verify intended side effects and confirm that unintended ones do not occur.

## Pure Functions

A **pure function** is commonly described as a function that:

- produces the same result for the same inputs
- has no observable side effects

For example, `normalize_col_name()` calculates and returns a normalized string without intentionally changing external state.

Not every function should be pure. An ETL pipeline must read sources and publish outputs. A useful design keeps calculation and validation helpers relatively free of side effects while placing necessary external changes in clearly named stage or I/O functions.

## Plain-Language Definition

> A function side effect is an observable change or action beyond returning a value. It can be intentional, but callers should be able to understand and expect it.

## Related Resources

- [Module 0 Python foundations reference](../reference/project1_module_0_python_foundations_reference.md)
- [Module 0 Python foundations practice](../starters/project1_module_0_python_foundations_practice.ipynb)
- [Data artifacts](project1_data_artifacts.md)
- [Atomic transactions](project1_atomic_transactions.md)
- [Idempotency](project1_idempotency.md)
