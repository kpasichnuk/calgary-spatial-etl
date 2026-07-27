# Stage 4 Python Practice Workbook

This workbook teaches the Python skills needed for the Stage 4 field-selection exercise without asking you to memorize its finished code.

The main challenge in Stage 4 is not any one difficult statement. It is combining several smaller ideas:

1. Copy an object before changing it.
2. Loop through a list of required names.
3. Test whether each name exists.
4. Create missing columns.
5. Record which columns were missing.
6. Select columns in a requested order.
7. Return two results and unpack them.

Work through the sections in order. Type the code instead of copying and pasting it.

## How to Use This Workbook

For each exercise:

1. Predict the result on paper or in a comment.
2. Type the code in a new notebook cell or a temporary Python file.
3. Run it.
4. Compare the output with your prediction.
5. If it fails, read the error before changing anything.
6. Make one correction at a time.
7. Explain the corrected code aloud in your own words.

Do not open the solutions until you have made a genuine attempt. Looking up the documentation for one method is allowed after you first try to recall it.

## Reducing VS Code Suggestions During Practice

Temporarily reducing automatic suggestions is a good learning technique for retrieval practice. It forces you to decide what the next step should be and exposes which syntax you do not yet know.

It is not necessary to disable assistance for all programming. A useful pattern is:

- **First attempt:** disable inline completions and try from memory.
- **Second attempt:** use documentation and normal IntelliSense for method names and signatures.
- **After solving:** re-enable Copilot and compare alternatives.

To disable Copilot completions temporarily, open the Command Palette with `Ctrl+Shift+P`, search for **GitHub Copilot: Disable Completions**, and choose the workspace or current language when offered. You can re-enable them from the same menu.

To hide inline suggestions more generally, open VS Code Settings, search for `inline suggest`, and temporarily clear **Editor: Inline Suggest: Enabled**.

If you want a dedicated practice setup, add this to the workspace's `.vscode/settings.json` only while practising:

```json
{
    "editor.inlineSuggest.enabled": false
}
```

Keep ordinary IntelliSense available at first. Parameter hints, syntax highlighting, and short method-name completions are closer to documentation than to having an entire solution generated. Disable more only if you notice that you are accepting suggestions without thinking.

## Practice Setup

Run this once before the GeoPandas exercises:

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
```

Use assertions frequently. An assertion states what you believe should be true:

```python
answer = 2 + 3
assert answer == 5
```

No output means the assertion passed. An `AssertionError` means the actual behavior did not match your expectation.

# Part 1: Lists and Membership Tests

## Concept 1: Lists Preserve Order

```python
required_fields = ["name", "sector", "population"]

print(required_fields[0])
print(required_fields[-1])
print(len(required_fields))
```

Before running it, predict all three outputs.

## Exercise 1A: Build a List

Create a list named `survey_fields` containing these strings in this order:

1. `site_id`
2. `elevation`
3. `status`

Then write assertions proving the order and length are correct.

```python
# Type your solution here.
```

## Concept 2: Membership

The `in` operator asks whether a value is present:

```python
columns = ["name", "sector", "geometry"]

print("name" in columns)
print("population" in columns)
print("population" not in columns)
```

Predict whether each expression is `True` or `False`.

## Exercise 1B: Make Three Membership Checks

Given:

```python
columns = ["road_id", "road_name", "geometry"]
```

Write assertions showing that:

- `road_id` exists.
- `speed_limit` does not exist.
- `geometry` exists.

## Exercise 1C: Correct the Condition

The following condition is intended to print only absent fields, but it does the opposite:

```python
required_fields = ["name", "class", "population"]
columns = ["name", "class", "geometry"]

for field in required_fields:
    if field in columns:
        print(f"Missing: {field}")
```

Predict the incorrect output, then change exactly one part of the condition.

# Part 2: Loops and Accumulation

## Concept 3: A Loop Visits Each Item

```python
required_fields = ["name", "sector", "population"]

for field in required_fields:
    print(field)
```

During each iteration, the name `field` refers to a different string from the list.

## Exercise 2A: Trace a Loop

Without running the code, write down the value of `field` during iterations 1, 2, and 3:

```python
for field in ["stop_id", "stop_name", "status"]:
    print(field)
```

Then run it and compare.

## Concept 4: Accumulate Results with `append`

```python
missing = []
missing.append("population")
missing.append("area")

print(missing)
```

`append()` mutates the existing list by adding one item to its end.

## Exercise 2B: Collect Long Names

Complete the loop so that `long_names` contains only field names longer than six characters:

```python
fields = ["id", "name", "population", "geometry", "class"]
long_names = []

for field in fields:
    # Add a condition and append here.
    pass

assert long_names == ["population", "geometry"]
```

## Exercise 2C: Collect Missing Names

Complete the loop:

```python
available = ["name", "sector", "geometry"]
required = ["name", "sector", "population", "area"]
missing = []

for field in required:
    # If the field is absent, record it.
    pass

assert missing == ["population", "area"]
```

## Exercise 2D: Predict the Final List

Predict `missing` before running this code:

```python
available = ["a", "c"]
required = ["a", "b", "c", "d"]
missing = []

for field in required:
    if field not in available:
        missing.append(field)

print(missing)
```

# Part 3: Copies and Mutation

## Concept 5: Two Names Can Refer to One Mutable Object

```python
original = ["name", "geometry"]
working = original
working.append("population")

print("original:", original)
print("working:", working)
```

Predict both outputs. Because both names refer to the same list, mutation through `working` is visible through `original`.

## Exercise 3A: Protect the Original List

Add one method call so the assertion passes:

```python
original = ["name", "geometry"]
working = original  # Change this line.
working.append("population")

assert original == ["name", "geometry"]
assert working == ["name", "geometry", "population"]
```

## Concept 6: Copy a DataFrame Before Adding Columns

```python
original = pd.DataFrame({"name": ["A", "B"]})
working = original.copy()
working["status"] = None

print("Original columns:", list(original.columns))
print("Working columns:", list(working.columns))
```

The copy protects the caller's object from later column assignment.

## Exercise 3B: Compare Copy and No Copy

Run each block separately and explain why the results differ.

```python
# Block A
original_a = pd.DataFrame({"name": ["A"]})
working_a = original_a
working_a["population"] = None

print(list(original_a.columns))
```

```python
# Block B
original_b = pd.DataFrame({"name": ["A"]})
working_b = original_b.copy()
working_b["population"] = None

print(list(original_b.columns))
print(list(working_b.columns))
```

## Exercise 3C: Write a Copying Function

Complete the function so it adds `reviewed` only to the returned DataFrame:

```python
def add_review_column(frame: pd.DataFrame) -> pd.DataFrame:
    # Copy, add the column, and return the copy.
    pass


original = pd.DataFrame({"site_id": [1, 2]})
result = add_review_column(original)

assert "reviewed" not in original.columns
assert "reviewed" in result.columns
assert result is not original
```

# Part 4: Creating Missing Columns

## Concept 7: Column Assignment

```python
frame = pd.DataFrame({"name": ["A", "B", "C"]})
frame["population"] = None

print(frame)
print(frame["population"].isna().all())
```

Assigning `None` to a new column fills every row with a missing value.

## Exercise 4A: Add One Missing Column

Create a DataFrame with a `site_id` column, then add a `condition` column filled with `None`. Write assertions for both column order and missing values.

## Exercise 4B: Add Only What Is Missing

Complete this code:

```python
frame = pd.DataFrame({
    "name": ["Deer Ridge"],
    "sector": ["South"],
})
required = ["name", "sector", "population"]

for field in required:
    # Add the field only when it is not already present.
    pass

assert list(frame.columns) == ["name", "sector", "population"]
assert frame.loc[0, "name"] == "Deer Ridge"
assert frame["population"].isna().all()
```

Why would assigning `None` to every required field be dangerous? Test your explanation by deliberately removing the condition and observing what happens to `name` and `sector`.

## Exercise 4C: Add and Record

Combine column creation with a missing-fields list:

```python
frame = pd.DataFrame({"name": ["A"]})
required = ["name", "sector", "population"]
missing = []

for field in required:
    # If absent, create the column and record its name.
    pass

assert list(frame.columns) == ["name", "sector", "population"]
assert missing == ["sector", "population"]
```

# Part 5: Selecting and Ordering Columns

## Concept 8: Selecting with a List

```python
frame = pd.DataFrame({
    "extra": [99],
    "sector": ["North"],
    "name": ["A"],
    "geometry": ["POINT (0 0)"],
})

selected = frame[["name", "sector", "geometry"]]

print(list(frame.columns))
print(list(selected.columns))
```

The list inside `frame[...]` controls both which columns are retained and their order.

## Exercise 5A: Reorder Columns

Create `selected` with columns in this exact order:

```text
site_id, elevation, geometry
```

Use this input:

```python
frame = pd.DataFrame({
    "geometry": ["POINT (0 0)"],
    "elevation": [1045.2],
    "notes": ["checked"],
    "site_id": [7],
})
```

Assert that `notes` is absent from the result.

## Concept 9: Concatenating Lists

```python
required = ["name", "sector"]
output_columns = required + ["geometry"]

print(required)
print(output_columns)
```

The `+` operator creates a new list. It does not change `required`.

## Exercise 5B: Build an Output Schema

Given:

```python
required = ["road_id", "road_name", "class_code"]
```

Create `output_columns` by adding `geometry` to the end. Prove with assertions that:

- `output_columns` has four items.
- `geometry` is last.
- `required` still has only three items.

## Exercise 5C: Select with a Constructed List

Complete the final statement:

```python
frame = pd.DataFrame({
    "extra": [10],
    "name": ["A"],
    "sector": ["West"],
    "geometry": ["POINT (1 1)"],
})
required = ["name", "sector"]
output_columns = required + ["geometry"]

# Select output_columns from frame.
result = None

assert list(result.columns) == ["name", "sector", "geometry"]
```

# Part 6: Returning and Unpacking Two Values

## Concept 10: A Function Can Return a Tuple

```python
def divide_with_remainder(number: int, divisor: int) -> tuple[int, int]:
    quotient = number // divisor
    remainder = number % divisor
    return quotient, remainder


result = divide_with_remainder(17, 5)
print(result)
print(type(result))
```

Python packs the two returned values into a tuple.

## Concept 11: Tuple Unpacking

```python
quotient, remainder = divide_with_remainder(17, 5)

print(quotient)
print(remainder)
```

The first returned value is assigned to `quotient`, and the second is assigned to `remainder`.

## Exercise 6A: Return Two Lists

Complete this function:

```python
def split_even_odd(numbers: list[int]) -> tuple[list[int], list[int]]:
    even = []
    odd = []

    for number in numbers:
        # Append the number to the correct list.
        pass

    # Return both lists.


even_numbers, odd_numbers = split_even_odd([1, 2, 3, 4, 5, 6])

assert even_numbers == [2, 4, 6]
assert odd_numbers == [1, 3, 5]
```

## Exercise 6B: Predict an Unpacking Error

What error do you expect here, and why?

```python
def get_values():
    return "a", "b"


first, second, third = get_values()
```

Run it only after writing your prediction.

## Exercise 6C: Return Data and Metadata

Complete this function so it returns a copied DataFrame and the name of the column it added:

```python
def add_status(frame: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    # Copy frame.
    # Add a status column filled with None.
    # Return the copy and the string "status".
    pass


original = pd.DataFrame({"id": [1]})
result, added_field = add_status(original)

assert added_field == "status"
assert "status" in result.columns
assert "status" not in original.columns
```

# Part 7: Small Functions That Combine Skills

## Exercise 7A: Report Missing Fields Without Changing Data

Write this function from the requirements:

```python
def find_missing_fields(
    available_fields: list[str], required_fields: list[str]
) -> list[str]:
    pass
```

Requirements:

- Start with an empty list.
- Visit every required field.
- Append only fields not found in `available_fields`.
- Preserve the order from `required_fields`.
- Return the missing list.

Checks:

```python
assert find_missing_fields(
    ["name", "geometry"],
    ["name", "sector", "population"],
) == ["sector", "population"]

assert find_missing_fields(
    ["name", "sector", "geometry"],
    ["name", "sector"],
) == []
```

## Exercise 7B: Ensure DataFrame Columns Exist

Write this function:

```python
def ensure_columns(
    frame: pd.DataFrame, required_fields: list[str]
) -> pd.DataFrame:
    pass
```

Requirements:

- Copy the input.
- Create every absent required column with `None`.
- Do not remove extra columns.
- Return the copy.

Checks:

```python
original = pd.DataFrame({"name": ["A"], "extra": [99]})
result = ensure_columns(original, ["name", "sector"])

assert list(original.columns) == ["name", "extra"]
assert list(result.columns) == ["name", "extra", "sector"]
assert result["sector"].isna().all()
```

## Exercise 7C: Select an Ordered Schema

Write this function:

```python
def select_schema(
    frame: pd.DataFrame, required_fields: list[str]
) -> pd.DataFrame:
    pass
```

Requirements:

- Assume every required field already exists.
- Keep required fields in the given order.
- Put `geometry` last.
- Exclude all extra fields.

Checks:

```python
frame = pd.DataFrame({
    "extra": [99],
    "sector": ["North"],
    "geometry": ["POINT (0 0)"],
    "name": ["A"],
})

result = select_schema(frame, ["name", "sector"])

assert list(result.columns) == ["name", "sector", "geometry"]
assert "extra" not in result.columns
```

## Exercise 7D: Combine Two Helpers

Without changing the two helpers, call them in sequence:

```python
original = pd.DataFrame({
    "name": ["A"],
    "extra": [99],
    "geometry": ["POINT (0 0)"],
})
required = ["name", "sector", "population"]

# First ensure the columns exist.
# Then select the ordered schema.
result = None

assert list(result.columns) == ["name", "sector", "population", "geometry"]
assert "extra" not in result.columns
assert "sector" not in original.columns
```

# Part 8: GeoDataFrame Practice

## Build a Small GeoDataFrame

```python
sites = gpd.GeoDataFrame(
    {
        "site_name": ["North", "South"],
        "elevation": [1050.2, 1041.8],
        "notes": ["stable", "review"],
    },
    geometry=[Point(-114.07, 51.05), Point(-114.08, 51.04)],
    crs="EPSG:4326",
)

print(sites)
print(list(sites.columns))
print(sites.crs)
```

## Exercise 8A: Add a Missing GeoDataFrame Field

Make a copy called `working_sites`. Add a `status` column filled with `None`, then prove:

- `sites` was not changed.
- `working_sites` contains `status`.
- Geometry and CRS were preserved.

Suggested checks:

```python
assert "status" not in sites.columns
assert "status" in working_sites.columns
assert working_sites.geometry.equals(sites.geometry)
assert working_sites.crs == sites.crs
```

## Exercise 8B: Remove Extras and Reorder

From `working_sites`, select only:

```text
site_name, status, geometry
```

Call the result `site_delivery`. Confirm that `elevation` and `notes` are not included.

## Exercise 8C: Preserve the GeoDataFrame Type

Print these values:

```python
print(type(sites))
print(type(site_delivery))
print(site_delivery.crs)
```

Explain why retaining the active `geometry` column in the selection matters.

# Part 9: Debugging Drills

For each problem:

1. Predict the failure or wrong result.
2. Run the code.
3. Read the complete error.
4. Change the smallest possible part.

## Debugging 9A: Wrong Membership Direction

```python
available = ["name", "geometry"]
required = ["name", "sector"]
missing = []

for field in required:
    if field in available:
        missing.append(field)

assert missing == ["sector"]
```

## Debugging 9B: Forgot to Call `append`

```python
missing = []
missing.append
assert missing == ["population"]
```

## Debugging 9C: Appended the Whole List

```python
available = ["name"]
required = ["name", "sector"]
missing = []

for field in required:
    if field not in available:
        missing.append(required)

assert missing == ["sector"]
```

## Debugging 9D: Overwrote Existing Data

```python
frame = pd.DataFrame({"name": ["Deer Ridge"]})
required = ["name", "population"]

for field in required:
    frame[field] = None

assert frame.loc[0, "name"] == "Deer Ridge"
```

## Debugging 9E: Forgot the Copy

```python
def add_population(frame: pd.DataFrame) -> pd.DataFrame:
    frame["population"] = None
    return frame


original = pd.DataFrame({"name": ["A"]})
result = add_population(original)

assert "population" not in original.columns
```

## Debugging 9F: Selected Before Creating

```python
frame = pd.DataFrame({
    "name": ["A"],
    "geometry": ["POINT (0 0)"],
})
required = ["name", "population"]

result = frame[required + ["geometry"]]
frame["population"] = None
```

Why does statement order matter here?

## Debugging 9G: Wrong Return Shape

```python
def prepare_fields(frame):
    missing = ["population"]
    return frame


result, missing = prepare_fields(pd.DataFrame({"name": ["A"]}))
```

What must the function return for this unpacking statement to work?

# Part 10: Capstone Practice

These capstones deliberately use requirements rather than line-by-line instructions.

## Capstone A: Prepare an Inspection Table

Write:

```python
def prepare_inspection_table(
    frame: pd.DataFrame, required_fields: list[str]
) -> tuple[pd.DataFrame, list[str]]:
    pass
```

Requirements:

- Do not change the caller's DataFrame.
- Ensure every requested field exists.
- Fill absent fields with `None`.
- Record absent fields in requested order.
- Keep only requested fields, followed by `geometry`.
- Return the prepared table and the missing-field report.

Use this check:

```python
original = pd.DataFrame({
    "asset_id": [101],
    "condition": ["good"],
    "internal_note": ["do not deliver"],
    "geometry": ["POINT (2 3)"],
})

prepared, absent = prepare_inspection_table(
    original,
    ["asset_id", "condition", "inspection_date", "inspector"],
)

assert list(prepared.columns) == [
    "asset_id",
    "condition",
    "inspection_date",
    "inspector",
    "geometry",
]
assert absent == ["inspection_date", "inspector"]
assert prepared[["inspection_date", "inspector"]].isna().all().all()
assert list(original.columns) == [
    "asset_id",
    "condition",
    "internal_note",
    "geometry",
]
```

## Capstone B: Prepare a GeoDataFrame

Adapt Capstone A to this input:

```python
original_sites = gpd.GeoDataFrame(
    {
        "site_id": [1, 2],
        "site_name": ["A", "B"],
        "internal_notes": ["x", "y"],
    },
    geometry=[Point(-114.0, 51.0), Point(-114.1, 51.1)],
    crs="EPSG:4326",
)
```

Required fields:

```python
required_site_fields = ["site_id", "site_name", "status", "review_date"]
```

Write assertions proving:

- The output column order is correct.
- `status` and `review_date` are reported missing.
- The input was not changed.
- The output remains a GeoDataFrame.
- The CRS and geometry are preserved.

## Bridge Back to Stage 4

Before returning to the assessment, write this plan in plain English without code:

1. What object will you copy?
2. What collection will begin empty?
3. What list will the loop visit?
4. What condition identifies an absent field?
5. What two actions occur inside that condition?
6. How will you construct the output column order?
7. What two objects will the function return?

If you can answer all seven questions, close this guide and implement Stage 4 from the requirements only.

# Solutions

Open only the exercise you have already attempted.

<details>
<summary>Solutions for Parts 1 and 2</summary>

### Exercise 1A

```python
survey_fields = ["site_id", "elevation", "status"]

assert survey_fields[0] == "site_id"
assert survey_fields[-1] == "status"
assert len(survey_fields) == 3
```

### Exercise 1B

```python
columns = ["road_id", "road_name", "geometry"]

assert "road_id" in columns
assert "speed_limit" not in columns
assert "geometry" in columns
```

### Exercise 1C

```python
for field in required_fields:
    if field not in columns:
        print(f"Missing: {field}")
```

### Exercise 2B

```python
for field in fields:
    if len(field) > 6:
        long_names.append(field)
```

### Exercise 2C

```python
for field in required:
    if field not in available:
        missing.append(field)
```

### Exercise 2D

```text
['b', 'd']
```

</details>

<details>
<summary>Solutions for Parts 3 and 4</summary>

### Exercise 3A

```python
working = original.copy()
```

### Exercise 3C

```python
def add_review_column(frame: pd.DataFrame) -> pd.DataFrame:
    working = frame.copy()
    working["reviewed"] = None
    return working
```

### Exercise 4A

```python
frame = pd.DataFrame({"site_id": [1, 2]})
frame["condition"] = None

assert list(frame.columns) == ["site_id", "condition"]
assert frame["condition"].isna().all()
```

### Exercise 4B

```python
for field in required:
    if field not in frame.columns:
        frame[field] = None
```

### Exercise 4C

```python
for field in required:
    if field not in frame.columns:
        frame[field] = None
        missing.append(field)
```

</details>

<details>
<summary>Solutions for Parts 5 and 6</summary>

### Exercise 5A

```python
selected = frame[["site_id", "elevation", "geometry"]]

assert list(selected.columns) == ["site_id", "elevation", "geometry"]
assert "notes" not in selected.columns
```

### Exercise 5B

```python
output_columns = required + ["geometry"]

assert len(output_columns) == 4
assert output_columns[-1] == "geometry"
assert len(required) == 3
```

### Exercise 5C

```python
result = frame[output_columns]
```

### Exercise 6A

```python
def split_even_odd(numbers: list[int]) -> tuple[list[int], list[int]]:
    even = []
    odd = []

    for number in numbers:
        if number % 2 == 0:
            even.append(number)
        else:
            odd.append(number)

    return even, odd
```

### Exercise 6B

The function returns two values, but the caller asks Python to unpack three. Python raises `ValueError: not enough values to unpack`.

### Exercise 6C

```python
def add_status(frame: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    working = frame.copy()
    working["status"] = None
    return working, "status"
```

</details>

<details>
<summary>Solutions for Part 7</summary>

### Exercise 7A

```python
def find_missing_fields(
    available_fields: list[str], required_fields: list[str]
) -> list[str]:
    missing = []

    for field in required_fields:
        if field not in available_fields:
            missing.append(field)

    return missing
```

### Exercise 7B

```python
def ensure_columns(
    frame: pd.DataFrame, required_fields: list[str]
) -> pd.DataFrame:
    working = frame.copy()

    for field in required_fields:
        if field not in working.columns:
            working[field] = None

    return working
```

### Exercise 7C

```python
def select_schema(
    frame: pd.DataFrame, required_fields: list[str]
) -> pd.DataFrame:
    output_columns = required_fields + ["geometry"]
    return frame[output_columns]
```

### Exercise 7D

```python
with_required = ensure_columns(original, required)
result = select_schema(with_required, required)
```

</details>

<details>
<summary>Solutions for Part 8</summary>

### Exercise 8A

```python
working_sites = sites.copy()
working_sites["status"] = None

assert "status" not in sites.columns
assert "status" in working_sites.columns
assert working_sites.geometry.equals(sites.geometry)
assert working_sites.crs == sites.crs
```

### Exercise 8B

```python
site_delivery = working_sites[["site_name", "status", "geometry"]]

assert "elevation" not in site_delivery.columns
assert "notes" not in site_delivery.columns
```

### Exercise 8C

Selecting the active geometry column allows GeoPandas to preserve the result as a spatially aware GeoDataFrame with its CRS and geometry operations.

</details>

<details>
<summary>Debugging answers for Part 9</summary>

### Debugging 9A

Change `if field in available` to `if field not in available`.

### Debugging 9B

Call the method with the item: `missing.append("population")`.

### Debugging 9C

Append the current field rather than the entire required list: `missing.append(field)`.

### Debugging 9D

Add a membership condition before assignment so existing data is not overwritten.

### Debugging 9E

Start the function with `frame = frame.copy()` before adding the column.

### Debugging 9F

Create `population` before attempting to select it. Otherwise pandas raises a `KeyError`.

### Debugging 9G

The function must return both values in the expected order, such as `return frame, missing`.

</details>

The capstone solutions are intentionally omitted. They are the final retrieval practice before returning to Stage 4.

# Suggested Review Schedule

- **Today:** Parts 1-6, with solutions available only after each attempt.
- **Tomorrow:** Parts 7 and 8 without opening earlier solutions.
- **In three days:** Debugging drills and Capstone A.
- **In one week:** Capstone B with different field names.
- **In two weeks:** Retry Stage 4 directly from its requirements.

You do not need to memorize every method. Aim to remember the sequence of decisions, then retrieve or look up exact syntax when necessary. Frequently used syntax such as `.copy()`, `in`, `not in`, `.append()`, and column selection will become automatic through repeated use.