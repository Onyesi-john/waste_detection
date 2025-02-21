from ultralytics import YOLO

# Load a smaller model (YOLOv5n instead of YOLOv8)
model = YOLO("yolov5nu.pt")  # Use YOLOv5 Nano model

# Train the model with fewer epochs
model.train(
    data="dataset/data.yaml",  
    epochs=15,  
    imgsz=416,  
    batch=8,  
    workers=2  
)
