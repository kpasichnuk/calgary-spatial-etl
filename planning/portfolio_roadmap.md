# GIS Developer Portfolio Roadmap

## Purpose

This roadmap combines two capabilities that a GIS developer needs:

1. **Geospatial development:** building reliable pipelines, databases, services, tests, and user-facing applications.
2. **Spatial reasoning:** framing useful geographic questions, selecting defensible methods, interpreting results, and explaining limitations.

The goal is not to choose development instead of analysis. The goal is to become a GIS developer who can identify spatial value and build dependable systems that deliver it.

## Portfolio Positioning

A useful professional statement is:

> I identify meaningful spatial questions and build reliable geospatial systems that answer them.

Development remains the primary specialization. Small analytical extensions are included throughout the development sequence so the technology always remains connected to a decision or user need.

## Learning Balance

During the three development projects, use an approximate balance:

- **80% development:** Python, SQL, PostGIS, APIs, testing, automation, deployment, and application architecture.
- **20% spatial reasoning:** question framing, spatial relationships, scale, measurement, assumptions, validation, interpretation, and communication.

After the three development projects, complete a deeper analysis case study with greater methodological depth.

This is a guideline rather than a time-tracking requirement. If an analytical question starts introducing an unrelated technology stack, reduce its scope and return to the current development objective.

## Portfolio Sequence

```text
Project 1: spatial ETL and PostGIS
    -> small community transit-stop density analysis
Project 2: spatial API or geospatial backend
    -> decision-focused proximity or spatial-query extension
Project 3: web GIS application
    -> interactive communication of spatial evidence
Project 4: dedicated spatial analysis case study
    -> deeper accessibility, suitability, network, or equity analysis
```

Projects 2, 3, and 4 are provisional. Their exact questions should be selected when the preceding project reveals which skills, data, and professional direction deserve deeper work.

## Tooling and Cost Constraint

Every project in this roadmap must remain buildable, testable, and demonstrable locally with open-source application tools. Proprietary GIS software is not required.

Public hosting is optional infrastructure rather than a learning prerequisite. Project 3 should begin as a static web GIS using precomputed GeoJSON or PMTiles so it can use a $0 static-hosting tier without an always-running API or database. Project 2 must retain a complete local demonstration path even if a temporary free public endpoint is added.

See the [open-source tools and hosting plan](open_source_and_hosting_plan.md) for the verified stack, hosting alternatives, current free-tier limitations, basemap considerations, and cost-control rules.

## Project 1: Calgary Spatial ETL

### Development Purpose

Build and explain a reliable pipeline that:

- extracts City of Calgary open data
- preserves provenance
- normalizes schemas, identifiers, geometry, and CRS
- blocks invalid publication through QA
- publishes approved layers to PostGIS transactionally
- verifies row counts, SRID, indexes, repeatability, and rollback

### Spatial Reasoning Extension

Use the trusted outputs to answer a deliberately limited first question:

> How does mapped transit-stop density vary among Calgary communities?

This extension belongs in the current repository because it directly demonstrates why the ETL guarantees matter.

The first analysis may compare:

- transit-stop counts by community
- community area in square kilometres
- stops per square kilometre
- raw counts versus area-normalized values
- boundary and data-quality edge cases

It must not claim to measure population equity, service frequency, walking accessibility, or network travel time without the additional data and methods those claims require.

### Project 1 Completion Gate

Project 1 is ready to close when:

- Modules 0-7 and their tests are complete.
- The ETL runs and its automated tests pass.
- The analysis extension answers its scoped question reproducibly.
- Results include assumptions, limitations, and several inspected edge cases.
- The root README explains the engineering and analytical value.
- The repository is safe to publish and attribution is complete.

## Project 2: Spatial API or Geospatial Backend

### Provisional Purpose

Create a separately deployable service that exposes useful spatial queries through a documented API. Candidate operations include:

- locate a point within a community
- find nearby transit stops
- filter by distance or containing district
- return GeoJSON with clear CRS and error contracts
- expose a summary generated from Project 1 data

### Development Skills

- API design and HTTP contracts
- request validation
- spatial SQL and PostGIS query planning
- pagination and response limits
- database connection management
- unit, integration, and contract testing
- containerization and deployment
- observability and safe error responses

### Spatial Reasoning Extension

Frame one user decision before designing endpoints. For example:

> Which mapped transit stops are within a stated distance of a proposed site, and what does that distance measure omit?

This introduces proximity, measurement choice, spatial indexing, and the distinction between straight-line proximity and real accessibility.

### Create-Later Gate

Do not create Project 2 merely because Project 1 has source files. Create it when:

- Project 1 meets its completion gate.
- The API user and decision are written in one paragraph.
- At least three endpoints and their contracts can be stated before coding.
- The service has an independent deployment purpose.
- The data dependency on Project 1 can be expressed as a stable database, file, or API contract.
- The API can be run, tested, and demonstrated locally without paid infrastructure.

At that point, create a sibling directory and separate Git repository rather than nesting it inside Project 1.

## Project 3: Web GIS Application

### Provisional Purpose

Build a user-facing map application that consumes a stable spatial API or published dataset and helps a defined audience compare geographic evidence.

Candidate capabilities include:

- map and table coordination
- community selection and comparison
- filtering and spatial search
- clear loading, empty, and error states
- accessible legends and symbology
- responsive layouts
- links between mapped results and their assumptions

### Development Skills

- frontend application architecture
- web mapping libraries
- API integration and asynchronous state
- map interaction and accessibility
- component and end-to-end testing
- performance with spatial payloads
- deployment and environment configuration

### Spatial Reasoning Extension

The application should communicate a defensible comparison rather than display layers without purpose. A possible question is:

> How can a planner compare mapped transit-stop coverage among communities without confusing stop density with service quality or accessibility?

### Create-Later Gate

Create Project 3 only when:

- Project 2 or another stable data service has a documented interface.
- A target user and recurring decision are known.
- A map is genuinely useful for that decision.
- The initial workflow can be described from opening the app to making a comparison.
- The app has value beyond demonstrating a mapping library.
- A static deployment using precomputed data has been evaluated before adding a paid backend dependency.

Create it as another sibling directory and separate Git repository.

## Project 4: Dedicated Spatial Analysis Case Study

After the three development projects, complete one deeper analytical project. Candidate directions include:

- walking or transit-network accessibility
- service-area gaps
- multi-criteria site suitability
- spatial inequality with population and demographic denominators
- spatial clustering and autocorrelation
- change over time

Select a question that requires stronger reasoning rather than simply more layers. The project should compare alternative methods, test sensitivity to assumptions, and explain uncertainty.

## Spatial Question Framework

Use this framework for every analytical extension:

1. **Decision:** Who will use the result, and what decision could change?
2. **Question:** What location, spatial relationship, and measurable outcome are involved?
3. **Hypothesis:** What pattern is expected before analysis?
4. **Data:** Which geometries, attributes, dates, CRS, and geographic scales are required?
5. **Method:** Why are containment, proximity, intersection, aggregation, routing, or clustering appropriate?
6. **Assumptions:** What does the method simplify or treat as true?
7. **Validation:** Which sample locations, edge cases, missing values, and surprising results will be inspected?
8. **Interpretation:** What does the result mean, and what does it not mean?
9. **Value:** What action, prioritization, or further investigation does the evidence support?
10. **Automation:** How will the valid method become tested and repeatable?

## Evidence Expected From Every Project

Each portfolio repository should make these elements easy to find:

- stakeholder or user
- decision and spatial question
- data sources and licences
- architecture and technology choices
- reproducible setup
- data-quality controls
- automated tests
- analytical assumptions
- results and limitations
- screenshots, maps, API examples, or other usable outputs
- next steps that do not overstate the evidence

## Repository and Workspace Timeline

### Now

Continue in `calgary-spatial-etl` only. Complete Project 1 and its analysis extension. Keep this roadmap as planning documentation, not executable coupling to future repositories.

### When Project 2 Starts

1. Create a sibling `spatial-api-project/` directory.
2. Initialize it as its own Git repository.
3. configure and test it independently.
4. Confirm Project 1 still opens and runs alone.
5. Create the portfolio multi-root workspace outside both repositories.

### When Project 3 Starts

1. Create a sibling `web-gis-application/` directory.
2. Initialize its independent repository and environment.
3. Add it to the existing portfolio workspace.
4. Keep its data/API dependency explicit and versioned.

The companion [workspace architecture](workspace_architecture.md) explains why these boundaries matter and includes the future workspace configuration.

The [open-source and hosting plan](open_source_and_hosting_plan.md) records the no-cost baseline and the conditions under which optional hosting expenses may become worthwhile.

## Review Rhythm

At the end of each project, perform four reviews:

- **Engineering review:** reliability, tests, security, maintainability, and deployment.
- **Spatial review:** scale, CRS, method, edge cases, uncertainty, and interpretation.
- **Portfolio review:** clarity of the README, evidence, screenshots, and honest attribution.
- **Career review:** which job descriptions match the demonstrated skills, and what recurring gap should the next project address?

The next project should be chosen from observed gaps, not from a desire to collect technologies.