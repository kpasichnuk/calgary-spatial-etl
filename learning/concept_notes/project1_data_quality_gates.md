# Data Quality and Blocking Publication Failures

## Core Idea

Data quality means whether data is fit for its intended use under explicit rules. In this project, the immediate question is whether a processed layer is technically safe to publish to PostGIS.

A quality gate converts those rules into a control-flow decision:

```text
processed layer -> independent checks -> pass -> Load
                                  \-> fail -> stop
```

## Current Blocking Failures

Publication is blocked when any expected processed layer has:

- a missing file
- zero rows
- missing required attributes
- no active geometry column
- null geometries
- empty geometries
- invalid geometries
- null values in a configured identifier
- duplicate values in a configured identifier
- a CRS other than `EPSG:3347`
- an error that prevents inspection

These rules are enforced in `src/qa.py`.

## Why These Failures Block Load

A missing or empty layer would create an incomplete publication. Missing fields would violate the expected database structure. Invalid geometry can break or mislead spatial operations. A wrong CRS gives coordinates the wrong spatial interpretation. Null or duplicate identifiers make feature identity ambiguous when an ID is required.

Loading first and checking later would allow known defects into the published database.

## Quality Dimensions

### Completeness

Required files, records, fields, geometry, and configured identifiers are present.

### Validity

Values, geometry, and CRS satisfy technical rules.

### Uniqueness

Configured identifiers distinguish records without duplication.

### Consistency

Related layers follow shared conventions, such as one target CRS.

### Accuracy

Data represents the real world correctly enough for its use.

### Freshness

Data is recent enough for its use.

### Reconciliation

Counts or other measures agree across a stage boundary.

## Technical Quality Is Not Perfection

Passing the current QA gate does not prove that:

- every boundary exactly matches current reality
- every descriptive value is factually correct
- the source is recent enough for every possible use
- no feature is semantically duplicated
- all cross-layer relationships are correct

Those claims require additional authoritative comparisons, domain rules, freshness policies, or spatial relationship checks.

## Transform Versus QA

Transform owns repair and standardization. QA owns independent verification.

For example:

1. Transform attempts to repair invalid land-use geometry.
2. Transform writes the processed layer.
3. QA reopens that file.
4. QA independently confirms that no invalid geometry remains.

QA should not silently repair a failure because that would hide whether Transform fulfilled its responsibility.

## Blocking Versus Informational Evidence

A blocking metric determines whether publication may continue. Informational evidence helps explain the run without deciding it by itself.

Examples:

| Evidence | Role |
|---|---|
| invalid geometry count greater than zero | blocking |
| wrong CRS | blocking |
| duplicate configured ID | blocking |
| check timestamp | informational |
| input path | informational |
| nonzero row count | informational and part of an empty-layer rule |

Severity is a policy choice. A future project could add warnings for unusual but acceptable values.

## Plain-Language Definition

“Identify which quality failures must block publication” means:

> Decide which data defects are serious enough that the processed layer must not be loaded into PostGIS.

## Related Resources

- [Module 5 QA/QC reference](../reference/project1_module_5_qa_qc_reference.md)
- [Module 5 QA/QC practice](../starters/project1_module_5_qa_qc_practice.ipynb)
