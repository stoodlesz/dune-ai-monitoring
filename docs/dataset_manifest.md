# Dataset Manifest

The dataset manifest is the project record of where each image came from, how it is labelled, and whether its bytes can be verified later.

Use `data/metadata/example_manifest.csv` as the starting template.

## Required Columns

- `image_path`: local path to the raw image, processed image, or tile
- `source_name`: provider or dataset name, such as Sentinel-2 or OpenAerialMap
- `source_url`: source page, API endpoint, or catalogue URL
- `capture_date`: image capture date in `YYYY-MM-DD` format when known
- `location_name`: human-readable site name
- `latitude` and `longitude`: approximate scene or tile centre
- `sensor`: source sensor or platform
- `bands`: semicolon-separated band list, for example `B2;B3;B4;B8`
- `stage`: optional psammosere label
- `label_source`: how the label was produced, such as `manual_review`, `field_survey`, or `derived_from_landcover`
- `label_confidence`: value from `0.0` to `1.0`
- `sha256`: integrity digest for the referenced file
- `license`: source licence or access terms
- `notes`: short free-text context

## Stage Labels

Current stage labels are:

- `embryo_dune`
- `yellow_dune`
- `grey_dune`
- `mature_dune_grassland`
- `dune_scrub_or_woodland`

## Security Notes

The `sha256`, `source_url`, `label_source`, and `label_confidence` fields are deliberately part of the first dataset format. They make it possible to detect accidental file changes, track data provenance, and separate high-confidence training labels from experimental or weak labels.

## Adding A Local Image

After installing the project with `pip install -e .`, add a downloaded image to a manifest with:

```bash
dune-manifest-add \
  --manifest data/metadata/manifest.csv \
  --image-path data/raw/sentinel2/ainsdale_2026_05_01.tif \
  --source-name Sentinel-2 \
  --source-url https://dataspace.copernicus.eu/ \
  --capture-date 2026-05-01 \
  --location-name "Ainsdale Dunes" \
  --latitude 53.602 \
  --longitude -3.055 \
  --sensor MSI \
  --bands "B2;B3;B4;B8" \
  --stage yellow_dune \
  --label-source manual_review \
  --label-confidence 0.85 \
  --license "Copernicus terms" \
  --notes "First local Sentinel-2 test image"
```

The command computes the file SHA-256 automatically and writes it into the manifest row.

## Downloading From Planetary Computer

The project also includes `dune-pc-download`, which searches Microsoft Planetary Computer's STAC API for Sentinel-2 L2A imagery, picks the least-cloudy matching item, downloads one asset, computes its SHA-256 hash, and registers it in the manifest.

Example for an Ainsdale Dunes bounding box:

```bash
dune-pc-download \
  --bbox "-3.08,53.59,-3.03,53.62" \
  --date-range 2025-06-01/2025-06-30 \
  --asset visual \
  --max-cloud-cover 20 \
  --output data/raw/sentinel2/ainsdale_visual_2025_06.tif \
  --manifest data/metadata/manifest.csv \
  --location-name "Ainsdale Dunes" \
  --latitude 53.602 \
  --longitude -3.055 \
  --stage yellow_dune \
  --label-source manual_review \
  --label-confidence 0.7 \
  --notes "First Planetary Computer Sentinel-2 test image"
```

Use `--asset visual` for a true-colour image, or a band key such as `B02`, `B03`, `B04`, or `B08` when you want individual spectral bands for vegetation index work.
