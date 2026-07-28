# Analysis Module A3: Normalization, Validation, and Interpretation

## Objective

Compare raw counts and area-normalized density, validate the result, and communicate only conclusions supported by the data and method.

## Calculate Density

For community $i$:

$$
D_i = \frac{C_i}{A_i}
$$

where:

- $C_i$ is matched transit-stop count
- $A_i$ is community area in square kilometres
- $D_i$ is stops per square kilometre

Reject or investigate non-positive areas before division.

## Compare Measures

Rank by both raw count and density. Inspect communities whose rank changes substantially.

A high count with low density may reflect a large polygon. A high density from a small count may reflect a very small polygon. Show numerator and denominator with the rate.

## Validate

Check:

- one output row per community
- no null or duplicate community identifiers
- non-negative integer stop counts
- positive area
- finite, non-negative density
- sum of community counts reconciles with matched stops
- zero-count communities remain present
- several highest, lowest, and surprising cases are mapped or inspected

## Interpretation Ladder

1. **Observation:** state the measured pattern.
2. **Comparison:** explain how raw and normalized views differ.
3. **Possible explanation:** identify hypotheses without claiming proof.
4. **Limitation:** state missing evidence and method constraints.
5. **Decision value:** recommend further investigation or a bounded action.

## Avoid Overclaiming

Stop density is not accessibility, equity, demand, frequency, or service quality. It can identify communities for deeper analysis but cannot diagnose service need alone.

## Reproducible Delivery

After exploration:

- extract stable functions from the notebook
- add deterministic fixtures and tests
- write an output schema and data dictionary
- record predicate, CRS, units, and input snapshot
- document how to regenerate the result

## Completion Criteria

You can complete this module when calculations reconcile, rankings are interpreted with denominators, edge cases are inspected, and conclusions explicitly separate evidence from hypothesis.

## Related Concepts

- [Counts, denominators, and normalization](../concept_notes/counts_denominators_normalization.md)
- [Proximity versus accessibility](../concept_notes/proximity_vs_accessibility.md)