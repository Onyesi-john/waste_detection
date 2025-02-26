from flask import Flask, render_template, request, redirect, url_for
import cv2
import torch
from PIL import Image
import numpy as np
from yolov5.models.experimental import attempt_load

app = Flask(__name__)

# Correct model path
model_path = '/home/john/waste_detection/waste_detection/exp/weights/best.pt'

# Ensure CPU usage
device = torch.device("cpu")  
model = attempt_load(model_path, map_location=device)  # Load trained model to CPU
model.eval()  # Set model to evaluation mode

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
        file_path = f"static/{file.filename}"
        file.save(file_path)  # Save the uploaded image
        img = Image.open(file_path)
        results = model(img)  # Run inference
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
    results = model(img)  # Run inference
    results.save()  # Save predictions
    cap.release()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
