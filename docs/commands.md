# Commands

Common local commands for working with the project.

## Setup

Run these from the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

If the virtual environment already exists, start here instead:

```bash
source venv/bin/activate
python -m pip install -e .
```

## Run Tests

```bash
python -m unittest discover -s tests
```

Expected output:

```text
OK
```

## Download Dune du Pilat Preview

This downloads a small Sentinel-2 preview image from Microsoft Planetary Computer, adds a manifest row, and writes a human-readable report.

```bash
dune-pc-download \
  --bbox "-1.26,44.55,-1.16,44.63" \
  --date-range 2025-06-01/2025-09-30 \
  --asset rendered_preview \
  --max-cloud-cover 30 \
  --output data/raw/sentinel2/dune_pilat_rendered_preview_2025_07.png \
  --manifest data/metadata/dune_pilat_manifest.csv \
  --report data/metadata/dune_pilat_report.md \
  --location-name "Dune du Pilat" \
  --latitude 44.589 \
  --longitude -1.214 \
  --stage yellow_dune \
  --label-source manual_review \
  --label-confidence 0.6 \
  --notes "Small preview image downloaded from Planetary Computer for visual inspection"
```

## View Outputs

Open the downloaded preview image:

```bash
open data/raw/sentinel2/dune_pilat_rendered_preview_2025_07.png
```

Read the image report:

```bash
cat data/metadata/dune_pilat_report.md
```

Read the manifest row:

```bash
cat data/metadata/dune_pilat_manifest.csv
```

## Commit Metadata

Raw imagery under `data/raw/` should stay local and should not be committed. Commit metadata and reports:

```bash
git add data/metadata/dune_pilat_manifest.csv data/metadata/dune_pilat_report.md
git commit -m "Add Dune du Pilat dataset metadata"
git push origin main
```

