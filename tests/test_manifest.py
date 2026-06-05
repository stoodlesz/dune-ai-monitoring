from datetime import date
import tempfile
import unittest
from pathlib import Path

from dune_ai_monitoring.datasets import DatasetRecord, compute_sha256, load_manifest, validate_manifest, write_manifest


class DatasetManifestTests(unittest.TestCase):
    def test_record_normalizes_stage_and_bands(self):
        record = DatasetRecord(
            image_path="data/raw/sample.tif",
            source_name="Sentinel-2",
            source_url="https://dataspace.copernicus.eu/",
            capture_date=date(2026, 5, 1),
            bands=(" B4 ", "B8"),
            stage="Grey Dune",
            label_source="manual_review",
            label_confidence=0.8,
        )

        self.assertEqual(record.stage, "grey_dune")
        self.assertEqual(record.bands, ("B4", "B8"))

    def test_record_rejects_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            DatasetRecord(
                image_path="data/raw/sample.tif",
                source_name="Sentinel-2",
                source_url="https://dataspace.copernicus.eu/",
                latitude=120,
            )

    def test_manifest_round_trip(self):
        record = DatasetRecord(
            image_path="data/raw/sample.tif",
            source_name="Sentinel-2",
            source_url="https://dataspace.copernicus.eu/",
            capture_date=date(2026, 5, 1),
            location_name="Ainsdale Dunes",
            latitude=53.602,
            longitude=-3.055,
            sensor="MSI",
            bands=("B2", "B3", "B4", "B8"),
            stage="yellow_dune",
            label_source="manual_review",
            label_confidence=0.9,
            license="Copernicus terms",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.csv"
            write_manifest(path, [record])

            loaded = load_manifest(path)

        self.assertEqual(loaded, [record])

    def test_validate_manifest_reports_provenance_gaps(self):
        record = DatasetRecord(
            image_path="data/raw/sample.tif",
            source_name="Sentinel-2",
            source_url="https://dataspace.copernicus.eu/",
            stage="yellow_dune",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.csv"
            write_manifest(path, [record])

            warnings = validate_manifest(path)

        self.assertIn("row 2: missing sha256 integrity digest", warnings)
        self.assertIn("row 2: labelled record is missing label_source", warnings)
        self.assertIn("row 2: labelled record is missing label_confidence", warnings)
        self.assertIn("row 2: missing band metadata", warnings)

    def test_compute_sha256(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.txt"
            path.write_text("dune data\n", encoding="utf-8")

            digest = compute_sha256(path)

        self.assertEqual(digest, "3a426b9d7dae293cb5f59fed49bf457a646c6e537064d561bbc8152d49965072")


if __name__ == "__main__":
    unittest.main()
