import sys
import os
from flask import Flask, render_template, request, redirect, url_for
import cv2
import torch
from PIL import Image
import numpy as np

# Ensure YOLOv5 is accessible
sys.path.append(os.path.join(os.getcwd(), "yolov5"))

from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression

app = Flask(__name__)

# Ensure CPU usage
device = torch.device("cpu")

# Load YOLOv5 model
model_path = "/home/john/waste_detection/waste_detection/exp/weights/best.pt"
model = attempt_load(model_path, device)  # ✅ Fixed map_location issue
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

        # Load and preprocess image
        img = Image.open(file_path).convert("RGB")
        img = img.resize((640, 640))  # Resize to match YOLOv5 expected input size
        img = np.array(img)

        # Convert to tensor and normalize
        img_tensor = torch.from_numpy(img).float().to(device)
        img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0) / 255.0

        if img_tensor.shape[1] != 3:  # Ensure 3 color channels (RGB)
            img_tensor = img_tensor.expand(1, 3, img_tensor.shape[2], img_tensor.shape[3])

        print(f"Input Tensor Shape: {img_tensor.shape}")  # Debugging print

        with torch.no_grad():
            results = model(img_tensor)

        # Process results
        results = non_max_suppression(results, 0.4, 0.5)[0]  # Apply NMS

        # Draw bounding boxes
        for det in results:
            x1, y1, x2, y2, conf, cls = det.tolist()
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, f"{cls} {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save detected image
        output_path = f"static/detected_{file.filename}"
        cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

        return render_template("result.html", image_path=output_path)

if __name__ == "__main__":
    app.run(debug=True)
