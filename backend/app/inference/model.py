import numpy as np
import logging
import os
import onnxruntime as ort
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class ModelWrapper:
    def __init__(self, model_path: str):
        self.classes = [
            "Abdominal", "Brain", "Cervix", "Femur", "Other", "Thorax"
        ]
        self.model_path = model_path
        self.session = None
        self.load_model()

    def load_model(self):
        """Loads the ONNX model."""
        if not os.path.exists(self.model_path):
            logger.critical(f"Model file not found at {self.model_path}")
            # In production, we might want to crash or raise Error,
            # but for now we log critical.
            self.session = None
            return

        try:
            self.session = ort.InferenceSession(self.model_path)
            logger.info(f"ONNX model loaded successfully from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {e}")
            self.session = None

    def predict(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Runs inference on the input image.
        Args:
            image: Preprocessed image (Batch, C, H, W)
        Returns:
            Dict containing probabilities and class predictions.
        """
        if self.session is None:
            raise RuntimeError("Model is not loaded.")

        input_name = self.session.get_inputs()[0].name
        # ONNX Runtime expects numpy input
        outputs = self.session.run(None, {input_name: image})
        logits = outputs[0]

        # Softmax
        exp_preds = np.exp(logits)
        probs = exp_preds / np.sum(exp_preds, axis=1, keepdims=True)
        probs = probs[0] # First sample

        # Get top class
        class_idx = np.argmax(probs)
        class_name = self.classes[class_idx]
        confidence = float(probs[class_idx])

        return {
            "class": class_name,
            "class_id": int(class_idx),
            "confidence": confidence,
            "probabilities": {cls: float(comp) for cls, comp in zip(self.classes, probs)}
        }

# Global model instance
model_engine = ModelWrapper(model_path=settings.MODEL_PATH)
