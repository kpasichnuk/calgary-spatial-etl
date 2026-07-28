# Spatial Question Workflow

## Purpose

A spatial operation creates value only when it supports a meaningful question and a defensible interpretation. Use this workflow before choosing a buffer, join, density, route, or map.

## 1. Identify the Decision

Start with a person or organization and a decision.

Weak starting point:

> Make a map of transit stops.

Stronger starting point:

> A planning team wants to identify communities that deserve closer investigation for potentially sparse mapped transit-stop coverage.

The analysis does not make the planning decision. It organizes evidence relevant to that decision.

## 2. Write the Spatial Question

A useful spatial question names:

- the geographic objects
- the spatial relationship
- the measure or comparison
- the study area or time, when relevant

Project 1 question:

> How does the number of mapped transit stops per square kilometre vary among Calgary community polygons in the current ETL snapshot?

## 3. State a Hypothesis

Record an expected pattern before calculating results. A hypothesis makes surprising results visible and reduces the temptation to invent a story after seeing a map.

Example:

> Communities with larger areas may have higher raw stop counts but not necessarily higher stop density.

## 4. Define the Unit of Analysis

For this case study, the unit is a Calgary community polygon. Every output row should represent one community.

Ask:

- Why is this unit relevant to the stakeholder?
- What variation exists inside it?
- Would another boundary system change the result?
- Are boundary versions and dates compatible?

## 5. Define Measures and Denominators

Raw count:

$$
C_i = \text{number of transit stops assigned to community } i
$$

Area-normalized density:

$$
D_i = \frac{C_i}{A_i}
$$

where $A_i$ is community area in square kilometres.

Density enables one comparison, but it is not service quality or resident accessibility. The denominator determines the meaning.

## 6. Select Data and Check Fitness

For each input, record:

- source and licence
- snapshot date
- geometry type
- identifier and descriptive fields
- CRS
- known omissions or collection bias
- QA status

Do not proceed merely because a file opens.

## 7. Choose a Spatial Relationship

A point-in-polygon join needs an explicit predicate:

- `within`: point interior lies within polygon interior
- `intersects`: point and polygon share any location, including a boundary
- `covered_by`: point lies in the polygon interior or boundary

Boundary points can behave differently under these predicates. State the choice and inspect unmatched or multiply matched features.

## 8. Measure in an Appropriate CRS

Longitude and latitude are angular coordinates. Community area must be calculated in a suitable projected CRS, such as the ETL target `EPSG:3347`.

Record units and conversion:

$$
1\ \text{km}^2 = 1{,}000{,}000\ \text{m}^2
$$

## 9. Validate the Result

At minimum, check:

- input and output row counts
- null and duplicate identifiers
- unmatched points
- points with more than one polygon match
- zero-count communities
- minimum, maximum, and implausible values
- several manually inspected map locations
- whether totals reconcile with source counts

A successful function call is not evidence that the spatial interpretation is correct.

## 10. Compare Alternative Views

Compare raw counts and normalized density. A community can rank high by count and low by area-normalized density.

If rankings differ, explain why. Do not select only the measure that produces the preferred story.

## 11. Interpret Without Overclaiming

Supported statement:

> Community A has fewer mapped transit stops per square kilometre than Community B in this snapshot.

Unsupported statement without more evidence:

> Community A is underserved and needs a new bus route.

The latter requires demand, population, routes, frequency, network access, destinations, and policy context.

## 12. Connect Evidence to Value

A suitable conclusion may prioritize further investigation rather than prescribe an intervention:

> Review the lowest-density communities using population, route frequency, walking-network, and destination data before drawing service-access conclusions.

This creates value by narrowing attention while respecting uncertainty.

## Analysis Record Template

For each exercise or case study, record:

```text
Stakeholder:
Decision:
Spatial question:
Hypothesis:
Unit of analysis:
Inputs and dates:
CRS and units:
Spatial relationship:
Measures and denominators:
Validation checks:
Results:
Surprising cases:
Supported interpretation:
Limitations:
Recommended next evidence or action:
```

## Developer Handoff

Once the exploratory method is defensible:

1. extract reusable logic from notebooks into functions
2. define input and output contracts
3. add deterministic fixtures and tests
4. reconcile Python and PostGIS implementations where useful
5. write outputs to an ignored or deliberately versioned location
6. document how another user reproduces the result

Spatial intuition decides what the system should calculate. Development makes that calculation reliable and reusable.