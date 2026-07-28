# Counts, Denominators, and Normalization

## Raw Counts

A raw count measures how many events or features are assigned to a unit:

$$
C_i = \text{number of stops in community } i
$$

Counts answer a valid question, but larger communities often have more opportunity to contain features.

## Normalization

Normalization divides a value by a meaningful denominator to enable a different comparison.

For area-normalized stop density:

$$
D_i = \frac{C_i}{A_i}
$$

where $A_i$ is area in square kilometres and $D_i$ is stops per square kilometre.

## The Denominator Defines Meaning

Different denominators answer different questions:

- stops per square kilometre: spatial concentration
- stops per 1,000 residents: population-relative provision
- stops per kilometre of road: relationship to road-network extent
- departures per resident: service supply relative to population

One denominator cannot stand in for another.

## Small Denominators

Very small areas can produce high densities from only a few stops. Always inspect the numerator and denominator alongside the ratio.

## Zero and Missing Values

A zero stop count means no matched stop was observed under the selected data and method. A missing value may mean the calculation or join failed. Do not treat them as equivalent without checking.

## Ranking

Rankings compress uncertainty and small differences. Communities ranked 10th and 11th may have nearly identical values. Report values, units, and relevant ties rather than only rank.

## Plain-Language Definition

> Normalization changes a raw value into a rate or density by dividing by a denominator whose meaning must match the question.

## Related Resources

- [Units of analysis, scale, and boundary effects](units_scale_boundaries.md)
- [Spatial question workflow](../guides/spatial_question_workflow.md)