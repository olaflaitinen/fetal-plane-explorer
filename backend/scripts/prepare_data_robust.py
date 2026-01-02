"""
Robust Data Preparation Script for Fetal Plane Classification.
Ensures:
1. Correct class mapping from original labels.
2. Patient-level stratified split (no data leakage - same patient cannot be in train AND val).
3. Reproducible random seed.
"""
import os
import pandas as pd
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from collections import defaultdict

# Paths
CSV_PATH = "assets/datasets/raw/FETAL_PLANES_DB_data.csv"
IMAGES_DIR = Path("assets/datasets/raw/Images")
OUTPUT_DIR = Path("assets/datasets")

# Reproducibility
RANDOM_SEED = 42
VAL_SPLIT = 0.2  # 20% validation

# Class Mapping from original dataset labels to our schema
CLASS_MAP = {
    "Fetal brain": "Brain",
    "Fetal thorax": "Thorax",
    "Fetal abdomen": "Abdominal",
    "Fetal femur": "Femur",
    "Maternal cervix": "Cervix",
    "Other": "Other"
}

def prepare_data():
    print("=" * 50)
    print("ROBUST DATA PREPARATION")
    print("=" * 50)

    # Load CSV
    df = pd.read_csv(CSV_PATH, sep=';')
    df.columns = [c.strip() for c in df.columns]
    print(f"Loaded {len(df)} records from CSV.")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nOriginal Class Distribution:")
    print(df['Plane'].value_counts())

    # Verify images exist
    missing = 0
    valid_records = []
    for _, row in df.iterrows():
        img_name = row['Image_name']
        # Try both png and jpg
        img_path = IMAGES_DIR / f"{img_name}.png"
        if not img_path.exists():
            img_path = IMAGES_DIR / f"{img_name}.jpg"
        if img_path.exists():
            valid_records.append({
                'image_path': img_path,
                'patient_id': row['Patient_num'],
                'original_class': row['Plane'],
                'mapped_class': CLASS_MAP.get(row['Plane'], 'Other')
            })
        else:
            missing += 1

    print(f"\nValid images: {len(valid_records)}, Missing: {missing}")

    # Convert to DataFrame for easier manipulation
    records_df = pd.DataFrame(valid_records)

    # CRITICAL: Patient-level split to prevent data leakage
    # Group images by patient
    patient_ids = records_df['patient_id'].unique()
    print(f"\nUnique patients: {len(patient_ids)}")

    # Stratified split by patient (approximate stratification by dominant class per patient)
    patient_class = records_df.groupby('patient_id')['mapped_class'].agg(lambda x: x.mode()[0]).reset_index()
    patient_class.columns = ['patient_id', 'dominant_class']

    train_patients, val_patients = train_test_split(
        patient_class['patient_id'].values,
        test_size=VAL_SPLIT,
        random_state=RANDOM_SEED,
        stratify=patient_class['dominant_class'].values
    )

    print(f"Train patients: {len(train_patients)}, Val patients: {len(val_patients)}")

    # Assign splits
    records_df['split'] = records_df['patient_id'].apply(
        lambda x: 'train' if x in train_patients else 'val'
    )

    # Create output directories
    for split in ['train', 'val']:
        for cls in CLASS_MAP.values():
            os.makedirs(OUTPUT_DIR / split / cls, exist_ok=True)

    # Copy files
    print("\nCopying files...")
    counts = defaultdict(lambda: defaultdict(int))

    for _, row in records_df.iterrows():
        src = row['image_path']
        split = row['split']
        cls = row['mapped_class']
        dst = OUTPUT_DIR / split / cls / src.name

        shutil.copy(src, dst)
        counts[split][cls] += 1

    # Summary
    print("\n" + "=" * 50)
    print("FINAL DISTRIBUTION (No Data Leakage)")
    print("=" * 50)

    for split in ['train', 'val']:
        print(f"\n{split.upper()}:")
        total = 0
        for cls in sorted(counts[split].keys()):
            print(f"  {cls}: {counts[split][cls]}")
            total += counts[split][cls]
        print(f"  TOTAL: {total}")

    # Verification
    train_pids = set(train_patients)
    val_pids = set(val_patients)
    overlap = train_pids.intersection(val_pids)
    print(f"\nData Leakage Check: Patient overlap = {len(overlap)} (should be 0)")

    if len(overlap) == 0:
        print("SUCCESS: No data leakage detected.")
    else:
        print("WARNING: Data leakage detected!")

if __name__ == "__main__":
    prepare_data()
