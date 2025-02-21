import gdown
import zipfile
import os

# Google Drive File ID (Replace with yours)
FILE_ID = "1BV-HLBtKluSgiwpPbAxv6Zh1lCAsZ1XO"
OUTPUT_ZIP = "dataset.zip"
EXTRACT_DIR = "/home/circleci/datasets/dataset"

# Ensure the dataset directory exists
os.makedirs(EXTRACT_DIR, exist_ok=True)

# Download dataset
print("📥 Downloading dataset from Google Drive...")
gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", OUTPUT_ZIP, quiet=False)

# Extract dataset
print("📂 Extracting dataset...")
with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

# Remove zip file
os.remove(OUTPUT_ZIP)

print(f"✅ Dataset downloaded and extracted successfully to {EXTRACT_DIR}")
