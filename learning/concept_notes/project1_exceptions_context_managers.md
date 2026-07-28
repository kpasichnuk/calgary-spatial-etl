# Exceptions and Context Managers

## Core Distinction

An **exception** is an object representing a failure or unusual condition that interrupts normal control flow.

A **context manager** defines setup and cleanup behavior around a block of code, usually through a `with` statement.

They often work together, but they are not the same mechanism:

```text
exception       -> reports and propagates a failure
context manager -> manages entering and leaving a resource or operation scope
```

A context manager still performs cleanup when an exception occurs inside its block.

## A Context Manager Is a Python Object

Context management is a Python language feature. The `with` and `as` words are Python syntax, while the **context manager is the Python object** used by that syntax.

```python
with open("extract_log.csv", "a", encoding="utf-8") as file:
    file.write("Extract completed\n")
```

In this example:

- `with` and `as` are Python keywords
- `open(...)` returns a file object that acts as a context manager
- `file` refers to the opened resource inside the block
- Python closes the file when execution leaves the block

An object acts as a context manager by following Python's **context-management protocol**. It provides entry and exit behavior, normally through the special methods `__enter__()` and `__exit__()`:

```python
class ExampleContextManager:
    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exception_type, exception, traceback):
        print("Leaving")
```

You usually use existing context managers rather than writing these methods yourself. Python file objects, temporary directories, and SQLAlchemy transactions all follow this same protocol.

In plain terms, `with` is the Python instruction to use managed setup and cleanup, and the context manager is the object that knows how to perform that setup and cleanup.

## Raising an Exception

Use `raise` when a function cannot fulfill its contract and the caller needs to know why.

The Load stage rejects a missing approved input:

```python
if not path.exists():
    raise FileNotFoundError(f"Missing QA-approved file: {path}")
```

It rejects a layer without CRS metadata:

```python
if gdf.crs is None:
    raise ValueError(f"{dataset_name}: cannot load data without a CRS")
```

Raising stops the current normal path. Python searches outward through the active function calls for a compatible `except` handler. If none exists, the program reports the uncaught exception and exits that operation.

## Exception Types Communicate Meaning

Different exception classes describe different categories of failure:

| Exception | Typical meaning in this project |
|---|---|
| `FileNotFoundError` | an expected input artifact does not exist |
| `ValueError` | a supplied value violates a requirement |
| `KeyError` | a required mapping or DataFrame key is absent |
| `OSError` | a filesystem or operating-system operation failed |
| `RuntimeError` | execution reached an invalid operational result |
| `QualityGateError` | one or more layers failed blocking QA rules |

Choosing a meaningful type lets callers handle only the failures they understand.

## Catching an Exception

A `try` block marks code that may raise. An `except` block handles compatible failures:

```python
try:
    frame = read_layer(path)
except OSError as error:
    return failure_result(error=str(error))
```

Here, `error` refers to the caught exception object. The handler translates the exception into a structured failure result.

Catching an exception is appropriate when the current layer can:

- recover safely
- add useful context
- translate it into a defined result
- perform necessary cleanup not already managed elsewhere

If the current layer cannot do one of those things, allowing the exception to propagate is often clearer.

## Targeted Versus Broad Handling

QA catches a selected group of expected inspection failures:

```python
except (FileNotFoundError, KeyError, OSError, ValueError) as error:
    ...
```

This communicates which failures become a normal failed QA result.

Transform's geometry fallback uses broader handling:

```python
try:
    return make_valid(geometry)
except Exception:
    try:
        return geometry.buffer(0)
    except Exception:
        return None
```

That broad catch is part of a deliberate fallback chain: preferred repair, compatibility repair, then a failure marker removed later. Broad `except Exception` elsewhere can conceal programming defects, so it should have a narrow, explicit purpose.

Never use an empty handler such as:

```python
try:
    risky_operation()
except Exception:
    pass
```

It discards evidence and can make a failed operation appear successful.

## Exception Propagation Through the Pipeline

An uncaught exception moves outward through callers until something handles it.

```text
load_layer() raises
    -> run_load() transaction exits
    -> SQLAlchemy rolls back
    -> run_pipeline() stops
    -> command reports failure
```

This is useful control flow. A failed Load precondition should stop the pipeline rather than allow later code to imply publication succeeded.

## The `finally` Block

A `finally` block runs when control leaves the associated `try`, whether the block succeeds, returns, or raises an exception.

The Load stage uses it to dispose an engine that it created:

```python
try:
    ...
finally:
    if owns_engine:
        active_engine.dispose()
```

`finally` is useful for unconditional cleanup. Context managers often provide a more focused and reusable way to express resource cleanup.

## Context Managers and `with`

A context manager controls what happens when execution enters and exits a block:

```python
with resource_manager() as resource:
    use(resource)
```

Conceptually:

```text
enter context
    -> acquire or configure resource
    -> run block
exit context
    -> release, commit, roll back, or otherwise clean up
```

The exit behavior runs even when the block raises an exception.

## File Context Managers

Extract appends its log inside a file context manager:

```python
with LOG_PATH.open("a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=...)
    writer.writerows(rows)
```

The file is closed when the block exits. This happens on success and when writing raises an exception.

Without managed cleanup, an open file descriptor could remain allocated longer than intended, and buffered data might not be flushed correctly.

## Temporary-Directory Context Managers

Tests use `TemporaryDirectory()`:

```python
with TemporaryDirectory() as temporary:
    path = Path(temporary) / "sites.geojson"
    create_test_layer(path)
```

The temporary directory is created on entry and removed on exit. This isolates test artifacts and avoids leaving files in the project directories.

Cleanup still runs if an assertion or tested function raises inside the block.

## Transaction Context Managers

Load uses SQLAlchemy's transaction context manager:

```python
with active_engine.begin() as connection:
    for dataset_name, config in DATASETS.items():
        load_layer(connection, dataset_name, ...)
```

Its exit behavior depends on the block outcome:

```text
block succeeds          -> commit transaction
exception leaves block  -> roll back transaction
```

The context manager does not make failures disappear. It performs the correct transaction cleanup and normally allows the exception to continue outward.

## Nested Context Managers

The rollback integration test nests three managed scopes:

```python
with TemporaryDirectory() as temporary:
    with self.assertRaises(RuntimeError):
        with self.engine.begin() as connection:
            load_layer(connection, "rollback_sites", path, self.schema)
            raise RuntimeError("force rollback")
```

From inside outward:

1. the transaction sees `RuntimeError` and rolls back
2. `assertRaises` verifies that `RuntimeError` occurred and treats it as the expected test outcome
3. `TemporaryDirectory` removes the test files

Nesting works because each context manager owns one responsibility.

## Can a Context Manager Suppress an Exception?

Yes. A context manager may choose to suppress a particular exception during exit.

`self.assertRaises(RuntimeError)` intentionally does this after confirming the expected exception occurred. The test then continues.

File and transaction context managers generally perform cleanup without treating an operational exception as success. Whether suppression occurs is part of the context manager's contract.

## Common Mistakes

### Catching Too Early

Catching a failure before a layer can add meaningful handling often produces vague logs or false success.

### Catching Too Broadly

A broad handler can accidentally convert programming defects into ordinary failure results.

### Forgetting the Original Cause

When translating an exception, preserve useful context through the message or exception chaining:

```python
raise RuntimeError("Could not publish roads") from error
```

### Assuming Cleanup Means Recovery

Closing a file or rolling back a transaction leaves resources in a controlled state. It does not mean the requested operation succeeded.

### Using Exceptions for Ordinary Branching

Expected alternatives such as an optional dictionary key are often clearer with `.get()` or an explicit membership test. Exceptions should represent contract failures or conditions best expressed by the called API.

## Plain-Language Definitions

> An exception is a failure signal that interrupts normal execution until it is handled or reaches the program boundary.

> A context manager controls setup and cleanup around a `with` block, including cleanup when an exception occurs.

## Related Resources

- [Module 0 Python foundations reference](../reference/project1_module_0_python_foundations_reference.md)
- [Module 0 Python foundations practice](../starters/project1_module_0_python_foundations_practice.ipynb)
- [Atomic transactions](project1_atomic_transactions.md)
- [Function side effects](project1_function_side_effects.md)
- [Data quality gates](project1_data_quality_gates.md)
