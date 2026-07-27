# Geographic and Projected Coordinate Reference Systems

## EPSG Codes

An EPSG code identifies a complete coordinate reference system (CRS). It does not by itself mean latitude/longitude or projected coordinates.

Examples:

| EPSG code | Type | Common coordinates |
|---|---|---|
| `EPSG:4326` | geographic | longitude and latitude in degrees |
| `EPSG:4269` | geographic | NAD83 longitude and latitude in degrees |
| `EPSG:3347` | projected | easting and northing in metres |
| `EPSG:3857` | projected | Web Mercator coordinates in metres |
| `EPSG:32612` | projected | UTM Zone 12N coordinates in metres |

## Geographic CRS

A geographic CRS describes locations on an ellipsoid using angular coordinates.

For Calgary in `EPSG:4326`, a location may look like:

```text
longitude = -114.07
latitude  = 51.05
```

The units are degrees. In GeoJSON and most GIS software storage, coordinate order is generally $x,y$, which means longitude before latitude.

People often say “latitude/longitude,” but that phrase does not guarantee storage order.

## Projected CRS

A projected CRS mathematically transforms locations from the curved Earth onto a flat coordinate plane.

`EPSG:3347` is NAD83 / Statistics Canada Lambert. It is designed for mapping and analysis across Canada.

Its coordinates are:

- easting: horizontal position
- northing: vertical position
- units: metres

The coordinate numbers change during projection, but the intended real-world location remains the same.

```text
EPSG:4326 longitude/latitude
             -> projection
EPSG:3347 easting/northing
```

## Why Not Measure Directly in Degrees?

Degrees are angular units, not fixed ground distances. One degree of longitude covers different distances at different latitudes.

Therefore, direct planar calculations of distance, area, or buffering in a longitude/latitude CRS can be misleading.

A suitable projected CRS provides linear units and controlled distortion for its intended region.

## Projection Distortion

No flat map can preserve every property of the curved Earth. A projection may distort some combination of:

- area
- distance
- direction
- shape

The correct CRS depends on location, scale, and analytical purpose. `EPSG:3347` is appropriate for this project’s Canada-focused common framework, though a more locally optimized Calgary projection could be preferable for some high-precision local measurements.

## Assigning Versus Transforming

These operations are different:

```python
gdf = gdf.set_crs("EPSG:4326")
```

`set_crs` labels what the existing coordinate numbers mean. It does not change the numbers.

```python
gdf = gdf.to_crs("EPSG:3347")
```

`to_crs` calculates new coordinate numbers in the target CRS.

Assigning the wrong CRS mislabels coordinates. Reprojecting from the wrong source CRS then produces wrong locations.

## Project Contract

Transform standardizes every processed layer to `EPSG:3347`. QA verifies the exact target CRS before Load, and PostGIS stores the corresponding SRID with geometry.

This shared CRS makes cross-layer operations consistent and supports metre-based analysis.

## Related Resources

- [Module 4 Transform reference](../reference/project1_module_4_transform_reference.md)
- [Module 1 Environment and PostGIS reference](../reference/project1_module_1_environment_postgis_reference.md)
