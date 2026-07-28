# Assertions as Executable Expectations

## Core Idea

An assertion expresses a condition that code expects to be true at a particular point.

It is **executable** because Python evaluates the condition. If the condition is true, execution continues. If it is false, Python raises `AssertionError`.

```python
assert list(result.columns) == ["name", "geometry"]
```

This turns a written expectation into a check that can directly agree or disagree with the observed behavior.

## Basic Assertion Anatomy

An assertion can contain a condition and an optional failure message:

```python
assert condition, "message shown when the condition is false"
```

For example:

```python
assert row_count > 0, "The processed layer must not be empty."
```

If `row_count` is positive, the statement produces no output. If it is zero, Python raises:

```text
AssertionError: The processed layer must not be empty.
```

Silence means this assertion passed during that execution. It does not prove all related behavior is correct.

## Assertions Encode Contracts in Tests

A useful test arranges controlled inputs, performs an operation, and asserts observable outcomes:

```python
original = fresh_places()
result = normalize_columns(original)

assert list(result.columns) == ["site_id", "display_name", "geometry"]
assert list(original.columns) == ["Site ID", "Display-Name", "geometry"]
assert result is not original
```

These assertions encode several expectations:

- output columns are normalized
- the input remains unchanged
- the result is a different object

Together they test more of the helper contract than merely checking that the function returned.

## Good Assertions Check Behavior

High-value assertions check externally meaningful results such as:

- returned values
- output fields and order
- row counts
- pass/fail status
- input mutation safety
- raised exception types
- written artifact contents
- database state after commit or rollback

Examples from this project include:

```python
assert result.passed is True
assert result.row_count == 2
assert missing == ["population", "area"]
assert "sector" not in source.columns
```

These checks state what the code must accomplish without requiring one particular internal implementation.

## Weak Assertions and Implementation Trivia

An assertion is less useful when it checks an incidental detail that is not part of the behavior contract.

For example, requiring a function to use exactly three local variables would make refactoring difficult without improving confidence in its output.

Prefer:

```python
assert normalize_col_name("Road Name / Type") == "road_name_type"
```

over checking which sequence of string methods the function used internally.

## One Assertion Proves One Observation

An assertion proves only the condition it checks for that execution and input.

```python
assert loaded_rows == source_rows
```

This supports row-count reconciliation. It does not prove that:

- every value is correct
- geometry is accurate
- CRS is correct
- a spatial index exists
- another dataset loaded successfully

Tests need multiple focused expectations when the contract has multiple dimensions.

## Failure Messages

A concise message can make a failed learning exercise easier to diagnose:

```python
assert required_fields == ["name", "sector"], (
    "Do not mutate the caller's required field list."
)
```

The message should explain the violated expectation, not merely say `failed`.

In mature test suites, assertion libraries often generate useful comparisons automatically, so custom messages are most valuable when they add domain context.

## Plain `assert` Versus `unittest` Methods

Practice notebooks commonly use Python's plain `assert`:

```python
assert result.passed is True
```

The production test suite uses `unittest.TestCase` methods:

```python
self.assertTrue(result.passed)
self.assertEqual(result.row_count, 2)
self.assertFalse(table_exists)
```

Both express executable expectations. `unittest` methods integrate with its runner and provide specialized failure output.

Common methods include:

| Method | Expectation |
|---|---|
| `assertEqual(actual, expected)` | values are equal |
| `assertTrue(value)` | value is truthy |
| `assertFalse(value)` | value is falsy |
| `assertIsNone(value)` | value is exactly `None` |
| `assertIn(item, collection)` | collection contains item |
| `assertRaises(Type)` | code raises the expected exception type |

## Expecting an Exception

A failure path can be the correct behavior. `assertRaises` verifies that invalid input is rejected:

```python
with self.assertRaises(RuntimeError):
    operation_that_must_fail()
```

If `RuntimeError` occurs, the expectation passes. If no exception occurs or a different type occurs, the test fails.

The rollback integration test deliberately raises `RuntimeError` inside a transaction and then checks that the table does not remain. This verifies both the failure signal and the resulting database state.

## Assertions and Side Effects

When testing a function with side effects, assert both the intended external change and important safety properties.

For a file-writing function, checks might include:

```python
assert output_path.exists()
assert output_path.read_text() == expected_text
assert unrelated_path.read_text() == original_text
```

For a database rollback:

```python
self.assertFalse(
    inspect(engine).has_table("rollback_sites", schema=test_schema)
)
```

A function raising the expected exception is not enough if it could still leave partial state.

## Assertions Are Not Production Validation

Plain Python `assert` statements can be removed when Python runs with optimization, such as:

```bash
python -O application.py
```

Therefore, application code must not rely on plain assertions to validate user input, source data, credentials, file existence, or publication safety.

Use explicit validation and exceptions in production paths:

```python
if not path.exists():
    raise FileNotFoundError(f"Missing processed file: {path}")
```

Use assertions primarily for tests, learning exercises, and internal developer expectations where optimization behavior is understood.

`unittest` assertion methods are ordinary method calls and are not removed by Python's `-O` flag, though tests should normally run without optimization changes that alter application behavior.

## Assertions Versus QA Rules

A test assertion and a pipeline quality check operate at different times:

- **Test assertion:** checks that the implementation behaves as expected under a controlled test case.
- **QA rule:** inspects the current processed dataset during an operational pipeline run.

For example:

```text
test assertion -> verifies duplicate IDs cause QA failure in a fixture
QA rule        -> measures duplicate IDs in today's Calgary dataset
```

Tests verify the checker. QA applies the checker to current data.

## Assertions Versus Exceptions

An assertion failure raises `AssertionError`, but assertions and application exceptions communicate different intent.

```text
assertion -> developer or test expectation was contradicted
exception -> operation cannot fulfill its runtime contract
```

Use a meaningful application exception for expected runtime failures. Use assertions to make development and test expectations executable.

## Avoiding False Confidence

A passing assertion can be weak or incomplete. Confidence depends on:

- whether the input exercises meaningful behavior
- whether the condition checks the correct outcome
- whether failure paths are covered
- whether side effects are isolated
- whether integration dependencies were actually exercised

A skipped database test is not a passing database assertion. It means that behavior was not checked during that run.

## Plain-Language Definition

> An assertion is an executable expectation: it checks a condition and reports a failure when observed behavior contradicts what the code or test expects.

## Related Resources

- [Module 0 Python foundations reference](../reference/project1_module_0_python_foundations_reference.md)
- [Module 0 Python foundations practice](../starters/project1_module_0_python_foundations_practice.ipynb)
- [Exceptions and context managers](project1_exceptions_context_managers.md)
- [Function side effects](project1_function_side_effects.md)
- [Data quality gates](project1_data_quality_gates.md)
- [Module 7 orchestration and testing reference](../reference/project1_module_7_orchestration_testing_reference.md)
