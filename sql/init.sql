SELECT 'CREATE DATABASE calgary_gis'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'calgary_gis')\gexec

\connect calgary_gis
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
