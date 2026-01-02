"""Convert PyTorch .pth model to ONNX format for inference."""
import torch
from torchvision import models
import torch.nn as nn
import argparse

IMG_SIZE = 224
NUM_CLASSES = 6

def convert_to_onnx(pth_path: str, onnx_path: str):
    # Load MobileNetV3-Small architecture
    model = models.mobilenet_v3_small(weights=None)
    num_ftrs = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(num_ftrs, NUM_CLASSES)

    # Load trained weights
    model.load_state_dict(torch.load(pth_path, map_location='cpu', weights_only=True))
    model.eval()

    # Export to ONNX
    dummy_input = torch.randn(1, 3, IMG_SIZE, IMG_SIZE)
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
        opset_version=14
    )
    print(f"ONNX model exported to {onnx_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pth", type=str, default="assets/models/fetal_plane_mobilenetv3.pth")
    parser.add_argument("--onnx", type=str, default="assets/models/fetal_plane_mobilenetv3.onnx")
    args = parser.parse_args()
    convert_to_onnx(args.pth, args.onnx)
