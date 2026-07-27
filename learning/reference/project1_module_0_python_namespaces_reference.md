# Project 1 Module 0: Python Namespaces Reference

## What Is a Namespace?

A **namespace** is a mapping between names and the Python objects those names currently refer to. You can think of it like a dictionary:

```python
{
    "TARGET_CRS": "EPSG:3347",
    "normalize_columns": <function object>,
    "gdf": <GeoDataFrame object>,
}
```

Python uses multiple namespaces while a program runs. In this project, the most important ones are:

1. The module or script namespace.
2. Each function call's local namespace.

A namespace manages **names**. It does not automatically copy or isolate the objects to which those names refer.

## The Script or Module Namespace

When Python executes `src/transform.py`, it creates a module namespace for that file. This is also commonly called the module's **global namespace**.

Names created outside functions belong to it:

```python
TARGET_CRS = "EPSG:3347"
KEEP_FIELDS = {...}
ID_FIELDS = {...}
LOG_PATH = Path(...)


def normalize_columns(...):
    ...
```

Conceptually, the module namespace contains entries like these:

```python
{
    "Path": <Path class>,
    "csv": <csv module>,
    "re": <re module>,
    "gpd": <geopandas module>,
    "DATASETS": <dictionary>,
    "TARGET_CRS": "EPSG:3347",
    "KEEP_FIELDS": <dictionary>,
    "ID_FIELDS": <dictionary>,
    "LOG_PATH": <Path object>,
    "normalize_columns": <function object>,
    "process_dataset": <function object>,
    "run_transform": <function object>,
}
```

These names become available as Python executes their statements. They normally remain in the module namespace while the module is loaded.

"Global" in this context means global **within this module**. It does not mean the name is automatically available in every Python file.

## A Function's Local Namespace

Every time a function is called, Python creates a new local namespace for that particular call.

Consider this function:

```python
def normalize_columns(gdf):
    gdf = gdf.copy()
    return gdf
```

When it is called:

```python
result = normalize_columns(original_gdf)
```

Python first creates a local namespace that conceptually looks like this:

```python
{
    "gdf": <original GeoDataFrame>,
}
```

The parameter name `gdf` initially refers to the same GeoDataFrame object as the caller's name `original_gdf`. Passing an object to a function does not automatically copy it.

After this line runs:

```python
gdf = gdf.copy()
```

The function's local namespace changes to:

```python
{
    "gdf": <copied GeoDataFrame>,
}
```

The local name `gdf` is now bound to the copy. The caller's name `original_gdf` still refers to the original object.

When the function returns, its local namespace is discarded. The copied object can remain alive because the caller binds `result` to it:

```python
result = normalize_columns(original_gdf)
```

## How Python Finds a Name: LEGB

When Python encounters a name, it generally searches namespaces using the **LEGB** order:

1. **Local**: the current function call.
2. **Enclosing**: an outer function, when functions are nested.
3. **Global**: the current module or script.
4. **Built-in**: names supplied by Python, such as `len`, `str`, and `print`.

Consider this function:

```python
def process_dataset(dataset_name, cfg):
    row = {
        "crs_out": TARGET_CRS,
    }
```

The function's local namespace contains `dataset_name`, `cfg`, and then `row`. It does not contain `TARGET_CRS`, so Python searches outward and finds `TARGET_CRS` in the `transform.py` module namespace.

In this statement:

```python
row["rows_in"] = len(gdf)
```

Python finds the names in different places:

- `row` is in the current function's local namespace.
- `gdf` is in the current function's local namespace.
- `len` is found in Python's built-in namespace.

## The Same Name Can Exist in Different Namespaces

The module and a function can both have a name called `gdf`:

```python
gdf = "module-level value"


def example(gdf):
    print(gdf)
```

Calling the function like this:

```python
example("function value")
```

prints:

```text
function value
```

Inside the function, the local parameter `gdf` takes priority over the module-level `gdf`. This is called **shadowing**.

The names exist separately and can refer to different objects:

```text
Module namespace:
gdf ----------> "module-level value"

Function namespace:
gdf ----------> "function value"
```

## Assignment Inside a Function

By default, assigning a name inside a function creates or rebinds a local name:

```python
TARGET_CRS = "EPSG:3347"


def example():
    TARGET_CRS = "EPSG:4326"
```

The assignment inside `example` does not change the module-level value:

```text
Module TARGET_CRS: EPSG:3347
Local TARGET_CRS:  EPSG:4326
```

When the function finishes, its local `TARGET_CRS` name disappears.

A function can read a module-level name without assigning to it:

```python
def example():
    print(TARGET_CRS)
```

Python does not find `TARGET_CRS` locally, so it continues searching and finds it in the module namespace.

## Rebinding a Name Versus Mutating an Object

This distinction is essential when working with mutable objects such as lists, dictionaries, DataFrames, and GeoDataFrames.

### Rebinding a local name

```python
def example(gdf):
    gdf = gdf.copy()
```

The assignment changes what the function's local name `gdf` refers to. It does not rebind the caller's variable.

Before the copy:

```text
caller's original_gdf ----+
                          +----> Original GeoDataFrame
function's local gdf -----+
```

After `gdf = gdf.copy()`:

```text
caller's original_gdf --------> Original GeoDataFrame
function's local gdf ---------> Copied GeoDataFrame
```

### Mutating a shared object

```python
def example(gdf):
    gdf["new_column"] = None
```

If no copy was made, the caller's name and the function's local name refer to the same GeoDataFrame. Adding a column mutates that shared object, so the change is visible through both names.

Namespaces isolate names, but they do not automatically isolate mutable objects. That is why this project's helper functions call `gdf.copy()` before modifying a GeoDataFrame.

## Namespace Flow in the Transform Pipeline

Consider these statements inside `process_dataset`:

```python
gdf = gpd.read_file(input_path)
gdf = normalize_columns(gdf)
```

There are two different local namespaces using the name `gdf`.

Before `normalize_columns` is called:

```text
process_dataset local namespace:
gdf ----------> Original GeoDataFrame
```

When `normalize_columns(gdf)` begins, its parameter initially refers to the same object:

```text
process_dataset local gdf ----+
                              +----> Original GeoDataFrame
normalize_columns local gdf --+
```

Inside `normalize_columns`, this runs:

```python
gdf = gdf.copy()
```

Only the helper function's local name is rebound:

```text
process_dataset local gdf ------> Original GeoDataFrame
normalize_columns local gdf ----> Copied GeoDataFrame
```

The helper then modifies and returns the copy:

```python
return gdf
```

Finally, the assignment in `process_dataset` receives the returned object:

```python
gdf = normalize_columns(gdf)
```

Its local `gdf` name is rebound to the returned copy:

```text
process_dataset local gdf ------> Copied and normalized GeoDataFrame
```

This pattern allows each helper function to create and return a transformed GeoDataFrame while `process_dataset` controls which returned object becomes the input to the next stage.

## Namespaces Are Created Per Function Call

Each call gets its own local namespace, even when the same function is called repeatedly:

```python
first_result = normalize_col_name("Road Name")
second_result = normalize_col_name("Stop Name")
```

The first call gets a local `name` bound to `"Road Name"`. After that call returns, its local namespace is discarded. The second call gets a new local `name` bound to `"Stop Name"`.

The calls do not share their local variables. They can share module-level objects if the function reads or mutates those objects.

## Summary

- A namespace maps names to objects.
- `transform.py` has a module-level or global namespace.
- Every function call receives a new local namespace.
- Function parameters initially refer to the objects passed by the caller; Python does not automatically copy them.
- `gdf.copy()` creates a separate GeoDataFrame object.
- `gdf = gdf.copy()` rebinds only the function's local `gdf` name.
- Names are generally resolved using Local, Enclosing, Global, and Built-in order.
- Local and module-level namespaces can contain the same name while referring to different objects.
- Rebinding changes the relationship between a name and an object.
- Mutation changes the object itself and is visible through every name that refers to that object.
