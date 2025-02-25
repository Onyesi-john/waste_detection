import sys, os, subprocess
from waste_detection.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin
from waste_detection.constant.application import APP_HOST, APP_PORT

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "/app/inputImage.jpg"  # Ensure correct path inside Docker
        self.model_path = "/app/yolov5nu/best.pt"  # Model location in Docker

clApp = ClientApp()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST', 'GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json.get('image')
        if not image:
            return Response("❌ No image provided!", status=400)
        
        decodeImage(image, clApp.filename)

        # Run YOLO detection using subprocess
        yolo_command = [
            "python", "yolov5nu/detect.py",
            "--weights", clApp.model_path,
            "--img", "416",
            "--conf", "0.5",
            "--source", clApp.filename
        ]

        result = subprocess.run(yolo_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return Response(f"❌ YOLOv5 Error:\n{result.stderr}", status=500)

        processed_image_path = "yolov5nu/runs/detect/exp/inputImage.jpg"
        if not os.path.exists(processed_image_path):
            return Response("❌ Processed image not found!", status=500)

        opencodedbase64 = encodeImageIntoBase64(processed_image_path)
        result = {"image": opencodedbase64.decode('utf-8')}

        # Only remove files inside the runs directory, don't delete everything
        subprocess.run(["rm", "-rf", "yolov5nu/runs/detect/exp"], check=True)

    except KeyError:
        return Response("❌ Key error: Incorrect key passed", status=400)
    except Exception as e:
        return Response(f"❌ Unexpected Error: {str(e)}", status=500)

    return jsonify(result)

@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        subprocess.run([
            "python", "yolov5nu/detect.py",
            "--weights", clApp.model_path,
            "--img", "416",
            "--conf", "0.5",
            "--source", "0"
        ], check=True)

        subprocess.run(["rm", "-rf", "yolov5nu/runs/detect/exp"], check=True)

        return "✅ Camera detection started!"

    except Exception as e:
        return Response(f"❌ Error starting webcam: {str(e)}", status=500)

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
