# Units of Analysis, Scale, and Boundary Effects

## Unit of Analysis

The unit of analysis is the entity represented by each observation in the result. In the first Project 1 analysis, one row represents one community polygon.

The unit controls what can be compared and what variation is hidden.

## Geographic Scale

Scale concerns the geographic level at which a pattern is observed. A community-level average cannot describe every block, stop, or resident inside the community.

A pattern may appear at one scale and weaken, reverse, or disappear at another.

## Boundary Effects

Administrative boundaries divide continuous geography into named units. A transit stop just outside a community boundary may be usable by nearby residents but will not count inside that community under a strict point-in-polygon method.

Boundary points also require a predicate decision. A point exactly on a polygon edge may fail `within` while satisfying a boundary-inclusive relationship.

## Modifiable Areal Unit Problem

The **modifiable areal unit problem**, or MAUP, describes how aggregated results can change when geographic units change in size or boundary arrangement.

Community stop density is therefore a property of the chosen community partition and snapshot, not an immutable property of Calgary.

## Ecological Fallacy

An ecological fallacy occurs when a group-level pattern is incorrectly assigned to individuals within the group.

Low community-level stop density does not prove that every resident has poor transit access. Stops and residents may be unevenly distributed, and nearby stops outside the boundary may matter.

## Validation Questions

- Are community boundaries relevant to the stakeholder?
- Are there multipart or unusually large polygons?
- How many stops lie near boundaries?
- Would buffers or network catchments better match the eventual decision?
- Are zero-count units real or caused by unmatched geometry?

## Plain-Language Definition

> The chosen geographic unit and boundary system shape the pattern an aggregated analysis can reveal.

## Related Resources

- [Counts, denominators, and normalization](counts_denominators_normalization.md)
- [Spatial question workflow](../guides/spatial_question_workflow.md)