import torch
import torchvision.models as models
import torch.nn as nn
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_demo_model():
    """
    Downloads a pretrained ResNet18 (ImageNet), modifies the final layer for 8 classes,
    and exports it to ONNX. This allows the system to run 'real' inference
    (mathematically correct) even if medically random without real training data.
    """
    output_dir = "assets/models"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fetal_plane_resnet18.onnx")

    logger.info("Downloading ResNet18...")
    # Use weights=None to perform a "cold start" or defaults if desired
    # For a demo that "works", verified weights are better, but we need 8 classes.
    # We will load default weights then replace the head.
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

    # Modify the fully connected layer for 8 classes (Fetal Planes)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 8)

    # Set to eval mode
    model.eval()

    # Create dummy input for ONNX export (Batch Size 1, 3 Channels, 224x224)
    dummy_input = torch.randn(1, 3, 224, 224)

    logger.info(f"Exporting to ONNX at {output_path}...")
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
        opset_version=12
    )

    logger.info("✅ ONNX model generated successfully. Real inference is now possible.")

if __name__ == "__main__":
    setup_demo_model()
