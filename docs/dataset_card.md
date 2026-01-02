# Dataset Card: FETAL_PLANES_DB

## Dataset Details

-   **Name**: FETAL_PLANES_DB
-   **Version**: 1.0
-   **Source**: Zenodo (https://zenodo.org/record/3904280)
-   **License**: CC BY 4.0
-   **Size**: 12,400 images (2.1 GB)

## Description

A large-scale dataset of 2D fetal ultrasound images collected from multiple clinical centers, annotated by expert sonographers for standard anatomical plane classification.

## Classes

| ID | Class Name | Count | Description |
|----|------------|-------|-------------|
| 0 | Abdominal | 711 | Fetal abdominal planes |
| 1 | Brain | 3,092 | Fetal brain planes (aggregated) |
| 2 | Cervix | 1,626 | Maternal cervix views |
| 3 | Femur | 1,040 | Fetal femur measurements |
| 4 | Other | 4,213 | Non-standard or ambiguous planes |
| 5 | Thorax | 1,718 | Fetal thorax views |

## Splits

| Split | Images | Patients |
|-------|--------|----------|
| Train | 10,005 | 1,433 |
| Validation | 2,395 | 359 |

**Split Method**: Patient-level stratified split to prevent data leakage.

## Collection Process

-   **Modality**: 2D B-mode Ultrasound
-   **Equipment**: Various clinical ultrasound machines
-   **Annotators**: Expert sonographers
-   **Quality Control**: Multi-reviewer consensus

## Uses

-   **Supported Tasks**: Image Classification, Transfer Learning
-   **Exclusions**: Biometry measurement (not annotated for segmentation)

## Download

Run the data preparation script:

```bash
py backend/scripts/prepare_data_robust.py
```

This script downloads from Zenodo, extracts, and organizes images with patient-level train/val split.
