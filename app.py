import torch
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import os  # Import the os module

app = Flask(__name__)

# Load your custom YOLOv5nu model using torch.hub
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/john/waste_detection/runs/detect/train/weights/best.pt', force_reload=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file temporarily
    temp_path = "/tmp/uploaded_image.jpg"
    file.save(temp_path)

    # Verify the file exists
    if not os.path.exists(temp_path):
        return jsonify({"error": "File could not be saved"}), 500

    # Perform object detection
    results = model(temp_path)

    # Extract detection results
    detections = []
    for *xyxy, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, xyxy)
        confidence = float(conf)
        label = model.names[int(cls)]
        detections.append({
            "label": label,
            "confidence": confidence,
            "bbox": [x1, y1, x2, y2]
        })

    # Clean up the temporary file
    os.remove(temp_path)

    return jsonify(detections)

if __name__ == '__main__':
    app.run(debug=True)