# Project 1 Module 5: QA/QC Reference

## Purpose

This reference teaches the quality concepts behind [Module 5 QA/QC practice](../starters/project1_module_5_qa_qc_practice.ipynb) and `src/qa.py`.

## 1. QA, QC, and the Quality Gate

Quality assurance emphasizes the process and controls used to prevent defects. Quality control emphasizes inspection of actual outputs.

A practical ETL quality stage contains both ideas. Its most important role is the **quality gate**: processed data must satisfy explicit rules before Load can publish it.

## 2. Stage Boundary

QA/QC accepts processed GeoJSON from Transform. It does not accept raw API data and should not silently repair defects.

```text
processed candidate
    -> independent checks
    -> pass or blocking failure
    -> QA report
```

Repair belongs in Transform. QA/QC independently verifies the result.

## 3. Quality Dimensions

### Completeness

Required files, rows, fields, geometry, and IDs are present.

### Validity

Values, geometries, and CRS satisfy defined technical rules.

### Uniqueness

Configured identifiers do not ambiguously describe multiple features.

### Consistency

Related representations agree, such as every layer using the expected target CRS.

### Accuracy

Data reflects real-world conditions closely enough for its intended use. Technical validity alone does not prove accuracy.

### Freshness

Data is recent enough for the use case.

### Referential integrity

Keys that refer to another dataset identify existing records.

### Reconciliation

Counts, totals, or identifiers agree across stage boundaries.

## 4. Current Blocking Checks

For every configured processed layer, the project checks:

- the file exists
- at least one row exists
- expected attributes exist
- the active geometry column exists
- no geometry is null
- no geometry is empty
- no geometry is invalid
- configured IDs are not null
- configured IDs are not duplicated
- CRS equals `EPSG:3347`

Any failed layer blocks the QA run.

## 5. Independent Inspection

QA/QC reopens processed files rather than trusting Transform's in-memory result or log.

This catches problems such as:

- a file was not written
- serialization changed a type or CRS
- an older artifact is being inspected
- Transform's claimed status disagrees with the actual file

Independent inspection reduces shared assumptions between stages.

## 6. QAResult as Structured Evidence

`QAResult` is a frozen dataclass that records one dataset's measurements and outcome.

Structured results are preferable to free-form print statements because they can be:

- written to CSV
- compared in tests
- aggregated across datasets
- inspected by another program
- extended with new metrics

A result includes measured counts, expected CRS, pass/fail status, time, and an error message.

## 7. Pass, Warning, and Failure

The current implementation primarily uses pass or blocking failure. A broader system may add:

- **pass:** rule satisfied
- **warning:** unusual but publication may continue under policy
- **failure:** publication must stop
- **diagnostic:** context that does not make a decision

Severity must be explicit. Printing a warning without a defined consequence is not a quality policy.

## 8. Reporting

The QA report is written to `outputs/qa/qa_report.csv`.

A useful report answers:

- what dataset was checked
- which artifact was inspected
- what was measured
- what was expected
- whether it passed
- when it was checked
- what error occurred

Generated reports are operational artifacts and remain outside Git history.

## 9. QualityGateError

After inspecting all layers and writing the report, `run_qa` raises `QualityGateError` when any dataset fails.

This design provides both:

- complete diagnostic evidence across datasets
- a non-successful control-flow result that prevents downstream Load

A report alone is not enough if the pipeline continues as though it passed.

## 10. Geometry Quality

Distinguish:

- **null:** no geometry value
- **empty:** geometry object with no coordinates
- **invalid:** coordinates violate geometry rules
- **inaccurate:** geometry may be structurally valid but not represent reality correctly

QA can test the first three mechanically. Accuracy usually requires authoritative comparison, domain review, or field evidence.

## 11. Identifier Quality

A configured ID should be present and unique when it represents one feature.

Null IDs prevent reliable identification. Duplicate IDs make joins, updates, and reconciliation ambiguous.

Not every dataset necessarily has a single natural ID. The quality rule must match the dataset contract.

## 12. Testing Quality Rules

Good tests include both acceptance and rejection:

- valid layer passes
- duplicate ID fails
- missing file returns an actionable result
- wrong CRS fails
- null or invalid geometry fails

Controlled temporary data keeps tests deterministic and protects project outputs.

## 13. Failure Ownership

When QA fails:

1. Read the failed metric and dataset.
2. Inspect the processed artifact.
3. Determine whether the source, Transform rule, or QA expectation owns the issue.
4. Fix the owning stage or contract.
5. Regenerate downstream artifacts.
6. Rerun QA before Load.

Do not edit the QA report to make a failure disappear.

## 14. Future Quality Controls

Possible extensions include:

- expected geometry types
- accepted value domains
- numeric ranges
- null-rate thresholds
- spatial extent checks
- referential integrity
- freshness thresholds
- source-to-processed reconciliation
- distribution-change warnings
- cross-layer spatial relationships

Each control needs an owner, severity, threshold, and diagnostic message.

## Common Misconceptions

- A file existing means it is acceptable. It does not.
- Valid geometry proves geographic accuracy. It does not.
- QA should repair defects. Repair belongs in Transform.
- A printed failure automatically blocks Load. Control flow must enforce it.
- All unusual values should block publication. Severity depends on the contract and use case.

## Review Checklist

You should be able to explain:

- QA versus QC
- quality gate and blocking behavior
- completeness, validity, uniqueness, consistency, and reconciliation
- null, empty, invalid, and inaccurate geometry
- why QA reopens processed files
- structured results and reports
- failure ownership and safe reruns

## Companion Resources

- [Module 5 QA/QC practice](../starters/project1_module_5_qa_qc_practice.ipynb)
- [Module 4 Transform reference](project1_module_4_transform_reference.md)
- [Module 6 Load/PostGIS reference](project1_module_6_load_postgis_reference.md)
