import os
import requests
import zipfile
import pandas as pd
import shutil
from pathlib import Path
from tqdm import tqdm

DATASET_URL = "https://zenodo.org/record/3904280/files/FETAL_PLANES_ZENODO.zip?download=1"
ZIP_PATH = "assets/datasets/FETAL_PLANES_ZENODO.zip"
EXTRACT_PATH = "assets/datasets/raw"
FINAL_PATH = "assets/datasets"

def download_file(url, filename):
    print(f"Downloading {url} to {filename}...")
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024 * 1024 # 1MB
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    print("Download complete.")

def organize_dataset():
    print("Organizing dataset...")

    # Locate the CSV
    # Structure usually: raw/FETAL_PLANES_ZENODO/FETAL_PLANES_DB_data.csv
    # and raw/FETAL_PLANES_ZENODO/Images/

    base_dir = Path(EXTRACT_PATH) / "FETAL_PLANES_ZENODO"
    csv_path = base_dir / "FETAL_PLANES_DB_data.csv"
    images_dir = base_dir / "Images"

    if not csv_path.exists():
        # Try finding it recursively
        csv_files = list(Path(EXTRACT_PATH).rglob("*.csv"))
        if csv_files:
            csv_path = csv_files[0]
            base_dir = csv_path.parent
            images_dir = base_dir / "Images"
        else:
            print("Error: Could not find dataset CSV.")
            return

    print(f"Found CSV at {csv_path}")
    df = pd.read_csv(csv_path, sep=';') # Commonly ; separated

    # Check separator
    if len(df.columns) < 3:
        df = pd.read_csv(csv_path, sep=',')

    print(f"Loaded {len(df)} records.")

    # Map classes
    # Dataset classes: 'Abdomen', 'Brain (Cerebellum)', 'Brain (Choroid Plexus)', 'Brain (Other)', 'Brain (Thalamic)', 'Cervix', 'Femur', 'Thorax', 'Other'
    # Our classes: "Trans-thalamic", "Trans-cerebellar", "Trans-ventricular", "Abdominal", "Femur", "Thorax", "Spine", "Other"

    # Mapping
    # Brain (Thalamic) -> Trans-thalamic
    # Brain (Cerebellum) -> Trans-cerebellar
    # Brain (Choroid Plexus) -> Trans-ventricular (approx)
    # Abdomen -> Abdominal
    # Femur -> Femur
    # Thorax -> Thorax
    # Cervix -> Other (or exclude)
    # Other -> Other

    class_map = {
        'Brain (Thalamic)': 'Trans-thalamic',
        'Brain (Cerebellum)': 'Trans-cerebellar',
        'Brain (Choroid Plexus)': 'Trans-ventricular', # Proxy
        'Abdomen': 'Abdominal',
        'Femur': 'Femur',
        'Thorax': 'Thorax',
        'Other': 'Other',
        'Cervix': 'Other'
    }

    for phase in ['train', 'val']:
        os.makedirs(f"{FINAL_PATH}/{phase}", exist_ok=True)
        for cls in set(class_map.values()):
            os.makedirs(f"{FINAL_PATH}/{phase}/{cls}", exist_ok=True)

    # Split (Train/Test is typically in column 'Train ' (0/1) check columns)
    # Columns usually: Image_name, Plane, Train

    print("Columns:", df.columns)

    # Normalize col names
    df.columns = [c.strip() for c in df.columns]

    count = 0
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        img_name = row.get('Image_name')
        plane = row.get('Plane')
        is_train = row.get('Train', 1) # Default to train if missing

        if plane not in class_map:
            target_class = 'Other'
        else:
            target_class = class_map[plane]

        src = images_dir / f"{img_name}.png" # Usually png
        if not src.exists():
            src = images_dir / f"{img_name}.jpg"

        if not src.exists():
            continue

        phase = 'train' if is_train == 1 else 'val'
        dst = Path(FINAL_PATH) / phase / target_class / src.name

        shutil.copy(src, dst)
        count += 1

    print(f"Processed {count} images.")

def main():
    os.makedirs("assets/datasets", exist_ok=True)

    if not os.path.exists(ZIP_PATH):
        download_file(DATASET_URL, ZIP_PATH)
    else:
        print("Zip already exists.")

    if not os.path.exists(EXTRACT_PATH):
        print("Extracting...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)

    organize_dataset()

if __name__ == "__main__":
    main()
