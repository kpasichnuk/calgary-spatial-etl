# Junior GIS Developer Python and SQL Learning Path

## Purpose

This guide defines a practical Python and SQL target for junior GIS developer roles and recommends free, exercise-based resources. Use these resources for routine instruction and automated feedback. Reserve AI assistance for targeted explanations, occasional review, and mock interviews.

The goal is not to memorize every method or write production systems without references. The goal is to receive a small GIS task, break it down, implement it with documentation, test the result, and explain why the data, CRS, joins, units, and output are correct.

## Python Readiness Target

A junior GIS developer should be able to:

- Use variables, strings, lists, dictionaries, loops, and conditionals comfortably.
- Write and call functions with parameters and return values.
- Read and write CSV, JSON, and common spatial files.
- Filter, join, group, clean, and validate data with pandas and GeoPandas.
- Use `pathlib`, imports, exceptions, and context managers.
- Read a traceback and isolate a failure with small test inputs.
- Write simple assertions and unit tests.
- Read a 100-200 line script and explain its control flow and side effects.
- Write a small data-processing script from a clear specification.
- Use official documentation to find exact library syntax.

This is comfortable intermediate Python applied to data work. Advanced algorithms, framework internals, and memorization of library APIs are not junior GIS requirements.

## SQL Readiness Target

A junior GIS developer should be able to write and explain:

- `SELECT`, aliases, `WHERE`, `ORDER BY`, and `LIMIT`.
- `INNER JOIN` and `LEFT JOIN`.
- `GROUP BY`, aggregate functions, and `HAVING`.
- `CASE`, null handling, subqueries, and common table expressions.
- Careful `INSERT`, `UPDATE`, and `DELETE` statements.
- Basic table definitions, keys, constraints, and indexes.
- Spatial predicates such as `ST_Intersects`, `ST_Within`, and `ST_DWithin`.
- Spatial measurements and transformations using functions such as `ST_Distance`, `ST_Area`, and `ST_Transform`.
- Spatial joins with a defensible choice of CRS and units.

Window functions are useful but are not required for every junior GIS position. Recursive SQL is optional at this stage.

## Recommended Free Resources

### 1. Python Programming MOOC

[University of Helsinki Python Programming MOOC 2026](https://programming-26.mooc.fi/) is the primary Python course. It requires typed programming solutions, awards exercise points, and provides programming exams.

Complete Parts 1-7. Aim to complete at least 80 percent of the exercises without having AI generate solutions. Use course hints and documentation when blocked. Parts 8-10 are useful extensions, but all 14 parts are not necessary before applying for junior GIS roles.

### 2. Exercism Python Track

[Exercism's Python track](https://exercism.org/tracks/python) provides free exercises with automated tests and optional mentoring.

Use it for additional fluency after or alongside the MOOC. Complete the concept exercises and approximately 30-50 practice exercises. More repetition is useful only when it addresses a specific weakness.

### 3. PostgreSQL Exercises

[PostgreSQL Exercises](https://pgexercises.com/) uses one consistent dataset for interactive query practice.

Complete these sections:

- Basic
- Joins and Subqueries
- Aggregates
- Modifying Data

Complete Date and String exercises selectively. Window-function exercises are beneficial. Recursive-query exercises are optional.

### 4. Automating GIS Processes

[Automating GIS Processes](https://autogis-site.readthedocs.io/en/latest/) is an open University of Helsinki course with hands-on GIS exercises. It covers Shapely, GeoPandas, coordinate reference systems, table and spatial joins, overlays, maps, networks, and rasters.

Use this course to transfer general Python skills into GIS work. Complete the vector-focused lessons first, especially geometry, spatial data I/O, projections, spatial queries, joins, and overlays.

### 5. Introduction to PostGIS

The official [Introduction to PostGIS workshop](https://postgis.net/workshops/postgis-intro/) provides free lessons, data, and exercises.

Prioritize these topics:

- Simple SQL and geometry
- Spatial relationships and joins
- Spatial indexes
- Projections and geography
- Geometry validity

Advanced topics such as topology, 3D data, database tuning, and triggers can wait until a project or job requires them.

## Recommended Sequence

```text
Python MOOC Parts 1-7
    -> PostgreSQL Exercises
    -> Automating GIS Processes
    -> Introduction to PostGIS
    -> independent work in this repository
```

SQL can overlap with the later Python modules. A reasonable part-time pace at 6-8 hours per week is:

| Area | Approximate time |
|---|---:|
| Python foundations | 8-12 weeks |
| SQL | 3-5 weeks |
| GIS Python and PostGIS | 6-10 weeks |
| Independent project transfer | 2-4 weeks |

The total is approximately four to six months, depending on prior experience and weekly consistency.

## Using AI Economically

Use automated tests, course feedback, documentation, and small experiments as the default learning loop. Reserve AI credits for tasks where contextual judgment adds value:

- Review one completed assignment rather than every exercise.
- Explain a specific error after an independent investigation.
- Give one hint without supplying the complete solution.
- Conduct a mock interview after a major course section.
- Review the final independent GIS project.

Before asking AI, spend approximately 30 minutes reading the error, checking documentation, reducing the problem, and trying course hints. Include those findings in the question so the response can focus on the unresolved issue.

## Readiness Check

The learner is ready to apply these skills when they can complete a small unfamiliar task using documentation but without generated code. A suitable assessment is to:

1. Read a new vector dataset and inspect its schema and CRS.
2. Clean fields and invalid or missing values.
3. Reproject it for an explicitly stated measurement or analysis.
4. Join it to another layer and summarize the result.
5. Load or query the result in PostGIS.
6. Add assertions or tests for important expectations.
7. Diagnose one deliberately introduced failure.
8. Explain the implementation, assumptions, units, and limitations.

Successful completion matters more than speed or memorized syntax. The result should be reproducible, tested, and defensible.