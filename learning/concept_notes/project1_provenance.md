# Data Provenance

## Core Idea

Data provenance is the recorded history of where data came from, when it was obtained, what happened to it, and which artifact was produced.

It answers questions such as:

- Which source supplied this dataset?
- When was it retrieved?
- Where was the retrieved content written?
- Did the request succeed?
- How many bytes were captured?
- Which later transformations and checks were applied?

Provenance makes a data artifact traceable rather than anonymous.

## Provenance in Extract

For each configured dataset, `src/extract.py` records:

| Field | Meaning |
|---|---|
| `dataset` | project name for the layer |
| `source_url` | endpoint from which content was requested |
| `output_path` | raw file written by Extract |
| `downloaded_at_utc` | timezone-aware retrieval time |
| `http_status` | source response status |
| `bytes_written` | size of the captured response body |

These rows are written to `outputs/logs/extract_log.csv`.

The raw GeoJSON and its log row belong together as evidence of one extraction event.

## Why UTC Matters

A timestamp without a timezone can be ambiguous. The project records an aware UTC timestamp, such as:

```text
2026-07-27T15:42:18+00:00
```

UTC provides one common reference independent of the operator's local timezone or daylight-saving changes.

## Provenance Across the Pipeline

Extract provides source provenance, but broader lineage continues through later stages:

```text
source URL
    -> raw GeoJSON and extract log
    -> processed GeoJSON and transform log
    -> QA report
    -> PostGIS table and reconciliation evidence
```

Useful evidence at each stage includes:

- **Extract:** source URL, time, HTTP status, raw path, bytes
- **Transform:** input and output paths, row counts, geometry repairs, CRS, status
- **QA/QC:** inspected path, measured defects, expected CRS, pass/fail result
- **Load:** source rows, loaded rows, SRID, spatial index, committed transaction
- **Git:** version of the source code and configuration that defined the run

Together, these records help reconstruct how a published table was produced.

## Provenance Versus Reproducibility

These concepts are related but different.

- **Provenance** records what source and process produced an artifact.
- **Reproducibility** means another person can recreate the process and obtain the expected result under stated conditions.

A source URL alone is provenance evidence, but it may not make a run reproducible if the endpoint changes over time. Preserving the raw snapshot makes downstream work more repeatable.

## Provenance Versus Validation

Provenance does not prove that data is correct.

An extract log can prove that a response came from a URL at a recorded time and was written to a path. It does not prove that:

- the source itself was accurate
- the response contained every expected record
- the schema matched expectations
- the geometry was valid
- later transformations were correct

QA and reconciliation provide different evidence.

## Stale Artifact Risk

A file's existence is not enough to establish current provenance. A processed file may remain from an earlier successful run even when the current Transform attempt failed.

To associate an artifact with the current run, inspect:

- current log timestamps and statuses
- input and output paths
- row counts
- command exit status
- file modification times when useful
- a future run ID or content checksum, if implemented

The current project records stage evidence but does not yet use one shared run identifier across every stage.

## Stronger Future Provenance

Possible improvements include:

- a unique pipeline run ID
- source and output checksums
- source metadata such as version or last-modified time
- package and code commit identifiers
- row-level lineage where required
- immutable centralized run manifests

The appropriate level depends on audit, regulatory, and reproducibility needs.

## Plain-Language Definition

> Provenance is the evidence that lets you trace a data artifact back to its source and the processing events that produced it.

## Related Resources

- [Module 3 Extract reference](../reference/project1_module_3_extract_reference.md)
- [Module 3 Extract practice](../practice/project1_module_3_extract_practice.ipynb)
- [Data contracts and stage boundaries](project1_data_contracts.md)
