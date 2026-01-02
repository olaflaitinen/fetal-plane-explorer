export interface PredictionResult {
    label: string;
    class_id: number;
    confidence: number;
}

export interface UncertaintyMetrics {
    predictive_entropy: number;
    calibrated_confidence: number;
}

export interface ExplanationArtifacts {
    heatmap_base64?: string;
    overlay_base64?: string;
}

export interface PredictionResponse {
    prediction: PredictionResult;
    uncertainty: UncertaintyMetrics;
    explanation: ExplanationArtifacts;
    originalImage?: string; // Client-side enhancement
}

export async function predict(file: File): Promise<PredictionResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/v1/predict", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error(`Prediction failed: ${response.statusText}`);
    }

    return response.json();
}
