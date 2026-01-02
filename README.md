# Fetal Plane Explorer

**A research-only demonstration of fetal ultrasound standard plane classification with uncertainty estimation and explainability.**

![Architecture Diagram](https://via.placeholder.com/800x400?text=Architecture+Diagram+Placeholder)

> [!IMPORTANT]
> **DISCLAIMER: NOT A MEDICAL DEVICE**
>
> This software is for **research and demonstration purposes only**. It is not intended for clinical use, diagnosis, treatment, or patient monitoring. The predictions, uncertainty estimates, and explanations provided by this system have not been validated for medical decision-making. No Protected Health Information (PHI) should be processed by this system in its default configuration.

## Overview

Fetal Plane Explorer is an open-source web application designed to showcase modern techniques in medical image analysis, specifically for fetal ultrasound. It demonstrates:

1.  **Standard Plane Classification**: Identifying 6 anatomical categories (Abdominal, Brain, Cervix, Femur, Thorax, Other) from 2D ultrasound images using a MobileNetV3-Small (~1.5M parameters) model.
2.  **Uncertainty Quantification**: Estimating the confidence of predictions using temperature scaling to detect out-of-distribution or ambiguous inputs.
3.  **Explainable AI (XAI)**: Visualizing the regions of interest used by the model for prediction via simulated Grad-CAM overlays.

## Features

-   **Interactive Web UI**: Built with Material Design 3, offering a clean, accessible, and responsive experience with light/dark themes.
-   **Real-time Inference**: Fast classification with uncertainty metrics.
-   **Visual Explanations**: Toggleable heatmaps to understand model focus.
-   **Privacy-First**: No data persistence by default; images are processed in-memory.
-   **Reproducible**: Dockerized deployment and pinned dependencies.

## Quickstart

### Prerequisities

-   Docker and Docker Compose
-   OR Python 3.12+ and Node.js 20+

### Using Docker (Recommended)

To start the full stack (backend + frontend):

```bash
docker-compose -f infra/docker-compose.yml up --build
```

Access the application at `http://localhost:3000`.
Access the API docs at `http://localhost:8000/docs`.

### Local Development

**Backend:**

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## API Usage

You can interact with the API directly:

```bash
curl -X POST "http://localhost:8000/v1/predict" \
  -F "file=@/path/to/ultrasound_image.png"
```

Response:

```json
{
  "prediction": {
    "label": "Brain",
    "class_id": 1,
    "confidence": 0.92
  },
  "uncertainty": {
    "entropy": 0.15,
    "calibrated_confidence": 0.89
  },
  "explanation": {
    "heatmap_base64": "..."
  }
}
```

## Architecture

The system follows a standard client-server architecture:

1.  **Frontend**: Vite + TypeScript app using Material Web components.
2.  **Backend Service**: FastAPI handling request validation, preprocessing, and orchestration.
3.  **Inference Engine**: ONNX Runtime (CPU default) for model execution.
4.  **XAI Module**: Custom Grad-CAM implementation for explanation generation.

See [docs/architecture.md](docs/architecture.md) for details.

## Reproducibility

We prioritize reproducibility through:
-   Deterministic training and inference modes.
-   Pinned versions in `pyproject.toml` and `package-lock.json`.
-   Publicly available model weights (see Model Card).

## Limitations

-   **Domain Shift**: Models trained on specific datasets (e.g., US-13) may not generalize to machines from other vendors without fine-tuning.
-   **Performance**: CPU inference is optimized for accessibility, but high-throughput scenarios may require GPU acceleration.
-   **Ambiguity**: Fetal ultrasound images are inherently noisy; uncertainty estimates are crucial but not infallible.

## Citation

If you use this repository in your research, please cite:

```bibtex
@misc{fetal_plane_explorer,
  author = {Laitinen, Olaf},
  title = {Fetal Plane Explorer: Standard Plane Classification with Uncertainty and XAI},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/olaflaitinen/fetal-plane-explorer}}
}
```
