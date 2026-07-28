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
| A0 | Spatial questions and decision value | [Reference](reference/project1_analysis_module_0_spatial_questions_reference.md) | [Practice](starters/project1_analysis_module_0_spatial_questions_practice.ipynb) | [Test](module_tests/project1_analysis_module_0_spatial_questions_test.ipynb) |
| A1 | Units, scale, CRS, and measurement | [Reference](reference/project1_analysis_module_1_measurement_scale_reference.md) | [Practice](starters/project1_analysis_module_1_measurement_scale_practice.ipynb) | [Test](module_tests/project1_analysis_module_1_measurement_scale_test.ipynb) |
| A2 | Point-in-polygon joins and aggregation | [Reference](reference/project1_analysis_module_2_spatial_joins_reference.md) | [Practice](starters/project1_analysis_module_2_spatial_joins_practice.ipynb) | [Test](module_tests/project1_analysis_module_2_spatial_joins_test.ipynb) |
| A3 | Normalization, validation, and interpretation | [Reference](reference/project1_analysis_module_3_interpretation_reference.md) | [Practice](starters/project1_analysis_module_3_interpretation_practice.ipynb) | [Test](module_tests/project1_analysis_module_3_interpretation_test.ipynb) |

Each test is worth 25 points. Written reasoning and open-ended code are graded by AI after the notebook is complete; the learner does not assign their own points. A recommended progression threshold is an AI-reviewed 20/25.

## Learning Sequence

Begin this extension after completing the core ETL modules and confirming that processed communities and transit stops pass QA.

For each analysis module:

1. Read the reference.
2. State predictions before running operations.
3. Create an ignored practice working copy with `python scripts/reset_notebook.py <module> --analysis`.
4. Complete the practice notebook, inspect at least one expected and one surprising result, and ask AI for formative feedback.
5. Preserve completed practice with `python scripts/save_attempt.py <module> --analysis`.
6. Create and complete the module-test working copy without the reference by adding `--test` to the reset command.
7. Run every completion check, preserve the test with the save command and `--test`, then ask AI to grade the recorded work.
8. Review any assumption or misconception that could change the conclusion.

Clean originals live in `starters/`, active copies live in the ignored `working/` folder, and completed work selected for preservation lives in `attempts/`.

## AI Grading Workflow

Complete the entire test before requesting a grade. Preserve the original answers, code, assertions, and outputs so the AI review reflects the attempt rather than a corrected version. AI should apply the question point values, verify executable evidence, cite support for each award or deduction, report the final score out of 25, and identify focused review actions.

Use this prompt:

> Grade my completed spatial-analysis module-test notebook. Preserve my original answers and code. Apply the stated question values, verify the executable checks and outputs, and cite specific evidence for each awarded or deducted point. Report the final score out of 25, demonstrated strengths, misconceptions, and prioritized review actions. Ask targeted follow-up questions before giving complete corrected answers.

Use the AI-reviewed result for progression. Check feedback against the module reference and notebook evidence, and request clarification for any unsupported deduction.

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