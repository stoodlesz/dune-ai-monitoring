import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dune_ai_monitoring.datasets import load_manifest
from dune_ai_monitoring.datasets.planetary_cli import main


class PlanetaryComputerCliTests(unittest.TestCase):
    def test_cli_downloads_asset_and_registers_manifest_row(self):
        fake_item = {
            "id": "S2_TEST_ITEM",
            "properties": {"datetime": "2025-06-12T11:20:00Z", "eo:cloud_cover": 3.2},
            "assets": {"visual": {"href": "https://example.com/visual.tif"}},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            output = tmp_path / "visual.tif"
            manifest = tmp_path / "manifest.csv"

            with (
                patch("dune_ai_monitoring.datasets.planetary_cli.search_sentinel2_items", return_value=[fake_item]),
                patch("dune_ai_monitoring.datasets.planetary_cli.signed_asset_href", return_value="https://example.com/signed.tif"),
                patch("dune_ai_monitoring.datasets.planetary_cli.download_asset") as download_asset,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                def fake_download(href, destination):
                    path = Path(destination)
                    path.write_bytes(b"visual bytes")
                    return path

                download_asset.side_effect = fake_download
                exit_code = main(
                    [
                        "--bbox",
                        "-3.08,53.59,-3.03,53.62",
                        "--date-range",
                        "2025-06-01/2025-06-30",
                        "--output",
                        str(output),
                        "--manifest",
                        str(manifest),
                        "--location-name",
                        "Ainsdale Dunes",
                        "--latitude",
                        "53.602",
                        "--longitude",
                        "-3.055",
                        "--stage",
                        "yellow_dune",
                        "--label-source",
                        "manual_review",
                        "--label-confidence",
                        "0.7",
                    ]
                )

            records = load_manifest(manifest)

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].source_name, "Microsoft Planetary Computer Sentinel-2 L2A")
        self.assertEqual(records[0].capture_date.isoformat(), "2025-06-12")
        self.assertEqual(records[0].bands, ("visual",))
        self.assertEqual(records[0].stage, "yellow_dune")
        self.assertIn("S2_TEST_ITEM", records[0].notes)


if __name__ == "__main__":
    unittest.main()
