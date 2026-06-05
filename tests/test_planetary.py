import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dune_ai_monitoring.datasets.planetary import (
    download_asset,
    item_cloud_cover,
    item_datetime,
    search_sentinel2_items,
    select_least_cloudy,
    signed_asset_href,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        if isinstance(self.payload, bytes):
            return self.payload
        return json.dumps(self.payload).encode("utf-8")


class PlanetaryComputerTests(unittest.TestCase):
    def test_search_sentinel2_items_posts_expected_query(self):
        payload = {"features": [{"id": "item-1"}]}

        with patch("dune_ai_monitoring.datasets.planetary.request.urlopen", return_value=FakeResponse(payload)) as urlopen:
            items = search_sentinel2_items(
                (-3.08, 53.59, -3.03, 53.62),
                "2025-06-01/2025-06-30",
                max_cloud_cover=15,
                limit=3,
            )

        request_obj = urlopen.call_args.args[0]
        body = json.loads(request_obj.data.decode("utf-8"))
        self.assertEqual(items, [{"id": "item-1"}])
        self.assertEqual(body["collections"], ["sentinel-2-l2a"])
        self.assertEqual(body["query"], {"eo:cloud_cover": {"lt": 15}})
        self.assertEqual(body["limit"], 3)

    def test_select_least_cloudy(self):
        item = select_least_cloudy(
            [
                {"id": "cloudy", "properties": {"eo:cloud_cover": 30}},
                {"id": "clear", "properties": {"eo:cloud_cover": 2}},
            ]
        )

        self.assertEqual(item["id"], "clear")

    def test_signed_asset_href_appends_sas_token(self):
        item = {
            "assets": {
                "visual": {
                    "href": "https://example.blob.core.windows.net/sentinel/visual.tif",
                }
            }
        }

        with patch(
            "dune_ai_monitoring.datasets.planetary.request.urlopen",
            return_value=FakeResponse({"token": "sig=abc"}),
        ):
            href = signed_asset_href(item, "visual")

        self.assertEqual(href, "https://example.blob.core.windows.net/sentinel/visual.tif?sig=abc")

    def test_download_asset_writes_file(self):
        response = io.BytesIO(b"satellite bytes")
        response.__enter__ = lambda: response
        response.__exit__ = lambda exc_type, exc, traceback: False

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "visual.tif"
            with patch("dune_ai_monitoring.datasets.planetary.request.urlopen", return_value=response):
                downloaded = download_asset("https://example.com/visual.tif", path)

            data = path.read_bytes()

        self.assertEqual(downloaded, path)
        self.assertEqual(data, b"satellite bytes")

    def test_item_metadata_helpers(self):
        item = {"properties": {"datetime": "2025-06-12T11:20:00Z", "eo:cloud_cover": 4.5}}

        self.assertEqual(item_datetime(item), "2025-06-12")
        self.assertEqual(item_cloud_cover(item), 4.5)


if __name__ == "__main__":
    unittest.main()

