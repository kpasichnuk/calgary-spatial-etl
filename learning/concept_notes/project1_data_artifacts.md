# Data Artifacts

## Core Idea

A data artifact is a saved data product that a workflow creates, consumes, or records.

An artifact may contain the data being processed, describe what happened to it, or provide evidence that a stage completed. The word *artifact* emphasizes that it is a concrete result left behind by a process.

## Artifacts in This Project

The Calgary Spatial ETL pipeline uses several kinds of data artifacts:

| Pipeline stage | Example artifact | Purpose |
|---|---|---|
| Extract | `data/raw/roads.geojson` | preserves a source snapshot |
| Extract | `outputs/logs/extract_log.csv` | records retrieval evidence |
| Transform | `data/processed/roads.geojson` | stores standardized spatial data |
| Transform | `outputs/logs/transform_log.csv` | records transformation results |
| QA/QC | a QA report in `outputs/qa/` | records quality measurements and pass/fail status |
| Load | a PostGIS `roads` table | publishes approved data for database use |

The artifacts form a chain through the workflow:

```text
City of Calgary API
        -> raw GeoJSON
        -> processed GeoJSON
        -> QA report
        -> PostGIS table
```

Each artifact represents the dataset or its evidence at a particular stage.

## Artifact Versus Process

An artifact is not the operation that creates it.

- `src/transform.py` contains code that performs a process.
- `data/processed/roads.geojson` is an artifact produced by that process.
- `src/qa.py` performs quality checks.
- The resulting QA report is an artifact that records those checks.

The code defines behavior; the artifact is a saved input, output, or record of that behavior.

## Data Artifacts and Code Artifacts

The broader software term *artifact* can also describe built packages, executables, container images, or test reports. This project usually discusses **data artifacts**, meaning files, reports, and database tables connected to the movement and validation of data.

Source code is versioned project content, but it is not normally called a data artifact here because it defines the pipeline rather than carrying or documenting a dataset through the pipeline.

## Artifacts as Evidence

Artifacts help answer operational questions:

- Did the source response get saved?
- What did Transform produce?
- Did the processed layer pass QA?
- What was loaded into PostGIS?
- Are the row counts and CRS consistent between stages?

A file's existence alone does not prove that it belongs to the latest run or that its contents are correct. Logs, timestamps, row counts, QA results, and load reconciliation provide the surrounding evidence needed to interpret it.

## Artifact Versus Provenance

These concepts are related but different:

- **Artifact:** the saved file, report, or table.
- **Provenance:** the evidence explaining where the artifact came from and how it was produced.

For example:

```text
Artifact:   data/raw/roads.geojson
Provenance: source URL, retrieval time, HTTP status, output path, and byte count
```

An artifact is the thing being traced. Provenance is its recorded history.

## Temporary and Durable Artifacts

Some artifacts are temporary intermediates; others are retained as durable project evidence.

- A raw snapshot is retained so downstream processing can be repeated without immediately querying the source again.
- A processed file is an intermediate publication candidate.
- A QA report and stage logs are retained as operational evidence.
- A PostGIS table is the final published data product for this pipeline.

Whether an artifact should be committed to Git is a separate decision. Generated data, logs, reports, and database contents can be valid artifacts even when `.gitignore` intentionally excludes them from version control.

## Plain-Language Definition

> A data artifact is a saved data product, such as a file, report, or database table, that is created, used, or recorded during a data workflow.

## Related Resources

- [Data provenance](project1_provenance.md)
- [Data contracts and stage boundaries](project1_data_contracts.md)
- [Data quality gates](project1_data_quality_gates.md)
- [Module 7 orchestration and testing reference](../reference/project1_module_7_orchestration_testing_reference.md)
