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

