# Research Roadmap

This document outlines the development stages for the Dune AI Monitoring project.

The goal is to build machine learning systems capable of analysing sand dune ecosystems (psammoseres) using satellite and aerial imagery, while ensuring model robustness and security.

---

## Phase 1 — Project Foundations

Objectives

- Establish repository structure
- Identify reliable environmental datasets
- Build preprocessing pipelines for satellite imagery
- Create labelled datasets for dune succession stages

Tasks

- Download Sentinel-2 imagery from Copernicus
- Collect aerial or drone imagery of coastal dunes
- Define psammosere classification categories
- Build dataset metadata and labelling structure

Expected output

- Clean dataset ready for model training
- Reproducible preprocessing pipeline

---

## Phase 2 — Psammosere Classification

Objectives

Train models to classify stages of dune ecological succession.

Typical stages may include:

- Embryo dunes
- Yellow dunes
- Grey dunes
- Mature dune grassland
- Dune scrub or woodland

Tasks

- Train baseline CNN classifier
- Evaluate model performance
- Visualise classification outputs
- Analyse misclassifications

Expected output

- First working ecological classification model

---

## Phase 3 — Temporal Ecosystem Change Detection

Objectives

Track ecosystem changes across time using satellite imagery.

Tasks

- Build time-series datasets
- Train models for change detection
- Identify dune erosion or vegetation loss

Potential outputs

- Detection of dune degradation
- Identification of vegetation expansion

---

## Phase 4 — Predictive Environmental Modelling

Objectives

Predict future ecosystem development.

Possible applications

- restoration planning
- dune stabilisation modelling
- vegetation spread prediction

Tasks

- train predictive models
- simulate ecological interventions
- evaluate restoration scenarios

---

## Phase 5 — Environmental AI Security

Objectives

Evaluate the robustness and security of environmental machine learning systems.

Research questions may include:

- Can environmental ML models be manipulated through adversarial imagery?
- Could satellite monitoring systems be fooled by synthetic images?
- How resilient are ecological models to dataset poisoning?

Tasks

- adversarial testing
- model robustness evaluation
- secure ML pipeline development

---

## Long-Term Research Extensions

Possible expansions of the project:

- wetland monitoring
- floodplain ecosystem analysis
- forest restoration monitoring
- biodiversity tracking

The long-term aim is to develop secure AI tools capable of assisting environmental protection and ecosystem management.
