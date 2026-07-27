# config.py Deep Explanation

## File Purpose
This module is a single source of truth for dataset configuration.
Every other module (extract, transform, QA, load) can import this structure instead of hard-coding URLs and file paths in multiple places.

## Current Source

```python
DATASETS = {
    "communities": {
        "url": "https://data.calgary.ca/api/v3/views/surr-xmvs/query.geojson",
        "output": "data/raw/communities.geojson",
        "format": "geojson",
    },
    "roads": {
        "url": "https://data.calgary.ca/api/v3/views/tqjs-vnhy/query.geojson",
        "output": "data/raw/roads.geojson",
        "format": "geojson",
    },
    "transit_stops": {
        "url": "https://data.calgary.ca/api/v3/views/muzh-c9qc/query.geojson",
        "output": "data/raw/transit_stops.geojson",
        "format": "geojson",
    },
    "land_use_districts": {
        "url": "https://data.calgary.ca/api/v3/views/qe6k-p9nh/query.geojson",
        "output": "data/raw/land_use_districts.geojson",
        "format": "geojson",
    },
}
```

## Line-by-Line Breakdown

### Line 1
`DATASETS = {`
- Creates a variable named `DATASETS`.
- Assigns a Python dictionary to it.
- This is a module-level constant-style object (all caps naming convention).

Python concept:
- A dictionary stores key-value pairs.
- Syntax: `{key: value, ...}`.

### Lines 2-6 (`"communities"` block)
- Key: `"communities"`.
- Value: another dictionary containing metadata.

Inner fields:
- `url`: source endpoint to download from.
- `output`: target path for raw file output.
- `format`: expected file format.

Python concepts:
- Nested dictionaries allow grouping structured metadata.
- String keys make this easy to serialize and read.

### Lines 7-11 (`"roads"` block)
Same structure as `communities`, with roads-specific URL and output path.

Why this pattern matters:
- Uniform schema across datasets means loop-based code can process all entries identically.

### Lines 12-16 (`"transit_stops"` block)
Same schema (`url`, `output`, `format`) for transit stops.

Design advantage:
- New datasets can be added with one new block, no code changes needed in the extract loop.

### Lines 17-21 (`"land_use_districts"` block)
Same schema for land-use district data.

Operational impact:
- This lets extract code remain generic and scalable.

### Line 22
`}`
- Closes the outer `DATASETS` dictionary.

## How Other Modules Use This

Example usage pattern:

```python
for dataset_name, cfg in DATASETS.items():
    url = cfg["url"]
    output_path = cfg["output"]
```

Python concepts used here:
- `dict.items()` returns `(key, value)` pairs.
- `cfg["url"]` accesses nested dictionary values.

## Why This Is Good ETL Design
1. Centralizes configuration.
2. Improves maintainability.
3. Reduces copy/paste bugs.
4. Supports reproducibility and auditability.

## Suggested Future Enhancements
1. Add `description` for human-readable dataset purpose.
2. Add `crs_expected` for validation.
3. Add `id_field` and `keep_fields` for transform/QA reuse.
4. Add a `license` field for attribution tracking.
