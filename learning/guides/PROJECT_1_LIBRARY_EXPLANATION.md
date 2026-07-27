# Project 1 Library Explanation

This note explains why each Python library is included in the Calgary Spatial ETL project and where it is used in the pipeline.

## Dependency List

- pandas
- geopandas
- shapely
- pyproj
- fiona
- sqlalchemy
- psycopg2-binary
- python-dotenv
- pyyaml

## Why `pip freeze > requirements.txt` Is Included

Command:

```bash
pip freeze > requirements.txt
```

Purpose:
- Writes a snapshot of all installed packages and exact versions from the active environment into `requirements.txt`.

Why this matters in Project 1:
- Reproducibility: anyone can recreate the same package set with `pip install -r requirements.txt`.
- Stability: pinned versions reduce "works on my machine" issues for your ETL runs.
- Collaboration: reviewers, teammates, and CI can install the same stack quickly.

Practical note:
- `pip freeze` captures everything currently installed in the environment, including packages you may not directly use.
- For portfolio projects, it is common to keep both files:
	- `requirements.txt` as the exact lock snapshot.
	- `environment.yml` as the curated high-level environment definition.

## Why `cat > environment.yml << 'YAML'` Is Used

Command:

```bash
cat > environment.yml << 'YAML'
```

Purpose:
- This is a shell command, not Python.
- It starts writing everything you type next into a file named `environment.yml`.
- The `<< 'YAML'` part tells the shell to keep reading lines until you type `YAML` on its own line.

How it ends:
- Paste the file contents after the command.
- Type `YAML` on a new line by itself.
- Press Enter, and the file is saved.

Why this matters in Project 1:
- It is a quick way to create a new text file directly from the terminal.
- It avoids needing to open a text editor if you are following a command-line workflow.
- It is commonly used in setup guides because the exact file content can be shown inline.

If you do not want to use the heredoc form:
- You can create the file in VS Code or another editor instead.
- You can also use `cat > environment.yml` without `<< 'YAML'`, then end input with Ctrl+D.

## Why `docker-compose.yml` Is Used

File:

- `docker-compose.yml`

Purpose:
- Describes one or more containers in a repeatable YAML format.
- Lets you start PostgreSQL/PostGIS with one command instead of retyping a long `docker run` command.
- Keeps the database setup in version control so the project can be recreated later.

Why this matters in Project 1:
- It is a realistic employer skill because many teams use Docker Compose for local development.
- It makes the PostGIS setup easier to share, review, and reset.
- It keeps the WSL workflow clean by separating the database service from your Python environment.

How you use it:
- Run `docker compose up -d` to start the database service.
- Run `docker compose down` to stop it.
- Use `docker compose exec postgis psql -U postgres -d postgres` to connect inside the container.

In this project, the compose file defines a `postgis` service backed by the `postgis/postgis:15-3.4` image and a persistent volume for database data.

## Why Each Library Is Needed

### 1) pandas
Purpose: general tabular data processing.

How it helps in this project:
- Cleans and normalizes non-spatial columns.
- Handles null values and duplicate checks.
- Builds the QA summary table and writes CSV output.

Most used in:
- Transform step (column cleanup, types, dates)
- QA step (counts and summary metrics)

### 2) geopandas
Purpose: spatial dataframe workflows built on pandas.

How it helps in this project:
- Reads and writes geospatial files (GeoJSON, Shapefile, GeoPackage).
- Stores geometry in a dataframe-like structure.
- Reprojects data to a standard CRS.
- Loads layers to PostGIS using built-in methods.

Most used in:
- Extract, Transform, and Load steps

### 3) shapely
Purpose: geometry operations and validity handling.

How it helps in this project:
- Checks geometry validity.
- Repairs invalid geometries where possible.
- Supports spatial geometry logic (buffer, intersection, etc.) if needed.

Most used in:
- Transform step
- QA step (invalid geometry counts)

### 4) pyproj
Purpose: coordinate reference system (CRS) definitions and transformations.

How it helps in this project:
- Converts datasets from mixed CRS into one common CRS.
- Prevents layer mismatch during analysis and loading.

Most used in:
- Transform step (CRS standardization)

### 5) fiona
Purpose: low-level geospatial file I/O backend.

How it helps in this project:
- Provides robust vector format read/write support used by GeoPandas.
- Helps with interoperability across common GIS formats.

Most used in:
- Extract and Transform file reads/writes

### 6) sqlalchemy
Purpose: database engine and SQL connection management.

How it helps in this project:
- Creates clean, reusable PostgreSQL/PostGIS connections.
- Executes SQL statements for index creation and analyze operations.

Most used in:
- Load step

### 7) psycopg2-binary
Purpose: PostgreSQL driver for Python.

How it helps in this project:
- Allows SQLAlchemy (and direct Python code) to communicate with Postgres/PostGIS.

Most used in:
- Load step (database connectivity)

### 8) python-dotenv
Purpose: environment variable management from a .env file.

How it helps in this project:
- Keeps credentials and connection strings out of source code.
- Makes local setup easier and safer.

Most used in:
- Config and Load steps

### 9) pyyaml
Purpose: YAML parsing for structured configuration.

How it helps in this project:
- Supports config-driven dataset definitions and settings.
- Keeps project options outside code for easier maintenance.

Most used in:
- Config, Extract, and Transform steps

## Pipeline-to-Library Mapping

- Extract: geopandas, fiona, pyyaml
- Transform: pandas, geopandas, shapely, pyproj
- QA: pandas, shapely
- Load: geopandas, sqlalchemy, psycopg2-binary
- Configuration and secrets: python-dotenv, pyyaml

## Minimal vs Optional (Practical Recommendation)

Minimal for first end-to-end run:
- pandas
- geopandas
- shapely
- pyproj
- sqlalchemy
- psycopg2-binary
- python-dotenv

Commonly included for stronger portability/config workflows:
- fiona
- pyyaml

## One-Line Summary

Think of the stack as:
- Data wrangling: pandas
- Spatial wrangling: geopandas + shapely + pyproj + fiona
- Database loading: sqlalchemy + psycopg2-binary
- Project configuration: python-dotenv + pyyaml
