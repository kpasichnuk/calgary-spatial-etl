from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import geopandas as gpd
from shapely.geometry import Point

from src.qa import inspect_layer


class InspectLayerTests(unittest.TestCase):
    def write_layer(self, path: Path, ids: list[int | None]) -> None:
        gdf = gpd.GeoDataFrame(
            {"feature_id": ids, "name": [f"site-{index}" for index in range(len(ids))]},
            geometry=[Point(index, index) for index in range(len(ids))],
            crs="EPSG:3347",
        )
        gdf.to_file(path, driver="GeoJSON")

    def test_valid_layer_passes(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "sites.geojson"
            self.write_layer(path, [1, 2])

            result = inspect_layer(
                "sites", path, ["feature_id", "name"], "feature_id"
            )

        self.assertTrue(result.passed)
        self.assertEqual(result.row_count, 2)
        self.assertEqual(result.duplicate_id_count, 0)

    def test_duplicate_id_fails(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "sites.geojson"
            self.write_layer(path, [1, 1])

            result = inspect_layer(
                "sites", path, ["feature_id", "name"], "feature_id"
            )

        self.assertFalse(result.passed)
        self.assertEqual(result.duplicate_id_count, 1)

    def test_missing_file_returns_actionable_failure(self) -> None:
        result = inspect_layer(
            "sites",
            "does-not-exist.geojson",
            ["feature_id", "name"],
            "feature_id",
        )

        self.assertFalse(result.passed)
        self.assertIn("Missing processed file", result.error)


if __name__ == "__main__":
    unittest.main()
