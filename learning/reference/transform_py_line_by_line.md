# transform.py Deep Explanation (Line-by-Line)

## File Purpose
This module performs the Transform stage of ETL:
1. Reads raw files downloaded by extract.
2. Standardizes schema (column names and selected fields).
3. Repairs and validates geometry.
4. Reprojects every layer to one target CRS.
5. Writes processed outputs and a transform log.

## Full Source Snapshot

```python
from pathlib import Path
from datetime import datetime, timezone
import csv
import re

import geopandas as gpd

from src.config import DATASETS


# Use one target CRS for all layers so spatial operations are consistent.
TARGET_CRS = "EPSG:3347"

# Optional field subsets by dataset (use normalized names).
# Edit these lists as you learn the exact source schema.
KEEP_FIELDS = {
    "communities": [
        "comm_code",
        "name",
        "class",
        "class_code",
        "sector",
    ],
    "roads": [
        "segment_id",
        "full_name",
        "street_type",
        "class_code",
        "one_way",
        "built_status",
    ],
    "transit_stops": [
        "teleride_number",
        "stop_name",
        "status",
        "globalid",
    ],
    "land_use_districts": [
        "lu_code",
        "label",
        "description",
        "major",
    ],
}

# If an ID field exists, cast it to string to avoid downstream join/type issues.
ID_FIELDS = {
    "communities": "comm_code",
    "roads": "segment_id",
    "transit_stops": "globalid",
    "land_use_districts": None,
}

LOG_PATH = Path("outputs/logs/transform_log.csv")


def normalize_col_name(name: str) -> str:
	# Convert to lowercase snake_case for predictable coding/SQL.
	name = name.strip().lower()
	name = re.sub(r"[^a-z0-9]+", "_", name)
	name = re.sub(r"_+", "_", name).strip("_")
	return name


def normalize_columns(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
	gdf = gdf.copy()
	gdf.columns = [normalize_col_name(c) for c in gdf.columns]
	return gdf


def processed_output_path(raw_output_path: str) -> Path:
	# Convert data/raw/<file> to data/processed/<file>.
	return Path(raw_output_path.replace("data/raw/", "data/processed/"))


def keep_required_fields(
	gdf: gpd.GeoDataFrame, keep_fields: list[str]
 ) -> tuple[gpd.GeoDataFrame, list[str]]:
	gdf = gdf.copy()
	missing = []

	# Ensure expected fields exist; create null fields if missing.
	for field in keep_fields:
		if field not in gdf.columns:
			gdf[field] = None
			missing.append(field)

	return gdf[keep_fields + ["geometry"]], missing


def cast_id_to_string(gdf: gpd.GeoDataFrame, id_field: str | None) -> gpd.GeoDataFrame:
	gdf = gdf.copy()
	if id_field and id_field in gdf.columns:
		gdf[id_field] = gdf[id_field].astype("string")
	return gdf


def repair_geom(geom):
	# Try make_valid first; fallback to buffer(0) for compatibility.
	try:
		from shapely import make_valid

		return make_valid(geom)
	except Exception:
		try:
			return geom.buffer(0)
		except Exception:
			return None


def clean_geometry(gdf: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, int, int]:
	gdf = gdf.copy()

	# Remove null and empty geometries before validation.
	gdf = gdf[gdf.geometry.notnull()]
	gdf = gdf[~gdf.geometry.is_empty]

	invalid_before = int((~gdf.is_valid).sum())

	if invalid_before > 0:
		mask = ~gdf.is_valid
		gdf.loc[mask, "geometry"] = gdf.loc[mask, "geometry"].apply(repair_geom)

	# Drop anything still invalid/null/empty after repair attempts.
	gdf = gdf[gdf.geometry.notnull()]
	gdf = gdf[~gdf.geometry.is_empty]
	gdf = gdf[gdf.is_valid]

	invalid_after = int((~gdf.is_valid).sum())
	return gdf, invalid_before, invalid_after


def ensure_crs_and_reproject(gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
	gdf = gdf.copy()

	# Calgary GeoJSON is typically EPSG:4326. Set only when missing.
	if gdf.crs is None:
		gdf = gdf.set_crs("EPSG:4326")

	return gdf.to_crs(target_crs)


def append_transform_log(rows: list[dict]) -> None:
	LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
	file_exists = LOG_PATH.exists()

	with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(
			f,
			fieldnames=[
				"dataset",
				"input_path",
				"output_path",
				"rows_in",
				"rows_out",
				"missing_fields",
				"invalid_before",
				"invalid_after",
				"crs_out",
				"processed_at_utc",
				"status",
				"error",
			],
		)
		if not file_exists:
			writer.writeheader()
		writer.writerows(rows)


def process_dataset(dataset_name: str, cfg: dict) -> dict:
	input_path = cfg["output"]
	output_path = processed_output_path(input_path)

	row = {
		"dataset": dataset_name,
		"input_path": input_path,
		"output_path": str(output_path),
		"rows_in": 0,
		"rows_out": 0,
		"missing_fields": "",
		"invalid_before": 0,
		"invalid_after": 0,
		"crs_out": TARGET_CRS,
		"processed_at_utc": datetime.now(timezone.utc).isoformat(),
		"status": "ok",
		"error": "",
	}

	try:
		if not Path(input_path).exists():
			raise FileNotFoundError(f"Missing raw file: {input_path}")

		gdf = gpd.read_file(input_path)
		row["rows_in"] = len(gdf)

		gdf = normalize_columns(gdf)

		keep_fields = KEEP_FIELDS.get(dataset_name, [])
		keep_fields = [f for f in keep_fields if f != "geometry"]
		if keep_fields:
			gdf, missing = keep_required_fields(gdf, keep_fields)
			row["missing_fields"] = ",".join(missing)

		id_field = ID_FIELDS.get(dataset_name)
		gdf = cast_id_to_string(gdf, id_field)

		gdf, invalid_before, invalid_after = clean_geometry(gdf)
		row["invalid_before"] = invalid_before
		row["invalid_after"] = invalid_after

		gdf = ensure_crs_and_reproject(gdf, TARGET_CRS)

		output_path.parent.mkdir(parents=True, exist_ok=True)
		gdf.to_file(output_path, driver="GeoJSON")
		row["rows_out"] = len(gdf)

		print(
			f"{dataset_name}: rows_in={row['rows_in']} rows_out={row['rows_out']} "
			f"invalid_before={invalid_before} invalid_after={invalid_after} "
			f"crs={TARGET_CRS} -> {output_path}"
		)

	except Exception as exc:
		row["status"] = "error"
		row["error"] = str(exc)
		print(f"{dataset_name}: ERROR -> {exc}")

	return row


def run_transform() -> None:
	# Run the same transform pipeline for each configured dataset.
	log_rows = []
	for dataset_name, cfg in DATASETS.items():
		log_rows.append(process_dataset(dataset_name, cfg))

	append_transform_log(log_rows)
	print(f"Wrote log -> {LOG_PATH}")


if __name__ == "__main__":
	# Allow direct execution: python -m src.transform
	run_transform()
```

## How to Read the Python Syntax

Before examining each section, it helps to recognize the repeated parts of a Python statement.

```python
result = function_name(argument)
```

Python evaluates the right side first. It calls `function_name(argument)`, receives the returned object, and then binds the name `result` to that object. Python variables are names that refer to objects; they are not fixed containers with a permanently declared type.

```python
object.method(argument)
```

The dot means "look up this attribute on this object." If the attribute is callable, such as `method`, the parentheses call it. For example, `gdf.copy()` asks the GeoDataFrame object referenced by `gdf` to create a copy.

```python
collection[key]
```

Square brackets retrieve an item. The meaning depends on the object:

- `cfg["output"]` retrieves a dictionary value by key.
- `gdf["geometry"]` retrieves a DataFrame column.
- `gdf[boolean_mask]` retrieves only rows where the mask is `True`.

A colon starts an indented block after statements such as `def`, `if`, `for`, `try`, `except`, and `with`. Indentation is part of Python syntax and determines which statements belong to that block.

## Detailed Explanation by Section

### 1) Imports and Dependencies

```python
from pathlib import Path
from datetime import datetime, timezone
import csv
import re

import geopandas as gpd

from src.config import DATASETS
```

An import makes code from another module available in this module.

`from pathlib import Path` means:

1. Load the standard-library module named `pathlib`.
2. Find the object named `Path` inside it.
3. Bind that object directly to the local name `Path`.

This lets the code write `Path(...)` instead of `pathlib.Path(...)`.

`import csv` and `import re` import entire modules. Their functions are accessed through the module names, such as `csv.DictWriter` and `re.sub`. This makes it visible where those functions came from.

`import geopandas as gpd` uses an alias. The module is named `geopandas`, but this file refers to it as `gpd`. The alias is conventional in GeoPandas projects and reduces repetition:

```python
gpd.read_file(input_path)
```

`from src.config import DATASETS` is an absolute project import. Python finds the `src` package, loads `config.py`, and binds its `DATASETS` object in this module. Both modules then refer to the same dictionary object unless one of them explicitly replaces or copies it.

### 2) Module-Level Constants and Collections

```python
TARGET_CRS = "EPSG:3347"
```

`=` is the assignment operator. It evaluates the string literal on the right and binds the name on the left to it. Uppercase names are a convention indicating that a value is configuration and should not normally be reassigned. Python does not enforce this convention.

```python
KEEP_FIELDS = {
	"communities": ["comm_code", "name", "class", "class_code", "sector"],
	...
}
```

Curly braces create a dictionary. A dictionary stores key-value pairs in the form `key: value`.

- A key such as `"communities"` is a string.
- Its value is a list, created with square brackets.
- Each list item is also a string.
- Commas separate dictionary entries and list items.

The structure can be described as "a dictionary whose keys are dataset names and whose values are lists of field names." A nested lookup works in two stages:

```python
community_fields = KEEP_FIELDS["communities"]
first_field = community_fields[0]
```

After these statements, `community_fields` refers to the communities list and `first_field` refers to `"comm_code"`. List positions use zero-based indexing, so `[0]` means the first item.

```python
ID_FIELDS = {
	"communities": "comm_code",
	"roads": "segment_id",
	"transit_stops": "globalid",
	"land_use_districts": None,
}
```

`None` is Python's special object for "no value." It is not the strings `"None"` or `"null"`. Here it deliberately means that the land-use dataset has no configured ID field to cast.

```python
LOG_PATH = Path("outputs/logs/transform_log.csv")
```

This calls the `Path` class. Calling a class constructs an instance, so `LOG_PATH` refers to a `Path` object rather than a plain string. A `Path` knows how to perform path operations such as `.exists()`, `.open()`, and `.parent`.

### 3) Defining and Calling Functions

```python
def normalize_col_name(name: str) -> str:
```

`def` creates a function and binds it to the name `normalize_col_name`.

- `name` is a parameter. It receives an argument when the function is called.
- `: str` is a parameter type hint saying that callers should pass a string.
- `-> str` is a return type hint saying the function should return a string.
- The final colon begins the indented function body.

Type hints are useful to readers, editors, and type checkers, but Python does not automatically reject a different type at runtime. The operations inside the function will fail only if the supplied object does not support them.

For this call:

```python
clean_name = normalize_col_name(" Road Name ")
```

Python binds the local parameter `name` to `" Road Name "`, executes the body, returns `"road_name"`, and then binds `clean_name` to that returned string.

Each function has a local namespace. Names such as `name` inside the function do not overwrite unrelated names outside it.

### 4) Normalizing One Column Name

```python
name = name.strip().lower()
```

Python evaluates chained methods from left to right:

1. `name.strip()` returns a new string without surrounding whitespace.
2. `.lower()` is called on that returned string and returns a lowercase string.
3. `name =` rebinds the local name to the final result.

Strings are immutable, so these methods do not change the original string object. They create and return new strings.

```python
name = re.sub(r"[^a-z0-9]+", "_", name)
```

`re.sub(pattern, replacement, text)` returns text with each pattern match replaced.

- The `r` prefix creates a raw string, which prevents Python from treating backslashes as Python escape characters. Raw strings are especially useful for regular expressions.
- `[...]` defines a character class.
- `^` inside the brackets means "not."
- `a-z` means lowercase letters.
- `0-9` means digits.
- `+` means one or more consecutive matches.

Therefore, one or more characters that are not lowercase letters or digits are replaced by one underscore. For example, `"road name/type"` becomes `"road_name_type"`.

```python
name = re.sub(r"_+", "_", name).strip("_")
```

This first collapses repeated underscores and then removes underscores from the beginning and end. It does not remove underscores from the middle.

```python
return name
```

`return` immediately ends the function call and sends the referenced object back to the caller. Without an explicit `return`, a Python function returns `None`.

### 5) Normalizing Every Column

```python
def normalize_columns(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
	gdf = gdf.copy()
	gdf.columns = [normalize_col_name(c) for c in gdf.columns]
	return gdf
```

`gpd.GeoDataFrame` in the hints names a class provided by GeoPandas.

`gdf = gdf.copy()` creates a separate GeoDataFrame and rebinds the local `gdf` name to the copy. Later assignments therefore do not unexpectedly rename columns in the caller's original object. This is called defensive copying.

The expression inside square brackets is a list comprehension:

```python
[normalize_col_name(c) for c in gdf.columns]
```

It is a compact form of this loop:

```python
normalized_names = []
for c in gdf.columns:
	normalized_names.append(normalize_col_name(c))
```

For each column name in `gdf.columns`, Python:

1. Binds that name temporarily to `c`.
2. Calls `normalize_col_name(c)`.
3. Adds the returned string to a new list.

The completed list is assigned to `gdf.columns`, replacing all column labels in one operation. The rows and cell values are unchanged.

### 6) Building the Processed Output Path

```python
def processed_output_path(raw_output_path: str) -> Path:
	return Path(raw_output_path.replace("data/raw/", "data/processed/"))
```

The innermost operation runs first. String `.replace(old, new)` returns a new string:

```text
data/raw/roads.geojson
		becomes
data/processed/roads.geojson
```

That string is passed to `Path(...)`, and the resulting `Path` object is returned. This illustrates function composition: the result of one call becomes the argument to another call.

### 7) Selecting Fields and Tracking Missing Ones

```python
def keep_required_fields(
	gdf: gpd.GeoDataFrame, keep_fields: list[str]
) -> tuple[gpd.GeoDataFrame, list[str]]:
```

Python permits a function signature to span multiple lines while it is inside parentheses. `list[str]` means a list expected to contain strings. The return hint `tuple[...]` says the function returns one tuple containing two objects: a GeoDataFrame and a list of strings.

```python
missing = []
```

This creates a new empty list each time the function is called. It will collect field names that were expected but absent.

```python
for field in keep_fields:
	if field not in gdf.columns:
		gdf[field] = None
		missing.append(field)
```

The `for` loop visits every item in `keep_fields`. On each iteration, `field` refers to the current string.

`not in` is a membership test. It evaluates to `True` when `field` is absent from the column index. When the condition is true:

- `gdf[field] = None` creates that DataFrame column and fills every row with a missing value.
- `missing.append(field)` mutates the list by adding the field name to its end.

```python
return gdf[keep_fields + ["geometry"]], missing
```

`keep_fields + ["geometry"]` uses list concatenation to create a new list. It does not modify `keep_fields`. If `keep_fields` is `["name", "sector"]`, the result is `["name", "sector", "geometry"]`.

Passing that list inside `gdf[...]` selects those columns in exactly that order. The comma in the `return` statement packs the two return values into a tuple.

The caller unpacks that tuple here:

```python
gdf, missing = keep_required_fields(gdf, keep_fields)
```

Python assigns the first tuple item to `gdf` and the second to `missing`. The number of names on the left must match the number of returned items.

### 8) Converting an ID Column to Text

```python
def cast_id_to_string(
	gdf: gpd.GeoDataFrame, id_field: str | None
) -> gpd.GeoDataFrame:
```

The `|` in a type hint creates a union. `str | None` means the argument may be a string or `None`.

```python
if id_field and id_field in gdf.columns:
```

`and` uses short-circuit evaluation:

1. Python first checks the truth value of `id_field`.
2. If it is `None` or an empty string, the condition is already false, so Python does not evaluate the membership test.
3. If it is a non-empty string, Python checks whether it is a column name.

This prevents the code from trying to use `None` as a configured field.

```python
gdf[id_field] = gdf[id_field].astype("string")
```

The right side selects one pandas Series and calls `.astype("string")`, which returns a converted Series. The left side assigns that converted Series back to the same column. Text IDs are safer for values where arithmetic is meaningless and leading zeros may matter.

### 9) Repairing One Geometry

```python
def repair_geom(geom):
	try:
		from shapely import make_valid

		return make_valid(geom)
	except Exception:
		try:
			return geom.buffer(0)
		except Exception:
			return None
```

This function has no type hints, so `geom` can refer to any object at runtime. The surrounding pipeline passes a Shapely geometry.

A `try` block tells Python to execute code that may raise an exception. If `make_valid(geom)` succeeds, `return` exits the function immediately and neither `except` block runs.

If an exception occurs, control jumps to `except Exception:`. `Exception` is a broad parent class covering most ordinary runtime errors. The fallback calls the geometry's `.buffer(0)` method, a traditional geometry-repair technique.

If that also raises an exception, the inner `except` returns `None`. Later cleaning steps recognize that missing geometry and remove the row.

The import is inside the function, but Python caches imported modules. Repeated calls do not normally reload Shapely from disk. The nested structure expresses an ordered fallback strategy: preferred repair, compatibility repair, then failure marker.

### 10) Boolean Masks and Geometry Cleaning

```python
gdf = gdf[gdf.geometry.notnull()]
```

This combines attribute access, a method call, and DataFrame filtering:

1. `gdf.geometry` retrieves the active geometry GeoSeries.
2. `.notnull()` creates a Boolean Series with one `True` or `False` per row.
3. `gdf[boolean_series]` keeps only rows whose value is `True`.
4. `gdf =` rebinds the local name to the filtered GeoDataFrame.

```python
gdf = gdf[~gdf.geometry.is_empty]
```

`gdf.geometry.is_empty` is a Boolean Series that is `True` for empty geometries. The unary `~` operator inverts every Boolean value, so empty rows become `False` and are excluded.

```python
invalid_before = int((~gdf.is_valid).sum())
```

The expression is evaluated from the inner parentheses outward:

1. `gdf.is_valid` produces one Boolean per geometry.
2. `~` changes valid `True` values to `False` and invalid `False` values to `True`.
3. `.sum()` counts `True` values because Boolean `True` behaves like `1` and `False` like `0` in this operation.
4. `int(...)` converts the result from a NumPy integer to a standard Python integer.

```python
if invalid_before > 0:
	mask = ~gdf.is_valid
	gdf.loc[mask, "geometry"] = gdf.loc[mask, "geometry"].apply(repair_geom)
```

`>` is a comparison operator and produces a Boolean. The repair block only runs when at least one invalid geometry exists.

`.loc[row_selector, column_selector]` selects by labels. Here:

- `mask` selects invalid rows.
- `"geometry"` selects the geometry column.
- `.apply(repair_geom)` calls `repair_geom` once for each selected geometry and returns the repaired values.
- Assignment writes those results back only into the selected cells.

The function then repeats the null, empty, and validity filters. This is important because a repair attempt can fail or return an unusable geometry.

```python
return gdf, invalid_before, invalid_after
```

This returns a three-item tuple. Its caller uses three-target unpacking:

```python
gdf, invalid_before, invalid_after = clean_geometry(gdf)
```

### 11) CRS Checking and Reprojection

```python
if gdf.crs is None:
	gdf = gdf.set_crs("EPSG:4326")
```

`is` checks object identity. Because `None` is a singleton, `is None` is the standard Python test for a missing optional value.

`set_crs` assigns CRS metadata; it does not change coordinate values. This code assumes unlabeled Calgary GeoJSON coordinates are longitude and latitude in EPSG:4326.

```python
return gdf.to_crs(target_crs)
```

`to_crs` performs the actual coordinate transformation and returns a reprojected GeoDataFrame. The distinction matters:

- `set_crs(...)` describes what the existing numbers mean.
- `to_crs(...)` calculates new coordinate numbers in another CRS.

The returned object replaces the caller's previous `gdf` when this line runs:

```python
gdf = ensure_crs_and_reproject(gdf, TARGET_CRS)
```

### 12) Writing the Transform Log

```python
def append_transform_log(rows: list[dict]) -> None:
```

`list[dict]` says `rows` should be a list of dictionaries. `-> None` communicates that the function performs a side effect, writing a file, rather than returning a useful result.

```python
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
```

`.parent` is a property, so it has no parentheses. It returns `outputs/logs`. `.mkdir(...)` then creates that directory.

- `parents=True` also creates missing ancestor directories.
- `exist_ok=True` prevents an error if the directory already exists.
- Named arguments make each Boolean's purpose clear.

```python
file_exists = LOG_PATH.exists()
```

`.exists()` returns a Boolean. This check happens before opening the file so the code knows whether a CSV header is needed.

```python
with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
```

`with` starts a context manager. `Path.open(...)` returns a file object, and `as f` binds that object to the local name `f`. Python closes the file automatically when execution leaves the block, even if an exception occurs.

- `"a"` means append mode, preserving previous log records.
- `newline=""` lets the `csv` module manage line endings correctly.
- `encoding="utf-8"` makes text encoding explicit.

```python
writer = csv.DictWriter(f, fieldnames=[...])
```

This constructs a `DictWriter` object. Its `fieldnames` list defines both CSV column order and the keys expected in every row dictionary.

```python
if not file_exists:
	writer.writeheader()
writer.writerows(rows)
```

`not` inverts the Boolean. The header is written only for a new file. `writerows` then iterates over the list and writes every dictionary as one CSV row. Notice that `writerows(rows)` is plural and accepts a collection; `writerow(row)` would write only one dictionary.

### 13) Processing One Dataset

```python
def process_dataset(dataset_name: str, cfg: dict) -> dict:
```

This function accepts a dataset-name string and one configuration dictionary, and returns one log dictionary.

```python
input_path = cfg["output"]
output_path = processed_output_path(input_path)
```

Dictionary bracket lookup requires the key to exist. If `"output"` were absent, Python would raise `KeyError`. The second statement passes the retrieved path to the helper function.

```python
row = {
	"dataset": dataset_name,
	...
	"processed_at_utc": datetime.now(timezone.utc).isoformat(),
	"status": "ok",
	"error": "",
}
```

This dictionary is initialized with every field expected by the CSV writer. Starting counters at `0` and text at `""` ensures the log has a complete schema even if processing fails early.

`datetime.now(timezone.utc)` creates a timezone-aware current UTC datetime. `.isoformat()` converts it to a standardized string such as `2026-07-25T01:05:11.098309+00:00`.

```python
if not Path(input_path).exists():
	raise FileNotFoundError(f"Missing raw file: {input_path}")
```

`raise` deliberately creates an error condition. `f"...{input_path}"` is an f-string: Python evaluates the expression inside braces and inserts its string representation. The raised exception immediately exits the `try` block and moves control to the matching `except` block.

```python
gdf = gpd.read_file(input_path)
row["rows_in"] = len(gdf)
```

`gpd.read_file` returns a GeoDataFrame. `len(gdf)` calls the object's length protocol and returns its number of rows. Dictionary item assignment updates the existing `"rows_in"` value.

```python
keep_fields = KEEP_FIELDS.get(dataset_name, [])
```

Dictionary `.get(key, default)` differs from bracket lookup. If the key is absent, it returns the supplied default instead of raising `KeyError`. The default here is a new empty list.

```python
keep_fields = [f for f in keep_fields if f != "geometry"]
```

This is a filtering list comprehension. It includes `f` in the new list only when the condition is true. The geometry column is removed from configuration because `keep_required_fields` adds it exactly once.

```python
if keep_fields:
```

Python collections have truth values. A non-empty list is truthy; an empty list is falsy. This condition therefore means "run field selection only if fields were configured."

```python
row["missing_fields"] = ",".join(missing)
```

String `.join(iterable)` combines strings using the string before the dot as a separator. If `missing` is `["field_a", "field_b"]`, the result is `"field_a,field_b"`. An empty list produces an empty string.

The remaining calls rebind `gdf` after each pipeline stage:

```python
gdf = normalize_columns(gdf)
gdf = cast_id_to_string(gdf, id_field)
gdf, invalid_before, invalid_after = clean_geometry(gdf)
gdf = ensure_crs_and_reproject(gdf, TARGET_CRS)
```

This creates a readable sequence where the output of one stage is the input to the next.

```python
output_path.parent.mkdir(parents=True, exist_ok=True)
gdf.to_file(output_path, driver="GeoJSON")
```

The first statement ensures the destination directory exists. `.to_file(...)` is a GeoDataFrame method. `driver="GeoJSON"` is a named argument selecting the output format.

The multi-line `print` call uses adjacent f-strings:

```python
print(
	f"first part "
	f"second part"
)
```

Python automatically concatenates adjacent string literals inside parentheses. Parentheses also allow the call to span lines without backslashes.

Inside an f-string, expressions such as `{row['rows_in']}` can perform dictionary lookup. The inner key uses single quotes because the surrounding f-string uses double quotes.

### 14) Handling a Dataset Failure

```python
except Exception as exc:
	row["status"] = "error"
	row["error"] = str(exc)
	print(f"{dataset_name}: ERROR -> {exc}")
```

`as exc` binds the caught exception object to `exc`. `str(exc)` asks that object for its human-readable message. The function does not re-raise the exception, so execution continues after the `except` block and reaches `return row`.

This design converts a Python exception into structured log data. It allows the outer batch loop to continue processing the other datasets. The tradeoff is that broad `Exception` handling can hide programming errors if logs are ignored, which is why recording `status` and `error` is essential.

`return row` is outside both the `try` and `except` blocks. It therefore runs after either a successful attempt or a handled failure.

### 15) Looping Through All Datasets

```python
log_rows = []
for dataset_name, cfg in DATASETS.items():
	log_rows.append(process_dataset(dataset_name, cfg))
```

`DATASETS.items()` produces each dictionary entry as a two-item pair: `(key, value)`. The loop uses tuple unpacking to bind the key to `dataset_name` and the value to `cfg`.

For one iteration, the values conceptually look like this:

```python
dataset_name = "communities"
cfg = {
	"url": "...",
	"output": "data/raw/communities.geojson",
	"format": "geojson",
}
```

Python calls `process_dataset`, waits for its returned log dictionary, and passes that dictionary directly to `log_rows.append(...)`. After all four iterations, `log_rows` contains four dictionaries.

```python
append_transform_log(log_rows)
```

This call occurs after the loop because it has the same indentation as `for`, not the deeper indentation of the loop body. Consequently, the log is written once after all datasets have been attempted.

### 16) Script Entry Point

```python
if __name__ == "__main__":
	run_transform()
```

Python automatically creates the module-level variable `__name__`.

- When run with `python -m src.transform`, `__name__` is set to `"__main__"`, so the condition is true and the pipeline runs.
- When another module executes `from src.transform import KEEP_FIELDS`, `__name__` is `"src.transform"`, so the pipeline does not run during import.

This pattern lets one file act as both reusable code and an executable script.

## One-Dataset Execution Trace

For the `communities` iteration, the main values move through the code like this:

1. `DATASETS.items()` provides `dataset_name = "communities"` and its `cfg` dictionary.
2. `cfg["output"]` returns `"data/raw/communities.geojson"`.
3. `processed_output_path(...)` returns `Path("data/processed/communities.geojson")`.
4. `gpd.read_file(...)` returns a GeoDataFrame containing 313 rows.
5. `normalize_columns(...)` returns a copy with normalized column names.
6. `KEEP_FIELDS.get(...)` returns the five configured community fields.
7. `keep_required_fields(...)` returns the selected columns plus geometry and an empty missing-fields list.
8. `ID_FIELDS.get(...)` returns `"comm_code"`, and that column is converted to pandas string dtype.
9. `clean_geometry(...)` returns the cleaned GeoDataFrame and two counts. Both community counts are zero.
10. `ensure_crs_and_reproject(...)` transforms the coordinates to EPSG:3347.
11. `gdf.to_file(...)` writes the processed GeoJSON.
12. `process_dataset(...)` returns its completed `row` dictionary.
13. `log_rows.append(...)` stores that dictionary for the final CSV write.

The same function is reused for each dataset. The changing configuration values control which file and fields it processes, while the transformation algorithm stays the same.

## Verified Result

The current pipeline was run successfully against all four raw datasets. Every processed output uses EPSG:3347, contains its expected columns, and has no null or invalid geometries. The land-use layer had 43 invalid geometries before cleaning and zero afterward.

The broad `except Exception` statements may still appear as lint warnings. They are not syntax or runtime failures; they are a deliberate batch-processing choice in this learning version of the ETL pipeline.
