import gdown
import zipfile
import os

# Google Drive File ID (Replace with yours)
FILE_ID = "1-3KPCCqF2kjNElo9f9L6QwricRqe0PKq"
OUTPUT_ZIP = "dataset.zip"

# Download dataset
print("Downloading dataset...")
try:
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", OUTPUT_ZIP, quiet=False)
except Exception as e:
    print(f"❌ Failed to download dataset: {e}")
    print("Please ensure the file is publicly accessible or download it manually.")
    exit(1)

# Extract dataset
print("Extracting dataset...")
try:
    with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
        zip_ref.extractall("dataset")
    print("✅ Dataset extracted successfully.")
except Exception as e:
    print(f"❌ Failed to extract dataset: {e}")
    exit(1)

# Remove zip file
try:
    os.remove(OUTPUT_ZIP)
    print("✅ Zip file removed successfully.")
except Exception as e:
    print(f"❌ Failed to remove zip file: {e}")

print("✅ Dataset downloaded and extracted successfully.")