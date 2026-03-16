# Dataset Instructions

This project uses environmental imagery to analyse sand dune ecosystems (psammoseres).  
Large datasets are **not stored in this repository**. Instead, users should download them from the original providers and place them in the correct folders.

Repository data structure:

data/

raw/  
Original downloaded datasets.

processed/  
Cleaned and prepared datasets used for training.

metadata/  
Labels, dataset descriptions, and annotation files.

---

# Recommended Data Sources

## Copernicus Sentinel-2

High resolution multispectral satellite imagery useful for monitoring vegetation change in dune ecosystems.

Provider  
Copernicus Open Access Hub

Access

https://scihub.copernicus.eu/

Suggested bands for vegetation and dune analysis:

- B2 (Blue)
- B3 (Green)
- B4 (Red)
- B8 (Near Infrared)

Possible indices to compute later:

- NDVI (vegetation health)
- NDWI (water detection)

Example placement:

data/raw/sentinel2/

---

## ESA WorldCover

Global land cover dataset useful for baseline classification.

Provider  
European Space Agency

Access

https://worldcover2020.esa.int/

Example placement:

data/raw/worldcover/

---

## OpenAerialMap

Drone and aerial imagery datasets that may include coastal environments.

Provider  
OpenAerialMap

Access

https://openaerialmap.org/

Example placement:

data/raw/aerial/

---

# Manual Field or Drone Data (Optional)

If custom imagery is collected using drones or field surveys, place it here:

data/raw/drone/

Include metadata such as:

- location
- date
- resolution
- sensor type

---

# Preprocessing Pipeline

Raw imagery should be processed before training.

Typical steps include:

1. Image cropping or tiling
2. Resolution normalisation
3. Vegetation index calculation
4. Label generation for psammosere stages
5. Train/test dataset split

Processed datasets should be stored here:

data/processed/

---

# Example Folder Layout

data/

raw/

sentinel2/  
aerial/  
drone/

processed/

train/  
test/  
validation/

metadata/

labels.csv  
dataset_description.md

---

# Notes

Large datasets should be stored using:

- external storage
- cloud storage
- dataset download scripts

Avoid committing large imagery files to Git.
