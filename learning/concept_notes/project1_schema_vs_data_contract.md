# Schema Versus Data Contract

## Core Distinction

A schema describes how data is structured. A data contract includes that schema and also defines meaning, quality rules, and expected behavior when rules fail.

```text
schema + meaning + quality rules + failure behavior = data contract
```

## What a Data Schema Defines

A data schema can specify:

- field names
- field data types
- required and nullable fields
- geometry column
- geometry type
- identifier or primary-key constraints
- CRS or SRID
- database column structure

Example:

```text
comm_code: string, required
name: string, required
sector: string, nullable
geometry: polygon, required, EPSG:3347
```

This describes technical structure but not the complete operational agreement.

## What the Contract Adds

A communities data contract can add:

### Meaning

- one row represents one Calgary community
- `comm_code` identifies the community
- `geometry` represents the community boundary

### Quality rules

- the layer cannot be empty
- `comm_code` cannot be null or duplicated
- geometry cannot be null, empty, or invalid
- CRS must be exactly `EPSG:3347`

### Failure behavior

- QA records the failed measurements
- Load does not run when the layer fails

## Two Meanings of Schema

This project uses “schema” in two related but different ways.

### Data schema

The structure of a dataset: fields, types, geometry, and constraints.

### PostgreSQL schema

A namespace that contains database objects such as tables. The default publication schema is `public`; tests and practice use isolated schemas such as `etl_test` or `etl_practice`.

A PostgreSQL schema does not by itself define the full data contract.

## How This Project Defines Structure

The current project distributes schema-related definitions across code:

- `KEEP_FIELDS` in `src/transform.py` defines retained attributes.
- `ID_FIELDS` defines configured identifiers.
- `TARGET_CRS` defines the processed CRS.
- `src/qa.py` checks fields, geometry, IDs, rows, and CRS.
- `src/load.py` controls destination schema and table publication.

There is no single formal schema document that enforces everything. The effective contract comes from configuration, transformation code, QA rules, loading logic, tests, and documentation together.

## Could a Formal Schema File Help?

Yes. A structured contract could centralize metadata such as:

```yaml
communities:
  fields:
    comm_code:
      type: string
      nullable: false
    name:
      type: string
      nullable: false
  identifier: comm_code
  geometry_type: Polygon
  crs: EPSG:3347
```

Code could then read that definition for transformation, QA, database creation, or documentation.

However, a schema file still needs executable validation. A declaration without tests or enforcement is only documentation.

## Mental Model

> **Schema:** How is the data organized?
>
> **Meaning:** What does each record and field represent?
>
> **Data contract:** What structure and meaning are promised, what quality rules apply, and what happens when the promise is broken?

## Related Resources

- [Data contracts and stage boundaries](project1_data_contracts.md)
- [Module 3 configuration reference](../reference/project1_module_3_config_reference.md)
- [Module 5 QA/QC reference](../reference/project1_module_5_qa_qc_reference.md)
