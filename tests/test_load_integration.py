from pathlib import Path
from tempfile import TemporaryDirectory
import os
import unittest

import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine, inspect, text

from src.load import database_url_from_environment, load_layer


@unittest.skipUnless(
    os.getenv("RUN_POSTGIS_TESTS") == "1",
    "Set RUN_POSTGIS_TESTS=1 to run PostGIS integration tests.",
)
class LoadIntegrationTests(unittest.TestCase):
    schema = "etl_test"

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine(database_url_from_environment(), pool_pre_ping=True)
        with cls.engine.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{cls.schema}"'))

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS "{cls.schema}" CASCADE'))
        cls.engine.dispose()

    def make_layer(self, path: Path) -> None:
        gdf = gpd.GeoDataFrame(
            {"feature_id": [1, 2], "name": ["A", "B"]},
            geometry=[Point(0, 0), Point(1, 1)],
            crs="EPSG:3347",
        )
        gdf.to_file(path, driver="GeoJSON")

    def test_repeat_load_replaces_without_duplicates(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "sites.geojson"
            self.make_layer(path)
            with self.engine.begin() as connection:
                first = load_layer(connection, "sites", path, self.schema)
            with self.engine.begin() as connection:
                second = load_layer(connection, "sites", path, self.schema)

        self.assertEqual(first.loaded_rows, 2)
        self.assertEqual(second.loaded_rows, 2)

    def test_failed_transaction_rolls_back_table_creation(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "rollback_sites.geojson"
            self.make_layer(path)
            with self.assertRaises(RuntimeError):
                with self.engine.begin() as connection:
                    load_layer(connection, "rollback_sites", path, self.schema)
                    raise RuntimeError("force rollback")

        self.assertFalse(
            inspect(self.engine).has_table("rollback_sites", schema=self.schema)
        )


if __name__ == "__main__":
    unittest.main()
