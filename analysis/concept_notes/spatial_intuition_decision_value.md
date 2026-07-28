# Spatial Intuition and Decision Value

## Core Idea

Spatial intuition is the habit of reasoning about how location, distance, direction, connectivity, scale, boundaries, and geographic context affect a question.

It is not a substitute for evidence. It helps formulate hypotheses, choose methods, identify implausible results, and recognize what a calculation omits.

## Tool Skill Versus Spatial Reasoning

Tool skill asks:

> How do I perform a spatial join?

Spatial reasoning asks:

> Which spatial relationship represents the real question, what happens at boundaries, and what conclusion can the join support?

A GIS developer needs both. The reasoning defines useful behavior; the technology makes it reproducible.

## Creating Value

Spatial work creates value when it changes or improves a decision. A map may be informative without being actionable. Begin by identifying:

- the user
- the decision
- the evidence currently missing
- how geography influences that evidence

For this project, community stop density can help a planning team prioritize communities for deeper review. It cannot independently decide where service should be added.

## Questions That Build Spatial Intuition

Before an operation, ask:

- Why should location affect this outcome?
- What geographic object represents the phenomenon?
- Is the relationship containment, adjacency, proximity, connectivity, or overlap?
- What geographic scale matches the decision?
- What variation is hidden inside the chosen unit?
- Could the boundary definition create the pattern?
- Are distance and area measured in suitable units?
- Are input dates compatible?
- What would make a result geographically implausible?
- What alternative explanation competes with the apparent pattern?

## Prediction Before Calculation

State a prediction before running analysis. Then compare expected and observed patterns.

A wrong prediction is useful when it exposes an incomplete mental model. A result that matches a prediction still needs validation because code or data errors can produce plausible numbers.

## Plain-Language Definition

> Spatial intuition is informed judgment about how geography shapes a question, method, result, and decision.

## Related Resources

- [Spatial question workflow](../guides/spatial_question_workflow.md)
- [Portfolio roadmap](../../planning/portfolio_roadmap.md)