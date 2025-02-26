from flask import Flask, render_template, request, redirect, url_for
import cv2
import torch
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load your YOLOv5NU model
model_path = ' /home/john/waste_detection/waste_detection/exp/weights/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, device='cpu')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        img = Image.open(file.stream)
        results = model(img)
        results.save()  # Save predictions
        return redirect(url_for('home'))

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/predict', methods=['POST'])
def predict():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        return 'Failed to capture image'
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    results = model(img)
    results.save()  # Save predictions
    cap.release()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)