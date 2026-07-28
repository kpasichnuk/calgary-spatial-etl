# Project 1 Spatial Analysis Extension

## Purpose

This extension uses Project 1's QA-approved Calgary data to develop spatial reasoning alongside GIS development skills.

The ETL pipeline answers:

> Can these spatial datasets be retrieved, standardized, validated, and published reliably?

The analysis extension asks:

> What defensible geographic evidence can be produced from those trusted datasets, and how might it support a decision?

## Initial Spatial Question

> How does mapped transit-stop density vary among Calgary communities?

This wording is intentionally limited. The current datasets can support transit-stop counts, community areas, and stops per square kilometre. They do not by themselves establish:

- population equity
- transit service frequency or capacity
- walking or wheelchair accessibility
- network travel time
- household demand
- service quality

Those would require additional data and methods.

## Why Python Is Appropriate

Yes, the analysis can be completed in Python. The primary tools are:

- **GeoPandas:** spatial joins, geometry operations, tabular summaries, and inspection
- **Shapely:** geometry predicates and edge-case reasoning
- **PyProj:** CRS and measurement understanding
- **pandas:** aggregation, normalization, ranking, and comparison
- **PostGIS/SQL:** database-side spatial queries and verification after the Python method is understood
- **Jupyter notebooks:** predictions, exploratory checks, maps, written interpretation, and reproducible evidence

QGIS is optional and useful for visual inspection, cartographic review, and checking surprising locations. It does not replace the reproducible Python or SQL analysis.

## Architecture Boundary

The analysis consumes approved ETL outputs. It does not silently repair source data or change the ETL contract.

```text
City source data
    -> Project 1 ETL
    -> blocking QA
    -> approved GeoJSON/PostGIS layers
    -> analysis inputs
    -> spatial joins and summaries
    -> validation and interpretation
    -> decision-oriented communication
```

If analysis reveals a data defect, document it and repair the owning ETL stage with tests. Do not hide the repair inside an analysis notebook.

## Learning Structure

| Module | Focus | Reference | Practice | Test |
|---:|---|---|---|---|
| A0 | Spatial questions and decision value | [Reference](reference/project1_analysis_module_0_spatial_questions_reference.md) | [Practice](practice/project1_analysis_module_0_spatial_questions_practice.ipynb) | [Test](module_tests/project1_analysis_module_0_spatial_questions_test.ipynb) |
| A1 | Units, scale, CRS, and measurement | [Reference](reference/project1_analysis_module_1_measurement_scale_reference.md) | [Practice](practice/project1_analysis_module_1_measurement_scale_practice.ipynb) | [Test](module_tests/project1_analysis_module_1_measurement_scale_test.ipynb) |
| A2 | Point-in-polygon joins and aggregation | [Reference](reference/project1_analysis_module_2_spatial_joins_reference.md) | [Practice](practice/project1_analysis_module_2_spatial_joins_practice.ipynb) | [Test](module_tests/project1_analysis_module_2_spatial_joins_test.ipynb) |
| A3 | Normalization, validation, and interpretation | [Reference](reference/project1_analysis_module_3_interpretation_reference.md) | [Practice](practice/project1_analysis_module_3_interpretation_practice.ipynb) | [Test](module_tests/project1_analysis_module_3_interpretation_test.ipynb) |

Each test is worth 25 points. A recommended progression threshold is 20/25.

## Learning Sequence

Begin this extension after completing the core ETL modules and confirming that processed communities and transit stops pass QA.

For each analysis module:

1. Read the reference.
2. State predictions before running operations.
3. Complete the practice notebook.
4. Inspect at least one expected and one surprising result.
5. Complete the module test without the reference.
6. Review any assumption that could change the conclusion.

## Supporting Material

- [Spatial question workflow](guides/spatial_question_workflow.md)
- [Concept notes](concept_notes/README.md)
- [Output policy](outputs/README.md)
- [Portfolio roadmap](../planning/portfolio_roadmap.md)

## Planned Deliverables

After the learning modules, the implemented case study should produce:

- a reproducible community-level summary table
- a mapped or otherwise inspectable comparison
- checks for unmatched and boundary-sensitive transit stops
- a comparison of raw stop counts and stops per square kilometre
- a short interpretation for a defined stakeholder
- explicit limitations and next-data requirements
- tested reusable analysis functions outside the exploratory notebook

The learning resources are scaffolded first. Production analysis code should be added only after the method has been exercised and its assumptions understood.