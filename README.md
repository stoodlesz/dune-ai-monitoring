# Dune AI Monitoring

## Project Overview

This repository contains experiments and research code exploring how machine learning and computer vision can be used to analyse coastal dune ecosystems (psammoseres). The long-term goal is to build models capable of detecting dune ecosystem stages, identifying degradation, and predicting ecological change from imagery.

The project combines:

- remote sensing and environmental imagery
- machine learning and computer vision
- secure AI pipelines and adversarial robustness

Initial focus is on psammosere ecosystems (sand dune ecological succession). Future expansions may include wetlands, reforestation, and environmental protection modelling.

---

## Research Goals

1. Detect psammosere stages from aerial or satellite imagery.
2. Track ecological change across time.
3. Predict dune degradation or restoration.
4. Experiment with AI-assisted ecological restoration scenarios.
5. Build secure ML pipelines resistant to data poisoning or adversarial manipulation.

---

## Repository Structure

```text
dune-ai-monitoring/
├── README.md
├── ROADMAP.md
├── SECURITY.md
├── pyproject.toml
├── requirements.txt
├── data/
│   ├── README.md
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── docs/
├── journal/
├── notebooks/
├── research/
├── src/
│   └── dune_ai_monitoring/
└── tests/
```

## File Breakdown

Core project files:

- `README.md`: project overview, structure, and setup notes.
- `ROADMAP.md`: research and development phases.
- `SECURITY.md`: secure ML considerations for environmental monitoring.
- `pyproject.toml`: Python package configuration and CLI entry points.
- `requirements.txt`: runtime dependencies.

Source code:

- `src/dune_ai_monitoring/datasets/manifest.py`: dataset manifest records, CSV loading/writing, validation, and SHA-256 hashing.
- `src/dune_ai_monitoring/datasets/cli.py`: `dune-manifest-add` command for registering a local image in a manifest.
- `src/dune_ai_monitoring/datasets/planetary.py`: Microsoft Planetary Computer STAC search, asset signing, and download helpers.
- `src/dune_ai_monitoring/datasets/planetary_cli.py`: `dune-pc-download` command for downloading Sentinel-2 imagery and writing manifest/report outputs.
- `src/dune_ai_monitoring/preprocessing/image_tiles.py`: image tiling helpers for model-ready patches.
- `src/dune_ai_monitoring/preprocessing/indices.py`: NDVI, NDWI, and normalized-difference calculations.
- `src/dune_ai_monitoring/preprocessing/metadata.py`: psammosere stage labels and label validation.

Data organisation:

- `data/raw/`: local raw imagery downloads. This folder is intentionally not used for committed satellite image files.
- `data/processed/`: future cleaned, tiled, or model-ready outputs.
- `data/metadata/example_manifest.csv`: blank/example manifest format.
- `data/metadata/dune_pilat_manifest.csv`: first Dune du Pilat Sentinel-2 metadata record.
- `data/metadata/dune_pilat_report.md`: readable report for the Dune du Pilat image.
- `data/README.md`: dataset source and storage guidance.

Documentation and notes:

- `docs/commands.md`: common setup, test, download, and viewing commands.
- `docs/dataset_manifest.md`: explanation of the manifest format and downloader commands.
- `journal/2026-06-05.md`: project diary entry tracking early progress.
- `research/literature.md`: reading list and background sources.

Exploration and experiments:

- `01_dune_imagery_exploration.ipynb`: initial exploration notebook.
- `notebooks/`: notebook workspace for future analysis.
- `experiments/`: placeholder for future modelling experiments.

Tests:

- `tests/test_manifest.py`: manifest record and validation tests.
- `tests/test_manifest_cli.py`: local manifest command tests.
- `tests/test_planetary.py`: Planetary Computer STAC helper tests.
- `tests/test_planetary_cli.py`: Sentinel-2 downloader command tests.
- `tests/test_preprocessing.py`: image tiling, spectral index, and label validation tests.

---

## Git Branching Workflow

The repository uses a simple branching model.

Main branches

main  
Stable versions of the project.

develop  
Active development branch.

Feature branches

All new work should branch from develop.

Examples

feature/data-preprocessing  
feature/psammosere-classifier  
feature/temporal-change-detection  
feature/secure-ml-pipeline  

Experimental work

experiment/gan-augmentation  
experiment/adversarial-test  

---

## Branching Instructions

Update develop

git fetch origin  
git checkout develop  
git pull origin develop  

Create a new feature branch

git checkout -b feature/your-feature-name

Example

git checkout -b feature/psammosere-classifier

Push the branch

git push -u origin feature/psammosere-classifier

Merge workflow

1. Work on the feature branch.
2. Commit locally.
3. Push the branch.
4. Open a pull request to develop.
5. Merge into develop after review.
6. Periodically merge develop into main when stable.

---

## Data Handling

Large environmental datasets should not be stored directly in Git.

Options

- cloud storage
- Git LFS
- dataset download scripts

The file data/README.md should describe:

- dataset sources
- download instructions
- preprocessing steps

---

## Environment Setup

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt

For local development, install the package in editable mode:

pip install -e .

Run the current test suite:

python -m unittest discover -s tests

---

## First Code Modules

The `src/dune_ai_monitoring/` package contains the first reusable project code:

- dataset manifest helpers for provenance and integrity metadata
- image tiling helpers for creating model-ready patches
- NDVI and NDWI spectral index calculations
- metadata validation for psammosere stage labels

The first dataset manifest template lives at `data/metadata/example_manifest.csv`, with notes in `docs/dataset_manifest.md`.

After installing the project, use `dune-manifest-add` to add a downloaded image to `data/metadata/manifest.csv` and compute its SHA-256 provenance hash automatically.

Use `dune-pc-download` to search Microsoft Planetary Computer for Sentinel-2 L2A imagery, download a selected asset, and register it in the manifest.

Common local setup, test, download, and viewing commands are listed in `docs/commands.md`.

---

## Planned Experiments

1. Collect labelled dune imagery datasets.
2. Train a psammosere stage classifier.
3. Analyse satellite and aerial imagery.
4. Detect ecosystem change across time.
5. Evaluate adversarial robustness of environmental ML models.

---

## Future Directions

Possible research expansions include:

- wetland monitoring
- coastal flooding prediction
- reforestation modelling
- habitat restoration planning

---

## Author

Stella Williams  
stella.williams286@gmail.com

Environmental AI research project focused on ecological monitoring and secure machine learning.
