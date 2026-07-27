# Dataset Identifiers

## Core Idea

A dataset identifier is a field whose value distinguishes one feature or record from other records in the same dataset.

For example, two transit stops might share a similar name, but each should have a distinct stable identifier.

## Identifiers in This Project

The configured identifiers are:

| Dataset | Identifier |
|---|---|
| communities | `comm_code` |
| roads | `segment_id` |
| transit stops | `globalid` |
| land-use districts | none currently configured |

These choices are defined by `ID_FIELDS` in `src/transform.py` and are used again by QA.

## Properties of a Useful Identifier

A strong identifier is normally:

- present for each record
- unique within the dataset
- stable across source snapshots
- assigned by an authoritative system
- treated as a label rather than a quantity

An identifier containing digits is not necessarily a number. For example, `"00123"` may be a code whose leading zeros are meaningful. Transform therefore converts configured identifiers to strings.

## Why Identifiers Matter

Identifiers support:

- duplicate detection
- reliable joins
- tracing features between stages
- comparing snapshots
- updating individual records
- incremental loading and upserts
- communicating which exact feature has a defect

## Not Every Dataset Requires One

A full-snapshot pipeline can process a dataset without a configured identifier when it replaces the entire destination table and does not perform record-level updates.

That is the current land-use district case. The retained `lu_code` field is a classification, not a unique feature identifier: many polygons may share the same land-use code.

It is better to configure no identifier than to falsely declare a non-unique field as unique.

## What QA Does

When an identifier is configured, QA checks that it:

- exists in the processed layer
- contains no null values
- contains no duplicate non-null values

A failure blocks publication because ambiguous or missing identities can make joins, comparisons, and updates unreliable.

When no identifier is configured, those identifier-specific checks are skipped. Other checks still apply, including file existence, fields, rows, geometry, and CRS.

## Generated Identifiers

A row number is usually a poor persistent identifier because source ordering may change between downloads.

A generated identifier based on geometry and attributes can be useful, but only after defining:

- which fields participate
- how nulls and formatting are normalized
- whether geometry coordinate order or precision may change
- what changes are allowed without changing identity
- collision handling

Use a stable source-provided identifier when one is available and trustworthy.

## Identifier Versus Classification

Consider two fields:

```text
feature_id = "polygon-8472"
lu_code    = "R-CG"
```

The first can identify one polygon. The second classifies the polygon and may appear in thousands of rows. Both can be strings, but they have different meanings.

## Related Resources

- [Module 4 Transform reference](../reference/project1_module_4_transform_reference.md)
- [Module 5 QA/QC reference](../reference/project1_module_5_qa_qc_reference.md)
