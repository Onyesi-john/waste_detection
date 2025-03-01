import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np

app = Flask(__name__)

# Path to trained YOLOv5 model
MODEL_PATH = "best.pt"

# Load YOLOv5 model using ultralytics
model = YOLO(MODEL_PATH)

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
        results[0].save(output_path)  # Save the first result (single image)

        # Ensure correct path for HTML
        output_web_path = f"{DETECTED_FOLDER}/{output_filename}"

        return render_template("result.html", image_path=output_web_path)

@app.route("/webcam")
def webcam():
    return render_template("webcam.html")

@app.route("/detect_webcam", methods=["POST"])
def detect_webcam():
    # Get the image data from the request
    image_data = request.files["image"].read()
    image_np = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Run YOLOv5 detection
    results = model(image)

    # Save the detected image
    output_path = os.path.join(DETECTED_FOLDER, "webcam_detection.jpg")
    results[0].save(output_path)

    # Return the path to the detected image
    return jsonify({"image_path": f"{DETECTED_FOLDER}/webcam_detection.jpg"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)