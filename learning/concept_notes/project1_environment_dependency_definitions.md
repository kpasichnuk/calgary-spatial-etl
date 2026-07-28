# Environment Dependency Definitions

## Core Idea

An environment dependency definition is a machine-readable description of the software a project needs in order to run.

It can declare:

- the Python version
- required libraries
- package versions or version ranges
- package sources or channels
- packages installed by different package managers
- sometimes platform-specific system dependencies

The definition is an installation recipe. The installed environment is the result of applying that recipe.

## Definition Versus Environment

These are related but different:

- **Dependency definition:** a file describing what should be installed.
- **Environment:** the actual interpreter and installed packages on a computer.

For example, [environment.yml](../../environment.yml) declares that this project needs Python 3.11 and geospatial libraries. The active `calgary-etl` Conda environment contains the particular package builds currently installed to satisfy that declaration.

An import succeeding in one developer's environment does not prove the dependency is declared. Another developer needs the definition to recreate the setup.

## This Project's Conda Definition

The main environment definition is [environment.yml](../../environment.yml). Its structure includes:

```yaml
name: calgary-etl
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pandas
  - geopandas
  - shapely
  - pyproj
  - fiona
  - sqlalchemy
  - geoalchemy2
  - psycopg2
  - pip
  - pip:
      - python-dotenv
      - pyyaml
```

The complete file also declares `proj`, `proj-data`, and other packages used by the spatial stack.

Each part has a role:

| Definition part | Meaning |
|---|---|
| `name` | default name for the created Conda environment |
| `channels` | repositories from which Conda resolves packages |
| `dependencies` | Python, libraries, and tools Conda should install |
| `python=3.11` | version constraint for the interpreter |
| nested `pip` list | packages that pip installs inside the Conda environment |

Create the declared environment with:

```bash
conda env create -f environment.yml
```

Update an existing environment and remove packages no longer declared with:

```bash
conda env update -f environment.yml --prune
```

## Why Conda Forge Matters Here

GeoPandas depends on compiled geospatial libraries such as GEOS, PROJ, and GDAL-related components. Conda resolves compatible package builds from the configured channel, not only Python source packages.

Using `conda-forge` gives the solver one consistent source for much of this compiled geospatial stack. The channel is therefore part of the dependency definition, not incidental metadata.

## This Project's Pip Definition

[requirements.txt](../../requirements.txt) is another dependency definition. It lists Python packages with exact versions:

```text
geopandas==1.1.4
GeoAlchemy2==0.18.0
psycopg2-binary==2.9.12
pyproj==3.7.2
shapely==2.1.2
SQLAlchemy==2.0.51
```

Install that list into the active environment with:

```bash
pip install -r requirements.txt
```

The file includes direct project packages and transitive dependencies such as NumPy, packaging, and six. Exact pins make Python package versions more repeatable than unpinned names, but they do not capture every factor needed to reproduce an environment on every operating system.

## Top-Level and Transitive Dependencies

A **top-level dependency** is selected because the project directly uses it. Examples include GeoPandas, SQLAlchemy, and GeoAlchemy2.

A **transitive dependency** is required by another package. For example, GeoPandas relies on lower-level packages such as pandas, NumPy, PyProj, and Shapely.

A concise environment definition often emphasizes top-level requirements and lets the package solver choose compatible transitive versions. A generated or pinned package list may record both kinds.

## Version Constraints

Dependency definitions can express different levels of flexibility:

```text
geopandas          any version the solver considers compatible
python=3.11        a constrained interpreter version
geopandas==1.1.4   exactly one package version
```

Broader constraints make updates easier but allow installations to change over time. Exact pins improve version consistency but may be platform-sensitive and require deliberate maintenance when security or compatibility updates are needed.

## Definition Versus Lock File

A lock file records the package solver's exact resolution, often including transitive versions, builds, hashes, and platform information.

This repository has dependency definitions, including an exact Python version list in `requirements.txt`, but it does not currently contain a complete Conda lock file. Therefore, package versions are substantially documented without every environment detail being frozen across platforms.

## Python Environment Versus Full Runtime

The Python dependency definition does not describe the entire system by itself. This project also depends on:

- Docker and Docker Compose
- the `postgis/postgis:15-3.4` container image
- PostgreSQL and PostGIS configuration
- environment variables such as `DATABASE_URL`
- the correct VS Code interpreter and notebook kernel

[Docker Compose](../../docker-compose.yml) defines the database service separately. Together, the repository files describe the larger runtime context.

## Common Mistakes

### Installing Without Declaring

Running `pip install some-package` may fix the current machine, but collaborators and automated systems will not know that the project requires it until the dependency file is updated.

### Declaring Without Updating

Changing a dependency definition does not automatically change an already-created environment. Run the appropriate update command and verify the selected interpreter.

### Mixing Package Managers Carelessly

Conda and pip can coexist, as shown in `environment.yml`, but compiled packages should generally be resolved through the project's established Conda pattern. Unplanned pip replacements can create incompatible binary combinations.

### Assuming a File Proves the Active Environment

A correct `environment.yml` does not prove that VS Code, a terminal, and a notebook are using the environment created from it. Check the interpreter and notebook kernel separately.

## Plain-Language Definition

> An environment dependency definition is a machine-readable installation recipe that lists the software and versions a project needs to run.

## Related Resources

- [Module 1 environment and PostGIS reference](../reference/project1_module_1_environment_postgis_reference.md)
- [Module 1 environment and PostGIS practice](../starters/project1_module_1_environment_postgis_practice.ipynb)
- [Data contracts and stage boundaries](project1_data_contracts.md)
