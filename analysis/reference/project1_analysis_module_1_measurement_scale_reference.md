# Analysis Module A1: Measurement, Scale, and CRS

## Objective

Choose defensible geographic units and measurement methods before calculating area or comparing communities.

## Geometry Roles

The analysis uses:

- community polygons as aggregation units
- transit-stop points as observed features

Inspect geometry types, emptiness, validity, CRS, identifiers, and bounds before a spatial operation.

## CRS and Units

`EPSG:4326` stores longitude and latitude in angular degrees. It is unsuitable for direct square-metre area calculations.

Project 1 standardizes outputs to `EPSG:3347`, whose linear units support metre-based measurements across Canada.

Community area in square kilometres is:

$$
A_{km^2} = \frac{A_{m^2}}{1{,}000{,}000}
$$

Always label the resulting unit.

## Unit and Scale

One result row represents one community. This supports community comparisons but hides within-community variation.

Community boundaries are administrative units, not transit catchments. Results can change under another partition, an example of MAUP.

## Boundary Cases

A point on a polygon boundary can produce different matches under `within`, `intersects`, and boundary-inclusive predicates. The method must state the predicate and inspect unmatched or duplicate assignments.

## Required Checks

Before joining:

- both layers have CRS metadata
- CRS values match
- community identifiers are non-null and unique
- communities are valid and non-empty
- stop points are non-empty
- bounds are geographically plausible
- area values are positive

## Completion Criteria

You can complete this module when you can explain why projected CRS matters, label area units, identify the unit of analysis, and predict how boundaries and scale limit interpretation.

## Related Concepts

- [Units of analysis, scale, and boundary effects](../concept_notes/units_scale_boundaries.md)
- [Geographic and projected CRS](../../learning/concept_notes/project1_geographic_projected_crs.md)