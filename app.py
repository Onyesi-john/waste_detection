from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import torch
import threading
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model
MODEL_PATH = "/app/best.pt"  # Update this for Docker compatibility
model = YOLO(MODEL_PATH)

# Create folders
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

# Allowed file types for uploads
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 🖼️ Upload & Process Image
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return "❌ No file uploaded!"
        if not allowed_file(file.filename):
            return "❌ Invalid file type! Upload PNG, JPG, or JPEG only."

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Run YOLO detection
        results = model(filepath)

        # Save processed image
        results[0].save(save_dir=PROCESSED_FOLDER)  

        return redirect(url_for("view_image", filename=file.filename))

    return render_template("index.html")


# 📸 View Processed Image
@app.route("/processed/<filename>")
def view_image(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)


# 🎥 Webcam Detection
def detect_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame)
        frame = results[0].plot()

        cv2.imshow("YOLO Real-Time Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# 🔗 Start Webcam Detection (Background Thread)
@app.route("/start_webcam")
def start_webcam():
    thread = threading.Thread(target=detect_webcam)
    thread.start()
    return "Webcam detection started!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
