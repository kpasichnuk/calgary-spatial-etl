# Portfolio Repository and Multi-Root Workspace Architecture

## Core Recommendation

Keep each main portfolio project in its own directory, Git repository, environment, and GitHub repository. When the second project exists, group the independent folders in a VS Code multi-root workspace stored above them.

```text
gis-portfolio/
├── gis-portfolio.code-workspace
├── calgary-spatial-etl/
├── spatial-api-project/
├── web-gis-application/
└── spatial-analysis-case-study/
```

The workspace is an editor view over several projects. It does not merge their files, dependencies, deployments, Git histories, or ownership boundaries.

## Three Different Concepts

### Directory

A directory is a filesystem container. Sibling project directories keep one project from physically living inside another.

### Git Repository

A Git repository records one project's files and history. Each repository has its own branches, commits, tags, remote, issues, and release lifecycle.

### VS Code Workspace

A VS Code workspace controls which folders appear in one editor window and can store shared editor settings or tasks. A multi-root workspace lists multiple folders without changing their Git boundaries.

These concepts are related but not interchangeable.

## Why Not Put Every Project in This Repository?

A single repository can be appropriate when components form one product, share releases, and must change atomically. That is not yet true for the proposed portfolio projects.

Putting unrelated portfolio projects into `calgary-spatial-etl` would create several problems:

- Project 1's ETL purpose would become harder to explain.
- Python API and frontend dependencies could become entangled.
- Git history would mix unrelated learning objectives.
- A reviewer could not clone one focused project.
- deployment configuration would become ambiguous.
- project completion would be difficult to define.
- future replacement of one project would affect the others.

Separate repositories preserve a clear story and force every project to document its public contract.

## Advantages of Separate Project Workspaces

### Focused Architecture

Each project has one primary purpose. Its README, source tree, tests, and issue history can be evaluated without navigating unrelated work.

### Independent Environments

Project 1 may use Python, GeoPandas, and PostGIS. Project 3 may use TypeScript and a web mapping library. Separate environments prevent dependency upgrades in one project from destabilizing another.

### Independent Git History

Commits explain one project's evolution. Releases and tags remain meaningful, and accidental staging across unrelated projects is less likely.

### Independent Deployment

An ETL job, API service, and web application have different runtime and security requirements. Separate repositories support distinct deployment pipelines and environment variables.

### Clear Portfolio Review

An employer can choose the project relevant to a role, read a focused README, run its tests, and see a coherent commit history.

### Explicit Contracts

When Project 2 consumes Project 1 data, it should rely on a documented contract such as:

- a named PostGIS schema and table contract
- a versioned GeoJSON or GeoPackage export
- a data dictionary
- an API response

This is healthier than importing internal functions from an unrelated repository. It models professional system boundaries.

### Flexible Ownership and Replacement

A project can be archived, redesigned, or deployed independently. The portfolio workspace can change its folder list without rewriting project history.

## Advantages of a Multi-Root Workspace

Once two projects exist, a multi-root workspace provides convenience without sacrificing isolation:

- navigate among related repositories in one window
- search across the portfolio when intentionally comparing contracts
- see separate Source Control entries for each repository
- define portfolio-wide tasks that invoke project-specific commands
- compare documentation and naming conventions
- keep the overall development sequence visible

It also allows each repository to remain independently openable. The multi-root workspace is an optional coordination layer, not a runtime dependency.

## Risks and Working Rules

### Wrong Repository

A terminal or Source Control action can target the wrong project.

**Rule:** check the terminal working directory and repository name before environment, package, commit, or push commands.

### Wrong Environment

A Python interpreter selected for one folder may not match another project.

**Rule:** keep project-specific interpreter settings within the appropriate folder and name terminal tabs by project.

### Noisy Search Results

Workspace-wide search can mix APIs, ETL code, and frontend code.

**Rule:** scope searches to the active folder unless cross-project comparison is intentional.

### Accidental Coupling

Convenient relative paths between sibling folders can make projects work only inside one machine layout.

**Rule:** communicate through documented database, file, package, or API contracts. Do not use paths such as `../calgary-spatial-etl/src` from another project.

### Shared Secrets

A portfolio-level settings file is the wrong place for credentials.

**Rule:** keep secrets out of Git and configure them per project through ignored environment files or secure deployment settings.

### AI Assistant Scope

An assistant may search all roots and infer the wrong owning project.

**Rule:** identify the active repository and goal in requests that involve multiple roots.

## Why the Workspace File Lives Above the Repositories

Place `gis-portfolio.code-workspace` in the parent `gis-portfolio/` directory because it describes the relationship among repositories rather than belonging to one of them.

This avoids making Project 1 appear to own Projects 2 and 3. It also prevents a clone of one repository from containing broken references to sibling folders that a reviewer may not have.

The workspace file may remain local. If it is later version-controlled, it should live in a small portfolio-coordination repository or another intentional shared location.

## Future Workspace Configuration

Do not create this file until Project 2 exists. At that point, a minimal configuration can be:

```json
{
    "folders": [
        {
            "name": "Project 1 - Calgary Spatial ETL",
            "path": "calgary-spatial-etl"
        },
        {
            "name": "Project 2 - Spatial API",
            "path": "spatial-api-project"
        }
    ],
    "settings": {
        "files.exclude": {
            "**/__pycache__": true,
            "**/.pytest_cache": true,
            "**/.ipynb_checkpoints": true
        }
    }
}
```

Add Project 3 later by adding another folder entry. Avoid putting one project's interpreter path, formatter, or environment variables in global workspace settings when they do not apply to every root.

## When a Monorepo Would Be Better

Separate repositories are not a universal rule. A monorepo may become appropriate if several components:

- form one deployable product
- share one release cycle
- require atomic cross-component changes
- share substantial tested code
- are maintained as one system rather than separate portfolio demonstrations

If the future API and web app become one tightly coupled product, reconsider the boundary based on evidence. Do not combine them merely because VS Code can display both.

## Future Setup Checklist

When Project 2 is ready:

1. Create a `gis-portfolio/` parent if one does not already exist.
2. Keep `calgary-spatial-etl/` as an intact repository.
3. Create `spatial-api-project/` as its sibling.
4. initialize Project 2 independently using its chosen stack.
5. Verify each project opens, installs, runs, and tests alone.
6. Create `gis-portfolio.code-workspace` in the parent directory.
7. Add both folders using relative paths.
8. Open the workspace and verify separate Source Control entries.
9. Document the data contract between projects.
10. Keep secrets and project-specific settings inside the appropriate project boundary.

When that milestone arrives, an AI programming assistant can create the sibling directory, scaffold Project 2, and produce the multi-root workspace after confirming the parent path and selected technology stack.

## Decision Summary

Use separate repositories to preserve technical, historical, deployment, and portfolio clarity. Use a multi-root workspace later to gain navigation and coordination convenience. The workspace should connect projects for the developer without coupling them for users or deployments.