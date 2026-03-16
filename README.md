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

dune-ai-monitoring/

README.md  
requirements.txt  

configs/  
Configuration files for model training and experiments.

data/  
  raw/  
  Original datasets (not stored in Git).

  processed/  
  Cleaned datasets prepared for training.

  metadata/  
  Dataset descriptions and labels.

  README.md  
  Instructions for downloading datasets.

notebooks/  
Exploratory notebooks for data analysis and visualisation.

src/

  preprocessing/  
  Image preparation and dataset pipelines.

  models/  
  Neural network architectures.

  training/  
  Training loops and optimisation scripts.

  evaluation/  
  Model evaluation and metrics.

  utils/  
  Shared utilities.

experiments/

  psammosere-classifier/  
  Models classifying dune succession stages.

  temporal-analysis/  
  Time-series change detection.

docs/  
Research notes and documentation.

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

Environmental AI research project focused on ecological monitoring and secure machine learning.
