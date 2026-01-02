# Architecture

## Component Diagram

```mermaid
graph TD
    Client[Web Client (Vite/TS)] -->|HTTP/REST| API[FastAPI Gateway]
    API -->|Preprocess| Pre[Preprocessing]
    Pre -->|Tensor| Model[ONNX Runtime Model]
    Model -->|Logits| Post[Postprocessing]
    Model -->|Gradients| XAI[Grad-CAM Engine]
    
    subgraph Backend
        API
        Pre
        Model
        XAI
        Post
        Uncertainty[Uncertainty Estimator]
        Post --> Uncertainty
    end
    
    XAI -->|Heatmap| API
    Post -->|Probabilities| API
    Uncertainty -->|Entropy/Confidence| API
```

## Data Flow

1.  **User Upload**: User uploads an image via the Frontend.
2.  **API Ingestion**: `POST /v1/predict` receives the file.
3.  **Preprocessing**:
    -   Image is decoded.
    -   Converted to Grayscale or RGB (configurable).
    -   Resized to 224x224.
    -   Normalized (e.g., ImageNet stats).
4.  **Inference**:
    -   ONNX Runtime session runs the model.
    -   Outputs: Logits, and optionally intermediate feature maps.
5.  **Uncertainty Estimation**:
    -   Sort logits to get top-k.
    -   Calculate Predictive Entropy.
    -   Apply Temperature Scaling (if calibrated) for confidence score.
6.  **Explanation Generation (XAI)**:
    -   Compute gradients of the target class w.r.t final convolutional layer.
    -   Generate Grid-CAM heatmap.
    -   Overlay heatmap on original image.
7.  **Response**: JSON payload with Prediction, Uncertainty metrics, and Base64 encoded Heatmap is sent back.
8.  **Rendering**: Frontend displays the label, confidence bars, and interactive overlay.

## Threat Model (High Level)

### Assets
-   **Model Weights**: Intellectual property (though open sourced here).
-   **User Data**: Ultrasound images (potentially sensitive if used clinically, though heavily discouraged).
-   **Availability**: The service itself.

### Risks & Mitigations

| Risk | Mitigation |
|Data Leakage| Images are processed in-memory and not persisted to disk. Logging is structured and redacted.|
|Malicious Input| Input validation (file type, size limits) in FastAPI. Library hardening (Pillow/OpenCV safety).|
|Model Theft| Rate limiting (optional integration). Public release mitigates motive.|
|Adversarial Attacks| Input preprocessing normalization. Uncertainty thresholds to reject anomalous inputs.|
|Usage Misinterpretation| Clear UI disclaimers. "Confidence" metrics to warn users of low certainty.|
