import numpy as np
from typing import Any

def calculate_uncertainty(probabilities: list[float], temperature: float = 1.0) -> dict[str, float]:
    """
    Calculate uncertainty metrics from probabilities.
    Includes entropy and calibrated confidence (conceptually).
    """
    probs = np.array(probabilities)
    
    # Predictive Entropy: -sum(p * log(p))
    # Add epsilon to avoid log(0)
    epsilon = 1e-10
    entropy = -np.sum(probs * np.log(probs + epsilon))
    
    # Max Probability (Confidence)
    confidence = np.max(probs)
    
    # Temperature scaling is usually applied to logits BEFORE softmax.
    # Here we assume probabilities are already post-temperature if handled in model, 
    # or we report the raw max prob as "calibrated_confidence" if the model is calibrated.
    # For MVP, we pass through.
    
    return {
        "entropy": float(entropy),
        "calibrated_confidence": float(confidence)
    }

def apply_temperature_scaling(logits: list[float], temperature: float) -> list[float]:
    """
    Apply temperature scaling to logits and return new probabilities.
    """
    logits_arr = np.array(logits) / temperature
    exp_logits = np.exp(logits_arr - np.max(logits_arr))
    probs = exp_logits / np.sum(exp_logits)
    return probs.tolist()
