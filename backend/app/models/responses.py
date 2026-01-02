from pydantic import BaseModel, Field

class PredictionResult(BaseModel):
    label: str
    class_id: int
    confidence: float

class UncertaintyMetrics(BaseModel):
    predictive_entropy: float = Field(..., description="Entropy of the predictive distribution")
    calibrated_confidence: float = Field(..., description="Calibrated top-1 confidence")

class ExplanationArtifacts(BaseModel):
    heatmap_base64: str | None = None
    overlay_base64: str | None = None

class PredictionResponse(BaseModel):
    prediction: PredictionResult
    uncertainty: UncertaintyMetrics
    explanation: ExplanationArtifacts
