import gdown
import zipfile
import os
import shutil

# Google Drive File ID (Replace with yours)
FILE_ID = "1BV-HLBtKluSgiwpPbAxv6Zh1lCAsZ1XO"
OUTPUT_ZIP = "dataset.zip"

# Define dataset path
EXTRACT_PATH = "/home/circleci/datasets/dataset"

try:
    # Ensure the directory exists
    os.makedirs(EXTRACT_PATH, exist_ok=True)
    print(f"✅ Directory '{EXTRACT_PATH}' created or already exists.")

    # Download dataset
    print("⏳ Downloading dataset...")
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", OUTPUT_ZIP, quiet=False)
    print(f"✅ Dataset downloaded as '{OUTPUT_ZIP}'.")

    # Extract dataset to the correct path
    print("⏳ Extracting dataset...")
    with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_PATH)
    print(f"✅ Dataset extracted to '{EXTRACT_PATH}'.")

    # Remove zip file
    os.remove(OUTPUT_ZIP)
    print(f"✅ Removed '{OUTPUT_ZIP}'.")

    # Verify extraction
    if os.path.exists(EXTRACT_PATH) and os.listdir(EXTRACT_PATH):
        print(f"✅ Dataset verified in '{EXTRACT_PATH}'.")
    else:
        raise FileNotFoundError(f"❌ Dataset extraction failed. No files found in '{EXTRACT_PATH}'.")

except Exception as e:
    print(f"❌ An error occurred: {e}")
    # Clean up in case of failure
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)
    if os.path.exists(EXTRACT_PATH):
        shutil.rmtree(EXTRACT_PATH)
    exit(1)