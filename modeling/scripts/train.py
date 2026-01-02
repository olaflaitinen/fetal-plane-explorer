import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import os
from PIL import Image
import time
import copy

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 64
NUM_EPOCHS = 2
LEARNING_RATE = 0.001
CLASSES = [
    "Abdominal", "Brain", "Cervix", "Femur", "Other", "Thorax"
]

class FetalUltrasoundDataset(Dataset):
    """
    Custom Dataset for Fetal Plane Classification.
    Expected structure:
    data_dir/
        train/
            Trans-thalamic/
            ...
        val/
            ...
    """
    def __init__(self, root_dir, phase='train', transform=None):
        self.root_dir = os.path.join(root_dir, phase)
        self.transform = transform
        self.classes = CLASSES
        self.image_paths = []
        self.labels = []

        if not os.path.exists(self.root_dir):
            print(f"Warning: Directory {self.root_dir} not found. Creating placeholder.")
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

def train_model(data_dir, output_dir):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data augmentation and normalization
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(IMG_SIZE),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(IMG_SIZE),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    image_datasets = {x: FetalUltrasoundDataset(data_dir, x, data_transforms[x]) for x in ['train', 'val']}

    # Check if data exists
    if len(image_datasets['train']) == 0:
        print("No training data found. Please populate assets/datasets/train with class folders.")
        print(f"Expected classes: {CLASSES}")
        return

    dataloaders = {x: DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
                   for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

    # Load pretrained MobileNetV3-Small (approx 2.5M params)
    print("Loading MobileNetV3-Small (Optimized for CPU)...")
    model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)

    # Modify classifier head
    # MobileNetV3 classifier is a Sequential block. Last layer is '3'.
    num_ftrs = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(num_ftrs, len(CLASSES))

    model = model.to(device)

    # Calculate and print parameter count
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Model: MobileNetV3-Small | Total Parameters: {total_params:,} (~2.5M) | Trainable: {trainable_params:,}")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    print("Starting training...")
    for epoch in range(NUM_EPOCHS):
        print(f'Epoch {epoch}/{NUM_EPOCHS - 1}')
        print('-' * 10)

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

    print(f'Best val Acc: {best_acc:4f}')

    # Save model
    model.load_state_dict(best_model_wts)
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, 'fetal_plane_mobilenetv3.pth')
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

    # Export to ONNX
    try:
        dummy_input = torch.randn(1, 3, IMG_SIZE, IMG_SIZE, device=device)
        onnx_path = os.path.join(output_dir, 'fetal_plane_mobilenetv3.onnx')
        torch.onnx.export(model, dummy_input, onnx_path, verbose=False, input_names=['input'], output_names=['output'])
        print(f"ONNX model exported to {onnx_path}")
    except Exception as e:
        print(f"Warning: ONNX export failed: {e}")
        print("Model .pth file is safe. You can likely use the PyTorch model directly.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="assets/datasets", help="Path to dataset")
    parser.add_argument("--output_dir", type=str, default="assets/models", help="output directory")
    args = parser.parse_args()

    train_model(args.data_dir, args.output_dir)
