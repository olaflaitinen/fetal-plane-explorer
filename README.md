# Fetal Plane Explorer

<div align="center">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/olaflaitinen/fetal-plane-explorer/ci.yml?logo=github)
![GitHub license](https://img.shields.io/github/license/olaflaitinen/fetal-plane-explorer?logo=opensourceinitiative)
![Last Updated](https://img.shields.io/badge/last%20updated-01%20Jan%202026-brightgreen?logo=github)
![Python Version](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![Node Version](https://img.shields.io/badge/node-20%2B-green?logo=nodedotjs&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?logo=typescript&logoColor=white)
![ONNX Runtime](https://img.shields.io/badge/ONNX%20Runtime-%23000000.svg?logo=onnx&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![GitHub issues](https://img.shields.io/github/issues/olaflaitinen/fetal-plane-explorer?logo=github)
![GitHub stars](https://img.shields.io/github/stars/olaflaitinen/fetal-plane-explorer?logo=github)
![GitHub forks](https://img.shields.io/github/forks/olaflaitinen/fetal-plane-explorer?logo=github)

**A research-only demonstration of fetal ultrasound standard plane classification with uncertainty estimation and explainability.**

[Request Feature](https://github.com/olaflaitinen/fetal-plane-explorer/issues) · [Report Bug](https://github.com/olaflaitinen/fetal-plane-explorer/issues)

</div>

---

## Overview

**Fetal Plane Explorer** is an open-source web application designed to showcase modern techniques in medical image analysis, specifically for fetal ultrasound. It demonstrates:

1.  **Standard Plane Classification**: Identifying the 6 standard anatomical planes (Abdominal, Brain, Cervix, Femur, Other, Thorax) from 2D ultrasound images.
2.  **Uncertainty Quantification**: Estimating the confidence of predictions using Monte Carlo Dropout and temperature scaling to detect out-of-distribution or ambiguous inputs.
3.  **Explainable AI (XAI)**: Visualizing the regions of interest used by the model for prediction via Grad-CAM overlays.

> [!IMPORTANT]
> **DISCLAIMER: NOT A MEDICAL DEVICE**
>
> This software is for **research and demonstration purposes only**. It is not intended for clinical use, diagnosis, treatment, or patient monitoring. The predictions, uncertainty estimates, and explanations provided by this system have not been validated for medical decision-making. No Protected Health Information (PHI) should be processed by this system in its default configuration.

## Features

-   **Interactive Web UI**: Built with **Material Design 3**, offering a clean, accessible, and responsive experience with light/dark themes.
-   **Real-time Inference**: Fast classification with uncertainty metrics using **ONNX Runtime**.
-   **Visual Explanations**: Toggleable heatmaps to understand model focus.
-   **Privacy-First**: No data persistence by default; images are processed in-memory.
-   **Reproducible**: Dockerized deployment and pinned dependencies.

## Architecture

The system follows a standard client-server architecture:

1.  **Frontend**: Vite + TypeScript app using Material Web components.
2.  **Backend Service**: FastAPI handling request validation, preprocessing, and orchestration.
3.  **Inference Engine**: ONNX Runtime (CPU default) for model execution (MobileNetV3-Small).
4.  **XAI Module**: Custom Grad-CAM implementation for explanation generation.

See [docs/architecture.md](docs/architecture.md) for details.

## Quickstart

### Prerequisities

-   **Docker** and **Docker Compose**
-   OR Python 3.12+ and Node.js 20+

### Using Docker (Recommended)

To start the full stack (backend + frontend):

```bash
docker-compose -f infra/docker-compose.yml up --build
```

-   Access the application at `http://localhost:3000`.
-   Access the API docs at `http://localhost:8000/docs`.

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

**Response:**

```json
{
  "prediction": {
    "label": "Trans-thalamic",
    "class_id": 2,
    "confidence": 0.95
  },
  "uncertainty": {
    "entropy": 0.12,
    "calibrated_confidence": 0.94
  },
  "explanation": {
    "heatmap_base64": "..."
  }
}
```

## Reproducibility

We prioritize reproducibility through:
-   Deterministic training and inference modes.
-   Pinned versions in `pyproject.toml` and `package-lock.json`.
-   Publicly available model weights (see Model Card).

## Limitations

-   **Domain Shift**: Models trained on specific datasets (e.g., US-13) may not generalize to machines from other vendors without fine-tuning.
-   **Performance**: CPU inference is optimized for accessibility, but high-throughput scenarios may require GPU acceleration.
-   **Ambiguity**: Fetal ultrasound images are inherently noisy; uncertainty estimates are crucial but not infallible.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## License

Distributed under the Apache License 2.0. See [LICENSE](LICENSE) for more information.

## Citation

If you use this repository in your research, please cite:

```bibtex
@misc{fetal_plane_explorer,
  author = {Laitinen, Olaf},
  title = {Fetal Plane Explorer: Standard Plane Classification with Uncertainty and XAI},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/olaflaitinen/fetal-plane-explorer}}
}
```
