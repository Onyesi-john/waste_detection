import gdown
import zipfile
import os

# Google Drive File ID (Replace with yours)
FILE_ID = "1mrujZFCNXstsKdO6gZ7XyTPTIP6ZqYjW"
OUTPUT_ZIP = "dataset.zip"

# Define dataset path within your project
EXTRACT_PATH = os.path.join(os.getcwd(), "dataset")

# Ensure the directory exists
os.makedirs(EXTRACT_PATH, exist_ok=True)

# Download dataset
gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", OUTPUT_ZIP, quiet=False)

# Extract dataset to the correct path
with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
    zip_ref.extractall(EXTRACT_PATH)

# Remove zip file
os.remove(OUTPUT_ZIP)

print(f"✅ Dataset downloaded and extracted to {EXTRACT_PATH} successfully.")
