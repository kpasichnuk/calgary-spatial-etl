# Analysis Module A2: Spatial Joins and Aggregation

## Objective

Assign transit-stop points to community polygons with an explicit predicate, then aggregate without losing zero-count communities or hiding unmatched points.

## Point-in-Polygon Join

A GeoPandas spatial join combines rows according to geometry relationships:

```python
joined = gpd.sjoin(
    stops,
    communities[["community_id", "geometry"]],
    how="left",
    predicate="within",
)
```

The exact identifier column must come from the ETL contract rather than this generic example.

## Join Direction and Type

Using stops as the left layer keeps every stop for reconciliation. A missing community identifier after the join identifies an unmatched stop.

Aggregation from matched points alone omits communities with zero stops. Preserve all communities by joining counts back to the complete community layer and filling absent counts with zero only after reconciliation.

## Reconciliation

Let:

- $S$ be source stop count
- $M$ be stops matched once
- $U$ be unmatched stops
- $D$ be excess duplicate matches

A one-to-one assignment should satisfy:

$$
S + D = M + U
$$

For a strict non-overlapping polygon partition, $D$ should normally be zero. Investigate rather than automatically deduplicate.

## Aggregation

Group by a stable community identifier, not only a display name. Names may change or repeat.

Preserve:

- identifier
- display name
- stop count
- area
- geometry when mapping is required

## Boundary Investigation

Inspect unmatched points and points near polygon edges. Alternative predicates can be compared, but choose one method before reporting results and document its consequences.

## Completion Criteria

You can complete this module when all source stops reconcile, zero-count communities remain in the result, duplicate matches are visible, and the selected predicate is explained.

## Related Concepts

- [Units of analysis, scale, and boundary effects](../concept_notes/units_scale_boundaries.md)
- [Data quality gates](../../learning/concept_notes/project1_data_quality_gates.md)