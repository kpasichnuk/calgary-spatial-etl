# Project 1 Module 0: Python Foundations Reference

## Purpose

This reference teaches the Python concepts used throughout the Calgary Spatial ETL project. Use it to understand a concept before or after attempting the exercises in [Module 0 Python foundations practice](../practice/project1_module_0_python_foundations_practice.ipynb).

The notebook is for retrieval and coding practice. This document is for explanation and review.

## 1. Names, Objects, and Assignment

Python variables are names that refer to objects.

```python
dataset_name = "communities"
row_count = 313
```

The assignment operator evaluates the expression on the right and binds the resulting object to the name on the left.

Assignment does not always create a new object:

```python
original = ["name", "geometry"]
working = original
working.append("sector")
```

Both names refer to the same mutable list, so both appear changed.

## 2. Mutable and Immutable Values

Common immutable values include:

- strings
- integers
- floating-point numbers
- booleans
- tuples

Common mutable values include:

- lists
- dictionaries
- sets
- pandas DataFrames
- GeoPandas GeoDataFrames

Mutation changes an existing object. Reassignment points a name at another object.

```python
fields = ["name"]
fields.append("geometry")  # mutates the list

fields = ["id", "name"]   # reassigns the name
```

This distinction matters when a function receives an object owned by its caller.

## 3. Copies and Caller Safety

Use a copy when a function should return modified data without changing its input.

```python
def add_status(frame):
    result = frame.copy()
    result["status"] = None
    return result
```

For this project, copying helps transformation helpers remain predictable and prevents surprising changes outside the function.

For lists, compare:

```python
working = required_fields
working += ["geometry"]
```

with:

```python
output_fields = required_fields + ["geometry"]
```

The first can mutate the original list. The second builds a new list.

## 4. Lists and Order

Lists preserve order and can contain repeated values.

```python
required_fields = ["name", "sector", "population"]
```

Important operations:

```python
required_fields[0]          # first item
required_fields[-1]         # last item
len(required_fields)        # number of items
"sector" in required_fields
required_fields.append("geometry")
```

Field order matters because selecting DataFrame columns with a list also controls output order.

## 5. Dictionaries and Configuration

Dictionaries map unique keys to values.

```python
dataset = {
    "url": "https://example.test/data.geojson",
    "output": "data/raw/example.geojson",
}
```

Read a required key with square brackets:

```python
url = dataset["url"]
```

Read an optional key with `.get()`:

```python
format_name = dataset.get("format", "geojson")
```

Nested dictionaries allow one processing loop to handle multiple configured datasets.

## 6. Membership and Conditions

Membership tests answer whether a collection contains a value.

```python
if field not in frame.columns:
    frame[field] = None
```

Comparison and logical operators include:

- `==` equal
- `!=` not equal
- `<`, `<=`, `>`, `>=` numeric or ordered comparisons
- `and` both conditions must be true
- `or` at least one condition must be true
- `not` reverses a truth value

Indentation defines which statements belong to a condition.

## 7. Loops and Accumulation

A `for` loop visits each item in an iterable.

```python
missing = []

for field in required_fields:
    if field not in frame.columns:
        missing.append(field)
```

The pattern has three parts:

1. Initialize an accumulator before the loop.
2. Test each item during the loop.
3. Append only the items that satisfy the condition.

Do not recreate the accumulator inside the loop, or earlier results will be lost.

## 8. Functions and Contracts

A function groups behavior behind a name.

```python
def normalize_name(name: str) -> str:
    return name.strip().lower()
```

A useful function contract identifies:

- accepted inputs
- returned output
- side effects
- failure behavior
- assumptions

Type hints communicate intended types to readers and tools, but Python does not automatically enforce most hints at runtime.

## 9. Returning and Unpacking Multiple Values

Python can return multiple values as a tuple.

```python
def inspect_fields(frame, required):
    missing = [field for field in required if field not in frame.columns]
    return frame, missing
```

The caller can unpack the tuple:

```python
result_frame, missing_fields = inspect_fields(frame, required_fields)
```

The number and order of names must match the returned values.

## 10. Comprehensions

A list comprehension builds a list from an iterable.

```python
normalized = [name.lower() for name in original_names]
```

It can include a filter:

```python
missing = [field for field in required if field not in available]
```

Use a normal loop when the logic needs multiple steps, logging, or complex error handling.

## 11. Exceptions

Exceptions represent failures that interrupt normal execution.

```python
if not input_path.exists():
    raise FileNotFoundError(f"Missing raw file: {input_path}")
```

Catch exceptions only when the current layer can add useful context, recover safely, or translate the failure into a defined result.

```python
try:
    frame = read_layer(path)
except OSError as exc:
    return failure_result(error=str(exc))
```

Avoid broad exception handling that silently hides defects.

## 12. Paths and Context Managers

`pathlib.Path` represents filesystem paths.

```python
from pathlib import Path

output_path = Path("outputs/logs/extract_log.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
```

Context managers release resources reliably:

```python
with output_path.open("w", encoding="utf-8") as file:
    file.write("complete\n")
```

The file closes even if an exception occurs inside the block.

## 13. DataFrames and GeoDataFrames

A pandas DataFrame is a labeled table. A GeoDataFrame adds:

- an active geometry column
- CRS metadata
- spatial methods and properties

Select and order columns with a list:

```python
selected = frame[["feature_id", "name", "geometry"]]
```

Create a missing column with null values:

```python
frame["status"] = None
```

The geometry must remain in a spatial output even when it is not part of the ordinary attribute list.

## 14. Assertions and Tests

An assertion states an expected condition.

```python
assert list(result.columns) == ["name", "geometry"]
```

No output means the assertion passed. An `AssertionError` means the observed result contradicted the expectation.

Good assertions test behavior, not implementation trivia:

- output fields and order
- input remains unchanged
- missing fields are reported
- geometry remains active
- CRS has the expected value

## 15. Imports, Modules, and Entry Points

An import makes names from another module available.

```python
from src.config import DATASETS
```

The entry-point guard allows one file to be imported safely and also executed directly:

```python
if __name__ == "__main__":
    run_transform()
```

Importing the module does not run the guarded statement. Executing it as a module does.

## Common Misconceptions

- Assignment always creates a copy. It does not.
- `+=` always creates a new list. It can mutate the existing list.
- Type hints validate data automatically. Usually they do not.
- A DataFrame copy and a second name for one DataFrame are equivalent. They are not.
- Geometry is just another optional field. It is the active spatial column.
- An assertion is production error handling. It is primarily a development and testing check.
- Catching every exception makes code robust. It can instead hide failures.

## Review Checklist

You are ready for the practice notebook when you can explain:

- names versus objects
- mutation versus reassignment
- why and when to copy
- list order and membership
- dictionary configuration
- conditions, loops, and accumulators
- function inputs, outputs, side effects, and failures
- tuple return and unpacking
- exceptions and context managers
- DataFrame column selection
- GeoDataFrame geometry and CRS metadata
- assertions as executable expectations

## Companion Resources

- [Module 0 Python foundations practice](../practice/project1_module_0_python_foundations_practice.ipynb)
- [Module 0 Python namespaces reference](project1_module_0_python_namespaces_reference.md)
- [Project 1 study guide](../guides/project1_study_guide.md)