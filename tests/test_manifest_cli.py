import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from dune_ai_monitoring.datasets import load_manifest
from dune_ai_monitoring.datasets.cli import main


class DatasetManifestCliTests(unittest.TestCase):
    def test_cli_adds_record_with_computed_sha256(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            image_path = tmp_path / "sample.tif"
            manifest_path = tmp_path / "manifest.csv"
            image_path.write_bytes(b"pretend satellite bytes")

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = main(
                    [
                        "--manifest",
                        str(manifest_path),
                        "--image-path",
                        str(image_path),
                        "--source-name",
                        "Sentinel-2",
                        "--source-url",
                        "https://dataspace.copernicus.eu/",
                        "--capture-date",
                        "2026-05-01",
                        "--location-name",
                        "Ainsdale Dunes",
                        "--latitude",
                        "53.602",
                        "--longitude",
                        "-3.055",
                        "--sensor",
                        "MSI",
                        "--bands",
                        "B2;B3;B4;B8",
                        "--stage",
                        "yellow_dune",
                        "--label-source",
                        "manual_review",
                        "--label-confidence",
                        "0.85",
                        "--license",
                        "Copernicus terms",
                        "--notes",
                        "Test record",
                    ]
                )

            records = load_manifest(manifest_path)

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].stage, "yellow_dune")
        self.assertEqual(records[0].bands, ("B2", "B3", "B4", "B8"))
        self.assertEqual(records[0].sha256, "1dd869e705a44a5924b8b4f621dfb9f21b89462b1b66ac2d782c659a927ac62e")

    def test_cli_rejects_missing_file_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_path = Path(tmpdir) / "missing.tif"
            manifest_path = Path(tmpdir) / "manifest.csv"

            with self.assertRaises(SystemExit):
                main(
                    [
                        "--manifest",
                        str(manifest_path),
                        "--image-path",
                        str(missing_path),
                        "--source-name",
                        "Sentinel-2",
                        "--source-url",
                        "https://dataspace.copernicus.eu/",
                    ]
                )


if __name__ == "__main__":
    unittest.main()
