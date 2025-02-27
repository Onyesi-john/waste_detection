from ultralytics import YOLO

# Load the model
model = YOLO("yolov5nu.pt")

# Train the model
model.train(
    data="/home/john/waste_detection/dataset/data.yaml",  # Update this path
    epochs=50,
    batch=8,
    imgsz=416,
    
)