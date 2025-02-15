from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import torch
from ultralytics import YOLO

app = Flask(__name__)

# Load trained YOLO model
MODEL_PATH = "/home/john/runs/detect/train3/weights/best.pt"
model = YOLO(MODEL_PATH)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER


# 🖼️ Route for Image Upload & Detection
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Run YOLO model on the image
        results = model(filepath)

        # Save processed image
        processed_path = os.path.join(app.config["PROCESSED_FOLDER"], file.filename)
        results[0].save(processed_path)

        return redirect(url_for("view_image", filename=file.filename))

    return render_template("index.html")


# 📸 Route to View Processed Image
@app.route("/processed/<filename>")
def view_image(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)


# 🎥 Route for Live Webcam Detection
@app.route("/webcam")
def webcam():
    return render_template("webcam.html")


# 🎥 Start Real-Time Webcam Detection
def detect_webcam():
    cap = cv2.VideoCapture(0)  # Use the first webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO detection
        results = model(frame)

        # Draw detections on the frame
        frame = results[0].plot()

        cv2.imshow("YOLO Real-Time Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# 🔗 Start Webcam Detection Route
@app.route("/start_webcam")
def start_webcam():
    detect_webcam()
    return "Webcam detection stopped."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
