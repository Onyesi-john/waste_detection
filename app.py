import os
from flask import Flask, render_template, request, redirect, url_for
import torch
from pathlib import Path

app = Flask(__name__)

# Path to trained YOLOv5 model
MODEL_PATH = "yolov5/runs/train/exp/weights/best.pt"

# Load YOLOv5 model from yolov5 directory
model = torch.hub.load("ultralytics/yolov5", "custom", path=MODEL_PATH, force_reload=True)
model.eval()

# Define folders
UPLOAD_FOLDER = "static/uploads"
DETECTED_FOLDER = "static/detected"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)

    if file:
        # Save uploaded image
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Run YOLOv5 detection
        results = model(file_path)

        # Save detected image in `static/detected/`
        output_filename = f"detected_{file.filename}"
        output_path = os.path.join(DETECTED_FOLDER, output_filename)
        results.save(Path(DETECTED_FOLDER))  # Saves detection results in the folder

        # Ensure correct path for HTML
        output_web_path = f"{DETECTED_FOLDER}/{output_filename}"

        return render_template("result.html", image_path=output_web_path)

if __name__ == "__main__":
    app.run(debug=True)
