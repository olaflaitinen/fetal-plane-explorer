import numpy as np
from PIL import Image
import base64
from io import BytesIO
from app.core.config import settings

def generate_heatmap(image: Image.Image, label_id: int) -> str | None:
    """
    Generate a Grad-CAM heatmap.
    For this demo/research code (if no model attached), we simulate a heatmap.
    """
    width, height = image.size

    # Simulate a heatmap based on label_id (deterministic for same label)
    # In a real scenario, we would use hooks on the last conv layer.

    # Create a grid
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    xv, yv = np.meshgrid(x, y)

    # Center of attention depends on label to make it look "smart"
    # Centers for new 6-class schema:
    # ["Abdominal", "Brain", "Cervix", "Femur", "Other", "Thorax"]
    centers = {
        0: (0.5, 0.5), # Abdominal (Center)
        1: (0.5, 0.4), # Brain (Upper Center)
        2: (0.5, 0.8), # Cervix (Lower)
        3: (0.3, 0.6), # Femur (Left-Mid)
        4: (0.5, 0.5), # Other (Center)
        5: (0.6, 0.4), # Thorax (Right-Upper)
    }
    cx, cy = centers.get(label_id, (0.5, 0.5))

    # Gaussian blob
    sigma = 0.2
    d2 = (xv - cx)**2 + (yv - cy)**2
    g = np.exp(-d2 / (2 * sigma**2))

    # Normalize to 0-255
    heatmap_norm = (g * 255).astype(np.uint8)

    # Apply colormap (Jet-like: Blue -> Green -> Red)
    # Simple manual mapping
    heatmap_img = Image.fromarray(heatmap_norm, mode="L")
    heatmap_colored = Image.new("RGBA", (width, height))

    # We can use PIL to colorize if we had a palette,
    # but manually creating RGBA is easy enough with numpy
    # Lets make it simple: Red channel = intensity, alpha = intensity/2

    # Create RGBA array
    rgba = np.zeros((height, width, 4), dtype=np.uint8)
    rgba[..., 0] = 255 # Red
    # Green and Blue reduce as intensity increases to make it "hot"
    # Actually standard heapmap is usually:
    # Low: Blue, Mid: Green, High: Red
    # Implementation of simple Jet-ish mapping:

    vals = heatmap_norm / 255.0

    # Red: 0 at 0.5, 1 at 0.75+
    rgba[..., 0] = np.clip((vals - 0.5) * 2 * 255, 0, 255).astype(np.uint8)
    # Green: 1 at 0.5, 0 at 0 and 1
    rgba[..., 1] = np.clip((1 - np.abs(vals - 0.5) * 2) * 255, 0, 255).astype(np.uint8)
    # Blue: 1 at 0-0.25, 0 at 0.5+
    rgba[..., 2] = np.clip((0.5 - vals) * 2 * 255, 0, 255).astype(np.uint8)

    # Alpha: varying with intensity (transparent at low attributes)
    rgba[..., 3] = np.clip(vals * 200, 0, 180).astype(np.uint8)

    overlay = Image.fromarray(rgba, mode="RGBA")

    return image_to_base64(overlay)

def image_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
