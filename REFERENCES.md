# References and Attribution

This document identifies the principal data, standards, software, and documentation used by the Calgary Spatial ETL project. It also records the attribution required for the City of Calgary open data.

Links and licence information were reviewed on July 28, 2026. External terms and documentation can change, so verify the current version before redistributing data or publishing a derived product.

## City of Calgary Open Data

The project retrieves four public geospatial datasets from the [City of Calgary Open Data portal](https://data.calgary.ca/). The City of Calgary is the information provider.

| Project name | Official dataset | Catalogue ID | GeoJSON API endpoint |
|---|---|---|---|
| communities | [Community District Boundaries](https://data.calgary.ca/d/surr-xmvs) | `surr-xmvs` | [GeoJSON](https://data.calgary.ca/api/v3/views/surr-xmvs/query.geojson) |
| roads | [Major Road Network](https://data.calgary.ca/d/tqjs-vnhy) | `tqjs-vnhy` | [GeoJSON](https://data.calgary.ca/api/v3/views/tqjs-vnhy/query.geojson) |
| transit stops | [Calgary Transit Stops](https://data.calgary.ca/d/muzh-c9qc) | `muzh-c9qc` | [GeoJSON](https://data.calgary.ca/api/v3/views/muzh-c9qc/query.geojson) |
| land-use districts | [Land Use Districts](https://data.calgary.ca/d/qe6k-p9nh) | `qe6k-p9nh` | [GeoJSON](https://data.calgary.ca/api/v3/views/qe6k-p9nh/query.geojson) |

The endpoint URLs used by the application are declared in [`src/config.py`](src/config.py).

### Data Licence and Required Attribution

The catalogue pages identify the [Open Government Licence - City of Calgary, version 2.1](https://data.calgary.ca/d/Open-Data-Terms/u45n-7awa) as the governing licence.

The licence permits copying, modification, publication, adaptation, distribution, and commercial use for lawful purposes, subject to its conditions. When the information provider does not specify another attribution statement, it requires:

> Contains information licensed under the Open Government Licence – City of Calgary.

This project uses that statement for all four datasets.

The licence does not grant rights to City names, crests, logos, official symbols, third-party rights the City is not authorized to license, or use that suggests official status or City endorsement. The information is provided without warranty. Consult the current licence text for the complete terms.

Generated raw and processed GeoJSON files are excluded from Git by [`.gitignore`](.gitignore). Anyone who separately publishes those files, maps, tables, screenshots, or other derived products should retain the City attribution and comply with the licence in force when the information was accessed.

## Geospatial Standards and Formats

| Reference | Use in this project |
|---|---|
| [EPSG:4326 - WGS 84](https://epsg.org/crs_4326/WGS-84.html) | typical source CRS for GeoJSON longitude and latitude |
| [EPSG:3347 - NAD83 / Statistics Canada Lambert](https://epsg.org/crs_3347/NAD83-Statistics-Canada-Lambert.html) | target projected CRS for processed layers and PostGIS tables |
| [RFC 7946 - The GeoJSON Format](https://www.rfc-editor.org/rfc/rfc7946) | interchange format used for source and processed spatial files |
| [EPSG Dataset](https://epsg.org/) | authoritative registry for CRS identifiers and definitions |

EPSG is a trademark of the International Association of Oil & Gas Producers. Referencing an EPSG code identifies a coordinate reference system; it does not transfer ownership of the EPSG dataset or branding.

## Primary Software and Documentation

The project calls these open-source tools through their public APIs or command-line interfaces. Their names and links are included for technical reference; each project remains governed by its own licence.

### Python and Data Processing

- [Python 3 documentation](https://docs.python.org/3/) - language, standard library, `unittest`, paths, CSV handling, dataclasses, and command-line parsing.
- [pandas documentation](https://pandas.pydata.org/docs/) - tabular data structures used by the geospatial stack.
- [GeoPandas documentation](https://geopandas.org/en/stable/docs.html) - GeoDataFrames, spatial file I/O, CRS operations, and PostGIS output.
- [Shapely documentation](https://shapely.readthedocs.io/en/stable/) - geometry validity, `make_valid()`, buffering, and geometry operations.
- [PyProj documentation](https://pyproj4.github.io/pyproj/stable/) - coordinate reference systems and transformations through PROJ.
- [Fiona documentation](https://fiona.readthedocs.io/) and [Pyogrio documentation](https://pyogrio.readthedocs.io/) - geospatial vector file access used by the GeoPandas environment.
- [Requests documentation](https://requests.readthedocs.io/) - HTTP retrieval in the Extract stage.
- [python-dotenv documentation](https://bbc2.github.io/python-dotenv/) - optional environment-variable loading support.
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) - YAML support included in the project environment.

Exact installed Python package versions are recorded in [`requirements.txt`](requirements.txt). The maintainable Conda environment declaration is [`environment.yml`](environment.yml).

### Database and Spatial Publication

- [PostgreSQL documentation](https://www.postgresql.org/docs/) - relational database, schemas, SQL, indexes, and transactions.
- [PostGIS documentation](https://postgis.net/documentation/) - PostgreSQL geometry types, SRIDs, spatial functions, and GIST indexes.
- [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/) - database engines, connections, SQL expressions, and transaction scopes.
- [GeoAlchemy2 documentation](https://geoalchemy-2.readthedocs.io/) - SQLAlchemy spatial types and PostGIS integration used by GeoPandas.
- [Psycopg documentation](https://www.psycopg.org/docs/) - PostgreSQL driver used by SQLAlchemy in this project.

### Environment and Containers

- [Conda documentation](https://docs.conda.io/) and [Conda Forge](https://conda-forge.org/docs/) - Python environment creation and compatible geospatial packages.
- [Docker documentation](https://docs.docker.com/) - containers, images, networks, volumes, and Docker Compose.
- [`postgis/postgis` container image](https://hub.docker.com/r/postgis/postgis) - PostgreSQL 15 with PostGIS 3.4, declared in [`docker-compose.yml`](docker-compose.yml).
- [Jupyter documentation](https://docs.jupyter.org/) - notebooks used for practice, walkthroughs, and assessments.

## Development Assistance

[Visual Studio Code](https://code.visualstudio.com/) and [GitHub Copilot](https://github.com/features/copilot) were used during project development and documentation. AI-assisted material was reviewed and integrated in the context of this repository; Copilot is a development tool, not an authoritative source for the geospatial standards, software behavior, or licence terms cited above.

## Project Authorship and Licensing

The repository's source code, tests, SQL, and learning materials are maintained as project content and include AI-assisted material as disclosed above, unless a file states otherwise. External libraries are dependencies and are not copied into this repository.

As of July 28, 2026, this repository does not contain a root software `LICENSE` file. Copyright exists automatically, so public visibility on GitHub does not by itself grant other people a general right to copy, modify, or redistribute the project. Add an explicit software licence only after choosing the permissions you want to grant.

This references file records attribution and sources; it is not a substitute for the complete external licence texts and is not legal advice.
