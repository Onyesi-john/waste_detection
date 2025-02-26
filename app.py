import sys
import os
from flask import Flask, render_template, request, redirect, url_for
import cv2
import torch
from PIL import Image
import numpy as np

# Ensure YOLOv5 is accessible
sys.path.append(os.path.join(os.getcwd(), "yolov5"))

from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

app = Flask(__name__)

# Ensure CPU usage
device = torch.device("cpu")

# Load YOLOv5 model
model_path = "/home/john/waste_detection/waste_detection/exp/weights/best.pt"
model = attempt_load(model_path, map_location=device)
model.eval()


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
        file_path = f"static/{file.filename}"
        file.save(file_path)  # Save the uploaded image

        img = Image.open(file_path)
        img = np.array(img)

        # Convert to tensor and run inference
        img_tensor = torch.from_numpy(img).float().to(device)
        img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0) / 255.0  # Normalize and reshape

        with torch.no_grad():
            results = model(img_tensor)

        # Process results
        results = non_max_suppression(results, 0.4, 0.5)[0]  # Apply NMS

        # Draw bounding boxes
        for det in results:
            x1, y1, x2, y2, conf, cls = det.tolist()
            plot_one_box([x1, y1, x2, y2], img, label=f"{cls} {conf:.2f}")

        # Save detected image
        output_path = f"static/detected_{file.filename}"
        cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

        return render_template("result.html", image_path=output_path)


@app.route("/webcam")
def webcam():
    return render_template("webcam.html")


@app.route("/predict", methods=["POST"])
def predict():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        return "Failed to capture image"

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Convert image for model input
    img_tensor = torch.from_numpy(np.array(img)).float().to(device)
    img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0) / 255.0

    with torch.no_grad():
        results = model(img_tensor)

    results = non_max_suppression(results, 0.4, 0.5)[0]

    for det in results:
        x1, y1, x2, y2, conf, cls = det.tolist()
        plot_one_box([x1, y1, x2, y2], frame, label=f"{cls} {conf:.2f}")

    cap.release()

    output_path = "static/webcam_output.jpg"
    cv2.imwrite(output_path, frame)

    return render_template("result.html", image_path=output_path)


if __name__ == "__main__":
    app.run(debug=True)
