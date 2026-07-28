# Docker Containers

## Core Idea

A container is an isolated, runnable instance of a container image.

It runs an application and its supporting software with its own process, filesystem, network, and environment configuration while sharing the host operating system's kernel. Containers are generally smaller and faster to start than full virtual machines because they do not boot a separate guest operating-system kernel.

## This Project's Container

[Docker Compose](../../docker-compose.yml) defines the local PostGIS service:

```yaml
services:
  postgis:
    image: postgis/postgis:15-3.4
    container_name: calgary-postgis
    ports:
      - "5433:5432"
    volumes:
      - postgis_data:/var/lib/postgresql/data
```

When Docker Compose starts this service, it creates and runs a container named `calgary-postgis`.

The resulting runtime can be pictured as:

```text
Linux host
    -> Docker Engine
        -> calgary-postgis container
            -> PostgreSQL 15
            -> PostGIS 3.4
            -> calgary_gis database
```

## Image Versus Container

An **image** is the reusable package or template from which containers are created. A **container** is a particular instance of that image.

This project uses:

```text
image:     postgis/postgis:15-3.4
container: calgary-postgis
```

A useful programming analogy is:

```text
class or blueprint -> image
object or instance -> container
```

The analogy is not exact, but it captures the template-versus-instance relationship. Multiple containers can be created from the same image, just as multiple objects can be created from one class.

## Compose Service Versus Container

A Docker Compose **service** is the configuration describing how a container should run. It includes the image, environment variables, ports, volumes, restart policy, and other settings.

The `postgis` service is a declaration in `docker-compose.yml`. The `calgary-postgis` container is the running instance created from that declaration.

```text
Compose service definition
    -> Docker creates container
    -> container runs PostgreSQL and PostGIS
```

## What Isolation Means

Inside its container, PostgreSQL has its own:

- processes
- filesystem view
- network identity
- environment variables
- installed PostgreSQL and PostGIS software

The isolation keeps the database runtime separate from Python packages in the `calgary-etl` Conda environment. The ETL code runs on the host and connects to PostgreSQL over a mapped network port.

Container isolation is useful, but it should not be treated as an absolute security boundary. Containers still share the host kernel and must be configured, updated, and granted privileges carefully.

## Port Mapping

PostgreSQL listens on port `5432` inside the container. The Compose configuration maps host port `5433` to it:

```text
Python on host
    -> localhost:5433
        -> calgary-postgis:5432
            -> PostgreSQL
```

The mapping uses this order:

```text
HOST_PORT:CONTAINER_PORT
5433:5432
```

Python running on the host therefore connects to `localhost:5433`. Software running inside the same Compose network would normally address the service by its service name and internal port instead.

## Containers and Persistent Data

A container is replaceable. Storing important database files only in its writable container layer would tie that data to the container's lifecycle.

This project uses the named volume `postgis_data`:

```text
calgary-postgis container
    -> /var/lib/postgresql/data
        -> postgis_data volume
```

The volume exists separately from the container. Docker can recreate the container while retaining the PostgreSQL database files in the volume.

This distinction matters:

- removing and recreating the container does not necessarily remove the volume
- explicitly deleting the volume removes the persisted database state
- committing source code to Git does not back up the Docker volume

## Environment Variables

The Compose service supplies initialization values inside the container:

```yaml
environment:
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  POSTGRES_DB: postgres
```

These are intentional local-development defaults. They initialize the database container; they are not suitable production credentials.

The ETL process uses its own connection configuration, such as `DATABASE_URL`, to reach the database from outside the container.

## Container Lifecycle

Common commands include:

```bash
docker compose up -d
docker compose ps
docker compose logs postgis
docker compose stop
docker compose down
```

Their roles differ:

- `up -d` creates or starts services in the background
- `ps` reports container state
- `logs postgis` shows service output
- `stop` stops the container without removing it
- `down` removes the Compose containers and network

A running status proves that the container process is active. It does not by itself prove that the database accepts connections, that PostGIS is enabled in the correct database, or that ETL integration tests pass.

## Container Versus Virtual Machine

A virtual machine emulates a computer and runs a separate guest operating system with its own kernel. A container isolates processes while sharing the host kernel.

| Container | Virtual machine |
|---|---|
| shares the host kernel | runs a guest operating-system kernel |
| usually starts quickly | usually takes longer to boot |
| commonly packages one service | can host a complete operating system |
| generally smaller | generally larger |

Both provide isolation, but at different layers and with different operational tradeoffs.

## Container Versus Conda Environment

These environments solve different dependency problems:

- **Conda environment:** isolates the Python interpreter and Python/geospatial packages used by the ETL code.
- **Docker container:** packages and runs the PostgreSQL/PostGIS database service.

In this project:

```text
calgary-etl Conda environment -> runs Python ETL code
calgary-postgis container      -> runs PostgreSQL and PostGIS
```

The network connection between them lets the Python Load stage publish approved spatial data to PostGIS.

## Plain-Language Definition

> A container is an isolated running instance of an image that packages an application and its required software while sharing the host operating system's kernel.

## Related Resources

- [Environment dependency definitions](project1_environment_dependency_definitions.md)
- [Module 1 environment and PostGIS reference](../reference/project1_module_1_environment_postgis_reference.md)
- [Module 1 environment and PostGIS practice](../practice/project1_module_1_environment_postgis_practice.ipynb)
- [Module 6 Load and PostGIS reference](../reference/project1_module_6_load_postgis_reference.md)
