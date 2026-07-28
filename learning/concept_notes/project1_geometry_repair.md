# Geometry Repair

## Core Idea

Geometry repair attempts to restructure malformed spatial geometry so that it satisfies formal validity rules and can be processed reliably by GIS software.

An invalid geometry may cause spatial operations such as intersection, buffering, area calculation, or database loading to fail or return misleading results.

Repair establishes technical validity. It does not prove that a feature accurately represents the real world.

## Common Geometry Problems

A geometry can be invalid because:

- a polygon boundary crosses itself
- an interior ring, or hole, lies outside its polygon
- polygon rings overlap incorrectly
- nested components have invalid topological relationships
- geometry components collapse or intersect in unsupported ways

A self-crossing polygon can resemble a bow tie:

```text
\ /
 X
/ \
```

The coordinates exist, but they do not form one unambiguous valid polygon boundary.

## This Project's Cleaning Sequence

The Transform stage implements geometry cleaning in `clean_geometry()` and individual repair in `repair_geom()`.

Its sequence is:

```text
input rows
    -> remove null geometries
    -> remove empty geometries
    -> count invalid_before
    -> attempt repair on invalid geometries
    -> remove repair results that are null or empty
    -> remove geometries that remain invalid
    -> count invalid_after among surviving rows
```

Null and empty geometries are removed before repair because they do not contain malformed shapes for the repair function to reconstruct.

## Preferred Repair: `make_valid()`

The project first tries Shapely's `make_valid()`:

```python
from shapely import make_valid

return make_valid(geom)
```

`make_valid()` analyzes the geometry's structure and returns a valid representation when possible. The result may not have the same geometry type as the input.

For example, repairing one invalid `Polygon` could produce:

- a valid `Polygon`
- a `MultiPolygon` containing several valid polygon parts
- a `GeometryCollection`
- lower-dimensional line or point components where parts collapsed

Repair therefore changes geometry structure, not merely a Boolean validity flag.

## Fallback Repair: `buffer(0)`

If importing or calling `make_valid()` raises an exception, the project tries:

```python
return geom.buffer(0)
```

A zero-distance buffer reconstructs polygon topology and can resolve some self-intersections and ring problems. It is a traditional compatibility fallback, but it may remove, split, or reshape problematic portions.

If both repair attempts raise exceptions, `repair_geom()` returns `None`. The later cleaning filters remove that row.

## What Happens to Unrepaired Geometry

After repair attempts, the project keeps only rows whose geometry is:

- non-null
- nonempty
- valid

A geometry that fails these conditions is dropped from the processed GeoDataFrame. Its attribute row is dropped with it because a GeoDataFrame row represents one feature and its geometry together.

This prevents known invalid geometry from reaching the processed output, but it can reduce the number of features.

## Understanding the Logged Counts

Transform records:

- `rows_in`: source rows read
- `rows_out`: rows written after all Transform cleaning
- `invalid_before`: invalid geometries found after initial null/empty removal
- `invalid_after`: invalid geometries among rows that survive final filtering

Because the code filters with `gdf = gdf[gdf.is_valid]` before calculating `invalid_after`, surviving rows should have:

```text
invalid_after = 0
```

This proves no known invalid geometry remains in the written layer. It does not prove that every invalid input geometry was successfully repaired.

Repair failures and initial null or empty geometries are not counted in separate log fields. Their effect can contribute to the difference between `rows_in` and `rows_out`, although other Transform behavior should also be considered when interpreting that difference.

## Validity Versus Accuracy

A valid geometry follows mathematical and topological rules. An accurate geometry correctly represents its real-world feature.

A repair operation cannot determine whether:

- a boundary is in the correct location
- a road follows its real-world route
- a missing polygon section should exist
- the source assigned the correct CRS
- a split or discarded component matches the source author's intent

For example, `make_valid()` may turn a bow-tie polygon into two valid polygon parts. The result is technically valid, but only authoritative source knowledge can establish whether those two parts represent the intended boundary.

## Validity Versus Geometry Type

A validity check and a geometry-type check answer different questions.

```text
Validity check:      Does this geometry obey topology rules?
Geometry-type check: Is this the kind of geometry expected for this layer?
```

A repaired `GeometryCollection` can be valid while still being unsuitable for a layer expected to contain only polygons. The current project blocks invalid, null, and empty geometry, but it does not enforce a per-layer geometry-type contract in QA.

A stricter future contract could require expected types such as:

- communities: `Polygon` or `MultiPolygon`
- roads: `LineString` or `MultiLineString`
- transit stops: `Point` or `MultiPoint`

Such rules should reflect the authoritative source and intended downstream use.

## Why QA Checks Again

Transform owns repair and standardization. QA independently reopens the processed file and checks that no null, empty, or invalid geometry remains.

```text
Transform attempts repair
    -> writes processed artifact
    -> QA reads artifact from disk
    -> QA independently verifies geometry
```

This separation catches serialization problems and prevents the repair stage from declaring its own output publishable without an independent check.

## When Repair Deserves Review

Repair activity deserves closer inspection when:

- `invalid_before` increases unexpectedly
- `rows_out` is lower than expected
- repaired geometry types differ from the layer contract
- areas or lengths change substantially
- many features become multipart geometries
- repaired output affects important boundaries or analysis results

For high-consequence data, preserve the original geometry and record repair details so changes can be audited feature by feature.

## Plain-Language Definition

> Geometry repair tries to restructure malformed spatial data so it follows valid geometry rules; in this pipeline, geometries that remain unusable are removed before output.

## Related Resources

- [Module 4 Transform reference](../reference/project1_module_4_transform_reference.md)
- [Module 4 Transform practice](../starters/project1_module_4_transform_practice.ipynb)
- [Data quality gates](project1_data_quality_gates.md)
- [Geographic and projected coordinate reference systems](project1_geographic_projected_crs.md)
- [Data artifacts](project1_data_artifacts.md)
