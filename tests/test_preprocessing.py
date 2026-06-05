import unittest

import numpy as np

from dune_ai_monitoring.preprocessing import ImageRecord, iter_windows, ndvi, tile_array, validate_stage


class ImageTilingTests(unittest.TestCase):
    def test_iter_windows_drops_partial_edges_by_default(self):
        windows = list(iter_windows(image_width=5, image_height=5, tile_size=2))

        self.assertEqual(len(windows), 4)
        self.assertEqual((windows[0].x, windows[0].y, windows[0].width, windows[0].height), (0, 0, 2, 2))
        self.assertEqual((windows[-1].x, windows[-1].y), (2, 2))

    def test_iter_windows_can_keep_partial_edges(self):
        windows = list(iter_windows(5, 5, 3, drop_partial=False))

        self.assertEqual(len(windows), 4)
        self.assertEqual((windows[-1].x, windows[-1].y, windows[-1].width, windows[-1].height), (3, 3, 2, 2))

    def test_tile_array_preserves_channel_dimension(self):
        image = np.arange(4 * 4 * 3).reshape(4, 4, 3)

        tiles = tile_array(image, tile_size=2)

        self.assertEqual(len(tiles), 4)
        self.assertEqual(tiles[0].shape, (2, 2, 3))


class SpectralIndexTests(unittest.TestCase):
    def test_ndvi_matches_expected_formula(self):
        nir = np.array([[0.8, 0.4]], dtype=np.float32)
        red = np.array([[0.2, 0.4]], dtype=np.float32)

        result = ndvi(nir, red)

        np.testing.assert_allclose(result, np.array([[0.6, 0.0]], dtype=np.float32), atol=1e-6)


class MetadataTests(unittest.TestCase):
    def test_validate_stage_normalizes_human_label(self):
        self.assertEqual(validate_stage("Yellow Dune"), "yellow_dune")

    def test_image_record_rejects_unknown_stage(self):
        with self.assertRaises(ValueError):
            ImageRecord("data/raw/example.tif", "unknown")

    def test_image_record_stores_normalized_stage(self):
        record = ImageRecord("data/raw/example.tif", "Grey Dune")

        self.assertEqual(record.stage, "grey_dune")


if __name__ == "__main__":
    unittest.main()
