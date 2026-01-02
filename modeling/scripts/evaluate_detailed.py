import torch
import torch.nn as nn
from torchvision import transforms, models
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Configuration (Must match training)
IMG_SIZE = 224
BATCH_SIZE = 32
CLASSES = [
    "Abdominal", "Brain", "Cervix", "Femur", "Other", "Thorax"
]

class FetalUltrasoundDataset(Dataset):
    def __init__(self, root_dir, phase='val', transform=None):
        self.root_dir = os.path.join(root_dir, phase)
        self.transform = transform
        self.classes = CLASSES
        self.image_paths = []
        self.labels = []

        if not os.path.exists(self.root_dir):
            print(f"Warning: Directory {self.root_dir} not found.")
            return

        for idx, class_name in enumerate(self.classes):
            class_dir = os.path.join(self.root_dir, class_name)
            if os.path.isdir(class_dir):
                for fname in os.listdir(class_dir):
                    if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.image_paths.append(os.path.join(class_dir, fname))
                        self.labels.append(idx)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

def evaluate_model(model_path, data_dir):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load Model Strategy
    # We used MobileNetV3-Small in the optimized run
    print("Loading architecture: MobileNetV3-Small")
    model = models.mobilenet_v3_small(weights=None)
    num_ftrs = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(num_ftrs, len(CLASSES))

    # Load Weights
    print(f"Loading weights from {model_path}...")
    if not os.path.exists(model_path):
        print("Error: Model file not found. Has training finished?")
        return

    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model = model.to(device)
    model.eval()

    # Data Loader
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_dataset = FetalUltrasoundDataset(data_dir, phase='val', transform=transform)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    print(f"Evaluating on {len(val_dataset)} images...")

    all_preds = []
    all_labels = []

    # Inference Loop
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    # Metrics
    acc = accuracy_score(all_labels, all_preds)
    f1_macro = f1_score(all_labels, all_preds, average='macro')
    f1_weighted = f1_score(all_labels, all_preds, average='weighted')

    print("\n" + "="*40)
    print("DETAILED RESULTS")
    print("="*40)
    print(f"Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    print(f"F1 Score (Macro): {f1_macro:.4f}")
    print(f"F1 Score (Weighted): {f1_weighted:.4f}")

    print("\nClassification Report:")
    print("-" * 60)
    print(classification_report(all_labels, all_preds, target_names=CLASSES))
    print("-" * 60)

    # Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASSES, yticklabels=CLASSES)
    plt.title(f'Confusion Matrix (Acc: {acc:.2f})')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')

    cm_path = "assets/evaluation_confusion_matrix.png"
    plt.tight_layout()
    plt.savefig(cm_path)
    print(f"\nConfusion matrix saved to {cm_path}")

    # Summary JSON for UI/Artifacts
    metrics = {
        "accuracy": acc,
        "f1_macro": f1_macro,
        "model_architecture": "MobileNetV3-Small",
        "parameters": "1.5M",
        "dataset_size_val": len(val_dataset)
    }

    with open("assets/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    # Note: train.py saves to this path by legacy default, even for mobilenet
    MODEL_PATH = "assets/models/fetal_plane_resnet18.pth"
    DATA_DIR = "assets/datasets"
    evaluate_model(MODEL_PATH, DATA_DIR)
