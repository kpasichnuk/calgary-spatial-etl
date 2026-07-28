# Open-Source Tools and Hosting Plan

## Verification Summary

The complete portfolio roadmap can be developed, tested, demonstrated locally, and documented with open-source software.

A publicly accessible web application does **not** necessarily require paid hosting. The recommended Project 3 architecture can be deployed as a static site containing precomputed spatial data, with no continuously running server or database.

An always-on public Python API connected to persistent hosted PostGIS is different. It may fit within temporary or constrained free tiers, but dependable availability should be treated as optional paid infrastructure.

This review was verified against official project and provider information on **July 28, 2026**. Hosting prices and free-tier limits can change, so they must be checked again when Projects 2 and 3 begin.

## Important Distinctions

### Open Source

Open-source software provides source code under a licence that permits use, inspection, modification, and redistribution under stated conditions.

### Free of Charge

A service may currently cost $0 without being open source. GitHub Pages, Cloudflare Pages, Render, and Supabase are hosted services operated by companies under their own terms.

### Self-Hosted

Open-source software can run on a personal computer or self-managed server. This avoids a platform subscription but still uses hardware, electricity, networking, maintenance, and security effort.

The roadmap should therefore promise an **open-source application stack**, not that every optional account or hosting platform is open source.

## Verified Open-Source Stack

### Project 1: ETL and Introductory Analysis

| Need | Open-source option | Role |
|---|---|---|
| Language | Python | ETL, analysis, testing, and automation |
| Tabular analysis | pandas | schemas, aggregation, and summaries |
| Spatial analysis | GeoPandas, Shapely, PyProj | geometry operations, CRS, joins, and measurement |
| Database | PostgreSQL and PostGIS | spatial storage, indexing, querying, and transactions |
| Database access | SQLAlchemy, GeoAlchemy2, psycopg | Python database integration |
| Reproducible services | Docker Engine/Moby and Docker Compose | local PostGIS and application containers |
| Notebooks | JupyterLab and Jupyter Notebook | executable learning and analysis |
| Desktop GIS | QGIS | optional visual inspection and cartographic review |
| Testing | Python `unittest` or pytest | deterministic and integration tests |

PostgreSQL uses the liberal PostgreSQL Licence. GeoPandas is BSD-3-Clause software. QGIS and PostGIS are established open-source geospatial projects.

### Project 2: Spatial API

| Need | Open-source option | Role |
|---|---|---|
| API framework | FastAPI | validated HTTP and OpenAPI contracts |
| Application server | Uvicorn | ASGI service runtime |
| Data validation | Pydantic | request and response models |
| Spatial database | PostgreSQL and PostGIS | indexed spatial queries |
| ORM/SQL | SQLAlchemy and GeoAlchemy2 | database integration |
| Testing | pytest, HTTPX, and FastAPI TestClient | unit, integration, and contract tests |
| Packaging | Docker Engine/Moby | portable local and hosted deployment |

FastAPI is MIT-licensed and can be deployed to any compatible host. A proprietary API gateway or commercial GIS server is not required.

### Project 3: Web GIS Application

| Need | Open-source option | Role |
|---|---|---|
| Language | TypeScript | typed browser application code |
| UI | React or standards-based HTML/CSS/JavaScript | interface and application state |
| Build tool | Vite | local development and static production build |
| Web map | MapLibre GL JS, OpenLayers, or Leaflet | browser map rendering and interaction |
| Static spatial delivery | GeoJSON or PMTiles | data files loaded without an application server |
| Tests | Vitest and Playwright | component and browser workflow tests |

MapLibre GL JS renders interactive maps in the browser. PMTiles can package tiled spatial data into a single read-only archive served with HTTP range requests. Neither requires a proprietary map SDK.

### Project 4: Deeper Spatial Analysis

The exact stack depends on the selected question. Open-source choices include:

- PySAL for spatial statistics
- NetworkX, OSMnx, or pgRouting for network analysis
- SciPy and statsmodels for statistical methods
- Rasterio, GDAL, and xarray for raster or multidimensional analysis
- QGIS for visual review and final cartography
- GeoPandas and PostGIS for vector operations and reproducible data management

No ArcGIS licence is required to complete the proposed case study, although learning how employers use ArcGIS may still have career value later.

## Development Environment Caveats

### VS Code

The Microsoft VS Code product is free to use but distributed under Microsoft's product licence. Its upstream `vscode` source is MIT-licensed. VSCodium provides freely licensed binaries built from that source and is the strict open-source alternative.

Using VS Code does not make the portfolio application proprietary. It is a development tool, not an application dependency.

### GitHub and GitHub Copilot

Git is open source. GitHub and GitHub Copilot are proprietary hosted services. The repositories can be mirrored to another Git host, and the projects can be built without Copilot.

GitHub remains practical for portfolio visibility, issue tracking, and static hosting, but it is not required by the source code.

### Conda Distributions

Conda itself is open source, but distributions and package channels can have separate terms. Miniforge is the clearest community-led open-source distribution when strict open-source tooling is desired.

The existing Miniconda environment can still be used for personal learning. Recheck its current terms before organizational or commercial deployment.

### Containers

On Linux, Docker Engine/Moby and Docker Compose provide an open-source-oriented path. Docker Desktop has separate commercial terms and is not required for this Linux workflow. Podman is another open-source container option.

## Recommended No-Cost Public Architecture

The safest $0 hosting plan is a static Project 3 application:

```text
Project 1 ETL and analysis
    -> generate reviewed GeoJSON or PMTiles
    -> commit or release a small public data artifact
Project 3 build
    -> bundle HTML, CSS, TypeScript, and MapLibre
Static host
    -> serve application and spatial files over HTTPS
Browser
    -> render, filter, and compare data locally
```

This architecture does not require:

- an always-running Python process
- a public PostGIS database
- server-side sessions
- paid compute
- a purchased domain

The site can use the host's provided subdomain. A custom domain is optional and normally has an annual registration cost even when the host supports it for free.

### Suitable Static Hosts

As of the verification date:

- **GitHub Pages** hosts static HTML, CSS, and JavaScript from a GitHub repository and provides a `github.io` address.
- **Cloudflare Pages** lists a $0 tier with unlimited sites, static requests, and bandwidth, subject to its terms and build limits.
- **Render Static Sites** can also be deployed for $0, subject to included bandwidth and build-pipeline allowances.

The provider is replaceable because the deployed artifact is ordinary static content.

## Optional Live API Demonstration

Project 2 should be complete and valuable even when run locally:

- repository and architecture documentation
- automated tests
- OpenAPI schema
- example requests and responses
- local Docker Compose demonstration
- screenshots or a short recorded walkthrough

A public endpoint is useful but not necessary to prove API development skill.

### Free-Tier Demonstration

Current free services can support a low-traffic demonstration, with limitations:

- Render free web services spin down after 15 minutes without inbound traffic and can take about one minute to restart.
- Render grants a limited number of free instance hours and applies bandwidth/build limits.
- Render's free PostgreSQL database expires after 30 days, so it is not a durable portfolio database.
- Supabase currently offers two free projects and a small PostgreSQL database allocation, but inactive free projects pause and limits apply.

Before selecting a managed database, verify that the required PostGIS extension and connection behavior are available on the current plan.

Free tiers are appropriate for learning and occasional demonstrations. They should not be described as reliable production infrastructure.

### Paid Always-On Demonstration

If a continuously available API and persistent database become important, some payment is likely.

For scale only, Render's published entry prices on the verification date started at approximately:

- **$7 USD/month** for a starter web service
- **$6 USD/month** for a basic 256 MB PostgreSQL instance

That suggests a nominal minimum near **$13 USD/month**, before taxes, bandwidth overages, storage, domains, backups, or a database size appropriate for the final workload. These prices are examples, not a commitment or recommendation.

Do not pay for hosting merely to make the architecture look professional. Pay only when reliable public availability creates enough portfolio or operational value to justify recurring cost.

## Basemap and Tile Costs

MapLibre is open source, but map libraries do not supply unlimited production basemap infrastructure.

OpenStreetMap data is open under its data licence, while the standard `tile.openstreetmap.org` service is community funded, best effort, and governed by a usage policy. It requires visible attribution and proper caching, prohibits bulk downloading, and may block inappropriate use.

For the portfolio app, choose one of these strategies:

1. Use no basemap when community polygons and labels provide enough context.
2. Use a hosted tile provider's documented free tier and attribution, then monitor its limits.
3. Build and host a Calgary-focused PMTiles basemap or thematic tiles when data size and licences permit.
4. Use standard OSM tiles only for modest interactive viewing that complies with the current tile policy, without assuming an availability guarantee.

Do not hard-code a proprietary provider into the application's analytical logic. Keep the basemap source configurable.

## Expected Cost by Portfolio Stage

| Stage | Required service cost | Recommended approach |
|---|---:|---|
| Project 1 local ETL and analysis | $0 | local open-source stack |
| Project 1 GitHub portfolio | $0 at current GitHub public-repository terms | publish code and documentation |
| Project 2 local API | $0 | Docker Compose, tests, and local OpenAPI docs |
| Project 2 public demo | $0 possible with limitations | optional sleeping free service; preserve local demo path |
| Project 3 static web GIS | $0 possible | static host plus precomputed GeoJSON or PMTiles |
| Project 3 custom domain | optional paid cost | use provider subdomain until a domain adds value |
| Always-on API and PostGIS | likely recurring cost | add only after measuring portfolio value |
| Project 4 analysis | $0 | local open-source analysis stack and static results |

Internet access, computer hardware, electricity, backups, and optional training materials are outside these hosting estimates.

## Cost-Control Rules

1. Prefer static outputs for public portfolio demonstrations.
2. Keep every project runnable locally without a commercial account.
3. Treat hosted providers as replaceable adapters, not application architecture.
4. Do not enter a payment method unless billing limits, alerts, and shutdown behavior are understood.
5. Enable provider spend caps where available.
6. Avoid committing credentials or provider-specific secrets.
7. Recheck prices and terms immediately before deployment.
8. Document service sleep, pause, expiry, and availability limitations honestly.
9. Keep source data and basemap attribution visible.
10. Purchase a custom domain or always-on service only when it improves a defined portfolio outcome.

## Official Sources Checked

- [PostgreSQL Licence](https://www.postgresql.org/about/licence/)
- [PostGIS](https://postgis.net/)
- [GeoPandas open-source status](https://geopandas.org/en/stable/about.html)
- [FastAPI and MIT licence](https://fastapi.tiangolo.com/)
- [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/)
- [PMTiles concepts](https://docs.protomaps.com/pmtiles/)
- [QGIS overview](https://qgis.org/project/overview/)
- [VSCodium and VS Code licensing distinction](https://vscodium.com/)
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)
- [Cloudflare Pages](https://pages.cloudflare.com/)
- [Render pricing](https://render.com/pricing)
- [Render free-tier limitations](https://render.com/docs/free)
- [Supabase pricing](https://supabase.com/pricing)
- [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/)

## Decision

Proceed with open-source application tools throughout the roadmap. Plan Project 3 as a static, no-cost web GIS first. Keep Project 2's API fully demonstrable locally, and treat public API/database hosting as an optional enhancement rather than a completion requirement.