# Project 1 Learning Modules

## Learning Path

Start with Module 0 and complete the modules in numerical order. Each module builds on guarantees and vocabulary introduced earlier.

For every module:

1. Read the teaching reference.
2. Create an ignored practice working copy with the reset command below.
3. Complete the working copy and its self-checks, then ask AI for formative feedback.
4. Save the completed practice notebook as a preserved attempt.
5. Close the reference and create an ignored module-test working copy.
6. Complete every test response and executable check without assigning your own points.
7. Save the completed test as a preserved attempt and ask AI to grade it.
8. Continue only after the AI-reviewed result is at least 20/25 (80%); otherwise, review the identified objectives and retake the test.

## Repeatable Notebook Workflow

The notebooks in `starters/` and `module_tests/` are clean, version-controlled originals. Do not record personal answers directly in those files. Create an ignored practice working copy for one module from the repository root:

```bash
python scripts/reset_notebook.py 0
```

The command creates `learning/working/project1_module_0_python_foundations_working.ipynb`. The entire `working/` directory is ignored by Git, so unfinished answers and execution outputs remain local.

After completing and reviewing the notebook, preserve it as a version-controlled attempt:

```bash
python scripts/save_attempt.py 0
```

This creates `learning/attempts/project1_module_0_python_foundations_attempt.ipynb` with the recorded answers and outputs intact.

Create the corresponding ignored module-test working copy:

```bash
python scripts/reset_notebook.py 0 --test
```

This creates `learning/working/project1_module_0_python_foundations_test_working.ipynb`. Preserve the completed test separately:

```bash
python scripts/save_attempt.py 0 --test
```

The save command creates `learning/attempts/project1_module_0_python_foundations_test_attempt.ipynb`, which can be reviewed and committed without exposing unfinished working files.

Create fresh practice and test working copies for every module:

```bash
python scripts/reset_notebook.py all
python scripts/reset_notebook.py all --test
```

The reset command refuses to overwrite existing work. Explicitly replace an existing working copy only when you intend to start again:

```bash
python scripts/reset_notebook.py 0 --force
python scripts/reset_notebook.py 0 --test --force
```

The reset command's `--force` option permanently replaces the matching working copy with a clean starter. The save command also refuses to replace a preserved attempt unless you deliberately run `python scripts/save_attempt.py <module> [--test] --force`.

## AI Grading Workflow

AI grading is the intended final step for module tests and cumulative assessments. The learner records answers and runs executable checks but does not assign points to written or open-ended work.

1. Complete the assessment in `working/` before requesting feedback.
2. Run all executable cells from top to bottom and save the notebook with its outputs.
3. Preserve it with `scripts/save_attempt.py`, then leave the recorded answers and code unchanged during grading.
4. Ask AI to apply the notebook rubric, inspect the recorded answers, code, assertions, and outputs, and cite evidence for every award or deduction.
5. Have AI report the written or open-ended score, automatic-check subtotal, combined result, demonstrated strengths, misconceptions, and prioritized review objectives.
6. Use the combined AI-reviewed result for the progression threshold. Retake weak objectives from a fresh attempt rather than editing answers to match the feedback.

Use this prompt for a module-test attempt:

> Grade my completed module-test attempt notebook. Preserve my original answers and code. Apply the assessment rubric to the written responses, verify the executable checks and outputs, and cite specific evidence for each awarded or deducted point. Report the written score out of 10, executable score out of 15, final score out of 25, strengths, misconceptions, and prioritized review objectives. Ask targeted follow-up questions before giving complete corrected answers.

The cumulative assessment notebooks contain their own grading prompts and rubrics. Point AI to the completed notebook path so it can review the saved work directly. AI feedback is diagnostic: check its claims against the references and executable evidence, and ask for clarification when a deduction is not supported.

Completed work selected for review or portfolio evidence belongs in [attempts](attempts/README.md). Module 0 currently has a preserved [Python foundations attempt](attempts/project1_module_0_python_foundations_attempt.ipynb).

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
| 0 | Python foundations | [Foundations](reference/project1_module_0_python_foundations_reference.md) and [namespaces](reference/project1_module_0_python_namespaces_reference.md) | [Practice](starters/project1_module_0_python_foundations_practice.ipynb) | [Test](module_tests/project1_module_0_python_foundations_test.ipynb) |
| 1 | Environment and PostGIS setup | [Reference](reference/project1_module_1_environment_postgis_reference.md) | [Practice](starters/project1_module_1_environment_postgis_practice.ipynb) | [Test](module_tests/project1_module_1_environment_postgis_test.ipynb) |
| 2 | Git and version control | [Reference](reference/project1_module_2_git_reference.md) | [Practice](starters/project1_module_2_git_practice.ipynb) | [Test](module_tests/project1_module_2_git_test.ipynb) |
| 3 | Configuration and Extract | [Configuration](reference/project1_module_3_config_reference.md) and [Extract](reference/project1_module_3_extract_reference.md) | [Practice](starters/project1_module_3_extract_practice.ipynb) | [Test](module_tests/project1_module_3_extract_test.ipynb) |
| 4 | Transform | [Reference](reference/project1_module_4_transform_reference.md) | [Practice](starters/project1_module_4_transform_practice.ipynb) | [Test](module_tests/project1_module_4_transform_test.ipynb) |
| 5 | QA/QC and the quality gate | [Reference](reference/project1_module_5_qa_qc_reference.md) | [Practice](starters/project1_module_5_qa_qc_practice.ipynb) | [Test](module_tests/project1_module_5_qa_qc_test.ipynb) |
| 6 | Load and PostGIS publication | [Reference](reference/project1_module_6_load_postgis_reference.md) | [Practice](starters/project1_module_6_load_postgis_practice.ipynb) | [Test](module_tests/project1_module_6_load_postgis_test.ipynb) |
| 7 | Orchestration, testing, and troubleshooting | [Reference](reference/project1_module_7_orchestration_testing_reference.md) | [Practice](starters/project1_module_7_orchestration_testing_practice.ipynb) | [Test](module_tests/project1_module_7_orchestration_testing_test.ipynb) |

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

Use the [concept notes](concept_notes/README.md) for focused explanations of questions that arise while reading the guides. Current topics cover GitHub publication, dataset identifiers, data quality gates, coordinate reference systems, data contracts, schemas, provenance, idempotency, data artifacts, API pagination, environment dependency definitions, Docker containers, geometry repair, atomic transactions, function side effects, exceptions and context managers, and assertions as executable expectations.

## Resource Roles

- **Reference:** teaches concepts, mental models, common mistakes, and review criteria.
- **Starter:** is a clean, version-controlled original for guided practice.
- **Working copy:** is an ignored notebook created from a starter or module test and edited locally.
- **Attempt:** is completed work intentionally copied from `working/` into version control for AI review, reflection, or portfolio evidence.
- **Module test:** measures closed-note retention at the end of one module; executable work is checked automatically and written work is graded by AI after completion.
- **Walkthrough:** demonstrates the connected project workflow.
- **Guide:** explains curriculum-wide concepts or operating decisions.
- **Concept note:** gives a focused explanation of one term or closely related idea.
- **Assessment:** measures cumulative understanding across multiple modules and uses AI review for written and open-ended work.

Generated data, QA reports, logs, credentials, local environments, and editor state are project artifacts rather than learning resources and should not be added to this index.