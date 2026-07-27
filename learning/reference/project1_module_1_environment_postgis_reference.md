# Project 1 Module 1: Environment and PostGIS Reference

## Purpose

This reference explains the project context, Python environment, Docker, and PostGIS concepts behind [Module 1 environment and PostGIS practice](../practice/project1_module_1_environment_postgis_practice.ipynb).

## 1. Project Context

Commands and relative paths depend on the current working directory. For this project, run operational commands from the repository root, where these markers exist:

- `environment.yml`
- `docker-compose.yml`
- `src/`
- `tests/`

A reliable root-finding function checks the current path and its parents for known markers. It should not silently change the process working directory.

```python
from pathlib import Path

project_root = Path.cwd()
```

Useful `Path` properties include:

- `.name`: final path component
- `.parent`: containing path
- `.resolve()`: absolute normalized path
- `.exists()`: whether the path exists
- `.is_file()` and `.is_dir()`: path type

## 2. Python Interpreter and Environment

The interpreter is the Python executable running the process. A Conda environment contains an interpreter and an isolated dependency set.

```bash
conda activate calgary-etl
which python
python --version
```

For this project, the interpreter should come from the `calgary-etl` environment. VS Code terminals and notebook kernels can select different interpreters, so confirm both contexts independently.

## 3. Dependency Reproducibility

`environment.yml` declares the environment another developer should recreate.

```bash
conda env create -f environment.yml
conda env update -f environment.yml --prune
```

An installed package proves only that the current environment has it. A declared dependency records that the project requires it.

The geospatial stack includes compiled components, so compatible packages from Conda Forge reduce installation conflicts.

## 4. Environment Variables and Secrets

Environment variables provide runtime configuration without hard-coding values.

```bash
export DATABASE_URL='postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE'
```

Code can read the value without printing it:

```python
import os

database_url = os.getenv("DATABASE_URL")
```

Do not commit real passwords, tokens, `.env` files, or notebook outputs containing secrets.

## 5. Docker Concepts

Docker Compose defines the local PostGIS service.

- **Image:** reusable service template.
- **Container:** running image instance.
- **Volume:** persistent storage outside the disposable container layer.
- **Port mapping:** connects a host port to a container port.
- **Environment configuration:** initializes the container's local development account and database.

Start and inspect the service:

```bash
docker compose up -d
docker compose ps
```

The project maps host port `5433` to PostgreSQL port `5432` inside the container.

## 6. PostgreSQL and PostGIS

PostgreSQL is a relational database. PostGIS is an extension that adds:

- geometry and geography types
- spatial reference metadata
- spatial functions such as `ST_Intersects`
- spatial indexes

Initialize the project database:

```bash
docker compose exec -T postgis psql -U postgres -d postgres < sql/init.sql
```

The script creates `calgary_gis` when needed and enables PostGIS extensions idempotently.

## 7. Connection URLs

A SQLAlchemy PostgreSQL URL has these parts:

```text
postgresql+psycopg2://user:password@host:port/database
```

For this local project:

- driver: `postgresql+psycopg2`
- host: `localhost`
- host port: `5433`
- database: `calgary_gis`

The container itself listens on port `5432`; Python running on the host uses `5433`.

## 8. Safe Verification

Verify layers of setup separately:

1. `docker compose ps` proves the container reports a running state.
2. A database connection proves the port and credentials work.
3. Querying PostGIS proves the extension exists.
4. Running integration tests proves selected application behavior works with the database.

No single check proves all four.

## 9. Common Failures

### Wrong Python interpreter

Symptoms include missing imports or unexpected package versions. Confirm `which python`, the VS Code interpreter, and notebook kernel.

### Connection refused

Check:

1. Docker is running.
2. The container is healthy.
3. The host port is `5433`.
4. `DATABASE_URL` is correct.

### Database does not exist

Run `sql/init.sql` against the initial `postgres` database.

### PostGIS functions unavailable

Confirm the extension is installed in `calgary_gis`, not only in another database.

### Data disappears after container recreation

Inspect the named volume configuration. Containers are replaceable; persistent database state belongs in the volume.

## 10. Mental Model

```text
repository root
    -> declared Conda environment
    -> selected Python interpreter/kernel
    -> Docker Compose service
    -> PostgreSQL database
    -> PostGIS extension
    -> application database connection
```

Diagnose this chain from left to right. Do not change ETL logic to compensate for a broken environment prerequisite.

## Review Checklist

You should be able to explain:

- working directory versus project root
- interpreter versus Conda environment
- installed versus declared dependencies
- environment variables and secret handling
- image, container, volume, and port mapping
- PostgreSQL versus PostGIS
- why host port `5433` differs from container port `5432`
- what each setup verification proves

## Companion Resources

- [Module 1 environment and PostGIS practice](../practice/project1_module_1_environment_postgis_practice.ipynb)
- [Module 6 Load and PostGIS reference](project1_module_6_load_postgis_reference.md)
- [Project 1 study guide](../guides/project1_study_guide.md)
