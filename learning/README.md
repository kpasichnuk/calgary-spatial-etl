# Project 1 Learning Modules

## Learning Path

Start with Module 0 and complete the modules in numerical order. Each module builds on guarantees and vocabulary introduced earlier.

For every module:

1. Read the teaching reference.
2. Complete the practice notebook and its self-checks.
3. Close the reference and practice notebook.
4. Complete the module test from memory.
5. Score the written responses honestly and run all executable checks.
6. Continue only after earning at least 20/25 (80%).
7. Review missed objectives and retake the test when the score is below 80%.

## Naming Convention

Module-specific resources use lowercase snake case:

```text
project1_module_<number>_<topic>_<resource_type>.<extension>
```

Examples:

- `project1_module_0_python_foundations_reference.md`
- `project1_module_0_python_foundations_practice.ipynb`
- `project1_module_0_python_foundations_test.ipynb`

The module number defines learning order. The final term defines the resource role: `reference`, `practice`, or `test`.

Curriculum-wide guides, walkthroughs, and cumulative assessments do not carry a module number because they span multiple modules.

## Modules in Order

| Module | Focus | Teaching reference | Practice notebook | End-of-module test |
|---:|---|---|---|---|
| 0 | Python foundations | [Foundations](reference/project1_module_0_python_foundations_reference.md) and [namespaces](reference/project1_module_0_python_namespaces_reference.md) | [Practice](practice/project1_module_0_python_foundations_practice.ipynb) | [Test](module_tests/project1_module_0_python_foundations_test.ipynb) |
| 1 | Environment and PostGIS setup | [Reference](reference/project1_module_1_environment_postgis_reference.md) | [Practice](practice/project1_module_1_environment_postgis_practice.ipynb) | [Test](module_tests/project1_module_1_environment_postgis_test.ipynb) |
| 2 | Git and version control | [Reference](reference/project1_module_2_git_reference.md) | [Practice](practice/project1_module_2_git_practice.ipynb) | [Test](module_tests/project1_module_2_git_test.ipynb) |
| 3 | Configuration and Extract | [Configuration](reference/project1_module_3_config_reference.md) and [Extract](reference/project1_module_3_extract_reference.md) | [Practice](practice/project1_module_3_extract_practice.ipynb) | [Test](module_tests/project1_module_3_extract_test.ipynb) |
| 4 | Transform | [Reference](reference/project1_module_4_transform_reference.md) | [Practice](practice/project1_module_4_transform_practice.ipynb) | [Test](module_tests/project1_module_4_transform_test.ipynb) |
| 5 | QA/QC and the quality gate | [Reference](reference/project1_module_5_qa_qc_reference.md) | [Practice](practice/project1_module_5_qa_qc_practice.ipynb) | [Test](module_tests/project1_module_5_qa_qc_test.ipynb) |
| 6 | Load and PostGIS publication | [Reference](reference/project1_module_6_load_postgis_reference.md) | [Practice](practice/project1_module_6_load_postgis_practice.ipynb) | [Test](module_tests/project1_module_6_load_postgis_test.ipynb) |
| 7 | Orchestration, testing, and troubleshooting | [Reference](reference/project1_module_7_orchestration_testing_reference.md) | [Practice](practice/project1_module_7_orchestration_testing_practice.ipynb) | [Test](module_tests/project1_module_7_orchestration_testing_test.ipynb) |

## Why This Order

### Module 0: Python Foundations

Learn names, objects, collections, functions, paths, exceptions, DataFrames, GeoDataFrames, and namespaces before reading project implementation code.

### Module 1: Environment and PostGIS

Learn how the repository, interpreter, dependencies, Docker service, PostgreSQL database, and PostGIS extension form the runtime context.

### Module 2: Git

Learn to inspect, stage, test, commit, recover, and protect secrets before making project changes.

### Module 3: Configuration and Extract

Learn the shared dataset contract first, then use it to retrieve and preserve source snapshots with provenance.

### Module 4: Transform

Use the raw snapshot and configuration to standardize fields, identifiers, geometry, and CRS.

### Module 5: QA/QC

Independently inspect transformed artifacts and block data that violates the project contract.

### Module 6: Load and PostGIS

Publish only QA-approved data, then reconcile counts, SRID, indexes, and transaction behavior.

### Module 7: Orchestration and Testing

Connect all previous stages in dependency order and learn how different forms of verification support operational confidence.

## After Module 7

Use these curriculum-wide resources after passing every module test:

1. Follow the [ETL walkthrough](walkthroughs/project1_etl_walkthrough.ipynb) to review the connected implementation.
2. Complete the [learning assessment](assessments/project1_learning_assessment.ipynb) for stage-level retrieval and coding.
3. Complete the [big-picture assessment](assessments/project1_big_picture_assessment.ipynb) for cumulative operational reasoning.
4. Revisit the [study guide](guides/project1_study_guide.md) and [big-picture guide](guides/project1_big_picture_guide.md) for weak areas and runbook details.
5. Use the [junior GIS developer guide](guides/project1_junior_gis_developer_guide.md) to frame the project for a portfolio or interview.

## Concept Notes

Use the [concept notes](concept_notes/README.md) for focused explanations of questions that arise while reading the guides. Current topics cover GitHub publication, dataset identifiers, data quality gates, coordinate reference systems, data contracts, schemas, provenance, and idempotency.

## Resource Roles

- **Reference:** teaches concepts, mental models, common mistakes, and review criteria.
- **Practice:** builds skills through guided exercises and immediate self-checks.
- **Module test:** measures closed-note retention at the end of one module.
- **Walkthrough:** demonstrates the connected project workflow.
- **Guide:** explains curriculum-wide concepts or operating decisions.
- **Concept note:** gives a focused explanation of one term or closely related idea.
- **Assessment:** measures cumulative understanding across multiple modules.

Generated data, QA reports, logs, credentials, local environments, and editor state are project artifacts rather than learning resources and should not be added to this index.