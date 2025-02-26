import gdown
import zipfile
import os

FILE_ID = "1j4aV5SU5jRFsHHz3bSgJSN-16o1rIjy8"
OUTPUT_ZIP = "dataset.zip"
OUTPUT_FOLDER = "dataset"

# Download dataset
print("📥 Downloading dataset...")
gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", OUTPUT_ZIP, quiet=False)

# Check if file exists
if not os.path.exists(OUTPUT_ZIP):
    raise FileNotFoundError(f"❌ Download failed! {OUTPUT_ZIP} not found.")

# Extract dataset
print("📂 Extracting dataset...")
try:
    with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
        zip_ref.extractall(OUTPUT_FOLDER)
except zipfile.BadZipFile:
    raise ValueError("❌ The downloaded ZIP file is corrupted!")

# Remove zip file
os.remove(OUTPUT_ZIP)

print("✅ Dataset downloaded and extracted successfully.")
