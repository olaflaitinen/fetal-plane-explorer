from PIL import Image
import io
import numpy as np

def load_image(file_bytes: bytes) -> Image.Image:
    """Load bytes into PIL Image and convert to RGB."""
    bg_image = Image.open(io.BytesIO(file_bytes))
    if bg_image.mode != "RGB":
        bg_image = bg_image.convert("RGB")
    return bg_image

def preprocess_for_model(image: Image.Image) -> np.ndarray:
    """Resize and normalize image for model inference."""
    # MVP: Resize to 224x224 and scale to 0-1
    img = image.resize((224, 224))
    img_arr = np.array(img).astype(np.float32) / 255.0
    # HWC -> CHW/Batch
    # img_arr = np.transpose(img_arr, (2, 0, 1))
    # img_arr = np.expand_dims(img_arr, axis=0) # Batch dim
    # Keeping it simple for MVP Dummy model which expects nothing specific yet
    return img_arr
