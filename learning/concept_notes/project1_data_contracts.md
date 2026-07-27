# Data Contracts and Stage Boundaries

## Core Idea

A data contract is the agreed structure, interpretation, quality rules, and failure behavior that data must satisfy when one system or pipeline stage passes it to another.

In this ETL pipeline, the main boundaries are:

```text
Extract -> Transform -> QA/QC -> Load
```

Each stage accepts an input, adds a guarantee, and leaves evidence.

## Shape

The shape is the technical organization of the data, including:

- expected files and datasets
- column names
- column types
- required and nullable fields
- geometry column and geometry type
- coordinate reference system
- identifier constraints
- whether an empty dataset is allowed

For example, a processed communities layer is expected to contain retained attributes plus an active geometry column in `EPSG:3347`.

## Meaning

Meaning describes what the structures represent and how they should be interpreted.

Examples:

- one row represents one community feature
- `comm_code` identifies a community
- `name` is the community name
- `geometry` represents its boundary
- coordinates are interpreted according to `EPSG:3347`
- the file represents one extracted snapshot rather than historical versions

Two fields can share the same data type while having different meanings. An identifier and a classification can both be strings, but they support different operations.

## Quality Rules

A contract also defines acceptable and unacceptable states, such as:

- required fields must exist
- geometry cannot be null, empty, or invalid
- configured identifiers cannot be null or duplicated
- CRS must equal `EPSG:3347`
- a processed layer cannot be empty

## Failure Behavior

A useful contract says what happens when a rule is violated.

In this project, QA writes diagnostic evidence and raises a blocking error when any processed layer fails. Load must not publish failed data.

## Contracts at Each Boundary

| Boundary | Accepted input | Guarantee added | Evidence |
|---|---|---|---|
| Extract output | HTTP response | stable raw snapshot and provenance | raw file and extract log |
| Transform output | raw source data | normalized fields, IDs, geometry, and CRS | processed file and transform log |
| QA output | processed candidate | explicit pass against blocking rules | QA report and successful exit |
| Load output | QA-approved layer | atomic database publication | counts, SRID, indexes, commit |

## Why Boundaries Matter

A boundary separates responsibilities. If Transform produces the wrong CRS, QA should report that defect rather than correcting it. If QA fails, Load should stop rather than publishing and checking afterward.

This makes failure ownership visible and prevents later stages from hiding earlier defects.

## Where This Project Defines Contracts

The contract is distributed across:

- `src/config.py`: expected datasets, sources, and raw paths
- `src/transform.py`: retained fields, identifiers, geometry handling, and target CRS
- `src/qa.py`: blocking rules
- `src/load.py`: destination schema, transaction, and reconciliation behavior
- tests: executable examples of accepted and rejected behavior
- learning guides: human-readable meaning and operating policy

A future project could centralize more of this metadata, but one file alone would still not replace implementation, tests, and documentation.

## Plain-Language Definition

> A data contract tells the next stage what data it will receive, what that data means, which rules it satisfies, and what must happen if those rules are broken.

## Related Resources

- [Big-picture project guide](../guides/project1_big_picture_guide.md)
- [Module 7 orchestration and testing reference](../reference/project1_module_7_orchestration_testing_reference.md)
