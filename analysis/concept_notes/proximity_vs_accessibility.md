# Proximity Versus Accessibility

## Core Distinction

**Proximity** measures geographic nearness under a specified distance model.

**Accessibility** describes the ability to reach a useful destination or service and usually depends on networks, barriers, travel modes, time, schedules, cost, and user capabilities.

A nearby transit stop is not automatically accessible.

## Straight-Line Distance

A Euclidean buffer measures straight-line distance in a projected coordinate system. It may be useful for screening, but it ignores:

- street and pathway connectivity
- rivers, railways, fences, and highways
- crossings and entrances
- slope
- travel mode
- actual route distance

## Network Distance and Time

A network method follows connected edges and can incorporate direction, speed, crossings, or schedules. It more closely represents travel but still depends on network quality and assumptions.

## Stop Density Is Neither

Stops per square kilometre describes the concentration of mapped stop points inside a polygon. It does not measure a resident's distance to a stop and does not model network access.

## Responsible Language

Supported:

> This community has a lower mapped stop density than the comparison community.

Requires additional analysis:

> Residents in this community have worse transit accessibility.

## Future Data

A stronger accessibility study may require:

- population or address locations
- pedestrian network and crossings
- stop entrances
- routes and schedules such as GTFS
- service frequency and operating hours
- destinations and travel purposes
- mobility constraints

## Plain-Language Definition

> Proximity is nearness; accessibility is the practical ability to reach and use something.

## Related Resources

- [Spatial intuition and decision value](spatial_intuition_decision_value.md)
- [Portfolio roadmap](../../planning/portfolio_roadmap.md)