# Model Card: Fetal Plane Classifier

## Model Details

-   **Name**: Fetal Plane Classifier v2.0
-   **Version**: 2.0.0
-   **Date**: 2026-01-02
-   **Type**: MobileNetV3-Small (Convolutional Neural Network)
-   **Parameters**: 1,524,006 (~1.5M)
-   **License**: Apache-2.0

## Intended Use

-   **Primary Use**: Research demonstration of standard plane classification in fetal ultrasound.
-   **Intended Users**: Machine learning researchers, medical imaging students.
-   **Out of Scope**: Clinical diagnosis, patient monitoring, commercial medical device use.

## Classes

| ID | Class Name | Description |
|----|------------|-------------|
| 0 | Abdominal | Fetal abdominal planes |
| 1 | Brain | Fetal brain planes |
| 2 | Cervix | Maternal cervix views |
| 3 | Femur | Fetal femur measurements |
| 4 | Other | Non-standard or ambiguous planes |
| 5 | Thorax | Fetal thorax views |

## Training Data

-   **Source**: FETAL_PLANES_DB (Zenodo)
-   **Train Set**: 10,005 images (1,433 patients)
-   **Validation Set**: 2,395 images (359 patients)
-   **Split Method**: Patient-level stratified split (no data leakage)
-   **Preprocessing**: Resized to 224x224, Normalized mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Epochs | 2 |
| Batch Size | 64 |
| Optimizer | SGD (momentum=0.9) |
| Learning Rate | 0.001 |
| Framework | PyTorch 2.x |

## Metrics (Placeholder - Update after training)

| Metric | Value |
|--------|-------|
| Accuracy | TBD |
| F1 Score (Macro) | TBD |
| F1 Score (Weighted) | TBD |

## Ethical Considerations

-   **Bias**: Dataset may be biased towards specific ultrasound machines or patient populations.
-   **Safety**: Model may hallucinate structures in noise. Uncertainty estimation is provided to mitigate this but is not foolproof.
-   **Privacy**: No PHI should be processed. All inference is stateless.
