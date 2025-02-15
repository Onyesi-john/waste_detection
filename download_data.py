import gdown
import zipfile
import os

# Google Drive File ID (Replace with yours)
FILE_ID = "1BV-HLBtKluSgiwpPbAxv6Zh1lCAsZ1XO"
OUTPUT_ZIP = "dataset.zip"

# Download dataset
gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", OUTPUT_ZIP, quiet=False)

# Extract dataset
with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
    zip_ref.extractall("dataset")

# Remove zip file
os.remove(OUTPUT_ZIP)

print("✅ Dataset downloaded and extracted successfully.")
